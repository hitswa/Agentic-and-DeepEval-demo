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

Update `.env` with your Azure OpenAI credentials:

```
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE-NAME.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2025-01-01-preview
```

## 4) Verify imports

```bash
python -c "import autogen, deepeval; print('ok')"
```