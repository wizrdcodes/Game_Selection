from utils import check_input, ReturnToMenu, print_wrapped, delayed_input


def guessing_game():
    #Looping Guessing Game
    import random


    def play_guessing_game():
        answer = random.randint(1, 10)
        guess_count = 0
        guess_limit = 3

        print_wrapped("""\nWelcome to the Guessing Game! I've chosen a number between 1 and 10.
You have three chances to guess the number. Good luck!""", newline_delay=1.5)

        while guess_count < guess_limit:  # Changed <= to < to allow exactly guess_limit tries
            try:
                guess = check_input("\nGuess: ")
            except ReturnToMenu:
                return None
            try:
                guess = int(guess)  # Convert guess to int here
            except ValueError:
                print_wrapped("That's not a number!", newline_delay=1)
                continue  # Skip to the next iteration without incrementing guess_count

            guess_count += 1

            if guess == answer:
                print_wrapped("You got it!", newline_delay=1)
                return True  # Indicate a win
            elif guess < answer:
                print_wrapped("Too low!", newline_delay=1)
            else:
                print_wrapped("Too high!", newline_delay=1)

        print_wrapped(f"You lost! The answer was {answer}. Better luck next time.", newline_delay=1.5)
        return False # Indicate a loss

    while True: #Loop to play again
        play_guessing_game()
        play_again = delayed_input("\nDo you want to play this game again? [Y]es / [N]o): ").lower()
        if play_again not in ["yes", "y"] or play_again in ["no", "n"]:
            break
        else:
            print_wrapped("I didn't catch that...", newline_delay=1)

    print_wrapped("Thanks for playing!", newline_delay=1)


