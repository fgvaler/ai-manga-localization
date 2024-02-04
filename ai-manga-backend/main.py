import sys
from utils import *
from ner import build_glossary_pipeline_gemini, build_glossary_pipeline_gpt3
from translate import translate_chunk_with_gpt4, refine_translation_with_gpt4

def pipeline(source_text: str):
    source_chunks = chunk_source_text(source_text)
    glossary = build_glossary_pipeline_gemini(source_text)

    translated_chunks = []
    for chunk in source_chunks:
        translated_chunk = translate_chunk_with_gpt4(chunk, glossary)
        

if __name__ == '__main__':
    file_path = sys.argv[1]
    source_text = load_source_text(file_path)
    pipeline(source_text)
