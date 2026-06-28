# MedScribe GitLab Issue Backlog

This document contains the complete list of issues ready for import into the self-hosted GitLab instance (`code.swecha.org`). These issues are ordered sequentially to support a single-developer execution pipeline.

---

## 📋 Issues Summary Table

| ID | Title | Estimate | Target Completion | Dependencies |
| :--- | :--- | :---: | :---: | :---: |
| 1 | Sample Data Collection | 0.5h | 10:30 AM | None |
| 2 | OCR Ingestion Pipeline (Tesseract Wrapper) | 1.0h | 11:30 AM | Issue 1 |
| 3 | Ollama Prompting, Schema Parsing & Retry Loop | 1.5h | 01:00 PM | Issue 2 |
| 4 | SQLite Database Schema & Storage Layer | 0.5h | 01:30 PM | Issue 3 |
| 5 | FastAPI Backend Service Development | 1.0h | 02:30 PM | Issue 4 |
| 6 | Frontend UI (Single-Page App) | 1.0h | 03:30 PM | Issue 5 |
| 7 | Offline Verification Demo Script | 0.5h | 04:00 PM | Issue 3, 4, 5, 6 |
| 8 | Pre-commit Hooks & CI Security Checks | 1.0h | 05:00 PM | Issue 7 |

---

## 📝 Detailed Issue Descriptions

### 1. Sample Data Collection
*   **Estimate:** `0.5h`
*   **Labels:** `phase::2`, `estimate::0.5h`, `component::data`
*   **Description:**
    Set up sample medical files for offline processing validation in `data/samples/`.
    *   Collect/generate at least one representative prescription image (handwritten/printed) named `prescription_sample_1.jpg`.
    *   Collect/generate at least one representative lab report image (with table columns) named `lab_report_sample_1.png`.
    *   Ensure all images are copyright-free, contain simulated/synthetic patient data, and are clean enough for OCR.

---

### 2. OCR Ingestion Pipeline (Tesseract Wrapper)
*   **Estimate:** `1.0h`
*   **Labels:** `phase::2`, `estimate::1.0h`, `component::ocr`
*   **Description:**
    Build a Python module `src/ocr.py` that processes raw input images.
    *   Integrate `pytesseract` to extract raw text from image files.
    *   Implement image preprocessing using `OpenCV` or `Pillow` (grayscaling, binarization/thresholding, and deskewing) to optimize text extraction quality.
    *   Implement basic image metadata collection (resolution check, format validation).
    *   Provide simple unit tests inside `src/tests/` to run against `data/samples/`.

---

### 3. Ollama Prompting, Schema Parsing & Retry Loop
*   **Estimate:** `1.5h`
*   **Labels:** `phase::2`, `estimate::1.5h`, `component::slm`
*   **Description:**
    Build the local SLM controller `src/llm.py` that communicates with the local Ollama daemon.
    *   Configure connector to communicate with local Ollama (`qwen2.5:1.5b` as primary, `phi3.5:mini` as fallback).
    *   Design a system prompt incorporating the exact JSON schema defined in `.specify/output-schema.json` and a few-shot formatting example.
    *   Implement local validation of the returned JSON using Python's `jsonschema` library.
    *   Implement a retry and repair loop (up to 3 retries) that sends validation errors back to the model for correction, or falls back to the secondary model on persistent failure.

---

### 4. SQLite Database Schema & Storage Layer
*   **Estimate:** `0.5h`
*   **Labels:** `phase::2`, `estimate::0.5h`, `component::storage`
*   **Description:**
    Implement the relational storage module `src/database.py`.
    *   Create a SQLite database schema to store extracted documents (`records` table) and their nested medications (`medications` table) and lab results (`lab_results` table).
    *   Implement CRUD functions to insert new records and query existing ones by patient name, record type, or date.
    *   Ensure proper transaction handling and connection pooling (using Python's built-in `sqlite3` or `SQLAlchemy`).

---

### 5. Minimal API (FastAPI Backend)
*   **Estimate:** `1.0h`
*   **Labels:** `phase::3`, `estimate::1.0h`, `component::api`
*   **Description:**
    Create a FastAPI application in `src/main.py`.
    *   Define `/upload` endpoint to receive and temporarily save prescription or lab report images.
    *   Define `/process` endpoint to run the image through OCR, Ollama parsing, validation, and insert results into the SQLite DB.
    *   Define `/records` endpoint (with optional filters) to fetch saved records from the database.
    *   Implement local CORS and exception handlers to gracefully return JSON error responses instead of stack traces.

---

### 6. Frontend UI (Single-Page App)
*   **Estimate:** `1.0h`
*   **Labels:** `phase::3`, `estimate::1.0h`, `component::ui`
*   **Description:**
    Build a local web dashboard to interact with the API.
    *   Create a clean, responsive single-page application using vanilla HTML5, CSS3, and JavaScript in `src/static/`.
    *   Implement a drag-and-drop file upload zone.
    *   Display real-time processing spinners and extraction confidence metrics (`high`, `medium`, `low`).
    *   Display extracted data in interactive tables (medication cards, lab results table) and allow querying/searching historical records.
    *   Apply premium styling: dark mode, glassmorphism, responsive grids, and micro-animations on actions.

---

### 7. Offline Verification Demo Script
*   **Estimate:** `0.5h`
*   **Labels:** `phase::3`, `estimate::0.5h`, `component::test`
*   **Description:**
    Write a standalone test script `src/verify_offline.py` to automate end-to-end testing with network interfaces disabled.
    *   The script must first attempt to ping an external server (e.g. `1.1.1.1` or `google.com`) to ensure the host is offline, or print a prominent notice requesting the user to disable Wi-Fi/Ethernet.
    *   Once offline status is established, it runs the sample images through `src/ocr.py`, `src/llm.py`, and `src/database.py`.
    *   Print validation outputs to stdout showing successful structured data extraction, SQLite database writes, and query results.

---

### 8. Pre-commit Hooks & CI Security Checks
*   **Estimate:** `1.0h`
*   **Labels:** `phase::3`, `estimate::1.0h`, `component::ci`
*   **Description:**
    Configure a comprehensive suite of local code quality, syntax, formatting, and security checks (minimum 10 real checks, no stubs).
    
    #### ⚙️ Local Pre-commit Config (`.pre-commit-config.yaml`):
    1.  `check-yaml`: Validates YAML files.
    2.  `end-of-file-fixer`: Ensures files end in a newline.
    3.  `trailing-whitespace`: Trims trailing whitespace.
    4.  `black`: Formats Python code.
    5.  `ruff`: Lints and organizes imports.
    6.  `mypy`: Performs static type checking.
    7.  `bandit`: Scans Python code for security vulnerabilities.
    8.  `detect-secrets`: Prevents commit of raw keys, credentials, or tokens.
    9.  `commitlint`: Validates that git commit messages conform to semantic standards (e.g., `feat:`, `fix:`, `chore:`).
    10. `pytest`: Runs the Python test suite on commit.

    #### 🧪 GitLab CI Config (`.gitlab-ci.yml`):
    *   Set up a GitLab pipeline executing these checks inside independent jobs (lint, test, security-scan, build-check) using local images, ensuring that any code push meets strict standard baselines.
