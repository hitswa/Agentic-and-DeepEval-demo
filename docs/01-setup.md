# Setup

## 1) Create a virtual environment

**macOS / Linux**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows (Command Prompt)**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## 2) Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 3) Configure environment variables

**macOS / Linux**
```bash
cp .env.example .env
```

**Windows (Command Prompt)**
```cmd
copy .env.example .env
```

**Windows (PowerShell)**
```powershell
Copy-Item .env.example .env
```

Update `.env` with your OpenAI API key:

```
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-4o-mini
```

## 4) Verify imports

```bash
python -c "import autogen, deepeval; print('ok')"
```
