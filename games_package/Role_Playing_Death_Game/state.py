import copy

default_game_state = {
    "noise_count": 0,
    "knight_in_library": False,
    "ask_librarian_first": False,
    "browse_books_first": False,
    "continue_browsing": False,
    "spied_on_librarian": False,
    "cave_noise": 0,
    "cave_creature_killed": False,
    "glowing_door_trap": False,
    "splash_amount": 0,
    "serpent_killed": False,
    "raft_status": "pool_shallow",
    "rope_on_raft": True,
}

def reset_game_state():
    """Return a fresh deep copy of the default state."""
    return copy.deepcopy(default_game_state)


default_player_state = {
    "location": None,
    "previous_location": None,
    "position": None,
    "previous_position": None,
    "state": None,
    "previous_state": None,
    "can_defend": False,
    "torch_lit": False,
    "inventory": [],
    "memory": [],
    "death_counter": 0
}



def reset_player_state():
    """Return a fresh deep copy of the default player state."""
    return copy.deepcopy(default_player_state)


ui_state = {
    "current_options": []
}