# Work Division Plan (Two-Person Team Split)

This document outlines the parallelized time-boxed execution plan for the MedScribe project today, dividing work between Sharique and Harshit.

---

## 👥 Team Members & Roles

*   **Sharique Khan (@shariquekhan)** — Backend & Core Pipeline Lead
    *   *Ownership:* Sample data, OCR ingestion, Ollama prompt/validator core loop, SQLite DB layer, FastAPI backend, and offline verification demo script.
*   **Harshit Reddy (@HarshithReddy11)** — Frontend & Developer Operations Lead
    *   *Ownership:* Single-page Web UI, styling (dark mode/micro-animations), and pre-commit hook / GitLab CI quality pipeline configuration.

---

## 🕒 Chronological Execution Schedule

Since this is a two-person team, tasks are parallelized where possible. Sharique's backend API development acts as the main dependency blocking Harshit's integration phase.

### 🛤️ Sharique's Track (Core Pipeline & API)

| Time Block | Target Issue | Goal | Key Deliverables | Risk Level |
| :--- | :--- | :--- | :--- | :---: |
| **10:00 - 10:30** | **N/A** | Phase 1: Planning & Specs | Align on specifications and schema definitions with Harshit. | 🟢 Low |
| **10:30 - 11:00** | **Issue 1** | Sample Data Setup | Collect/generate mock prescription and lab report images. | 🟢 Low |
| **11:00 - 12:00** | **Issue 2** | OCR Pipeline Setup | Build Tesseract wrapper, configure image preprocessing filters. | 🟡 Medium |
| **12:00 - 13:30** | **Issue 3** | Ollama & Schema Parser | Implement prompt template, schema validator, and retry loop. | 🔴 High |
| **13:30 - 14:00** | **N/A** | *Lunch Break & Buffer* | Catch up on any delays in the OCR + Ollama pipeline. | 🟢 Low |
| **14:00 - 14:30** | **Issue 4** | Database Integration | Create SQLite schema, write insertion and query DB layers. | 🟢 Low |
| **14:30 - 15:30** | **Issue 5** | FastAPI Backend | Implement local API endpoints (`/upload`, `/process`, `/records`). | 🟡 Medium |
| **15:30 - 16:00** | **Issue 7** | Offline Verification | Create verification script (`verify_offline.py`) to test without Wi-Fi. | 🟡 Medium |
| **16:00 - 16:30** | **N/A** | Integration & Audit | Sync with Harshit to connect UI with API and perform code audit. | 🟢 Low |

---

### 🛤️ HarshithReddy11's Track (UI & Devops CI)

| Time Block | Target Issue | Goal | Key Deliverables | Risk Level |
| :--- | :--- | :--- | :--- | :---: |
| **10:00 - 10:30** | **N/A** | Phase 1: Planning & Specs | Align on specs, review inputs, and output JSON schemas. | 🟢 Low |
| **10:30 - 12:00** | **Issue 6 (Part 1)** | UI Mocking & Static Assets | Build static HTML/CSS structure, configure premium dark mode. | 🟢 Low |
| **12:00 - 13:30** | **Issue 8 (Part 1)** | Pre-commit Hook Setup | Configure local `.pre-commit-config.yaml` with lint/type checks. | 🟢 Low |
| **13:30 - 14:00** | **N/A** | *Lunch Break* | Sync with Sharique on Ollama pipeline readiness. | 🟢 Low |
| **14:00 - 14:30** | **Issue 8 (Part 2)** | GitLab CI Pipeline | Write `.gitlab-ci.yml` runner jobs (security checks, pytest). | 🟡 Medium |
| **14:30 - 15:30** | **Issue 6 (Part 2)** | UI & API Integration | Connect drag-and-drop uploads and tables to FastAPI endpoints. | 🔴 High |
| **15:30 - 16:30** | **Issue 8 (Part 3)** | CI Pipeline Testing | Run linting checks locally and verify commits match rules. | 🟢 Low |
| **16:00 - 16:30** | **N/A** | Integration & Audit | Sync with Sharique to connect UI with API and perform code audit. | 🟢 Low |

---

## 🔄 Sync Points & Dependencies

To ensure parallel tracks run smoothly without blocking each other:

1.  **Contract Freeze (10:30 AM):** Sharique and Harshit finalize and freeze the target output format (`output-schema.json`) so Harshit can mock the API responses in the frontend.
2.  **API Integration Handshake (14:30 PM):** Sharique shares the FastAPI endpoints and contracts (`/upload`, `/process`, `/records`) with Harshit. Harshit begins pointing frontend AJAX calls to the live local server endpoints.
3.  **Final Integration Sync (16:00 PM):** Merge branches, run the local server offline, perform cross-component validation, and run pre-commit verification before submission.

---

## ⚡ Risk Analysis & Mitigation Strategies

### 1. Non-Negotiable Core (Must Deliver)
*   **Ollama/SLM Extraction Loop (Sharique):** High risk of output formatting issues. If Sharique falls behind, Harshit will assist by adding basic regex-based JSON cleaning filters.
*   **API Integration (Harshit + Sharique):** Connecting frontend to backend is a common point of failure. Mitigation: Both will use strict mock JSON files if endpoint communication exhibits CORS or routing errors.

### 2. De-prioritized / Scoped-out (Drop if running late)
*   **Issue 8 (CI & Pre-commit Hooks):** Harshit can disable non-essential checks (e.g. strict Markdown linting or complex static type checks) if time is running short, keeping only core python linting (`ruff`/`black`) and unit tests.
*   **Issue 7 (Offline Verification Script):** Sharique can simplify the offline script to a basic execution command and demonstrate offline capability manually if automation debugging is too slow.
