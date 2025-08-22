
import React, { useState, useEffect, useCallback } from 'react';
import type { Settings, TaxonomyCapsule, HistoryItem, Note, SplitOptions } from './types';
import { storageService } from './services/storageService';
import { atomizerService } from './services/atomizerService';
import { geminiService } from './services/geminiService';
import { DEFAULT_SETTINGS, DEFAULT_TAXONOMY, DEFAULT_SPLIT_OPTIONS, APP_KEY } from './constants';
import InputSection from './components/InputSection';
import PreviewSection from './components/PreviewSection';
import Header from './components/Header';
import SettingsModal from './components/SettingsModal';
import HistoryModal from './components/HistoryModal';
import TaxonomyModal from './components/TaxonomyModal';
import Toast from './components/Toast';

const App: React.FC = () => {
    const [settings, setSettings] = useState<Settings>(DEFAULT_SETTINGS);
    const [taxonomy, setTaxonomy] = useState<TaxonomyCapsule>(DEFAULT_TAXONOMY);
    const [history, setHistory] = useState<HistoryItem[]>([]);
    const [splitOptions, setSplitOptions] = useState<SplitOptions>(DEFAULT_SPLIT_OPTIONS);

    const [projectName, setProjectName] = useState<string>('');
    const [inputText, setInputText] = useState<string>('');
    const [notes, setNotes] = useState<Note[]>([]);
    
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [loadingMessage, setLoadingMessage] = useState<string>('Atomizing text...');
    const [currentView, setCurrentView] = useState<'input' | 'preview'>('input');

    const [isSettingsModalOpen, setIsSettingsModalOpen] = useState<boolean>(false);
    const [isHistoryModalOpen, setIsHistoryModalOpen] = useState<boolean>(false);
    const [isTaxonomyModalOpen, setIsTaxonomyModalOpen] = useState<boolean>(false);

    const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);

    useEffect(() => {
        const storedData = storageService.loadData();
        if (storedData) {
            setSettings(storedData.config || DEFAULT_SETTINGS);
            setTaxonomy(storedData.capsule || DEFAULT_TAXONOMY);
            setHistory(storedData.history || []);
            // @ts-ignore
            if (process && process.env) process.env.API_KEY = storedData.config?.apiKey || '';
        } else {
             // On first load, if there's no data, create the root key
            storageService.saveData({
                [APP_KEY]: {
                    capsule: DEFAULT_TAXONOMY,
                    history: [],
                    config: DEFAULT_SETTINGS,
                }
            });
        }
    }, []);

    const showToast = (message: string, type: 'success' | 'error') => {
        setToast({ message, type });
        setTimeout(() => setToast(null), 5000);
    };

    const handleSettingsSave = (newSettings: Settings) => {
        setSettings(newSettings);
        storageService.saveSettings(newSettings);
         // @ts-ignore
        if (process && process.env) process.env.API_KEY = newSettings.apiKey;
        showToast('Settings saved successfully!', 'success');
        setIsSettingsModalOpen(false);
    };
    
    const handleTaxonomySave = (newTaxonomy: TaxonomyCapsule) => {
        setTaxonomy(newTaxonomy);
        storageService.saveTaxonomy(newTaxonomy);
        showToast('Taxonomy capsule saved!', 'success');
        setIsTaxonomyModalOpen(false);
    };

    const handleAtomize = useCallback(async () => {
        if (!inputText.trim()) {
            showToast('Please enter some text to atomize.', 'error');
            return;
        }
        setIsLoading(true);
        
        try {
            let generatedNotes: Note[] = [];

            if (settings.apiMode === 'api' && settings.apiKey) {
                // New AI-powered workflow
                setLoadingMessage('Analyzing content and planning note structure...');
                const notePlan = await geminiService.planNoteStructure(inputText);

                if (!notePlan || notePlan.length === 0) {
                    throw new Error("The AI couldn't create a plan from the text. Try different content or check the API key.");
                }

                const allNoteTitles = notePlan.map(p => p.title);

                for (let i = 0; i < notePlan.length; i++) {
                    const planItem = notePlan[i];
                    setLoadingMessage(`Generating note ${i + 1} of ${notePlan.length}: "${planItem.title}"`);
                    
                    // Ensure relations are valid titles from the plan
                    const validRelations = planItem.relations.filter(r => allNoteTitles.includes(r));
                    
                    const noteContent = await geminiService.generateNoteContent(
                        { ...planItem, relations: validRelations },
                        inputText,
                        taxonomy
                    );
                    
                    const slug = atomizerService.slugify(planItem.title);
                    const summary = planItem.concept; // The plan's concept serves as a good summary
                    
                    generatedNotes.push({
                        id: `${Date.now()}-${i}`,
                        title: planItem.title,
                        slug: slug,
                        content: noteContent,
                        summary: summary,
                        tags: [...taxonomy.baseTags], // AI will add more in frontmatter
                        created: new Date().toISOString(),
                        source: projectName || 'pasted-ai',
                        relations: validRelations.map(r => atomizerService.slugify(r)),
                    });
                }
            } else {
                // Fallback to original local heuristic method
                setLoadingMessage('Splitting text into chunks...');
                const chunks = atomizerService.splitText(inputText, splitOptions);
                setLoadingMessage(`Generating titles for ${chunks.length} notes...`);

                let tempNotes: Note[] = chunks.map((chunk, index) => {
                    const title = atomizerService.generateTitle(chunk, taxonomy.stopwords);
                    const summary = atomizerService.generateSummary(chunk);
                    const created = new Date().toISOString();
                    const source = projectName || 'pasted-local';
                    return {
                        id: `${Date.now()}-${index}`,
                        title: title,
                        slug: atomizerService.slugify(title),
                        content: chunk,
                        summary: summary,
                        tags: [...taxonomy.baseTags],
                        created,
                        source,
                        relations: [],
                    };
                });
                setLoadingMessage('Suggesting backlinks...');
                generatedNotes = atomizerService.suggestBacklinks(tempNotes, 0.18);
            }
            
            setNotes(generatedNotes);
            setCurrentView('preview');

        } catch (error) {
            console.error("Atomization failed:", error);
            showToast(error instanceof Error ? error.message : 'An unknown error occurred during atomization.', 'error');
        } finally {
            setIsLoading(false);
        }
    }, [inputText, splitOptions, taxonomy, settings, projectName]);

    const handleExport = useCallback(async () => {
        if (notes.length === 0) {
            showToast('No notes to export.', 'error');
            return;
        }
        setIsLoading(true);
        setLoadingMessage('Generating MOC and preparing ZIP...');
        try {
            const finalProjectName = projectName || `Project-${new Date().toISOString().split('T')[0]}`;
            const mocContent = atomizerService.generateMoc(notes, finalProjectName);
            
            setLoadingMessage('Creating ZIP file...');
            await atomizerService.createZip(notes, mocContent, finalProjectName);

            const newHistoryItem: HistoryItem = {
                id: `hist-${Date.now()}`,
                project: finalProjectName,
                files: notes.length,
                created: new Date().toISOString(),
            };
            const updatedHistory = [newHistoryItem, ...history.slice(0, 4)];
            setHistory(updatedHistory);
            storageService.saveHistory(updatedHistory);

            showToast('ZIP file exported successfully!', 'success');
        } catch (error) {
            console.error("Export failed:", error);
            showToast(error instanceof Error ? error.message : 'Failed to create ZIP file.', 'error');
        } finally {
            setIsLoading(false);
        }
    }, [notes, projectName, history]);

    const updateNote = (updatedNote: Note) => {
        setNotes(prevNotes => prevNotes.map(note => note.id === updatedNote.id ? updatedNote : note));
    };

    const handleStartOver = () => {
        setInputText('');
        setNotes([]);
        setProjectName('');
        setCurrentView('input');
    };

    return (
        <div className="min-h-screen bg-gray-900 text-gray-300 font-sans flex flex-col custom-scrollbar">
            {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
            
            <Header
                onOpenSettings={() => setIsSettingsModalOpen(true)}
                onOpenHistory={() => setIsHistoryModalOpen(true)}
                onOpenTaxonomy={() => setIsTaxonomyModalOpen(true)}
            />

            <main className="flex-grow container mx-auto p-4 md:p-6 lg:p-8 flex flex-col">
                {isLoading ? (
                    <div className="flex-grow flex flex-col items-center justify-center">
                        <svg className="animate-spin h-12 w-12 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        <p className="mt-4 text-lg text-gray-400">{loadingMessage}</p>
                    </div>
                ) : currentView === 'input' ? (
                     <InputSection
                        inputText={inputText}
                        setInputText={setInputText}
                        projectName={projectName}
                        setProjectName={setProjectName}
                        onAtomize={handleAtomize}
                    />
                ) : (
                    <PreviewSection
                        notes={notes}
                        updateNote={updateNote}
                        splitOptions={splitOptions}
                        setSplitOptions={setSplitOptions}
                        onReAtomize={handleAtomize}
                        onExport={handleExport}
                        onStartOver={handleStartOver}
                    />
                )}
            </main>

            {isSettingsModalOpen && <SettingsModal settings={settings} onSave={handleSettingsSave} onClose={() => setIsSettingsModalOpen(false)} />}
            {isHistoryModalOpen && <HistoryModal history={history} onClose={() => setIsHistoryModalOpen(false)} />}
            {isTaxonomyModalOpen && <TaxonomyModal taxonomy={taxonomy} onSave={handleTaxonomySave} onClose={() => setIsTaxonomyModalOpen(false)} />}
        </div>
    );
};

export default App;
