"""Central API-key store — the one place Maggy reads/writes provider keys.

Keys live in ``~/.maggy/.env`` (mode 600, outside any repo). The CLI wrappers
(``~/bin/glm`` etc.), Maggy, and — once the user sources it in their shell —
``claude`` / ``codex`` all read the same file. Values are never returned raw:
``list_keys`` reports presence + a masked tail only.
"""

from __future__ import annotations

import os
import re
import tempfile
from pathlib import Path

from maggy.config import CONFIG_DIR

ENV_PATH = CONFIG_DIR / ".env"
_NAME_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")

# Providers Maggy knows how to configure: env-var name -> human label.
KNOWN_KEYS: dict[str, str] = {
    "GLM_API_KEY": "GLM / BigModel",
    "GROQ_API_KEY": "Groq",
    "TOGETHER_API_KEY": "Together AI",
    "DEEPSEEK_API_KEY": "DeepSeek",
    "OPENAI_API_KEY": "OpenAI / Codex",
    "ANTHROPIC_API_KEY": "Anthropic / Claude",
    "GEMINI_API_KEY": "Google Gemini",
    "GROK_API_KEY": "xAI Grok",
    "GITHUB_TOKEN": "GitHub",
}


def _read_raw(path: Path | None = None) -> dict[str, str]:
    """Parse KEY=VALUE lines; ignore blanks and comments."""
    p = path or ENV_PATH
    if not p.exists():
        return {}
    out: dict[str, str] = {}
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, _, value = line.partition("=")
        out[name.strip()] = value.strip()
    return out


def _write_raw(data: dict[str, str], path: Path | None = None) -> None:
    """Atomically write the key file at 0600 (dir 0700) — credentials never
    touch disk at looser permissions, even briefly."""
    p = path or ENV_PATH
    p.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    _chmod_quiet(p.parent, 0o700)  # tighten if the dir pre-existed looser
    body = "".join(f"{k}={v}\n" for k, v in sorted(data.items()))
    content = "# Maggy API keys — managed by secrets_store. Do not commit.\n" + body
    # mkstemp creates the file 0600; write, then atomically replace the target.
    fd, tmp = tempfile.mkstemp(dir=str(p.parent), prefix=".env-")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(content)
        os.replace(tmp, p)
    except BaseException:
        _chmod_quiet(Path(tmp), 0o600)
        Path(tmp).unlink(missing_ok=True)
        raise


def _chmod_quiet(p: Path, mode: int) -> None:
    try:
        p.chmod(mode)
    except OSError:
        pass


def set_key(name: str, value: str, path: Path | None = None) -> None:
    """Store (or overwrite) a key. Raises ValueError on a bad name/value."""
    if not _NAME_RE.match(name or ""):
        raise ValueError(f"invalid key name: {name!r}")
    if not value or not value.strip():
        raise ValueError("value must not be empty")
    # Reject control chars: an interior newline survives .strip() and would inject
    # extra KEY=VALUE lines into the env file (e.g. override PATH), and NUL truncates.
    if any(ord(c) < 32 for c in value):
        raise ValueError("value must not contain control characters (newline/CR/NUL/tab)")
    data = _read_raw(path)
    data[name] = value.strip()
    _write_raw(data, path)


def unset_key(name: str, path: Path | None = None) -> None:
    """Remove a key if present (no-op otherwise)."""
    data = _read_raw(path)
    if name in data:
        del data[name]
        _write_raw(data, path)


def _mask(value: str) -> str:
    """Show only the last 4 chars, e.g. 'sk-…abcd'."""
    tail = value[-4:] if len(value) >= 4 else value
    return f"…{tail}"


def list_keys(path: Path | None = None) -> list[dict]:
    """All KNOWN_KEYS (plus any extras on disk) with masked presence only."""
    data = _read_raw(path)
    names = list(KNOWN_KEYS) + [n for n in data if n not in KNOWN_KEYS]
    out = []
    for name in names:
        present = bool(data.get(name))
        out.append({
            "name": name,
            "label": KNOWN_KEYS.get(name, name),
            "set": present,
            "masked": _mask(data[name]) if present else "",
        })
    return out


def load_into_env(path: Path | None = None) -> None:
    """Merge stored keys into os.environ without clobbering existing shell vars."""
    for name, value in _read_raw(path).items():
        os.environ.setdefault(name, value)
