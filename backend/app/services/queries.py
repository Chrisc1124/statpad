"""
Database query functions for StatPad.
Handles all database operations for players, teams, and stats.
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Optional, Any

# Get database path (database is in backend directory)
# queries.py is in backend/app/services/, so parent.parent.parent is backend/
BACKEND_ROOT = Path(__file__).parent.parent.parent
DB_PATH = BACKEND_ROOT / "statpad.db"


def get_db_connection():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn


def normalize_season(season: str) -> str:
    """Normalize season format (e.g., '2022-2023' -> '2022-23', '2024-2025' -> '2024-25')."""
    if not season:
        return season
    # Handle both - and / separators
    season = season.replace('/', '-')
    if '-' in season:
        parts = season.split('-')
        if len(parts) == 2:
            start = parts[0].strip()
            end = parts[1].strip()
            # Convert full year to short (e.g., 2023 -> 23, 2025 -> 25)
            if len(end) == 4:
                end = end[2:]
            elif len(end) == 2:
                # Already in short format
                pass
            return f"{start}-{end}"
    return season


def get_player_stats(player_name: str, season: str) -> Optional[Dict[str, Any]]:
    """Get player stats for a specific season."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Normalize season format
        normalized_season = normalize_season(season)
        
        # Case-insensitive player name search
        cursor.execute("""
            SELECT 
                p.player_id,
                p.name,
                p.position,
                t.team_name,
                t.team_abbrev,
                ps.*,
                s.season
            FROM players p
            JOIN player_stats ps ON p.player_id = ps.player_id
            JOIN seasons s ON ps.season_id = s.season_id
            LEFT JOIN teams t ON ps.team_id = t.team_id
            WHERE LOWER(p.name) = LOWER(?) AND s.season = ?
        """, (player_name.strip(), normalized_season))
        
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    finally:
        conn.close()


def compare_players(player1: str, player2: str, season: str) -> Dict[str, Any]:
    """Compare two players' stats for a specific season."""
    # Normalize season format
    normalized_season = normalize_season(season)
    
    # Get player1 stats
    player1_stats = get_player_stats(player1, normalized_season)
    
    # Get player2 stats
    player2_stats = get_player_stats(player2, normalized_season)
    
    return {
        "player1": player1_stats,
        "player2": player2_stats,
        "season": normalized_season
    }


def get_head_to_head_game_logs(
    player1: str, 
    player2: str, 
    season: Optional[str] = None,
    last_n: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Get head-to-head game logs for two players."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Normalize season if provided
        normalized_season = normalize_season(season) if season else None
        
        # Get player IDs (case-insensitive)
        cursor.execute("SELECT player_id FROM players WHERE LOWER(name) = LOWER(?)", (player1.strip(),))
        player1_row = cursor.fetchone()
        if not player1_row:
            return []
        player1_id = player1_row[0]
        
        cursor.execute("SELECT player_id FROM players WHERE LOWER(name) = LOWER(?)", (player2.strip(),))
        player2_row = cursor.fetchone()
        if not player2_row:
            return []
        player2_id = player2_row[0]
        
        # Build query - use subqueries to get only one game_stat per player per game
        # This handles cases where players have multiple game_stat entries (e.g., trades)
        # Use MAX(game_stat_id) to get the most recent entry for each player per game
        query = """
            SELECT 
                g.game_id,
                g.game_date,
                g.season_id,
                s.season,
                g.home_team_id,
                g.away_team_id,
                g.home_score,
                g.away_score,
                g.home_win,
                g.game_type,
                ht.team_name as home_team_name,
                ht.team_abbrev as home_team_abbrev,
                at.team_name as away_team_name,
                at.team_abbrev as away_team_abbrev,
                gs1.points as player1_points,
                gs1.field_goals_made as player1_fgm,
                gs1.field_goals_attempted as player1_fga,
                gs1.three_pointers_made as player1_3pm,
                gs1.three_pointers_attempted as player1_3pa,
                gs1.free_throws_made as player1_ftm,
                gs1.free_throws_attempted as player1_fta,
                gs1.total_rebounds as player1_rebounds,
                gs1.assists as player1_assists,
                gs1.steals as player1_steals,
                gs1.blocks as player1_blocks,
                gs1.turnovers as player1_turnovers,
                gs1.plus_minus as player1_plus_minus,
                gs2.points as player2_points,
                gs2.field_goals_made as player2_fgm,
                gs2.field_goals_attempted as player2_fga,
                gs2.three_pointers_made as player2_3pm,
                gs2.three_pointers_attempted as player2_3pa,
                gs2.free_throws_made as player2_ftm,
                gs2.free_throws_attempted as player2_fta,
                gs2.total_rebounds as player2_rebounds,
                gs2.assists as player2_assists,
                gs2.steals as player2_steals,
                gs2.blocks as player2_blocks,
                gs2.turnovers as player2_turnovers,
                gs2.plus_minus as player2_plus_minus
            FROM games g
            JOIN seasons s ON g.season_id = s.season_id
            JOIN teams ht ON g.home_team_id = ht.team_id
            JOIN teams at ON g.away_team_id = at.team_id
            JOIN game_stats gs1 ON g.game_id = gs1.game_id 
                AND gs1.player_id = ?
                AND gs1.game_stat_id = (
                    SELECT MAX(game_stat_id) 
                    FROM game_stats 
                    WHERE game_id = g.game_id AND player_id = ?
                )
            JOIN game_stats gs2 ON g.game_id = gs2.game_id 
                AND gs2.player_id = ?
                AND gs2.game_stat_id = (
                    SELECT MAX(game_stat_id) 
                    FROM game_stats 
                    WHERE game_id = g.game_id AND player_id = ?
                )
            WHERE (gs1.team_id != gs2.team_id)
        """
        
        params = [player1_id, player1_id, player2_id, player2_id]
        
        if normalized_season:
            query += " AND s.season = ?"
            params.append(normalized_season)
        
        query += " ORDER BY g.game_date DESC"
        
        if last_n:
            query += " LIMIT ?"
            params.append(last_n)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    finally:
        conn.close()


def compare_teams(
    team1: str, 
    team2: str, 
    season: str,
    include_game_logs: bool = False,
    last_n: Optional[int] = None
) -> Dict[str, Any]:
    """Compare two teams for a specific season."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Normalize season format
        normalized_season = normalize_season(season)
        
        # Get team IDs (case-insensitive, also check if team name contains the search term)
        team1_search = team1.strip().lower()
        cursor.execute("""
            SELECT team_id FROM teams 
            WHERE LOWER(team_abbrev) = ? 
            OR LOWER(team_name) = ?
            OR LOWER(team_name) LIKE ?
            OR LOWER(team_abbrev) LIKE ?
        """, (team1_search, team1_search, f'%{team1_search}%', f'%{team1_search}%'))
        team1_row = cursor.fetchone()
        if not team1_row:
            return {"error": f"Team {team1} not found"}
        team1_id = team1_row[0]
        
        team2_search = team2.strip().lower()
        cursor.execute("""
            SELECT team_id FROM teams 
            WHERE LOWER(team_abbrev) = ? 
            OR LOWER(team_name) = ?
            OR LOWER(team_name) LIKE ?
            OR LOWER(team_abbrev) LIKE ?
        """, (team2_search, team2_search, f'%{team2_search}%', f'%{team2_search}%'))
        team2_row = cursor.fetchone()
        if not team2_row:
            return {"error": f"Team {team2} not found"}
        team2_id = team2_row[0]
        
        # Get season ID
        cursor.execute("SELECT season_id FROM seasons WHERE season = ?", (normalized_season,))
        season_row = cursor.fetchone()
        if not season_row:
            return {"error": f"Season {season} not found"}
        season_id = season_row[0]
        
        # Get aggregate stats for each team (from player_stats)
        # This is a simplified version - in production, you'd aggregate from game_stats
        result = {
            "team1": team1,
            "team2": team2,
            "season": normalized_season,
            "game_logs": []
        }
        
        if include_game_logs:
            # Get game logs
            query = """
                SELECT 
                    g.game_id,
                    g.game_date,
                    g.home_team_id,
                    g.away_team_id,
                    g.home_score,
                    g.away_score,
                    g.home_win,
                    ht.team_name as home_team_name,
                    ht.team_abbrev as home_team_abbrev,
                    at.team_name as away_team_name,
                    at.team_abbrev as away_team_abbrev
                FROM games g
                JOIN teams ht ON g.home_team_id = ht.team_id
                JOIN teams at ON g.away_team_id = at.team_id
                WHERE g.season_id = ?
                AND ((g.home_team_id = ? AND g.away_team_id = ?) OR (g.home_team_id = ? AND g.away_team_id = ?))
                ORDER BY g.game_date DESC
            """
            
            if last_n:
                query += " LIMIT ?"
                cursor.execute(query, (season_id, team1_id, team2_id, team2_id, team1_id, last_n))
            else:
                cursor.execute(query, (season_id, team1_id, team2_id, team2_id, team1_id))
            
            rows = cursor.fetchall()
            result["game_logs"] = [dict(row) for row in rows]
        
        return result
    finally:
        conn.close()

