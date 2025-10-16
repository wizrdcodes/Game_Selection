from random import choice
from utils import print_wrapped, delayed_input, set_skip_all, ReturnToMenu, check_input
from games_package import Guessing_Game, Rock_Paper_Scissors, Infinity_Game
from games_package.Role_Playing_Death_Game import role_playing_game


print_wrapped()
print_wrapped("Aspects of this code are paced for immersion.", newline_delay=0.75)
print_wrapped("To opt out and skip all delays, press [S] + Enter,", newline_delay=0.75)
print_wrapped("Or press Enter to continue (and allow immersion). ")
_choice = delayed_input("> ").strip().lower()   # uses prompt_input()
set_skip_all(_choice == "s")


print()
print_wrapped("Hello!", newline_delay=1)
print_wrapped("Welcome to the game selection menu.", newline_delay=1)
print_wrapped("Enter 'q' or 'quit' at any time to return to this menu.", newline_delay=1.5)
while True:
    print_wrapped()
    print_wrapped("Which game would you like to play?", newline_delay=1)
    print_wrapped("1) Guessing Game", newline_delay=0.5)
    print_wrapped("2) Rock Paper Scissors", newline_delay=0.5)
    print_wrapped("3) Infinity Game", newline_delay=0.5)
    print_wrapped("4) Role Playing Game", newline_delay=0.5)
    print_wrapped("0) Quit Game Selection", newline_delay=0.5)
    game_selection = delayed_input("""
Type 'Help' or 'H' for help. 
> """).strip().lower()
    if game_selection == "1":
        Guessing_Game.guessing_game()
    elif game_selection == "2":
        Rock_Paper_Scissors.rock_paper_scissors()
    elif game_selection == "3":
        Infinity_Game.infinity_game()
    elif game_selection == "4":
        role_playing_game()
    elif game_selection == "0":
        confirm_quit = delayed_input("\nAre you sure you want to quit? Yes/Y/0/Enter to quit. "
                             "\n > ").lower()
        if confirm_quit in ["yes", "y", "0", ""]:
            print_wrapped("Quitting now. Thanks for playing!")
            quit()
    elif game_selection in ["help", "h"]:
        print_wrapped("""\nHelp Menu - select one of the following options by typing your choice (1-4, or 0):
 1) Guessing Game
 2) Rock Paper Scissors
 3) Infinity Game
 4) Role Playing Game
 0) Quit Game Selection
 \n > """)
    else:
        print_wrapped("Invalid input. Please try again.")

