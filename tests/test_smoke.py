"""Smoke test to verify modules import and basic functionality."""

import os
import shutil
import pytest
from unittest.mock import patch, MagicMock
from src.main import get_status
from src.ocr import extract_text
from src.extractor import extract_data

TESSERACT_EXISTS = shutil.which("tesseract") is not None or os.path.exists(
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def test_get_status() -> None:
    """Verify that get_status returns the correct status structure."""
    status = get_status()
    assert status["status"] == "healthy"
    assert status["offline"] is True
    assert "ocr_engine" in status
    assert "inference_engine" in status


@pytest.mark.skipif(
    not TESSERACT_EXISTS, reason="Tesseract OCR binary not installed on this system"
)
def test_ocr_extraction() -> None:
    """Verify that OCR returns non-empty text containing expected patient name from sample 1."""
    sample_path = os.path.join("data", "samples", "prescription_sample_01.jpg")
    assert os.path.exists(sample_path), f"Sample image not found: {sample_path}"

    text = extract_text(sample_path)
    assert len(text) > 0
    assert "Maria" in text
    assert "Sharapova" in text
    assert "Smith" in text


@patch("src.extractor.ollama.chat")
def test_validator_retry(mock_chat: MagicMock) -> None:
    """Verify that the extractor correctly retries once on malformed JSON from Ollama."""
    # First response is malformed JSON (not valid json)
    first_response = {"message": {"content": "This is not JSON at all! Just raw text."}}

    # Second response is a valid JSON string matching the required ExtractionResult schema
    second_response = {
        "message": {
            "content": (
                '{"patient": {"name": "Test Patient", "age": 30, "gender": "Male"}, '
                '"record": {"type": "prescription", "date": "2023-10-10T00:00:00Z", '
                '"doctor_name": "Test Doctor", "facility": "Test Clinic"}, '
                '"medications": [], "diagnosis": "Healthy", "lab_results": [], '
                '"extraction_confidence": "high"}'
            )
        }
    }

    # Configure mock to return first response, then second response
    mock_chat.side_effect = [first_response, second_response]

    result = extract_data("Mock raw OCR text")

    # Check that it called Ollama twice
    assert mock_chat.call_count == 2
    # Verify the final returned object matches the second response
    assert result.patient.name == "Test Patient"
    assert result.record.type == "prescription"
    assert result.extraction_confidence == "high"
