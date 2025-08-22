
import React, { useState } from 'react';
import type { Settings } from '../types';
import Modal from './Modal';
import Button from './Button';

interface SettingsModalProps {
    settings: Settings;
    onSave: (settings: Settings) => void;
    onClose: () => void;
}

const SettingsModal: React.FC<SettingsModalProps> = ({ settings, onSave, onClose }) => {
    const [currentSettings, setCurrentSettings] = useState<Settings>(settings);

    const handleChange = <K extends keyof Settings,>(field: K, value: Settings[K]) => {
        setCurrentSettings(prev => ({ ...prev, [field]: value }));
    };

    const handleSave = () => {
        onSave(currentSettings);
    };

    const footer = (
        <div className="space-x-2">
            <Button variant="secondary" onClick={onClose}>Cancelar</Button>
            <Button onClick={handleSave}>Salvar Configurações</Button>
        </div>
    );

    return (
        <Modal title="Configurações" onClose={onClose} footer={footer}>
            <div className="space-y-4">
                <div>
                    <label htmlFor="apiMode" className="block text-sm font-medium text-gray-300">Modo de Aprimoramento com IA</label>
                    <select
                        id="apiMode"
                        value={currentSettings.apiMode}
                        onChange={(e) => handleChange('apiMode', e.target.value as 'mock' | 'api')}
                        className="mt-1 block w-full bg-gray-700 border-gray-600 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    >
                        <option value="mock">Apenas Heurísticas Locais</option>
                        <option value="api">Google Gemini API</option>
                    </select>
                     <p className="mt-2 text-xs text-gray-400">
                        Selecione 'Google Gemini API' para usar IA para melhores resumos e tags. Requer uma chave de API.
                    </p>
                </div>
                 {currentSettings.apiMode === 'api' && (
                    <div className="animate-fade-in">
                        <label htmlFor="apiKey" className="block text-sm font-medium text-gray-300">Chave de API do Google Gemini</label>
                        <input
                            type="password"
                            id="apiKey"
                            value={currentSettings.apiKey}
                            onChange={(e) => handleChange('apiKey', e.target.value)}
                            placeholder="Digite sua chave de API"
                            className="mt-1 block w-full bg-gray-700 border-gray-600 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        />
                    </div>
                 )}
            </div>
        </Modal>
    );
};

export default SettingsModal;
