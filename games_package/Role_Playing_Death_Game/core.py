from .state import reset_game_state, reset_player_state
from utils.input_handlers import ReturnToMenu
from utils import (
delayed_check_input as check_input,
delayed_input,
print_wrapped
)
import random
import os
import inspect




TORTURE_MODE = os.getenv("TORTURE_MODE", "false").lower() == "true"
# run TORTURE_MODE=true python3 Game_Selection.py for less second chances

game_state, player_state = reset_game_state(), reset_player_state()

current_options = []

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
    "mortal peril": ["Drink a healing potion.", "Pray for a miracle."],
    "shadow": ["Tell the shadow you'll leave and never come back.", "Strike the shadow.",
               "Don't move and hope the shadow leaves you be."],
    "cyclops": ["Hide from the cyclops.", "Strike at the cyclops.",
                "Offer the cyclops treasure."],
    "snake_poison": ["Chew on healing herbs.", "Drink a potion.", "Relax your muscles to slow the poison."],
    "snake_medium": ["Pull the snake off you.", "Strike the snake.", "Kick the snake off you."],
    "serpent_grip": ["Push back against the serpent's grip.", "Use your sword to cut the serpent."],
    "serpent_swimming": ["Get back to your senses.", "Wield your sword.", "Stay still."]
}

final_deaths = {
    "fall": ["Your fingers slip, and you plummet into darkness.", "Flapping does nothing. Gravity does.",
             "You forgot to grasp your end of the rope...",
             "There is no softer surface. Did you think this was a movie?"],
    "beast": ["The beast is unmoved. It strikes.", "You get a few hits in, but the beast is stronger.",
              "The beast is faster...did you think you could outrun it?",
              "The beast, insulted, rips you apart."],
    "drowning": ["You surface, gasping...only for the current to drag you under again.",
                 "No one hears your screams.", "There was nothing to grasp.",
                 "You never see the surface again."],
    "trapped": ["You claw away until exhaustion takes you.",
                "You sit quietly as darkness consumes you.",
                "The echoes of your efforts drive you mad."],
    "ghost": ["The being listens...then takes your soul anyway.",
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
    "mortal peril": ["You didn't pass potions class...", "No one answers your prayers."],
    "shadow": ["The shadow grabs you anyway, and you fade into darkness.",
               "The blow passes through the shadow, to no effect. It engulfs you in its darkness.",
               "The shadow doesn't forget where you are. The moment it touches you, you become a shadow."],
    "cyclops": ["The cyclops finds you and finishes you with one blow.",
                "The cyclops grabs you and crushes you in its hand.",
                "The cyclops roars and attacks. It looks like it doesn't know English..."],
    "snake_poison": ["As you frantically chew, you feel your body go numb, and you slip away...",
                     "You were swindled - your potion is only holy water. You feel yourself slip away.",
                     "The poison does its job anyway...you feel it numbing your body and you slip away."],
    "snake_medium": ["The snake's grip prevails...its poison overcomes you.",
                     "You get the snake off you, but it's too late — its poison overcomes you.",
                     "The snake's grip prevails...its poison overcomes you."],
    "serpent_grip": ["The serpent's grip tightens around you...and it strikes.",
                "Your sword bounces off the serpent's scales...it strikes."],
    "serpent_swimming": ["It's too late - the giant serpent strikes before you can react.",
                         "You wield your piece of metal...and the serpent swallows you. There's no escape.",
                         "The serpent knows where you are. It makes a meal out of you."]
}

SILENT_DEATHS = {
    "gem_trap",
    "glyph_trap",
    "bat-creature",
    "small_serpent",
    "medium_serpent",
    "large_serpent",
    "giant_serpent"
}

def check_or_return_none(prompt=None):
    try:
        choice = check_input(prompt or "\n> ").strip().lower()
    except ReturnToMenu:
        return None
    if choice == "r":
        return "RETRY"
    return choice

def get_random_choice(options, num_choices=2):
    if num_choices > len(options):
        num_choices = len(options)
    selected = random.sample(options, num_choices)
    while True:
        print_wrapped()
        for i, option in enumerate(selected, start=1):
            print_wrapped(f"{i}. {option['description']}", newline_delay=0.5)
        choice = check_or_return_none()
        if choice is None:
            return None
        if choice.isdigit():
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(selected):
                return selected[choice_index]
        print_wrapped("Invalid input. Please try again.")

def check_and_run_random_handler(options, num_choices=2, checkpoint=None):
    """
    Show randomized options and run the chosen handler.
    NOTE: Do NOT catch ReturnToMenu here. Let it bubble to top-level.
    """
    if checkpoint is not None:
        game_state["last_choice"] = (checkpoint, [], {})
    choice = get_random_choice(options, num_choices)
    if choice is None:
        return
    handler = choice["handler"]
    args    = choice.get("args",   ())
    kwargs  = choice.get("kwargs", {})
    game_state["last_choice"] = (handler, args, kwargs)
    return handler(*args, **kwargs)

def _supports_kwarg(func, name: str) -> bool:
    """
    Returns True if `func` accepts a keyword argument called `name`.
    Safe for most Python callables; falls back to False for builtins/C funcs.
    """
    try:
        sig = inspect.signature(func)
        return name in sig.parameters
    except (ValueError, TypeError):
        # Builtins / C-level callables or objects without a Python signature
        return False

def _invoke_with_optional_force_intro(handler, args, kwargs, want_force_intro: bool = True):
    """
    Calls `handler(*args, **kwargs)`, adding force_intro=True ONLY if the handler
    actually supports that kwarg. Prevents TypeError on undecorated handlers.
    """
    if want_force_intro and _supports_kwarg(handler, "force_intro"):
        kw = dict(kwargs)
        kw.setdefault("force_intro", True)
        return handler(*args, **kw)
    return handler(*args, **kwargs)

def game_over(reason, death_type):
    global game_state, player_state
    print_wrapped(f"\n{reason}", newline_delay=1.5)
    if (
            not death_type
            or death_type in SILENT_DEATHS
            or death_type not in death_scenarios
            or death_type not in final_deaths):
        print_wrapped("Your journey ends here.", newline_delay=1)
    else:
        print_wrapped("You have one last chance to survive...", newline_delay=1)
    options = death_scenarios.get(death_type)
    # ["Do nothing.", "Panic.", "Try to wake from this nightmare."]
    if options:
        selected_indices = random.sample(range(len(options)), 2)
        print_wrapped()
        print_wrapped(f"1. {options[selected_indices[0]]}", newline_delay=1)
        print_wrapped(f"2. {options[selected_indices[1]]}", newline_delay=1)
        choice = check_or_return_none()
        if choice is None:
            return None
        if choice == "1":
            chosen_index = selected_indices[0]
        elif choice == "2":
            chosen_index = selected_indices[1]
        else:
            print_wrapped("\nYou hesitated... and that was your downfall.", newline_delay=1)
            return None
        if death_type in final_deaths:
            print_wrapped(f"\n{final_deaths[death_type][chosen_index]}", newline_delay=1)
    game_state["death_count"] = game_state.get("death_count", 0) + 1
    dc = game_state["death_count"]
    if dc == 1:
        print_wrapped("You died, but it doesn't have to end here. You can try again...", newline_delay=1)
    elif dc == 2:
        print_wrapped("Death found you again...but the persistent are rewarded tenfold...", newline_delay=1)
    elif dc == 3:
        print_wrapped("Third time's the charm...but, wouldn't your next try be the fourth?...", newline_delay=1)
    else:
        print_wrapped("\nYou have died (again). Better luck awaits those who follow a different path...",
                      newline_delay=1)
    from .start import start_game
    prompt = (
            "\nPress [R] + Enter to retry your last move,\n"
            "or press [N] + Enter to start a new game,\n"
            "or any other key to return to the main menu:\n"
            "> "
    )
    resp = delayed_input(prompt).strip().lower()
    if resp == "r" and game_state.get("last_choice"):
        if death_type in ["bat-creature"]:
            game_state["cave_noise"] = max(0, game_state.get("cave_noise", 1) - 1)
        elif death_type in []:
            game_state["splash_amount"] = max(0, game_state.get("splash_amount", 1) - 1)
        handler, args, kwargs = game_state["last_choice"]
        return _invoke_with_optional_force_intro(handler, args, kwargs, want_force_intro=True)
    elif resp == "n":
        game_state, player_state = reset_game_state(), reset_player_state()
        return start_game()
    raise ReturnToMenu

def role_playing_game():
    """
    Entry point from Game_Selection. Runs the RPG and returns cleanly to the
    game selection menu when the player opts out at a death screen.
    """
    from utils.input_handlers import ReturnToMenu
    from .start import start_game
    try:
        start_game()
    except ReturnToMenu:
        # Print once, at the top level, then return control to Game_Selection.py
        print_wrapped("Quitting...", newline_delay=0.5)
        return

