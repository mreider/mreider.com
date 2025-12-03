#!/bin/bash
# Fitness Tracker Update Script for Mac Terminal
# NOTE: This script is for Mac Terminal use only - it won't work on iOS!
# For iOS, see: IOS_SHORTCUT_SETUP.md
#
# Usage: 
#   GITHUB_TOKEN=your_token_here ./trigger_fitness_update.sh 2024-12-03 true false
#   GITHUB_TOKEN=your_token_here ./trigger_fitness_update.sh [date] [workout] [diet]

set -e

# Configuration
GITHUB_OWNER="mreider"  # Replace with your GitHub username
GITHUB_REPO="mreider.com"  # Replace with your repo name
WORKFLOW_ID="update-fitness.yml"

# Check if GitHub token is provided
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN environment variable is required"
    echo "Create a token at: https://github.com/settings/tokens"
    echo "Required scopes: repo, workflow"
    exit 1
fi

# Parse arguments (can be passed from Shortcuts)
DATE="${1:-$(date +%Y-%m-%d)}"
WORKOUT="${2:-false}"
DIET="${3:-false}"

# Validate date format
if ! [[ "$DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    echo "Error: Invalid date format. Use YYYY-MM-DD"
    exit 1
fi

# Validate boolean values
if [[ "$WORKOUT" != "true" && "$WORKOUT" != "false" ]]; then
    echo "Error: Workout must be 'true' or 'false'"
    exit 1
fi

if [[ "$DIET" != "true" && "$DIET" != "false" ]]; then
    echo "Error: Diet must be 'true' or 'false'"
    exit 1
fi

# Display what we're doing
echo "Updating fitness tracker..."
echo "Date: $DATE"
echo "Workout: $WORKOUT"
echo "Diet: $DIET"

# Trigger the GitHub Actions workflow
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "https://api.github.com/repos/$GITHUB_OWNER/$GITHUB_REPO/actions/workflows/$WORKFLOW_ID/dispatches" \
    -d "{\"ref\":\"main\",\"inputs\":{\"date\":\"$DATE\",\"workout\":\"$WORKOUT\",\"diet\":\"$DIET\"}}")

# Extract HTTP status code (last line)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

# Check if successful
if [ "$HTTP_CODE" = "204" ]; then
    echo "✅ Success! Workflow triggered."
    echo "View progress at: https://github.com/$GITHUB_OWNER/$GITHUB_REPO/actions"
    exit 0
else
    echo "❌ Failed to trigger workflow. HTTP Status: $HTTP_CODE"
    echo "$RESPONSE" | head -n-1
    exit 1
fi
