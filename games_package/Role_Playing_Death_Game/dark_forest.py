from utils.helper_functions import update_player_state
from .core import player_state  # If you're using player_state directly here
from .core import game_state, check_and_run_random_handler, game_over, print_wrapped
from .state import ui_state

# --------------------
# Dark Forest
# --------------------

def scene_dark_forest():
    print_wrapped("\nThe trees whisper as you step forward. The path splits ahead.")
    options = [
        {"description": "Follow the glowing mushrooms.", "handler": scene_glowing_mushrooms},
        {"description": "Walk towards the eerie howling sound.", "handler": scene_howling_sound},
        {"description": "Venture down the lone cobblestone road.", "handler": scene_stone_road}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3, checkpoint=scene_dark_forest)

# --------------------
# Glowing Mushrooms
# --------------------

def scene_glowing_mushrooms():
    update_player_state(location="mushroom_path")
    print_wrapped("As you walk along the mushrooms, you notice the mushrooms quickly growing, blocking the path "
                  "forwards and backwards.")
    options = [
        {"description": "Climb the mushrooms to stay above them.", "handler": scene_climb_mushrooms},
        {"description": "Turn back to avoid this unnatural nature.", "handler": scene_turn_back},
        {"description": "Cut down the mushrooms growing in your way.", "handler": scene_cut_mushrooms},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3, checkpoint=scene_glowing_mushrooms)

def scene_climb_mushrooms():
    print_wrapped("As you climb the mushrooms, you see an old wooden nest above in a tree.")
    options = [
        {"description": "Keep climbing towards the tree.", "handler": scene_climb_to_tree},
        {"description": "Jump towards the platform to grab its ledge.", "handler": scene_jump_to_platform}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_climb_mushrooms)

def scene_climb_to_tree():
    game_over("The mushrooms stop growing...spraying a golden mist at you. As the mist touches you, "
              "your movements slow.", "curse")

def scene_jump_to_platform():
    print_wrapped("\nYou grab the ledge, the mushrooms underneath you spraying a golden mist where you once stood.")
    options = [
        {"description": "Climb higher to check your surroundings.", "handler": scene_climb_tree},
        {"description": "Take a moment to rest and gather your bearings.", "handler": scene_rest_on_platform}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_jump_to_platform)

def scene_rest_on_platform():
    game_over("The mist from the mushrooms rises up to you. As it touches your skin, you feel your limbs begin to "
              "slow.", "curse")

def scene_climb_tree():
    print_wrapped("\nYou notice the golden mist rising to where you were just standing...")
    options = [
        {"description": "Abandon the tree and jump to another.", "handler": scene_jump_to_tree},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_climb_tree)

def scene_jump_to_tree():
    game_over("You're not as nimble as you think. You slip and fall into the mist...which numbs your body and "
              "slows your movement.", "curse")

def scene_cut_mushrooms():
    game_over("As you cut the mushrooms, they spray a golden mist at you...which paralyzes your limbs one at a "
              "time.", "curse")

# --------------------
# Stone Road
# --------------------

def scene_stone_road():
    update_player_state(location="stone_road")
    print_wrapped("\nAs you follow the road, the sounds of creaking wood and ruffling leaves seem to surround you.")
    options = [
        {"description": "Get off the road.", "handler": scene_get_off_road},
        {"description": "Unsheathe your sword.", "handler": scene_unsheathe_sword}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_stone_road)

def scene_get_off_road():
    game_over("As you walk into the bushes, your skin brushes against poisonous thorns that shoot pain through "
              "your body.", "poison")

def scene_unsheathe_sword():
    print_wrapped("\nTo your amazement, branches begin swinging at you. You tear them all down...until a giant tree shows "
          "itself.")
    options = [
        {"description": "Cut at the tree's trunk.", "handler": scene_cut_trunk},
        {"description": "Flee the giant tree.", "handler": scene_flee_tree},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_unsheathe_sword)

def scene_cut_trunk():
    game_over("The tree's trunk is too thick...your sword is not enough.", "enemy")

def scene_flee_tree():
    game_over("The giant tree is too large...as you run, it swings its long branches at you.", "enemy")

# --------------------
# Howling Sounds
# --------------------

def scene_howling_sound():
    update_player_state(location="howling_path")
    print_wrapped("As you peer through the branches, pairs of yellow eyes fixate on you from the shadows...")
    options = [
        {"description": "Wield your sword in preparation.", "handler": scene_wield_sword},
        {"description": "Slowly back away into the shadows.", "handler": scene_back_away},
        {"description": "Turn back before meeting the holders of these eyes.", "handler": scene_turn_back},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3, checkpoint=scene_howling_sound)

def scene_wield_sword():
    update_player_state(weapon_ready=True)
    print_wrapped("Two wolves emerge from the bushes, stepping into view. The wolf on the left bears its teeth, "
                  "while the one on the right crouches down. Which side do you defend first?")
    options = [
        {"description": "Defend against the left.", "handler": scene_defend_left},
        {"description": "Prepare for an attack from the right.", "handler": scene_prep_for_right},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_wield_sword)

def scene_defend_left():
    update_player_state(state="wounded")
    print_wrapped("From your right side, you feel a sharp pain as a wolf strikes you. It had pounced from its "
                  "crouched position.")
    scene_fend_off_wolves()

def scene_prep_for_right():
    print_wrapped("")

def scene_fend_off_wolves():
    print_wrapped("One by one, vicious wolves lunge at you. You strike them down, each retreating, one by one...until "
          "the alpha emerges.")
    options = [
        {"description": "Stand ready.", "handler": scene_stand_ready},
        {"description": "Surrender and submit.", "handler": scene_surrender},
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_fend_off_wolves)

def scene_stand_ready():
    if not player_state.get("weapon_ready"):
        print_wrapped("You stand your ground, but without your weapon at the ready, the alpha strikes swiftly.")
        game_over("You are overpowered in moments.", "beast")
    elif player_state.get("wounded"):
        print_wrapped("You raise your weapon, but your earlier wounds slow you down...")
        game_over("The alpha outpaces your reaction and takes you down.", "beast")
    else:
        print_wrapped("You ready your weapon just in time and deliver a swift strike!")
        print_wrapped("The alpha flees into the darkness, and the forest path clears...")
        update_player_state(location="dark_forest_alpha_defeated")
        # You can route to a new scene if needed


def scene_surrender():
    game_over("\nThe alpha does not show mercy. It bears its teeth and strikes.", "beast")

def scene_back_away():
    game_over("The beasts still smell you...you are easy prey. After not watching your back, a wolf lunges at you "
              "from behind.", "beast")

# --------------------
# Turn Back
# --------------------

def scene_turn_back():
    if player_state["location"] == "mushroom_path":
        print_wrapped("\nThe glowing mushrooms continue to rapidly grow, as if they do not want you to return from where "
              "you came.")
        options = [
            {"description": "Cut down the mushrooms blocking your path.", "handler": scene_cut_mushrooms},
            {"description": "Weave through the mushrooms.", "handler": scene_weave_through_mushrooms}
        ]
        ui_state["current_options"] = options
        check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_turn_back)
    elif player_state["location"] == "stone_road":
        print_wrapped("\nWhen you turn around, the cobblestone path behind you is gone, replaced with thick, bushy trees.")
        options = [
            {"description": "Continue forward into the forest.", "handler": scene_continue_into_forest},
            {"description": "Cut down the trees.", "handler": scene_cut_down_trees}
        ]
        ui_state["current_options"] = options
        check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_turn_back)
    elif player_state["location"] == "howling_path":
        game_over("It's too late...a large wolf comes out of the shadows, bearing its fangs at you...", "beast")

def scene_weave_through_mushrooms():
    game_over("As your skin brushes against the mushrooms, your skin burns more and more...bringing you to nearly "
              "unbearable pain.", "poison")

def scene_continue_into_forest():
    print_wrapped("\nThe path forward is also gone...replaced with more trees...")
    options = [
        {"description": "Cut down the trees in your path.", "handler": scene_cut_down_trees}
    ]
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_continue_into_forest)

def scene_cut_down_trees():
    game_over("As you cut at the trees, every time you blink, they reappear...after cutting the same trees over "
              "and over, you realize you are unnaturally trapped.", "trapped")
