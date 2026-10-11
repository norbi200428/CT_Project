import crud

VALID_MAPS = ["Abyss", "Ascent", "Haven", "Lotus", "Split", "Summit"]
VALID_AGENTS = ["Astra", "Breach", "Brimstone", "Chamber", "Clove", "Cypher", "Deadlock", "Fade", "Gekko", "Harbor", 
          "Iso", "Jett", "KAY/O", "Killjoy", "Neon", "Omen", "Phoenix", "Raze", "Reyna", "Sage", "Skye", "Sova", 
          "Tejo", "Veto", "Viper", "Vyse", "Waylay", "Yoru"]
# tested
def handle_view_matches(matches):
    if not matches:
        print("\n No match data available.")
        return

    print("\n" + "=" * 80)
    print(f"{'ID':<6} {'Player':<8} {'Map':<10} {'Agent':<10} {'Result':<8} {'Score':<8} {'K/D':<6} {'ADR':<7} {'HS%':<6}")
    print("-" * 80)

#tested
# !!!!!!!!!!!!!!!!!!!! DO NOT FORGET TO REMOVE THE SLICE
# so far KDA is useless so might delete later
    for m in matches:
        kd, _, adr, headshot_rate = crud.calculate_metrics(m)

        score = f"{m['rounds_won']}-{m['rounds_lost']}"
        print(f"{m['match_id']:<6} {m['player_id']:<8} {m['map_name']:<10} {m['character']:<10} "
              f"{m['result']:<8} {score:<8} {kd:<6.2f} {adr:<7.1f} {headshot_rate:<5.1f}%")
    print("=" * 80) 

# tested
def handle_view_player(matches):
    try:
        player_id = int(input("\nEnter a Player ID: ").strip())
    except ValueError:
        print("Player ID must be an integer.")
        return

    stats = crud.get_player_stats(matches, player_id)
    if not stats:
        print(f"No records found for Player ID: {player_id}")
        return

    print("\n" + "-" * 35)
    print(f"      CAREER SUMMARY: {stats['player_id']}")
    print("-" * 35)
    print(f"Matches Logged : {stats['matches_count']}")
    print(f"Record         : {stats['wins']}W - {stats['losses']}L")
    print(f"Win Rate       : {stats['win_rate']:.1f}%")
    print(f"Overall K/D    : {stats['career_kd']:.2f}")
    print(f"Overall ADR    : {stats['career_adr']:.1f}")
    print("-" * 35)

# CREATE A NEW RECORD IN THE DATABASE
def handle_create(matches):
    print("\n--- Log a New Match Record ---")
    try:
        player_id = int(input("Player ID (default 10001): ").strip() or "10001")
        map_name = input("Map Name (e.g., Haven, Ascent): ").strip().capitalize()
        agent = input("Agent/Character (e.g., Jett, Clove): ").strip().capitalize()

        result = input("Result (Win/Lose): ").strip().capitalize()
        if result not in ["Win", "Lose"]:
            print("Defaulting result to 'Lose'.")
            result = "Lose"

        rounds_w = int(input("Rounds Won: "))
        rounds_l = int(input("Rounds Lost: "))
        kills = int(input("Kills: "))
        deaths = int(input("Deaths: "))
        assists = int(input("Assists: "))
        headshots = int(input("Headshots: "))
        damage = int(input("Total Damage: "))

        # some extra checks for the input data
        total_rounds = rounds_w + rounds_l
        max_r, min_r = max(rounds_w, rounds_l), min(rounds_w, rounds_l)

        if min(rounds_w, rounds_l, kills, deaths, assists, headshots, damage) < 0:
            raise ValueError("Stats and rounds cannot be negative.")

        if (result == "Win" and rounds_w <= rounds_l) or (result == "Lose" and rounds_l <= rounds_w):
            raise ValueError(f"Score ({rounds_w}-{rounds_l}) does not match result '{result}'.")

        is_regulation = (max_r == 13 and min_r <= 11)
        is_overtime = (max_r >= 14 and min_r >= 12 and (max_r - min_r == 2))

        if not (is_regulation or is_overtime):
            raise ValueError(
                f"Invalid score ({rounds_w}-{rounds_l}). Must be 13-X (max 11) or win by 2 in overtime (e.g., 14-12)."
            )
        
        if kills > total_rounds * 5:
            raise ValueError(f"Kills ({kills}) exceed maximum possible.")

        if not map_name in VALID_MAPS:
            raise ValueError(f"Invalid map name: {map_name}.")

        if not agent in VALID_AGENTS:
            raise ValueError(f"Invalid agent name: {agent}.")
            
        record = crud.add_match(
            matches, player_id, map_name, agent, result,
            rounds_w, rounds_l, kills, deaths, assists, headshots, damage
        )
        print(f"\nMatch {record['match_id']} created and saved successfully.")

    except ValueError as e:
        print(f"Validation Error: {e}")

# UPDATE AN EXISTING RECORD 
# Interactive CLI; ask for each field value, if not provided, data remains unchanged
# might be a good idea to not allow the user to change the outcome of the match (results, rounds_won, rounds_lost, total_rounds) ?
# tested
def handle_update(matches):
    try:
        match_id = int(input("\nEnter the Match ID to update: ").strip())
        match = crud.get_match_by_id(matches, match_id)
        if not match:
            print(f"No match found with ID: {match_id}")
            return

        # comment out the ones that you dont want the user to be able to change
        print(f"\nUpdating Match ID: {match_id}. Leave blank to keep current value.")
        map_name = input(f"Map Name [{match['map_name']}]: ").strip().capitalize() or match['map_name']
        agent = input(f"Agent/Character [{match['character']}]: ").strip().capitalize() or match['character']
        # result = input(f"Result (Win/Lose) [{match['result']}]: ").strip().capitalize() or match['result']
        # rounds_w = input(f"Rounds Won [{match['rounds_won']}]: ").strip()
        # rounds_l = input(f"Rounds Lost [{match['rounds_lost']}]: ").strip()
        kills = input(f"Kills [{match['kills']}]: ").strip()
        deaths = input(f"Deaths [{match['deaths']}]: ").strip()
        assists = input(f"Assists [{match['assists']}]: ").strip()
        headshots = input(f"Headshots [{match['headshots']}]: ").strip()
        damage = input(f"Total Damage [{match['damage']}]: ").strip()

        # comment them out from here too 
        updated_values = {
            "map_name": map_name,
            "character": agent,
            # "result": result,
            # "rounds_won": int(rounds_w) if rounds_w else match['rounds_won'],
            # "rounds_lost": int(rounds_l) if rounds_l else match['rounds_lost'],
            "kills": int(kills) if kills else match['kills'],
            "deaths": int(deaths) if deaths else match['deaths'],
            "assists": int(assists) if assists else match['assists'],
            "headshots": int(headshots) if headshots else match['headshots'],
            "damage": int(damage) if damage else match['damage'],
        }

        crud.update_match(matches, match_id, **updated_values)
        print(f"\nMatch {match_id} updated successfully.")
    except ValueError as e:
        print(f"Validation Error: {e}")
# DELETE A RECORD
# would be nice to ask for a confirmation before delete
# tested
def handle_delete(matches):
    try:
        match_id = int(input("\nEnter the Match ID to delete: ").strip())
        match = crud.get_match_by_id(matches, match_id)
        if not match:
            print(f"No match found with ID: {match_id}")
            return

        confirm = input(f"Are you sure you want to delete Match ID {match_id}? (y/n): ").strip().lower()
        if confirm == 'y':
            success = crud.delete_match(matches, match_id)
            if success:
                print(f"Match {match_id} deleted successfully.")
            else:
                print(f"Failed to delete Match {match_id}.")
        else:
            print("Deletion canceled.")

    except ValueError:
        print("Invalid input. Please enter a valid Match ID.")

def main():
    matches = crud.load_matches()
    print(f"Loaded {len(matches)} match records from the database.")

    while True:
        print("\n" + "=" * 32)
        print("   ESPORTS TRACKER CLI  ")
        print("=" * 32)
        print("1. [Read]   View All Matches")
        print("2. [Read]   Player All Career Stats")
        print("3. [Create] Log New Match")
        print("4. [Update] Edit a Match Record")
        print("5. [Delete] Remove a Match")
        print("6. [Exit]   Exit Program")
        print("=" * 32)

        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            handle_view_matches(matches)
        elif choice == "2":
            handle_view_player(matches)
        elif choice == "3":
            handle_create(matches)
        elif choice == "4":
            handle_update(matches)
        elif choice == "5":
            handle_delete(matches)
        elif choice == "6":
            print("\nExiting program. All data saved.")
            break
        else:
            print("Invalid option. Enter a number 1-6.")

if __name__ == "__main__":
    main()