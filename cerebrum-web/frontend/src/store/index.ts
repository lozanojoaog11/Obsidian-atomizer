/**
 * Global State Store - Zustand
 * Simple and elegant state management
 */

import { create } from 'zustand';
import { ProcessingResult } from '../lib/api';

interface AppState {
  // Processing state
  currentJobId: string | null;
  processingStatus: 'idle' | 'uploading' | 'processing' | 'completed' | 'error';
  processingStage: string | null;
  processingProgress: number;
  processingResult: ProcessingResult | null;
  processingError: string | null;

  // Actions
  setProcessing: (jobId: string) => void;
  updateProgress: (stage: string, progress: number) => void;
  setCompleted: (result: ProcessingResult) => void;
  setError: (error: string) => void;
  reset: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  // Initial state
  currentJobId: null,
  processingStatus: 'idle',
  processingStage: null,
  processingProgress: 0,
  processingResult: null,
  processingError: null,

  // Actions
  setProcessing: (jobId) =>
    set({
      currentJobId: jobId,
      processingStatus: 'processing',
      processingStage: 'starting',
      processingProgress: 0,
      processingResult: null,
      processingError: null,
    }),

  updateProgress: (stage, progress) =>
    set({
      processingStage: stage,
      processingProgress: progress,
    }),

  setCompleted: (result) =>
    set({
      processingStatus: 'completed',
      processingStage: 'complete',
      processingProgress: 1,
      processingResult: result,
    }),

  setError: (error) =>
    set({
      processingStatus: 'error',
      processingError: error,
    }),

  reset: () =>
    set({
      currentJobId: null,
      processingStatus: 'idle',
      processingStage: null,
      processingProgress: 0,
      processingResult: null,
      processingError: null,
    }),
}));
