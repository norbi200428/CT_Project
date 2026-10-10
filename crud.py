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