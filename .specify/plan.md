# Project Execution Plan: MedScribe

This execution plan outlines the deliverables and time-boxing checkpoints for developing MedScribe today. 

---

## 📅 Chronological Checkpoints (Today's Timeline)

| Checkpoint | Target Time | Focus / Milestone | Key Deliverables |
| :--- | :--- | :--- | :--- |
| **Checkpoint 1** | **10:00 AM** | Plan & Spec Submission (Phase 1) | Scaffold, README, Spec-kit, LICENSE, Issue Scaffolding |
| **Checkpoint 2** | **1:00 PM (Lunch)** | Core MVP Implementation (Phase 2) | OCR Ingestion, Ollama prompt/retry core loop, SQLite integration |
| **Checkpoint 3** | **3:00 PM** | Local UI, Demo Script, Repo Audit | FastAPI backend, vanilla web UI, offline verification script |
| **Final Review** | **4:00 PM** | Verification & Polish | Pre-commit / CI setup validation, 100% offline verification run |

---

## 🛠️ Phase-by-Phase Plan

### Phase 1: Planning & Specification (Target: 10:00 AM)
*   **Scaffolding:** Directory layout and `.gitignore` setup.
*   **Documentation:** Detailed `README.md` and licensing (`LICENSE` with AGPLv3).
*   **Specs:** Input specification, output JSON Schema, and constitutional constraints.
*   **Ticketing:** Scaffold project issues (in self-hosted GitLab or `docs/ISSUES.md`).

### Phase 2: Ingestion & Core Extraction Loop (Target: 1:00 PM)
*   **Task 2.1: Ingestion & OCR Wrapper:** Write Python script to wrap Tesseract OCR and run image preprocessing (e.g. grayscaling, thresholding).
*   **Task 2.2: Local SLM Integration:** Configure Ollama connector, build prompt templates with in-context examples, and implement a JSON repair/retry parser.
*   **Task 2.3: SQLite Database Integration:** Create schemas and DB handlers to insert structured JSON data.

### Phase 3: APIs, Frontend, and Verification (Target: 3:00 PM)
*   **Task 3.1: FastAPI App:** Create local endpoint routes (`/upload`, `/process`, `/records`).
*   **Task 3.2: Web UI:** Build a single-page HTML/CSS/JS frontend to upload photos and display structured patient cards.
*   **Task 3.3: Verification Script:** Write a comprehensive shell/python command to test with Wi-Fi disabled.
*   **Task 3.4: Repo Audit & CI Scaffolding:** Set up code quality tools, pre-commit hooks, and a local GitLab CI config.
