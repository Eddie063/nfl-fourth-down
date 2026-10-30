# Import and define the seasons once
import nflreadpy as nfl

SEASONS = list(range(2010, 2026))
print(SEASONS[0], SEASONS[-1], len(SEASONS))

# Load the two season-based tables
pbp = nfl.load_pbp(SEASONS)
schedules = nfl.load_schedules(SEASONS)

# Load the two lookup tables
teams = nfl.load_teams()
players = nfl.load_players()

# Print the shape of each
for name, df in [("pbp", pbp), ("schedules", schedules), ("teams", teams), ("players", players)]:
    print(name, df.shape)

REQUIRED = ["game_id", "play_id", "posteam", "down", "ydstogo",
            "yardline_100", "wp", "play_type"]
missing = [c for c in REQUIRED if c not in pbp.columns]
if missing:
    raise ValueError(f"pbp is missing columns: {missing}")
print("All required pbp columns present")