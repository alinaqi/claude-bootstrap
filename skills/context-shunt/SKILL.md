---
name: context-shunt
description: Offload large / multi-file reads to a cheap worker model so raw files never enter Claude's context (token savings)
when-to-use: When answering a question that requires reading large or many files, reviewing logs, or scanning generated output — anything you don't need to edit
user-invocable: false
effort: low
---

# Context Shunt — Read Cheap, Keep Context Small

Reading big files into context is the most expensive thing an agent does for the
least reasoning value. The shunt hands those reads to a cheap worker model
(`bulk-read`) that answers a question about the files and returns a compact
summary. The raw bytes never enter this session's context.

This is orthogonal to whole-turn routing (srooter / `route-task`): those pick the
model for the *turn*; the shunt trims what a *tool call* pulls into context when
the turn is legitimately here.

## Decision: read raw, shunt, or graph?

- **Editing this exact file** — read it raw. You need every line; never edit against a summary.
- **A fact/answer across large or many files** — `bulk-read "<question>" file...`.
- **A code symbol (function/class/route)** — `get_code_snippet(qualified_name)`: free and exact.
- **Small file (under threshold) you need in full** — read it raw.

A shunt answer is for understanding, not for producing a diff.

## Usage

```bash
bulk-read "how does token refresh work?" src/auth/session.ts src/auth/refresh.ts
bulk-read "which config keys are read at startup?" $(git ls-files 'config/*.yaml')
```

`bulk-read` prints structured bullets citing `path:line`, or
`NOT FOUND IN PROVIDED FILES`. A token-savings report goes to stderr.

## Configuration

Env vars or `~/.claude/shunt.conf` (see `templates/shunt.conf`):

- `SHUNT` — `on`/`off` master switch for the PreToolUse hook.
- `SHUNT_MIN_LINES` — large-read threshold (default 350).
- `SHUNT_MODE` — `suggest` (default) / `block` / `off` for the hook's large-read action.
- `SHUNT_GRAPH_NUDGE` — `on`/`off` once-per-session graph nudge.
- `SHUNT_MODEL` — worker command (default `deepseek --flash`; also `gemini-api --flash-lite`, `qwen3`, `glm`).

The `context-shunt-gate` PreToolUse hook enforces the thresholds; this skill tells
you when to reach for `bulk-read` yourself.
