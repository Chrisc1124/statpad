"""
Database setup and schema initialization for StatPad.
Creates SQLite database with all required tables.
"""

import sqlite3
import os
from pathlib import Path

# Get database path (database is in backend directory)
# setup.py is in backend/app/database/, so parent.parent.parent is backend/
BACKEND_ROOT = Path(__file__).parent.parent.parent
DB_PATH = BACKEND_ROOT / "statpad.db"


def create_database():
    """Create SQLite database with all required tables."""
    
    # Create database connection
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")
    
    try:
        # Create teams table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teams (
                team_id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_abbrev TEXT UNIQUE NOT NULL,
                team_name TEXT NOT NULL,
                conference TEXT,
                division TEXT,
                city TEXT,
                arena TEXT
            )
        """)
        
        # Create players table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                team_id INTEGER,
                position TEXT,
                age INTEGER,
                height TEXT,
                weight INTEGER,
                college TEXT,
                draft_year INTEGER,
                draft_pick INTEGER,
                FOREIGN KEY (team_id) REFERENCES teams(team_id)
            )
        """)
        
        # Create seasons table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS seasons (
                season_id INTEGER PRIMARY KEY AUTOINCREMENT,
                season TEXT UNIQUE NOT NULL,
                start_year INTEGER NOT NULL,
                end_year INTEGER NOT NULL,
                is_current BOOLEAN DEFAULT 0
            )
        """)
        
        # Create player_stats table (season-level aggregates)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS player_stats (
                stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                season_id INTEGER NOT NULL,
                team_id INTEGER,
                games_played INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                minutes_per_game REAL DEFAULT 0,
                points_per_game REAL DEFAULT 0,
                field_goals_made REAL DEFAULT 0,
                field_goals_attempted REAL DEFAULT 0,
                field_goal_percentage REAL DEFAULT 0,
                three_pointers_made REAL DEFAULT 0,
                three_pointers_attempted REAL DEFAULT 0,
                three_point_percentage REAL DEFAULT 0,
                free_throws_made REAL DEFAULT 0,
                free_throws_attempted REAL DEFAULT 0,
                free_throw_percentage REAL DEFAULT 0,
                offensive_rebounds REAL DEFAULT 0,
                defensive_rebounds REAL DEFAULT 0,
                total_rebounds REAL DEFAULT 0,
                assists REAL DEFAULT 0,
                turnovers REAL DEFAULT 0,
                steals REAL DEFAULT 0,
                blocks REAL DEFAULT 0,
                personal_fouls REAL DEFAULT 0,
                fantasy_points REAL DEFAULT 0,
                double_doubles INTEGER DEFAULT 0,
                triple_doubles INTEGER DEFAULT 0,
                plus_minus REAL DEFAULT 0,
                true_shooting_percentage REAL DEFAULT 0,
                UNIQUE(player_id, season_id),
                FOREIGN KEY (player_id) REFERENCES players(player_id),
                FOREIGN KEY (season_id) REFERENCES seasons(season_id),
                FOREIGN KEY (team_id) REFERENCES teams(team_id)
            )
        """)
        
        # Create games table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS games (
                game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                season_id INTEGER NOT NULL,
                game_date DATE NOT NULL,
                home_team_id INTEGER NOT NULL,
                away_team_id INTEGER NOT NULL,
                home_score INTEGER DEFAULT 0,
                away_score INTEGER DEFAULT 0,
                home_win BOOLEAN DEFAULT 0,
                game_type TEXT DEFAULT 'Regular Season',
                FOREIGN KEY (season_id) REFERENCES seasons(season_id),
                FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
                FOREIGN KEY (away_team_id) REFERENCES teams(team_id)
            )
        """)
        
        # Create game_stats table (individual game stats per player)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS game_stats (
                game_stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER NOT NULL,
                player_id INTEGER NOT NULL,
                team_id INTEGER NOT NULL,
                minutes_played REAL DEFAULT 0,
                points INTEGER DEFAULT 0,
                field_goals_made INTEGER DEFAULT 0,
                field_goals_attempted INTEGER DEFAULT 0,
                three_pointers_made INTEGER DEFAULT 0,
                three_pointers_attempted INTEGER DEFAULT 0,
                free_throws_made INTEGER DEFAULT 0,
                free_throws_attempted INTEGER DEFAULT 0,
                offensive_rebounds INTEGER DEFAULT 0,
                defensive_rebounds INTEGER DEFAULT 0,
                total_rebounds INTEGER DEFAULT 0,
                assists INTEGER DEFAULT 0,
                turnovers INTEGER DEFAULT 0,
                steals INTEGER DEFAULT 0,
                blocks INTEGER DEFAULT 0,
                personal_fouls INTEGER DEFAULT 0,
                plus_minus INTEGER DEFAULT 0,
                FOREIGN KEY (game_id) REFERENCES games(game_id),
                FOREIGN KEY (player_id) REFERENCES players(player_id),
                FOREIGN KEY (team_id) REFERENCES teams(team_id)
            )
        """)
        
        # Create indexes for better query performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_player_stats_player_season ON player_stats(player_id, season_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_game_stats_game_player ON game_stats(game_id, player_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_games_date ON games(game_date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_games_teams ON games(home_team_id, away_team_id)")
        
        # Commit changes
        conn.commit()
        print(f"✅ Database created successfully at {DB_PATH}")
        print("✅ All tables and indexes created")
        
    except sqlite3.Error as e:
        print(f"❌ Error creating database: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    create_database()

