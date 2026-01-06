#!/bin/bash

# Install Claude Code Review Git Hooks
# Run this in any git repository to enable pre-push code review

set -e

CLAUDE_DIR="$HOME/.claude"
HOOKS_DIR="$CLAUDE_DIR/hooks"

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

echo ""
echo "🔧 Claude Code Review - Git Hook Installer"
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ Error: Not a git repository${NC}"
    echo "   Run this command from a git project root."
    exit 1
fi

# Check if hooks exist
if [ ! -d "$HOOKS_DIR" ]; then
    echo -e "${RED}❌ Error: Hook templates not found${NC}"
    echo "   Run ~/.claude-bootstrap/install.sh first."
    exit 1
fi

# Check for existing pre-push hook
if [ -f ".git/hooks/pre-push" ]; then
    echo -e "${YELLOW}⚠️  Existing pre-push hook found${NC}"
    read -p "   Overwrite? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "   Skipped. Existing hook preserved."
        exit 0
    fi
fi

# Install pre-push hook
cp "$HOOKS_DIR/pre-push" ".git/hooks/pre-push"
chmod +x ".git/hooks/pre-push"

echo -e "${GREEN}✅ Pre-push hook installed${NC}"
echo ""
echo "What happens now:"
echo "  • Every 'git push' runs Claude code review"
echo "  • 🔴 Critical or 🟠 High issues block the push"
echo "  • 🟡 Medium and 🟢 Low issues are advisory only"
echo ""
echo "To disable:"
echo "  rm .git/hooks/pre-push"
echo ""
