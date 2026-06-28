# Input Schema Spec: MedScribe Ingestion Modality

This document defines the raw input requirements and assumptions for the MedScribe local processing pipeline.

---

## 📸 1. Supported File Formats

MedScribe processes static images of medical documents. The ingestion layer accepts:
*   **JPEG / JPG** (`image/jpeg`)
*   **PNG** (`image/png`)
*   **TIFF** (`image/tiff`)
*   **BMP** (`image/bmp`)

*Note: Multi-page PDFs are out of scope for the initial MVP. If a PDF is provided, it must be converted to individual page images before processing by the API.*

---

## 🔍 2. Image Resolution & Quality Assumptions

To achieve high extraction confidence with local OCR (Tesseract) and local SLMs:
*   **Resolution:** Minimum resolution of `150 DPI` is required; `300 DPI` is highly recommended for small handwritten text.
*   **Orientation:** Images should be oriented upright (portrait preferred). Rotation correction is performed in the preprocessing layer if skew is within $\pm 15$ degrees.
*   **Contrast & Lighting:** High contrast between text and background. Photos taken under poor, casting-shadow lighting or extremely skewed angles may result in low `extraction_confidence` or parsing errors.
*   **Text Types:**
    *   *Prescriptions:* Can contain handwriting, but clear/printed prescriptions yield significantly higher accuracy.
    *   *Lab Reports:* Primarily printed text, structured in columns/grids representing tests, results, and reference ranges.

---

## 📁 3. Test Sample Set (`data/samples/`)

The repository includes standard mock files in `data/samples/` to validate the offline ingestion pipeline:
1.  `prescription_sample_1.jpg`: A photographed handwritten prescription featuring a patient name, two medications with dosages, and a signature.
2.  `lab_report_sample_1.png`: A scanned printed lab report with a table of hematology results (Hemoglobin, WBC, Platelets) including numerical values, units, and reference ranges.

These samples must be used by the offline verification script (`verify_offline.py`) to demonstrate correct operation under zero-network conditions.
