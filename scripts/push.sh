#!/bin/bash
# Quick push script for regular commits

# Get current branch
BRANCH=$(git branch --show-current)

# Check if there are changes
if [ -z "$(git status --porcelain)" ]; then
    echo "No changes to commit"
    exit 0
fi

# Add all changes
git add .

# Commit with a message (you can customize this)
COMMIT_MSG="${1:-chore: update code}"

# Commit
git commit -m "$COMMIT_MSG"

# Push to current branch
git push origin "$BRANCH"

echo "✅ Pushed to $BRANCH"

