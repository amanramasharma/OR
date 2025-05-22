
from ai.gpt_extractor import extract_with_gpt

def analyzeResume(text: str) -> dict:
    return extract_with_gpt(text)