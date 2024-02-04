import tiktoken
import os
from openai import OpenAI
import json
import google.generativeai as genai
import re
from utils import *
from typing import Generator

prompt_1 = f"You are localizing an anime light novel. Use the provided glossary with preferred terminology mappings to translate the following passage from Chinese to English. Match the style and tone of the original text, and preserve line breaks. Output format: string of translated text only"
prompt_2 = "Refine your translation to natural English without losing nuance. Output format: string of refined translation only"

gpt_client = OpenAI(
    api_key=os.environ.get("OPENAI_MANGA_API_KEY"),
)

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
gemini = genai.GenerativeModel('gemini-pro')

def translate_pipeline_gpt4(source_text: str, glossary: dict = None) -> Generator[str, None, None]:
    """Translate a source text using the GPT model."""
    source_chunks = chunk_source_text(source_text)
    stream_chain = [translate_chunk_with_gpt4(chunk, glossary) for chunk in source_chunks]

    for translated_chunk_stream in stream_chain:
        translated_chunk = ""
        for data in translated_chunk_stream:
            if data.choices[0].delta.content is not None:
                translated_chunk += data.choices[0].delta.content
            else: # end of stream
                packet = json.dumps({"data": str(translated_chunk)}) + '\n'
                print(packet, end="")
                yield packet
                translated_chunk = ""
                continue
            
            if translated_chunk.endswith("\n"): # flush line by line
                packet = json.dumps({"data": str(translated_chunk)}) + '\n'
                print(packet, end="")
                yield packet
                translated_chunk = ""


def translate_chunk_with_gpt4(text: str, glossary: dict = None): # returns a stream (generator)
    """Translate a chunk of text using the GPT model."""
    messages = [
        {"role": "system", "content": prompt_1},
        {"role": "user", "content": text},
    ]

    if glossary:
        sub_glossary = {k: v for k, v in glossary.items() if k in text}
        sub_glossary_string = str(sub_glossary)
        messages.insert(1, {"role": "assistant", "content": f"Glossary: {sub_glossary_string}"})

    completion_stream = gpt_client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=messages,
        temperature=0,
        stream=True,
    )

    return completion_stream

def refine_translation_with_gpt4(source_chunk: str, translated_chunk: str): # returns a stream (generator)
    """Refine a translation using the GPT model."""
    messages = [
        {"role": "system", "content": "You are localizing an anime light novel."},
        {"role": "user", "content": source_chunk},
        {"role": "assistant", "content": translated_chunk},
        {"role": "user", "content": prompt_2},
    ]

    completion_stream = gpt_client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=messages,
        temperature=0,
        stream=True,
    )

    for chunk in completion_stream:
        if chunk.choices[0].delta.content is not None:
            current_response = chunk.choices[0].delta.content
            yield current_response
