#  StatPad

NBA Statistics & Analytics Platform - Compare players, teams, and query stats in natural language.

## Features

-  **Player Statistics** - View individual player stats for any season (2015-16 through 2024-25)
-  **Head-to-Head Comparisons** - Compare two players with detailed game logs
-  **Team Comparisons** - Compare teams with game-by-game results
-  **Natural Language Querying** - Ask questions in plain English about NBA stats

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite3
- **Data Source**: NBA API (`nba_api` Python library)
- **Server**: Uvicorn (ASGI server)

### Frontend
- **Framework**: React 19
- **Build Tool**: Vite
- **Styling**: Tailwind CSS 3.4
- **HTTP Client**: Axios
- **Routing**: React Router DOM

##  Getting Started

### Prerequisites

- Python 3.12+
- Node.js (Latest LTS)
- pip (Python package manager)
- npm (Node package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/statpad.git
   cd statpad
   ```

2. **Set up Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up Frontend**
   ```bash
   cd frontend
   npm install
   ```

### Running the Application

1. **Start Backend Server** (Terminal 1)
   ```bash
   cd backend
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start Frontend Server** (Terminal 2)
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the Application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Database Setup

1. **Initialize Database**
   ```bash
   cd backend
   python app/database/setup.py
   ```

2. **Seed Teams** (if needed)
   ```bash
   python app/scripts/seed_teams.py
   ```

3. **Import Data** (if needed)
   ```bash
   python app/scripts/import_player_stats_csv.py
   python app/scripts/import_league_gamelogs.py
   ```

## Project Structure

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
│   │       ├── seed_teams.py
│   │       ├── import_player_stats_csv.py
│   │       └── import_league_gamelogs.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx                 # Main app component
│   │   ├── main.jsx                # React entry point
│   │   ├── index.css               # Tailwind CSS imports
│   │   ├── components/
│   │   │   ├── PlayerStats.jsx
│   │   │   ├── HeadToHeadGameLogs.jsx
│   │   │   └── NaturalLanguageQuery.jsx
│   │   └── services/
│   │       └── api.js              # API client functions
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
├── docs/
│   ├── PROJECT_SPECIFICATION.md
│   └── GITHUB_SETUP.md
└── README.md
```

## Documentation

- [Project Specification](./docs/PROJECT_SPECIFICATION.md) - Detailed project requirements
- [GitHub Setup Guide](./docs/GITHUB_SETUP.md) - Git workflow and commit guidelines

## API Endpoints

### Player Stats
- `GET /players/{player_name}/seasons/{season}` - Get player stats for a season

### Player Comparisons
- `GET /compare/players/{player1}/{player2}/seasons/{season}` - Compare two players' season stats
- `GET /compare/players/{player1}/{player2}/game-logs/seasons/{season}?last_n={N}` - Get head-to-head game logs
- `GET /compare/players/{player1}/{player2}/game-logs/all-seasons?last_n={N}` - Get game logs across all seasons

### Team Comparisons
- `GET /compare/teams/{team1}/{team2}/seasons/{season}?include_game_logs=true&last_n={N}` - Compare teams
- `GET /compare/teams/{team1}/{team2}/game-logs/seasons/{season}?last_n={N}` - Get team game logs

### Natural Language Query
- `POST /query` - Process natural language query

See API documentation at http://localhost:8000/docs for detailed endpoint information.

##  Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

##  Commit Message Guidelines

We follow conventional commit format:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

##  License

MIT License

## Acknowledgments

- NBA API data provided by [nba_api](https://github.com/swar/nba_api)
- Built with FastAPI, React, and Tailwind CSS

---



