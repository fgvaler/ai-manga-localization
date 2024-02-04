import sys
from utils import *
from ner import create_glossary
from translate import translate_pipeline_gpt4

def get_translation(source_text: str):
    glossary = create_glossary(source_text, model='gpt')
    translation_stream = translate_pipeline_gpt4(source_text, glossary)
    return translation_stream

if __name__ == '__main__':
    file_path = sys.argv[1]
    source_text = load_source_text(file_path)
    get_translation(source_text)
