#!/bin/bash
# AutoFlow Complete Setup Script

echo "=================================================="
echo "🚀 AutoFlow Setup"
echo "=================================================="
echo ""

cd /Users/samiullah/AutoFlow

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install anthropic --quiet 2>&1 | grep -v "already satisfied" || true
echo "✅ anthropic installed"
echo ""

# Check for API keys
echo "🔑 Checking API keys..."

if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo ""
    echo "⚠️  ANTHROPIC_API_KEY not set"
    echo ""
    echo "Add to your ~/.zshrc or ~/.bashrc:"
    echo ""
    echo "  export ANTHROPIC_API_KEY='your-key-here'"
    echo ""
    echo "Then run: source ~/.zshrc"
    echo ""
else
    echo "✅ ANTHROPIC_API_KEY found"
fi

# Check GitHub CLI
echo ""
echo "🔧 Checking GitHub CLI..."
if /opt/homebrew/bin/gh auth status &>/dev/null; then
    echo "✅ GitHub CLI authenticated"
else
    echo "⚠️  GitHub CLI not authenticated"
    echo ""
    echo "Run: /opt/homebrew/bin/gh auth login"
    echo ""
fi

echo ""
echo "=================================================="
echo "✅ Setup Complete"
echo "=================================================="
echo ""
echo "Usage:"
echo "  ./autoflow \"implement user authentication\""
echo ""
echo "Or run demo:"
echo "  ./demo.sh"
echo ""
