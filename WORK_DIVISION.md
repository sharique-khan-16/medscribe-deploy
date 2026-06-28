# Work Division Plan (Solo Hackathon Timeline)

This document provides a single-developer, time-boxed execution plan for the MedScribe project today. Since this is a solo project, tasks are sequenced linearly to avoid context-switching and resolve dependencies in order.

---

## 🕒 Chronological Execution Schedule

| Time Block | Target Issue | Goal | Key Deliverables | Risk Level |
| :--- | :--- | :--- | :--- | :---: |
| **09:30 - 10:00** | **N/A** | Phase 1: Planning & Specs | Complete repo structure, spec files, license, and backlog definition. | 🟢 Low |
| **10:00 - 10:30** | **Issue 1** | Sample Data Setup | Create synthetic/mock medical files for local system testing. | 🟢 Low |
| **10:30 - 11:30** | **Issue 2** | OCR Pipeline Setup | Build Tesseract wrapper, configure basic OpenCV binarization. | 🟡 Medium |
| **11:30 - 13:00** | **Issue 3** | Ollama & Schema Parser | Prompting setup, JSON validation loop, repair/retry logic. | 🔴 High |
| **13:00 - 13:30** | **N/A** | *Lunch Break & Buffer* | Catch up on any delays in the OCR + Ollama pipeline. | 🟢 Low |
| **13:30 - 14:00** | **Issue 4** | Database Integration | Create SQLite schema, CRUD operations, database connection. | 🟢 Low |
| **14:00 - 15:00** | **Issue 5** | FastAPI Backend | Implement API endpoints (`/upload`, `/process`, `/records`). | 🟡 Medium |
| **15:00 - 16:00** | **Issue 6** | Frontend Dashboard | HTML/CSS/JS single-page UI for uploads and record review. | 🟡 Medium |
| **16:00 - 16:30** | **Issue 7** | Offline Verification | Automated test script to verify processing with Wi-Fi disabled. | 🟡 Medium |
| **16:30 - 17:30** | **Issue 8** | CI & Pre-commit Hooks | Setup `.pre-commit-config.yaml` and `.gitlab-ci.yml`. | 🟢 Low |

---

## ⚡ Risk Analysis & Mitigation Strategies

If development time runs short or technical bugs slow down progress, the following prioritizations will be enforced:

### 1. Non-Negotiable Core (Must Deliver)
*   **Issue 3 (Ollama/SLM Extraction Loop):** This is the heart of the project. If Ollama formatting fails or has high latency, the entire system breaks. **Mitigation:** Fall back immediately to a simpler system prompt or try `phi3.5:mini` if `qwen2.5:1.5b` behaves unpredictably on CPU.
*   **Issue 2 (OCR Pipeline):** OCR must yield clean text for the SLM to perform. **Mitigation:** Keep image preprocessing minimal (simple grayscaling and thresholding) unless character recognition is unacceptably low.

### 2. High Risk/High Complexity (Monitor closely)
*   **Issue 3 (JSON Schema compliance):** Local models under 3B parameters frequently fail to generate strictly conforming JSON. **Mitigation:** Implement regex-based extraction to extract the JSON block out of the model response, and use standard string-repair techniques (e.g. adding missing brackets/braces) before validation.

### 3. De-prioritized / Scoped-out (Drop if running late)
*   **Issue 8 (CI & Pre-commit Hooks):** Having 10+ validation checks in CI is valuable for repository health, but can be bypassed temporarily or reduced to standard Python formatting (`ruff` / `black`) if submission is close.
*   **Issue 7 (Offline Verification Script):** While required for the demo, if time is extremely short, a manual demonstration (turning off Wi-Fi in the OS and running the app through the browser) can suffice instead of debugging automated shell/python network pings.
*   **Issue 6 (Frontend UI Styling):** If premium styling takes too long, stick to clean semantic HTML with a basic stylesheet first. A working black-and-white functional UI is better than a broken premium page.
