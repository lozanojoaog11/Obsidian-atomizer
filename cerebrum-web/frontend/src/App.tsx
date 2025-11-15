/**
 * Cerebrum Web App - Beautiful & Minimal
 * Apple/Obsidian inspired design
 */

import { useState, useCallback } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { motion, AnimatePresence } from 'framer-motion';
import { useAppStore } from './store';
import { processFile } from './lib/api';
import { connectWebSocket, WSMessage } from './lib/websocket';

// Create QueryClient
const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-primary-900">
        <Header />
        <MainContent />
      </div>
    </QueryClientProvider>
  );
}

function Header() {
  return (
    <header className="glass border-b border-primary-600/30 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="text-3xl">🧠</div>
          <div>
            <h1 className="text-xl font-display font-semibold text-primary-100">
              Cerebrum
            </h1>
            <p className="text-xs text-primary-400">It just works, beautifully</p>
          </div>
        </div>
      </div>
    </header>
  );
}

function MainContent() {
  const { processingStatus, processingResult, reset } = useAppStore();

  return (
    <main className="max-w-5xl mx-auto px-6 py-12">
      <AnimatePresence mode="wait">
        {processingStatus === 'idle' && <UploadView key="upload" />}
        {processingStatus === 'processing' && <ProcessingView key="processing" />}
        {processingStatus === 'completed' && processingResult && (
          <ResultsView key="results" result={processingResult} onReset={reset} />
        )}
        {processingStatus === 'error' && <ErrorView key="error" onReset={reset} />}
      </AnimatePresence>
    </main>
  );
}

function UploadView() {
  const [isDragging, setIsDragging] = useState(false);
  const { setProcessing, setError } = useAppStore();

  const handleFile = useCallback(async (file: File) => {
    if (!file.name.endsWith('.pdf')) {
      setError('Only PDF files are supported');
      return;
    }

    try {
      // Upload file
      const { job_id } = await processFile(file);
      setProcessing(job_id);

      // Connect WebSocket for updates
      const ws = connectWebSocket(job_id, (message: WSMessage) => {
        if (message.type === 'progress') {
          useAppStore.getState().updateProgress(
            message.stage || 'processing',
            message.progress || 0
          );
        } else if (message.type === 'complete' && message.result) {
          useAppStore.getState().setCompleted(message.result);
          ws.close();
        } else if (message.type === 'error') {
          setError(message.error || 'Processing failed');
          ws.close();
        }
      });
    } catch (error: any) {
      setError(error.message || 'Failed to upload file');
    }
  }, [setProcessing, setError]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  }, [handleFile]);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  }, [handleFile]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="space-y-8"
    >
      {/* Hero */}
      <div className="text-center space-y-4">
        <h2 className="text-5xl font-display font-bold text-primary-100">
          Transform Knowledge
        </h2>
        <p className="text-lg text-primary-400">
          Drop a PDF, get atomic notes with semantic connections
        </p>
      </div>

      {/* Drop Zone */}
      <div
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        className={`drop-zone p-16 text-center cursor-pointer ${isDragging ? 'active' : ''}`}
        onClick={() => document.getElementById('file-input')?.click()}
      >
        <div className="space-y-4">
          <div className="text-6xl">📄</div>
          <div>
            <p className="text-xl font-medium text-primary-200">
              Drop PDF here
            </p>
            <p className="text-sm text-primary-400 mt-2">
              or click to browse
            </p>
          </div>
        </div>
        <input
          id="file-input"
          type="file"
          accept=".pdf"
          onChange={handleFileInput}
          className="hidden"
        />
      </div>
    </motion.div>
  );
}

function ProcessingView() {
  const { processingStage, processingProgress } = useAppStore();

  const stages = [
    { key: 'extraction', label: 'Extracting content', emoji: '📄' },
    { key: 'classification', label: 'Classifying content', emoji: '🏷️' },
    { key: 'destillation', label: 'Creating atomic notes', emoji: '⚗️' },
    { key: 'connection', label: 'Linking concepts', emoji: '🔗' },
    { key: 'moc', label: 'Building maps', emoji: '🗺️' },
    { key: 'save', label: 'Saving to vault', emoji: '💾' },
  ];

  const currentStageIndex = stages.findIndex(s => s.key === processingStage);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="space-y-8"
    >
      <div className="text-center space-y-4">
        <div className="text-6xl animate-pulse-glow">✨</div>
        <h2 className="text-3xl font-display font-semibold text-primary-100">
          Processing...
        </h2>
      </div>

      {/* Progress Bar */}
      <div className="card">
        <div className="h-2 bg-primary-700 rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-accent-purple"
            initial={{ width: 0 }}
            animate={{ width: `${processingProgress * 100}%` }}
            transition={{ duration: 0.3 }}
          />
        </div>
      </div>

      {/* Stages */}
      <div className="space-y-3">
        {stages.map((stage, index) => {
          const isActive = index === currentStageIndex;
          const isCompleted = index < currentStageIndex;

          return (
            <motion.div
              key={stage.key}
              className={`card flex items-center gap-4 ${
                isActive ? 'border-accent-purple' : ''
              }`}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <div className="text-2xl">{isCompleted ? '✓' : stage.emoji}</div>
              <div className="flex-1">
                <p className={`font-medium ${
                  isActive ? 'text-accent-purple' : 'text-primary-300'
                }`}>
                  {stage.label}
                </p>
              </div>
              {isActive && (
                <div className="w-2 h-2 bg-accent-purple rounded-full animate-pulse" />
              )}
            </motion.div>
          );
        })}
      </div>
    </motion.div>
  );
}

interface ResultsViewProps {
  result: any;
  onReset: () => void;
}

function ResultsView({ result, onReset }: ResultsViewProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      className="space-y-8"
    >
      {/* Success Header */}
      <div className="text-center space-y-4">
        <div className="text-6xl">✓</div>
        <h2 className="text-3xl font-display font-semibold text-primary-100">
          Done!
        </h2>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4">
        <StatCard
          label="Atomic Notes"
          value={result.permanent_notes.length}
          icon="📝"
        />
        <StatCard
          label="Connections"
          value={result.links_created}
          icon="🔗"
        />
        <StatCard
          label="MOCs"
          value={result.mocs_created.length + result.mocs_updated.length}
          icon="🗺️"
        />
        <StatCard
          label="Time"
          value={`${Math.round(result.duration_seconds)}s`}
          icon="⏱️"
        />
      </div>

      {/* Notes List */}
      {result.permanent_notes.length > 0 && (
        <div className="card space-y-4">
          <h3 className="text-lg font-display font-semibold text-primary-100">
            📝 Permanent Notes
          </h3>
          <div className="space-y-2">
            {result.permanent_notes.slice(0, 8).map((note: any) => (
              <div
                key={note.id}
                className="p-3 bg-primary-700 rounded-apple-sm hover:bg-primary-600 transition-colors"
              >
                <p className="text-sm font-medium text-primary-200">{note.title}</p>
                {note.domain && (
                  <p className="text-xs text-primary-400 mt-1">{note.domain}</p>
                )}
              </div>
            ))}
            {result.permanent_notes.length > 8 && (
              <p className="text-sm text-primary-400 text-center pt-2">
                + {result.permanent_notes.length - 8} more
              </p>
            )}
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-4">
        <button onClick={onReset} className="btn-primary flex-1">
          Process Another
        </button>
      </div>
    </motion.div>
  );
}

interface StatCardProps {
  label: string;
  value: string | number;
  icon: string;
}

function StatCard({ label, value, icon }: StatCardProps) {
  return (
    <div className="card text-center">
      <div className="text-3xl mb-2">{icon}</div>
      <div className="text-2xl font-display font-bold text-primary-100">
        {value}
      </div>
      <div className="text-sm text-primary-400 mt-1">{label}</div>
    </div>
  );
}

function ErrorView({ onReset }: { onReset: () => void }) {
  const { processingError } = useAppStore();

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="text-center space-y-6"
    >
      <div className="text-6xl">⚠️</div>
      <div>
        <h2 className="text-2xl font-display font-semibold text-primary-100">
          Something went wrong
        </h2>
        <p className="text-primary-400 mt-2">
          {processingError || 'An error occurred during processing'}
        </p>
      </div>
      <button onClick={onReset} className="btn-primary">
        Try Again
      </button>
    </motion.div>
  );
}

export default App;
