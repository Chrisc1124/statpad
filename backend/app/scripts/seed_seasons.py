"""
Seed NBA seasons into the database.
"""

import sqlite3
from pathlib import Path

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
DB_PATH = PROJECT_ROOT / "statpad.db"


def seed_seasons():
    """Seed seasons from 2015-16 to 2024-25."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        seasons = [
            ("2015-16", 2015, 2016, 0),
            ("2016-17", 2016, 2017, 0),
            ("2017-18", 2017, 2018, 0),
            ("2018-19", 2018, 2019, 0),
            ("2019-20", 2019, 2020, 0),
            ("2020-21", 2020, 2021, 0),
            ("2021-22", 2021, 2022, 0),
            ("2022-23", 2022, 2023, 0),
            ("2023-24", 2023, 2024, 0),
            ("2024-25", 2024, 2025, 1),  # Current season
        ]
        
        for season, start_year, end_year, is_current in seasons:
            cursor.execute("""
                INSERT OR IGNORE INTO seasons (season, start_year, end_year, is_current)
                VALUES (?, ?, ?, ?)
            """, (season, start_year, end_year, is_current))
        
        conn.commit()
        print(f"✅ Seeded {len(seasons)} seasons")
    except Exception as e:
        print(f"❌ Error seeding seasons: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    seed_seasons()

