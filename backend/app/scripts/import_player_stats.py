"""
Import player stats from NBA API.
Fetches season stats for players and stores in database.
"""

import sqlite3
from pathlib import Path
from nba_api.stats.endpoints import leaguedashplayerstats
from nba_api.stats.static import players
import time

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
DB_PATH = PROJECT_ROOT / "statpad.db"

# Seasons to import (most recent first for faster testing)
SEASONS = ["2023-24", "2022-23", "2021-22"]


def get_season_id(cursor, season):
    """Get season_id for a season string."""
    cursor.execute("SELECT season_id FROM seasons WHERE season = ?", (season,))
    row = cursor.fetchone()
    return row[0] if row else None


def get_team_id(cursor, team_abbrev):
    """Get team_id for a team abbreviation."""
    if not team_abbrev:
        return None
    cursor.execute("SELECT team_id FROM teams WHERE team_abbrev = ?", (team_abbrev,))
    row = cursor.fetchone()
    return row[0] if row else None


def get_or_create_player(cursor, player_name):
    """Get or create a player and return player_id."""
    cursor.execute("SELECT player_id FROM players WHERE name = ?", (player_name,))
    row = cursor.fetchone()
    if row:
        return row[0]
    
    # Create new player
    cursor.execute("""
        INSERT INTO players (name)
        VALUES (?)
    """, (player_name,))
    return cursor.lastrowid


def import_season_stats(season):
    """Import player stats for a specific season."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        season_id = get_season_id(cursor, season)
        if not season_id:
            print(f"❌ Season {season} not found in database. Run seed_seasons.py first.")
            return
        
        # Convert season to NBA API format (e.g., "2023-24" -> "2023-24")
        season_param = season
        
        print(f"📊 Fetching stats for {season}...")
        
        # Get player stats from NBA API
        stats = leaguedashplayerstats.LeagueDashPlayerStats(
            season=season_param,
            season_type_all_star='Regular Season'
        )
        
        df = stats.get_data_frames()[0]
        
        imported = 0
        for _, row in df.iterrows():
            player_name = row['PLAYER_NAME']
            team_abbrev = row['TEAM_ABBREVIATION']
            
            # Get or create player
            player_id = get_or_create_player(cursor, player_name)
            
            # Get team_id
            team_id = get_team_id(cursor, team_abbrev)
            
            # Calculate per-game averages
            gp = int(row.get('GP', 1))  # Games played, avoid division by zero
            if gp == 0:
                gp = 1
            
            # Insert or update player stats (NBA API returns totals, we calculate per-game)
            cursor.execute("""
                INSERT OR REPLACE INTO player_stats (
                    player_id, season_id, team_id,
                    games_played, wins, losses,
                    minutes_per_game, points_per_game,
                    field_goals_made, field_goals_attempted, field_goal_percentage,
                    three_pointers_made, three_pointers_attempted, three_point_percentage,
                    free_throws_made, free_throws_attempted, free_throw_percentage,
                    offensive_rebounds, defensive_rebounds, total_rebounds,
                    assists, turnovers, steals, blocks,
                    personal_fouls, plus_minus
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                player_id, season_id, team_id,
                gp, int(row.get('W', 0)), int(row.get('L', 0)),
                float(row.get('MIN', 0)) / gp,  # Minutes per game
                float(row.get('PTS', 0)) / gp,  # Points per game
                float(row.get('FGM', 0)) / gp,  # FGM per game
                float(row.get('FGA', 0)) / gp,  # FGA per game
                float(row.get('FG_PCT', 0)),  # Percentage
                float(row.get('FG3M', 0)) / gp,  # 3PM per game
                float(row.get('FG3A', 0)) / gp,  # 3PA per game
                float(row.get('FG3_PCT', 0)),  # 3P%
                float(row.get('FTM', 0)) / gp,  # FTM per game
                float(row.get('FTA', 0)) / gp,  # FTA per game
                float(row.get('FT_PCT', 0)),  # FT%
                float(row.get('OREB', 0)) / gp,  # Offensive rebounds per game
                float(row.get('DREB', 0)) / gp,  # Defensive rebounds per game
                float(row.get('REB', 0)) / gp,  # Total rebounds per game
                float(row.get('AST', 0)) / gp,  # Assists per game
                float(row.get('TOV', 0)) / gp,  # Turnovers per game
                float(row.get('STL', 0)) / gp,  # Steals per game
                float(row.get('BLK', 0)) / gp,  # Blocks per game
                float(row.get('PF', 0)) / gp,  # Personal fouls per game
                float(row.get('PLUS_MINUS', 0)) / gp  # Plus/minus per game
            ))
            imported += 1
        
        conn.commit()
        print(f"✅ Imported {imported} player stats for {season}")
        
    except Exception as e:
        print(f"❌ Error importing stats for {season}: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


def import_all_seasons():
    """Import stats for all configured seasons."""
    for season in SEASONS:
        try:
            import_season_stats(season)
            time.sleep(1)  # Rate limiting
        except Exception as e:
            print(f"⚠️  Skipping {season}: {e}")
            continue


if __name__ == "__main__":
    print("🚀 Starting player stats import...")
    import_all_seasons()
    print("✅ Import complete!")

