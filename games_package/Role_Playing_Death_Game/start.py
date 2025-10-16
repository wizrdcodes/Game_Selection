from .core import check_or_return_none, print_wrapped, game_state, check_and_run_random_handler
from .state import reset_game_state, reset_player_state
from utils.input_handlers import ReturnToMenu
from utils.helper_functions import delay

# Import each scene entry-point from its own file
from .dark_forest           import scene_dark_forest
from .abandoned_castle      import scene_abandoned_castle
from .forgotten_cavern      import scene_forgotten_cavern
from .misty_bridge          import scene_misty_bridge
from .mountain_of_echoes    import scene_mountain_of_echoes

def start_game():
    """Starts the game and presents the first set of choices."""
    global game_state, player_state
    game_state, player_state = reset_game_state(), reset_player_state()
    print_wrapped()
    print_wrapped("Welcome, traveler.", newline_delay=1)
    print_wrapped("You stand at the entrance of a mysterious land.", newline_delay=1)
    print_wrapped("Tread carefully...", newline_delay=1)
    print_wrapped("1. Enter the Dark Forest.", newline_delay=0.5)
    print_wrapped("2. Walk toward the Abandoned Castle.", newline_delay=0.5)
    print_wrapped("3. Descend into the Forgotten Cavern.", newline_delay=0.5)
    print_wrapped("4. Cross the Misty Bridge.", newline_delay=0.5)
    print_wrapped("5. Climb the Mountain of Echoes.", newline_delay=0.5)

    try:
        choice = check_or_return_none()
    except ReturnToMenu:
        print_wrapped("Returning to menu...", newline_delay=1.5)
        return None

    if choice == "1":
        scene_dark_forest()
    elif choice == "2":
        scene_abandoned_castle()
    elif choice == "3":
        scene_forgotten_cavern()
    elif choice == "4":
        scene_misty_bridge()
    elif choice == "5":
        scene_mountain_of_echoes()
    else:
        print_wrapped("\nInvalid choice. Try again.")
        start_game()
