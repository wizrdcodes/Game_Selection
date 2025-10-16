import random
from .core import (
game_state,
player_state,
check_and_run_random_handler,
game_over,
print_wrapped,
check_or_return_none,
TORTURE_MODE
)
from .state import reset_game_state, ui_state
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
from utils.scene_helpers import scene_intro


# -------------------- Forgotten Cavern - Dictionaries --------------------

single_entrance_locations = {
    "dripping_cave",
    "glowing_hallway",
    "sword_chamber",
    "pool_shallow",
    "pool_mid",
    "pool_deep",
}

def get_creature_warning_message(level):
    default_messages = {
        1: "You hear something shift in the darkness...",
        2: "A faint screech echoes faintly through the cave. Something is aware of your presence...",
        3: "A deep, throaty hiss rolls across the cave walls. It's close.",
    }
    seen_messages = {
        1: "You hear the creature shift somewhere in the darkness...",
        2: "The creature screeches again...this time much closer...",
        3: "You hear the beating of leathery wings. It's hunting you.",
    }
    if has_memory("creature_seen"):
        return seen_messages.get(level, "")
    else:
        return default_messages.get(level, "")

def get_splash_warning_message(level):
    lit = player_state.get("torch_lit", False)

    # First-time warnings (no reliance on torchlight phrasing)
    default_messages = {
        1: "Shallow ripples swirl around you—something small slithers beneath the surface.",
        2: "The water sloshes higher, and you catch a flash of scales at your feet — this snake looks bigger.",
        3: "Waves crash around you as a larger serpent's head breaks the surface, narrowing its eyes on you.",
        4: "A massive serpent coils in the water’s center, its hood flared — something far deadlier approaches."
    }

    # Seen-before warnings (gate any torchlight references on actual torch state)
    # Keep your original lines; only the level-2 line conditionally adds the torchlight clause.
    seen_messages = {
        1: "You glimpse a tiny snake writhing just under the water’s edge.",
        2: ("A mid-sized snake’s tongue flickers — its scales glint in the torchlight."
            if lit else
            "A mid-sized snake’s tongue flickers somewhere in the dark."),
        3: "A serpent’s head lunges forward, fangs dripping venom as it sizes you up.",
        4: "The giant serpent hisses and rears — its jaws open wide in a deadly arc."
    }

    if has_memory("serpent_seen"):
        return seen_messages.get(level, "")
    else:
        return default_messages.get(level, default_messages[4])

# -------------------- Forgotten Cavern - Utility Functions --------------------

def light_torch():
    if player_state.get("torch_lit", False):
        print_wrapped("Your torch is already lit.", newline_delay=1)
    else:
        # turn the torch on
        update_player_state(torch_lit=True)
        print_wrapped("You light your torch...it dimly lights your surroundings.", newline_delay=1)
        # keep your incremental discovery system
        apply_discovery_for_current_state()
        # NEW: one-shot distance spotting only where apply_discovery doesn't cover it.
        # pool_shallow is already handled by apply_discovery_for_current_state(),
        # so we only need an explicit vantage for sword_chamber.
        loc = player_state.get("location")
        if loc == "sword_chamber":
            # You’ll need to implement this helper if you haven’t already.
            # It should be idempotent via memory flags to avoid doubles.
            maybe_spot_dock_raft_from_vantage("sword_chamber")
        # your existing location-specific "first time lit" hooks
        if loc == "forgotten_cavern":
            forgotten_cavern_lit()
        elif loc == "rock_pile":
            rock_pile_lit()
        elif loc == "dripping_cave":
            dripping_cavern_lit()
        elif loc == "glowing_hallway":
            glowing_hallway_lit()
        # your existing scene refresh routine
        if loc == "sword_chamber":
            return scene_sword_chamber(only_options=True)
        elif loc == "pool_shallow":
            return scene_wade_in_pool(only_options=True)
        elif loc == "pool_mid":
            return scene_pool_mid()
    # keep your option list rewrite + random handler
    updated_options = [opt for opt in ui_state["current_options"]
                       if "torch" not in opt["description"].lower()]
    updated_options.append({"description": "Extinguish your torch.",
                            "handler": extinguish_torch})
    ui_state["current_options"] = updated_options
    return check_and_run_random_handler(ui_state["current_options"], 8)

def extinguish_torch():
    if not player_state.get("torch_lit", False):
        print_wrapped("Your torch is already extinguished.", newline_delay=1)
    else:
        update_player_state(torch_lit=False)
        print_wrapped("You snuff out your torch. Darkness swallows your surroundings.", newline_delay=1)
    updated_options = []
    for opt in ui_state["current_options"]:
        if "torch" not in opt["description"].lower():
            updated_options.append(opt)
    updated_options.append({
        "description": "Light your torch.",
        "handler": light_torch
    })
    ui_state["current_options"] = updated_options
    check_and_run_random_handler(ui_state["current_options"], 8)

def check_and_trigger_lit_scene():
    if not player_state.get("torch_lit", False):
        return
    loc = player_state.get("location")
    run_first_time_lit_handler(loc)

def run_first_time_lit_handler(location: str) -> bool:
    """
    If this is the first time the torch has been lit in `location`,
    mark its flag and run its special handler.
    Returns True if we ran the handler, False otherwise.
    """
    entry = first_time_lit_scenes.get(location)
    if not entry:
        return False
    flag = entry["flag"]
    if not player_state.get(flag, False):
        player_state[flag] = True
        # call the single‐time handler
        entry["handler"]()
        return True
    return False

def add_torch_options(options_list):
    if not player_state.get("torch_lit", False):
        options_list.append({
            "description": "Light your torch.",
            "handler": light_torch
        })
    else:
        options_list.append({
            "description": "Extinguish your torch.",
            "handler": extinguish_torch
        })

def set_return_point(fn, *args, **kwargs):
    game_state["last_choice"] = (fn, args, kwargs)

def run_scene_with_options(options, num_choices=8, checkpoint=None):
    # Guardrails: catch accidental calls like checkpoint=foo() and handler=bar()
    if checkpoint is not None and not callable(checkpoint):
        raise TypeError(
            "Invalid checkpoint. Pass a function reference like 'checkpoint=loot_soldier' NOT "
            "'checkpoint=loot_soldier()'."
        )
    for i, opt in enumerate(options):
        h = opt.get("handler")
        if not callable(h):
            raise TypeError(
                f"Invalid options[{i}].handler. Pass a function reference like 'handler=read_soldiers_orders' (NOT "
                f"'handler=read_soldiers_orders()')."
            )
    if player_state.get("state") != "swimming":
        add_torch_options(options)
    ui_state["current_options"] = options
    check_and_run_random_handler(options, num_choices, checkpoint=checkpoint)

def return_to_scene_before_attack():
    """
    Jump back to whatever scene/options the caller registered as the 'safe return point'.
    Falls back to sword chamber options if nothing was registered.
    """
    print_wrapped("You gather your wits about you and continue...", newline_delay=1)
    handler, args, kwargs = game_state.get(
        "last_choice",
        (scene_sword_chamber, (), {"only_options": True})
    )
    return handler(*args, **kwargs)

# -------------------- Forgotten Cavern - Preludes --------------------

def check_too_much_noise(previous_noise):
    if game_state.get("cave_creature_killed", False):
        return False
    current_noise = game_state["cave_noise"]
    for level in range(previous_noise + 1, current_noise + 1):
        msg = get_creature_warning_message(level)
        if msg:
            print_wrapped(msg, newline_delay=1)
        if level >= 4:
            player_state["previous_location"] = player_state.get("location")
            scene_too_much_noise()
            return True
    return False

def slip_calculation(action="move"):
    if player_state.get("torch_lit", False):
        slip_chance = random.randint(0, 3)
        if slip_chance == 1:
            prefix = "With your lit torch in one hand, "
            if action == "climb":
                detail = "you slip mid-climb, hitting your head on the stone...never waking again."
            elif action == "descend":
                detail = "you slip as you descend the rocks, cracking your skull on the ground."
            elif action == "swing":
                detail = "you lose your grip on the bone ladder and fall to your doom down the drop."
            else:
                prefix = ""
                detail = "You slip in the darkness, your torch offering little protection as your head meets stone."
            print_wrapped(prefix + detail, newline_delay=1)
            print_wrapped("You have died. Better luck awaits those who follow a different path...", newline_delay=1.5)
            return True
    return False

def maybe_make_noise(condition: bool, message: str = None, chance: int = 2, noise_amount: int = 1):
    """
    condition: when to allow noise (e.g. player_state['torch_lit'] or always True)
    message: what to print when noise occurs
    chance: 1 in X chance for noise (default 1 in 2)
    noise_amount: how much to increase game_state['cave_noise'] by
    """
    if condition and random.randint(1, chance) == 1:
        if message is not None:
            print_wrapped(message, newline_delay=1.5)
            if "step on something" in message:
                remember("cracked_bones")
        prev = game_state["cave_noise"]
        game_state["cave_noise"] += noise_amount
        return check_too_much_noise(prev)
    return False

# -------------------- Forgotten Cavern - Preludes --------------------

def _prelude_rock_descension():
    """
    Landing noise when descending with torch lit from the rock pile (or climb-down string).
    """
    if player_state.get("location") == "rock_pile":
        if player_state.get("torch_lit", False):
            return maybe_make_noise(True, "Your landing echoes through the cave...",
                chance=1, noise_amount=1)
    return False

def maybe_crack_bones():
    if not has_memory("cracked_bones"):
        if not has_memory("bones"):
            return maybe_make_noise(not player_state.get("torch_lit", False),
            "You hear a loud crack echo through the cave as you step on something in the dark...",
            noise_amount=1)
        else:
            return maybe_make_noise(not player_state.get("torch_lit", False),
            "You step on a bone, and a loud crack echoes through the cave in the dark...",
            noise_amount=1)
    else:
        if not has_memory("bones"):
            return maybe_make_noise(not player_state.get("torch_lit", False),
            "Your steps cause another loud crack to echo in the dark again...",
            noise_amount=1)
        else:
            return maybe_make_noise(not player_state.get("torch_lit", False),
            "You step on another bone, its loud crack echoing in the dark again...",
            noise_amount=1)

def _prelude_crack_if_unlit():
    """
    Before entering any dark scene, if torch is unlit, crack bones noise.
    """
    if not player_state.get("torch_lit", False):
        return maybe_crack_bones()
    return False

# -------------------- Forgotten Cavern --------------------

def forgotten_cavern_intro():
    if not has_seen_intro("forgotten_cavern"):
        print_wrapped("The cavern gets darker and colder as you climb deeper.", newline_delay=1.5)
        print_wrapped("This cave is larger than you thought, and you struggle to see...", newline_delay=1.5)
        print_wrapped("To your left is a large pile of rocks, and to your right a distant glow.", newline_delay=1.5)
        print_wrapped("You hear what sounds like dripping water echo through tunnels...", newline_delay=1.5)
    remember_intro("forgotten_cavern")

@scene_intro([
    "The cavern is dark and cold.", "As you climb deeper, you realize the cave is larger than you thought... ", 1.5,
    "You struggle to see. To your left is a large pile of rocks, and to your right a distant glow. ", 2,
    "You hear dripping sounds echo through the tunnels...", 1.5
], return_entries=[
    "You return to the cavern floor."
], preludes=[
    _prelude_crack_if_unlit
])
def scene_forgotten_cavern(only_options=False):
    if not only_options:
        update_player_state(location="forgotten_cavern")
        if player_state.get("torch_lit", False):
            forgotten_cavern_lit()
    options = []
    if not has_seen_intro("dripping_cavern"):
        options.append({"description": "Follow the dripping sounds.", "handler": scene_dripping_cavern})
    else:
        options.append({"description": "Return to the fallen soldier's cavern.", "handler": scene_dripping_cavern})
    if not has_seen_intro("glowing_hallway"):
        options.append({"description": "Follow the distant glow.", "handler": scene_glowing_hallway})
    else:
        options.append({"description": "Return to the glowing hallway.", "handler": scene_glowing_hallway})
    if not has_memory("rock_pile"):
        options.append({"description": "Climb up onto the rocks to scope out the cave.", "handler": scene_rock_pile})
    else:
        options.append({"description": "Climb the rocks again.", "handler": scene_rock_pile})
    run_scene_with_options(options, 4, checkpoint=scene_forgotten_cavern)

@scene_intro([
    "As you gaze around the cave, you see bones littering the ground.",
])
def forgotten_cavern_lit():
    has_memory("bones")
    pass

def scene_return_to_cavern_floor():
    if player_state.get("location") == "dripping_cave":
        print_wrapped("You return to the main cavern, the dripping sounds reducing to echoes...", newline_delay=1)
        update_player_state(location="forgotten_cavern")
        if player_state.get("torch_lit", False):
            forgotten_cavern_lit()
        elif maybe_crack_bones():
            return
    if player_state.get("location") == "rock_pile":
        if slip_calculation(action="descend"):
            return
        print_wrapped("You return to the cavern floor...", newline_delay=1)
        if player_state.get("torch_lit", False):
            forgotten_cavern_lit()
        update_player_state(location="forgotten_cavern")
    if player_state.get("location") == "glowing_hallway":
        print_wrapped("You return from the hallway to the main cavern, the glow fading behind you...", newline_delay=1)
        update_player_state(location="forgotten_cavern")
        if player_state.get("torch_lit", False):
            forgotten_cavern_lit()
        if maybe_crack_bones():
            return
    scene_forgotten_cavern(only_options=True)

# -------------------- Rock Pile Functions --------------------

def maybe_displace_rocks():
    prev = player_state.get("location") or player_state.get("previous_location")
    if prev in ("bone_ladder", "sword_chamber", "rock_pile"):
        return maybe_make_noise(not player_state.get("torch_lit", False),
        "Rocks scatter noisily as you move blindly, the sharp echoes bouncing off unseen walls.",
        noise_amount=1)
    else:
        return False

def _prelude_return_from_chamber_or_ladder():
    """
    Fire-and-forget noise when arriving from sword_chamber/ladder.
    Never aborts entry into scene_rock_pile.
    """
    loc = player_state.get("location")
    pos = player_state.get("position")
    if loc in ("sword_chamber", "ladder", "dock"):
        _ = maybe_displace_rocks()  # may print & bump cave_noise; ignore return
    return False

def _prelude_dynamic_slip_rock_pile():
    """
    If we’re at the top of the rock pile (i.e. ‘rock_pile’ location),
    choose the slip direction based on the last known position:
      – If we came *up* here (previous_location was one of the pool or cavern
        scenes), use 'climb'
      – If we came *down* here (previous_location was the pillar or dungeon),
        use 'descend'
    Only works if we update location for every real movement.
    """
    if player_state.get("location") != "rock_pile": return False
    prev = player_state.get("previous_location")
    # pick your incoming scenes accordingly:
    if prev in ("forgotten_cavern", "dripping_cavern", "glowing_hallway"):
        action = "climb"
    elif prev == "sword_chamber":
        return False
    else:
        action = "descend"
    return slip_calculation(action=action)

# -------------------- Rock Pile  --------------------

@scene_intro([
    "You climb the rocks to survey your surroundings...jagged stones and narrow ledges test your balance.", 2,
    "You reach the top to find a tunnel to your left, and a steep drop ahead.", 1.5,
    "You hear a faint vocal clicking from above, subtle and short..."
], return_entries=[
    "You return to the rocky ledge overlooking the cavern."
], preludes=[
    maybe_displace_rocks,
    lambda: _prelude_tunnel_water_extinguish(),
    _prelude_dynamic_slip_rock_pile,
    _prelude_return_from_chamber_or_ladder
])
def scene_rock_pile(only_options=False):
    if not only_options:
        # if slip_calculation(action="climb"):
        #     return
        update_player_state(location="rock_pile")
        if player_state.get("torch_lit", False):
            rock_pile_lit()
    options = [
        {"description": "Get down from the rocks.", "handler": scene_return_to_cavern_floor},
    ]
    if not has_seen_intro("glowing_hallway"):
        options.append({"description": "Follow the distant glow.", "handler": scene_glowing_hallway})
    else:
        options.append({"description": "Return to the glowing hallway.", "handler": scene_glowing_hallway})
    if not has_seen_intro("dripping_cavern"):
        options.append({"description": "Follow the dripping sounds.", "handler": scene_dripping_cavern})
    else:
        options.append({"description": "Return to the fallen soldier's cavern.", "handler": scene_dripping_cavern})
    if not has_seen_intro("sword_chamber"):
        options.append({"description": "Enter the tunnel on your left.", "handler": scene_sword_chamber})
    else:
        options.append({"description": "Return to the chamber.", "handler": scene_sword_chamber})
    if has_memory("ladder_seen"):
        options.append({"description": "Jump to the ladder of bones.", "handler": scene_jump_to_ladder})
    run_scene_with_options(options, 6, checkpoint=scene_rock_pile)

@scene_intro([
    "You make out a ladder of bones hanging from a cliff above you, over the drop...",
])
def rock_pile_lit():
    if not has_memory("creature_seen") and not game_state.get("cave_creature_killed"):
        if not has_memory("attacked_by_creature"):
            print_wrapped("The light from your torch illuminates a creature suspended from the cave ceiling...", newline_delay=1.5)
            print_wrapped("In a sleepy trance, its almost-human figure stretches its winged arms, then folds them up again"
                          " to rest...", newline_delay=2.5)
        else:
            print_wrapped("The light from your torch illuminates the creature that came after you before, suspended "
                          "from the cave ceiling...", newline_delay=2.5)
            print_wrapped("In a sleepy trance, its almost-human figure stretches its winged arms, then folds them up again"
                          " to rest...", newline_delay=2.5)
        remember("ladder_seen")
        remember("creature_seen")

# -------------------- Dripping Sounds --------------------

@scene_intro([
    "You enter the tunnel into a small cave...and find the source of the dripping sound.", 1.5,
    "A soldier's fresh corpse lays across a rock, drained of his blood...save the drops hitting the ground.", 2,
    "Under the soldier, you see an elegant shield, emitting a faint glow...", 1.5
], return_entries=[
    "You return to the cave of the fallen soldier."
], preludes=[
    _prelude_dynamic_slip_rock_pile,
    _prelude_rock_descension,
    _prelude_crack_if_unlit
])
def scene_dripping_cavern(only_options=False):
    if not only_options:
        # if player_state.get("location") == "rock_pile":
        #     if slip_calculation(action="descend"): return
        #     if player_state.get("torch_lit"):
        #         print_wrapped("With your lit torch in hand, you resort to hopping down from the rocks.", newline_delay=1)
        #         if maybe_make_noise(True,"Your landing echoes through the cave...",
        #             chance=1, noise_amount=1): return
        #         update_player_state(location="forgotten_cavern")
        # if player_state.get("location") != "dripping_cave":
        #     if not player_state.get("torch_lit", False) and maybe_crack_bones(): return
        update_player_state(location="dripping_cave")
        if player_state.get("torch_lit", False):
            dripping_cavern_lit()
    options = [
        {"description": "Leave the small cave.", "handler": scene_return_to_cavern_floor},
    ]
    if not has_item("elegant_shield"):
        options.append({"description": "Take the elegant shield.", "handler": take_shield})
    elif not has_item("soldiers_orders"):
        options.append({"description": "Check the fallen soldier.", "handler": loot_soldier})
    else:
        options.append({"description": "Read the note.", "handler": read_soldiers_orders})
    run_scene_with_options(options, 3, checkpoint=scene_dripping_cavern)

@scene_intro([
    "You make out a warning written in blood on the cave's wall: 'Beware the creature'..."
])
def dripping_cavern_lit():
    pass

def take_shield(only_options=False):
    if not only_options:
        print_wrapped("As you pull the shield from the soldier, he noisily rolls over and falls, his armour clanging, "
                      "echoing through the cavern.", newline_delay=2)
        print_wrapped("The shield continues to glow faintly as you hold it. You feel a powerful sense of protection...", newline_delay=1.5)
        add_to_inventory("elegant_shield")
        if maybe_make_noise(True, chance=1,noise_amount=2):
            return
    options = [
        {"description": "Leave the small cave.", "handler": scene_return_to_cavern_floor},
    ]
    if not has_item("soldiers_orders"):
        options.append({"description": "Check the fallen soldier.", "handler": loot_soldier})
    run_scene_with_options(options, checkpoint=scene_dripping_cavern)

def loot_soldier(only_options=False):
    if not only_options:
        print_wrapped("You check the soldier for any information.", newline_delay=1)
        print_wrapped("You find a slip of paper tucked under his sheath, and pull it out to store it.", newline_delay=1.5)
        print_wrapped("The sheath falls to the floor, its impact echoing through the cavern...", newline_delay=1.5)
        add_to_inventory("soldiers_orders")
        if maybe_make_noise(True, chance=1,noise_amount=1):
            return
    options = [
        {"description": "Leave the small cave.", "handler": scene_return_to_cavern_floor},
        {"description": "Read the note.", "handler": read_soldiers_orders},
    ]
    run_scene_with_options(options, checkpoint=loot_soldier)

def read_soldiers_orders():
    print_wrapped("The paper you found on the fallen soldier reads:", newline_delay=1)
    print_wrapped("By decree of the High Council, you are to descend into the Forgotten Cavern and recover proof of "
                  "the myth they call Valhalla. ", newline_delay=2.5)
    print_wrapped("Beware the creature that stalks the dark. It is drawn to noise. ", newline_delay=2)
    print_wrapped("Return if the way proves false. If the glowing key reveals itself...proceed. ", newline_delay=1.5)
    print_wrapped("Glory to those who open the gate of gods.", newline_delay=1)
    options = [
        {"description": "Leave the small cave.", "handler": scene_return_to_cavern_floor},
    ]
    run_scene_with_options(options, checkpoint=scene_dripping_cavern)

# -------------------- Distant Glow --------------------

@scene_intro([
    "As you follow the soft light, the cavern turns into a smooth-stone hallway.",
    "Further down the hallway, you see the light, somehow emitting through a solid wall...", 1.5,
], return_entries=[
    "You return to the hallway, the glowing light still pouring through the wall..."
], preludes=[
    _prelude_dynamic_slip_rock_pile,
    _prelude_rock_descension,
    _prelude_crack_if_unlit
])
def scene_glowing_hallway(only_options=False):
    if not only_options:
        # if player_state["location"] == "rock_pile":
        #     if player_state["torch_lit"]:
        #         print_wrapped("With your lit torch in hand, you resort to hopping down from the rocks.", newline_delay=1)
        #         if maybe_make_noise(player_state["torch_lit"],
        #             "Your landing echoes through the cave...",
        #             chance=1, noise_amount=1):
        #             return
        #     else:
        #         print_wrapped("You climb down from the rocks.", newline_delay=1)
        #     update_player_state(location="forgotten_cavern")
        # if player_state["location"] == "forgotten_cavern":
        #     if maybe_crack_bones():
        #         return
        # elif player_state["location"] == "glowing_door":
        #     print_wrapped("You head back through the hallway, the glowing light fading behind you...", newline_delay=1)
        update_player_state(location="glowing_hallway")
        if player_state.get("torch_lit", False):
            glowing_hallway_lit()
    options = [
        {"description": "Leave the hallway.", "handler": scene_return_to_cavern_floor},
    ]
    if not has_seen_intro("glowing_door"):
        options.append({"description": "Head to the glowing door.", "handler": scene_glowing_door})
    else:
        options.append({"description": "Return to the glowing door.", "handler": scene_glowing_door})
    run_scene_with_options(options, 3, checkpoint=scene_glowing_hallway)

@scene_intro([
    "As your flickering light lands on the walls, you notice hieroglyphs etched into them...", 1.5,
    "You're able to decipher two words...'Danger'...and 'Shield'...", 1.5
])
def glowing_hallway_lit():
    pass

@scene_intro([
    "As you walk up to the wall, you discover that the glow emits from solid lines in the wall...", 1.5,
    "Somehow, solid light has been fused into the door, surrounding a glowing slot in the center.", 1.5
])
def scene_glowing_door(only_options=False):
    if not only_options and not game_state.get("glowing_door_trap_triggered", False):
        game_state["glowing_door_trap_triggered"] = True
        print_wrapped("Suddenly, as you take a step forward, the stone below your foot sinks...", newline_delay=1.5)
        print_wrapped("Ancient glyphs around the door flicker to life, shimmering in fiery orange.", newline_delay=1)
        print_wrapped("You feel any and all light around you surge into the door, then into the glyphs, "
                      "aimed towards you...", newline_delay=2.5)
        if not has_item("elegant_shield"):
            print_wrapped("A celestial fire erupts from the glyphs, engulfing you. Your scream echoes through the "
                          "cave, long after your demise.", newline_delay=2)
            print_wrapped("You have died. Better luck awaits those who follow a different path...", newline_delay=1.5)
            return
        else:
            options = [
                {"description": "Wield the shield...", "handler": survive_glowing_door_trap},
            ]
            ui_state["current_options"] = options
            check_and_run_random_handler(ui_state["current_options"], checkpoint=scene_glowing_door)
            return
    else:
        options = [
            {"description": "Leave the glowing door.", "handler": scene_glowing_hallway},
        ]
        if has_item("glowing_key"):
            options.append({"description": "Insert the glowing key.", "handler": insert_glowing_key})
        if not has_memory("glowing_slot"):
            options.append({"description": "Examine the glowing slot.", "handler": examine_glowing_slot})
        else:
            options.append({"description": "Examine the glowing slot again.", "handler": examine_glowing_slot})
        update_player_state(location="glowing_door")
        run_scene_with_options(options, 4, checkpoint=scene_glowing_door)

@scene_intro([
    "You take a closer look at the glowing slot. You're missing something...", 1.25
], return_entries=[
    "You examine the glowing slot again...maybe something can open it..."
])
def examine_glowing_slot():
    options = [
        {"description": "Leave the hallway.", "handler": scene_return_to_cavern_floor},
    ]
    run_scene_with_options(options, checkpoint=examine_glowing_slot)

def insert_glowing_key():
    print_wrapped("You pull the glowing key out of your pack, its light matching the door...almost fusing with it...", newline_delay=1.5)
    print_wrapped("The key perfectly fits the slot, like an eternal light being reunited with its source.", newline_delay=1.5)
    print_wrapped("The light infused into the door begins to spread until the entire door is ony light, and you see "
                  "the truth: Valhalla exists, and you have found it.", newline_delay=2.5)
    print_wrapped("Congratulations! You survived the Forgotten Cavern. Great choices!", newline_delay=1.5)

def survive_glowing_door_trap():
    game_state["glowing_door_trap_triggered"] = True
    print_wrapped("You hold the shield in front of you...and a white/orange beam of fire blasts around you.", newline_delay=1)
    print_wrapped("The celestial energy subsides, and you feel the shield's power unscathed, your body "
                  "completely unharmed.", newline_delay=2)
    print_wrapped("You gather your wits about you and consider your next move...", newline_delay=1.5)
    scene_glowing_door(only_options=True)

# -------------------- Sword Tunnel - Functions & Variables --------------------

def check_too_much_splash(previous_splash):
    """Returns True if an attack scene (snake or giant serpent) has run. Otherwise, returns False."""
    if game_state.get("serpent_killed", False):
        return False
    current_splash = game_state.get("splash_amount", 0)
    for level in range(previous_splash + 1, current_splash + 1):
        msg = get_splash_warning_message(level)
        if msg:
            print_wrapped(msg, newline_delay=1.5)
        if level in (1, 2, 3, 4):
            player_state["previous_location"] = player_state.get("location")
            if level == 1:
                scene_tiny_snake_attack()
            elif level == 2:
                scene_medium_snake_attack()
            elif level == 3:
                scene_large_snake_attack()
            elif level >= 4:
                scene_serpent_attack()
            return True
    return False

def maybe_splash(chance: int = 2):
    previous_splash = game_state.get("splash_amount", 0)
    if random.randint(1, chance) == 1:
        game_state["splash_amount"] = previous_splash + 1
    return check_too_much_splash(previous_splash)

def _prelude_tunnel_water_extinguish():
    """Runs only when crossing the tunnel boundary between rock_pile and sword_chamber."""
    # At prelude time, your scenes haven't called update_player_state() yet,
    # so player_state["location"] still reflects the *previous* location.
    prev = player_state.get("location") or player_state.get("previous_location")

    # Only fire if we are *coming from* the other side of the tunnel
    if prev not in ("rock_pile", "sword_chamber"):
        return False  # ignore entries from cavern floor, docks, etc.

    print_wrapped("As you pass through the tunnel mouth, a thin sheet of water spatters over you.")
    if player_state.get("torch_lit"):
        print_wrapped("Your torch sputters and goes dark.", newline_delay=0.6)
        player_state["torch_lit"] = False
    return False  # never abort

def _prelude_splash_in_tunnel():
    """
    Trigger water splash or serpent warning before entering tunnel.
    """
    loc = player_state.get("location")
    pos = player_state.get("position")
    if loc in ("pool_mid", "pool_shallow", "pool_deep") or pos in ("raft", "submerged_pillar"):
        return maybe_splash()
    return False

def _prelude_spot_on_arrival_to_sword_chamber():
    if player_state.get("current_scene") == "sword_chamber":
        maybe_spot_dock_raft_from_vantage("sword_chamber")
    return False

def _pool_shallow_return_entries():
    loc = player_state.get("location")
    if loc == "pool_mid":
        return ["You head towards the chamber entrance again..."]
    if loc in ("sword_chamber", "dock"):
        return ["You head towards the stone pillars again..."]
    return ["You find yourself near the tunnel mouth again."]

def _prelude_splash_on_arrival_to_pillar():
    # This is exactly what your maybe_splash() does today in scene_submerged_pillar
    return maybe_splash()  # returns True if an attack scene ran

def _prelude_slip_from_pillar():
    """
    Slip check when jumping to or from a submerged pillar.
    """
    if player_state.get("location") in ("pool_mid", "pool_deep") and player_state.get("position") == "submerged_pillar":
        # use 'jump' to indicate leap
        return slip_calculation(action="jump")
    return False

DISCOVERY_ORDER = ("none", "silhouette", "hint", "boulder_sword")

def _base_discovery_level_for(location: str) -> int:
    """
    Torch OFF baseline:
      sword_chamber: 0 (mist only)
      pool_shallow:  1 (silhouette of ruins)
      pool_mid:      2 (pillars + shadowed boulder)
      pool_deep:     3 (boulder + sword)
    """
    if location == "sword_chamber": return 0
    if location == "pool_shallow":  return 1
    if location == "pool_mid":      return 2
    if location == "pool_deep":     return 3
    return 0

def _current_target_discovery_level() -> int:
    loc = player_state.get("location")
    base = _base_discovery_level_for(loc)
    # Torch lit gives +1 (capped at 3)
    if player_state.get("torch_lit"):
        base = min(3, base + 1)
    return base

def apply_discovery_for_current_state():
    """
    Prints the *next* unseen reveal(s) up to the target level and stores memory keys so
    we never print them again. Also handles dock/raft side-note in shallow.
    """
    target = _current_target_discovery_level()

    # Level 1: silhouettes of ruins
    if target >= 1 and not has_memory(MEM_RUINS_SILH):
        print_wrapped("Past the shallow water, you make out a structure through the haze...")
        remember(MEM_RUINS_SILH)

    # Level 2: pillars + larger shadowed form (boulder silhouette)
    if target >= 2 and not has_memory(MEM_RUINS_HINT):
        print_wrapped("Through the mist, you see ruined pillars, leading deeper towards a shadowy form looming behind...")
        remember(MEM_RUINS_HINT)

    # Level 3: boulder + sword
    if target >= 3 and not has_memory(MEM_BOULDER_SWORD):
        print_wrapped("Up close, the boulder looms out of the dark water. A sword glints from its heart...", newline_delay=1.2)
        print_wrapped("A mystic energy gravitates around the hilt of the sword...")
        remember(MEM_BOULDER_SWORD)

    # --- Side note: dock/raft discovery rules at shallow ---
    if player_state.get("location") == "pool_shallow":

        # Spot DOCK from the shallow
        if not has_memory(MEM_DOCK_SPOTTED):
            print_wrapped("Through the haze, you can make out a weathered dock along the near shore.",
                          newline_delay=0.8)
            remember(MEM_DOCK_SPOTTED)

        # Spot RAFT from the shallow (only if it’s actually there)
        if (game_state.get("raft_status") == "pool_shallow"
                and not has_memory(MEM_RAFT_SPOTTED)):

            # Skip if you’ve already examined it up close to avoid “double” copy in the same traversal
            if not has_memory(MEM_RAFT_EXAMINED):
                print_wrapped("Something floats, loosely moored at the dock—looks like a small raft.",
                              newline_delay=0.8)
                remember(MEM_RAFT_SPOTTED)

# Memory keys used in this file
MEM_RUINS_SILH = "seen:ruins_silhouette"   # set at pool_shallow when silhouettes are first noticed
MEM_RUINS_HINT = "seen:ruins_hint"         # “pillars before a structure” (upgrade from silhouette)
MEM_DOCK       = "dock_seen"               # dock identified (raft details still mostly at shallow)
MEM_RAFT_SEEN = "raft_seen"
MEM_DOCK_SPOTTED = "dock_spotted"
MEM_DOCK_EXAMINED = "dock_examined"
MEM_RAFT_SPOTTED = "raft_spotted"
MEM_RAFT_EXAMINED = "raft_examined"
MEM_BOULDER_SWORD = "seen:boulder_sword"
MEM_BOARD_RAFT_POOL_MID = "intro:board_raft_pool_mid"

# -------------------- Sword Chamber --------------------

def sword_chamber():
    if not has_seen_intro("sword_chamber"):
        print_wrapped("At the pool’s far edge, a massive boulder juts from the water, a mystic sword embedded "
                      "deep within its core.", newline_delay=2)
        print_wrapped("The blade glows faintly, as if calling to you...", newline_delay=1.5)
    remember_intro("sword_chamber")

@scene_intro([
    "The chamber opens into darkness.", "You see the shallow end of a pool of water, the misty air obscuring what "
    "lays ahead...", 1.75
], return_entries=[
    "You return to the chamber entrance. The air is cool and damp."
], preludes=[
    maybe_displace_rocks,
    _prelude_tunnel_water_extinguish,
    _prelude_spot_on_arrival_to_sword_chamber
])
def scene_sword_chamber(only_options=False):
    if not only_options:
        loc = player_state.get("location")
        pos = player_state.get("position")
        if has_seen_intro("sword_chamber"):
            if pos == "raft":
                print_wrapped("You return to the chamber's entrance from the misty waters.", newline_delay=1)
                print_wrapped("As the old raft reaches the shore, it breaks apart.", newline_delay=1)
                break_raft("pool_shallow")
            elif loc == "pool_shallow" and player_state.get("state") == "wading":
                print_wrapped("You wade out of the shallow water to the chamber's tunnel entrance.", newline_delay=1)
            # elif prev == "pool_mid":
            #     print_wrapped("You return to the cave which holds the sword.")
            # elif loc == "rock_pile":
            #     if not has_memory(MEM_BOULDER_SWORD):
            #         print_wrapped("You return to the pool chamber.")
            #     elif has_item("mystic_sword"):
            #         print_wrapped("You return to the cave which held the mystic sword.", newline_delay=1)
            #     else:
            #         print_wrapped("You return to the cave which holds the mystic sword.", newline_delay=1)
    update_player_state(location="sword_chamber", position=None, state=None)
    apply_discovery_for_current_state()
    if player_state.get("torch_lit", False):
        dock_lit()
    options = [
        {"description": "Return through the tunnel.", "handler": scene_return_to_rocks},
        {"description": "Wade into the pool.", "handler": scene_wade_in_pool},
    ]
    if has_memory(MEM_DOCK):
        options.append({"description": "Check out the old dock.", "handler": scene_dock})
    run_scene_with_options(options, 5, checkpoint=scene_sword_chamber)

@scene_intro([
    # "As you scan the chamber, you spot a dock nearby, old ropes holding old logs together.", 1.5
])
def dock_lit():
    if not has_memory(MEM_DOCK):
        print_wrapped("You spot an old dock to the side of the shallows.")
        remember(MEM_DOCK)

# -------------------- Dock + Raft Functions & Preludes --------------------

def break_raft(at: str, *, sink_oar_if_left: bool = True):
    """
    Mark the raft as broken and remember *where* it broke.
    Optionally sinks the oar if it was still on the raft and not in inventory.
    """
    game_state["raft_status"] = "broken"
    game_state["raft_broken_at"] = at  # "pool_shallow" or "pool_mid"
    if sink_oar_if_left and game_state.get("oar_on_raft", False) and not has_item("oar"):
        game_state["oar_status"] = "underwater"
        game_state["oar_on_raft"] = False

def raft_is_available_at(location: str) -> bool:
    """True only when the raft is intact and currently at the requested location."""
    return game_state.get("raft_status") in ("pool_shallow", "pool_mid") and game_state.get("raft_status") == location

def raft_wreck_at(location: str) -> bool:
    """True when the broken raft wreck is at the requested location."""
    return game_state.get("raft_status") == "broken" and game_state.get("raft_broken_at") == location

def maybe_spot_dock_raft_from_vantage(vantage: str):
    """
    Print one-shot 'spotted from afar' lines when torch is lit.
    vantage: 'sword_chamber' | 'pool_shallow'
    """
    if not player_state.get("torch_lit"):
        return
    if vantage == "sword_chamber":
        # Distant, no raft unless it can plausibly be seen from here (your call).
        if not has_memory(MEM_DOCK_SPOTTED):
            print_wrapped("In the distance, a weathered dock clings to the near shore of the cavern pool.", newline_delay=0.8)
            remember(MEM_DOCK_SPOTTED)
        # If you DO allow raft visibility from here:
        if game_state.get("raft_status") == "pool_shallow" and not has_memory(MEM_RAFT_SPOTTED):
            print_wrapped("Something small floats by that dock—likely a raft.", newline_delay=0.8)
            remember(MEM_RAFT_SPOTTED)
    elif vantage == "pool_shallow":
        if not has_memory(MEM_DOCK_SPOTTED):
            print_wrapped("Through the haze, you can make out a weathered dock along the near shore.", newline_delay=0.8)
            remember(MEM_DOCK_SPOTTED)
        if game_state.get("raft_status") == "pool_shallow" and not has_memory(MEM_RAFT_SPOTTED):
            print_wrapped("Something floats, loosely moored at the dock—looks like a small raft.", newline_delay=0.8)
            remember(MEM_RAFT_SPOTTED)
    # Invariant: seeing raft implies dock seen
    if has_memory(MEM_RAFT_SPOTTED) and not has_memory(MEM_DOCK_SPOTTED):
        remember(MEM_DOCK_SPOTTED)

def _prelude_spot_on_arrival_to_shallow():
    if player_state.get("current_scene") == "pool_shallow":
        maybe_spot_dock_raft_from_vantage("pool_shallow")
    return False

# -------------------- Dock + Raft --------------------

def dock_intro_entries():
    """
    Close-up dock/raft intro when actually at the dock.
    - If not examined yet, do detailed lines and mark EXAMINED (and SPOTTED for consistency).
    - If already examined, return [] so return_entries handles revisits.
    """
    out = []
    # Up-close dock (first time)
    if not has_memory(MEM_DOCK_EXAMINED):
        out += ["Up close, the dock’s planks are slick and splintered at the edges.", 1.0]
        remember(MEM_DOCK_EXAMINED)
        # If you jumped straight here without seeing it from afar, mark spotted too
        if not has_memory(MEM_DOCK_SPOTTED):
            remember(MEM_DOCK_SPOTTED)
    # Up-close raft (first time) only if it's actually here
    if (game_state.get("raft_status") == "pool_shallow"
        and not has_memory(MEM_RAFT_EXAMINED)):
        out += ["A bound log-raft bobs against the mooring line.", 1.0]
        remember(MEM_RAFT_EXAMINED)
        if not has_memory(MEM_RAFT_SPOTTED):
            remember(MEM_RAFT_SPOTTED)
        # Oar detail only if present and not already taken
        if game_state.get("oar_on_raft", True) and not has_item("oar"):
            out += ["An old wooden oar rests across the logs; a short coil of rope is tucked beneath.", 1.0]
    return out

def describe_dock_raft_examined():
    # Dock (first up-close)
    if not has_memory(MEM_DOCK_EXAMINED):
        print_wrapped("Up close, the dock’s planks are slick and splintered at the edges.", newline_delay=1.0)
        remember(MEM_DOCK_EXAMINED)
        if not has_memory(MEM_DOCK_SPOTTED):
            remember(MEM_DOCK_SPOTTED)
    # Raft (first up-close, only if here)
    if game_state.get("raft_status") == "pool_shallow" and not has_memory(MEM_RAFT_EXAMINED):
        print_wrapped("A bound log-raft bobs against the mooring line.", newline_delay=1.0)
        remember(MEM_RAFT_EXAMINED)
        if not has_memory(MEM_RAFT_SPOTTED):
            remember(MEM_RAFT_SPOTTED)
        if game_state.get("oar_on_raft", True) and not has_item("oar"):
            print_wrapped("An old wooden oar rests across the logs; a short coil of rope is tucked beneath.", newline_delay=0.9)

@scene_intro([dock_intro_entries], return_entries=["You return to the dock."])
def scene_dock(only_options=False):
    if not only_options:
        update_player_state(location="pool_shallow", position="dock", state=None)
        apply_discovery_for_current_state()
    options = [
        {"description": "Return through the tunnel.", "handler": scene_return_to_rocks},
        {"description": "Wade into the pool.", "handler": scene_wade_in_pool},
    ]
    if has_memory("raft_seen") and raft_is_available_at("pool_shallow"):
        options.append({"description": "Board the raft.", "handler": scene_board_raft})
    run_scene_with_options(options, 4, checkpoint=scene_dock)

def arrival_interrupts_board_raft():
    # Run immediately after the intro is shown, before changing state or printing options.
    if maybe_make_noise(True, chance=3, noise_amount=1):
        return True
    if maybe_splash(chance=3):
        return True
    return False

# def board_raft_message():
#     if not has_seen_intro("board_raft"):
#         print_wrapped("You step onto the raft, your feet inches above the surface of the water. ", newline_delay=1.5)
#         print_wrapped("Its logs creak under each step and send small splashes across the pool...", newline_delay=1.5)
#         remember_intro("board_raft")
#         if maybe_make_noise(True,
#             chance=3, noise_amount=1):
#             return
#         if maybe_splash(chance=3):
#             return
#     elif player_state["position"] == "raft":
#         return
#     elif player_state["location"] == "pool_mid":
#         if not has_seen_intro("board_raft_pool_mid") and game_state["raft_status"] == "pool_mid":
#             if player_state["state"] not in ["swimming", "wading"]:
#                 print_wrapped("You step onto the raft again, each step causing more wood creaks, sending ripples "
#                               "across the pool...", newline_delay=2.5)
#                 if maybe_make_noise(True,
#                     chance=3, noise_amount=1):
#                     return
#                 if maybe_splash(chance=3):
#                     return
#             elif player_state["state"] in ["swimming", "wading"]:
#                 print_wrapped("You climb onto the raft, sending splashes across the pool, and sounds of creaking wood "
#                               "out into the chamber...", newline_delay=2.5)
#                 if maybe_make_noise(True,
#                     chance=3, noise_amount=1):
#                     return
#                 if maybe_splash(chance=3):
#                     return
#             remember_intro("board_raft_pool_mid")
#         elif player_state["position"] == "raft":
#             return
#     else:
#         print_wrapped("You board the old raft again, your feet inches above the surface of the water.", newline_delay=1.5)

def board_raft_entries():
    # Decide the correct text based on state, but DO NOT call maybe_* here.
    if not has_seen_intro("board_raft"):
        return ["You step onto the raft, your feet inches above the surface of the water.", 1.5,
                "Its logs creak under each step and send small splashes across the pool...", 1.5,]
    if (player_state.get("location") == "pool_mid"
        and game_state.get("raft_status") == "pool_mid"
        and not has_memory(MEM_BOARD_RAFT_POOL_MID)):
        remember(MEM_BOARD_RAFT_POOL_MID)
        if player_state.get("state") in ("swimming", "wading"):
            return ["You climb onto the raft, sending splashes across the pool, and creaking echoes out into the chamber...", 2.5]
        else:
            return ["You step onto the raft again; the wood protests and ripples spread across the pool...", 2.5]
    if player_state.get("position") == "raft":
        return []
    return ["You board the old raft again, your feet inches above the surface of the water.", 1.5]

@scene_intro([
    board_raft_entries
])
def scene_board_raft(only_options=False, checkpoint_from=None):
    if not has_seen_intro("board_raft"):
        remember_intro("board_raft")
    if only_options:
        return _render_raft_options(checkpoint_from)
    # if arrival_interrupts_board_raft():
    #     return None
    if player_state.get("location") in ("sword_chamber", "pool_shallow") or player_state.get("position") == "dock":
        update_player_state(position="raft", location="pool_shallow", state=None)
    else:
        update_player_state(position="raft", location="pool_mid", state=None)
    apply_discovery_for_current_state()
    set_return_point(scene_board_raft, only_options=True, checkpoint_from=checkpoint_from)
    if maybe_make_noise(True, chance=3, noise_amount=1):
        return True
    if maybe_splash(chance=3):
        return True
    _render_raft_options(checkpoint_from)
    return None

def _render_raft_options(checkpoint_from):
    options = []
    if player_state.get("location") == "pool_shallow":
        options += [
            {"description": "Step onto the dock.", "handler": scene_dock},
            {"description": "Wade into the pool.", "handler": scene_wade_in_pool},
            {"description": "Push off towards the boulder.", "handler": scene_push_raft},
        ]
    elif player_state.get("location") == "pool_mid":
        options += [
            {"description": "Push off towards the dock.", "handler": scene_push_raft},
            {"description": "Step onto the submerged pillar.", "handler": scene_submerged_pillar},
            {"description": "Go into the pool.", "handler": scene_swim_in_pool_mid},
        ]
    if game_state.get("oar_status") != "underwater":
        options.append({"description": "Row the raft with the oar.", "handler": scene_row_with_oar})
    if not has_item("rope") and game_state.get("rope_on_raft", True):
        options.append({"description": "Take the rope.", "handler": scene_take_rope})
    if not has_item("oar") and game_state.get("oar_on_raft", True):
        options.append({"description": "Take the oar.", "handler": scene_take_oar})
    checkpoint_target = checkpoint_from or scene_board_raft
    return run_scene_with_options(options, 6, checkpoint=checkpoint_target)

# -------------------- Raft actions --------------------

def scene_take_rope():
    """
    Rope is only pickable from the raft or raft-wreck.
    """
    add_to_inventory("rope")
    game_state["rope_on_raft"] = False
    print_wrapped("You coil the rope and secure it to your belt.", newline_delay=0.8)
    return scene_board_raft(only_options=True)

def scene_take_oar():
    """
    Oar starts on the raft; if the raft wrecks and you didn't take it, it falls underwater.
    Keeping oar in inventory lets you row as long as game_state['oar_status'] != 'underwater'.
    """
    add_to_inventory("oar")
    game_state["oar_on_raft"] = False
    # Keep oar_status out of 'underwater' so rowing stays allowed.
    if game_state.get("oar_status") == "underwater":
        game_state["oar_status"] = "available"
    print_wrapped("You take the oar.", newline_delay=0.6)
    return scene_board_raft(only_options=True)

def scene_row_with_oar():
    """
    Controlled movement dock <-> mid without breaking the raft.
    Keep player on the raft and toggle raft_status.
    """
    loc = player_state.get("location")
    if loc == "pool_shallow":
        print_wrapped("You use the oar to guide the raft away from the dock and toward the deeper water.", newline_delay=1.2)
        update_player_state(location="pool_mid", position="raft", state=None)
        apply_discovery_for_current_state()
        set_return_point(scene_board_raft, only_options=True)
        if maybe_make_noise(True, chance=4, noise_amount=1): return True
        if maybe_splash(chance=4): return True
    elif loc == "pool_mid":
        print_wrapped("You pull the raft back toward the dock with steady strokes.", newline_delay=1.2)
        update_player_state(location="pool_shallow", position="raft", state=None)
        apply_discovery_for_current_state()
        set_return_point(scene_board_raft, only_options=True)
        if maybe_make_noise(True, chance=4, noise_amount=1): return True
        if maybe_splash(chance=4): return True
    return scene_board_raft(only_options=True)

def scene_push_raft():
    """
    Kick off WITHOUT the oar — always breaks the raft.
    - From shallow (pool_shallow) pushing 'towards the boulder':
        crash into the submerged pillar in mid; raft breaks (remains climbable for rope).
        Land at SP (position='submerged_pillar'), off the raft.
    - From mid pushing 'towards the dock':
        crash near the dock; raft breaks; land in the shallows wading.
    Order: update world + player state first, THEN hazards (noise -> splash).
    If a hazard scene runs, bail out early.
    """
    loc = player_state.get("location")
    next_scene = None
    if loc == "pool_shallow":
        print_wrapped("You kick hard — the raft lurches forward.", newline_delay=0.8)
        print_wrapped("The lashings snap as it slams the submerged pillar; the logs split and twist underfoot.", newline_delay=1.1)
        # Break raft; keep wreck climbable; rope stays unless taken
        break_raft("pool_mid")
        # If oar wasn't taken, it sinks with the wreck
        if game_state.get("oar_on_raft", False) and not has_item("oar"):
            game_state["oar_status"] = "underwater"
            game_state["oar_on_raft"] = False
        # Land at SP off the raft
        update_player_state(location="pool_mid", position="submerged_pillar", state=None)
        print_wrapped("You steady yourself on the flat top of the submerged pillar.", newline_delay=0.8)
        set_return_point(scene_submerged_pillar, only_options=True)
        next_scene = scene_submerged_pillar  # show SP options next
    elif loc == "pool_mid":
        print_wrapped("You shove off — the raft scrapes and skids across the water toward the dock.", newline_delay=0.8)
        print_wrapped("The binding gives way; logs split as you near the shallow edge.", newline_delay=1.0)
        break_raft("pool_shallow")
        if game_state.get("oar_on_raft", False) and not has_item("oar"):
            game_state["oar_status"] = "underwater"
            game_state["oar_on_raft"] = False
        # Land near the dock/shallow, off the raft
        update_player_state(location="pool_shallow", position=None, state="wading")
        print_wrapped("You stumble into the shallows near the dock.", newline_delay=0.8)
        set_return_point(scene_wade_in_pool, only_options=True)
        next_scene = scene_wade_in_pool  # or your local shallow scene
    else:
        # Fallback: treat unknown zone like mid → dock
        break_raft("pool_shallow")
        update_player_state(location="pool_shallow", position=None, state="wading")
        set_return_point(scene_wade_in_pool, only_options=True)
        next_scene = scene_wade_in_pool
    # --- Common hazards AFTER state is updated (so attacks have correct context) ---
    if maybe_make_noise(True, chance=2, noise_amount=1):
        return None  # an interrupt scene ran
    if maybe_splash(chance=2):
        return None  # an interrupt scene ran (snake/serpent)
    # If no interrupts, proceed to the appropriate next scene
    return next_scene() if next_scene else None

# -------------------- Pool (Shallow) --------------------

def pool_shallow_lit():  # <-- additive helper, no @scene_intro
    """
    Shallow-area reveals when torch is lit.
    Idempotent: safe to call multiple times; uses memory keys to avoid repeats.
    """
    if player_state.get("location") != "pool_shallow":
        return
    # Upgrade the silhouette + show dock from here if not yet seen
    if not has_memory(MEM_RUINS_SILH):
        print_wrapped("By the shallow water, you make out ruined pillars standing before a larger shape in the haze.")
        remember(MEM_RUINS_SILH)
    if not has_memory(MEM_DOCK):
        print_wrapped("A weathered dock clings to the near shore.")
        remember(MEM_DOCK)
    # Reveal the raft at shallow, but only if it's actually here
    if game_state.get("raft_status") == "pool_shallow" and not has_memory(MEM_RAFT_SEEN):
        print_wrapped("A bound-log raft bobs gently beside the dock.")
        remember(MEM_RAFT_SEEN)

@scene_intro([
"You see the outline of a structure just beyond the ruins..."
], return_entries=[
    _pool_shallow_return_entries
], preludes=[
    _prelude_splash_in_tunnel,
    _prelude_spot_on_arrival_to_shallow
])
def scene_pool_shallow(only_options=False):
    pos = player_state.get("position")
    if pos == "raft":
        if not only_options:
            scene_board_raft(checkpoint_from=scene_pool_shallow)
        else:
            scene_board_raft(only_options=True, checkpoint_from=scene_pool_shallow)
        return
    if pos == "dock":
        if not only_options:
            scene_board_raft(checkpoint_from=scene_dock)
        else:
            scene_board_raft(only_options=True, checkpoint_from=scene_dock)
        return
    if not only_options:
        scene_wade_in_pool()
    else:
        scene_wade_in_pool(only_options=True)

def wade_in_pool_intro():
    if player_state.get("location") == "pool_shallow":
        if not has_seen_intro("wade_into_pool_from_tunnel"):
            print_wrapped("You walk into the cold water. Ripples spread outward as you disrupt the surface...", newline_delay=1.5)
            remember_intro("wade_into_pool_from_tunnel")
    elif player_state.get("state") == "swimming":
        print_wrapped("Your feet find the pool floor as you move through the water, away from the middle.", newline_delay=1.5)
    else:
        print_wrapped("You wade into the water again...", newline_delay=1.5)

def wade_in_pool_entries():
    if player_state.get("location") == "sword_chamber" and player_state.get("position") != "dock":
        return ["You walk into the cold water. Ripples spread outward as you disrupt the surface...", 1.5]
    elif player_state.get("position") == "dock":
        return ["You hop into the pool from the dock, sending waves across the water's surface...", 1.5]
    elif player_state.get("location") == "pool_mid":
        return ["Your feet find the pool floor as you move through the water, towards the chamber entrance."]
    return ["You wade through the pool."]

@scene_intro([wade_in_pool_entries], return_entries=["You wade through the pool again..."])
def scene_wade_in_pool(only_options=False):
    if not only_options:
        update_player_state(location="pool_shallow", state="wading", position=None)
        apply_discovery_for_current_state()
        set_return_point(scene_wade_in_pool, only_options=True)
        if player_state.get("torch_lit"):
            pool_shallow_lit()
        if maybe_splash():
                return
    options = [
        {"description": "Go deeper into the pool.", "handler": scene_pool_mid},
        {"description": "Return to the chamber entrance.", "handler": scene_sword_chamber},
    ]
    if has_memory("raft_seen") and raft_is_available_at("pool_shallow"):
        options.append({"description": "Climb up onto the raft.", "handler": scene_board_raft})
    run_scene_with_options(options, 4, checkpoint=scene_wade_in_pool)

# -------------------- Pool (Mid) --------------------

def reveal_boulder_from_mid_if_needed():
    """
    Fires the one-time 'boulder + sword' reveal when the player first truly reaches pool_mid
    (from swimming, from SP, or on the raft at mid). Safe to call multiple times.
    """
    if not has_memory(MEM_BOULDER_SWORD):
        print_wrapped("Beyond the half-submerged pillars, a massive boulder rises. A sword glints from its heart...", newline_delay=1.5)
        print_wrapped("A mystic energy gravitates around the hilt of the sword...")
        remember(MEM_BOULDER_SWORD)

def scene_pool_mid(only_options=False):
    if player_state.get("state") == "swimming":
        if not only_options:
            scene_swim_in_pool_mid()
        else:
            scene_swim_in_pool_mid(only_options=True)
    elif player_state.get("position") == "submerged_pillar":
        if not only_options:
            apply_discovery_for_current_state()
            scene_submerged_pillar(only_options=True)
        else:
            scene_submerged_pillar(only_options=True)
    elif player_state.get("position") == "raft":
        if not only_options:
            if game_state.get("raft_status") == "pool_mid":
                apply_discovery_for_current_state()
            if player_state.get("previous_location") == "pool_shallow":
                scene_board_raft(checkpoint_from=scene_board_raft)
            elif player_state.get("previous_state") == "swimming":
                scene_board_raft(checkpoint_from=scene_swim_in_pool_mid)
            elif player_state.get("previous_position") == "submerged_pillar":
                scene_board_raft(checkpoint_from=scene_submerged_pillar)
        else:
            if player_state.get("previous_location") == "pool_shallow":
                scene_board_raft(only_options=True, checkpoint_from=scene_board_raft)
            elif player_state.get("previous_state") == "swimming":
                scene_board_raft(only_options=True, checkpoint_from=scene_swim_in_pool_mid)
            elif player_state.get("previous_position") == "submerged_pillar":
                scene_board_raft(only_options=True, checkpoint_from=scene_submerged_pillar)

def scene_swim_in_pool_mid(only_options=False):
    if not only_options:
        if not has_memory("swim_into_pool_mid"):
            print_wrapped("The water swirls around you; you don't feel the earth beneath the pool as you tread water.")
            remember_intro("swim_into_pool_mid")
        else:
            print_wrapped("You swim into the middle of the pool again.", newline_delay=1.5)
        update_player_state(location="pool_mid", state="swimming", torch_lit=False)
        apply_discovery_for_current_state()
        set_return_point(scene_swim_in_pool_mid, only_options=True)
        if maybe_splash():
            return
    options = [
        {"description": "Swim over to the boulder.", "handler": scene_swim_to_boulder},
        {"description": "Hoist yourself up onto the submerged pillar.", "handler": scene_submerged_pillar},
        {"description": "Head towards the chamber entrance.", "handler": scene_wade_in_pool},
    ]
    if has_memory("raft_seen") and raft_is_available_at("pool_mid"):
        options.append({"description": "Climb onto the raft.", "handler": scene_board_raft})
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 2)

def submerged_pillar():
    if not has_seen_intro("submerged_pillar"):
        if player_state["position"] == "raft":
            print_wrapped("You step onto the submerged pillar, sending splashes across the pool surface. The sudden "
                          "shift in weight breaks the raft's old ropes, leaving its wooden logs to drift apart...")
            break_raft("pool_mid")
        elif player_state.get("state") == "swimming":
            print_wrapped("You climb onto the submerged pillar, feeling safer than a moment ago, sending a splash across "
                          "the pool...")
        print_wrapped("Between you and the chamber entrance lies the misty pool...and between you and the mystic sword, "
                      "wedged into the boulder, stands half-submerged pillars, each standing a bit farther apart than "
                      "the last...")
        remember(MEM_BOULDER_SWORD)
        remember_intro("submerged_pillar")

@scene_intro([], return_entries=[
    "You climb up the submerged pillar again, your ankles still in the water."
], preludes=[
    _prelude_splash_on_arrival_to_pillar
])
def scene_submerged_pillar(only_options=False):
    if not only_options:
        submerged_pillar()
        update_player_state(location="pool_mid", position="submerged_pillar")
        apply_discovery_for_current_state()
        set_return_point(scene_submerged_pillar, only_options=True)
        if maybe_splash():
            return
        print_wrapped("As you stand on the submerged pillar, you examine your options...", newline_delay=1.5)
    options = [
        {"description": "Jump to the closest half-submerged pillar.", "handler": scene_first_pillar},
        {"description": "Get into the pool.", "handler": scene_swim_in_pool_mid},
    ]
    if game_state["raft_status"] == "pool_mid":
        options.append({"description": "Climb onto the raft.", "handler": scene_board_raft})
    run_scene_with_options(options, 5, checkpoint=scene_submerged_pillar)

def submerged_pillar_lit():
    if player_state.get("torch_lit") and player_state.get("position") == "submerged_pillar":
        print_wrapped("With the light, you judge the distance to the next pillar better...", newline_delay=1.5)

# -------------------- Pool (Deep) --------------------

MEM_MEMO_SP_P1    = "memorized:sp_to_p1"
MEM_MEMO_P1_P2    = "memorized:p1_to_p2"
MEM_MEMO_P2_LEDGE = "memorized:p2_to_ledge"

def _reveal_boulder_from_deep_if_needed():
    """Safety reveal from deep (in case player saw deep first)."""
    if not has_memory(MEM_BOULDER_SWORD):
        print_wrapped("Up close, the boulder looms out of the dark water. A sword glints from its heart...", newline_delay=1.2)
        print_wrapped("A mystic energy gravitates around the hilt of the sword...")
        remember(MEM_BOULDER_SWORD)

# -------- Pillar jump helpers (deterministic pity + rope catch) --------

def _start_pillar_attempt_if_from_sp():
    """
    Starting a full attempt from the submerged pillar resets/advances the deterministic slip schedule.
    """
    if player_state.get("position") == "submerged_pillar":
        # New 'attempt' begins at SP
        game_state["pillar_attempt_epoch"] = game_state.get("pillar_attempt_epoch", 0) + 1
        game_state["pillar_attempt_slips_used"] = 0

def _should_slip_on_jump(jump_index: int) -> bool:
    """
    Deterministic pity:
      - First slip of this attempt may occur only on jump 2 (P1 <-SP-> P1 -> P2).
      - Second slip of this attempt may occur only on jump 1 (SP->P1).
      - Never more than 2 slips per attempt.
    'jump_index' is 1 for SP->P1, 2 for P1->P2, 3 for P2->ledge.
    """
    slips_used = game_state.get("pillar_attempt_slips_used", 0)
    if slips_used >= 2:
        return False
    if slips_used == 0 and jump_index == 2:
        return True
    if slips_used == 1 and jump_index == 1:
        return True
    return False

def _apply_slip_fall_to_deep(nudge_after=False):
    """Common slip handling: fall into deep, splash, optional nudge line."""
    update_player_state(location="pool_deep", state="swimming", position=None, torch_lit=False)
    if nudge_after:
        print_wrapped("You slide back into the deep water...", newline_delay=0.8)
    # Splash may trigger a snake scene; if so, bail out.
    if maybe_splash(chance=2):
        return True
    return False

def _nudge_memorize_if_lit(jump_mem_key: str):
    """
    On a lit pillar, teach the distance and nudge to snuff before jumping.
    - First time: one combined line, then remember the distance.
    - Later times (still lit): short reminder.
    - In the dark: a different short reminder that judging distance is hard.
    """
    if player_state.get("torch_lit"):
        if not has_memory(jump_mem_key):
            print_wrapped(
                "With the torch lit, you can tell exactly how far the next pillar is. "
                "Maybe jump after putting out the torch...",
                newline_delay=0.7
            )
            remember(jump_mem_key)
        else:
            print_wrapped("You can see the distance clearly; snuff the torch before the jump...", newline_delay=0.5)
    else:
        if not has_memory(jump_mem_key):
            print_wrapped("In the dark, it’s hard to judge the distance to the next pillar...", newline_delay=0.7)

def _rope_catch_if_tied(near_p2: bool) -> bool:
    """
    If rope is tied at P2 and we slip near/toward P2, convert the fall into a 'catch the rope' beat.
    Returns True if we handled with a rope catch (and did NOT fall to water).
    """
    if near_p2 and game_state.get("rope_tied", False):
        print_wrapped("Your hands snag the rope — you hang for a breath, then pull yourself up.", newline_delay=1.0)
        # Land on P2 safely.
        update_player_state(location="pool_deep", position="pillar_p2", state=None)
        return True
    return False

# -------- Entry from mid to deep by swimming --------

def scene_swim_to_boulder():
    print_wrapped("You abandon the submerged pillar and swim toward the boulder that holds the mystic sword.", newline_delay=1.2)
    if maybe_splash(chance=1):  # deep swim is splashy; use stricter chance
        return
    update_player_state(location="pool_deep", state="swimming", torch_lit=False)
    apply_discovery_for_current_state()
    options = [
        {"description": "Try to climb the boulder.", "handler": scene_try_climb_boulder_from_water},
        {"description": "Swim back toward the middle.", "handler": scene_swim_in_pool_mid},
        # {"description": "Dive underwater.", "handler": scene_dive_underwater},
    ]
    # From water in deep, you can attempt the taller pillar ONLY if rope tied at P2.
    if game_state.get("rope_tied", False):
        options.insert(1, {"description": "Grab the rope and climb the taller pillar.", "handler": scene_climb_rope_to_p2})
    run_scene_with_options(options, 4, checkpoint=scene_swim_to_boulder)

def scene_try_climb_boulder_from_water():
    # Forced fail with a soft nudge (ellipsis ending per your preference)
    print_wrapped("You reach for holds on the wet stone...they slip away.")
    print_wrapped("Maybe you can't climb from here...")
    # Always slip back into deep; stay here, not mid.
    if _apply_slip_fall_to_deep(nudge_after=False):
        return
    # Subtle teaching line
    print_wrapped("Maybe the pillars are the way...", newline_delay=0.8)
    return scene_swim_to_boulder()  # re-render options in deep

def scene_climb_rope_to_p2():
    """
    From the water in deep, if rope is tied at P2, allow climbing back onto P2.
    """
    if not game_state.get("rope_tied", False):
        print_wrapped("You reach up for the pillar, but it’s too tall from the water...")
        if _apply_slip_fall_to_deep():
            return
        return scene_swim_to_boulder()
    print_wrapped("You find the rope and hand-over-hand climb to the pillar.", newline_delay=1.0)
    update_player_state(location="pool_deep", position="pillar_p2", state=None)
    return scene_pillar_two()  # show P2 options

# -------- PILLARS: SP -> P1 -> P2 -> Ledge --------

def scene_first_pillar():
    """
    Jump from the submerged pillar (mid) to the first taller pillar (deep).
    Deterministic pity applies; no rope catch here (rope is at P2).
    """
    # Starting a full attempt from SP resets the schedule
    _start_pillar_attempt_if_from_sp()
    # Nudge/memorize on SP if torch is lit
    _nudge_memorize_if_lit(MEM_MEMO_SP_P1)
    # Decide slip
    slip = _should_slip_on_jump(jump_index=1)
    if slip:
        game_state["pillar_attempt_slips_used"] = game_state.get("pillar_attempt_slips_used", 0) + 1
        print_wrapped("You leap — your foot skids on wet stone.", newline_delay=0.8)
        if _apply_slip_fall_to_deep(nudge_after=True):
            return
        return scene_swim_to_boulder()
    # Success: land on P1
    print_wrapped("You leap and catch the edge, hauling yourself onto the pillar.")
    update_player_state(location="pool_deep", position="pillar_p1", state=None)
    return scene_pillar_one()

def scene_pillar_one(only_options: bool = False):
    """
    Standing on P1 in deep.
    """
    if not only_options:
        _reveal_boulder_from_deep_if_needed()
        print_wrapped("Balanced on the first pillar, you gauge the next jump...")
    options = [
        {"description": "Jump to the next pillar.", "handler": scene_second_pillar_jump},
        {"description": "Drop into the water.", "handler": scene_swim_to_boulder},
        {"description": "Jump back to the submerged pillar.", "handler": scene_submerged_pillar},
    ]
    # Torch/light 'study' happens wherever you toggle torch; we only nudge in jump handlers.
    return run_scene_with_options(options, 5, checkpoint=scene_pillar_one)

def scene_second_pillar_jump():
    """
    Jump from P1 to P2. Deterministic slip; rope catch transforms a fall near P2.
    """
    _nudge_memorize_if_lit(MEM_MEMO_P1_P2)
    slip = _should_slip_on_jump(jump_index=2)
    if slip:
        game_state["pillar_attempt_slips_used"] = game_state.get("pillar_attempt_slips_used", 0) + 1
        print_wrapped("You spring across — the landing slicks away under you!", newline_delay=0.8)
        # Rope catch if tied at/near P2
        if _rope_catch_if_tied(near_p2=True):
            return scene_pillar_two()
        # Otherwise, fall to deep
        if _apply_slip_fall_to_deep(nudge_after=True):
            return
        return scene_swim_to_boulder()
    # Success to P2
    print_wrapped("You hit the pillar and steady yourself.")
    update_player_state(location="pool_deep", position="pillar_p2", state=None)
    return scene_pillar_two()

def scene_pillar_two(only_options: bool = False):
    """
    Standing on P2 (near boulder). Can tie rope here. Next: jump to boulder ledge.
    """
    if not only_options:
        _reveal_boulder_from_deep_if_needed()
        print_wrapped("From here the boulder is close — one more jump.")
    options = [
        {"description": "Make the final jump to the boulder ledge.", "handler": scene_final_jump_to_ledge},
        {"description": "Drop into the water.", "handler": scene_swim_to_boulder},
        {"description": "Jump back to the previous pillar.", "handler": scene_pillar_one},
    ]
    # Tie rope option (only if you have it and it isn't tied yet)
    if not game_state.get("rope_tied", False) and has_item("rope"):
        options.insert(0, {"description": "Tie the rope here.", "handler": scene_tie_rope_at_p2})
    return run_scene_with_options(options, 5, checkpoint=scene_pillar_two)

def scene_tie_rope_at_p2():
    game_state["rope_tied"] = True
    print_wrapped("You fix the rope to the pillar, knotting it tight.")
    # Stay on P2 and re-render options
    return scene_pillar_two(only_options=True)

def scene_final_jump_to_ledge():
    """
    Final leap from P2 to the boulder ledge.
    Deterministic pity: no forced slips left if two already happened.
    If a slip occurs toward P2 and rope is tied, we convert to a rope catch to P2.
    On success, drop into your sword interaction.
    """
    _nudge_memorize_if_lit(MEM_MEMO_P2_LEDGE)
    # Treat final jump as jump_index=3 (no predetermined slip by schedule; but allow rope catch if we decide to slip anyway)
    slip = _should_slip_on_jump(jump_index=3)
    if slip:
        game_state["pillar_attempt_slips_used"] = game_state.get("pillar_attempt_slips_used", 0) + 1
        print_wrapped("Your toes scrape the edge — and you’re falling!", newline_delay=0.7)
        if _rope_catch_if_tied(near_p2=True):
            return scene_pillar_two()  # caught rope back to P2
        if _apply_slip_fall_to_deep(nudge_after=True):
            return
        return scene_swim_to_boulder()
    # Success: reach boulder ledge (you can later split this to a separate scene)
    print_wrapped("Stone bites your palms; you kick and roll up onto the ledge.", newline_delay=0.9)
    # This is the point where your game transitions to the sword interaction scene.
    # If you later add a dedicated 'boulder_ledge' scene, jump there instead.
    return scene_boulder_ledge()

def scene_dive_underwater():
    if player_state.get("torch_lit"):
        update_player_state(torch_lit=False)
    player_state["previous_location"] = player_state.get("location")
    print_wrapped("You take a deep breath and plunge beneath the surface. The world goes silent except for your "
                  "pounding heartbeat.")
    if has_memory("creature_seen"):
        print_wrapped("You hear the faint whoosh above — the bat-creature must have missed you... for now.")
    else:
        print_wrapped("You hear a rush of wind above the water... then nothing. Whatever was coming for you seems "
                      "to have vanished — for now.")
    print_wrapped("You resurface slowly, gasping for air. The cave is silent once again.")
    if maybe_splash():
        return
    return_to_scene_before_attack()

# -------------------- Mystic Sword --------------------

def scene_boulder_ledge():
    ...



# -------------------- Bone Ladder Preludes --------------------

def _prelude_slip_from_ladder():
    """
    Slip check when climbing or jumping to the bone ladder.
    """
    if player_state.get("location") == "rock_pile" and player_state.get("position") == "ladder":
        return slip_calculation(action="jump")
    return False

# -------------------- Bone Ladder --------------------

def scene_jump_to_ladder():
    update_player_state(location="bone_ladder")

def scene_return_to_rocks():
    if player_state["location"] == "sword_chamber":
        print_wrapped("You return through the tunnel to the rocks...")
        if maybe_displace_rocks():
            return
    if player_state["location"] == "bone_ladder":
        print_wrapped("You swing from the bone ladder towards the rocks...")
        if slip_calculation(action="swing"):
            return
        print_wrapped("You land on the rocks, knocking a few down the large pile...")
        if maybe_displace_rocks():
            return
    update_player_state(location="rock_pile")
    scene_rock_pile(only_options=True)

# -------------------- Bat Creature Attack --------------------

def scene_too_much_noise():
    if not has_memory("attacked_by_creature"):
        remember("attacked_by_creature")
    if player_state.get("state") == "swimming":
        print_wrapped("A piercing screech echoes through the cavern, reverberating across the water’s surface...", newline_delay=1.5)
        options = [
            {"description": "Dive underwater.", "handler": scene_dive_underwater}
        ]
        ui_state["current_options"] = options
        check_and_run_random_handler(ui_state["current_options"],
            checkpoint=None if TORTURE_MODE else return_to_scene_before_attack)
        return
    print_wrapped("You hear a screech from inside the cave...", newline_delay=1.5)
    location = player_state.get("location")
    if location == "rock_pile":
        print_wrapped("From atop the rocks, you feel the air shift above you...", newline_delay=1.5)
    if location == "forgotten_cavern":
        print_wrapped("From the center of the cavern, you freeze as the sound echoes from above...", newline_delay=1.5)
    if location in single_entrance_locations:
        print_wrapped("Through the shadows, you hear movement from where you entered...", newline_delay=1.5)

    if player_state["torch_lit"]:
        if has_memory("creature_seen"):
            print_wrapped("You see the bat-creature take flight and fly directly towards you, fangs ready...", newline_delay=1.5)
        if not has_memory("creature_seen"):
            print_wrapped("A monstrous winged shape hurtles toward you, bearing its fangs...", newline_delay=1.5)
            remember("creature_seen")
        options = [
            {"description": "Strike at the creature as it reaches you.", "handler": scene_strike_bat_creature},
            {"description": "Extinguish your torch and duck.", "handler": scene_extinguish_torch_duck},
        ]
        if has_item("elegant_shield"):
            options.append({"description": "Wield the shield.", "handler": scene_wield_shield})
        ui_state["current_options"] = options
        check_and_run_random_handler(
            ui_state["current_options"], 3,
            checkpoint=None if TORTURE_MODE else return_to_scene_before_attack)

    if not player_state["torch_lit"]:
        if location not in single_entrance_locations:
            if has_memory("creature_seen"):
                game_over("In total darkness, you hear wings close in. You know what's coming for you...", "bat-creature")
            else:
                game_over("Within seconds, you hear wings and feel hot breath. In the dark, something reaches you...", "bat-creature")
        else:
            options = [
                {"description": "Test your instincts and swing your sword in the darkness.", "handler": scene_strike_bat_creature},
            ]
            if has_item("elegant_shield"):
                options.append({"description": "Wield the shield.", "handler": scene_wield_shield})
            ui_state["current_options"] = options
            check_and_run_random_handler(
                ui_state["current_options"], 2 if len(options) == 2 else 3,
                checkpoint=None if TORTURE_MODE else return_to_scene_before_attack)

def scene_strike_bat_creature():
    location = player_state.get("location")
    single_entrance = location in single_entrance_locations
    survival_chance = random.randint(0, 2)
    if player_state.get("torch_lit"):
        print_wrapped("You swing your sword...", newline_delay=1)
        print_wrapped("...and decapitate the creature. You survived.", newline_delay=1.5)
        print_wrapped("You count your blessings, and continue your journey.", newline_delay=1.5)
        game_state["cave_creature_killed"] = True
        return return_to_scene_before_attack()
    elif single_entrance and survival_chance in range(1, 3):
        print_wrapped("You trust your instincts in the dark, swinging your sword... ", newline_delay=1.5)
        print_wrapped("...and, with luck, you decapitate the creature mid-flight.", newline_delay=1.5)
        game_state["cave_creature_killed"] = True
        return return_to_scene_before_attack()
    else:
        game_over("You swing your sword and miss, unable to see. The creature closes in...", "bat-creature")
        return

def scene_extinguish_torch_duck():
    game_over("The creature can see better than you in this darkness. It finds you...", "bat-creature")

def scene_wield_shield():
    print_wrapped("You hold the shield in front of you...", newline_delay=1.5)
    if player_state["torch_lit"] and has_memory("creature_seen"):
        print_wrapped("The bat-creature screeches and dives. You brace yourself...and the shield deflects the "
                      "creature's strike with a blinding flash.")
        print_wrapped("When your vision clears, the creature is nowhere to be seen.")
    elif player_state["torch_lit"] and not has_memory("creature_seen"):
        print_wrapped("A monstrous bat-creature hurtles toward you...just in time, the shield pulses and repels "
                      "it with a shock of light.")
        print_wrapped("You see a glimpse of wings and fangs before the thing vanishes into the dark.")
        remember("creature_seen")
    elif not player_state["torch_lit"] and has_memory("creature_seen"):
        print_wrapped("In the dark, you sense the creature's presence closing in...the shield vibrates with "
                      "energy and deflects a savage blow.")
        print_wrapped("You hear its flapping wings and screeches fade away...")
    elif not player_state["torch_lit"] and not has_memory("creature_seen"):
        print_wrapped("You wait in pitch blackness, shield raised, heartbeat pounding...", newline_delay=1.5)
        print_wrapped("Suddenly, something crashes against the shield and recoils with a furious screech.", newline_delay=1.5)
        print_wrapped("You hear its flapping wings fade away...", newline_delay=1.5)
    game_state["cave_noise"] = max(0, game_state["cave_noise"] - 2)
    return return_to_scene_before_attack()

# -------------------- Serpent Attack --------------------

def handle_snake_outcome(size, action):
    """Decide success/failure based on size and action. For tiny snake, success chance is high if dodge or block,
    strike only works if mystic sword in hand."""
    if size == "tiny":
        if action == "dodge":
            print_wrapped("You strafe just in time — the snake’s fangs snap shut on empty air.")
        elif action == "block":
            print_wrapped("You slam your shield down as the snake lunges; it recoils and retreats with a hiss.")
        elif action == "strike":
            if has_item("mystic_sword"):
                print_wrapped("Your mystic sword glows as you slash — and the snake falls limp.")
            else:
                print_wrapped("You swing wildly with your blunt blade — and miss. The snake sinks its fangs into you.")
                game_over("You kick the snake off, but its poison courses through your veins...", "snake_poison")
                return
    if size == "medium":
        if action == "dodge":
            if random.random() < 0.6:
                print_wrapped("You roll aside just as the snake’s fangs cut through the water.")
            else:
                print_wrapped("You misjudge its speed — and its fangs scrape your leg.")
                game_over("Venom surges through your body...", "snake_poison")
                return
        elif action == "block":
            if has_item("elegant_shield"):
                print_wrapped("You brace your shield; the serpent strikes and ricochets off, hissing in pain.")
            else:
                print_wrapped("You have no shield—there’s nothing to stop its strike.")
                game_over("The medium serpent’s fangs sink deep...", "snake_medium")
                return
        elif action == "strike":
            if has_item("mystic_sword"):
                print_wrapped("Your mystic sword hums. You slash through the serpent’s neck—its body goes limp.")
            else:
                print_wrapped("Your blade scrapes its scaled hide; it lunges past and bites you.")
                game_over("Venom takes hold...", "snake_medium")
                return
    if size == "large":
        if action == "retreat":
            # 50% chance to slip in water, 50% to get away
            if random.random() < 0.5:
                print_wrapped("You stumble — its fangs flash as they scrape your thigh.")
                game_over("Venom courses through your veins...", "snake_poison")
                return
            else:
                print_wrapped("You scramble out of the way just as it lunges past you.")
        elif action == "block":
            if has_item("elegant_shield"):
                print_wrapped("You brace your shield; the large serpent smashes into it and recoils, savage and wounded.")
            else:
                print_wrapped("Without a shield, there’s nothing to stop its crushing strike.")
                game_over("The large serpent’s fangs crush you...", "large_serpent")
                return
        elif action == "strike":
            if has_item("mystic_sword"):
                print_wrapped("You drive the mystic sword through its neck—its body thrashes before collapsing.")
            else:
                print_wrapped("Your blade glances off its thick scales; it lunges past and bites down.")
                game_over("The large serpent seeps its venomous fangs into you...", "snake_medium")
                return
    if size == "giant":
        if action == "strike":
            if has_item("mystic_sword"):
                print_wrapped(
                    "Your mystic sword pulses with energy. You plunge it into the serpent’s eye — its roar shakes the cavern as it collapses.")
                game_state["serpent_killed"] = True
            else:
                print_wrapped("Your weapon shatters on its scaly skull; you are swallowed by its jaws.")
                game_over("The giant serpent finishes you in one crushing bite.", "giant_serpent")
                return
        elif action == "retreat":
            print_wrapped("You turn to run, but its coils whip around you instantly. You feel crushing pressure.")
            game_over("The giant serpent squeezes you with lethal force...", "serpent_grip")
            return
        elif action == "block":
            if has_item("elegant_shield"):
                print_wrapped(
                    "The giant serpent’s fangs slam into your shield, cracking it to splinters. You are thrown into the water.")
                game_over("Dazed, you sink beneath its thrashing coils...", "serpent_swimming")
                return
            else:
                print_wrapped("With no shield, there’s nothing to stop its crushing blow.")
                game_over("You are crushed instantly.", "giant_serpent")
                return
    return return_to_scene_before_attack()
    # (You can return to the correct scene via return_to_scene_before_attack())

def scene_tiny_snake_attack():
    """A small snake lunges from the shallows. The player can dodge or try a quick strike."""
    remember("serpent_seen")  # mark that the player has now seen snakes
    lit = player_state.get("torch_lit", False)
    print_wrapped(
        "A tiny snake darts out of the water — its fangs glint as it strikes at your ankle!"
        if lit else
        "A tiny snake darts from the water — teeth flash toward your ankle in the dark!"
    )
    options = [
        {"description": "Quickly dodge backward.", "handler": lambda: handle_snake_outcome(size="tiny", action="dodge")},
        {"description": "Strike at it with your blade.", "handler": lambda: handle_snake_outcome(size="tiny", action="strike")}
    ]
    if has_item("elegant_shield"):
        options.append({"description": "Raise your shield to block.", "handler": lambda: handle_snake_outcome(size="tiny", action="block")})
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3,
        checkpoint=None if TORTURE_MODE else return_to_scene_before_attack)

def scene_medium_snake_attack():
    """A slightly larger snake, faster and more aggressive. Lower dodge chance."""
    remember("serpent_seen")
    lit = player_state.get("torch_lit", False)
    print_wrapped(
        "The mid‐sized serpent bursts from the shallows, its tongue flickering in the torchlight!"
        if lit else
        "A mid‐sized serpent bursts from the shallows — water explodes around your legs in the dark!"
    )
    options = [
        {"description": "Dodge sideways along the shoreline.", "handler": lambda: handle_snake_outcome(size="medium", action="dodge")},
        {"description": "Swing at its head with your blade.", "handler": lambda: handle_snake_outcome(size="medium", action="strike")}
    ]
    if has_item("elegant_shield"):
        options.append({"description": "Brace your shield and wait for it to strike.", "handler": lambda: handle_snake_outcome(size="medium", action="block")})
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3,
        checkpoint=None if TORTURE_MODE else return_to_scene_before_attack)

def scene_large_snake_attack():
    """A big serpent coils at the water’s edge, ready to strike. Harder to dodge."""
    remember("serpent_seen")
    lit = player_state.get("torch_lit", False)
    print_wrapped(
        "The large serpent rears up from the pool — its hood flared, eyes gleaming with malice!"
        if lit else
        "A large serpent rears up from the pool — its hood flared, eyes gleaming with malice!"
    )
    options = [
        {"description": "Back away quickly—try to find higher ground.", "handler": lambda: handle_snake_outcome(size="large", action="retreat")},
        {"description": "Strike with your blade before it lunges.", "handler": lambda: handle_snake_outcome(size="large", action="strike")}
    ]
    if has_item("elegant_shield"):
        options.append({"description": "Plant your shield and hold your ground.", "handler": lambda: handle_snake_outcome(size="large", action="block")})
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3,
        checkpoint=None if TORTURE_MODE else return_to_scene_before_attack)

def scene_serpent_attack():
    """Final showdown: the giant serpent itself. If you lack the mystic sword, it’s instant death."""
    remember("serpent_seen")
    print_wrapped("From the deepest part of the pool, a colossal serpent rises — its maw wide, eyes burning with hunger!")
    options = []
    if has_item("mystic_sword"):
        options.append({"description": "Strike with the mystic sword before it attacks.", "handler": lambda: handle_snake_outcome(size="giant", action="strike")})
    options.append({"description": "Try to sprint back toward the tunnel entrance.", "handler": lambda: handle_snake_outcome(size="giant", action="retreat")})
    if has_item("elegant_shield"):
        options.append({"description": "Brace your shield for its strike.", "handler": lambda: handle_snake_outcome(size="giant", action="block")})
    ui_state["current_options"] = options
    check_and_run_random_handler(ui_state["current_options"], 3,
        checkpoint=None if TORTURE_MODE else return_to_scene_before_attack)

first_time_lit_scenes = {
        "forgotten_cavern": {
            "flag": "cavern_floor_lit",
            "handler": forgotten_cavern_lit
        },
        "dripping_cave": {
            "flag": "dripping_cavern_lit",
            "handler": dripping_cavern_lit
        },
        "rock_pile": {
            "flag": "rocks_lit",
            "handler": rock_pile_lit
        },
        "glowing_hallway": {
            "flag": "glowing_hallway_lit",
            "handler": glowing_hallway_lit
        },
        "sword_chamber": {
            "flag": "sword_chamber_lit",
            # "sword_chamber_lit" became "old_raft_found"
            "handler": dock_lit
        }
    }

handler_lookup = {
    "forgotten_cavern": forgotten_cavern_lit,
    "dripping_cave": dripping_cavern_lit,
    "rock_pile": rock_pile_lit,
    "glowing_hallway": glowing_hallway_lit,
    "sword_chamber": dock_lit
}