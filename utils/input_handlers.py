from utils.io_helpers import input_with_prompt  # uses narration.prompt_input under the hood

class ReturnToMenu(Exception):
    """Custom exception to return to the game selection menu."""
    pass

def check_input(prompt: str):
    """Prompt + ReturnToMenu support."""
    user_input = input_with_prompt(prompt)
    if user_input.strip().lower() in ["q", "quit"]:
        raise ReturnToMenu
    return user_input

def delayed_check_input(prompt: str, delay: float = 0.020):
    """
    Backwards-compat signature; ignore delay because narration controls pacing.
    """
    return check_input(prompt)
