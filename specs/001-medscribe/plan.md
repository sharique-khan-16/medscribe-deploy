# Implementation Plan: MedScribe

This implementation plan details the technical stack, phases, and time-boxed checkpoints for building MedScribe.

---

## 🛠️ Technology Stack
*   **OCR Engine:** Tesseract OCR (via `pytesseract` Python wrapper) for raw character extraction.
*   **Local SLM Runtime:** Ollama hosting the `qwen2.5:1.5b` model (with `phi3.5:mini` as secondary/fallback) for unstructured text-to-JSON parsing.
*   **Database:** SQLite (relational local file storage, no vector DB).
*   **Backend Server:** FastAPI (local execution, exposes endpoints).
*   **Frontend Dashboard:** Single-page vanilla HTML/CSS/JavaScript with dark mode and micro-animations.

---

## 📅 Chronological Checkpoints

| Checkpoint | Target Time | Milestone / Focus | Key Deliverables |
| :--- | :--- | :--- | :--- |
| **Checkpoint 1** | **10:00 AM** | Phase 1: Plan & Spec | Repository scaffolding, specs, plan, license, and backlog definition. |
| **Checkpoint 2** | **01:30 PM** | Phase 2: Core Loop MVP | OCR pipeline, local Ollama integration, schema validation, and SQLite DB. |
| **Checkpoint 3** | **03:30 PM** | Phase 3: APIs & Frontend | FastAPI server endpoints, drag-and-drop web UI, and local verification. |
| **Final Review** | **04:30 PM** | Phase 3: QA & CI | Offline verification testing, pre-commit configuration, and local CI linting. |

---

## 🏗️ Phase-by-Phase Deliverables

### Phase 1: Planning & Specification
*   Create repository folders (`.specify/`, `docs/`, `agent/`, `src/`, `data/samples/`).
*   Establish project specifications, input/output schemas, and project constitution.
*   Draft issue backlog and define solo/team division of responsibilities.

### Phase 2: Ingestion & Core Extraction Loop (Target: 01:30 PM)
*   **Task 2.1 (OCR Wrapper):** Python scripts to invoke Tesseract OCR with preprocessing (binarization, grayscaling, and deskewing).
*   **Task 2.2 (SLM Connector & Validator):** Set up Ollama connection, prompt template, schema parsing, and a 3-retry validation loop.
*   **Task 2.3 (SQLite Database):** Table design for patient records, medications, and lab results, with insert/query handlers.

### Phase 3: APIs, Frontend, and Verification (Target: 04:30 PM)
*   **Task 3.1 (FastAPI Server):** Develop endpoints (`/upload`, `/process`, `/records`).
*   **Task 3.2 (Web UI):** Single-page upload and query dashboard.
*   **Task 3.3 (Offline Verification):** Script to verify full local execution with no internet.
*   **Task 3.4 (CI & Hooks):** Implement `.pre-commit-config.yaml` and `.gitlab-ci.yml` with 10+ validation checks.
