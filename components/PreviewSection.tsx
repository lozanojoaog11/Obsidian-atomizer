
import React from 'react';
import type { Note, SplitOptions } from '../types';
import NoteCard from './NoteCard';
import SettingsPanel from './SettingsPanel';
import Button from './Button';

interface PreviewSectionProps {
    notes: Note[];
    updateNote: (note: Note) => void;
    splitOptions: SplitOptions;
    setSplitOptions: (options: SplitOptions) => void;
    onReAtomize: () => void;
    onExport: () => void;
    onStartOver: () => void;
}

const PreviewSection: React.FC<PreviewSectionProps> = ({ notes, updateNote, splitOptions, setSplitOptions, onReAtomize, onExport, onStartOver }) => {
    return (
        <div className="flex-grow flex flex-col md:flex-row gap-6 h-full overflow-hidden">
            {/* Main Content: Notes List */}
            <div className="flex-grow md:w-2/3 flex flex-col">
                <div className="flex justify-between items-center mb-4">
                    <h2 className="text-2xl font-bold text-white">Notas Geradas ({notes.length})</h2>
                    <div className="flex space-x-2">
                       <Button onClick={onStartOver} variant="secondary">Começar de Novo</Button>
                       <Button onClick={onExport}>Exportar .zip</Button>
                    </div>
                </div>
                <div className="flex-grow overflow-y-auto space-y-4 pr-2 custom-scrollbar">
                    {notes.map(note => (
                        <NoteCard key={note.id} note={note} allNotes={notes} updateNote={updateNote} />
                    ))}
                </div>
            </div>

            {/* Right Sidebar: Settings Panel */}
            <div className="md:w-1/3 flex-shrink-0">
                <SettingsPanel 
                    splitOptions={splitOptions}
                    setSplitOptions={setSplitOptions}
                    onReAtomize={onReAtomize}
                />
            </div>
        </div>
    );
};

export default PreviewSection;
