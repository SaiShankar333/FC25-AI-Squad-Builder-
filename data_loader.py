import json
import os

def load_player_data(json_path):
    with open(json_path, "r") as f:
        players = json.load(f)

    players = [p for p in players if p.get("Name")]
    return sorted(players, key=lambda p: int(p.get("OVR", 0)), reverse=True)

def load_players():
    return load_player_data(os.path.join("Manchester_City", "ManchesterCity_Combined.json"))

