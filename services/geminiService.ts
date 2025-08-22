
import { GoogleGenAI, Type } from "@google/genai";
import type { TaxonomyCapsule, NotePlanItem } from "../types";

class GeminiService {
    private ai: GoogleGenAI | null = null;
    
    private getAI() {
        // @ts-ignore
        const apiKey = process?.env?.API_KEY;
        if (!apiKey) {
            console.error("Gemini API key is not set.");
            return null;
        }
        if (!this.ai) {
             this.ai = new GoogleGenAI({ apiKey });
        }
        return this.ai;
    }

    public async planNoteStructure(
        fullText: string
    ): Promise<NotePlanItem[]> {
        const ai = this.getAI();
        if (!ai) {
           throw new Error("API client not initialized.");
        }

        const systemInstruction = `You are an expert in knowledge management and the Zettelkasten method. Your task is to analyze the provided text and create a structured plan for a network of atomic, interconnected notes for an Obsidian vault.
1.  Read the entire text to understand its core concepts, arguments, examples, and structure.
2.  Identify the main ideas that can be distilled into individual, self-contained "atomic" notes.
3.  For each identified idea, define a plan for a note. Each plan should include:
    - A concise, descriptive 'title'.
    - A 'concept' string, which is a 1-2 sentence instruction for a future AI writer, explaining what this specific note should contain and its purpose.
    - A 'relations' array, listing the exact titles of other notes it should link to.
4.  Ensure the notes are conceptually linked, forming a web of knowledge. A central note or Map of Content (MOC) is often a good starting point.
5.  The output must be a JSON object containing a single key "notes" which is an array of these note plans.`;

        const prompt = `Analyze the following text and generate the note-making plan.

TEXT:
---
${fullText.slice(0, 100000)}
---
`;

        try {
            const response = await ai.models.generateContent({
                model: "gemini-2.5-pro",
                contents: prompt,
                config: {
                    systemInstruction,
                    responseMimeType: "application/json",
                    responseSchema: {
                        type: Type.OBJECT,
                        properties: {
                            notes: {
                                type: Type.ARRAY,
                                description: "An array of planned notes, each with a title, concept, and relations.",
                                items: {
                                    type: Type.OBJECT,
                                    properties: {
                                        title: { type: Type.STRING, description: "The concise title of the note." },
                                        concept: { type: Type.STRING, description: "A 1-2 sentence summary of the note's purpose and content." },
                                        relations: {
                                            type: Type.ARRAY,
                                            description: "An array of exact titles of other notes it should link to.",
                                            items: { type: Type.STRING }
                                        }
                                    },
                                    required: ["title", "concept", "relations"]
                                }
                            }
                        },
                        required: ["notes"],
                    },
                    temperature: 0.3,
                }
            });

            const jsonText = response.text.trim();
            const parsed = JSON.parse(jsonText);
            return parsed.notes || [];

        } catch (error) {
            console.error("Error calling Gemini API for planning:", error);
            throw new Error("Failed to generate a note plan from the AI.");
        }
    }


    public async generateNoteContent(
        plan: NotePlanItem,
        fullText: string,
        taxonomy: TaxonomyCapsule
    ): Promise<string> {
        const ai = this.getAI();
        if (!ai) {
           throw new Error("API client not initialized.");
        }

        const systemInstruction = `You are a world-class knowledge synthesizer and an expert Obsidian user. Your task is to write the full markdown content for a single, atomic Zettelkasten note based on a plan and a source text.

**Formatting Rules:**
-   **YAML Frontmatter:** Start with a YAML block (---). Include 'tags' (using relevant tags from the provided list and generating new ones), 'created' (ISO date: ${new Date().toISOString()}), and 'status: ephemeral'.
-   **Rich Markdown:** Use headings (#, ##, ###), lists, bold, italics, and blockquotes to structure the content beautifully. The main title of the note should be a level 1 heading (#).
-   **Obsidian Callouts:** Enhance the note with Obsidian callouts like >[!info], >[!important], >[!quote], >[!example], >[!tip].
-   **Wikilinks:** Create internal links to related notes using the exact titles provided in the plan, formatted as [[Note Title]].
-   **Mermaid Diagrams:** If the concept involves a process, hierarchy, or relationship, generate a Mermaid diagram (e.g., mindmap, graph TD) to visualize it.
-   **Content:** The content must be derived from the provided source text, but synthesized and rephrased for clarity and atomicity. The note must be self-contained and understandable on its own.
-   **Tone:** Be insightful, clear, and structured.

**Base Tags to consider:** ${taxonomy.baseTags.join(', ')}
`;

        const prompt = `
Source Text (for context):
---
${fullText.slice(0, 100000)}
---

Note Generation Plan:
-   **Title:** "${plan.title}"
-   **Concept to write about:** "${plan.concept}"
-   **Link to these notes:** ${plan.relations.map(r => `[[${r}]]`).join(', ') || 'None'}

Now, generate the complete markdown for this single note, starting with the YAML frontmatter.
`;

        try {
            const response = await ai.models.generateContent({
                model: "gemini-2.5-flash",
                contents: prompt,
                config: {
                    systemInstruction,
                    temperature: 0.5,
                }
            });

            return response.text.trim();
        } catch (error) {
            console.error(`Error generating content for note "${plan.title}":`, error);
            return `# ${plan.title}\n\nError: AI failed to generate content for this note.`;
        }
    }
}

export const geminiService = new GeminiService();
