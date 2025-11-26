"""
StatPad FastAPI Application
NBA Statistics & Analytics Platform API
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.services import queries
from app.services import nlp_query

# Create FastAPI app
app = FastAPI(
    title="StatPad API",
    description="NBA Statistics & Analytics Platform API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    type: str
    data: Dict[str, Any]
    original_query: str


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to StatPad API",
        "version": "1.0.0",
        "docs": "/docs"
    }


# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "healthy"}


# Player Stats Endpoints
@app.get("/players/{player_name}/seasons/{season}")
async def get_player_stats(player_name: str, season: str):
    """Get player stats for a specific season."""
    try:
        stats = queries.get_player_stats(player_name, season)
        if not stats:
            raise HTTPException(
                status_code=404,
                detail=f"Player stats not found for {player_name} in season {season}"
            )
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Player Comparison Endpoints
@app.get("/compare/players/{player1}/{player2}/seasons/{season}")
async def compare_players_season(player1: str, player2: str, season: str):
    """Compare two players' stats for a specific season."""
    try:
        result = queries.compare_players(player1, player2, season)
        if not result.get("player1") or not result.get("player2"):
            raise HTTPException(
                status_code=404,
                detail="One or both players not found for the specified season"
            )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/compare/players/{player1}/{player2}/game-logs/seasons/{season}")
async def get_player_game_logs_season(
    player1: str,
    player2: str,
    season: str,
    last_n: Optional[int] = Query(None, description="Get last N games")
):
    """Get head-to-head game logs for two players in a specific season."""
    try:
        game_logs = queries.get_head_to_head_game_logs(player1, player2, season, last_n)
        return {
            "player1": player1,
            "player2": player2,
            "season": season,
            "last_n": last_n,
            "game_logs": game_logs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/compare/players/{player1}/{player2}/game-logs/all-seasons")
async def get_player_game_logs_all_seasons(
    player1: str,
    player2: str,
    last_n: Optional[int] = Query(None, description="Get last N games")
):
    """Get head-to-head game logs for two players across all seasons."""
    try:
        game_logs = queries.get_head_to_head_game_logs(player1, player2, None, last_n)
        return {
            "player1": player1,
            "player2": player2,
            "last_n": last_n,
            "game_logs": game_logs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Team Comparison Endpoints
@app.get("/compare/teams/{team1}/{team2}/seasons/{season}")
async def compare_teams_season(
    team1: str,
    team2: str,
    season: str,
    include_game_logs: bool = Query(False, description="Include game logs"),
    last_n: Optional[int] = Query(None, description="Get last N games")
):
    """Compare two teams for a specific season."""
    try:
        result = queries.compare_teams(team1, team2, season, include_game_logs, last_n)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/compare/teams/{team1}/{team2}/game-logs/seasons/{season}")
async def get_team_game_logs_season(
    team1: str,
    team2: str,
    season: str,
    last_n: Optional[int] = Query(None, description="Get last N games")
):
    """Get game logs for two teams in a specific season."""
    try:
        result = queries.compare_teams(team1, team2, season, True, last_n)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return {
            "team1": team1,
            "team2": team2,
            "season": season,
            "last_n": last_n,
            "game_logs": result.get("game_logs", [])
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/compare/teams/{team1}/{team2}/game-logs/all-seasons")
async def get_team_game_logs_all_seasons(
    team1: str,
    team2: str,
    last_n: Optional[int] = Query(None, description="Get last N games")
):
    """Get game logs for two teams across all seasons."""
    try:
        # This would require modifying queries.compare_teams to handle all seasons
        # For now, return a placeholder
        raise HTTPException(
            status_code=501,
            detail="All-seasons team comparison not yet implemented"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Natural Language Query Endpoint
@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process natural language query about NBA stats."""
    try:
        # Parse query
        parsed = nlp_query.parse_query(request.query)
        
        # Route to appropriate handler
        query_type = parsed.get("type")
        data = {}
        
        if query_type == "player_stats":
            player_name = parsed.get("player_name")
            season = parsed.get("season")
            if not player_name or not season:
                raise HTTPException(
                    status_code=400,
                    detail="Player name and season are required"
                )
            stats = queries.get_player_stats(player_name, season)
            data = {"stats": stats} if stats else {"error": "Player stats not found"}
        
        elif query_type == "player_comparison":
            player1 = parsed.get("player1")
            player2 = parsed.get("player2")
            season = parsed.get("season")
            if not player1 or not player2 or not season:
                raise HTTPException(
                    status_code=400,
                    detail="Both player names and season are required"
                )
            comparison = queries.compare_players(player1, player2, season)
            data = comparison
        
        elif query_type == "player_comparison_game_logs":
            player1 = parsed.get("player1")
            player2 = parsed.get("player2")
            season = parsed.get("season")
            last_n = parsed.get("last_n")
            game_logs = queries.get_head_to_head_game_logs(player1, player2, season, last_n)
            data = {
                "player1": player1,
                "player2": player2,
                "season": season,
                "last_n": last_n,
                "game_logs": game_logs
            }
        
        elif query_type == "team_comparison":
            team1 = parsed.get("team1")
            team2 = parsed.get("team2")
            season = parsed.get("season")
            include_game_logs = parsed.get("include_game_logs", False)
            if not team1 or not team2 or not season:
                raise HTTPException(
                    status_code=400,
                    detail="Both team names and season are required"
                )
            comparison = queries.compare_teams(team1, team2, season, include_game_logs)
            data = comparison
        
        elif query_type == "team_comparison_game_logs":
            team1 = parsed.get("team1")
            team2 = parsed.get("team2")
            season = parsed.get("season")
            last_n = parsed.get("last_n")
            comparison = queries.compare_teams(team1, team2, season, True, last_n)
            data = comparison
        
        elif query_type == "error":
            raise HTTPException(
                status_code=400,
                detail=parsed.get("message", "Could not parse query")
            )
        
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown query type: {query_type}"
            )
        
        return QueryResponse(
            type=query_type,
            data=data,
            original_query=request.query
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

