
import React from 'react';
import type { SplitOptions } from '../types';
import Button from './Button';

interface SettingsPanelProps {
    splitOptions: SplitOptions;
    setSplitOptions: (options: SplitOptions) => void;
    onReAtomize: () => void;
}

const SettingsPanel: React.FC<SettingsPanelProps> = ({ splitOptions, setSplitOptions, onReAtomize }) => {
    
    const handleOptionChange = <K extends keyof SplitOptions,>(field: K, value: SplitOptions[K]) => {
        setSplitOptions({ ...splitOptions, [field]: value });
    };

    return (
        <div className="bg-gray-800 border border-gray-700 rounded-lg p-4 h-full">
            <h3 className="text-lg font-semibold text-white mb-4">Splitting Adjustments</h3>
            <div className="space-y-4">
                <div>
                    <label htmlFor="minLen" className="block text-sm font-medium text-gray-400">Min Words: {splitOptions.minLen}</label>
                    <input
                        type="range"
                        id="minLen"
                        min="50"
                        max="200"
                        step="10"
                        value={splitOptions.minLen}
                        onChange={(e) => handleOptionChange('minLen', Number(e.target.value))}
                        className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
                    />
                </div>
                <div>
                    <label htmlFor="maxLen" className="block text-sm font-medium text-gray-400">Max Words: {splitOptions.maxLen}</label>
                    <input
                        type="range"
                        id="maxLen"
                        min="200"
                        max="500"
                        step="10"
                        value={splitOptions.maxLen}
                        onChange={(e) => handleOptionChange('maxLen', Number(e.target.value))}
                        className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
                    />
                </div>
                 <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-400">Split by Headings (#)</span>
                     <label htmlFor="useHeadings" className="relative inline-flex items-center cursor-pointer">
                        <input type="checkbox" id="useHeadings" className="sr-only peer" checked={splitOptions.useHeadings} onChange={(e) => handleOptionChange('useHeadings', e.target.checked)} />
                        <div className="w-11 h-6 bg-gray-600 rounded-full peer peer-focus:ring-4 peer-focus:ring-blue-800 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                    </label>
                </div>
                <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-400">Split by Timestamps</span>
                    <label htmlFor="useTimestamps" className="relative inline-flex items-center cursor-pointer">
                        <input type="checkbox" id="useTimestamps" className="sr-only peer" checked={splitOptions.useTimestamps} onChange={(e) => handleOptionChange('useTimestamps', e.target.checked)} />
                        <div className="w-11 h-6 bg-gray-600 rounded-full peer peer-focus:ring-4 peer-focus:ring-blue-800 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                    </label>
                </div>
                <Button onClick={onReAtomize} className="w-full">
                    Re-Atomize
                </Button>
            </div>
        </div>
    );
};

export default SettingsPanel;
