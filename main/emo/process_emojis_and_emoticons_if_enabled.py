import os
from .process_emojis import process_emojis
from .process_emoticons import process_emoticons

TRUTHFUL_VALUES = ['1', 'true', 'yes', 'on', 'enable', 'enabled', 'y']

ENABLE_EMOJIS_PREPROCESSING = os.getenv('ENABLE_EMOJI_PREPROCESSING', 'ON').lower() in TRUTHFUL_VALUES

ENABLE_EMOTICONS_PREPROCESSING = os.getenv('ENABLE_EMOTICONS_PREPROCESSING', 'ON').lower() in TRUTHFUL_VALUES

def process_emojis_and_emoticons_if_enabled(text: str) -> str:
    if ENABLE_EMOJIS_PREPROCESSING:
        text = process_emojis(text)
    if ENABLE_EMOTICONS_PREPROCESSING:
        text = process_emoticons(text)
    return text
