
import type { Settings, TaxonomyCapsule, SplitOptions } from './types';

export const APP_KEY = 'obsidianatomizer';

export const DEFAULT_SETTINGS: Settings = {
    apiMode: 'mock',
    apiEndpoint: 'https://generativelanguage.googleapis.com',
    apiKey: '',
};

export const DEFAULT_TAXONOMY: TaxonomyCapsule = {
    namespaces: ["ai/negocios","educacao/ia","comunidade/processos"],
    baseTags: ["d.IA.logo","research"],
    stopwords: ["a", "o", "e", "de", "da", "do", "para", "com", "uma", "um", "é", "ser", "foi", "tá", "que", "em", "se", "os", "as", "ao", "na", "no", "mas", "por", "mais", "como", "eu", "ele", "ela", "nós"],
    synonyms: {
        "ia": ["inteligencia artificial", "ai"],
        "comunidade": ["grupo", "coorte"],
    },
};

export const DEFAULT_SPLIT_OPTIONS: SplitOptions = {
    minLen: 120,
    maxLen: 300,
    useHeadings: true,
    useTimestamps: false,
};
