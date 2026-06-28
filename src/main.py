"""MedScribe Backend Main Entry Point."""

from typing import Dict, Any


def get_status() -> Dict[str, Any]:
    """Returns the backend service health status."""
    return {
        "status": "healthy",
        "offline": True,
        "inference_engine": "Ollama (qwen2.5:1.5b)",
        "ocr_engine": "Tesseract OCR",
    }


if __name__ == "__main__":
    status = get_status()
    print(f"MedScribe backend is {status['status']} (Offline: {status['offline']})")
