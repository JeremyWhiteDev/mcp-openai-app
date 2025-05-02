import os
import shutil
import subprocess
import time
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerSse
from agents.model_settings import ModelSettings

from fastapi.middleware.cors import CORSMiddleware

# ---------- FastAPI Models ----------
class PromptRequest(BaseModel):
    prompt: str
    previous_response_id: Optional[str] = None # Had to create thread_id in hopes of conversation tracking.


# ---------- Global MCP Server ----------
mcp_server: MCPServer | None = None

# ---------- FastAPI App ----------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins for better security
    allow_credentials=True,
    allow_methods=["*"],  # e.g., ["GET", "POST"]
    allow_headers=["*"],  # e.g., ["Authorization", "Content-Type"]
)


@app.post("/ask")
async def ask_agent(req: PromptRequest):
    if mcp_server is None:
        raise HTTPException(status_code=503, detail="MCP Server not initialized yet")

    trace_id = gen_trace_id()
    with trace(workflow_name="API Prompt", trace_id=trace_id):
        agent = Agent(
            name="Assistant",
            instructions="You are Jordan, an assistant that helps the people of flex with their every day work. You speak with a laid back, cool, but helpful and intelligent tone. Use the tools to answer the questions. ask follow up questions if you thing that you can answer them with a tool, prompt users for missing information if you think a tool will answer the question. respond in HTML markup",
            mcp_servers=[mcp_server],
            model_settings=ModelSettings(tool_choice="required"),
        )
        result = await Runner.run(starting_agent=agent, input=req.prompt, previous_response_id=req.previous_response_id)
        print(f"Responseid>>> {result.last_response_id}")

        return {"response": result.final_output, "previous_response_id": result.last_response_id}


# ---------- MCP Setup + FastAPI Startup ----------
async def startup_mcp_server():
    global mcp_server
    mcp_server = MCPServerSse(
        name="SSE Python Server",
        params={"url": "http://localhost:8000/sse"},
    )
    await mcp_server.__aenter__()


@app.on_event("startup")
async def on_startup():
    await startup_mcp_server()


@app.on_event("shutdown")
async def on_shutdown():
    if mcp_server:
        await mcp_server.__aexit__(None, None, None)


# ---------- Run Locally with SSE Server ----------
def start_sse_subprocess():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    server_file = os.path.join(this_dir, "server.py")

    print("Starting SSE server at http://localhost:8000/sse ...")

    process = subprocess.Popen(["uv", "run", server_file])
    time.sleep(3)
    return process


if __name__ == "__main__":
    if not shutil.which("uv"):
        raise RuntimeError("uv is not installed. Please install it: https://docs.astral.sh/uv/getting-started/installation/")

    # Optional: load API key
    # set_default_openai_key(os.getenv("OPENAI_API_KEY"))

    sse_process: subprocess.Popen[Any] | None = None
    try:
        sse_process = start_sse_subprocess()

        print("SSE server started. Starting FastAPI app on http://localhost:9000 ...\n\n")
        uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=False)
    finally:
        if sse_process:
            sse_process.terminate()
