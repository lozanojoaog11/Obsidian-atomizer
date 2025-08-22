
import React from 'react';
import type { HistoryItem } from '../types';
import Modal from './Modal';

interface HistoryModalProps {
    history: HistoryItem[];
    onClose: () => void;
}

const HistoryModal: React.FC<HistoryModalProps> = ({ history, onClose }) => {
    return (
        <Modal title="Project History" onClose={onClose}>
            <div className="mt-4 space-y-3 max-h-96 overflow-y-auto custom-scrollbar pr-2">
                {history.length === 0 ? (
                    <p className="text-gray-400 text-center">No projects in your history yet.</p>
                ) : (
                    history.map(item => (
                        <div key={item.id} className="bg-gray-700 p-3 rounded-lg flex justify-between items-center">
                            <div>
                                <p className="font-semibold text-white">{item.project}</p>
                                <p className="text-sm text-gray-400">{item.files} notes created</p>
                            </div>
                            <div className="text-right">
                                <p className="text-xs text-gray-400">{new Date(item.created).toLocaleDateString()}</p>
                                <p className="text-xs text-gray-400">{new Date(item.created).toLocaleTimeString()}</p>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </Modal>
    );
};

export default HistoryModal;
