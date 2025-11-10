#!/bin/bash
set -e

# AutoFlow Demo Script
# Demonstrates the complete 5-phase workflow

echo "=================================================="
echo "🚀 AutoFlow - Git-Native Workflow System Demo"
echo "=================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo "📋 Checking prerequisites..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi
echo "✅ Python: $(python3 --version)"

# Check Git
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install Git 2.25+"
    exit 1
fi
echo "✅ Git: $(git --version)"

# Check GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI not found. Please install: brew install gh"
    exit 1
fi
echo "✅ GitHub CLI: $(gh --version | head -1)"

echo ""
echo "=================================================="
echo "📁 Demo: Directory Structure"
echo "=================================================="
echo ""

echo "AutoFlow uses this structure:"
echo ""
echo "your-project/"
echo "├── .autoflow/"
echo "│   ├── agents/                  # Orchestrator + agents"
echo "│   ├── context-firewalls/       # 90% token reduction"
echo "│   ├── resources/               # MCP resources"
echo "│   └── hooks/                   # PreCompact hook"
echo "├── .github/ISSUE_TEMPLATE/      # GitHub Issue templates"
echo "├── worktrees/                   # Parallel execution"
echo "└── scripts/                     # Worktree management"
echo ""

read -p "Press Enter to continue..."

echo ""
echo "=================================================="
echo "🔍 Demo 1: Context Firewalls (90% Token Reduction)"
echo "=================================================="
echo ""

echo "Problem: Agent outputs 20,000 tokens → token explosion"
echo "Solution: Save full output to file, pass only summary"
echo ""

echo "Creating demo context firewall..."
mkdir -p .autoflow/context-firewalls

cat > .autoflow/context-firewalls/demo-research-20250110.md << 'EOF'
# Research: User Authentication

## Knowledge Base Results (5 found)

- JWT with Passport.js (relevance: 0.95)
  - Most popular Node.js authentication pattern
  - Supports multiple strategies (local, Google, GitHub)
  - Well-documented, battle-tested

- OAuth 2.0 with Auth0 (relevance: 0.89)
  - Managed authentication service
  - Reduces implementation complexity
  - Costs: Free tier available

- Session-based authentication (relevance: 0.82)
  - Traditional approach
  - Server-side session storage
  - Works with Redis for scaling

[... 15,000 more lines of detailed research ...]
EOF

echo "✅ Full research saved: .autoflow/context-firewalls/demo-research-20250110.md"
echo "   Size: $(wc -l < .autoflow/context-firewalls/demo-research-20250110.md) lines (≈20,000 tokens)"
echo ""

echo "Creating summary (90% reduction)..."
cat > .autoflow/context-firewalls/demo-research-summary.md << 'EOF'
SUMMARY (3 key patterns):

- JWT + Passport.js recommended (most popular, well-tested)
- OAuth 2.0 considered (managed service, reduces complexity)
- Session-based ruled out (scaling complexity)

RECOMMENDATION: Proceed with JWT + Passport.js approach

FULL DOCUMENT: .autoflow/context-firewalls/demo-research-20250110.md
EOF

echo "✅ Summary created: .autoflow/context-firewalls/demo-research-summary.md"
echo "   Size: $(wc -l < .autoflow/context-firewalls/demo-research-summary.md) lines (≈2,000 tokens)"
echo ""

FULL_SIZE=$(wc -l < .autoflow/context-firewalls/demo-research-20250110.md)
SUMMARY_SIZE=$(wc -l < .autoflow/context-firewalls/demo-research-summary.md)
REDUCTION=$((100 - (SUMMARY_SIZE * 100 / FULL_SIZE)))

echo "📊 Token Reduction: ${REDUCTION}%"
echo ""

read -p "Press Enter to continue..."

echo ""
echo "=================================================="
echo "🌲 Demo 2: Git Worktrees (Parallel Execution)"
echo "=================================================="
echo ""

echo "Problem: Agents on same branch → merge conflicts"
echo "Solution: Each agent gets isolated git worktree"
echo ""

# Create worktrees directory
mkdir -p worktrees

echo "Creating demo worktrees..."
echo ""

# Check if we're in a git repo
if [ ! -d .git ]; then
    echo "Not in a git repo. Initializing..."
    git init
    git config user.name "AutoFlow Demo"
    git config user.email "demo@autoflow.dev"
    echo "# AutoFlow Demo" > README.md
    git add README.md
    git commit -m "Initial commit"
    git branch -M main
fi

# Create first worktree
if [ ! -d worktrees/implement-auth ]; then
    echo "Creating worktree: implement-auth"
    git worktree add worktrees/implement-auth -b implement-auth 2>/dev/null || true
    echo "✅ Agent 1 workspace: worktrees/implement-auth/"
fi

# Create second worktree
if [ ! -d worktrees/implement-api ]; then
    echo "Creating worktree: implement-api"
    git worktree add worktrees/implement-api -b implement-api 2>/dev/null || true
    echo "✅ Agent 2 workspace: worktrees/implement-api/"
fi

echo ""
echo "Current worktrees:"
git worktree list
echo ""

echo "Both agents can now work in parallel without conflicts!"
echo ""

read -p "Press Enter to continue..."

echo ""
echo "=================================================="
echo "📝 Demo 3: GitHub Issues (Git-Native Tasks)"
echo "=================================================="
echo ""

echo "Problem: External task database (PostgreSQL) → complexity"
echo "Solution: GitHub Issues with labels"
echo ""

echo "Example GitHub Issue workflow:"
echo ""
echo "1. Create research issue:"
echo "   ${BLUE}gh issue create --title '[RESEARCH] User auth' --label 'phase:research'${NC}"
echo ""
echo "2. Add comment with summary:"
echo "   ${BLUE}gh issue comment 42 --body 'Research complete. Found 5 patterns.'${NC}"
echo ""
echo "3. Close issue:"
echo "   ${BLUE}gh issue close 42${NC}"
echo ""
echo "4. List issues:"
echo "   ${BLUE}gh issue list --label 'phase:research'${NC}"
echo ""

read -p "Press Enter to continue..."

echo ""
echo "=================================================="
echo "🚦 Demo 4: Human Checkpoints (Control)"
echo "=================================================="
echo ""

echo "Problem: Agents make wrong decisions → wasted work"
echo "Solution: 4 human approval checkpoints"
echo ""

echo "Checkpoint 1: After Research"
echo "────────────────────────────────────────"
echo "Summary:"
echo "  - Found 5 authentication patterns"
echo "  - JWT + Passport.js recommended"
echo "  - Estimated: 4 hours implementation"
echo ""
echo -n "❓ Approve research direction? [yes/no]: "
read -t 5 APPROVAL1 || APPROVAL1="yes"
echo "$APPROVAL1"

if [ "$APPROVAL1" != "yes" ] && [ "$APPROVAL1" != "y" ]; then
    echo "❌ Research not approved. Workflow stopped."
    exit 1
fi

echo "✅ Approved! Continuing to planning..."
echo ""

echo "Checkpoint 2: After Planning"
echo "────────────────────────────────────────"
echo "Summary:"
echo "  - 6 tasks identified"
echo "  - 13 hours estimated"
echo "  - Medium complexity"
echo ""
echo -n "❓ Approve implementation plan? [yes/no]: "
read -t 5 APPROVAL2 || APPROVAL2="yes"
echo "$APPROVAL2"

if [ "$APPROVAL2" != "yes" ] && [ "$APPROVAL2" != "y" ]; then
    echo "❌ Plan not approved. Workflow stopped."
    exit 1
fi

echo "✅ Approved! Continuing to implementation..."
echo ""

echo "Checkpoint 3: After Implementation"
echo "────────────────────────────────────────"
echo "Summary:"
echo "  - 4 files created"
echo "  - 4 commits made"
echo "  - Tests added"
echo ""
echo -n "❓ Approve code for testing? [yes/no]: "
read -t 5 APPROVAL3 || APPROVAL3="yes"
echo "$APPROVAL3"

if [ "$APPROVAL3" != "yes" ] && [ "$APPROVAL3" != "y" ]; then
    echo "❌ Code not approved. Workflow stopped."
    exit 1
fi

echo "✅ Approved! Continuing to validation..."
echo ""

echo "Checkpoint 4: After Validation"
echo "────────────────────────────────────────"
echo "Summary:"
echo "  ✅ 15/15 tests passed"
echo "  ✅ 85% coverage"
echo "  ✅ 0 security vulnerabilities"
echo ""
echo -n "❓ Approve deployment to main? [yes/no]: "
read -t 5 APPROVAL4 || APPROVAL4="yes"
echo "$APPROVAL4"

if [ "$APPROVAL4" != "yes" ] && [ "$APPROVAL4" != "y" ]; then
    echo "❌ Deployment not approved. Workflow stopped."
    exit 1
fi

echo "✅ Approved! Merging to main..."
echo ""

read -p "Press Enter to continue..."

echo ""
echo "=================================================="
echo "📚 Demo 5: MCP Resources (Reusable Templates)"
echo "=================================================="
echo ""

echo "Problem: Agents need instructions, not just data"
echo "Solution: MCP resources with templates"
echo ""

echo "Available resources:"
echo "  - ${BLUE}workflow://overview${NC}     → Complete workflow guide"
echo "  - ${BLUE}task://template/feature${NC} → Feature template"
echo "  - ${BLUE}checkpoint://pre-merge${NC}  → Pre-merge checklist"
echo ""

echo "Example: Reading workflow resource..."
echo ""
python3 .autoflow/resources/mcp-server.py 2>/dev/null | head -30 || echo "MCP server demo"
echo ""

read -p "Press Enter to continue..."

echo ""
echo "=================================================="
echo "🎨 Demo 6: Design System Integration (UI Tasks)"
echo "=================================================="
echo ""

echo "Problem: UI hallucination (inconsistent spacing, colors)"
echo "Solution: Load complete design system"
echo ""

echo "For UI tasks, AutoFlow loads:"
echo "  - ${GREEN}design-tokens.ts${NC}     → Spacing, colors, typography"
echo "  - ${GREEN}components-guide.md${NC}  → Decision tree"
echo "  - ${GREEN}responsive-rules.md${NC}  → Mobile-first patterns"
echo "  - ${GREEN}accessibility.md${NC}     → WCAG 2.1 AA standards"
echo "  - ${GREEN}anti-patterns.md${NC}     → What NOT to do"
echo ""

echo "Result: Perfect UI on first try. No rework!"
echo ""

read -p "Press Enter to continue..."

echo ""
echo "=================================================="
echo "✅ Demo Complete!"
echo "=================================================="
echo ""

echo "Summary of what you learned:"
echo ""
echo "1. ${GREEN}Context Firewalls${NC}    → 90% token reduction"
echo "2. ${GREEN}Git Worktrees${NC}        → Parallel execution"
echo "3. ${GREEN}GitHub Issues${NC}        → Git-native tasks"
echo "4. ${GREEN}Human Checkpoints${NC}    → Control at critical points"
echo "5. ${GREEN}MCP Resources${NC}        → Reusable templates"
echo "6. ${GREEN}Design System${NC}        → No UI hallucination"
echo ""

echo "Next steps:"
echo ""
echo "1. Run your first workflow:"
echo "   ${BLUE}python .autoflow/agents/orchestrator.py 'implement user authentication'${NC}"
echo ""
echo "2. Read detailed guides:"
echo "   - ${BLUE}cat QUICKSTART.md${NC}       (5-minute start)"
echo "   - ${BLUE}cat GETTING_STARTED.md${NC}  (detailed guide)"
echo "   - ${BLUE}cat README.md${NC}           (architecture)"
echo ""

echo "Cleanup demo files? [y/n]"
read -t 10 CLEANUP || CLEANUP="n"

if [ "$CLEANUP" = "y" ] || [ "$CLEANUP" = "yes" ]; then
    echo ""
    echo "Cleaning up demo files..."

    # Remove demo worktrees
    if [ -d worktrees/implement-auth ]; then
        git worktree remove worktrees/implement-auth --force 2>/dev/null || true
        git branch -D implement-auth 2>/dev/null || true
    fi

    if [ -d worktrees/implement-api ]; then
        git worktree remove worktrees/implement-api --force 2>/dev/null || true
        git branch -D implement-api 2>/dev/null || true
    fi

    # Remove demo context firewalls
    rm -f .autoflow/context-firewalls/demo-*.md

    echo "✅ Cleanup complete!"
fi

echo ""
echo "=================================================="
echo "🎉 Thank you for trying AutoFlow!"
echo "=================================================="
echo ""
