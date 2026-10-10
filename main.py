import crud

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
    pass

# UPDATE AN EXISTING RECORD 
# Interactive CLI; ask for each field value, if not provided, data remains unchanged
# might be a good idea to not allow the user to change the outcome of the match (results, rounds_won, rounds_lost, total_rounds) ?
def handle_update(matches):
    pass
# DELETE A RECORD
# would be nice to ask for a confirmation before delete
def handle_delete(matches):
    pass

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