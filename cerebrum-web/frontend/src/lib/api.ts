/**
 * API Client - Simple and clean
 */

import axios from 'axios';

const api = axios.create({
  baseURL: '/api',  // Proxied by Vite
  timeout: 120000,  // 2 minutes for processing
});

export interface ProcessingResult {
  job_id: string;
  success: boolean;
  literature_note?: any;
  permanent_notes: any[];
  mocs_created: any[];
  mocs_updated: any[];
  links_created: number;
  duration_seconds: number;
  errors: string[];
}

export interface JobStatus {
  job_id: string;
  status: 'processing' | 'completed' | 'failed';
  stage: string | null;
  progress: number;
  result: ProcessingResult | null;
}

/**
 * Upload and process a file
 */
export async function processFile(file: File): Promise<{ job_id: string }> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post('/process', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });

  return response.data;
}

/**
 * Get job status
 */
export async function getJobStatus(jobId: string): Promise<JobStatus> {
  const response = await api.get(`/jobs/${jobId}`);
  return response.data;
}

/**
 * List all jobs
 */
export async function listJobs() {
  const response = await api.get('/jobs');
  return response.data;
}

/**
 * Get vault stats
 */
export async function getVaultStats() {
  const response = await api.get('/vault/stats');
  return response.data;
}

/**
 * List notes
 */
export async function listNotes(folder?: string) {
  const response = await api.get('/vault/notes', { params: { folder } });
  return response.data;
}

/**
 * Get note content
 */
export async function getNote(noteId: string) {
  const response = await api.get(`/vault/notes/${noteId}`);
  return response.data;
}

/**
 * List MOCs
 */
export async function listMOCs() {
  const response = await api.get('/vault/mocs');
  return response.data;
}

/**
 * Get settings
 */
export async function getSettings() {
  const response = await api.get('/settings');
  return response.data;
}

/**
 * Update settings
 */
export async function updateSettings(settings: any) {
  const response = await api.put('/settings', settings);
  return response.data;
}

export default api;
