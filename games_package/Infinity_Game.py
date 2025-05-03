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
        "\nAre you positive you want to type '0'? "
    ]

    yes_variants = [
        "yes", "yeah", "yep", "yup", "yea", "y", "0",
        "i do", "i really do", "im sure", "i'm sure", "i am",
        "i am sure", "i'm really sure", "im really sure", "i'm really really sure",
        "im really really sure", "i am really sure", "i am really really sure", "i want to",
        "i really want to", "i really really want to", "i do want to", "im going to anyways",
        "i really do want to", "i really really do want to", "sucks for you", "i'm going to anyways",
        "too bad", "i want to anyway", "i'm going to anyway", "im going to anyway", "i will anyway",
        "why not", "why not?", "why", "sure", "want to", "do want to", "anyway", "im positive",
        "i'm positive", "i will", "i would anyway", "i will anyways", "idc", "i dont care", "i don't care"
    ]

    print("\nHello! Welcome to the Infinity Game!")

    def input_structure(string):
        user_response = input(f'{string}\n\n> ').strip().lower()
        return user_response

    while True:
        # Initial question loop (infinite until valid input)
        user_input = input_structure("\nType something...(just not '0') ")
        if user_input == "0":
            break  # Exit to confirmation sequence if valid input is given

    # Confirmation loop, ensuring user must enter yes variant to proceed
    shuffled_prompts = confirm_prompts[:]
    random.shuffle(shuffled_prompts)
    prompt_index = 0

    while loop_counter < 7:
        # If we’ve gone through all prompts, reshuffle and restart
        if prompt_index >= len(shuffled_prompts):
            random.shuffle(shuffled_prompts)
            prompt_index = 0

        response_confirmation = shuffled_prompts[prompt_index]
        user_input = input_structure(response_confirmation)

        if user_input in yes_variants:
            loop_counter += 1
            prompt_index += 1
        else:
            # If the user types anything else, send them back to the initial question
            while True:
                user_input = input_structure("\nType something...(just not '0') ")
                if user_input == "0":
                    break  # Return to confirmation sequence

    print("\nOkay! Goodbye!")
