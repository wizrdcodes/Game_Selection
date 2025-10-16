from .core import game_state, check_and_run_random_handler, game_over, print_wrapped, check_or_return_none
from .state import ui_state

# --------------------
# Mountain of Echoes
# --------------------

def scene_mountain_of_echoes():
    print_wrapped("\nThe wind howls as you climb higher.")
    options = [
        {"description": "Seek shelter in a small cave.",
         "handler": scene_seek_shelter},
        {"description": "Push forward.",
         "handler": scene_push_forward},
    ]
    check_and_run_random_handler(options)

def scene_seek_shelter():
    print_wrapped("\nYou find a beast sleeping in the cave, surrounded by bones.")
    print_wrapped("1. Unsheathe your blade and prepare for the worst.")
    print_wrapped("2. Abandon the cave and chance the mountain path.")

    choice = check_or_return_none()
    if choice is None:
        return None

    if choice == "1":
        game_over("The beast is larger than you thought...you knew your chances were slim.", "beast")
    elif choice == "2":
        game_over("You exit the cave too quickly, and lose your footing...", "fall")
    else:
        print_wrapped("\nInvalid choice. Try again.")
        scene_seek_shelter()

def scene_push_forward():
    print_wrapped("\nYou see the peak of the icy mountain ahead, merely a few feet away.")
    options = [
        {"description": "Push forward to the peak.", "handler": scene_push_to_peak},
        {"description": "Rest and admire the view.", "handler": scene_admire_view}
    ]
    check_and_run_random_handler(options)

def scene_push_to_peak():
    game_over("The peak was an illusion. You step into the void.", "void")

def scene_admire_view():
        game_over("The ice beneath you gives way, dropping you into the void.", "void")

