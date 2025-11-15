"""WebSocket Handler - Real-time processing updates"""

from fastapi import WebSocket, WebSocketDisconnect
import asyncio
import json

from app.services.processor import get_processor


async def websocket_endpoint(websocket: WebSocket, job_id: str):
    """
    WebSocket endpoint for real-time job updates

    Simple polling approach - checks job status every 500ms
    """

    await websocket.accept()

    try:
        processor = get_processor()

        while True:
            # Get current job status
            job_data = processor.get_job_status(job_id)

            if job_data['status'] == 'not_found':
                await websocket.send_json({
                    'type': 'error',
                    'error': 'Job not found'
                })
                break

            # Send update
            await websocket.send_json({
                'type': 'progress',
                'job_id': job_id,
                'status': job_data['status'],
                'stage': job_data['stage'],
                'progress': job_data['progress']
            })

            # If completed or failed, send result and close
            if job_data['status'] in ['completed', 'failed']:
                await websocket.send_json({
                    'type': 'complete',
                    'job_id': job_id,
                    'status': job_data['status'],
                    'result': job_data['result']
                })
                break

            # Wait before next update
            await asyncio.sleep(0.5)

    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await websocket.send_json({
                'type': 'error',
                'error': str(e)
            })
        except:
            pass
