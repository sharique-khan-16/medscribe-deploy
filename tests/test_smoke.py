"""Smoke test to verify modules import and basic functionality."""

from src.main import get_status


def test_get_status() -> None:
    """Verify that get_status returns the correct status structure."""
    status = get_status()
    assert status["status"] == "healthy"
    assert status["offline"] is True
    assert "ocr_engine" in status
    assert "inference_engine" in status
