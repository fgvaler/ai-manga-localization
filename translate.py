import tiktoken
import os
from openai import OpenAI
import json
import google.generativeai as genai
import re

prompt_1 = f"You are localizing an anime light novel. Use the provided glossary with preferred terminology mappings to translate the following passage from Chinese to English. Match the style and tone of the original text. Output format: string of translated text only"
prompt_2 = "Refine your translation to natural English without losing nuance. Output format: string of refined translation only"

gpt_client = OpenAI(
    api_key=os.environ.get("OPENAI_MANGA_API_KEY"),
)

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
gemini = genai.GenerativeModel('gemini-pro')

def translate_chunk_with_gpt4(text: str, glossary: dict = None) -> str:
    """Translate a chunk of text using the GPT model."""
    messages = [
        {"role": "system", "content": prompt_1},
        {"role": "user", "content": text},
    ]

    if glossary:
        sub_glossary = {k: v for k, v in glossary.items() if k in text}
        sub_glossary_string = str(sub_glossary)
        messages.insert(1, {"role": "assistant", "content": f"Glossary: {sub_glossary_string}"})

    completion = gpt_client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=messages,
        temperature=0,
    )

    return completion.choices[0].message.content.strip()

def refine_translation_with_gpt4(source_text: str, translated_text: str) -> str:
    """Refine a translation using the GPT model."""
    messages = [
        {"role": "system", "content": "You are localizing an anime light novel."},
        {"role": "user", "content": source_text},
        {"role": "assistant", "content": translated_text},
        {"role": "user", "content": prompt_2},
    ]

    completion = gpt_client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=messages,
        temperature=0,
    )

    return completion.choices[0].message.content.strip()