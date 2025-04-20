from formation_config import FORMATIONS

def select_best_11_and_bench(players, formation_name):
    formation = FORMATIONS.get(formation_name, [])
    starting_xi = []
    used_players = set()

    # Define alternate position mappings
    alt_positions = {
        "GK": ["GK"],  # no alt really
        "RB": ["RWB", "CB"],
        "LB": ["LWB", "CB"],
        "CB": ["RB", "LB"],
        "RWB": ["RB", "RM"],
        "LWB": ["LB", "LM"],
        "CDM": ["CM"],
        "CM": ["CDM", "CAM"],
        "CAM": ["CM", "CF"],
        "RM": ["RW", "CM"],
        "LM": ["LW", "CM"],
        "RW": ["RM", "ST"],
        "LW": ["LM", "ST"],
        "ST": ["CF", "CAM"],
        "CF": ["ST", "CAM"],
    }

    for row in formation:
        row_players = []
        for role in row:
            if not isinstance(role, str):
                row_players.append(None)
                continue

            role = role.upper()

            # Try exact role first
            player = next((p for p in players if role in p.get("Position", []) and p["Name"] not in used_players), None)

            # Try alternates
            if not player:
                alternates = alt_positions.get(role, [])
                player = next((p for p in players if any(alt in p.get("Position", []) for alt in alternates) and p["Name"] not in used_players), None)

            if player:
                used_players.add(player["Name"])

            row_players.append(player)
        starting_xi.append(row_players)

    # Top 7 remaining players for bench
    substitutes = [p for p in players if p["Name"] not in used_players][:7]
    return starting_xi, substitutes
