# A demo for 2025 Relay 1 Innovation

Run a server that starts up a RestAPI and an MCP server to allow an LLM to interact with external tools, specifically the Flex5 Open API.

### Learnings

1. Date parsing can be hard with LLMs when I want a plain text human readable string to be parsed as an ISO String.
2. When I did this, the results were indeterminate. Sometimes it would successfully make a quote, sometimes it wouldn't.
3. APIs might have to be redisigned to better work with prompting and a tool architecture. Older APIs implementations might be strongly determined by UI implementations and have their contracts determined by the UI, rather than being implemented with consideration of "good API design". Those failures become more apparent when using APIs in different contexts.


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
pip install fastapi uvicorn pydantic requests python-dateutil pytz openai-agents-sdk python-dotenv
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
