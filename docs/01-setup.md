# Setup

## 1) Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate # for mac or linux
# ./venv/bin/activate # for windows
```

## 2) Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 3) Configure environment variables

```bash
cp .env.example .env
```

Update `.env` with your OpenAI API key:

```
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-4o-mini
```

## 4) Verify imports

```bash
PYTHONPATH=src python -c "import autogen, deepeval; print('ok')"
```
