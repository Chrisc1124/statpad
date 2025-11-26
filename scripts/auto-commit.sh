#!/bin/bash
# Auto-commit script - runs in background and commits changes periodically

INTERVAL=${1:-1800}  # Default: 30 minutes (1800 seconds)

echo "Starting auto-commit every $INTERVAL seconds..."
echo "Press Ctrl+C to stop"

while true; do
    sleep $INTERVAL
    
    # Check if there are changes
    if [ -n "$(git status --porcelain)" ]; then
        echo "[$(date)] Changes detected, committing..."
        
        # Add all changes
        git add .
        
        # Generate a simple commit message
        COMMIT_MSG="chore: update code - $(date +'%Y-%m-%d %H:%M:%S')"
        
        # Commit
        git commit -m "$COMMIT_MSG" 2>/dev/null
        
        # Push if remote exists
        if git remote | grep -q origin; then
            git push origin main 2>/dev/null && echo "[$(date)] Pushed to remote" || echo "[$(date)] Push failed (might need to pull first)"
        fi
    else
        echo "[$(date)] No changes to commit"
    fi
done

