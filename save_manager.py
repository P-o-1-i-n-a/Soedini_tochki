import json
import os
import atexit

SAVE_FILE = os.path.join(os.path.dirname(__file__), 'save.json')
game_data = {}

def save_game(data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

def load_game():
    if not os.path.exists(SAVE_FILE):
        return None
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def delete_save():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)

atexit.register(save_game, game_data)