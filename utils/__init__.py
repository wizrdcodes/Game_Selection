class ReturnToMenu(Exception):
    pass

def check_input(prompt):
    user_input = input(prompt).strip().lower()
    if user_input in ['q', 'quit']:
        raise ReturnToMenu
    return user_input

