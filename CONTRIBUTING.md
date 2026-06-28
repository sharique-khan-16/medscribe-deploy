# Contributing to MedScribe

Thank you for contributing to MedScribe! As a 100% offline, privacy-first application, we maintain strict standards for security, code quality, and licensing.

---

## ⚖️ Licensing
By contributing, you agree that your contributions will be licensed under the **GNU Affero General Public License v3 (AGPLv3)**. Ensure all new dependencies are fully compatible with AGPLv3.

---

## 🛠️ Setup & Development Workflow

### 1. Prerequisites
Ensure you have the following installed locally:
*   Python 3.10+
*   Tesseract OCR
*   Ollama (pre-pulled `qwen2.5:1.5b` and `phi3.5:mini`)

### 2. Environment Setup
```bash
python -m venv .venv
# Activate virtual environment
.\.venv\Scripts\Activate.ps1   # Windows PowerShell
source .venv/bin/activate       # Unix/macOS

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

---

## 🎨 Code Style and Quality Checks
We enforce strict style and type checking on every commit. Run the following checks locally before committing:

*   **Formatter (Black):** `black --check src/`
*   **Linter (Ruff):** `ruff check src/`
*   **Type Checker (Mypy):** `mypy src/`
*   **Security Scanner (Bandit):** `bandit -r src/`
*   **Unit Tests (Pytest):** `pytest`

---

## 📝 Commit Guidelines
We use **Semantic Commits**. Commit messages must follow this structure:
```
<type>(<scope>): <short summary>
```

Allowed types:
*   `feat`: A new feature
*   `fix`: A bug fix
*   `docs`: Documentation changes
*   `style`: Code formatting changes (whitespace, semicolons)
*   `refactor`: Code restructuring without behavior changes
*   `test`: Adding or correcting tests
*   `ci`: Changes to CI/CD configurations
*   `chore`: General repository maintenance
