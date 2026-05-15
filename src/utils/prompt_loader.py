from pathlib import Path

def get_system_prompt():
    PROMPT_PATH = Path(__file__).parent.parent.parent / "prompt" / "main_prompt.txt"

    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        main_prompt = f.read()
    return main_prompt