import tiktoken
import os
from openai import OpenAI
import json
import google.generativeai as genai
import re
from utils import *

instructions_1 = "You are localizing an anime light novel. Identify named entities (such as proper nouns and unique terminologies) in the provided text passage and suggest English translations. Do not include common or general terms."
instructions_2 = "Do not redefine terms already in the glossary. "
instructions_3 = "Output in JSON format: `{ \"original_word\": \"translated_word\", ... }`."

CHUNK_SIZE = 8192

gpt_client = OpenAI(
    api_key=os.environ.get("OPENAI_MANGA_API_KEY"),
)

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
gemini = genai.GenerativeModel('gemini-pro')

def get_named_entities_from_gpt3(text: str, glossary: dict = None) -> str:
    """Ask GPT model to extract named entities from text."""
    glossary_instructions = instructions_2 if glossary else ""
    instructions = instructions_1 + glossary_instructions + instructions_3
    
    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": text},
    ]

    if glossary:
        sub_glossary = {k: v for k, v in glossary.items() if k in text}
        sub_glossary_string = str(sub_glossary)
        messages.insert(1, {"role": "assistant", "content": f"Current glossary: {sub_glossary_string}"})

    completion = gpt_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
    )

    completion_message = completion.choices[0].message.content
    return completion_message

def get_named_entities_from_gpt4(text: str, glossary: dict = None) -> str:
    """Ask GPT model to extract named entities from text."""
    glossary_instructions = instructions_2 if glossary else ""
    instructions = instructions_1 + glossary_instructions + instructions_3
    
    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": text},
    ]

    if glossary:
        sub_glossary = {k: v for k, v in glossary.items() if k in text}
        sub_glossary_string = str(sub_glossary)
        messages.insert(1, {"role": "assistant", "content": f"Current glossary: {sub_glossary_string}"})

    completion = gpt_client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=messages,
        response_format={ "type": "json_object" },
        temperature=0,
    )

    completion_message = completion.choices[0].message.content
    return completion_message

def get_named_entities_from_gemini(text: str, glossary: dict = None) -> str:
    glossary_instructions = instructions_2 if glossary else ""
    instructions = instructions_1 + glossary_instructions + instructions_3

    if glossary:
        sub_glossary = {k: v for k, v in glossary.items() if k in text}
        sub_glossary_string = str(sub_glossary)
        instructions += f" Current glossary: {sub_glossary_string}"
    
    message = f"{instructions}\n\nText:\n```{text}```"

    response = gemini.generate_content(message)
    return response.text

def update_glossary(glossary: dict, new_terms: dict):
    for k, v in new_terms.items():
        if len(k) > 10: # too long
            continue
        glossary[k] = v

def build_glossary_pipeline_gpt3(source_text: str, chunk_size: int = CHUNK_SIZE) -> dict:
    """Extract named entities from source text and build terminology dictionary."""
    assert chunk_size <= 16384, "Chunk size must be less than 16384 tokens for GPT-3.5"
    glossary = {}
    chunks = chunk_source_text(source_text, chunk_size)

    for chunk in chunks:
        named_entities = get_named_entities_from_gpt3(chunk, glossary)
        update_glossary(glossary, json.loads(named_entities))
        print(str(glossary), end='\r')

    return glossary

def build_glossary_pipeline_gemini(source_text: str, chunk_size: int = CHUNK_SIZE) -> dict:
    assert chunk_size <= 8192, "Chunk size must be less than 8192 tokens for Gemini"
    glossary = {}
    chunks = chunk_source_text(source_text, chunk_size)

    for text in chunks:
        glossary_instructions = instructions_2 if glossary else ""
        instructions = instructions_1 + glossary_instructions + instructions_3

        if glossary:
            sub_glossary = {k: v for k, v in glossary.items() if k in text}
            sub_glossary_string = str(sub_glossary)
            instructions += f" Current glossary: {sub_glossary_string}"
        
        message = f"{instructions}\n\nText:\n```{text}```"
        
        chat = gemini.start_chat()
        response = chat.send_message(
            message,
            generation_config=genai.types.GenerationConfig(
                temperature=0
            )
        )
        
        match = re.search(r"{.*}", response.text, re.DOTALL)
        if match:
            update_glossary(glossary, json.loads(match.group()))
            print(str(glossary), end='\r')

    return glossary