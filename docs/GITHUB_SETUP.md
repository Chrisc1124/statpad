# GitHub Repository Setup Guide

## Initial Setup

### 1. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `statpad` (or your preferred name)
3. Description: "NBA Statistics & Analytics Platform - Compare players, teams, and query stats in natural language"
4. Choose **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we'll add these)
6. Click "Create repository"

### 2. Initialize Git Locally

```bash
cd /Users/cc/statpad

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: StatPad NBA Statistics App

- FastAPI backend with SQLite database
- React frontend with Tailwind CSS
- Player stats, head-to-head comparisons, team comparisons
- Natural language query processing
- Game logs for seasons 2020-21 through 2024-25"
```

### 3. Connect to GitHub

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/statpad.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## .gitignore Configuration

Create/update `.gitignore` in project root:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
statpad-env/
*.egg-info/
dist/
build/

# Database
*.db
*.sqlite
*.sqlite3
statpad.db

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# Frontend build
frontend/dist/
frontend/.vite/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Environment variables
.env
.env.local
.env.*.local

# Logs
*.log
logs/
/tmp/

# Testing
.coverage
.pytest_cache/
htmlcov/

# Temporary files
*.tmp
*.temp
```

## Recommended Branch Strategy

### Main Branches
- `main` - Production-ready code
- `develop` - Development branch

### Feature Branches
- `feature/player-stats` - New player stats features
- `feature/team-comparison` - Team comparison features
- `feature/nlp-improvements` - NLP query enhancements
- `feature/ui-redesign` - UI/styling improvements
- `feature/database-optimization` - Database improvements

### Example Workflow

```bash
# Create feature branch
git checkout -b feature/ui-redesign

# Make changes, commit frequently
git add .
git commit -m "Add modern sporty design with basketball theme"

# Push feature branch
git push origin feature/ui-redesign

# Create Pull Request on GitHub
# After PR is merged, delete branch locally
git checkout main
git pull origin main
git branch -d feature/ui-redesign
```

## Commit Message Guidelines

Use clear, descriptive commit messages:

### Format
```
<type>: <subject>

<body (optional)>

<footer (optional)>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

### Examples

```bash
git commit -m "feat: Add head-to-head game logs for players

- Implement game log fetching for player vs player
- Add filtering by season
- Display game-by-game stats comparison"

git commit -m "fix: Resolve CORS issues for frontend connection

- Update CORS middleware to allow all localhost ports
- Fix axios request configuration"

git commit -m "style: Update UI with modern sporty design

- Add basketball-themed color palette
- Implement glassmorphism effects
- Add animated stat counters"
```

## GitHub Actions (Optional)

Create `.github/workflows/ci.yml` for automated testing:

```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      - name: Run tests
        run: |
          cd frontend
          npm test
```

## README.md Template

Create a comprehensive `README.md`:

```markdown
# 🏀 StatPad

NBA Statistics & Analytics Platform

## Features

- 📊 Player statistics by season
- ⚔️ Head-to-head player comparisons
- 🏆 Team comparisons with game logs
- 💬 Natural language querying
- 📈 Detailed game-by-game analysis

## Tech Stack

- **Backend**: FastAPI, SQLite, NBA API
- **Frontend**: React, Vite, Tailwind CSS

## Getting Started

See [START_SERVERS.md](./START_SERVERS.md) for detailed setup instructions.

## Project Structure

- `backend/` - FastAPI application
- `frontend/` - React application
- `statpad.db` - SQLite database

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License
```

## Regular Push Workflow

### Daily Development

```bash
# Morning: Pull latest changes
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/your-feature

# Work on feature, commit frequently
git add .
git commit -m "feat: Description of changes"

# Push to GitHub
git push origin feature/your-feature

# End of day: Push all work
git push origin feature/your-feature
```

### Weekly Review

```bash
# Review all commits
git log --oneline --graph --all

# Clean up merged branches
git branch -d feature/old-feature

# Update main branch
git checkout main
git pull origin main
```

## Tags for Releases

```bash
# Create a release tag
git tag -a v1.0.0 -m "Initial release: MVP features complete"
git push origin v1.0.0

# List tags
git tag

# Delete tag (if needed)
git tag -d v1.0.0
git push origin --delete v1.0.0
```

## Collaboration Tips

1. **Pull before push**: Always pull latest changes before pushing
2. **Small commits**: Commit frequently with clear messages
3. **Branch protection**: Protect `main` branch (require PR reviews)
4. **Issue tracking**: Use GitHub Issues for bugs and features
5. **Project board**: Use GitHub Projects for task management

## Useful Git Commands

```bash
# See what changed
git status
git diff

# Undo changes
git checkout -- <file>  # Discard changes
git reset HEAD <file>   # Unstage file

# View history
git log --oneline --graph
git log --all --decorate --oneline --graph

# Stash changes (temporary save)
git stash
git stash pop

# Create alias for common commands
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
```

---

Happy coding! 🚀


