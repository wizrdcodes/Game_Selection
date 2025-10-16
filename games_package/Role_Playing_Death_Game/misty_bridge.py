from .core import (
check_and_run_random_handler,
check_or_return_none,
game_over,
game_state,
print_wrapped
)
from .state import ui_state

# --------------------
# Misty Bridge
# --------------------

def scene_misty_bridge():
    print_wrapped("\nThe bridge sways as you step onto it, fog obscuring your vision.")

    options = [
        {"description": "Walk slowly and carefully.",
         "handler": scene_walk_slowly},
        {"description": "Run across before the mist thickens.",
         "handler": scene_run_across},
    ]
    check_and_run_random_handler(options)

def scene_walk_slowly():
    print_wrapped("\nWith every step, your vision becomes more and more obscured from the fog.")
    print_wrapped("1. Light a torch to light the way and avoid misstepping.")
    print_wrapped("2. Carefully test each step ahead of you.")

    choice = check_or_return_none()
    if choice is None:
        return None

    if choice == "1":
        game_over("You accidentally light the bridge on fire...dropping you into the abyss.", "fall")
    elif choice == "2":
        game_over("A reaper appears from the fog and steals your soul.", "ghost")
    else:
        print_wrapped("\nInvalid choice. Try again.")
        scene_walk_slowly()

def scene_run_across():
        print_wrapped("\nYou hear the bridge snap and creak, the old wood and rope becoming undone.")
        print_wrapped("1. Try to cross quickly before the bridge gives way.")
        print_wrapped("2. Stop running to avoid moving the bridge too much.")

        choice = check_or_return_none()
        if choice is None:
            return None

        if choice == "1":
            game_over("Your movements overwhelm the bridge...and fall into the abyss.", "fall")
        elif choice == "2":
            game_over("Your sudden halt snaps the rope...the bridge fails and you fall into the abyss.", "fall")
        else:
            print_wrapped("\nInvalid choice. Try again.")
            scene_run_across()
