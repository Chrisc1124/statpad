"""
Natural Language Processing for StatPad queries.
Processes plain English queries and routes to appropriate endpoints.
"""

import re
from typing import Dict, Any, Optional


def parse_query(query: str) -> Dict[str, Any]:
    """
    Parse natural language query and return structured query information.
    
    Supported query types:
    - Player stats: "How many points did Stephen Curry score in 2023-24?"
    - Player comparison: "Compare Stephen Curry and LeBron James in 2023-24"
    - Player comparison (last N): "Compare Stephen Curry and LeBron James last 5 games"
    - Team comparison: "Compare Lakers and Warriors in 2023-24"
    - Team comparison (last N): "Lakers vs Warriors last 10 games"
    """
    
    query = query.strip()
    query_lower = query.lower()
    
    # Pattern for season (e.g., "2023-24", "2023-24 season")
    season_pattern = r'(\d{4}-\d{2})'
    
    # Pattern for "last N games"
    last_n_pattern = r'last\s+(\d+)\s+games?'
    
    # Extract season
    season_match = re.search(season_pattern, query)
    season = season_match.group(1) if season_match else None
    
    # Extract last_n
    last_n_match = re.search(last_n_pattern, query_lower)
    last_n = int(last_n_match.group(1)) if last_n_match else None
    
    # Player stats query - improved pattern matching
    if re.search(r'how many|what|points|rebounds|assists|stats?|average', query_lower):
        # Try multiple patterns
        patterns = [
            r'(?:did|does|is|was)\s+([A-Z][a-zA-Z\s]+?)(?:\s+(?:score|average|get|have))',
            r'([A-Z][a-zA-Z\s]+?)\s+(?:score|average|had|has)\s+(?:in|for)',
            r'([A-Z][a-zA-Z\s]+?)\s+stats?\s+(?:in|for)',
            r'([A-Z][a-zA-Z\s]+?)\s+(?:in|for)\s+(\d{4}-\d{2})',
        ]
        
        for pattern in patterns:
            player_match = re.search(pattern, query, re.IGNORECASE)
            if player_match:
                player_name = player_match.group(1).strip()
                # Extract season if in the match
                if len(player_match.groups()) > 1 and player_match.group(2):
                    extracted_season = player_match.group(2).strip()
                    if not season:
                        season = extracted_season
                return {
                    "type": "player_stats",
                    "player_name": player_name,
                    "season": season,
                    "original_query": query
                }
    
    # Player comparison - improved pattern matching
    if re.search(r'compare|vs|versus|against', query_lower):
        # Extract two player names - try multiple patterns
        patterns = [
            r'compare\s+([A-Z][a-zA-Z\s]+?)\s+and\s+([A-Z][a-zA-Z\s]+?)(?:\s+in|\s+for|$)',
            r'([A-Z][a-zA-Z\s]+?)\s+(?:vs|versus|against)\s+([A-Z][a-zA-Z\s]+?)(?:\s+in|\s+for|$)',
            r'([A-Z][a-zA-Z\s]+?)\s+and\s+([A-Z][a-zA-Z\s]+?)(?:\s+in|\s+for|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                player1 = match.group(1).strip()
                player2 = match.group(2).strip()
                
                if last_n:
                    return {
                        "type": "player_comparison_game_logs",
                        "player1": player1,
                        "player2": player2,
                        "season": season,
                        "last_n": last_n,
                        "original_query": query
                    }
                else:
                    return {
                        "type": "player_comparison",
                        "player1": player1,
                        "player2": player2,
                        "season": season,
                        "original_query": query
                    }
    
    # Team comparison
    team_keywords = ['lakers', 'warriors', 'celtics', 'heat', 'bulls', 'knicks', 'nets', 'clippers', 
                     'mavericks', 'suns', 'nuggets', 'bucks', '76ers', 'raptors', 'rockets', 'spurs',
                     'thunder', 'jazz', 'blazers', 'pelicans', 'kings', 'timberwolves', 'pistons',
                     'hornets', 'magic', 'pacers', 'wizards', 'hawks', 'cavaliers', 'grizzlies']
    
    team_found = [team for team in team_keywords if team in query_lower]
    if len(team_found) >= 2:
        # Simple team name extraction (this could be improved)
        team_match = re.search(r'compare\s+([A-Z][a-zA-Z\s]+?)\s+and\s+([A-Z][a-zA-Z\s]+?)', query, re.IGNORECASE)
        if team_match:
            team1 = team_match.group(1).strip()
            team2 = team_match.group(2).strip()
            
            if last_n:
                return {
                    "type": "team_comparison_game_logs",
                    "team1": team1,
                    "team2": team2,
                    "season": season,
                    "last_n": last_n,
                    "original_query": query
                }
            else:
                return {
                    "type": "team_comparison",
                    "team1": team1,
                    "team2": team2,
                    "season": season,
                    "include_game_logs": True,
                    "original_query": query
                }
        
        # Try "team1 vs team2" format
        vs_match = re.search(r'([A-Z][a-zA-Z\s]+?)\s+(?:vs|versus|against)\s+([A-Z][a-zA-Z\s]+?)', query, re.IGNORECASE)
        if vs_match:
            team1 = vs_match.group(1).strip()
            team2 = vs_match.group(2).strip()
            
            if last_n:
                return {
                    "type": "team_comparison_game_logs",
                    "team1": team1,
                    "team2": team2,
                    "season": season,
                    "last_n": last_n,
                    "original_query": query
                }
            else:
                return {
                    "type": "team_comparison",
                    "team1": team1,
                    "team2": team2,
                    "season": season,
                    "include_game_logs": True,
                    "original_query": query
                }
    
    # Default: return error
    return {
        "type": "error",
        "message": "Could not parse query. Please try rephrasing.",
        "original_query": query
    }

