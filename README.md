# Stock AI Technical Analyst

This repository contains a FastAPI backend for stock technical analysis.

## Getting Started

### Opening in VS Code

This project includes a VS Code workspace configuration for an enhanced development experience.

**Option 1: Open with Workspace File**
1. Open VS Code
2. Go to `File > Open Workspace from File...`
3. Select `stock-ai-technical-analyst.code-workspace` from the project root

**Option 2: Open Folder with Settings**
1. Open the project folder in VS Code
2. The `.vscode` settings will be automatically applied

### Recommended Extensions

When you open the workspace, VS Code will prompt you to install recommended extensions:
- Python
- Pylance
- Black Formatter
- Pylint
- Python Debugger
- Jupyter
- Even Better TOML
- YAML
- GitHub Copilot
- GitLens

### Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   - Linux/Mac: `source .venv/bin/activate`
   - Windows: `.venv\Scripts\activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

**Using VS Code Debug Configuration:**
- Press `F5` or go to `Run > Start Debugging`
- Select "Python: FastAPI" from the debug configuration

**Using Terminal:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Available VS Code Tasks

Access tasks via `Terminal > Run Task...`:
- **Install Dependencies** - Install Python packages from requirements.txt
- **Run FastAPI Server** - Start the development server
- **Run Tests** - Execute pytest tests
- **Format Code** - Format code with Black
- **Lint Code** - Lint code with Pylint

### API Documentation

Once the server is running, access the documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
