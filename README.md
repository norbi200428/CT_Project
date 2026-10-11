# CT_Project

A lightweight Python project for tracking esports match performance using a CSV-backed data store. The project currently focuses on Valorant-style match records, with synthetic data generation, basic CRUD-style logic, and a CLI menu for viewing and managing match stats.

## Project goal

This project is designed to help track individual player match history and summarize performance through simple metrics such as:

- K/D ratio
- K/D/A ratio
- ADR (average damage per round)
- Headshot percentage
- Win/loss record and win rate

It is a small data-focused project intended to practice Python file handling, CSV processing, data validation, and console application design.

## Current status

The project is in an early but working state. The main pieces implemented so far are:

- Synthetic match data generation
- Loading and saving records to `matches.csv`
- Viewing all matches in a compact formatted table
- Viewing a specific player's career summary
- Creating a new match record with validation checks

Planned or incomplete areas include:

- Full update flow for editing existing records
- Full delete flow with confirmation handling
- More advanced analytics and reporting

## Repository structure

```text
CT_Project/
├── generate_data.py   # creates a sample dataset in matches.csv
├── crud.py            # CSV CRUD helpers and match metrics logic
├── main.py            # interactive CLI entry point
├── matches.csv        # generated match data
├── requirements.txt   # project environment notes
├── README.md          # project documentation
├── .venv              # local virtual environment
└── .gitignore
```

## Data model

The generated CSV uses the following columns:

- `match_id`
- `player_id`
- `map_name`
- `character`
- `result`
- `rounds_won`
- `rounds_lost`
- `total_rounds`
- `kills`
- `deaths`
- `assists`
- `headshots`
- `damage`

## Supported maps and agents

The app validates against a fixed set of Valorant-inspired values:

Maps:

- Abyss
- Ascent
- Haven
- Lotus
- Split
- Summit

Agents:

- Astra
- Breach
- Brimstone
- Chamber
- Clove
- Cypher
- Deadlock
- Fade
- Gekko
- Harbor
- Iso
- Jett
- KAY/O
- Killjoy
- Neon
- Omen
- Phoenix
- Raze
- Reyna
- Sage
- Skye
- Sova
- Tejo
- Veto
- Viper
- Vyse
- Waylay
- Yoru

## Python environment

This repository uses a local Python virtual environment in `.venv`.

In PowerShell, activate it with:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then check the Python version:

```powershell
python --version
```

To leave the environment:

```powershell
deactivate
```

## Setup

1. Open a terminal in the project root.
2. Activate the virtual environment.
3. Ensure Python is available.
4. Run the generator to create sample data if `matches.csv` is missing or needs to be refreshed.

## Usage

### Generate sample match data

```powershell
python generate_data.py
```

This creates a CSV file named `matches.csv` with 100 generated match records.

### Run the CLI

```powershell
python main.py
```

The CLI menu includes:

1. View all matches
2. View a player's career stats
3. Log a new match
4. Edit a match record
5. Delete a match
6. Exit

## Example flow

```powershell
.\.venv\Scripts\Activate.ps1
python generate_data.py
python main.py
```

## Notes

- The project uses the Python standard library only (`csv`, `os`, and `random`), so there are no external dependencies beyond Python itself.
- `matches.csv` is the main persistence layer at this stage.
- The generated records are synthetic and intended for testing, learning, and dashboard-style analysis.

## Future improvements

A likely next step for this project would be to expand the CLI into a more complete tracker with:

- export to CSV or JSON
- a simple dashboard or charting view
- database-backed storage instead of a flat CSV file

This README reflects the current project state and may be expanded as the app grows.