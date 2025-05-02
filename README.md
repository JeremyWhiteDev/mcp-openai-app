# A demo for 2025 Relay 1 Innovation

Run a server that starts up a RestAPI and an MCP server to allow an LLM to interact with external tools.


## Example use
```bash
curl -X POST http://localhost:9000/ask \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Tell me about my business locations"}'
```

Provide the previous response in order to thread the conversation together
```bash
curl -X POST http://localhost:9000/ask \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Tell me more about Chicago", "previous_response_id": "resp_abcdef....."}'
```

## Project Setup

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

run the server
```bash
python main.py
```