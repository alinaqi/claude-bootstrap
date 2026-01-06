#!/bin/bash

# Claude Skills Installer

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

echo "Installing Claude Skills..."

# Create directories
mkdir -p "$CLAUDE_DIR/commands"
mkdir -p "$CLAUDE_DIR/skills"
mkdir -p "$CLAUDE_DIR/hooks"

# Copy slash command
cp "$SCRIPT_DIR/commands/initialize-project.md" "$CLAUDE_DIR/commands/"
echo "✓ Installed /initialize-project command"

# Copy skills
cp "$SCRIPT_DIR/skills/"*.md "$CLAUDE_DIR/skills/"
echo "✓ Installed skills:"
ls -1 "$CLAUDE_DIR/skills/" | sed 's/^/  - /'

# Copy hooks
cp "$SCRIPT_DIR/hooks/"* "$CLAUDE_DIR/hooks/" 2>/dev/null || true
chmod +x "$CLAUDE_DIR/hooks/"* 2>/dev/null || true
echo "✓ Installed git hooks (templates)"

# Copy hook installer script
cp "$SCRIPT_DIR/scripts/install-hooks.sh" "$CLAUDE_DIR/" 2>/dev/null || true
chmod +x "$CLAUDE_DIR/install-hooks.sh" 2>/dev/null || true

echo ""
echo "Installation complete!"
echo ""
echo "Usage:"
echo "  1. Open any project folder"
echo "  2. Run Claude Code"
echo "  3. Type: /initialize-project"
echo ""
echo "Git Hooks (optional):"
echo "  To enable pre-push code review in a project:"
echo "  ~/.claude/install-hooks.sh"
echo ""
