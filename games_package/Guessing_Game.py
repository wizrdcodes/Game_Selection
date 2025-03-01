from utils import check_input, ReturnToMenu


def guessing_game():
    #Looping Guessing Game
    import random


    def play_guessing_game():
        answer = random.randint(1, 10)
        guess_count = 0
        guess_limit = 3

        print("""\nWelcome to the Guessing Game! I've chosen a number between 1 and 10.
You have three chances to guess the number. Good luck!""")

        while guess_count < guess_limit:  # Changed <= to < to allow exactly guess_limit tries
            try:
                guess = check_input("\nGuess: ")
            except ReturnToMenu:
                return None
            try:
                guess = int(guess)  # Convert guess to int here
            except ValueError:
                print("That's not a number!")
                continue  # Skip to the next iteration without incrementing guess_count

            guess_count += 1

            if guess == answer:
                print("You got it!")
                return True  # Indicate a win
            elif guess < answer:
                print("Too low!")
            else:
                print("Too high!")

        print(f"You lost! The answer was {answer}. Better luck next time.")
        return False # Indicate a loss

    while True: #Loop to play again
        play_guessing_game()
        play_again = input("\nDo you want to play this game again? (yes/no): ").lower()
        if play_again not in ["yes", "y"] or play_again in ["no", "n"]:
            break
        else:
            print("I didn't catch that...")

    print("Thanks for playing!")


