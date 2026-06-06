import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents import consultar

app = FastAPI(title="Bavafy AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    reply: str

@app.get("/")
def health():
    return { "status": "Bavafy AI corriendo" }

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    respuesta = consultar(req.message)
    return { "reply": respuesta }