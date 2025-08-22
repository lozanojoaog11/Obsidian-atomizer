
import React, { useCallback } from 'react';
import Button from './Button';

interface InputSectionProps {
    inputText: string;
    setInputText: (text: string) => void;
    projectName: string;
    setProjectName: (name: string) => void;
    onAtomize: () => void;
}

const InputSection: React.FC<InputSectionProps> = ({ inputText, setInputText, projectName, setProjectName, onAtomize }) => {

    const handleFileDrop = useCallback((event: React.DragEvent<HTMLDivElement>) => {
        event.preventDefault();
        event.stopPropagation();
        const file = event.dataTransfer.files[0];
        if (file) {
            readFile(file);
        }
    }, []);

    const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            readFile(file);
        }
    };

    const readFile = (file: File) => {
        setProjectName(file.name.split('.').slice(0, -1).join('.'));
        const reader = new FileReader();
        reader.onload = (e) => {
            const text = e.target?.result as string;
            setInputText(text);
        };
        reader.readAsText(file);
    };

    const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
        event.preventDefault();
        event.stopPropagation();
    };

    return (
        <div className="flex-grow flex flex-col space-y-6">
            <div className="text-center">
                <h2 className="text-3xl font-bold text-white">From Raw Text to Atomic Notes</h2>
                <p className="mt-2 text-lg text-gray-400">Transform your content into a linked knowledge base with one click.</p>
            </div>

            <div 
                className="flex-grow flex flex-col p-4 border-2 border-dashed border-gray-600 rounded-lg hover:border-blue-500 transition-colors"
                onDrop={handleFileDrop}
                onDragOver={handleDragOver}
            >
                <textarea
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    placeholder="Paste your raw text here, or drop a .txt/.md file..."
                    className="flex-grow w-full bg-gray-800 border-none rounded-md p-4 text-gray-300 placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:outline-none resize-none custom-scrollbar"
                />
                 <div className="text-center mt-4 text-gray-500">
                    or
                    <label htmlFor="file-upload" className="ml-2 font-semibold text-blue-500 hover:text-blue-400 cursor-pointer">
                        Upload a file
                    </label>
                    <input id="file-upload" name="file-upload" type="file" className="sr-only" accept=".txt,.md" onChange={handleFileSelect}/>
                </div>
            </div>

            <div className="flex flex-col sm:flex-row items-center space-y-4 sm:space-y-0 sm:space-x-4">
                <input
                    type="text"
                    value={projectName}
                    onChange={(e) => setProjectName(e.target.value)}
                    placeholder="Enter project name (optional)"
                    className="w-full sm:flex-grow bg-gray-800 border border-gray-600 rounded-md py-2 px-4 text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
                <Button onClick={onAtomize} className="w-full sm:w-auto" disabled={!inputText.trim()}>
                    Atomize Text
                </Button>
            </div>
        </div>
    );
};

export default InputSection;
