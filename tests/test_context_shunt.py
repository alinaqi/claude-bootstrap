"""Behavioural tests for the context-shunt gate hook and bulk-read worker.

The gate is a PreToolUse hook that (a) steers large reads to `bulk-read` and
(b) nudges code discovery toward the code graph. Unlike the injection hooks it
MAY block (exit 2) — but only as a *configured* decision. On any malformed or
empty input it must fail-open (exit 0) so a bug can never wedge the session.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "hooks" / "context-shunt-gate"
BULK = ROOT / "bin" / "bulk-read"


def _run(argv, stdin="", env=None):
    base = {"PATH": "/usr/bin:/bin:/usr/local/bin", "HOME": "/tmp/shunt-nohome"}
    if env:
        base.update(env)
    return subprocess.run(
        argv, input=stdin, capture_output=True, text=True, timeout=20, env=base
    )


def _gate(stdin, env=None):
    return _run(["bash", str(GATE)], stdin=stdin, env=env)


def _big(tmp_path, lines=400):
    f = tmp_path / "big.txt"
    f.write_text("\n".join(str(i) for i in range(lines)) + "\n")
    return f


# --- fail-open contract -----------------------------------------------------

@pytest.mark.parametrize("stdin", ["", "{not json", '{"tool_name":null}', "null"])
def test_gate_fails_open_on_bad_input(stdin):
    r = _gate(stdin, env={"SHUNT_GRAPH_NUDGE": "off"})
    assert r.returncode == 0
    assert r.stdout.strip() == ""


def test_master_switch_off_disables_everything(tmp_path):
    f = _big(tmp_path)
    payload = json.dumps({"tool_name": "Read", "tool_input": {"file_path": str(f)}})
    r = _gate(payload, env={"SHUNT": "off"})
    assert r.returncode == 0
    assert r.stdout.strip() == ""


# --- large-read shunt -------------------------------------------------------

def test_large_read_block_mode_denies_with_bulk_read_hint(tmp_path):
    f = _big(tmp_path)
    payload = json.dumps({"tool_name": "Read", "tool_input": {"file_path": str(f)}})
    r = _gate(payload, env={"SHUNT_MODE": "block", "SHUNT_GRAPH_NUDGE": "off"})
    assert r.returncode == 2
    assert "bulk-read" in r.stderr


def test_large_read_suggest_mode_allows_with_valid_json(tmp_path):
    f = _big(tmp_path)
    payload = json.dumps({"tool_name": "Read", "tool_input": {"file_path": str(f)}})
    r = _gate(payload, env={"SHUNT_MODE": "suggest", "SHUNT_GRAPH_NUDGE": "off"})
    assert r.returncode == 0
    out = json.loads(r.stdout)  # must be valid JSON
    hso = out["hookSpecificOutput"]
    assert hso["hookEventName"] == "PreToolUse"
    assert hso["permissionDecision"] == "allow"
    assert "bulk-read" in hso["permissionDecisionReason"]


def test_small_read_does_not_fire(tmp_path):
    f = tmp_path / "small.txt"
    f.write_text("a\nb\nc\n")
    payload = json.dumps({"tool_name": "Read", "tool_input": {"file_path": str(f)}})
    r = _gate(payload, env={"SHUNT_MODE": "block", "SHUNT_GRAPH_NUDGE": "off"})
    assert r.returncode == 0
    assert r.stdout.strip() == ""


def test_bash_cat_large_file_is_gated(tmp_path):
    f = _big(tmp_path)
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": f"cat {f}"}})
    r = _gate(payload, env={"SHUNT_MODE": "block", "SHUNT_GRAPH_NUDGE": "off"})
    assert r.returncode == 2


def test_bash_non_read_command_is_ignored(tmp_path):
    f = _big(tmp_path)
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": f"rm -f {f}"}})
    r = _gate(payload, env={"SHUNT_MODE": "block", "SHUNT_GRAPH_NUDGE": "off"})
    assert r.returncode == 0
    assert r.stdout.strip() == ""


def test_mode_off_ignores_file_size(tmp_path):
    f = _big(tmp_path)
    payload = json.dumps({"tool_name": "Read", "tool_input": {"file_path": str(f)}})
    r = _gate(payload, env={"SHUNT_MODE": "off", "SHUNT_GRAPH_NUDGE": "off"})
    assert r.returncode == 0
    assert r.stdout.strip() == ""


# --- code-discovery graph nudge ---------------------------------------------

def test_graph_nudge_blocks_first_discovery_call():
    # Clear any session marker so this call is treated as the first.
    for p in Path("/tmp").glob("cbm-code-discovery-gate-*"):
        try:
            p.unlink()
        except OSError:
            pass
    payload = json.dumps({"tool_name": "Grep", "tool_input": {"pattern": "x"}})
    r = _gate(payload, env={"SHUNT_GRAPH_NUDGE": "on", "SHUNT_MODE": "off"})
    assert r.returncode == 2
    assert "codebase-memory-mcp" in r.stderr


# --- bulk-read worker -------------------------------------------------------

def test_bulk_read_usage_without_args():
    r = _run(["bash", str(BULK)])
    assert r.returncode == 2
    assert "Usage" in r.stderr


def test_bulk_read_missing_worker_binary(tmp_path):
    f = tmp_path / "f.txt"
    f.write_text("hello\n")
    r = _run(["bash", str(BULK), "q?", str(f)], env={"SHUNT_MODEL": "no-such-bin-xyz"})
    assert r.returncode == 3
    assert "not found" in r.stderr


def test_bulk_read_pipes_corpus_to_worker(tmp_path):
    f = tmp_path / "f.txt"
    f.write_text("needle-value\n")
    # `cat` as a stand-in worker echoes the prompt (which embeds the file body).
    r = _run(["bash", str(BULK), "what value?", str(f)], env={"SHUNT_MODEL": "cat"})
    assert r.returncode == 0
    assert "needle-value" in r.stdout
    assert "% saved" in r.stderr
