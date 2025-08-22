
import { APP_KEY } from '../constants';
import type { AppData, Settings, TaxonomyCapsule, HistoryItem } from '../types';

class StorageService {

    public loadData(): AppData | null {
        try {
            const rawData = localStorage.getItem(APP_KEY);
            if (rawData) {
                const parsedData = JSON.parse(rawData);
                // The root object is 'obsidianatomizer'
                return parsedData[APP_KEY] || null;
            }
            return null;
        } catch (error) {
            console.error("Failed to load data from localStorage", error);
            return null;
        }
    }

    public saveData(data: { [APP_KEY]: AppData }): void {
        try {
            localStorage.setItem(APP_KEY, JSON.stringify(data));
        } catch (error) {
            console.error("Failed to save data to localStorage", error);
        }
    }
    
    private getFullData(): { [APP_KEY]: AppData } | null {
        try {
            const raw = localStorage.getItem(APP_KEY);
            return raw ? JSON.parse(raw) : null;
        } catch {
            return null;
        }
    }

    public saveSettings(settings: Settings): void {
        const data = this.getFullData();
        if (data && data[APP_KEY]) {
            data[APP_KEY].config = settings;
            this.saveData(data);
        }
    }
    
    public saveTaxonomy(taxonomy: TaxonomyCapsule): void {
        const data = this.getFullData();
        if (data && data[APP_KEY]) {
            data[APP_KEY].capsule = taxonomy;
            this.saveData(data);
        }
    }

    public saveHistory(history: HistoryItem[]): void {
        const data = this.getFullData();
        if (data && data[APP_KEY]) {
            data[APP_KEY].history = history;
            this.saveData(data);
        }
    }
}

export const storageService = new StorageService();
