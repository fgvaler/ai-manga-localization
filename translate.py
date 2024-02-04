import tiktoken
import os
from openai import OpenAI
import json
import google.generativeai as genai
import re

prompt_1 = f"You are localizing an anime light novel. Use the provided glossary with preferred terminology mappings to translate the following passage from Chinese to English. Match the style and tone of the original text."
prompt_2 = "Refine the translation to natural English without losing nuance."

gpt_client = OpenAI(
    api_key=os.environ.get("OPENAI_MANGA_API_KEY"),
)

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
gemini = genai.GenerativeModel('gemini-pro')