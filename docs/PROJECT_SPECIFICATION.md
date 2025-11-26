# StatPad - NBA Statistics Application

## 📋 Project Overview

**StatPad** is a full-stack web application for querying and comparing NBA player and team statistics. It's similar to StatMuse but focused on providing detailed head-to-head comparisons, game logs, and natural language querying capabilities.

### Core Concept
A modern, interactive platform where users can:
- Search individual player statistics by season
- Compare two players head-to-head with detailed game logs
- Compare teams with game-by-game results
- Ask questions in natural language about NBA stats

---

## 🎯 Core Features

### 1. **Player Statistics**
- View individual player stats for any season (2015-16 through 2024-25)
- Displays comprehensive stats including:
  - Points, rebounds, assists per game
  - Shooting percentages (FG%, 3PT%, FT%)
  - Advanced stats (steals, blocks, turnovers, plus/minus)
  - Games played, wins/losses
  - Team affiliation

### 2. **Head-to-Head Player Comparisons**
- Compare two players' season averages side-by-side
- View detailed game logs where both players faced each other
- Shows game-by-game stats when players were on opposing teams
- Filter by season (2020-21 through 2024-25 for game logs)
- "Last N games" functionality across all seasons

### 3. **Team Comparisons**
- Compare two teams' aggregate statistics for a season
- View game-by-game results when teams played each other
- Shows team totals (points, rebounds, assists, etc.) per game
- Win/loss indicators
- "Last N games" functionality across all seasons

### 4. **Natural Language Querying**
- Ask questions in plain English about NBA stats
- Supported query types:
  - **Player Stats**: "How many points did Stephen Curry score in 2023-24?"
  - **Player Comparison**: "Compare Stephen Curry and LeBron James in 2023-24"
  - **Player Comparison (Last N)**: "Compare Stephen Curry and LeBron James last 5 games"
  - **Team Comparison**: "Compare Lakers and Warriors in 2023-24"
  - **Team Comparison (Last N)**: "Lakers vs Warriors last 10 games"
- Handles variations in player/team name formatting
- Returns structured data with game logs when applicable

---

## 🗄️ Database Schema

### Tables

#### **teams**
- `team_id` (PRIMARY KEY)
- `team_abbrev` (UNIQUE) - e.g., "LAL", "GSW"
- `team_name` - e.g., "Los Angeles Lakers"
- `conference` - Eastern/Western
- `division` - Atlantic, Pacific, etc.
- `city` - City name
- `arena` - Arena name

#### **players**
- `player_id` (PRIMARY KEY)
- `name` - Full player name
- `team_id` (FOREIGN KEY) - Current team
- `position` - PG, SG, SF, PF, C
- `age` - Player age
- `height` - Height in feet/inches
- `weight` - Weight in pounds
- `college` - College attended
- `draft_year` - Year drafted
- `draft_pick` - Draft position

#### **seasons**
- `season_id` (PRIMARY KEY)
- `season` (UNIQUE) - Format: "2023-24"
- `start_year` - 2023
- `end_year` - 2024
- `is_current` - Boolean flag for current season

#### **player_stats** (Season-level aggregates)
- `stat_id` (PRIMARY KEY)
- `player_id` (FOREIGN KEY)
- `season_id` (FOREIGN KEY)
- `team_id` (FOREIGN KEY)
- `games_played`, `wins`, `losses`
- `minutes_per_game`, `points_per_game`
- `field_goals_made`, `field_goals_attempted`, `field_goal_percentage`
- `three_pointers_made`, `three_pointers_attempted`, `three_point_percentage`
- `free_throws_made`, `free_throws_attempted`, `free_throw_percentage`
- `offensive_rebounds`, `defensive_rebounds`, `total_rebounds`
- `assists`, `turnovers`, `steals`, `blocks`
- `personal_fouls`, `fantasy_points`
- `double_doubles`, `triple_doubles`
- `plus_minus`, `true_shooting_percentage`
- UNIQUE constraint on (player_id, season_id)

#### **games**
- `game_id` (PRIMARY KEY)
- `season_id` (FOREIGN KEY)
- `game_date` - DATE format
- `home_team_id` (FOREIGN KEY)
- `away_team_id` (FOREIGN KEY)
- `home_score` - Final score
- `away_score` - Final score
- `home_win` - Boolean
- `game_type` - "Regular Season" or "Playoffs"

#### **game_stats** (Individual game stats per player)
- `game_stat_id` (PRIMARY KEY)
- `game_id` (FOREIGN KEY)
- `player_id` (FOREIGN KEY)
- `team_id` (FOREIGN KEY)
- `minutes_played`
- `points`, `field_goals_made`, `field_goals_attempted`
- `three_pointers_made`, `three_pointers_attempted`
- `free_throws_made`, `free_throws_attempted`
- `offensive_rebounds`, `defensive_rebounds`, `total_rebounds`
- `assists`, `turnovers`, `steals`, `blocks`
- `personal_fouls`, `plus_minus`

---

## 🔌 API Endpoints

### Base URL
`http://localhost:8000` (development)

### Endpoints

#### **Teams**
- `GET /teams` - Get all teams
- `POST /teams` - Add a team (team_abbrev, team_name)
- `DELETE /teams` - Delete a team (team_id)

#### **Player Stats**
- `GET /players/{player_name}/seasons/{season}` - Get player stats for a season
  - Example: `/players/Stephen%20Curry/seasons/2023-24`

#### **Player Comparisons**
- `GET /compare/players/{player1}/{player2}/seasons/{season}` - Compare two players' season stats
- `GET /compare/players/{player1}/{player2}/game-logs/seasons/{season}?last_n={N}` - Get head-to-head game logs for a season
- `GET /compare/players/{player1}/{player2}/game-logs/all-seasons?last_n={N}` - Get head-to-head game logs across all seasons

#### **Team Comparisons**
- `GET /compare/teams/{team1}/{team2}/seasons/{season}?include_game_logs=true&last_n={N}` - Compare teams with optional game logs
- `GET /compare/teams/{team1}/{team2}/game-logs/seasons/{season}?last_n={N}` - Get team game logs for a season
- `GET /compare/teams/{team1}/{team2}/game-logs/all-seasons?last_n={N}` - Get team game logs across all seasons

#### **Natural Language Query**
- `POST /query` - Process natural language query
  - Body: `{"query": "Compare Stephen Curry and LeBron James in 2023-24"}`
  - Returns structured data with query type, results, and game logs

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite3
- **Data Source**: NBA API (`nba_api` Python library)
- **Server**: Uvicorn (ASGI server)
- **CORS**: Configured for localhost development

### Frontend
- **Framework**: React 19
- **Build Tool**: Vite
- **Styling**: Tailwind CSS 3.4
- **HTTP Client**: Axios
- **Routing**: React Router DOM

### Development Tools
- **Python**: 3.12+
- **Node.js**: Latest LTS
- **Package Managers**: pip (Python), npm (Node)

---

## 📁 Project Structure

```
statpad/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app and routes
│   │   ├── database/
│   │   │   ├── setup.py            # Database initialization
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   ├── queries.py          # Database query functions
│   │   │   └── nlp_query.py        # Natural language processing
│   │   └── scripts/
│   │       ├── import_player_stats_csv.py
│   │       ├── import_league_gamelogs.py
│   │       └── backfill_season_aggregates_api.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx                 # Main app component
│   │   ├── main.jsx               # React entry point
│   │   ├── index.css              # Tailwind CSS imports
│   │   ├── components/
│   │   │   ├── PlayerStats.jsx
│   │   │   ├── HeadToHeadGameLogs.jsx
│   │   │   └── NaturalLanguageQuery.jsx
│   │   └── services/
│   │       └── api.js              # API client functions
│   ├── package.json
│   ├── tailwind.config.js
│   └── postcss.config.js
├── statpad.db                      # SQLite database
└── README.md
```

---

## 📊 Data Sources & Ingestion

### Data Sources
1. **NBA API** (`nba_api` Python library)
   - Player season stats: `leaguedashplayerstats`
   - Game logs: `leaguegamelog` (player and team)
   - Supports regular season and playoffs

2. **CSV Files** (optional, for historical data)
   - Player stats CSV files for seasons 2020-2025

### Data Ingestion Scripts
1. **`import_player_stats_csv.py`** - Import player stats from CSV
2. **`import_league_gamelogs.py`** - Import game logs from NBA API
3. **`backfill_season_aggregates_api.py`** - Backfill season stats from NBA API

### Supported Seasons
- **Player Stats**: 2015-16 through 2024-25
- **Game Logs**: 2020-21 through 2024-25 (most complete)
- **Playoffs**: Supported for seasons with playoff data

---

## 🎨 Current UI Features

### Design System
- **Color Scheme**: Blue/purple gradients, gray backgrounds
- **Typography**: System fonts (San Francisco, Segoe UI, etc.)
- **Components**: Cards, buttons, inputs with Tailwind CSS
- **Animations**: Fade-in, slide-up transitions
- **Responsive**: Mobile-friendly grid layouts

### Main Views
1. **Player Stats Tab**
   - Search form (player name + season)
   - Stat cards with key metrics
   - Detailed stats tables

2. **Head-to-Head Tab**
   - Two-player input form
   - Season selector
   - Game-by-game comparison cards

3. **Ask Question Tab**
   - Natural language input
   - Example queries
   - Results display with game logs

---

## 🚀 Future Enhancements & Modern Sporty Design Ideas

### Design Improvements
1. **Sporty Theme**
   - Basketball court-inspired color scheme (orange, wood brown, court green)
   - Team color accents based on selected teams
   - Animated basketball icons
   - Scoreboard-style stat displays
   - Jersey number styling for player cards

2. **Modern UI Elements**
   - Glassmorphism effects
   - Smooth micro-interactions
   - Loading skeletons
   - Toast notifications
   - Dark mode support
   - Animated stat counters
   - Interactive charts/graphs

3. **Enhanced Visualizations**
   - Player comparison charts (bar charts, radar charts)
   - Game log timeline visualization
   - Shot chart visualization (if data available)
   - Win/loss streak indicators
   - Performance trends over time

### Feature Additions
1. **Advanced Filtering**
   - Filter by date range
   - Filter by game type (regular season, playoffs)
   - Filter by team
   - Filter by stat thresholds

2. **Player Profiles**
   - Career stats overview
   - Season-by-season comparison
   - Team history
   - Awards and achievements

3. **Team Pages**
   - Roster view
   - Team stats dashboard
   - Schedule/results
   - Team vs team history

4. **Search Improvements**
   - Autocomplete for player/team names
   - Search history
   - Favorite players/teams
   - Recent searches

5. **Data Export**
   - Export stats to CSV
   - Shareable links for comparisons
   - Print-friendly views

6. **Performance Optimizations**
   - Caching frequently accessed data
   - Pagination for large result sets
   - Lazy loading for game logs
   - Optimistic UI updates

---

## 📝 Development Workflow

### Setup
1. **Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```

2. **Frontend**
   ```bash
   cd frontend
   npm install
   ```

### Running
1. **Backend** (Terminal 1)
   ```bash
   source venv/bin/activate
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Frontend** (Terminal 2)
   ```bash
   cd frontend
   npm run dev
   ```

### Database Setup
1. Initialize database: `python backend/app/database/setup.py`
2. Seed teams: `python backend/app/scripts/seed_teams.py`
3. Import player stats: `python backend/app/scripts/import_player_stats_csv.py`
4. Import game logs: `python backend/app/scripts/import_league_gamelogs.py`

---

## 🔐 Environment & Configuration

### Backend Configuration
- Database file: `statpad.db` (SQLite, project root)
- CORS: Configured for localhost development
- API port: 8000

### Frontend Configuration
- API URL: `http://localhost:8000` (configurable in `src/services/api.js`)
- Dev server port: 5173 (Vite default, auto-increments if taken)
- Tailwind: Configured with custom theme

---

## 📦 Key Dependencies

### Backend (`requirements.txt`)
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `nba_api` - NBA data API client
- `pydantic` - Data validation

### Frontend (`package.json`)
- `react` - UI library
- `react-dom` - React DOM bindings
- `react-router-dom` - Routing
- `axios` - HTTP client
- `tailwindcss` - CSS framework
- `vite` - Build tool

---

## 🎯 MVP Features (Minimum Viable Product)

For starting from scratch, prioritize:

1. ✅ **Player Stats Search** - Basic player stats by season
2. ✅ **Player Comparison** - Compare two players' season stats
3. ✅ **Head-to-Head Game Logs** - Game-by-game player comparisons
4. ✅ **Team Comparison** - Compare two teams
5. ✅ **Natural Language Query** - Basic NLP for player/team queries
6. ✅ **Responsive Design** - Mobile-friendly layout

---

## 🏀 Sporty Design Inspiration

### Color Palette Ideas
- **Primary**: Orange (#FF8C00) - Basketball color
- **Secondary**: Deep Blue (#003366) - Court lines
- **Accent**: Red (#DC143C) - Scoreboard red
- **Background**: Off-white (#F5F5F5) - Court color
- **Text**: Dark Gray (#1a1a1a)

### Visual Elements
- Basketball texture backgrounds
- Court line patterns as dividers
- Scoreboard-style stat displays
- Jersey number badges
- Team logo placeholders
- Animated stat counters
- Win/loss indicators with team colors

### Typography
- Bold, sporty fonts for headers
- Condensed fonts for stats
- Number fonts (like scoreboards)
- Clear hierarchy for readability

---

## 📚 Documentation Files

- `START_SERVERS.md` - How to run backend/frontend
- `NLP_QUERY_GUIDE.md` - Natural language query examples
- `TROUBLESHOOTING.md` - Common issues and solutions
- `FRONTEND_FILES_EXPLAINED.md` - Frontend component explanations

---

## 🎓 Learning Resources

### FastAPI
- Official docs: https://fastapi.tiangolo.com
- SQLite with FastAPI: https://fastapi.tiangolo.com/tutorial/sql-databases/

### React
- Official docs: https://react.dev
- React Hooks: https://react.dev/reference/react

### Tailwind CSS
- Official docs: https://tailwindcss.com
- Tailwind UI: https://tailwindui.com (for component inspiration)

### NBA API
- nba_api docs: https://github.com/swar/nba_api
- API endpoints: https://github.com/swar/nba_api/blob/master/docs/table_of_contents.md

---

## 🚦 Getting Started Checklist

When starting fresh:

- [ ] Set up GitHub repository
- [ ] Initialize backend (FastAPI + SQLite)
- [ ] Initialize frontend (React + Vite + Tailwind)
- [ ] Set up database schema
- [ ] Create data ingestion scripts
- [ ] Build API endpoints
- [ ] Create frontend components
- [ ] Implement natural language querying
- [ ] Add modern sporty styling
- [ ] Test all features
- [ ] Deploy (optional)

---

## 📝 Notes for Fresh Start

1. **Database**: Start with SQLite for simplicity, can migrate to PostgreSQL later
2. **API**: Use FastAPI for automatic docs and type validation
3. **Styling**: Use Tailwind CSS for rapid development
4. **Data**: NBA API is free but has rate limits; consider caching
5. **NLP**: Start simple with regex patterns, can upgrade to ML later
6. **Deployment**: Consider Vercel (frontend) + Railway/Render (backend)

---

This specification provides everything needed to rebuild StatPad from scratch with a modern, sporty design! 🏀


