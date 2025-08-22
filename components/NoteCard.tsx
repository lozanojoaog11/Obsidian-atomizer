
import React, { useState } from 'react';
import type { Note } from '../types';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface NoteCardProps {
    note: Note;
    allNotes: Note[]; // Keep for context if needed later
    updateNote: (note: Note) => void;
}

const NoteCard: React.FC<NoteCardProps> = ({ note, updateNote }) => {
    const [isEditing, setIsEditing] = useState(false);
    const [editedContent, setEditedContent] = useState(note.content);

    const handleSave = () => {
        // A simple heuristic to update title from content
        const newTitleMatch = editedContent.match(/^#\s+(.*)/);
        const newTitle = newTitleMatch ? newTitleMatch[1] : note.title;
        updateNote({ ...note, content: editedContent, title: newTitle });
        setIsEditing(false);
    };
    
    const handleCancel = () => {
        setEditedContent(note.content);
        setIsEditing(false);
    }

    return (
        <div className="bg-gray-800 border border-gray-700 rounded-lg transition-shadow hover:shadow-lg hover:border-blue-500/50">
            <div className="p-4 border-b border-gray-700 flex justify-between items-center">
                <h3 className="text-lg font-semibold text-white truncate" title={note.title}>{note.title}</h3>
                <div className="flex space-x-2 flex-shrink-0 ml-4">
                    {isEditing ? (
                        <>
                           <button onClick={handleSave} className="text-xs px-2 py-1 rounded bg-green-600 hover:bg-green-700 text-white font-semibold">Save</button>
                           <button onClick={handleCancel} className="text-xs px-2 py-1 rounded bg-gray-600 hover:bg-gray-700 text-white">Cancel</button>
                        </>
                    ) : (
                        <button onClick={() => setIsEditing(true)} className="text-xs px-2 py-1 rounded bg-blue-600 hover:bg-blue-700 text-white font-semibold">Edit</button>
                    )}
                </div>
            </div>
            
            <div className="p-4">
                {isEditing ? (
                     <textarea
                        value={editedContent}
                        onChange={(e) => setEditedContent(e.target.value)}
                        className="w-full h-96 bg-gray-900 border border-gray-600 rounded-md p-2 text-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none custom-scrollbar font-mono text-sm"
                        aria-label={`Edit content for note ${note.title}`}
                    />
                ) : (
                    <div className="prose prose-invert prose-sm max-w-none prose-pre:bg-gray-900 prose-pre:rounded-md prose-pre:p-3 custom-scrollbar max-h-96 overflow-y-auto">
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                            {note.content}
                        </ReactMarkdown>
                    </div>
                )}
            </div>
        </div>
    );
};

export default NoteCard;
