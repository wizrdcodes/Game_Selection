from utils import ReturnToMenu, check_input, print_wrapped, delayed_input


def rock_paper_scissors():
    import random

    print_wrapped("\nLet's play rock, paper, or scissors!", newline_delay=1)
    print_wrapped("Best out of three wins...", newline_delay=1)

    def play_rock_paper_scissors():
        player_wins = 0
        computer_wins = 0
        winner = None

        while player_wins < 2 and computer_wins < 2:
            try:
                player_choice = delayed_input("\nChoose (R)ock, (P)aper, or (S)cissors: ").lower()
            except ReturnToMenu:
                return None

            computer_choices = ["rock", "paper", "scissors"]
            computer_choice = random.choice(computer_choices)
            print_wrapped(f"\nComputer chose: {computer_choice}", newline_delay=1)

            rock_choices = ["rock", "r"]
            paper_choices = ["paper", "p"]
            scissors_choices = ["scissors", "s"]

            if (player_choice.lower() in rock_choices and computer_choice == "scissors") or (
                    player_choice.lower() in paper_choices and computer_choice == "rock") or (
                    player_choice.lower() in scissors_choices and computer_choice == "paper"):
                winner = "Player"

            elif (player_choice.lower() in rock_choices and computer_choice == "rock") or (
                    player_choice.lower() in paper_choices and computer_choice == "paper") or (
                    player_choice.lower() in scissors_choices and computer_choice == "scissors"):
                winner = "Tie"

            elif (player_choice.lower() in rock_choices and computer_choice == "paper") or (
                    player_choice.lower() in paper_choices and computer_choice == "scissors") or (
                    player_choice.lower() in scissors_choices and computer_choice == "rock"):
                winner = "Computer"
            else:
                print_wrapped("You didn't type a valid option...", newline_delay=1)
                continue

            if winner == "Player":
                player_wins += 1
                print_wrapped("You won!", newline_delay=1)

            elif winner == "Computer":
                computer_wins += 1
                print_wrapped("Computer won :)", newline_delay=1)

            else:
                print_wrapped("It's a tie!", newline_delay=1)

            print_wrapped(f"Score - Player: {player_wins}, Computer: {computer_wins}", newline_delay=1)

        if player_wins > computer_wins:
            print_wrapped("Congratulations! You won!", newline_delay=1)
        else:
            print_wrapped("Computer won. Better luck next time! ", newline_delay=1)

    while True: #Loop to play again
        play_rock_paper_scissors()
        play_again = delayed_input("\nDo you want to play this game again? [Y]es / [N]o: ").lower()
        if play_again not in ["yes", "y"] or play_again in ["no", "n"]:
            break
        else:
            print_wrapped("I didn't catch that...", newline_delay=1)

    print_wrapped("Thanks for playing!", newline_delay=1)