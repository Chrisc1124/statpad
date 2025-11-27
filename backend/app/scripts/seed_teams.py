"""
Seed NBA teams into the database.
Uses nba_api to fetch team data.
"""

import sqlite3
from pathlib import Path
from nba_api.stats.static import teams

# Get database path (database is in backend directory)
# Script is in backend/app/scripts/, so parent.parent.parent is backend/
BACKEND_ROOT = Path(__file__).parent.parent.parent
DB_PATH = BACKEND_ROOT / "statpad.db"


def seed_teams():
    """Seed all NBA teams into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Get all teams from nba_api
        nba_teams = teams.get_teams()
        
        for team in nba_teams:
            cursor.execute("""
                INSERT OR IGNORE INTO teams (team_abbrev, team_name, city, conference, division, arena)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                team['abbreviation'],
                team['full_name'],
                team['city'],
                team.get('conference', None),
                team.get('division', None),
                team.get('arena_name', None)
            ))
        
        conn.commit()
        print(f"✅ Seeded {len(nba_teams)} teams")
    except Exception as e:
        print(f"❌ Error seeding teams: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    seed_teams()

