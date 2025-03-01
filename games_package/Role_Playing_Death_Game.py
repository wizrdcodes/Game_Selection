def role_playing_game():
    import random
    from utils import check_input, ReturnToMenu


    death_scenarios = {
        "fall": ["Try to grab onto something.", "Flap your arms wildly.",
                 "Throw your rope towards something sturdy.", "Aim for a softer impact."],
        "beast": ["Beg for mercy.", "Try to fight back.", "Flee as fast as you can.",
                  "Try to distract the beast."],
        "drowning": ["Swim up to resurface.", "Call for help.", "Reach out for a final grasp.",
                     "Hold your breath."],
        "trapped": ["Look for an escape route.", "Accept your fate.", "Strike the wall."],
        "ghost": ["Plead with the spirit.", "Use a protective charm.", "Defend yourself.",
                  "Pray for protection."],
        "void": ["Try to float.", "Close your eyes and accept fate.", "Ponder what went wrong.",
                 "Wake up from this nightmare."],
        "fire": ["Stop, drop, and roll.", "Try to outrun the flames.", "Drink a fire resistance potion.",
                 "Find water to douse the flame."],
        "curse": ["Pray for salvation.", "Attempt to break the curse.", "Chant a counter-spell.",
                  "Drink a healing potion."],
        "poison": ["Drink a strong antidote.", "Chew on healing herbs.", "Cut off the exposed limb..."],
        "lightning": ["Ground yourself with a metal rod.", "Seek shelter under anything sturdy."]
    }

    final_deaths = {
        "fall": ["Your fingers slip, and you plummet into darkness.", "Flapping does nothing. Gravity does.",
                 "You forgot to grasp your end of the rope...",
                 "There is no softer surface. Did you think this was a movie?"],
        "beast": ["The beast is unmoved. It strikes.", "You get a few hits in, but the beast is stronger.",
                  "The beast is faster...after all, you only have two legs.",
                  "The beast, insulted, rips you apart."],
        "drowning": ["You surface, gasping...only for the current to drag you under again.",
                     "No one hears your screams.", "There was nothing to grasp.",
                     "You never see the surface again."],
        "trapped": ["You claw at the walls until exhaustion takes you.",
                    "You sit quietly as darkness consumes you.",
                    "The echoes of your efforts drive you mad."],
        "ghost": ["The ghost listens...then takes your soul anyway.",
                  "The charm glows but shatters. You fade away.",
                  "Earthly things are meaningless. You cross over to the other side.",
                  "You're on your own. You feel your soul fade away."],
        "void": ["The void does not care. You keep falling.", "You drift away, dissolving into nothingness.",
                 "Maybe if you made a different decision, you would still be alive.", "You aren't dreaming."],
        "fire": ["The air burns your lungs. You collapse.", "The fire is faster. It overtakes you.",
                 "Fire consumes you. Did you use the right ingredients?",
                 "There is no water nearby...you perish."],
        "curse": ["No god answers. Your body crumbles to dust.", "The curse fights back. You are consumed.",
                  "You cast the spell incorrectly. The curse takes you.",
                  "It's too late...the potion did not act fast enough."],
        "poison": ["No remedy can halt the venom...you lose consciousness forever",
                   "The slow-acting herbs are not enough. Toxicity overwhelms you.",
                   "You stopped the poison...and inevitably your heart. You lost too much blood."],
        "lightning": ["A searing bolt of lightning strikes you, leaving only the metal rod behind.",
                      "There is no shelter from nature's fury. Electricity surges through you in an instant, turning you to ash."]
    }


    def get_random_choice(options):
        selected = random.sample(options, 2)
        print()
        for i, option in enumerate(selected, start=1):
            print(f"{i}. {option['description']}")
        try:
            choice = check_input("\n> ").strip()
        except ReturnToMenu:
            return None
        if choice == "1":
            return selected[0]
        elif choice == "2":
            return selected[1]
        else:
            print("Invalid input. Please try again.")
            return get_random_choice(options)


    # Set up for various path choices
    def scene_dark_forest():
        print("\nThe trees whisper as you step forward. The path splits ahead.")

        options = [
            {"description": "Follow the glowing mushrooms.",
                "handler": scene_glowing_mushrooms},
            {"description": "Walk towards the eerie howling sound.",
                "handler": scene_howling_sound},
            # {"description": "Follow the lone stone road.",
            #     "handler": scene_stone_road}
        ]
        try:
            choice = get_random_choice(options)
            choice['handler']()
        except ReturnToMenu:
            return None


    def scene_glowing_mushrooms():
        print("\nYou follow the mushrooms into a golden mist.")
        print("1. Drink a protection potion and continue.")
        print("2. Turn back immediately.")
        try:
            choice = check_input("> ")
        except ReturnToMenu:
            return
        if choice == "1":
            game_over("As the mist brushes against your skin, you become paralyzed. Did you brew the potion correctly?", "curse")
        elif choice == "2":
            game_over("The mist has already reached you...you start to lose your sight to the mist.", "curse")
        else:
            print("\nInvalid choice. Try again.")
            scene_glowing_mushrooms()


    def scene_howling_sound():
        print("\nAs you peer through the branches, a pair of yellow eyes fixates on you from the shadows...")
        print("1. Wield your sword in preparation.")
        print("2. Slowly back away into the shadows.")
        try:
            choice = check_input("\n> ").strip()
        except ReturnToMenu:
            print("Returning to menu...")
            return None
        if choice == "1":
            game_over(
                "The wolf attacks...you swing your sword...into a tree. Despite your best efforts...it overcomes you.",
                "beast")
        elif choice == "2":
            game_over("The wolf still smells you...you've become easy prey. It bears its teeth and strikes.", "beast")
        else:
            print("\nInvalid choice. Try again.")
            scene_howling_sound()


    def scene_abandoned_castle():
        print("\nThe castle looms ahead. You find two staircases.") # Upstairs and downstairs...how to always have an upstairs or downstairs?

        options = [
            {"description": "Go upatairs to the grand hall.",
             "handler": scene_grand_hall},
            {"description": "Walk towards the eerie howling sound.",
             "handler": scene_dungeon},
            # {"description": "Go up to the lone tower.",
            #     "handler": scene_lone_tower}
        ]
        try:
            choice = get_random_choice(options)
            choice['handler']()
        except ReturnToMenu:
            return None


    def scene_grand_hall():
        print("\nYou find dozens of chests filled with treasure next to an empty throne.")
        print("1. Step up to the throne and take your seat.")
        print("2. Grab your treasure and admire its glory.")
        try:
            choice = check_input("> ")
        except ReturnToMenu:
            return
        if choice == "1":
            game_over("As the mist brushes against your skin, you become paralyzed. Did you brew the potion correctly?",
                      "curse")
        elif choice == "2":
            game_over("The mist has already reached you...you start to lose your sight to the mist.", "curse")
        else:
            print("\nInvalid choice. Try again.")
            scene_grand_hall()


    def scene_dungeon():
        print("\nYou find two large, locked doors. A set of keys hangs from a nail between them.")
        print("1. Unlock and enter the door on the left.")
        print("2. Unlock and enter the door on the right.")

        try:
            choice = check_input("\n> ").strip()
        except ReturnToMenu:
            print("Returning to menu...")
            return None

        if choice == "1":
            game_over("A prisoner in chains lunges at you. You awake, finding the door locked.", "trapped")
        elif choice == "2":
            game_over("You begin to feel death's grasp as a ghoul emerges from the shadows.", "ghost")
        else:
            print("\nInvalid choice. Try again.")
            scene_dungeon()


    def scene_forgotten_cavern():
        print("\nThe cavern is dark and cold. You see two paths ahead.")

        options = [
            {"description": "Light a torch and explore deeper.",
             "handler": scene_explore_deeper},
            {"description": "Follow the sound of rushing water.",
             "handler": scene_rushing_water},
        ]
        try:
            choice = get_random_choice(options)
            choice['handler']()
        except ReturnToMenu:
            return None


    def scene_explore_deeper():
        print("\nYou find a skeleton of armor holding a glowing rune.")
        print("1. Examine the markings on the rune.")
        print("2. Remove the rune from the skeleton's grasp.")

        try:
            choice = check_input("\n> ").strip()
        except ReturnToMenu:
            print("Returning to menu...")
            return None

        if choice == "1":
            game_over("The markings warn that fire will consume any who dare to read the markings.", "fire")
        elif choice == "2":
            game_over("As soon as you move the rune, a fierce rumbling brings the rocks around you crashing down.",
                      "trapped")
        else:
            print("\nInvalid choice. Try again.")
            scene_explore_deeper()


    def scene_rushing_water():
        print("\nYou find an underground river, flowing at a moderate speed.")
        print("1. Refill your canteen to prepare for the remainder of your journey.")
        print("2. Carefully follow along the river to see where it ends.")

        try:
            choice = check_input("\n> ").strip()
        except ReturnToMenu:
            print("Returning to menu...")
            return None

        if choice == "1":
            game_over("The river reaches out to you, pulling you off your feet and under itself.", "drowning")
        elif choice == "2":
            game_over("You've underestimated the cave. You slip and the current takes you.", "drowning")
        else:
            print("\nInvalid choice. Try again.")
            scene_rushing_water()


    def scene_misty_bridge():
        print("\nThe bridge sways as you step onto it, fog obscuring your vision.")

        options = [
            {"description": "Walk slowly and carefully.",
             "handler": scene_walk_slowly},
            {"description": "Run across before the mist thickens.",
             "handler": scene_run_across},
            # {"description": "Follow the lone stone road.",
            #     "handler": scene_stone_road}
        ]
        try:
            choice = get_random_choice(options)
            choice['handler']()
        except ReturnToMenu:
            return None


    def scene_walk_slowly():
        print("\nWith every step, your vision becomes more and more obscured from the fog.")
        print("1. Light a torch to light the way and avoid misstepping.")
        print("2. Carefully test each step ahead of you.")

        try:
            choice = check_input("\n> ").strip()
        except ReturnToMenu:
            print("Returning to menu...")
            return None

        if choice == "1":
            game_over("You accidentally light the bridge on fire...dropping you into the abyss.", "fall")
        elif choice == "2":
            game_over("A reaper appears from the fog and steals your soul.", "ghost")
        else:
            print("\nInvalid choice. Try again.")
            scene_walk_slowly()


    def scene_run_across():
        print("\nYou hear the bridge snap and creak, the old wood and rope becoming undone.")
        print("1. Try to cross quickly before the bridge gives way.")
        print("2. Stop running to avoid moving the bridge too much.")

        try:
            choice2 = check_input("\n> ").strip()
        except ReturnToMenu:
            print("Returning to menu...")
            return None

        if choice2 == "1":
            game_over("Your movements overwhelm the bridge...and fall into the abyss.", "fall")
        elif choice2 == "2":
            game_over("Your sudden halt snaps the rope...the bridge fails and you fall into the abyss.", "fall")
        else:
            print("\nInvalid choice. Try again.")
            scene_run_across()


    def scene_mountain_of_echoes():
        print("\nThe wind howls as you climb higher.")

        options = [
            {"description": "Seek shelter in a small cave.",
             "handler": scene_seek_shelter},
            {"description": "Push forward.",
             "handler": scene_push_forward},
        ]
        try:
            choice = get_random_choice(options)
            choice['handler']()
        except ReturnToMenu:
            return None


    def scene_seek_shelter():
        print("\nYou find a beast sleeping in the cave, surrounded by bones.")
        print("1. Unsheathe your blade and prepare for the worst.")
        print("2. Abandon the cave and chance the mountain path.")

        try:
            choice2 = check_input("\n> ").strip()
        except ReturnToMenu:
            print("Returning to menu...")
            return None

        if choice2 == "1":
            game_over("The beast is larger than you thought...you knew your chances were slim.", "beast")
        elif choice2 == "2":
            game_over("You exit the cave too quickly, and lose your footing...", "fall")
        else:
            print("\nInvalid choice. Try again.")
            scene_seek_shelter()


    def scene_push_forward():
        print("\nYou see the peak of the icy mountain ahead, merely a few feet away.")
        print("1. Push forward to the peak.")
        print("2. Stop to admire the view.")

        try:
            choice2 = check_input("\n> ").strip()
        except ReturnToMenu:
            print("Returning to menu...")
            return None

        if choice2 == "1":
            game_over("The peak was an illusion. You step into the void.", "void")
        elif choice2 == "2":
            game_over("The ice beneath you gives way, dropping you into the void.", "void")
        else:
            print("\nInvalid choice. Try again.")
            scene_push_forward()


    def game_over(reason, death_type):
        """Gives the player a final chance before their inevitable demise, based on the cause."""
        print(f"\n{reason}")
        print("You have one last chance to survive...")

        options = death_scenarios.get(death_type, ["Do nothing.", "Panic.", "Try to wake from this nightmare."])
        selected_indices = random.sample(range(len(options)), 2)
        print()
        print(f"1. {options[selected_indices[0]]}")
        print(f"2. {options[selected_indices[1]]}")

        try:
            choice = check_input("\n> ").strip()
        except ReturnToMenu:
            print("Returning to menu...")
            return None

        if choice == "1":
            chosen_index = selected_indices[0]
        elif choice == "2":
            chosen_index = selected_indices[1]
        else:
            print("\nYou hesitated... and that was your downfall.")
            return

        print(f"\n{final_deaths[death_type][chosen_index]}")

        print("\nYou have died. Would you like to try again? (yes/no)")
        retry = input("> ").strip().lower()
        if retry in ["yes", "y"] or retry not in ["no", "n"]:
            start_game()
        else:
            print("\nThanks for playing!")


    def start_game():
        """Starts the game and presents the first set of choices."""
        print("\nWelcome, traveler. You stand at the entrance of a mysterious land.")
        print("What do you do?")
        print("\n1. Enter the Dark Forest.")
        print("2. Walk toward the Abandoned Castle.")
        print("3. Descend into the Forgotten Cavern.")
        print("4. Cross the Misty Bridge.")
        print("5. Climb the Mountain of Echoes.")

        try:
            choice = check_input("\n> ").strip()
        except ReturnToMenu:
            print("Returning to menu...")
            return None

        if choice == "1":
            scene_dark_forest()
        elif choice == "2":
            # Create scenes
            scene_abandoned_castle()
        elif choice == "3":
            scene_forgotten_cavern()
        elif choice == "4":
            scene_misty_bridge()
        elif choice == "5":
            scene_mountain_of_echoes()
        else:
            print("\nInvalid choice. Try again.")
            start_game()


    # Start the game
    start_game()

