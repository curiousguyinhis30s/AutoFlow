#!/bin/bash
# AutoFlow Installation Script
# Usage: ./install-to-project.sh /path/to/your/project

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 /path/to/your/project"
    echo "Example: $0 ~/my-webapp"
    exit 1
fi

TARGET_DIR="$1"
AUTOFLOW_SOURCE="/Users/samiullah/AutoFlow"

echo "=================================================="
echo "🚀 Installing AutoFlow to: $TARGET_DIR"
echo "=================================================="
echo ""

# Check if target directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "❌ Directory not found: $TARGET_DIR"
    exit 1
fi

# Navigate to target
cd "$TARGET_DIR"

echo "📁 Creating AutoFlow directory structure..."
mkdir -p .autoflow/agents
mkdir -p .autoflow/context-firewalls
mkdir -p .autoflow/resources
mkdir -p .autoflow/hooks
mkdir -p .github/ISSUE_TEMPLATE
mkdir -p scripts
mkdir -p worktrees

echo "✅ Directories created"
echo ""

echo "📋 Copying core files..."

# Copy orchestrator
cp "$AUTOFLOW_SOURCE/.autoflow/agents/orchestrator.py" .autoflow/agents/
echo "✓ orchestrator.py"

# Copy MCP server
cp "$AUTOFLOW_SOURCE/.autoflow/resources/mcp-server.py" .autoflow/resources/
echo "✓ mcp-server.py"

# Copy PreCompact hook
cp "$AUTOFLOW_SOURCE/.autoflow/hooks/pre-compact" .autoflow/hooks/
chmod +x .autoflow/hooks/pre-compact
echo "✓ pre-compact hook"

# Copy design system integration
cp "$AUTOFLOW_SOURCE/.autoflow/design-system-integration.py" .autoflow/
echo "✓ design-system-integration.py"

# Copy scripts
cp "$AUTOFLOW_SOURCE/scripts/worktree-create.sh" scripts/
cp "$AUTOFLOW_SOURCE/scripts/worktree-merge.sh" scripts/
chmod +x scripts/*.sh
echo "✓ worktree scripts"

# Copy GitHub Issue templates
cp "$AUTOFLOW_SOURCE/.github/ISSUE_TEMPLATE/"*.yml .github/ISSUE_TEMPLATE/ 2>/dev/null || true
echo "✓ GitHub Issue templates"

# Copy documentation
cp "$AUTOFLOW_SOURCE/QUICKSTART.md" . 2>/dev/null || true
cp "$AUTOFLOW_SOURCE/USAGE.md" . 2>/dev/null || true
echo "✓ Documentation"

echo ""
echo "=================================================="
echo "✅ AutoFlow installed successfully!"
echo "=================================================="
echo ""
echo "📖 Next steps:"
echo ""
echo "1. Ensure prerequisites:"
echo "   - Python 3.8+"
echo "   - Git 2.25+ (worktree support)"
echo "   - GitHub CLI (gh) installed and authenticated"
echo ""
echo "2. Authenticate GitHub CLI (if not done):"
echo "   gh auth login"
echo ""
echo "3. Run your first workflow:"
echo "   cd $TARGET_DIR"
echo "   python .autoflow/agents/orchestrator.py \"implement user authentication\""
echo ""
echo "4. Read the quick start guide:"
echo "   cat QUICKSTART.md"
echo ""
echo "🎉 Happy building!"
echo ""
