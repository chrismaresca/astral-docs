#!/bin/bash
# -------------------------------------------------------------------------------- #
# push-to-branch.sh - Script to easily commit and push changes to specified branch
# -------------------------------------------------------------------------------- #

# Get current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)
COMMIT_MSG=${1:-""}

# Validate that we're on either dev or main
if [ "$BRANCH" != "dev" ] && [ "$BRANCH" != "main" ]; then
    echo "Error: This script can only be used when on 'dev' or 'main' branches."
    echo "You are currently on: $BRANCH"
    echo "Please checkout either 'dev' or 'main' first."
    exit 1
fi

# Add all changes
git add .

# Prompt for commit message if not provided as argument
if [ -z "$COMMIT_MSG" ]; then
    echo "Enter commit message:"
    read COMMIT_MSG
    COMMIT_MSG=${COMMIT_MSG:-"Update documentation"}
fi

git commit -m "$COMMIT_MSG"

# Push changes to remote
git push origin $BRANCH

# Check if GitHub CLI is installed
if command -v gh &> /dev/null; then
    # Wait for CI/CD to complete (requires GitHub CLI)
    echo "Waiting for CI/CD workflow to complete on $BRANCH branch..."
    
    REPO="chrismaresca/astral-docs"
    WORKFLOW_NAME="Pepare Documentation"
    
    # Add a delay to allow the workflow to register
    echo "Waiting 10 seconds for workflow to register..."
    sleep 10
    
    # Get the latest run ID for the workflow on the specified branch.
    RUN_ID=$(gh run list --repo "$REPO" --workflow "$WORKFLOW_NAME" --branch "$BRANCH" --limit 1 --json databaseId -q ".[0].databaseId")
    
    if [ -z "$RUN_ID" ]; then
        echo "No workflow run found for '$WORKFLOW_NAME' on branch $BRANCH"
        echo "This could be due to a workflow name mismatch or delay in GitHub registering the run."
        echo "Proceeding without waiting for workflow completion."
    else
        echo "Watching workflow run ID: $RUN_ID"
        gh run watch "$RUN_ID" --repo "$REPO"
    fi
else
    echo "GitHub CLI (gh) not found. Install it to track workflow progress."
    echo "Visit https://cli.github.com/ for installation instructions."
    echo "Proceeding without waiting for workflow completion."
fi

# After the push, make sure we have the latest version
echo "Ensuring we have the latest version of $BRANCH..."

# Pull any changes made by CI/CD
git pull --rebase origin $BRANCH

# Make sure we have the absolute latest version to avoid conflicts with component replacement
git fetch origin $BRANCH
git reset --hard origin/$BRANCH

echo "Changes successfully pushed to $BRANCH branch and latest changes incorporated!"
echo "You now have the most up-to-date version of the $BRANCH branch."
