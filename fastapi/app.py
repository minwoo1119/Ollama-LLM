from fastapi import FastAPI
from pydantic import BaseModel
import requests
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False, 
)

OLLAMA_API = os.getenv("OLLAMA_API", "http://localhost:11434")

class GenerateRequest(BaseModel):
    prompt: str
    model: str = "llama3.1:8b"

@app.post("/generate")
def generate(req: GenerateRequest):
    try:
        payload = {
            "model": req.model,
            "prompt": req.prompt,
            "stream": False
        }

        res = requests.post(f"{OLLAMA_API}/api/generate", json=payload)
        
        return res.json()

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    
@app.get("/health") 
def health(): return {"ok": True}