
import React, { useEffect } from 'react';

interface ModalProps {
    title: string;
    children: React.ReactNode;
    onClose: () => void;
    footer?: React.ReactNode;
}

const Modal: React.FC<ModalProps> = ({ title, children, onClose, footer }) => {
    useEffect(() => {
        const handleEsc = (event: KeyboardEvent) => {
            if (event.key === 'Escape') {
                onClose();
            }
        };
        window.addEventListener('keydown', handleEsc);
        return () => window.removeEventListener('keydown', handleEsc);
    }, [onClose]);

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-75" aria-modal="true" role="dialog">
            <div 
                className="bg-gray-800 rounded-lg shadow-xl w-full max-w-lg mx-4 border border-gray-700 transform transition-all"
                onClick={(e) => e.stopPropagation()}
            >
                <div className="flex items-center justify-between p-4 border-b border-gray-700">
                    <h3 className="text-lg font-semibold text-white">{title}</h3>
                    <button onClick={onClose} className="text-gray-400 hover:text-white" aria-label="Close">
                        <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
                <div className="p-6 text-gray-300">
                    {children}
                </div>
                {footer && (
                    <div className="flex justify-end p-4 bg-gray-800 border-t border-gray-700 rounded-b-lg">
                        {footer}
                    </div>
                )}
            </div>
        </div>
    );
};

export default Modal;
