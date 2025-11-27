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


def get_player_stats(player_name: str, season: str) -> Optional[Dict[str, Any]]:
    """Get player stats for a specific season."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
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
            WHERE p.name = ? AND s.season = ?
        """, (player_name, season))
        
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    finally:
        conn.close()


def compare_players(player1: str, player2: str, season: str) -> Dict[str, Any]:
    """Compare two players' stats for a specific season."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get player1 stats
        player1_stats = get_player_stats(player1, season)
        
        # Get player2 stats
        player2_stats = get_player_stats(player2, season)
        
        return {
            "player1": player1_stats,
            "player2": player2_stats,
            "season": season
        }
    finally:
        conn.close()


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
        # Get player IDs
        cursor.execute("SELECT player_id FROM players WHERE name = ?", (player1,))
        player1_row = cursor.fetchone()
        if not player1_row:
            return []
        player1_id = player1_row["player_id"]
        
        cursor.execute("SELECT player_id FROM players WHERE name = ?", (player2,))
        player2_row = cursor.fetchone()
        if not player2_row:
            return []
        player2_id = player2_row["player_id"]
        
        # Build query
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
                gs1.total_rebounds as player1_rebounds,
                gs1.assists as player1_assists,
                gs2.points as player2_points,
                gs2.total_rebounds as player2_rebounds,
                gs2.assists as player2_assists
            FROM games g
            JOIN seasons s ON g.season_id = s.season_id
            JOIN teams ht ON g.home_team_id = ht.team_id
            JOIN teams at ON g.away_team_id = at.team_id
            JOIN game_stats gs1 ON g.game_id = gs1.game_id AND gs1.player_id = ?
            JOIN game_stats gs2 ON g.game_id = gs2.game_id AND gs2.player_id = ?
            WHERE (gs1.team_id != gs2.team_id)
        """
        
        params = [player1_id, player2_id]
        
        if season:
            query += " AND s.season = ?"
            params.append(season)
        
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
        # Get team IDs
        cursor.execute("SELECT team_id FROM teams WHERE team_abbrev = ? OR team_name = ?", (team1, team1))
        team1_row = cursor.fetchone()
        if not team1_row:
            return {"error": f"Team {team1} not found"}
        team1_id = team1_row["team_id"]
        
        cursor.execute("SELECT team_id FROM teams WHERE team_abbrev = ? OR team_name = ?", (team2, team2))
        team2_row = cursor.fetchone()
        if not team2_row:
            return {"error": f"Team {team2} not found"}
        team2_id = team2_row["team_id"]
        
        # Get season ID
        cursor.execute("SELECT season_id FROM seasons WHERE season = ?", (season,))
        season_row = cursor.fetchone()
        if not season_row:
            return {"error": f"Season {season} not found"}
        season_id = season_row["season_id"]
        
        # Get aggregate stats for each team (from player_stats)
        # This is a simplified version - in production, you'd aggregate from game_stats
        result = {
            "team1": team1,
            "team2": team2,
            "season": season,
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
                    at.team_name as away_team_name
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

