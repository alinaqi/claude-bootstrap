"""Robustness guardrail for the bootstrap PreToolUse hooks.

Every PreToolUse hook MUST, for any input (empty, malformed, adversarial):
  1. exit 0 (fail-open — never block or error the session), and
  2. write valid JSON or nothing to stdout (a malformed payload is surfaced by
     Claude Code as a "hook error").
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

HOOKS_DIR = Path(__file__).resolve().parents[1] / "hooks"
PRETOOL_HOOKS = ["icpg-record-intent", "icpg-inject-context", "mid-task-escalation"]

PAYLOADS = {
    "empty": "",
    "malformed": "{not valid json",
    "edit_missing_file": '{"tool_name":"Edit","tool_input":{"file_path":"/no/such/f.py"}}',
    "edit_special_chars": '{"tool_name":"Edit","tool_input":'
    '{"file_path":"/tmp/a\\"b.py","new_string":"x\\ny"}}',
    "non_edit_tool": '{"tool_name":"Read","tool_input":{"file_path":"/tmp/x"}}',
    "null_input": '{"tool_name":"Edit","tool_input":null}',
}


def _run(hook: str, stdin: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(HOOKS_DIR / hook)],
        input=stdin, capture_output=True, text=True, timeout=15,
    )


@pytest.mark.parametrize("hook", PRETOOL_HOOKS)
@pytest.mark.parametrize("name", list(PAYLOADS))
def test_hook_exits_zero_and_emits_valid_json_or_nothing(hook: str, name: str) -> None:
    r = _run(hook, PAYLOADS[name])
    assert r.returncode == 0, f"{hook} exited {r.returncode} on {name}: {r.stderr}"
    out = r.stdout.strip()
    if out:
        json.loads(out)  # must parse — malformed JSON would raise


def test_record_intent_no_crash_on_double_read_regression() -> None:
    # Regression for the json.loads(sys.stdin) bug that silently disabled the
    # hook: a well-formed Edit payload must be processed without a Python trace.
    r = _run("icpg-record-intent", PAYLOADS["edit_missing_file"])
    assert r.returncode == 0
    assert "Traceback" not in r.stderr
