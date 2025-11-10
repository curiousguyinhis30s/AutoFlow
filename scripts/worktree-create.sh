#!/bin/bash

# Create git worktree for parallel agent execution
# Usage: ./scripts/worktree-create.sh <branch-name> <issue-number>

set -e

BRANCH_NAME=$1
ISSUE_NUMBER=$2

if [ -z "$BRANCH_NAME" ] || [ -z "$ISSUE_NUMBER" ]; then
    echo "❌ Usage: $0 <branch-name> <issue-number>"
    echo "   Example: $0 implement-auth 123"
    exit 1
fi

WORKTREE_DIR="worktrees/${BRANCH_NAME}"

echo "🌳 Creating git worktree for parallel execution"
echo "================================================"
echo ""
echo "  Branch: ${BRANCH_NAME}"
echo "  Issue: #${ISSUE_NUMBER}"
echo "  Directory: ${WORKTREE_DIR}"
echo ""

# Check if worktree already exists
if [ -d "$WORKTREE_DIR" ]; then
    echo "❌ Worktree already exists: ${WORKTREE_DIR}"
    echo "   Remove it first: git worktree remove ${WORKTREE_DIR}"
    exit 1
fi

# Create worktree
echo "📂 Creating worktree directory..."
git worktree add "$WORKTREE_DIR" -b "$BRANCH_NAME"

# Link issue in commit message template
cat > "${WORKTREE_DIR}/.git/COMMIT_EDITMSG.template" << EOF
# Issue #${ISSUE_NUMBER}

# What changed:


# Why:


# Testing:

EOF

echo ""
echo "✅ Worktree created successfully!"
echo ""
echo "📝 Next steps:"
echo "   1. cd ${WORKTREE_DIR}"
echo "   2. # ... make your changes ..."
echo "   3. git commit -m 'Your message'"
echo "   4. cd ../.."
echo "   5. ./scripts/worktree-merge.sh ${BRANCH_NAME}"
echo ""
echo "🔗 Worktree is linked to issue #${ISSUE_NUMBER}"
