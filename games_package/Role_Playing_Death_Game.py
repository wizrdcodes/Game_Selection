from requests import options


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
        "trapped": ["Look for an escape route.", "Accept your fate.", "Strike with your sword."],
        "ghost": ["Plead with the spirit.", "Use a protective charm.", "Defend yourself.",
                  "Pray for protection."],
        "void": ["Try to float.", "Close your eyes and accept fate.", "Ponder what went wrong.",
                 "Wake up from this nightmare."],
        "fire": ["Stop, drop, and roll.", "Try to outrun the flames.", "Drink a fire resistance potion.",
                 "Find water to douse the flame."],
        "curse": ["Pray for salvation.", "Attempt to break the curse.", "Chant a counter-spell.",
                  "Drink a healing potion."],
        "poison": ["Drink a strong antidote.", "Chew on healing herbs.", "Cut off the exposed limb..."],
        "lightning": ["Ground yourself with a metal rod.", "Seek shelter under anything sturdy."],
        "enemy": ["Plead for forgiveness.", "Try to attack one last time.", "Hope for mercy."],
        "mortal peril": ["Drink a healing potion.", "Pray for a miracle."]
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
        "trapped": ["You claw away until exhaustion takes you.",
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
        "curse": ["No god answers. You succumb to the curse forever.", "The curse fights back. You are consumed.",
                  "You cast the spell incorrectly. The curse overcomes you.",
                  "It's too late...the potion won't save you."],
        "poison": ["No remedy can halt the venom...you lose consciousness forever",
                   "The slow-acting herbs are not enough. Toxicity overwhelms you.",
                   "You stopped the poison...and inevitably your heart. You lost too much blood."],
        "lightning": ["A searing bolt of lightning strikes you, leaving only the metal rod behind.",
                      "There is no shelter from nature's fury. Electricity surges through you in an instant, "
                      "turning you to ash."],
        "enemy": ["Your words fall on deaf ears.", "It's too late...you've met your peril.", "Your foe shows no mercy."],
        "mortal peril": ["You didn't pass potions class...", "No one answers your prayers."]
    }

    def check_or_return_none():
        try:
            choice = check_input("\n> ").strip()
            return choice
        except ReturnToMenu:
            print("Quitting...")
            return None

    def get_random_choice(options, num_choices=2):
        if num_choices > len(options):
            num_choices = len(options)
        selected = random.sample(options, num_choices)
        while True:
            print()
            for i, option in enumerate(selected, start=1):
                print(f"{i}. {option['description']}")
            choice = check_or_return_none()
            if choice is None:
                return None
            if choice.isdigit():
                choice_index = int(choice) - 1
                if 0 <= choice_index < len(selected):
                    return selected[choice_index]
            print("Invalid input. Please try again.")

    def check_and_run_random_handler(options, num_choices=2):
        try:
            choice = get_random_choice(options, num_choices)
            if choice is None:
                return
            choice['handler']()
        except ReturnToMenu:
            print("Quitting...")
            return None

    game_state = {
        "book_on_pedestal": True,
        "orb_on_table": True,
        "mushrooms": False,
        "stone_road": False,
        "howling_sound": False,
        "noise_count": 0
    }

    def scene_dark_forest():
        print("\nThe trees whisper as you step forward. The path splits ahead.")
        options = [
            {"description": "Follow the glowing mushrooms.", "handler": scene_glowing_mushrooms},
            {"description": "Walk towards the eerie howling sound.", "handler": scene_howling_sound},
            {"description": "Venture down the lone cobblestone road.", "handler": scene_stone_road}
        ]
        check_and_run_random_handler(options, 3)

    def scene_glowing_mushrooms():
        game_state["mushrooms"] = True
        print("\nAs you walk along the mushrooms, you notice the mushrooms quickly growing, blocking the path forward "
              "and backwards.")
        options = [
            {"description": "Climb the mushrooms to stay above them.", "handler": scene_climb_mushrooms},
            {"description": "Turn back to avoid this unnatural nature.", "handler": scene_turn_back},
            {"description": "Cut down the mushrooms growing in your way.", "handler": scene_cut_mushrooms},
        ]
        check_and_run_random_handler(options, 3)

    def scene_climb_mushrooms():
        print("\nAs you climb the mushrooms, you see an old wooden nest above in a tree.")
        options = [
            {"description": "Keep climbing towards the tree.", "handler": scene_climb_to_tree},
            {"description": "Jump towards the platform to grab its ledge.", "handler": scene_jump_to_platform}
        ]
        check_and_run_random_handler(options)

    def scene_climb_to_tree():
        game_over("The mushrooms stop growing...spraying a golden mist at you. As the mist touches you, "
                  "your movements slow.", "curse")

    def scene_jump_to_platform():
        print("\nYou grab the ledge, the mushrooms underneath you spraying a golden mist where you once stood.")
        options = [
            {"description": "Climb higher to check your surroundings.", "handler": scene_climb_tree},
            {"description": "Take a moment to rest and gather your bearings.", "handler": scene_rest_on_platform}
        ]
        check_and_run_random_handler(options)

    def scene_rest_on_platform():
        game_over("The mist from the mushrooms rises up to you. As it touches your skin, you feel your limbs begin to "
                  "slow.", "curse")

    def scene_climb_tree():
        print("\nYou notice the golden mist rising to where you were just standing...")
        options = [
            {"description": "Abandon the tree and jump to another.", "handler": scene_jump_to_tree},
        ]
        check_and_run_random_handler(options)

    def scene_jump_to_tree():
        game_over("You're not as nimble as you think. You slip and fall into the mist...which numbs your body and "
                  "slows your movement.", "curse")

    def scene_cut_mushrooms():
        game_over("As you cut the mushrooms, they spray a golden mist at you...which paralyzes your limbs one at a "
                  "time.", "curse")

    def scene_stone_road():
        game_state["stone_road"] = True
        print("\nAs you follow the road, the sounds of creaking wood and ruffling leaves seem to surround you.")
        options = [
            {"description": "Get off the road.", "handler": scene_get_off_road},
            {"description": "Unsheathe your sword.", "handler": scene_unsheathe_sword}
        ]
        check_and_run_random_handler(options)

    def scene_get_off_road():
        game_over("As you walk into the bushes, your skin brushes against poisonous thorns that shoot pain through "
                  "your body.", "poison")

    def scene_unsheathe_sword():
        print("\nTo your amazement, branches begin swinging at you. You tear them all down...until a giant tree shows "
              "itself.")
        options = [
            {"description": "Cut at the tree's trunk.", "handler": scene_cut_trunk},
            {"description": "Flee the giant tree.", "handler": scene_flee_tree},
        ]
        check_and_run_random_handler(options)

    def scene_cut_trunk():
        game_over("The tree's trunk is too thick...your sword is not enough.", "enemy")

    def scene_flee_tree():
        game_over("The giant tree is too large...as you run, it swings its long branches at you.", "enemy")



        # print("1. Drink a protection potion and continue.")
        # print("2. Turn back immediately.")
        # try:
        #     choice = check_input("> ")
        # except ReturnToMenu:
        #     print("Returning to menu...")
        #     return None
        # if choice == "1":
        #     game_over("As the mist brushes against your skin, you become paralyzed. Did you brew the potion correctly?", "curse")
        # elif choice == "2":
        #     game_over("The mist has already reached you...you start to lose your sight to the mist.", "curse")
        # else:
        #     print("\nInvalid choice. Try again.")
        #     scene_glowing_mushrooms()

    def scene_howling_sound():
        game_state["howling_sound"] = True
        print("\nAs you peer through the branches, pairs of yellow eyes fixate on you from the shadows...")
        options = [
            {"description": "Wield your sword in preparation.", "handler": scene_wield_sword},
            {"description": "Slowly back away into the shadows.", "handler": scene_back_away},
            {"description": "Turn back before meeting the holders of these eyes.", "handler": scene_turn_back},
        ]

        check_and_run_random_handler(options, 3)

    def scene_wield_sword():
        print("\nOne by one, vicious wolves lunge at you. You strike them down, each retreating, one by one...until "
              "the alpha emerges.")
        options = [
            {"description": "Stand ready.", "handler": scene_stand_ready},
            {"description": "Surrender and submit.", "handler": scene_surrender},
        ]
        check_and_run_random_handler(options)

    def scene_stand_ready():
        game_over("The alpha attacks...and you swing your sword...into a tree. Despite your best efforts...it "
                  "overcomes you.", "beast")

    def scene_surrender():
        game_over("\nThe alpha does not show mercy. It bears its teeth and strikes.", "beast")

    def scene_back_away():
        game_over("The beasts still smell you...you are easy prey. After not watching your back, a wolf lunges at you "
                  "from behind.", "beast")

    def scene_turn_back():
        if game_state["mushrooms"]:
            print("\nThe glowing mushrooms continue to rapidly grow, as if they do not want you to return from where "
                  "you came.")
            options = [
                {"description": "Cut down the mushrooms blocking your path.", "handler": scene_cut_mushrooms},
                {"description": "Weave through the mushrooms.", "handler": scene_weave_through_mushrooms}
            ]
            check_and_run_random_handler(options)
        elif game_state["stone_road"]:
            print("\nWhen you turn around, the cobblestone path behind you is gone, replaced with thick, bushy trees.")
            options = [
                {"description": "Continue forward into the forest.", "handler": scene_continue_into_forest},
                {"description": "Cut down the trees.", "handler": scene_cut_down_trees}
            ]
            check_and_run_random_handler(options)
        elif game_state["howling_sound"]:
            game_over("It's too late...a large wolf comes out of the shadows, bearing its fangs at you...", "beast")

    def scene_weave_through_mushrooms():
        game_over("As your skin brushes against the mushrooms, your skin burns more and more...bringing you to nearly "
                  "unbearable pain.", "poison")

    def scene_continue_into_forest():
        print("\nThe path forward is also gone...replaced with more trees...")
        options = [
            {"description": "Cut down the trees in your path.", "handler": scene_cut_down_trees}
        ]
        check_and_run_random_handler(options)

    def scene_cut_down_trees():
        game_over("As you cut at the trees, every time you blink, they reappear...after cutting the same trees over "
                  "and over, you realize you are unnaturally trapped.", "trapped")

    def scene_abandoned_castle():
        options = [
            {"description": "Go upstairs to the grand hall.", "handler": scene_grand_hall},
            {"description": "Descend into the dungeon.", "handler": scene_dungeon},
            {"description": "Climb up to the lone tower.", "handler": scene_lone_tower},
            {"description": "Head down to the library.", "handler": scene_library}
        ]
        selected = random.sample(options, 4)
        upstairs_keywords = ["up", "ascend", "upper", "tower", "upstairs"]
        downstairs_keywords = ["down", "descend", "dungeon", "basement", "cellar", "crypt"]
        upstairs = False; downstairs = False
        for option in selected:
            description = option["description"].lower()
            if any(keyword in description for keyword in upstairs_keywords):
                upstairs = True
            if any(keyword in description for keyword in downstairs_keywords):
                downstairs = True

        if upstairs and downstairs:
            print("\nThe castle looms ahead. You see paths leading up and down.")
        elif upstairs:
            print("\nThe castle looms ahead. The only way forward is up.")
        elif downstairs:
            print("\nThe castle looms ahead. The only way forward is down.")
        else:
            print("\nThe castle looms ahead. You stand at a crossroads.")

        check_and_run_random_handler(selected, 2)

    def scene_grand_hall():
        print("\nYou find dozens of chests filled with treasure next to an empty throne.")
        options = [
            {"description": "Step up to the throne and take your seat.", "handler": scene_sit_on_throne},
            {"description": "Pick up some treasure and admire its glory.", "handler": scene_admire_treasure},
        ]
        check_and_run_random_handler(options)

    def scene_sit_on_throne():
        print("\nAs you sit on the throne, you notice a boy watching you...signaling to follow him.")
        options = [
            {"description": "Follow the boy.", "handler": scene_follow_boy},
            {"description": "Ignore the boy. You're royalty!", "handler": scene_ignore_boy}
        ]
        check_and_run_random_handler(options)

    def scene_follow_boy():
        print("\nThe boy walks into a room. You step through the doorway to find more kids, keeping themselves "
              "entertained.")
        options = [
            {"description": "Ask the kids why they're alone.", "handler": scene_ask_why_alone},
            {"description": "Ask the boy who his friends are.", "handler": scene_ask_who_kids_are},
            {"description": "Leave the room.", "handler": scene_kids_surround_user},
        ]
        check_and_run_random_handler(options, 3)

    def scene_ask_why_alone():
        print("\nThe kids, confused, stare at you for a few seconds. One girl finally says, 'We've been alone for a "
              "long time.'")
        options = [
            {"description": "Ask the boy if he's seen any adults.", "handler": scene_ask_where_adults},
            {"description": "Distract the kids to make them less somber.", "handler": scene_make_kids_happy},
        ]
        check_and_run_random_handler(options)

    def scene_make_kids_happy():
        print("\nThe kids' mood lightens, and you see a few smile at you. The boy walks up to you and says, "
              "'You should stay with us forever.'")
        options = [
            {"description": "Pat the boy's head.", "handler": scene_pat_boys_head},
            {"description": "Tell the boy he's sweet, but you have to leave.", "handler": scene_kids_say_cant_leave}
        ]
        check_and_run_random_handler(options)

    def scene_pat_boys_head():
        print("\nYour hand passes through the boy's head as he looks up at you...awaiting your response. You realise "
              "you are the only living person in the room.")
        options = [
            {"description": "Tell the kids you'll be right back.", "handler": scene_kids_say_cant_leave},
            {"description": "Ask the kids to give you a minute alone.", "handler": scene_ask_kids_for_space},
        ]
        check_and_run_random_handler(options)

    def scene_ask_who_kids_are():
        print("\nThe boy says they're his friends. They just don't remember each other's names because it's been so "
              "long...")
        options = [
            {"description": "Ask the boy if there are any adults around.", "handler": scene_ask_where_adults},
            {"description": "Cheer up the kids with a joke or hand trick.", "handler": scene_make_kids_happy}
        ]
        check_and_run_random_handler(options)

    def scene_ignore_boy():
        print("\nThe boy disappears from your view. Within a moment, you see him again, a bit closer...facing away "
              "from you.")
        options = [
            {"description": "Address the boy.", "handler": scene_address_boy},
            {"description": "Stay seated and watch the boy.", "handler": scene_watch_boy}
        ]
        check_and_run_random_handler(options)

    def scene_address_boy():
        print("\nYou speak to the boy...but he doesn't answer. Instead, the air becomes freezing cold as the boy "
              "turns around.")
        options = [
            {"description": "Ask the boy if he's seen any adults.", "handler": scene_ask_where_adults},
            {"description": "Ask the boy what his name is.", "handler": scene_ask_boys_name},
        ]
        check_and_run_random_handler(options)

    def scene_ask_where_adults():
        print("\nThe boy nods and beckons for you to follow him. He brings you to a room littered with bodies.")
        options = [
            {"description": "Ask the boy what happened to these people.", "handler": scene_ask_about_bodies},
            {"description": "Tell the boy you'll be right back...and leave.", "handler": scene_kids_surround_user},
        ]
        check_and_run_random_handler(options)

    def scene_ask_about_bodies():
        print("\nThe boy says, 'They didn't want to play with us.'")
        options = [
            {"description": "Tell the boy not to worry, you'll play with them...but you have to leave for a minute.", "handler": scene_kids_surround_user},
            {"description": "Leave the boy in the room to escape the kids...", "handler": scene_kids_surround_user},
        ]
        check_and_run_random_handler(options)

    def scene_ask_boys_name():
        print("\nThe boy disappears...but you hear him say 'We don't remember our names. Will you play with us?'")
        scene_kids_surround_user()

    def scene_watch_boy():
        print("\nAs you sit on the throne, watching the boy, he disappears into thin air. You hear the boy crying, "
              "but he is nowhere to be seen.")
        options = [
            {"description": "Leave the grand hall.", "handler": scene_kids_surround_user},
            {"description": "Leave the throne.", "handler": scene_kids_surround_user},
        ]
        check_and_run_random_handler(options)

    def scene_kids_surround_user():
        print("\nThe boy suddenly appears before you. One by one, more and more ghostly kids appear out of thin "
              "air, surrounding you.")
        options = [
            {"description": "Tell the kids you'll be right back.", "handler": scene_kids_say_cant_leave},
            {"description": "Ask the kids to give you a minute alone.", "handler": scene_ask_kids_for_space}
        ]
        check_and_run_random_handler(options)

    def scene_kids_say_cant_leave():
        game_over("The boy says, 'You can't leave...you have to stay with us.' They reach out and grab you.", "ghost")

    def scene_ask_kids_for_space():
        game_over("The boy says, 'Being alone is bad...stay with us.' They reach out and grab you.", "ghost")

    def scene_admire_treasure():
        print("\nYou admire the shiny treasure...it must be worth more than you've ever seen in your life.")
        options = [
            {"description": "Take some treasure.", "handler": scene_treasure},
            {"description": "Find some treasure.", "handler": scene_treasure},
            {"description": "Grab some treasure.", "handler": scene_treasure},
            {"description": "Hold some treasure.", "handler": scene_treasure}
        ]
        check_and_run_random_handler(options)

    def scene_treasure():
        print("\nThere's something special about this treasure...you should protect it...it can't fall into the wrong "
              "hands...")
        options = [
            {"description": "Protect the treasure.", "handler": scene_treasure_2},
            {"description": "Guard the treasure.", "handler": scene_treasure_2},
            {"description": "Hoard the treasure.", "handler": scene_treasure_2},
            {"description": "Keep the treasure.", "handler": scene_treasure_2},
        ]
        check_and_run_random_handler(options)

    def scene_treasure_2():
        game_over("You can feel the treasure poisoning your mind...but you have to listen to the treasure...", "curse")

    def scene_dungeon():
        print("\nYou find another staircase and two large, locked doors. A set of keys hangs from a nail between them.")
        options = [
            {"description": "Unlock and enter the door on the left.", "handler": scene_left_door},
            {"description": "Unlock and enter the door on the right.", "handler": scene_right_door},
            {"description": "Follow the staircase deeper into the dungeon.", "handler": scene_explore_deeper},
        ]
        check_and_run_random_handler(options, 3)

    def scene_left_door():
        print("\nA prisoner in chains lunges at you. You wake up, finding the door locked...the prisoner chuckling to "
              "himself on the other side of the door.")
        options = [
            {"description": "Ask the prisoner to let you out.", "handler": scene_ask_for_freedom},
            {"description": "Ask the prisoner why he locked you in his cell.", "handler": scene_ask_for_freedom},
            {"description": "Ask the prisoner who he is.", "handler": scene_ask_who_prisoner_is}
        ]
        check_and_run_random_handler(options, 3)

    def scene_ask_for_freedom():
        game_over("The prisoner, delirious, responds, 'I've done my time...now it's your turn.' then leaves you to die.", "trapped")

    def scene_ask_who_prisoner_is():
        print("\nThe prisoner stares at you, then bitterly says, 'I used to be the king of this castle, before you "
              "betrayed me...Now you'll rot in there.'")
        options = [
            {"description": "Assure the prisoner that you've never seen him before.", "handler": scene_tell_prisoner_truth},
            {"description": "Tell the prisoner that you're sorry and filled with regret.", "handler": scene_lie_to_prisoner}
        ]
        check_and_run_random_handler(options)

    def scene_tell_prisoner_truth():
        game_over("The prisoner doesn't believe you...he leaves you alone to die.", "trapped")

    def scene_lie_to_prisoner():
        print("\nThe prisoner listens to you plead for forgiveness...that you regret what you did, and you're "
              "sorry...and he gets closer to you...")
        options = [
            {"description": "Grab the prisoner to wrestle the key from him.", "handler": scene_grab_prisoner},
            {"description": "Ask the prisoner to show mercy and let you go.", "handler": scene_ask_prisoner_for_mercy},
            {"description": "Tell the prisoner you'll leave and never come back if he releases you.", "handler": scene_tell_prisoner_youll_leave}
        ]
        check_and_run_random_handler(options, 3)

    def scene_grab_prisoner():
        game_over("You accidentally knock the prisoner's head against the door, and he falls to the ground...before "
                  "you get the key.", "trapped")

    def scene_tell_prisoner_youll_leave():
        game_over("The prisoner tells you he wants you to suffer the way you made him suffer...he leaves you to die.", "trapped")

    def scene_ask_prisoner_for_mercy():
        print("\nThe prisoner accuses you of having no mercy...and asks why he should show you mercy.")
        options = [
            {"description": "Tell the prisoner that he'd find good karma for letting you go.", "handler": scene_tell_prisoner_good_karma},
            {"description": "Tell the prisoner that you're a good person and don't want to die there.", "handler": scene_tell_prisoner_good_person},
            {"description": "Tell the prisoner that you realise you were terrible to him and you're sorry.", "handler": scene_tell_prisoner_youre_sorry}
        ]
        check_and_run_random_handler(options, 3)

    def scene_tell_prisoner_good_karma():
        game_over("The prisoner tells you karma doesn't exist...and to enjoy your new cell. He leaves you forever.", "trapped")

    def scene_tell_prisoner_good_person():
        game_over("The prisoner reminds you of how you betrayed him, and you deserve to die in his old cell, "
                  "before he abandons you.", "trapped")

    def scene_tell_prisoner_youre_sorry():
        game_over("The prisoner says, 'I'm glad you're sorry, but that's not enough...Goodbye.'", "trapped")

    def scene_right_door():
        print("\nYou find a cloaked old lady laying in the shadows...seemingly frail and old. She tells you she knew you were coming.")
        options = [
            {"description": "Ask the lady what she means.", "handler": scene_ask_lady_for_explanation},
            {"description": "Ask the lady who she is.", "handler": scene_ask_lady_for_explanation},
        ]
        check_and_run_random_handler(options, 3)

    def scene_ask_lady_for_explanation():
        print("\nThe lady tells you that she's a sorcerer...and she knows your future.")
        options = [
            {"description": "Ask the sorcerer what your future holds.", "handler": scene_ask_lady_about_future},
            {"description": "Ask the sorcerer if this castle keeps any treasures.", "handler": scene_ask_lady_about_castle}
        ]
        check_and_run_random_handler(options, 2)

    def scene_ask_lady_about_future():
        print("\nThe sorcerer tells you that the castle is dangerous, and you will face an obstacle soon. She asks "
              "you to help her to her feet...")
        options = [
            {"description": "Help the sorcerer to her feet.", "handler": scene_help_lady},
            {"description": "Don't go near the sorcerer.", "handler": scene_dont_help_lady},
            {"description": "Thank the sorcerer for her time, but tell her you must leave.",
             "handler": scene_dont_help_lady}
        ]
        check_and_run_random_handler(options, 3)

    def scene_ask_lady_about_castle():
        print("\nThe sorcerer informs you that this castle keeps many very valuable treasures, but they are not easy "
              "to obtain. She asks you to help her stand up...")
        options = [
            {"description": "Help the sorcerer to her feet.", "handler": scene_help_lady},
            {"description": "Don't go near the sorcerer.", "handler": scene_dont_help_lady},
            {"description": "Thank the sorcerer for her time, but tell her you must leave.",
             "handler": scene_dont_help_lady}
        ]

    def scene_help_lady():
        print("\nAs you draw near her, the sorcerer grabs your arm and you help her up...but you suddenly feel ten times weaker.")
        game_over("The sorcerer tells you she sees death in your future...that soon, she will absorb your life force.", "enemy")

    def scene_dont_help_lady():
        print("\nThe sorcerer says, 'Don't you know it's rude to deny your elders?' With a wave of her hand, the door closes and locks behind you.")
        game_over("The sorcerer waves her hand again and you are pulled towards her. She grabs your arm and absorbs your energy.", "enemy")

    def scene_deeper_into_dungeon():
        ...

    def scene_lone_tower():
        print("\nYou stumble upon a wizard's chambers. You notice a book on a pedestal and a cloudy glass orb on a "
              "table.")
        options = [
            {"description": "Inspect the book.", "handler": scene_inspect_book},
            {"description": "Inspect the orb.", "handler": scene_inspect_orb},
        ]
        check_and_run_random_handler(options)

    def scene_inspect_book():
        print("\nYou approach the book. It's ancient, and emits a faint magical aura...")
        options = [
            {"description": "Take the book.", "handler": scene_take_book},
            {"description": "Read from the book.", "handler": scene_read_from_book}
        ]
        check_and_run_random_handler(options)

    def scene_take_book():
        game_state["book_on_pedestal"] = False
        print("\nYou grab the book and store it in your bag.")
        options = [
            {"description": "Leave the chambers.", "handler": scene_leave_chambers}
        ]
        if game_state["orb_on_table"]:
            options.append({"description": "Inspect the orb.", "handler": scene_inspect_orb})
        check_and_run_random_handler(options)

    def scene_read_from_book():
        print("\nThe book's cover reads: 'Book of Spells'.")
        options = [
            {"description": "Read the 'Flame of Power'...", "handler": scene_read_flame_spell},
            {"description": "Read 'Apparitional Escape'...", "handler": scene_read_apparitional_escape},
            {"description": "Read 'Unbreakable Barrier'...", "handler": scene_unbreakable_barrier},
        ]
        check_and_run_random_handler(options, 3)

    def scene_read_flame_spell():
        game_state["book_on_pedestal"] = False
        print("\nYou recite the book's flame spell. A flame lights in the middle of the book and engulfs it...burning "
              "it to ashes.")
        options = [
            {"description": "Inspect the orb.", "handler": scene_inspect_orb},
            {"description": "Leave the chambers.", "handler": scene_leave_chambers}
        ]
        check_and_run_random_handler(options)

    def scene_read_apparitional_escape():
        game_over("\nYou recite the teleportation spell...and find yourself teleported right outside of the lone "
                  "tower, falling to your death.", "fall")

    def scene_unbreakable_barrier():
        game_over("\nYou recite the barrier spell...which creates an unbreakable, inescapable barrier around you. "
                  "There's no escape.", "trapped")

    def scene_inspect_orb():
        print("\nYou approach the orb. It begins to whisper to you: 'What is it you seek?...'")
        options = [
            {"description": "Tell the orb you wish to know your future.", "handler": scene_know_future},
            {"description": "Ask the orb if the castle keeps any treasure.", "handler": scene_ask_orb},
            {"description": "Take the orb with you.", "handler": scene_take_orb}
        ]
        check_and_run_random_handler(options, 3)

    def scene_know_future():
        print("\nThe orb says, 'There is unavoidable danger in your future...prepare for the worst'.")
        options = [
            {"description": "Ask the orb if the castle keeps any treasure.", "handler": scene_ask_orb},
            {"description": "Take the orb with you.", "handler": scene_take_orb}
        ]
        check_and_run_random_handler(options)

    def scene_ask_orb():
        print("\nThe orb tells you that there are many treasures in the castle...but you may not live long enough to "
              "reach them.")
        options = [
            {"description": "Take the orb...it could help you.", "handler": scene_take_orb},
            {"description": "Ask the orb how to survive in the castle.", "handler": scene_ask_orb_2},
        ]
        check_and_run_random_handler(options)

    def scene_ask_orb_2():
        print("\nThe orb tells you it's too late, you won't survive...unless you happen to posses powerful magic.")
        options = [
            {"description": "Ask the orb to clarify.", "handler": scene_ask_orb_clarify},
            {"description": "Take the orb, for it posses powerful magic.", "handler": scene_take_orb},
        ]
        check_and_run_random_handler(options)

    def scene_ask_orb_clarify():
        print("\nThe orb informs you that someone strong is coming from down below...")
        options = [
            {"description": "Take the orb.", "handler": scene_take_orb},
            {"description": "Leave the chambers.", "handler": scene_leave_chambers}
        ]
        if game_state["book_on_pedestal"]:
            options.append({"description": "Inspect the book.", "handler": scene_inspect_book})
        check_and_run_random_handler(options, 3)

    def scene_take_orb():
        game_state["orb_on_table"] = False
        print("\nYou grab the orb store it in your bag.")
        options = [
            {"description": "Leave the chambers.", "handler": scene_leave_chambers}
        ]
        if game_state["book_on_pedestal"]:
            options.append({"description": "Inspect the book.", "handler": scene_inspect_book})
        check_and_run_random_handler(options)

    def scene_leave_chambers():
        print("\nYou step towards where you came...and suddenly, a ring of fire erupts and surrounds you from the floor.")
        if not game_state["book_on_pedestal"] or not game_state["orb_on_table"]:
            print("You hear a voice: 'I will not allow a thief to loot my chambers and escape with their life!'...")
        elif game_state["book_on_pedestal"] and game_state["orb_on_table"]:
            print("You hear a voice: 'I will not allow someone to enter my chambers and escape with their life!'...'")
        game_over("A wizard enters the chamber. He waves his hand upwards, and the fire closes in around you...", "enemy")

    def scene_library():
        print("\nYou find old bookshelves and candles lining the walls. An old lady sits at a desk in the front of "
              "the room...")
        options = [
            {"description": "Ask the lady if you can check out the library.", "handler": scene_ask_librarian},
            {"description": "Casually browse the books.", "handler": scene_browse_books},
            {"description": "Don't let the lady see you...", "handler": scene_avoid_librarian},
            {"description": "Spy on the lady.", "handler": scene_watch_librarian},
        ]
        check_and_run_random_handler(options, 3)

    def scene_ask_librarian():
        game_state["noise_count"] += 1
        if game_state["noise_count"] >= 2:
            print("\nA shadow rises from the ground, and morphs into a body. It begins to turn its head left and "
                  "right...")
            options = [
                {"description": ".", "handler": scene_},
                {"description": ".", "handler": scene_},
            ]
            check_and_run_random_handler(options)
        else:
            print("\nDespite never having moved, the lady freezes, her body stiff at the sound of your voice. The candles "
                "flicker...and you hear a faint 'Shhh...' escape her.")
            options = [
                {"description": "Don't speak to the librarian...", "handler": scene_stay_quiet},
                {"description": ".", "handler": scene_},
                {"description": ".", "handler": scene_},
            ]
            check_and_run_random_handler(options, 3)

    def scene_stay_quiet():
        options = [
            {"description": ".", "handler": scene_},
            {"description": ".", "handler": scene_},
        ]
        check_and_run_random_handler(options)

    def scene_browse_books():
        print("\nAs you look through the library, you look up and notice the lady's desk is empty. The candles "
              "suddenly feel weaker, as if shadows are overcoming the library...")
        options = [
            {"description": ".", "handler": scene_},
            {"description": ".", "handler": scene_},
        ]
        check_and_run_random_handler(options)

    def scene_avoid_librarian():
        print("\nAs you step away, you step on a pressured plate...and a latch releases a bookcase "
              "outside the library. The bookcase swing slighty ajar...")
        options = [
            {"description": "Enter the secret bookcase...", "handler": scene_enter_bookcase}
        ]
        check_and_run_random_handler(options)

    def scene_enter_bookcase():
        print("\nYou discover a hidden library, with scrolls older than the castle itself, and tables with corked "
              "vials of liquid.")
        options = [
            {"description": "Check out the old scrolls.", "handler": scene_see_scrolls},
            {"description": "Check out the vials of liquid.", "handler": scene_see_vials},
        ]
        check_and_run_random_handler(options)

    def scene_see_scrolls():
        ...

    def scene_see_vials():
        ...

    def scene_watch_librarian():
        print("\nThe librarian picks up a book and reads one word, out loud: 'goat'. She then holds the book open towards "
              "the floor, and a goat emerges from the book's pages. She sets the book down...")

    def scene_forgotten_cavern():
        print("\nThe cavern is dark and cold. You see two paths ahead.")
        options = [
            {"description": "Light a torch and explore deeper.",
             "handler": scene_explore_deeper},
            {"description": "Follow the sound of rushing water.",
             "handler": scene_rushing_water},
        ]
        check_and_run_random_handler(options)

    def scene_explore_deeper():
        print("\nYou find a skeleton of armor holding a glowing rune.")
        options = [
            {"description": "Examine the markings on the rune.", "handler": scene_examine_rune},
            {"description": "Remove the rune from the skeleton's grasp.", "handler": scene_take_rune},
        ]
        check_and_run_random_handler(options)

    def scene_examine_rune():
        game_over("The markings warn that fire will consume any who dare to read the markings.", "fire")

    def scene_take_rune():
        print("\nOnce you store the rune away, the skeleton begins to move...")
        options = [
            {"description": "Behead the skeleton.", "handler": scene_behead_skeleton},
            {"description": "Give the rune back to the skeleton.", "handler": scene_return_rune}
        ]
        check_and_run_random_handler(options)

    def scene_behead_skeleton():
        game_over("The headless skeleton swings its sword, striking one of your major arteries...skeletons don't need "
                  "heads.", "mortal peril")

    def scene_return_rune():
        game_over("As you put the rune back in the skeleton's bony hand, he crumbles to dust...and you begin to "
                  "replace him, your limbs becoming bones.", "curse")

    def scene_rushing_water():
        print("\nYou find an underground river, flowing at a moderate speed.")
        print("1. Refill your canteen to prepare for the remainder of your journey.")
        print("2. Carefully follow along the river to see where it ends.")

        choice = check_or_return_none()
        if choice is None:
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
        ]
        check_and_run_random_handler(options)

    def scene_walk_slowly():
        print("\nWith every step, your vision becomes more and more obscured from the fog.")
        print("1. Light a torch to light the way and avoid misstepping.")
        print("2. Carefully test each step ahead of you.")

        choice = check_or_return_none()
        if choice is None:
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

        choice = check_or_return_none()
        if choice is None:
            return None

        if choice == "1":
            game_over("Your movements overwhelm the bridge...and fall into the abyss.", "fall")
        elif choice == "2":
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
        check_and_run_random_handler(options)

    def scene_seek_shelter():
        print("\nYou find a beast sleeping in the cave, surrounded by bones.")
        print("1. Unsheathe your blade and prepare for the worst.")
        print("2. Abandon the cave and chance the mountain path.")

        choice = check_or_return_none()
        if choice is None:
            return None

        if choice == "1":
            game_over("The beast is larger than you thought...you knew your chances were slim.", "beast")
        elif choice == "2":
            game_over("You exit the cave too quickly, and lose your footing...", "fall")
        else:
            print("\nInvalid choice. Try again.")
            scene_seek_shelter()

    def scene_push_forward():
        print("\nYou see the peak of the icy mountain ahead, merely a few feet away.")
        options = [
            {"description": "Push forward to the peak.", "handler": scene_push_to_peak},
            {"description": "Rest and admire the view.", "handler": scene_admire_view}
        ]
        check_and_run_random_handler(options)

    def scene_push_to_peak():
        game_over("The peak was an illusion. You step into the void.", "void")

    def scene_admire_view():
        game_over("The ice beneath you gives way, dropping you into the void.", "void")

    # def try_again():
    #     print("Would you like to try again? (yes/no)")
    #     retry = input("> ").strip().lower()
    #     if retry in ["yes", "y"] or retry not in ["no", "n"]:
    #         start_game()
    #     else:
    #         print("\nThanks for playing!")

    def game_over(reason, death_type):
        """Gives the player a final chance before their inevitable demise, based on the cause."""
        print(f"\n{reason}")
        print("You have one last chance to survive...")

        options = death_scenarios.get(death_type, ["Do nothing.", "Panic.", "Try to wake from this nightmare."])
        selected_indices = random.sample(range(len(options)), 2)
        print()
        print(f"1. {options[selected_indices[0]]}")
        print(f"2. {options[selected_indices[1]]}")

        choice = check_or_return_none()
        if choice is None:
            return None

        if choice == "1":
            chosen_index = selected_indices[0]
        elif choice == "2":
            chosen_index = selected_indices[1]
        else:
            print("\nYou hesitated... and that was your downfall.")
            return

        print(f"\n{final_deaths[death_type][chosen_index]}")

        print("\nYou have died. Better luck awaits those who follow a different path...")
        # try_again()

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

    while True:
        start_game()
        play_again = input("\nDo you want to try again? (yes/no): ").lower()
        if play_again not in ["yes", "y"] or play_again in ["no", "n"]:
            break
        else:
            print("I didn't catch that...")

    print("Thanks for playing!")


