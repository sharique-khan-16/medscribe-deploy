"""OCR Ingestion Module."""

import os
import cv2
import numpy as np
import pytesseract  # type: ignore
from PIL import Image

# Set the Tesseract binary path on Windows if it exists
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def extract_text(image_path: str) -> str:
    """Load an image, apply preprocessing (grayscale, contrast enhancement, thresholding), and run OCR.

    Args:
        image_path: Path to the image file.

    Returns:
        Raw extracted text.

    Raises:
        ValueError: If the image cannot be read or OCR returns empty text.
    """
    if not os.path.exists(image_path):
        raise ValueError(f"Image path does not exist: {image_path}")

    # Try loading with OpenCV
    img = cv2.imread(image_path)
    if img is None:
        # Fallback to PIL
        try:
            with Image.open(image_path) as pil_img:
                img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        except Exception as e:
            raise ValueError(f"Could not read image file {image_path}: {e}") from e

    if img is None:
        raise ValueError(f"Could not load image: {image_path}")

    # Basic Preprocessing
    # 1. Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Contrast Enhancement (especially useful for dark/degraded images)
    avg_brightness = np.mean(gray)
    if avg_brightness < 120:
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)

    # 3. Thresholding (Otsu's binarization after Gaussian blur)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Run OCR (try both binarized and grayscale to see if we get better text)
    # We will run OCR on the binarized image first, and fallback to grayscale if empty.
    config = "--psm 4"  # Assume a single column of text of variable sizes
    text = pytesseract.image_to_string(thresh, config=config).strip()

    if not text:
        # Fallback to grayscale if binarized returned nothing
        text = pytesseract.image_to_string(gray, config=config).strip()

    if not text:
        # Direct image fallback
        text = pytesseract.image_to_string(img, config=config).strip()

    if not text:
        raise ValueError("OCR returned empty text from the image.")

    return text
