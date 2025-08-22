
import React, { useState } from 'react';
import type { TaxonomyCapsule } from '../types';
import Modal from './Modal';
import Button from './Button';

interface TaxonomyModalProps {
    taxonomy: TaxonomyCapsule;
    onSave: (taxonomy: TaxonomyCapsule) => void;
    onClose: () => void;
}

const TaxonomyModal: React.FC<TaxonomyModalProps> = ({ taxonomy, onSave, onClose }) => {
    const [currentTaxonomy, setCurrentTaxonomy] = useState<TaxonomyCapsule>(taxonomy);

    const handleSave = () => {
        onSave({
            ...currentTaxonomy,
            // Clean up text area inputs into arrays
            baseTags: Array.isArray(currentTaxonomy.baseTags) ? currentTaxonomy.baseTags : (currentTaxonomy.baseTags as string).split(',').map(t => t.trim()).filter(Boolean),
            stopwords: Array.isArray(currentTaxonomy.stopwords) ? currentTaxonomy.stopwords : (currentTaxonomy.stopwords as string).split(',').map(t => t.trim()).filter(Boolean),
        });
    };
    
    const footer = (
        <div className="space-x-2">
            <Button variant="secondary" onClick={onClose}>Cancel</Button>
            <Button onClick={handleSave}>Save Capsule</Button>
        </div>
    );

    return (
        <Modal title="Taxonomy Capsule" onClose={onClose} footer={footer}>
            <div className="space-y-4 max-h-[60vh] overflow-y-auto custom-scrollbar pr-2">
                 <div>
                    <label htmlFor="baseTags" className="block text-sm font-medium text-gray-300">Base Tags</label>
                    <textarea
                        id="baseTags"
                        rows={2}
                        value={Array.isArray(currentTaxonomy.baseTags) ? currentTaxonomy.baseTags.join(', ') : currentTaxonomy.baseTags}
                        onChange={(e) => setCurrentTaxonomy(prev => ({...prev, baseTags: e.target.value.split(',').map(t => t.trim())}))}
                        className="mt-1 block w-full bg-gray-700 border-gray-600 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 custom-scrollbar"
                        placeholder="e.g. research, d.IA.logo, inbox"
                    />
                    <p className="mt-1 text-xs text-gray-400">Comma-separated tags to add to every new note.</p>
                </div>
                 <div>
                    <label htmlFor="stopwords" className="block text-sm font-medium text-gray-300">Stopwords</label>
                    <textarea
                        id="stopwords"
                        rows={4}
                        value={Array.isArray(currentTaxonomy.stopwords) ? currentTaxonomy.stopwords.join(', ') : currentTaxonomy.stopwords}
                        onChange={(e) => setCurrentTaxonomy(prev => ({...prev, stopwords: e.target.value.split(',').map(t => t.trim())}))}
                        className="mt-1 block w-full bg-gray-700 border-gray-600 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 custom-scrollbar"
                        placeholder="e.g. de, da, do, para, com"
                    />
                    <p className="mt-1 text-xs text-gray-400">Common words to ignore when generating titles and keywords.</p>
                </div>
                 {/* A simple synonym editor could be added here in the future */}
            </div>
        </Modal>
    );
};

export default TaxonomyModal;
