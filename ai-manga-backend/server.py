from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils import *
from ner import build_glossary_pipeline_gemini, build_glossary_pipeline_gpt3
from translate import translate_chunk_with_gpt4, refine_translation_with_gpt4

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:8080",
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

@app.post("/ner")
async def get_proposed_glossary(request):
    source_text = await request.body()
    return propose_glossary(source_text)

@app.post("/translate")
async def get_body(request):
    text_to_translate = await request.json['text']
    glossary = await request.json['glossary']
    def freyaTODO(text):
        return [
            ['orig1', 'trans1'],
            ['orig2', 'trans2'],
            ['orig3', 'trans3'],
            ['orig4', 'trans4'],
            ['orig5', 'trans5'],
            ['orig6', 'trans6'],
        ]
    return freyaTODO(text_to_translate)

def propose_glossary(source_text: str) -> list[list[str]]:
    glossary = build_glossary_pipeline_gemini(source_text)
    glossary_list = []
    for k, v in glossary.items():
        glossary_list.append([k, v])
    return glossary_list