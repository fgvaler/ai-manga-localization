from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from utils import *
from main import get_translation
from typing import Dict, Any

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message": "Hello World"}

@app.post("/translate")
def translate(payload: Dict[Any, Any]):
    text_to_translate = payload['text']

    return StreamingResponse(
        get_translation(text_to_translate),
        media_type='text/event-stream'
    )