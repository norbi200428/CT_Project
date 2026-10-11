import csv
import os

CSV_FILE = "matches.csv"
FIELD_NAMES = [
    "match_id", "player_id", "map_name", "character", "result", "rounds_won", "rounds_lost", "total_rounds", "kills", "deaths", "assists", "headshots", "damage"
]

def load_matches(filepath=CSV_FILE):
    """Read matches.csv into a list of dictionaries"""

    matches = []

    if not os.path.exists(filepath):
        print(f"File: '{filepath}' not found.")
        return matches

    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            matches.append({
                "match_id": int(row["match_id"]),
                "player_id": int(row["player_id"]),
                "map_name": row["map_name"],
                "character": row["character"],
                "result": row["result"],
                "rounds_won": int(row["rounds_won"]),
                "rounds_lost": int(row["rounds_lost"]),
                "total_rounds": int(row["total_rounds"]),
                "kills": int(row["kills"]),
                "deaths": int(row["deaths"]),
                "assists": int(row["assists"]),
                "headshots": int(row["headshots"]),
                "damage": int(row["damage"]),
            })
            
    return matches

def save_matches(matches, filepath=CSV_FILE):
    """Save the list of matches in matches.csv"""

    with open(filepath, mode="w", newline= "", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELD_NAMES)
        writer.writeheader()
        writer.writerows(matches)

def calculate_metrics(match):
    """Calculate K/D, K/D/A, ADR, and HS%"""
    deaths = match["deaths"] if match["deaths"] > 0 else 1 # avoid "divide by 0"
    total_rounds = match["total_rounds"] if match["total_rounds"] > 0 else 1 # same as above
    kills = match["kills"]
    
    kd = kills / deaths
    kda = (kills + 0.5 * match["assists"]) / deaths
    adr =  match["damage"] / total_rounds
    headshot_rate = (match["headshots"] / kills * 100) if kills > 0 else 0.0

    return kd, kda, adr, headshot_rate

def get_all_matches(matches):
    """Return all stored matches."""
    return matches

# prob will need this for update tasks - if not just delete
def get_match_by_id(matches, match_id):
    """Return a single match by its id or None"""
    for m in matches:
        if m["match_id"] == match_id:
            return m
    return None

def get_player_stats(matches, player_id):
    """Calculate stats for a specific player"""
    player_matches = [m for m in matches if m["player_id"] == player_id]
    if not player_matches:
        return None

    total_kills = sum(m["kills"] for m in player_matches)
    total_deaths = sum(m["deaths"] for m in player_matches)
    total_rounds = sum(m["total_rounds"] for m in player_matches)
    total_damage = sum(m["damage"] for m in player_matches)
    wins = sum(1 for m in player_matches if m["result"].lower() == "win")
    total_matches = len(player_matches)

    return {
        "player_id": player_id,
        "matches_count": total_matches,
        "wins": wins,
        "losses": total_matches - wins,
        "win_rate": (wins / total_matches) * 100,
        "career_kd": total_kills / total_deaths if total_deaths > 0 else float(total_kills),
        "career_adr": total_damage / total_rounds if total_rounds > 0 else 0.0,
    }

def add_match(matches, player_id, map_name, character, result, rounds_won, rounds_lost, kills, deaths, assists, headshots, damage):
    """Create a new match record, append it, and persist to file."""
    existing_ids = [m["match_id"] for m in matches]
    next_id = max(existing_ids, default=0) + 1
    total_rounds = rounds_won + rounds_lost

    new_record = {
        "match_id": next_id,
        "player_id": player_id,
        "map_name": map_name,
        "character": character,
        "result": result,
        "rounds_won": rounds_won,
        "rounds_lost": rounds_lost,
        "total_rounds": total_rounds,
        "kills": kills,
        "deaths": deaths,
        "assists": assists,
        "headshots": headshots,
        "damage": damage,
    }

    matches.append(new_record)
    save_matches(matches)
    return new_record


def delete_match(matches, match_id):
    """Delete a match by its ID and persist changes."""
    match_to_delete = get_match_by_id(matches, match_id)
    if match_to_delete:
        matches.remove(match_to_delete)
        save_matches(matches)
        return True
    return False

def update_match(matches, match_id, **kwargs):
    """Update a match record by its ID and persist changes."""
    match_to_update = get_match_by_id(matches, match_id)
    if not match_to_update:
        return False

    for key, value in kwargs.items():
        if key in match_to_update:
            match_to_update[key] = value

    # recalculate total rounds if rounds_won or rounds_lost are updated
    if "rounds_won" in kwargs or "rounds_lost" in kwargs:
        match_to_update["total_rounds"] = match_to_update["rounds_won"] + match_to_update["rounds_lost"]

    save_matches(matches)
    return True