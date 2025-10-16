import random
from .core import game_state, check_and_run_random_handler, game_over, print_wrapped, player_state
from .state import ui_state
from utils.helper_functions import (
update_player_state,
add_to_inventory,
remember,
has_memory,
remember_intro,
has_seen_intro,
delay,
has_item
)


# --------------------
# Abandoned Castle
# --------------------

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
        print_wrapped("\nThe castle looms ahead. You see paths leading up and down.")
    elif upstairs:
        print_wrapped("\nThe castle looms ahead. The only way forward is up.")
    elif downstairs:
        print_wrapped("\nThe castle looms ahead. The only way forward is down.")
    else:
        print_wrapped("\nThe castle looms ahead. You stand at a crossroads.")

    ui_state["current_options"] = selected
    check_and_run_random_handler(ui_state["current_options"], 4, checkpoint=scene_abandoned_castle)

# --------------------
# Grand Hall
# --------------------

def scene_grand_hall():
    print_wrapped("\nYou find dozens of chests filled with treasure next to an empty throne.")
    options = [
        {"description": "Step up to the throne and take your seat.", "handler": scene_sit_on_throne},
        {"description": "Pick up some treasure and admire its glory.", "handler": scene_admire_treasure},
    ]
    if "library_scroll" in player_state["inventory"]:
        options.append({"description": "Examine the throne.", "handler": scene_examine_throne})
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3, checkpoint=scene_grand_hall)

# --------------------
# Examine Throne
# --------------------

def scene_examine_throne():
    print_wrapped("\nYou step up to the throne, and you peer behind it. You notice a gem on the wall behind the "
                  "throne that matches a symbol from the map you found...")
    options = [
        {"description": "Check the map.", "handler": scene_check_map},
        {"description": "Investigate the gem.", "handler": scene_investigate_gem},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_examine_throne)

def scene_check_map():
    print_wrapped("\nUnder the symbol, you find a warning...to only approach the gem with the map held out towards it.")
    options = [
        {"description": "Hold the map out towards the gem and approach it.", "handler": scene_approach_gem_with_map},
        {"description": "Investigate the gem.", "handler": scene_investigate_gem},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_check_map)

def scene_investigate_gem():
    print_wrapped("\nYou approached the gem without holding out the map...the gem hums, then unleashes a black smoke.", newline_delay=1)
    return game_over("The smoke turns you to ash and dust as it brushes your skin.", "gem_trap")

def scene_approach_gem_with_map():
    print_wrapped("\nAs you approach the gem, it hums with magical power...and suddenly, the stones around it "
                  "begin to split. As you watch, the stone splits form a doorway around the gem, with the gem in "
                  "the center of the entryway.")
    options = [
        {"description": "Enter the hidden room.", "handler": scene_enter_hidden_room},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_approach_gem_with_map)

def scene_enter_hidden_room():
    print_wrapped("\nYou enter the hidden room. You find treasures worthy of a king...royal armour, commanding "
                  "swords, chests of gold. In the center of the room stands a pedestal with a book titled, "
                  "'Secrets of the Castle'.")
    print_wrapped("Etched into the pedestal reads a message: 'Here sits the only safe treasures of the castle. "
                  "May your days be long and fruitful.'")
    print_wrapped("\nCongratulations! You survived the Abandoned Castle. Great choices!")

# --------------------
# Sit on Throne
# --------------------

def scene_sit_on_throne():
    print_wrapped("\nAs you sit on the throne, you notice a boy watching you...signaling to follow him.")
    options = [
        {"description": "Follow the boy.", "handler": scene_follow_boy},
        {"description": "Ignore the boy. You're royalty!", "handler": scene_ignore_boy}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_sit_on_throne)

def scene_follow_boy():
    print_wrapped("\nThe boy walks into a room. You step through the doorway to find more kids, keeping themselves "
          "entertained.")
    options = [
        {"description": "Ask the kids why they're alone.", "handler": scene_ask_why_alone},
        {"description": "Ask the boy who his friends are.", "handler": scene_ask_who_kids_are},
        {"description": "Leave the room.", "handler": scene_kids_surround_user},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3, checkpoint=scene_follow_boy)

def scene_ask_why_alone():
    print_wrapped("\nThe kids, confused, stare at you for a few seconds. One girl finally says, 'We've been alone for a "
          "long time.'")
    options = [
        {"description": "Ask the boy if he's seen any adults.", "handler": scene_ask_where_adults},
        {"description": "Distract the kids to make them less somber.", "handler": scene_make_kids_happy},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_ask_why_alone)

def scene_make_kids_happy():
    print_wrapped("\nThe kids' mood lightens, and you see a few smile at you. The boy walks up to you and says, "
          "'You should stay with us forever.'")
    options = [
        {"description": "Pat the boy's head.", "handler": scene_pat_boys_head},
        {"description": "Tell the boy he's sweet, but you have to leave.", "handler": scene_kids_say_cant_leave}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_make_kids_happy)

def scene_pat_boys_head():
    print_wrapped("\nYour hand passes through the boy's head as he looks up at you...awaiting your response. You realise "
          "you are the only living person in the room.")
    options = [
        {"description": "Tell the kids you'll be right back.", "handler": scene_kids_say_cant_leave},
        {"description": "Ask the kids to give you a minute alone.", "handler": scene_ask_kids_for_space},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_pat_boys_head)

def scene_ask_who_kids_are():
    print_wrapped("\nThe boy says they're his friends. They just don't remember each other's names because it's been so "
          "long...")
    options = [
        {"description": "Ask the boy if there are any adults around.", "handler": scene_ask_where_adults},
        {"description": "Cheer up the kids with a joke or hand trick.", "handler": scene_make_kids_happy}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_ask_who_kids_are)

def scene_ignore_boy():
    print_wrapped("\nThe boy disappears from your view. Within a moment, you see him again, a bit closer...facing away "
          "from you.")
    options = [
        {"description": "Address the boy.", "handler": scene_address_boy},
        {"description": "Stay seated and watch the boy.", "handler": scene_watch_boy}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_ignore_boy)

def scene_address_boy():
    print_wrapped("\nYou speak to the boy...but he doesn't answer. Instead, the air becomes freezing cold as the boy "
          "turns around.")
    options = [
        {"description": "Ask the boy if he's seen any adults.", "handler": scene_ask_where_adults},
        {"description": "Ask the boy what his name is.", "handler": scene_ask_boys_name},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_address_boy)

def scene_ask_where_adults():
    print_wrapped("\nThe boy nods and beckons for you to follow him. He brings you to a room littered with bodies.")
    options = [
        {"description": "Ask the boy what happened to these people.", "handler": scene_ask_about_bodies},
        {"description": "Tell the boy you'll be right back...and leave.", "handler": scene_kids_surround_user},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_ask_where_adults)

def scene_ask_about_bodies():
    print_wrapped("\nThe boy says, 'They didn't want to play with us.'")
    options = [
        {"description": "Tell the boy not to worry, you'll play with them...but you have to leave for a minute.", "handler": scene_kids_surround_user},
        {"description": "Leave the boy in the room to escape the kids...", "handler": scene_kids_surround_user},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_ask_about_bodies)

def scene_ask_boys_name():
    print_wrapped("\nThe boy disappears...but you hear him say 'We don't remember our names. Will you play with us?'")
    scene_kids_surround_user()

def scene_watch_boy():
    print_wrapped("\nAs you sit on the throne, watching the boy, he disappears into thin air. You hear the boy crying, "
          "but he is nowhere to be seen.")
    options = [
        {"description": "Leave the grand hall.", "handler": scene_kids_surround_user},
        {"description": "Leave the throne.", "handler": scene_kids_surround_user},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_watch_boy)

def scene_kids_surround_user():
    print_wrapped("\nThe boy suddenly appears before you. One by one, more and more ghostly kids appear out of thin "
          "air, surrounding you.")
    options = [
        {"description": "Tell the kids you'll be right back.", "handler": scene_kids_say_cant_leave},
        {"description": "Ask the kids to give you a minute alone.", "handler": scene_ask_kids_for_space}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_kids_surround_user)

def scene_kids_say_cant_leave():
    game_over("The boy says, 'You can't leave...you have to stay with us.' They reach out and grab you.", "ghost")

def scene_ask_kids_for_space():
    game_over("The boy says, 'Being alone is bad...stay with us.' They reach out and grab you.", "ghost")

# --------------------
# Treasure Curse
# --------------------

def scene_admire_treasure():
    print_wrapped("\nYou admire the shiny treasure...it must be worth more than you've ever seen in your life.")
    options = [
        {"description": "Take some treasure.", "handler": scene_treasure},
        {"description": "Find some treasure.", "handler": scene_treasure},
        {"description": "Grab some treasure.", "handler": scene_treasure},
        {"description": "Hold some treasure.", "handler": scene_treasure}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 4, checkpoint=scene_admire_treasure)

def scene_treasure():
    print_wrapped("\nThere's something special about this treasure...you should protect it...it can't fall into the wrong "
          "hands...")
    options = [
        {"description": "Protect the treasure.", "handler": scene_treasure_2},
        {"description": "Guard the treasure.", "handler": scene_treasure_2},
        {"description": "Hoard the treasure.", "handler": scene_treasure_2},
        {"description": "Keep the treasure.", "handler": scene_treasure_2},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 4, checkpoint=scene_treasure)

def scene_treasure_2():
    game_over("You can feel the treasure poisoning your mind...but you have to listen to the treasure...", "curse")

# --------------------
# Dungeon
# --------------------

def scene_dungeon():
    if "library_scroll" in player_state["inventory"]:
        print_wrapped("\nYou find another staircase and two large, locked doors. A set of keys hangs from a nail "
                      "between them. A lone chair sits in a corner, and just behind it, a square metal trapdoor "
                      "sits closed...")
    else:
        print_wrapped("\nYou find another staircase and two large, locked doors. A set of keys hangs from a nail "
                      "between them.")
    options = [
        {"description": "Unlock and enter the door on the left.", "handler": scene_left_door},
        {"description": "Unlock and enter the door on the right.", "handler": scene_right_door},
        {"description": "Follow the staircase deeper into the dungeon.", "handler": scene_explore_deeper},
    ]
    if "library_scroll" in player_state["inventory"]:
        options.append({"description": "Open the trapdoor.", "handler": scene_open_trapdoor})
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 4, checkpoint=scene_dungeon)

def scene_open_trapdoor():
    print_wrapped("\nYou open the trapdoor...and see a singular eye open in the dark below. A cyclops reaches up "
                  "towards you...")
    options = [
        {"description": "Close the door.", "handler": scene_close_trapdoor},
        {"description": "Leave the dungeon.", "handler": scene_leave_dungeon}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_open_trapdoor)

def scene_close_trapdoor():
    print_wrapped("\nYou close the trapdoor just in time. The cyclops is trapped.")
    options = [
        {"description": "Read the clue from the map again.", "handler": scene_read_map_clue_dungeon},
        {"description": "Retrace your steps...", "handler": scene_abandoned_castle},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3, checkpoint=scene_close_trapdoor)

def scene_read_map_clue_dungeon():
    print_wrapped("""You read the clue again...
'A seat of power tempts the bold,
But hides a truth not plainly told.
Look not with pride, but with a gaze,
Behind the seat, a secret lays.'""")
    options = [
        {"description": "Unlock and enter the door on the left.", "handler": scene_left_door},
        {"description": "Unlock and enter the door on the right.", "handler": scene_right_door},
        {"description": "Follow the staircase deeper into the dungeon.", "handler": scene_explore_deeper},
        {"description": "Retrace your steps to the castle entrance...", "handler": scene_abandoned_castle},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 4, checkpoint=scene_read_map_clue_dungeon)

def scene_leave_dungeon():
    game_over("You hear the cyclops escapes the trapdoor and follow you...", "cyclops")

def scene_left_door():
    print_wrapped("\nA prisoner in chains lunges at you. You wake up, finding the door locked...the prisoner "
                  "chuckling to himself on the other side of the door.")
    options = [
        {"description": "Ask the prisoner to let you out.", "handler": scene_ask_for_freedom},
        {"description": "Ask the prisoner why he locked you in his cell.", "handler": scene_ask_for_freedom},
        {"description": "Ask the prisoner who he is.", "handler": scene_ask_who_prisoner_is}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3, checkpoint=scene_left_door)

def scene_ask_for_freedom():
    game_over("The prisoner, delirious, responds, 'I've done my time...now it's your turn.' then leaves you to die.", "trapped")

def scene_ask_who_prisoner_is():
    print_wrapped("\nThe prisoner stares at you, then bitterly says, 'I used to be the king of this castle, before you "
          "betrayed me...Now you'll rot in there.'")
    options = [
        {"description": "Assure the prisoner that you've never seen him before.", "handler": scene_tell_prisoner_truth},
        {"description": "Tell the prisoner that you're sorry and filled with regret.", "handler": scene_lie_to_prisoner}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_ask_who_prisoner_is)

def scene_tell_prisoner_truth():
    game_over("The prisoner doesn't believe you...he leaves you alone to die.", "trapped")

def scene_lie_to_prisoner():
    print_wrapped("\nThe prisoner listens to you plead for forgiveness...that you regret what you did, and you're "
          "sorry...and he gets closer to you...")
    options = [
        {"description": "Grab the prisoner to wrestle the key from him.", "handler": scene_grab_prisoner},
        {"description": "Ask the prisoner to show mercy and let you go.", "handler": scene_ask_prisoner_for_mercy},
        {"description": "Tell the prisoner you'll leave and never come back if he releases you.", "handler": scene_tell_prisoner_youll_leave}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3, checkpoint=scene_lie_to_prisoner)

def scene_grab_prisoner():
    game_over("You accidentally knock the prisoner's head against the door, and he falls to the ground...before "
              "you get the key.", "trapped")

def scene_tell_prisoner_youll_leave():
    game_over("The prisoner tells you he wants you to suffer the way you made him suffer...he leaves you to die.", "trapped")

def scene_ask_prisoner_for_mercy():
    print_wrapped("\nThe prisoner accuses you of having no mercy...and asks why he should show you mercy.")
    options = [
        {"description": "Tell the prisoner that he'd find good karma for letting you go.", "handler": scene_tell_prisoner_good_karma},
        {"description": "Tell the prisoner that you're a good person and don't want to die there.", "handler": scene_tell_prisoner_good_person},
        {"description": "Tell the prisoner that you realise you were terrible to him and you're sorry.", "handler": scene_tell_prisoner_youre_sorry}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3, checkpoint=scene_ask_prisoner_for_mercy)

def scene_tell_prisoner_good_karma():
    game_over("The prisoner tells you karma doesn't exist...and to enjoy your new cell. He leaves you forever.", "trapped")

def scene_tell_prisoner_good_person():
    game_over("The prisoner reminds you of how you betrayed him, and you deserve to die in his old cell, "
              "before he abandons you.", "trapped")

def scene_tell_prisoner_youre_sorry():
    game_over("The prisoner says, 'I'm glad you're sorry, but that's not enough...Goodbye.'", "trapped")

def scene_right_door():
    print_wrapped("\nYou find a cloaked old lady laying in the shadows...seemingly frail and old. She tells you she knew you were coming.")
    options = [
        {"description": "Ask the lady what she means.", "handler": scene_ask_lady_for_explanation},
        {"description": "Ask the lady who she is.", "handler": scene_ask_lady_for_explanation},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3, checkpoint=scene_right_door)

def scene_ask_lady_for_explanation():
    print_wrapped("\nThe lady tells you that she's a sorcerer...and she knows your future.")
    options = [
        {"description": "Ask the sorcerer what your future holds.", "handler": scene_ask_lady_about_future},
        {"description": "Ask the sorcerer if this castle keeps any treasures.", "handler": scene_ask_lady_about_castle}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_ask_lady_for_explanation)

def scene_ask_lady_about_future():
    print_wrapped("\nThe sorcerer tells you that the castle is dangerous, and you will face an obstacle soon. She asks "
          "you to help her to her feet...")
    options = [
        {"description": "Help the sorcerer to her feet.", "handler": scene_help_lady},
        {"description": "Don't go near the sorcerer.", "handler": scene_dont_help_lady},
        {"description": "Thank the sorcerer for her time, but tell her you must leave.",
         "handler": scene_dont_help_lady}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3, checkpoint=scene_ask_lady_about_future)

def scene_ask_lady_about_castle():
    print_wrapped("\nThe sorcerer informs you that this castle keeps many very valuable treasures, but they are not easy "
          "to obtain. She asks you to help her stand up...")
    options = [
        {"description": "Help the sorcerer to her feet.", "handler": scene_help_lady},
        {"description": "Don't go near the sorcerer.", "handler": scene_dont_help_lady},
        {"description": "Thank the sorcerer for her time, but tell her you must leave.",
         "handler": scene_dont_help_lady}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3, checkpoint=scene_ask_lady_about_castle)

def scene_help_lady():
    print_wrapped("\nAs you draw near her, the sorcerer grabs your arm and you help her up...but you suddenly feel ten times weaker.")
    game_over("The sorcerer tells you she sees death in your future...that soon, she will absorb your life force.", "enemy")

def scene_dont_help_lady():
    print_wrapped("\nThe sorcerer says, 'Don't you know it's rude to deny your elders?' With a wave of her hand, the door closes and locks behind you.")
    game_over("The sorcerer waves her hand again and you are pulled towards her. She grabs your arm and absorbs your energy.", "enemy")

def scene_deeper_into_dungeon():
    ...

# --------------------
# Lone Tower
# --------------------

def scene_lone_tower():
    if not "library_scroll" in player_state["inventory"]:
        print_wrapped("\nYou stumble upon a wizard's chambers. You notice a book on a pedestal and a cloudy glass orb on a "
          "table.")
    if "library_scroll" in player_state["inventory"]:
        print_wrapped("\nYou stumble upon a wizard's chambers. You notice a book on a pedestal, a cloudy glass orb on a "
          "table, and a stone seat. Behind the seat hangs a painting of mountains of gold coins...")
    options = [
        {"description": "Inspect the book.", "handler": scene_inspect_book},
        {"description": "Inspect the orb.", "handler": scene_inspect_orb},
    ]
    if "library_scroll" in player_state["inventory"]:
        options.append({"description": "Inspect the painting.", "handler": scene_inspect_painting})
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3, checkpoint=scene_lone_tower)

def scene_inspect_painting():
    print_wrapped("\nYou approach the painting...and you start to feel a gravitational force pulling you into "
                  "it...the painting envelopes you, and you become nothing more than paint strokes. ")
    print_wrapped("\nYou have died. Better luck awaits those who follow a different path...")
    return

def scene_inspect_book():
    print_wrapped("\nYou approach the book. It's ancient, and emits a faint magical aura...")
    options = [
        {"description": "Take the book.", "handler": scene_take_book},
        {"description": "Read from the book.", "handler": scene_read_from_book}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_inspect_book)

def scene_take_book():
    game_state["book_burned"] = True
    add_to_inventory("ancient_book")
    print_wrapped("\nYou grab the book and store it in your bag.")
    options = [
        {"description": "Leave the chambers.", "handler": scene_leave_chambers}
    ]
    if not has_item("glass_orb"):
        options.append({"description": "Inspect the orb.", "handler": scene_inspect_orb})
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_take_book)

def scene_read_from_book():
    print_wrapped("\nThe book's cover reads: 'Book of Spells'.")
    options = [
        {"description": "Read the 'Flame of Power'...", "handler": scene_read_flame_spell},
        {"description": "Read 'Apparitional Escape'...", "handler": scene_read_apparitional_escape},
        {"description": "Read 'Unbreakable Barrier'...", "handler": scene_unbreakable_barrier},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3, checkpoint=scene_read_from_book)

def scene_read_flame_spell():
    print_wrapped("\nYou recite the book's flame spell. A flame lights in the middle of the book and engulfs it...burning "
          "it to ashes.")
    game_state["book_burned"] = True
    options = [
        {"description": "Inspect the orb.", "handler": scene_inspect_orb},
        {"description": "Leave the chambers.", "handler": scene_leave_chambers}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_read_flame_spell)

def scene_read_apparitional_escape():
    game_over("\nYou recite the teleportation spell...and find yourself teleported right outside of the lone "
              "tower, falling to your death.", "fall")

def scene_unbreakable_barrier():
    game_over("\nYou recite the barrier spell...which creates an unbreakable, inescapable barrier around you. "
              "There's no escape.", "trapped")

def scene_inspect_orb():
    print_wrapped("\nYou approach the orb. It begins to whisper to you: 'What is it you seek?...'")
    options = [
        {"description": "Tell the orb you wish to know your future.", "handler": scene_know_future},
        {"description": "Ask the orb if the castle keeps any treasure.", "handler": scene_ask_orb},
        {"description": "Take the orb with you.", "handler": scene_take_orb}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3, checkpoint=scene_inspect_orb)

def scene_know_future():
    print_wrapped("\nThe orb says, 'There is unavoidable danger in your future...prepare for the worst'.")
    options = [
        {"description": "Ask the orb if the castle keeps any treasure.", "handler": scene_ask_orb},
        {"description": "Take the orb with you.", "handler": scene_take_orb}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_know_future)

def scene_ask_orb():
    print_wrapped("\nThe orb tells you that there are many treasures in the castle...but you may not live long enough to "
          "reach them.")
    options = [
        {"description": "Take the orb...it could help you.", "handler": scene_take_orb},
        {"description": "Ask the orb how to survive in the castle.", "handler": scene_ask_orb_2},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_ask_orb)

def scene_ask_orb_2():
    print_wrapped("\nThe orb tells you it's too late, you won't survive...unless you happen to posses powerful magic.")
    options = [
        {"description": "Ask the orb to clarify.", "handler": scene_ask_orb_clarify},
        {"description": "Take the orb, for it posses powerful magic.", "handler": scene_take_orb},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_ask_orb_2)

def scene_ask_orb_clarify():
    print_wrapped("\nThe orb informs you that someone strong is coming from down below...")
    options = [
        {"description": "Take the orb.", "handler": scene_take_orb},
        {"description": "Leave the chambers.", "handler": scene_leave_chambers}
    ]
    if not game_state["book_burned"] and "ancient_book" not in player_state["inventory"]:
        options.append({"description": "Inspect the book.", "handler": scene_inspect_book})
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3, checkpoint=scene_ask_orb_clarify)

def scene_take_orb():
    print_wrapped("\nYou grab the orb store it in your bag.")
    add_to_inventory("glass_orb")
    options = [
        {"description": "Leave the chambers.", "handler": scene_leave_chambers}
    ]
    if not game_state["book_burned"] and "ancient_book" not in player_state["inventory"]:
        options.append({"description": "Inspect the book.", "handler": scene_inspect_book})
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_take_orb)

def scene_leave_chambers():
    print_wrapped("\nYou step towards where you came...and suddenly, a ring of fire erupts and surrounds you from the floor.")
    if game_state["book_burned"] or "ancient_book" in player_state["inventory"] or "glass_orb" in player_state["inventory"]:
        print_wrapped("You hear a voice: 'I will not allow a thief to loot my chambers and escape with their life!'...")
    elif not game_state["book_burned"] and "ancient_book" not in player_state["inventory"] and "glass_orb" not in player_state["inventory"]:
        print_wrapped("You hear a voice: 'I will not allow someone to enter my chambers and escape with their life!'...'")
    game_over("A wizard enters the chamber. He waves his hand upwards, and the fire closes in around you...", "enemy")

# --------------------
# Library
# --------------------

def scene_library():
    print_wrapped("\nYou find a large, shadowy room, with seemingly no ceiling, lined with old bookshelves, "
                  "and candles mounted large distances from each other on the walls. An old lady sits at a desk "
                  "in the front of the room...")
    print_wrapped("A lone hallway looms next to the library entrance, with scattered bookcases built into the "
                  "walls.")
    options = [
        {"description": "Ask the lady if you can check out the library.", "handler": scene_ask_librarian},
        {"description": "Casually browse the books.", "handler": scene_start_browsing_books},
        {"description": "Investigate the hallway...", "handler": scene_hallway},
        {"description": "Spy on the lady.", "handler": scene_watch_librarian},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 4, checkpoint=scene_library)

def scene_ask_librarian():
    if not game_state["browse_books_first"]:
        game_state["ask_librarian_first"] = True
    game_state["noise_count"] += 1
    if game_state["noise_count"] >= 2:
        shadows_descend()
    else:
        print_wrapped("\nShe freezes, her body stiff at the sound of your voice. The candles flicker...and you "
                      "hear a faint 'Shhh...' escape her.")
        options = [
            {"description": "Ask the lady again.", "handler": scene_ask_librarian_again},
            {"description": "Leave the library and walk down the hallway.", "handler": scene_hallway},
        ]
        if game_state["ask_librarian_first"]:
            options.append({"description": "Leave the lady alone and browse the books.", "handler": scene_start_browsing_books})
        if game_state["browse_books_first"]:
            options.append({"description": "Continue browsing.", "handler": scene_continue_browsing})
        ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 4, checkpoint=scene_ask_librarian)

def scene_ask_librarian_again():
    game_state["noise_count"] += 1
    shadows_descend()

# def scene_stay_quiet():
#     options = [
#         {"description": ".", "handler": scene_},
#         {"description": ".", "handler": scene_},
#     ]
#     ui_state["current_options"] = options
#     check_and_run_random_handler(ui_state["current_options"])

def scene_start_browsing_books():
    if not game_state["ask_librarian_first"]:
        game_state["browse_books_first"] = True
    print_wrapped("\nAs you start to explore a bookshelf of books, you feel the air displace behind you. You "
                  "slowly turn around, and find the lady standing still behind you, a gaunt look on her face. ")
    print_wrapped("The candles flicker weakly, as if the shadows above are attempting to overcome the "
                  "library...The lady whispers, 'Stay...quiet'. Then, she slowly turns toward her desk to "
                  "continue her work.")
    options = [
        {"description": "Leave the library and explore the hallway.", "handler": scene_hallway},
        {"description": "Continue through the library.", "handler": scene_continue_browsing},
        {"description": "Ask the lady why.", "handler": scene_ask_librarian},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3, checkpoint=scene_start_browsing_books)

def scene_continue_browsing():
    game_state["continue_browsing"] = True
    print_wrapped("\nAs you stroll through the library, seeking invaluable knowledge, you feel the weight of the shadows above...")
    options = [
        {"description": "Glance up at the shadows.", "handler": scene_glance_at_shadows},
    ]
    if not game_state["spied_on_librarian"]:
        options.append({"description": "Ignore the shadows and spy on the lady.", "handler": scene_watch_librarian})
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_continue_browsing)

def scene_glance_at_shadows():
    print_wrapped("As you glance up, you notice dark movements...")
    shadows_descend()

def shadows_descend():
    print_wrapped("\nAs if on cue, a shadow pours from the ceiling, dripping onto the ground like black paint. "
                  "The shadow morphs into a body, and slowly turns its head left and right. It begins to roam "
                  "around, its footsteps silent as it walks..investigating every sound.")
    options = [
        {"description": "Slowly back away from the shadow...", "handler": scene_back_away_from_shadow},
    ]
    if not game_state["continue_browsing"]:
        options.append({"description": "Don't move...watch the shadow.", "handler": scene_watch_shadow})
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=shadows_descend)

def scene_watch_shadow():
    if game_state["knight_in_library"]:
        print_wrapped("\nAs you watch, the knight's armour clinks away, grabbing the shadow's attention. The "
                      "shadow abruptly takes two inhuman, shadowy steps towards the knight, wraps its shadowy "
                      "hand around him, and the knight becomes engulfed in darkness. As you watch the shadow, "
                      "it turns towards you...listening...")
    options = [
        {"description": "Do not make a sound...", "handler": scene_dont_make_a_sound},
        {"description": "Slowly back away from the shadow...", "handler": scene_back_away_from_shadow},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_watch_shadow)

def scene_back_away_from_shadow():
    game_over("The shadow hears your footsteps...and steps over to you...darkness gripping you.", "shadow")

def scene_dont_make_a_sound():
    game_over("The shadow hears you breathing rapidly...and steps over to you...darkness gripping you.", "shadow")

def scene_hallway():
    print_wrapped("\nAs you walk down the hallway, you step on a pressured plate...and you hear a latch release. A "
          "bookcase swings open...")
    options = [
        {"description": "Enter the secret bookcase...", "handler": scene_enter_bookcase}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_hallway)

def scene_enter_bookcase():
    print_wrapped("\nYou discover a hidden room, with three items on a table: a scroll, a book, and a corked vial of liquid.")
    options = [
        {"description": "Investigate the scroll.", "handler": scene_see_scroll},
        {"description": "Examine the book.", "handler": scene_see_book},
        {"description": "Check out the vial of liquid.", "handler": scene_see_vial},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3, checkpoint=scene_enter_bookcase)

def scene_see_scroll():
    print_wrapped("\nAs you pick up the scroll, you realize that it's a treasure map...to a location within the castle.")
    options = [
        {"description": "Bring the scroll with you.", "handler": scene_pick_up_scroll},
        {"description": "Examine the book.", "handler": scene_see_book},
        {"description": "Check out the vial of liquid.", "handler": scene_see_vial},
        {"description": "Read the clue on the map.", "handler": scene_read_map_clue},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 4, checkpoint=scene_see_scroll)

def scene_read_map_clue():
    print_wrapped("""\nYou read the clue...
'A seat of power tempts the bold,
But hides a truth not plainly told.
Look not with pride, but with a gaze,
Behind the seat, a secret lays.'""")
    options = [
        {"description": "Bring the scroll with you.", "handler": scene_pick_up_scroll},
        {"description": "Examine the book.", "handler": scene_see_book},
        {"description": "Check out the vial of liquid.", "handler": scene_see_vial},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3, checkpoint=scene_read_map_clue)

def scene_pick_up_scroll():
    add_to_inventory("library_scroll")
    print_wrapped("\nYou stored the map.")
    options = [
        {"description": "Examine the book.", "handler": scene_see_book},
        {"description": "Check out the vial of liquid.", "handler": scene_see_vial},
        {"description": "Return to the library.", "handler": scene_return_to_library},
        {"description": "Retrace your steps to the castle entrance...", "handler": scene_abandoned_castle},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 4, checkpoint=scene_pick_up_scroll)

def scene_return_to_library():
    print_wrapped("\nYou exit the bookcase and return to the library.")
    options = [
        {"description": "Ask the lady if you can check out the library.", "handler": scene_ask_librarian},
        {"description": "Casually browse the books.", "handler": scene_start_browsing_books},
        {"description": "Spy on the lady.", "handler": scene_watch_librarian},
        {"description": "Retrace your steps to the castle entrance...", "handler": scene_abandoned_castle},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 4, checkpoint=scene_return_to_library)

def scene_see_book():
    print_wrapped("\nYou read the book's title: 'Book of Life'...")
    options = [
        {"description": "Read the book.", "handler": scene_read_book_of_life},
        {"description": "Check out the vial of liquid.", "handler": scene_see_vial},
        {"description": "Investigate the scroll.", "handler": scene_see_scroll},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3, checkpoint=scene_see_book)

def scene_read_book_of_life():
    print_wrapped("\nYou see that there are hundreds of names written in the book, each written in different "
                  "handwriting...You recall a legend about the power of the book of life...and the power of "
                  "writing your name in it...")
    options = [
        {"description": "Write your name in the book.", "handler": scene_write_your_name},
        {"description": "Check out the vial of liquid.", "handler": scene_see_vial},
        {"description": "Investigate the scroll.", "handler": scene_see_scroll},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3, checkpoint=scene_read_book_of_life)

def scene_write_your_name():
    from .core import check_or_return_none

    user_name = check_or_return_none("\nYou write your name in the book: ")
    if user_name is None:
        return None
    print_wrapped(f"\nThe ink dries as the letter ‘{user_name[-1]}’ lingers longer than the rest. You suddenly "
                  f"feel weak...")
    print_wrapped("As your strength fades, you realize that you misremembered the legend...for it does not give "
                  "life, but takes life away! ")
    print_wrapped(f"As you gaze upon your name...'{user_name}'...your life fades away, into the book.")
    print_wrapped("\nYou have died. Better luck awaits those who follow a different path...")
    return

def scene_see_vial():
    print_wrapped("\nYou pick up the vial of liquid...which is tied to a note with string. It reads: 'Vial of Preservation'.")
    options = [
        {"description": "Drink from the vial.", "handler": scene_drink_the_vial},
        {"description": "Examine the book.", "handler": scene_see_book},
        {"description": "Investigate the scroll.", "handler": scene_see_scroll},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3, checkpoint=scene_see_vial)

def scene_drink_the_vial():
    game_over("You drink the liquid. You feel odd...and start to see your limbs hardening to stone.", "curse")

def scene_watch_librarian():
    game_state["spied_on_librarian"] = True
    print_wrapped("\nThe lady picks up a book and whispers one word from its pages, out loud: 'goat'. She then "
                  "holds the book open towards the floor, and a goat emerges from the book's pages. The lady "
                  "points at the hallway, and the goat wanders off, down the hallway, and turns out of view. She "
                  "sets the book down and picks up another...")
    options = [
        {"description": "Walk up to the librarian.", "handler": scene_walk_up_to_librarian},
        {"description": "Follow the hallway the goat disappeared to.", "handler": scene_hallway},
    ]
    if game_state["continue_browsing"]:
        options.append({"description": "Ignore the lady. Glance up at the shadows.", "handler": scene_glance_at_shadows})
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3, checkpoint=scene_watch_librarian)

def scene_walk_up_to_librarian():
    game_state["knight_in_library"] = True
    print_wrapped("\nThe librarian whispers another word from another book out loud: 'knight'. Then she holds the "
                  "book open towards the floor again, and a knight in full armour emerges from the book's pages. "
                  "She then notices you...and whispers, 'Can I help you?'")
    options = [
        {"description": "Ask the librarian why she's whispering.", "handler": scene_ask_librarian},
        {"description": "Ask the librarian about the hallway.", "handler": scene_ask_librarian},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_walk_up_to_librarian)

def scene_explore_deeper():
    print_wrapped("\nYou find a skeleton of armor holding a glowing rune.")
    options = [
        {"description": "Examine the markings on the rune.", "handler": scene_examine_rune},
        {"description": "Remove the rune from the skeleton's grasp.", "handler": scene_take_rune},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_explore_deeper)

def scene_examine_rune():
    game_over("The markings warn that fire will consume any who dare to read the markings.", "fire")

def scene_take_rune():
    print_wrapped("\nOnce you store the rune away, the skeleton begins to move...")
    options = [
        {"description": "Behead the skeleton.", "handler": scene_behead_skeleton},
        {"description": "Give the rune back to the skeleton.", "handler": scene_return_rune}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_take_rune)

def scene_behead_skeleton():
    game_over("The headless skeleton swings its sword, striking one of your major arteries...skeletons don't need "
              "heads.", "mortal peril")

def scene_return_rune():
    game_over("As you put the rune back in the skeleton's bony hand, he crumbles to dust...and you begin to "
              "replace him, your limbs becoming bones.", "curse")


