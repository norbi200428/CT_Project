import csv
import random

ROW_NUMBER = 100

maps = ["Abyss", "Ascent", "Haven", "Lotus", "Split", "Summit"]
agents = ["Astra", "Breach", "Brimstone", "Chamber", "Clove", "Cypher", "Deadlock", "Fade", "Gekko", "Harbor", 
          "Iso", "Jett", "KAY/O", "Killjoy", "Neon", "Omen", "Phoenix", "Raze", "Reyna", "Sage", "Skye", "Sova", 
          "Tejo", "Veto", "Viper", "Vyse", "Waylay", "Yoru"]
match_result = ["Win", "Lose"]

with open("matches.csv", mode="w", newline="", encoding="utf-8") as f:
    
    writer = csv.writer(f)
    writer.writerow([
        "match_id", "player_id", "map_name", "character", "result", "rounds_won", "rounds_lost", "total_rounds", "kills", "deaths", "assists", "headshots", "damage" 
    ])

    for match_id in range(1, ROW_NUMBER + 1):
        is_overtime = random.random() < 0.15 # the prob of OT in VCT is about 15%
        
        player_id = random.randint(10000, 50000)
        map_name = random.choice(maps)
        agent = random.choice(agents)
        result = random.choice(match_result)
        
        if result == "Win":
            if is_overtime:
                overtime_sets = random.randint(1, 11) # number of OT's (longest VCT match had 11 OT's)
                rounds_lost = 11 + overtime_sets
                rounds_won = rounds_lost + 2
            else:
                rounds_won = 13
                rounds_lost = random.randint(0, 11)
        else:
            if is_overtime:
                overtime_sets = random.randint(1, 11)
                rounds_won = 11 + overtime_sets
                rounds_lost = rounds_won + 2
            else:
                rounds_won = random.randint(0, 11)
                rounds_lost = 13

        kills = random.randint(0, 47)
        deaths = random.randint(1, 32)
        assists = random.randint(0, 28)
        headshots = random.randint(0, kills)
        total_rounds = rounds_won + rounds_lost
        damage = int(kills * random.uniform(100, 150) + assists * random.uniform(0, 50) + random.uniform(100, 400))
        writer.writerow([
            match_id, player_id, map_name, agent, result, rounds_won, rounds_lost, total_rounds, kills, deaths, assists, headshots, damage
        ])


print(f"matches.csv generated successfully with {ROW_NUMBER} rows.")
