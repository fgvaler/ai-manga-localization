from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from utils import *
from main import get_translation
from typing import Dict, Any
import json
import time

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
        media_type='application/x-ndjson'
    )

@app.post("/translate_mock")
def translate_mock(payload: Dict[Any, Any]):
    text_to_translate = payload['text']
    time.sleep(1)
    def mockTranslations():
        for i in range(10):
            time.sleep(1)
            yield json.dumps({"data": f"Mock translation {i}"}) + '\n'

    return StreamingResponse(
        mockTranslations(),
        media_type='application/x-ndjson'
    )

