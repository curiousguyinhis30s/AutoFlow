#!/bin/bash
# AutoFlow Launcher - Starts Claude Code session for AutoFlow

cd /Users/samiullah/AutoFlow

# Check if task provided
if [ -z "$1" ]; then
    echo "Usage: ./start-autoflow.sh \"your task description\""
    echo ""
    echo "Example:"
    echo "  ./start-autoflow.sh \"build a contact form with validation\""
    echo ""
    exit 1
fi

TASK="$1"

# Create the prompt for Claude Code
PROMPT="Execute AutoFlow workflow for this task:

**Task:** $TASK

**Workflow Steps:**
1. Create GitHub Issue for tracking
2. Phase 1 (Research): Research relevant patterns and best practices
3. Phase 2 (Plan): Create implementation plan
4. Phase 3 (Implement): Build the actual code
5. Phase 4 (Validate): Test and verify
6. Phase 5 (Integrate): Commit to git and push

Execute all 5 phases and close the issue when complete.

AutoFlow Project: /Users/samiullah/AutoFlow
GitHub Repo: https://github.com/curiousguyinhis30s/AutoFlow"

echo "🚀 Starting AutoFlow with Claude Code..."
echo "📋 Task: $TASK"
echo ""

# Start Claude Code with the prompt
claude "$PROMPT"
