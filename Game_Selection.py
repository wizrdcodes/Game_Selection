from utils import check_input, ReturnToMenu
from games_package import Guessing_Game, Rock_Paper_Scissors, Infinity_Game, Role_Playing_Death_Game


print("\nHello! Welcome to the game selection menu. Enter 'q' or 'quit' at any time to return to this menu.")
while True:
    game_selection = input("""Which game would you like to play? 
 \n1) Guessing Game
2) Rock Paper Scissors
3) Infinity Game
4) Role Playing Game
0) Quit Game Selection
\nType 'Help' or 'H' for help. 
\n> """).strip().lower()
    if game_selection == "1":
        Guessing_Game.guessing_game()
    elif game_selection == "2":
        Rock_Paper_Scissors.rock_paper_scissors()
    elif game_selection == "3":
        Infinity_Game.infinity_game()
    elif game_selection == "4":
        Role_Playing_Death_Game.role_playing_game()
    elif game_selection == "0":
        confirm_quit = input("\nAre you sure you want to quit? Yes/Y/0/Enter to quit. "
                             "\n > ").lower()
        if confirm_quit == "yes" or "y" or "0":
            print("Quitting now. Thanks for playing!")
            quit()
    elif game_selection in ["help", "h"]:
        print("""\nHelp Menu - select one of the following options by typing your choice (1-4, or 0):
 1) Guessing Game
 2) Rock Paper Scissors
 3) Infinity Game
 4) Role Playing Game
 0) Quit Game Selection
 \n > """)
    else:
        print("Invalid input. Please try again.")

