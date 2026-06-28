"""MedScribe FastAPI Application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any
import os

# Initialize FastAPI app
app = FastAPI(
    title="MedScribe API",
    description="Offline-first medical document digitizer API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
async def root() -> Dict[str, Any]:
    """Root endpoint - health check."""
    return {
        "status": "healthy",
        "service": "MedScribe API",
        "version": "1.0.0",
        "offline": True,
        "inference_engine": "Ollama (qwen2.5:1.5b)",
        "ocr_engine": "Tesseract OCR",
    }


@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, Any]:
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "offline": True,
        "inference_engine": "Ollama (qwen2.5:1.5b)",
        "ocr_engine": "Tesseract OCR",
        "database": "SQLite",
    }


@app.get("/status", tags=["Health"])
async def get_status() -> Dict[str, Any]:
    """Returns the backend service health status."""
    return {
        "status": "healthy",
        "offline": True,
        "inference_engine": "Ollama (qwen2.5:1.5b)",
        "ocr_engine": "Tesseract OCR",
    }


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not found",
            "message": "The requested resource was not found",
        },
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 handler."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
        },
    )


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")  # nosec B104
    uvicorn.run(app, host=host, port=port)
