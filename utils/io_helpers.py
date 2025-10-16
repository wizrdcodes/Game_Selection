# utils/io_helpers.py  (replace file contents)

from utils.narration import (
    narrate as _narrate,
    print_wrapped as _print_wrapped,
    prompt_input as _prompt_input,
    set_skip_all as _set_skip_all,
)

# Backward-compatible wrapper (same signature you use everywhere)
def print_wrapped(text: str = "", width: int = 90, char_delay: float = 0.020, newline_delay: float = 0.0):
    # width/char_delay are passed through so old callsites keep working
    return _print_wrapped(text, newline_delay=newline_delay, char_delay=char_delay, width=width)

# New: expose narrate so you can pass [text, delay, ...] blocks
def narrate(entries, default_delay: float = 1.0, char_delay: float = 0.020, width: int = 90):
    return _narrate(entries, default_delay=default_delay, char_delay=char_delay, width=width)

# Prompts: always use this to reset “fast-forward until next prompt”
def delayed_input(prompt: str = "> "):
    return _prompt_input(prompt)

def input_with_prompt(prompt: str = "> "):  # alias if you used this name elsewhere
    return _prompt_input(prompt)

# Skip-all toggle (S at the start)
def set_skip_all(value: bool):
    _set_skip_all(bool(value))

