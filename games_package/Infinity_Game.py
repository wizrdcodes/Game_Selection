def infinity_game():
    import random

    loop_counter = 0

    confirm_prompts = [
        "\nAre you sure you want to type '0'?... ",
        "\nAre you really sure you want to type '0'? ",
        "\nAre you really, really sure you want to type '0'? ",
        "\nOkay, suit yourself...if you really want to... ",
        "\nWhat if I told you that you shouldn't type '0'? ",
        "\nDo you want to type '0'? ",
        "\nDo you really want to type '0'? ",
        "\nDo you really, really want to type '0'? ",
    ]

    yes_variants = [
        "yes", "yeah", "yep", "yup", "yea", "y", "0",
        "i do", "i really do", "im sure", "i'm sure", "i am",
        "i am sure", "i'm really sure", "i'm really really sure",
        "i am really sure", "i am really really sure", "i want to",
        "i really want to", "i really really want to", "i do want to",
        "i really do want to", "i really really do want to", "sucks for you",
        "too bad", "i want to anyway", "i'm going to anyway", "i will anyway",
        "why not", "why not?", "why", "sure", "want to", "do want to", "anyway"
    ]

    print("\nHello! Welcome to Infinity Game!")

    while True:
        # Initial question loop (infinite until valid input)
        user_input = input("\nType something...(just not '0') >> ").strip().lower()
        if user_input == "0":
            break  # Exit to confirmation sequence if valid input is given

    # Confirmation loop, ensuring user must enter "0", "yes", or "y" to proceed
    while loop_counter < 7:
        user_input = input(random.choice(confirm_prompts)).strip().lower()
        if any(variant in user_input for variant in yes_variants):
            loop_counter += 1
        else:
            # If the user types anything else, send them back to the initial question
            while True:
                user_input = input("\nType something...(just not '0') >> ").strip().lower()
                if user_input == "0": # if user_input.lower() in yes_variants:
                    break  # Return to confirmation sequence

    print("\nOkay! Goodbye!")

