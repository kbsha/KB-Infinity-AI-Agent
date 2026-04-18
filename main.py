from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agent import run_agent
import uvicorn

app = FastAPI()

# Serve static files (JS/CSS if needed later)
app.mount("/static", StaticFiles(directory="static"), name="static")


# Request model
class AgentRequest(BaseModel):
    prompt: str


# Response model
class AgentResponse(BaseModel):
    response: str


# Home page (IMPORTANT FIX)
@app.get("/")
def home():
    return FileResponse("static/index.html")


# AI endpoint
@app.post("/agent", response_model=AgentResponse)
def invoke_agent(request: AgentRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    result = run_agent(request.prompt)
    return AgentResponse(response=result)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)