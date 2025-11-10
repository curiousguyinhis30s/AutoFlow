#!/bin/bash

# Merge worktree back to main branch
# Usage: ./scripts/worktree-merge.sh <branch-name>

set -e

BRANCH_NAME=$1

if [ -z "$BRANCH_NAME" ]; then
    echo "❌ Usage: $0 <branch-name>"
    echo "   Example: $0 implement-auth"
    exit 1
fi

WORKTREE_DIR="worktrees/${BRANCH_NAME}"

if [ ! -d "$WORKTREE_DIR" ]; then
    echo "❌ Worktree not found: ${WORKTREE_DIR}"
    exit 1
fi

echo "🔄 Merging worktree to main branch"
echo "===================================="
echo ""
echo "  Branch: ${BRANCH_NAME}"
echo "  Directory: ${WORKTREE_DIR}"
echo ""

# Check if there are uncommitted changes
cd "$WORKTREE_DIR"
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ Uncommitted changes in worktree!"
    echo "   Commit or stash changes first."
    cd ../..
    exit 1
fi
cd ../..

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)

# Checkout main if not already there
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "📌 Switching to main branch..."
    git checkout main
fi

# Merge the worktree branch
echo "🔀 Merging ${BRANCH_NAME} into main..."
git merge --no-ff "$BRANCH_NAME" -m "Merge ${BRANCH_NAME}"

# Remove worktree
echo "🗑️  Removing worktree..."
git worktree remove "$WORKTREE_DIR"

# Delete branch
echo "🗑️  Deleting branch..."
git branch -d "$BRANCH_NAME"

echo ""
echo "✅ Merge complete!"
echo ""
echo "📊 Summary:"
git log --oneline -5
echo ""
echo "🚀 Next steps:"
echo "   1. Push to remote: git push origin main"
echo "   2. Close related GitHub issue"
