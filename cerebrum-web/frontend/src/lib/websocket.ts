/**
 * WebSocket Client - Real-time updates
 */

export type WSMessage = {
  type: 'progress' | 'complete' | 'error';
  job_id: string;
  status?: string;
  stage?: string;
  progress?: number;
  result?: any;
  error?: string;
};

export function connectWebSocket(
  jobId: string,
  onMessage: (message: WSMessage) => void,
  onError?: (error: Event) => void
): WebSocket {
  // Connect to WebSocket
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const ws = new WebSocket(`${protocol}//${window.location.host}/ws/process/${jobId}`);

  ws.onmessage = (event) => {
    const message: WSMessage = JSON.parse(event.data);
    onMessage(message);
  };

  ws.onerror = (error) => {
    if (onError) onError(error);
  };

  return ws;
}
