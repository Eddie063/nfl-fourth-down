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

# DuckDB library: lets Python create and query a local database file
import duckdb  

# Write the four tables into DuckDB

# Open the database file, or create it if it does not exist yet.
con = duckdb.connect("data/nfl.duckdb")

# Schema: "raw" holds the source data exactly as downloaded, untouched.
con.execute("CREATE SCHEMA IF NOT EXISTS raw")

# Copy each Python dataframe into a DuckDB table.
con.execute("CREATE OR REPLACE TABLE raw.pbp AS SELECT * FROM pbp")
con.execute("CREATE OR REPLACE TABLE raw.schedules AS SELECT * FROM schedules")
con.execute("CREATE OR REPLACE TABLE raw.teams AS SELECT * FROM teams")
con.execute("CREATE OR REPLACE TABLE raw.players AS SELECT * FROM players")

# Show what is now in the raw schema, as proof the load worked.
con.sql("""
    SELECT table_name, estimated_size
    FROM duckdb_tables()
    WHERE schema_name = 'raw'
    ORDER BY table_name
""").show()

# Release the database file.
con.close()