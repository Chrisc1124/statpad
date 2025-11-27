"""
Import game logs from NBA API.
Fetches game-by-game stats for players and teams.
"""

import sqlite3
from pathlib import Path
from nba_api.stats.endpoints import leaguegamelog
import time
from datetime import datetime

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
DB_PATH = PROJECT_ROOT / "statpad.db"

# Seasons to import (most recent first)
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


def get_or_create_game(cursor, season_id, game_date, home_team_id, away_team_id, home_score, away_score, game_type="Regular Season"):
    """Get or create a game and return game_id."""
    cursor.execute("""
        SELECT game_id FROM games 
        WHERE season_id = ? AND game_date = ? 
        AND home_team_id = ? AND away_team_id = ?
    """, (season_id, game_date, home_team_id, away_team_id))
    
    row = cursor.fetchone()
    if row:
        return row[0]
    
    # Create new game
    home_win = 1 if home_score > away_score else 0
    cursor.execute("""
        INSERT INTO games (season_id, game_date, home_team_id, away_team_id, home_score, away_score, home_win, game_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (season_id, game_date, home_team_id, away_team_id, home_score, away_score, home_win, game_type))
    
    return cursor.lastrowid


def import_player_game_logs(season):
    """Import player game logs for a specific season."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        season_id = get_season_id(cursor, season)
        if not season_id:
            print(f"❌ Season {season} not found. Run seed_seasons.py first.")
            return
        
        print(f"📊 Fetching player game logs for {season}...")
        
        # Get player game logs from NBA API
        player_logs = leaguegamelog.LeagueGameLog(
            season=season,
            season_type_all_star='Regular Season',
            player_or_team_abbreviation='P'  # P for Player
        )
        
        df = player_logs.get_data_frames()[0]
        
        games_created = set()
        stats_imported = 0
        
        for _, row in df.iterrows():
            try:
                player_name = row['PLAYER_NAME']
                team_abbrev = row['TEAM_ABBREVIATION']
                game_date_str = row['GAME_DATE']
                matchup = row['MATCHUP']  # e.g., "DEN vs. LAL" or "LAL @ DEN"
                
                # Parse game date (already in YYYY-MM-DD format from API)
                if len(game_date_str) == 10 and '-' in game_date_str:
                    game_date = game_date_str
                else:
                    # Try to parse other formats
                    try:
                        game_date = datetime.strptime(game_date_str, '%b %d, %Y').strftime('%Y-%m-%d')
                    except:
                        continue
                
                # Parse matchup to get home/away teams
                if '@' in matchup:
                    # Away @ Home (e.g., "LAL @ DEN")
                    parts = matchup.split(' @ ')
                    away_abbrev = parts[0].strip()
                    home_abbrev = parts[1].strip()
                elif 'vs.' in matchup or ' vs ' in matchup:
                    # Home vs. Away (e.g., "DEN vs. LAL")
                    parts = matchup.replace('vs.', 'vs').split(' vs ')
                    home_abbrev = parts[0].strip()
                    away_abbrev = parts[1].strip()
                else:
                    continue
                
                # Get team IDs
                home_team_id = get_team_id(cursor, home_abbrev)
                away_team_id = get_team_id(cursor, away_abbrev)
                
                if not home_team_id or not away_team_id:
                    continue
                
                # Get player's team ID
                player_team_id = get_team_id(cursor, team_abbrev)
                if not player_team_id:
                    continue
                
                # Determine if player's team is home or away
                is_home = (player_team_id == home_team_id)
                
                # Get game or create it (scores will be updated by team logs)
                game_key = (season_id, game_date, home_team_id, away_team_id)
                if game_key not in games_created:
                    # Create game with placeholder scores (will be updated by team logs)
                    game_id = get_or_create_game(
                        cursor, season_id, game_date, home_team_id, away_team_id,
                        0, 0, "Regular Season"
                    )
                    games_created.add(game_key)
                else:
                    cursor.execute("""
                        SELECT game_id FROM games 
                        WHERE season_id = ? AND game_date = ? 
                        AND home_team_id = ? AND away_team_id = ?
                    """, (season_id, game_date, home_team_id, away_team_id))
                    result = cursor.fetchone()
                    if result:
                        game_id = result[0]
                    else:
                        continue
                
                # Get or create player
                player_id = get_or_create_player(cursor, player_name)
                
                # Insert game stats
                cursor.execute("""
                    INSERT OR REPLACE INTO game_stats (
                        game_id, player_id, team_id,
                        minutes_played, points,
                        field_goals_made, field_goals_attempted,
                        three_pointers_made, three_pointers_attempted,
                        free_throws_made, free_throws_attempted,
                        offensive_rebounds, defensive_rebounds, total_rebounds,
                        assists, turnovers, steals, blocks,
                        personal_fouls, plus_minus
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    game_id, player_id, player_team_id,
                    float(row.get('MIN', 0)),
                    int(row.get('PTS', 0)),
                    int(row.get('FGM', 0)), int(row.get('FGA', 0)),
                    int(row.get('FG3M', 0)), int(row.get('FG3A', 0)),
                    int(row.get('FTM', 0)), int(row.get('FTA', 0)),
                    int(row.get('OREB', 0)), int(row.get('DREB', 0)), int(row.get('REB', 0)),
                    int(row.get('AST', 0)), int(row.get('TOV', 0)), int(row.get('STL', 0)), int(row.get('BLK', 0)),
                    int(row.get('PF', 0)), int(row.get('PLUS_MINUS', 0))
                ))
                
                stats_imported += 1
                
            except Exception as e:
                # Skip problematic rows
                continue
        
        conn.commit()
        print(f"✅ Imported {stats_imported} player game stats for {season}")
        
    except Exception as e:
        print(f"❌ Error importing game logs for {season}: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
        raise
    finally:
        conn.close()


def import_team_game_logs(season):
    """Import team game logs to get accurate scores."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        season_id = get_season_id(cursor, season)
        if not season_id:
            return
        
        print(f"📊 Fetching team game logs for {season}...")
        
        # Get team game logs from NBA API
        team_logs = leaguegamelog.LeagueGameLog(
            season=season,
            season_type_all_star='Regular Season',
            player_or_team_abbreviation='T'  # T for Team
        )
        
        df = team_logs.get_data_frames()[0]
        
        for _, row in df.iterrows():
            try:
                team_abbrev = row['TEAM_ABBREVIATION']
                game_date_str = row['GAME_DATE']
                matchup = row['MATCHUP']
                team_score = int(row.get('PTS', 0))
                
                # Parse game date (already in YYYY-MM-DD format from API)
                if len(game_date_str) == 10 and '-' in game_date_str:
                    game_date = game_date_str
                else:
                    try:
                        game_date = datetime.strptime(game_date_str, '%b %d, %Y').strftime('%Y-%m-%d')
                    except:
                        continue
                
                # Parse matchup
                if '@' in matchup:
                    parts = matchup.split(' @ ')
                    away_abbrev = parts[0].strip()
                    home_abbrev = parts[1].strip()
                    is_home = (team_abbrev == home_abbrev)
                elif 'vs.' in matchup or 'vs' in matchup:
                    parts = matchup.replace('vs.', 'vs').split(' vs ')
                    home_abbrev = parts[0].strip()
                    away_abbrev = parts[1].strip()
                    is_home = (team_abbrev == home_abbrev)
                else:
                    continue
                
                home_team_id = get_team_id(cursor, home_abbrev)
                away_team_id = get_team_id(cursor, away_abbrev)
                
                if not home_team_id or not away_team_id:
                    continue
                
                # Update game scores
                if is_home:
                    cursor.execute("""
                        UPDATE games 
                        SET home_score = ? 
                        WHERE season_id = ? AND game_date = ? 
                        AND home_team_id = ? AND away_team_id = ?
                    """, (team_score, season_id, game_date, home_team_id, away_team_id))
                else:
                    cursor.execute("""
                        UPDATE games 
                        SET away_score = ? 
                        WHERE season_id = ? AND game_date = ? 
                        AND home_team_id = ? AND away_team_id = ?
                    """, (team_score, season_id, game_date, home_team_id, away_team_id))
                
                # Update home_win flag
                cursor.execute("""
                    UPDATE games 
                    SET home_win = CASE 
                        WHEN home_score > away_score THEN 1 
                        ELSE 0 
                    END
                    WHERE season_id = ? AND game_date = ? 
                    AND home_team_id = ? AND away_team_id = ?
                """, (season_id, game_date, home_team_id, away_team_id))
                
            except Exception as e:
                continue
        
        conn.commit()
        print(f"✅ Updated game scores for {season}")
        
    except Exception as e:
        print(f"❌ Error importing team game logs for {season}: {e}")
        conn.rollback()
    finally:
        conn.close()


def import_all_seasons():
    """Import game logs for all configured seasons."""
    for season in SEASONS:
        try:
            print(f"\n🔄 Processing {season}...")
            import_player_game_logs(season)
            time.sleep(2)  # Rate limiting
            import_team_game_logs(season)
            time.sleep(2)  # Rate limiting
        except Exception as e:
            print(f"⚠️  Error with {season}: {e}")
            continue


if __name__ == "__main__":
    print("🚀 Starting game logs import...")
    print("⚠️  This may take several minutes due to API rate limits...")
    import_all_seasons()
    print("\n✅ Game logs import complete!")

