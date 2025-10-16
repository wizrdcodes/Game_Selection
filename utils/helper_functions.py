from games_package.Role_Playing_Death_Game.core import player_state
import time
from utils.narration import SKIP_ALL, IMMERSION


def update_player_state(game_state=None, location=None, position=None, state=None, **kwargs):
    if location is not None:
        player_state["previous_location"] = player_state.get("location")
        player_state["location"] = location
    if position is not None:
        player_state["previous_position"] = player_state.get("position")
        player_state["position"] = position
    if state is not None:
        player_state["previous_state"] = player_state.get("state")
        player_state["state"] = state

    if game_state is not None:
        player_state["can_defend"] = (
            game_state.get("elegant_shield_in_hand", False) and
            player_state.get("state") not in ("swimming", "underwater")
        )

    # Handle any additional fields like weapon_ready, raft_status, etc.
    for key, value in kwargs.items():
        player_state[key] = value

def add_to_inventory(item):
    inventory = player_state.setdefault("inventory", [])
    if item not in inventory:
        inventory.append(item)

def has_item(item):
    return item in player_state.get("inventory", [])

def remember(key):
    memory = player_state.setdefault("memory", [])
    if key not in memory:
        memory.append(key)

def has_memory(key):
    return key in player_state.get("memory", [])

def remember_intro(scene_key):
    remember(f"intro_seen:{scene_key}")

def has_seen_intro(scene_key):
    return has_memory(f"intro_seen:{scene_key}")

def delay(seconds: float):
    if not SKIP_ALL and IMMERSION and seconds > 0:
        time.sleep(seconds)