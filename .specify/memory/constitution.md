# MedScribe Project Constitution

This constitution outlines the non-negotiable architectural and behavioral constraints of the MedScribe project. Any code contribution, model selection, or implementation pattern must adhere strictly to these principles.

---

## Core Principles

### I. 100% Offline Execution (No Cloud Dependencies)
The entire ingestion, processing, extraction, structuring, and storage pipeline must run with zero internet connection. No external HTTP/HTTPS calls, cloud APIs (such as OpenAI, Anthropic, Gemini, Azure, AWS, etc.), or external webhooks are permitted in any runtime module. The system must run flawlessly when the network interface card is disabled (airplane mode).

### II. CPU-Only Target Hardware
MedScribe must run efficiently on consumer laptops without dedicated GPUs. The processing stack must rely solely on local CPU inference for the local SLM (Ollama running `qwen2.5:1.5b` or `phi3.5:mini`) and OCR (Tesseract). The memory footprint of the active SLM must not exceed 2GB of RAM.

### III. AGPLv3 License Enforcement
MedScribe is licensed under the GNU Affero General Public License v3 (AGPLv3). All dependencies must have licenses compatible with AGPLv3. Any modification to the source code must remain open-source and be distributed under the AGPLv3 license.

### IV. Robust and Graceful Error Handling
Structured data extraction must fail gracefully when encountering illegible documents, corrupt images, or malformed SLM outputs.
*   If the local SLM returns invalid JSON or fails to conform to the target schema, the pipeline must attempt a fallback model (e.g. `phi3.5:mini`) or run a local regex/JSON-repair block.
*   If repair fails after 3 retries, the pipeline must log the failure, flag the record with a `low` confidence score, and save the raw text to the database rather than crashing.
*   Never expose raw Python exceptions or stack traces to the user interface.

## Governance
This constitution supersedes all other engineering guidelines or practices. All pull requests, code reviews, and architectural changes must verify compliance with these core principles.

**Version**: 1.0.0 | **Ratified**: 2026-06-28
