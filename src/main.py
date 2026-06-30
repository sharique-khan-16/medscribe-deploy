"""MedScribe FastAPI Main Application."""

import os
import uuid
import shutil
from typing import Any
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from src.ocr import extract_text
from src.extractor import extract_data, ExtractionResult
from src.db import save_extraction, get_all_records, init_db

# Initialize database
init_db()

# Initialize FastAPI App
app = FastAPI(
    title="MedScribe API",
    description="Offline-first medical document digitizer API",
    version="1.0.0",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.join("data", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/", include_in_schema=False)
async def root():
    """Serve the MedScribe PWA frontend."""
    return FileResponse(os.path.join("static", "index.html"))


app.mount("/static", StaticFiles(directory="static"), name="static")


def get_status() -> dict[str, Any]:
    """Returns the backend service health status."""
    return {
        "status": "healthy",
        "offline": True,
        "inference_engine": "Ollama (qwen2.5:1.5b)",
        "ocr_engine": "Tesseract OCR",
    }


@app.get("/health", tags=["Health"])
@app.get("/status", tags=["Health"])
async def health() -> dict[str, Any]:
    """Health check endpoint."""
    return get_status()


@app.post("/upload", response_model=ExtractionResult, tags=["Ingestion"])
async def upload_prescription(file: UploadFile = File(...)):
    """Accepts a prescription/report image, runs OCR, extracts structured data, and saves to SQLite."""
    # Validate file extension
    orig_filename = file.filename or "file"
    ext = os.path.splitext(orig_filename)[1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".pdf"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Please upload a JPG, PNG, or PDF.",
        )

    # Save file to upload directory
    unique_id = uuid.uuid4().hex[:8]
    filename = f"{unique_id}_{orig_filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to save uploaded file: {e}"
        )

    # Process pipeline
    try:
        # 1. OCR Ingestion
        raw_text = extract_text(file_path)

        # 2. Ollama structured data extraction & validation
        extraction = extract_data(raw_text)

        # 3. Save to database
        save_extraction(extraction)

        return extraction

    except ValueError as val_err:
        raise HTTPException(status_code=422, detail=str(val_err))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline processing failed: {e}")
    finally:
        # Cleanup uploaded file to save disk space if desired
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:  # nosec B110
                pass


@app.get("/records", tags=["Records"])
async def get_records() -> list[dict[str, Any]]:
    """Retrieves all processed medical records from the database."""
    try:
        return get_all_records()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch records: {e}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)  # nosec B104
