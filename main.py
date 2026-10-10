import crud

def handle_view_matches(matches):
    if not matches:
        print("\n No match data available.")
        return

    print("\n" + "=" * 80)
    print(f"{'ID':<6} {'Player':<8} {'Map':<10} {'Agent':<10} {'Result':<8} {'Score':<8} {'K/D':<6} {'ADR':<7} {'HS%':<6}")
    print("-" * 80)

# !!!!!!!!!!!!!!!!!!!! DO NOT FORGET TO REMOVE THE SLICE
# so far KDA is useless so might delete later
    for m in matches[0:10]:
        kd, _, adr, headshot_rate = crud.calculate_metrics(m)

        score = f"{m['rounds_won']}-{m['rounds_lost']}"
        print(f"{m['match_id']:<6} {m['player_id']:<8} {m['map_name']:<10} {m['character']:<10} "
              f"{m['result']:<8} {score:<8} {kd:<6.2f} {adr:<7.1f} {headshot_rate:<5.1f}%")
    print("=" * 80) 

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
            pass
            handle_view_matches(matches)
        elif choice == "2":
            pass
            # handle_view_player(matches)
        elif choice == "3":
            pass 
            # handle_create(matches)
        elif choice == "4":
            pass 
            # handle_update(matches)
        elif choice == "5":
            pass
            # handle_delete(matches)
        elif choice == "6":
            print("\nExiting program. All data saved.")
            break
        else:
            print("Invalid option. Enter a number 1-6.")


if __name__ == "__main__":
    main()