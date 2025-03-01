from utils import ReturnToMenu, check_input


def rock_paper_scissors():
    import random

    print("\nLet's play rock, paper, or scissors!")

    def play_rock_paper_scissors():
        player_wins = 0
        computer_wins = 0
        winner = None

        while player_wins < 2 and computer_wins < 2:
            try:
                player_choice = check_input("\nChoose rock, paper, or scissors: ").lower()
            except ReturnToMenu:
                return None

            choices = ["rock", "paper", "scissors"]
            computer_choice = random.choice(choices)
            print(f"\nComputer chose: {computer_choice}")

            if (player_choice == "rock" and computer_choice == "scissors") or (
                    player_choice == "paper" and computer_choice == "rock") or (
                    player_choice == "scissors" and computer_choice == "paper"):
                winner = "Player"

            elif (player_choice == "rock" and computer_choice == "rock") or (
                    player_choice == "paper" and computer_choice == "paper") or (
                    player_choice == "scissors" and computer_choice == "scissors"):
                winner = "Tie"

            elif (player_choice == "rock" and computer_choice == "paper") or (
                    player_choice == "paper" and computer_choice == "scissors") or (
                    player_choice == "scissors" and computer_choice == "rock"):
                winner = "Computer"
            else:
                print("You didn't type a valid option...")
                continue

            if winner == "Player":
                player_wins += 1
                print("You won")

            elif winner == "Computer":
                computer_wins += 1
                print("Computer won")

            else:
                print("It's a tie")

            print(f"Current Score - Player: {player_wins}, Computer: {computer_wins}")

        if player_wins > computer_wins:
            print("Congratulations! You won")
        else:
            print("Computer won. Better luck next time! ")

    while True: #Loop to play again
        play_rock_paper_scissors()
        play_again = input("\nDo you want to play this game again? (yes/no): ").lower()
        if play_again not in ["yes", "y"] or play_again in ["no", "n"]:
            break
        else:
            print("I didn't catch that...")

    print("Thanks for playing!")