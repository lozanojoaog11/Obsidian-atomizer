
import type { Note, SplitOptions } from '../types';

class AtomizerService {

    /**
     * Splits a large block of text into smaller, more manageable chunks based on specified options.
     * This is the first step in creating atomic notes.
     */
    public splitText(text: string, options: SplitOptions): string[] {
        // Normalize line endings and clean up multiple blank lines
        let normalizedText = text.replace(/\r\n/g, '\n').replace(/(\n\s*){3,}/g, '\n\n');
        
        let preliminaryChunks: string[] = [];
        const headingRegex = /^#{1,3}\s.*$/gm;
        const timestampRegex = /^\s*\[\d{1,2}:\d{2}(:\d{2})?\]\s*.*$/gm;

        let splitRegex: RegExp | null = null;
        if (options.useHeadings && normalizedText.match(headingRegex)) {
            splitRegex = /(?=^#{1,3}\s.*$)/m;
        } else if (options.useTimestamps && normalizedText.match(timestampRegex)) {
            splitRegex = /(?=\s*\[\d{1,2}:\d{2}(:\d{2})?\])/m;
        }

        if (splitRegex) {
            preliminaryChunks = normalizedText.split(splitRegex).filter(c => c.trim() !== '');
        } else {
            preliminaryChunks = normalizedText.split('\n\n').filter(p => p.trim() !== '');
        }

        const finalChunks: string[] = [];
        let currentChunk = '';

        for (const chunk of preliminaryChunks) {
            const chunkWordCount = this.wordCount(chunk);
            const currentWordCount = this.wordCount(currentChunk);

            if (currentChunk === '') {
                currentChunk = chunk;
            } else if (currentWordCount + chunkWordCount <= options.maxLen) {
                currentChunk += `\n\n${chunk}`;
            } else {
                if(currentWordCount >= options.minLen) {
                   finalChunks.push(currentChunk.trim());
                }
                currentChunk = chunk;
            }
        }
        if (currentChunk.trim() !== '' && this.wordCount(currentChunk) >= options.minLen) {
            finalChunks.push(currentChunk.trim());
        }

        return finalChunks.filter(c => c.length > 0);
    }

    /**
     * Generates a concise and relevant title for a chunk of text.
     * It prioritizes the first heading if present, otherwise uses n-grams.
     */
    public generateTitle(text: string, stopwords: string[]): string {
        const firstLine = text.split('\n')[0].trim();
        
        // Use heading as title if available
        const headingMatch = firstLine.match(/^#{1,3}\s+(.*)/);
        if (headingMatch && headingMatch[1]) {
            return this.capitalize(headingMatch[1].trim());
        }
        
        // Fallback to n-gram analysis on the first few sentences
        const sentenceEnd = /[.!?]/;
        const firstSentence = text.split(sentenceEnd)[0] || firstLine;

        const words = firstSentence.toLowerCase().replace(/[^\w\s]/g, '').split(/\s+/);
        const filteredWords = words.filter(w => w && !stopwords.includes(w)).slice(0, 10);
        
        if (filteredWords.length === 0) return "Untitled Note";

        // Simple heuristic: find the most "important" 3-5 words
        const titleWords = filteredWords.slice(0, 5);

        return this.capitalize(titleWords.join(' '));
    }
    
    public generateSummary(text: string): string {
        // A simple heuristic: take the first 1-2 sentences.
        const sentences = text.replace(/(\n)/g, " ").split(/[.!?]\s/).filter(s => s.trim().length > 10);
        if (sentences.length === 0) return text.slice(0, 150) + '...';
        let summary = sentences[0];
        if (sentences.length > 1 && (summary.length < 100)) {
            summary += `. ${sentences[1]}`;
        }
        return summary.slice(0, 250) + (summary.length > 250 ? '...' : '');
    }

    public slugify(text: string): string {
        return text
            .toLowerCase()
            .trim()
            .replace(/[^\w\s-]/g, '')
            .replace(/[\s_-]+/g, '-')
            .replace(/^-+|-+$/g, '');
    }

    /**
     * Suggests backlinks between notes using a lightweight TF-IDF and cosine similarity algorithm.
     */
    public suggestBacklinks(notes: Note[], similarityThreshold: number): Note[] {
        if (notes.length < 2) return notes;

        const stopwords = new Set(["a", "o", "e", "de", "da", "do", "para", "com", "uma", "um", "é", "ser", "foi"]);
        const documents = notes.map(note => note.content.toLowerCase().replace(/[^\w\s]/g, '').split(/\s+/).filter(w => !stopwords.has(w)));

        // Calculate IDF
        const idf: { [term: string]: number } = {};
        const allTerms = new Set(documents.flat());
        allTerms.forEach(term => {
            const docsWithTerm = documents.filter(doc => doc.includes(term)).length;
            idf[term] = Math.log(notes.length / (1 + docsWithTerm));
        });

        // Calculate TF-IDF vectors for each document
        const tfidfVectors = documents.map(doc => {
            const vector: { [term: string]: number } = {};
            const termCounts: { [term: string]: number } = {};
            doc.forEach(term => { termCounts[term] = (termCounts[term] || 0) + 1; });

            for (const term in termCounts) {
                const tf = termCounts[term] / doc.length;
                vector[term] = tf * (idf[term] || 0);
            }
            return vector;
        });
        
        const cosineSimilarity = (vecA: {[key:string]:number}, vecB: {[key:string]:number}) => {
            let dotProduct = 0;
            let magnitudeA = 0;
            let magnitudeB = 0;
            const allKeys = new Set([...Object.keys(vecA), ...Object.keys(vecB)]);
            
            allKeys.forEach(key => {
                const valA = vecA[key] || 0;
                const valB = vecB[key] || 0;
                dotProduct += valA * valB;
                magnitudeA += valA * valA;
                magnitudeB += valB * valB;
            });
            
            magnitudeA = Math.sqrt(magnitudeA);
            magnitudeB = Math.sqrt(magnitudeB);
            
            if (magnitudeA === 0 || magnitudeB === 0) return 0;
            return dotProduct / (magnitudeA * magnitudeB);
        };

        const notesWithRelations = [...notes];
        
        for (let i = 0; i < notes.length; i++) {
            const similarities: { slug: string; score: number }[] = [];
            for (let j = 0; j < notes.length; j++) {
                if (i === j) continue;
                const score = cosineSimilarity(tfidfVectors[i], tfidfVectors[j]);
                if (score > similarityThreshold) {
                    similarities.push({ slug: notes[j].slug, score });
                }
            }
            
            similarities.sort((a, b) => b.score - a.score);
            notesWithRelations[i].relations = similarities.slice(0, 3).map(s => s.slug);
        }
        
        return notesWithRelations;
    }

    /**
     * Generates the content for the Map of Content (MOC) file.
     */
    public generateMoc(notes: Note[], projectName: string): string {
        let content = `# MOC for ${projectName}\n\n`;
        content += `Generated on: ${new Date().toLocaleString()}\n`;
        content += `Total Notes: ${notes.length}\n\n---\n\n`;
        
        content += "## All Notes\n\n";
        notes.forEach(note => {
            content += `- [[${note.title}]]\n`;
        });
        
        return content;
    }

    /**
     * Creates a ZIP file in the browser containing all notes and the MOC without external libraries.
     */
    public async createZip(notes: Note[], mocContent: string, projectName: string) {
        const files = [];

        // Add MOC file
        files.push({
            name: `00_MOC_${this.slugify(projectName)}.md`,
            content: mocContent
        });
        
        // Add individual note files
        notes.forEach(note => {
            let fileContent = note.content;

            // Fallback: Add frontmatter if it doesn't exist
            if (!fileContent.trim().startsWith('---')) {
                const frontmatter = `---
title: "${note.title.replace(/"/g, '\\"')}"
summary: "${note.summary.replace(/"/g, '\\"')}"
tags: [${note.tags.join(', ')}]
created: ${note.created}
source: ${note.source}
relations: [${note.relations.map(r => `"${r}"`).join(', ')}]
---

`;
                fileContent = frontmatter + note.content;
            }
            
            // Add a "See Also" section if relations exist and section is missing
            const seeAlsoSection = note.relations.length > 0
                ? `\n\n---\n\n## See Also\n\n${note.relations.map(slug => {
                    const relatedNote = notes.find(n => n.slug === slug);
                    return `- [[${relatedNote?.title || slug}]]`;
                }).join('\n')}`
                : '';
            
            if (note.relations.length > 0 && !fileContent.includes('## See Also')) {
                fileContent += seeAlsoSection;
            }
            
            files.push({
                name: `notes/${note.slug}.md`,
                content: fileContent
            });
        });

        const zipBlob = await this.zipWriter(files);
        const url = URL.createObjectURL(zipBlob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${this.slugify(projectName)}.zip`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    // --- Private Helper Methods ---

    private wordCount(text: string): number {
        return text.trim().split(/\s+/).length;
    }

    private capitalize(s: string): string {
        if (!s) return '';
        return s.charAt(0).toUpperCase() + s.slice(1);
    }
    
    // Simple CRC32 implementation (needed for ZIP format)
    private crc32(buf: Uint8Array): number {
        let crc = -1;
        for (let i = 0; i < buf.length; i++) {
            crc = (crc >>> 8) ^ this.crc32Table[(crc ^ buf[i]) & 0xFF];
        }
        return (crc ^ -1) >>> 0;
    }

    private crc32Table = (() => {
        const table = new Uint32Array(256);
        for (let i = 0; i < 256; i++) {
            let c = i;
            for (let k = 0; k < 8; k++) {
                c = ((c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1));
            }
            table[i] = c;
        }
        return table;
    })();

    // No-compression ZIP file writer
    private async zipWriter(files: {name: string, content: string}[]): Promise<Blob> {
        const textEncoder = new TextEncoder();
        const buffers: ArrayBuffer[] = [];
        const centralDirectoryRecords: Uint8Array[] = [];
        let offset = 0;

        for (const file of files) {
            const nameBytes = textEncoder.encode(file.name);
            const contentBytes = textEncoder.encode(file.content);
            const crc = this.crc32(contentBytes);
            const lastModTime = new Date();

            // Local file header
            const header = new Uint8Array(30 + nameBytes.length);
            const view = new DataView(header.buffer);
            view.setUint32(0, 0x04034b50, true); // Signature
            view.setUint16(4, 10, true); // Version needed to extract
            view.setUint16(6, 0, true); // General purpose bit flag
            view.setUint16(8, 0, true); // Compression method (0=store)
            view.setUint16(10, (lastModTime.getHours() << 11) | (lastModTime.getMinutes() << 5) | (lastModTime.getSeconds() / 2), true); // Last mod time
            view.setUint16(12, ((lastModTime.getFullYear() - 1980) << 9) | ((lastModTime.getMonth() + 1) << 5) | lastModTime.getDate(), true); // Last mod date
            view.setUint32(14, crc, true); // CRC-32
            view.setUint32(18, contentBytes.length, true); // Compressed size
            view.setUint32(22, contentBytes.length, true); // Uncompressed size
            view.setUint16(26, nameBytes.length, true); // File name length
            view.setUint16(28, 0, true); // Extra field length
            header.set(nameBytes, 30);
            
            buffers.push(header.buffer, contentBytes.buffer);

            // Central directory file header
            const cdHeader = new Uint8Array(46 + nameBytes.length);
            const cdView = new DataView(cdHeader.buffer);
            cdView.setUint32(0, 0x02014b50, true); // Signature
            cdView.setUint16(4, 20, true); // Version made by
            //... copy from local header
            cdView.setUint16(6, 10, true);
            cdView.setUint16(8, 0, true);
            cdView.setUint16(10, 0, true);
            cdView.setUint16(12, view.getUint16(10, true), true); // time
            cdView.setUint16(14, view.getUint16(12, true), true); // date
            cdView.setUint32(16, crc, true);
            cdView.setUint32(20, contentBytes.length, true);
            cdView.setUint32(24, contentBytes.length, true);
            cdView.setUint16(28, nameBytes.length, true);
            cdView.setUint16(30, 0, true); // extra field length
            cdView.setUint16(32, 0, true); // file comment length
            cdView.setUint16(34, 0, true); // disk number start
            cdView.setUint16(36, 0, true); // internal file attributes
            cdView.setUint32(38, 0, true); // external file attributes
            cdView.setUint32(42, offset, true); // relative offset of local header
            cdHeader.set(nameBytes, 46);
            
            centralDirectoryRecords.push(cdHeader);
            offset += header.length + contentBytes.length;
        }

        let cdSize = 0;
        centralDirectoryRecords.forEach(r => cdSize += r.length);
        
        // End of central directory record
        const eocd = new Uint8Array(22);
        const eocdView = new DataView(eocd.buffer);
        eocdView.setUint32(0, 0x06054b50, true); // Signature
        eocdView.setUint16(4, 0, true); // number of this disk
        eocdView.setUint16(6, 0, true); // number of the disk with the start of the central directory
        eocdView.setUint16(8, files.length, true); // total number of entries in the central directory on this disk
        eocdView.setUint16(10, files.length, true); // total number of entries in the central directory
        eocdView.setUint32(12, cdSize, true); // size of the central directory
        eocdView.setUint32(16, offset, true); // offset of start of central directory
        eocdView.setUint16(20, 0, true); // .ZIP file comment length

        const finalBuffers = [...buffers];
        centralDirectoryRecords.forEach(r => finalBuffers.push(r.buffer));
        finalBuffers.push(eocd.buffer);

        return new Blob(finalBuffers, { type: 'application/zip' });
    }
}

// Export a singleton instance
export const atomizerService = new AtomizerService();
