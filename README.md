# A demo for 2025 Relay 1 Innovation

Setup the python virtual environment

```bash
python3 -m venv venv
source venv/bin/activate

```

Install dependencies

```bash
pip install fastapi uvicorn pydantic requests python-dateutil pytz openai-agents-sdk
```

Add Open API key

```bash
export OPENAI_API_KEY=sk_...
```

Create a `.env` file based off the `.example.env` and add your variables