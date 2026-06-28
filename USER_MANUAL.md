# MedScribe User Manual

Welcome to **MedScribe**, an offline-first medical document digitizer. MedScribe extracts structured JSON data from physical prescriptions and lab reports using local OCR and a locally-run Large Language Model (LLM).

---

## 🚀 Key Features
1. **OCR Ingestion**: Grayscale conversion, CLAHE contrast enhancement, and Otsu binarization for clean text extraction from clean and degraded images.
2. **Local AI Structuring**: Query-optimized Prompt engineering utilizing Ollama's `qwen2.5:1.5b` model to structure raw OCR text.
3. **Pydantic Validation**: Strong runtime schema constraints with automated retry-once error handling.
4. **Relational Database**: Storage of patients, medical records, medications, and lab results in SQLite.

---

## 🛠️ Requirements & Installation

### 1. Prerequisites
- **Python**: Version 3.11 or higher.
- **Tesseract OCR**: 
  - *Windows*: Download and run the installer from the [UB-Mannheim Tesseract Wiki](https://github.com/UB-Mannheim/tesseract/wiki). Ensure it is installed at `C:\Program Files\Tesseract-OCR`.
  - *Linux/macOS*: Install via your package manager (`apt-get install tesseract-ocr` or `brew install tesseract`).
- **Ollama**: Download and install from [Ollama.com](https://ollama.com). Pull the Qwen model:
  ```bash
  ollama pull qwen2.5:1.5b
  ```

### 2. Setup
Clone the repository and install the dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

---

## 🖥️ Running the Application

Start the FastAPI backend server:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```
Once started, the interactive API documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 🔌 API Endpoints

### 1. `POST /upload`
Uploads a prescription or lab report image, runs OCR and LLM validation, and saves the record.
- **Payload**: Multipart Form (`file` field containing image/pdf)
- **Response**: Structured JSON matching the output schema.

### 2. `GET /records`
Retrieves all historical extracted records from the SQLite database.
- **Response**: Array of structured records.

### 3. `GET /health` / `GET /status`
Returns the status of local OCR and LLM inference engines.

---

## 🗂️ Data Schema
Reconstructed SQLite output:
- **Patient**: Name, Age, Gender
- **Record**: Type (`prescription` | `lab_report`), Issuing Doctor, Date, Facility Location, Diagnosis
- **Medications**: Name, Dosage, Frequency, Duration
- **Lab Results**: Test Name, Value, Unit, Reference Range, Flag (`normal` | `high` | `low`)
