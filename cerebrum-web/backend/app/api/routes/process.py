"""Process Routes - Simple and clean"""

from fastapi import APIRouter, File, UploadFile, HTTPException
from pathlib import Path
import tempfile
import shutil

from app.models.response import ProcessingResult, JobStatus
from app.services.processor import get_processor

router = APIRouter()


@router.post("/process", response_model=dict)
async def process_file(file: UploadFile = File(...)):
    """
    Process a PDF file

    Simple flow:
    1. Save uploaded file
    2. Process with Cerebrum
    3. Return job_id
    """

    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files supported")

    # Save to temp file
    temp_dir = Path(tempfile.mkdtemp())
    temp_file = temp_dir / file.filename

    try:
        with temp_file.open('wb') as f:
            shutil.copyfileobj(file.file, f)

        # Process
        processor = get_processor()
        job_id = processor.process_file(temp_file)

        return {"job_id": job_id, "status": "processing"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/jobs/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """Get status of a processing job"""

    processor = get_processor()
    job_data = processor.get_job_status(job_id)

    if job_data['status'] == 'not_found':
        raise HTTPException(status_code=404, detail="Job not found")

    return JobStatus(
        job_id=job_id,
        status=job_data['status'],
        stage=job_data['stage'],
        progress=job_data['progress'],
        result=job_data['result']
    )


@router.get("/jobs", response_model=list)
async def list_jobs():
    """List all processing jobs (history)"""

    processor = get_processor()

    jobs = []
    for job_id, job_data in processor.jobs.items():
        jobs.append({
            'job_id': job_id,
            'status': job_data['status'],
            'result': job_data.get('result')
        })

    return jobs
