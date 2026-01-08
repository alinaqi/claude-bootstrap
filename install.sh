#!/bin/bash

# Claude Bootstrap Installer

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
BOOTSTRAP_DIR="$HOME/.claude-bootstrap"

echo "Installing Claude Bootstrap..."
echo ""

# Create directories
mkdir -p "$CLAUDE_DIR/commands"
mkdir -p "$CLAUDE_DIR/skills"
mkdir -p "$CLAUDE_DIR/hooks"
mkdir -p "$CLAUDE_DIR/plugins"

# Copy all commands
cp "$SCRIPT_DIR/commands/"*.md "$CLAUDE_DIR/commands/"
echo "✓ Installed commands:"
ls -1 "$CLAUDE_DIR/commands/" | sed 's/^/  - \//' | sed 's/\.md$//'

# Copy skills (folder structure with SKILL.md)
echo ""
echo "Installing skills..."
# First, remove old skills to ensure clean state
rm -rf "$CLAUDE_DIR/skills"
mkdir -p "$CLAUDE_DIR/skills"
skill_count=0
for skill_dir in "$SCRIPT_DIR/skills"/*/; do
    if [ -d "$skill_dir" ] && [ -f "$skill_dir/SKILL.md" ]; then
        skill_name=$(basename "$skill_dir")
        # Remove trailing slash and copy the folder itself
        cp -r "${skill_dir%/}" "$CLAUDE_DIR/skills/"
        skill_count=$((skill_count + 1))
    fi
done
echo "✓ Installed $skill_count skills (folder/SKILL.md structure)"

# Copy hooks
cp "$SCRIPT_DIR/hooks/"* "$CLAUDE_DIR/hooks/" 2>/dev/null || true
chmod +x "$CLAUDE_DIR/hooks/"* 2>/dev/null || true
echo "✓ Installed git hooks (templates)"

# Copy hook installer script
cp "$SCRIPT_DIR/scripts/install-hooks.sh" "$CLAUDE_DIR/" 2>/dev/null || true
chmod +x "$CLAUDE_DIR/install-hooks.sh" 2>/dev/null || true

# Create symlink for ~/.claude-bootstrap (for validation scripts)
if [ "$SCRIPT_DIR" != "$BOOTSTRAP_DIR" ]; then
    if [ -L "$BOOTSTRAP_DIR" ]; then
        rm "$BOOTSTRAP_DIR"
    fi
    if [ ! -d "$BOOTSTRAP_DIR" ]; then
        ln -s "$SCRIPT_DIR" "$BOOTSTRAP_DIR"
        echo "✓ Created symlink: ~/.claude-bootstrap -> $SCRIPT_DIR"
    fi
fi

# Check for Ralph Loop plugin
echo ""
if [ -d "$CLAUDE_DIR/plugins/marketplaces/claude-plugins-official/plugins/ralph-loop" ]; then
    echo "✓ Ralph Loop plugin available in marketplace"
    echo "  To install: /plugin install ralph-loop@claude-plugins-official"
else
    echo "⚠ Ralph Loop plugin not found in marketplace"
    echo "  Update marketplace: /plugin update (in Claude Code)"
    echo "  Then install: /plugin install ralph-loop@claude-plugins-official"
fi

# Run validation
echo ""
echo "Running validation..."
if [ -f "$SCRIPT_DIR/tests/validate-structure.sh" ]; then
    if "$SCRIPT_DIR/tests/validate-structure.sh" --quick; then
        echo ""
    else
        echo ""
        echo "⚠ Validation found issues. Run full validation:"
        echo "  $SCRIPT_DIR/tests/validate-structure.sh --full"
    fi
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  Installation complete!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Usage:"
echo "  1. Open any project folder"
echo "  2. Run: claude"
echo "  3. Type: /initialize-project"
echo ""
echo "Commands installed:"
echo "  /initialize-project   - Full project setup"
echo "  /check-contributors   - Team coordination"
echo "  /update-code-index    - Regenerate code index"
echo ""
echo "Git Hooks (per-project):"
echo "  cd your-project && ~/.claude/install-hooks.sh"
echo ""
echo "Validation:"
echo "  ~/.claude-bootstrap/tests/validate-structure.sh --full"
echo ""
