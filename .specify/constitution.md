# MedScribe Project Constitution

This constitution outlines the non-negotiable architectural and behavioral constraints of the MedScribe project. Any code contribution, model selection, or implementation pattern must adhere strictly to these principles.

---

## 🚫 1. 100% Offline Execution (No Cloud Dependencies)
*   **Principle:** The entire ingestion, processing, extraction, structuring, and storage pipeline must run with zero internet connection.
*   **Rule:** No external HTTP/HTTPS calls, cloud APIs (such as OpenAI, Anthropic, Gemini, Azure, AWS, etc.), or external webhooks are permitted in any runtime module.
*   **Compliance Verification:** The system must run flawlessly when the network interface card is disabled (airplane mode).

## 💻 2. CPU-Only Target Hardware
*   **Principle:** MedScribe must run efficiently on consumer laptops without dedicated GPUs.
*   **Rule:** The processing stack must rely solely on local CPU inference for the local SLM (Ollama running `qwen2.5:1.5b` or `phi3.5:mini`) and OCR (Tesseract).
*   **Constraint:** Memory footprint of the active SLM must not exceed 2GB of RAM.

## ⚖️ 3. AGPLv3 License Enforcement
*   **Principle:** MedScribe is licensed under the GNU Affero General Public License v3 (AGPLv3).
*   **Rule:** All dependencies must have licenses compatible with AGPLv3. Any modification to the source code must remain open-source and be distributed under the AGPLv3 license.

## 🛡️ 4. Robust and Graceful Error Handling
*   **Principle:** Structured data extraction must fail gracefully when encountering illegible documents, corrupt images, or malformed SLM outputs.
*   **Rule:** 
    *   If the local SLM returns invalid JSON or fails to conform to the target schema, the pipeline must attempt a fallback model (e.g. `phi3.5:mini`) or run a local regex/JSON-repair block.
    *   If repair fails after 3 retries, the pipeline must log the failure, flag the record with a `low` confidence score, and save the raw text to the database rather than crashing.
    *   Never expose raw Python exceptions or stack traces to the user interface.
