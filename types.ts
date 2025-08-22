
export interface Note {
    id: string;
    title: string;
    slug: string;
    content: string;
    summary: string;
    tags: string[];
    created: string;
    source: string;
    relations: string[]; // array of note slugs
}

export interface SplitOptions {
    minLen: number;
    maxLen: number;
    useHeadings: boolean;
    useTimestamps: boolean;
}

export interface Settings {
    apiMode: 'mock' | 'api';
    apiEndpoint: string;
    apiKey: string;
}

export interface TaxonomyCapsule {
    namespaces: string[];
    baseTags: string[];
    stopwords: string[];
    synonyms: { [key: string]: string[] };
}

export interface HistoryItem {
    id: string;
    project: string;
    files: number;
    created: string;
}

export interface AppData {
    capsule: TaxonomyCapsule;
    history: HistoryItem[];
    config: Settings;
}

export interface NotePlanItem {
    title: string;
    concept: string; 
    relations: string[];
}
