#!/bin/bash
# Quick commit script - use this when you want to commit manually

# Check if there are changes
if [ -z "$(git status --porcelain)" ]; then
    echo "No changes to commit"
    exit 0
fi

# Add all changes
git add .

# Use provided message or default
COMMIT_MSG="${1:-chore: update code}"

# Commit
git commit -m "$COMMIT_MSG"

# Push if remote exists
if git remote | grep -q origin; then
    git push origin main
    echo "✅ Committed and pushed: $COMMIT_MSG"
else
    echo "✅ Committed: $COMMIT_MSG (no remote configured)"
fi

