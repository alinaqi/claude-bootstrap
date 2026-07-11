"""Evaluate a project + past routing history and recommend a routing profile.

The brain behind ``/route-eval``. Pure, testable functions:
  scan_project()   — deterministic structural signals (langs, size, security).
  history_signal() — tier distribution from ~/.claude/routing-log.jsonl (a prior).
  recommend()      — pick simple | balanced | critical + a default model.

CLI: ``python3 -m maggy.route_eval plan|apply [--cwd DIR] [--model glm-5.2]``.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

from maggy.project_routing import ProjectProfile, save_project_profile

_CODE_EXT = {"py", "ts", "tsx", "js", "jsx", "go", "rs", "rb", "java", "kt", "c", "cpp", "cs"}
_SECURITY_HINTS = ("auth", "login", "oauth", "jwt", "password", "secret",
                   "payment", "billing", "crypto", "token")
_SKIP_DIRS = {".git", "node_modules", "dist", "build", "__pycache__", ".venv", "venv"}
_DEFAULT_LOG = Path.home() / ".claude" / "routing-log.jsonl"
_ESCALATE_PATHS = {"**/auth/**": "claude", "**/payments/**": "claude",
                   "**/billing/**": "claude"}


@dataclass
class ProjectScan:
    langs: dict[str, int] = field(default_factory=dict)
    file_count: int = 0
    loc: int = 0
    has_tests: bool = False
    security_surface: list[str] = field(default_factory=list)
    dep_files: list[str] = field(default_factory=list)


def _iter_files(root: Path):
    for p in root.rglob("*"):
        if p.is_file() and not any(part in _SKIP_DIRS for part in p.parts):
            yield p


def scan_project(path: str) -> ProjectScan:
    """Deterministic structural signals about a project."""
    root = Path(path)
    scan = ProjectScan()
    for p in _iter_files(root):
        rel = p.relative_to(root).as_posix()
        ext = p.suffix.lstrip(".").lower()
        if ext in _CODE_EXT:
            scan.langs[ext] = scan.langs.get(ext, 0) + 1
            scan.file_count += 1
            scan.loc += _count_lines(p)
        if "test" in rel.lower():
            scan.has_tests = True
        if any(h in rel.lower() for h in _SECURITY_HINTS):
            scan.security_surface.append(rel)
        if p.name in ("package.json", "pyproject.toml", "go.mod", "Cargo.toml"):
            scan.dep_files.append(rel)
    return scan


def _count_lines(p: Path) -> int:
    try:
        return sum(1 for _ in p.open("r", errors="ignore"))
    except OSError:
        return 0


def history_signal(log_path: Path | None = None) -> dict[str, float]:
    """Tier distribution (fractions) from the routing log; {} if none."""
    path = log_path or _DEFAULT_LOG
    if not path.exists():
        return {}
    counts: dict[str, int] = {}
    for line in path.read_text(errors="ignore").splitlines():
        try:
            tier = json.loads(line).get("tier")
        except (json.JSONDecodeError, AttributeError):
            continue
        if tier:
            counts[tier] = counts.get(tier, 0) + 1
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()} if total else {}


def _premium_fraction(history: dict[str, float]) -> float:
    return history.get("CLAUDE", 0.0) + history.get("CODEX", 0.0)


def recommend(scan: ProjectScan, history: dict[str, float],
              cheap: tuple[str, str] = ("glm", "glm-5.2")) -> ProjectProfile:
    """Pick a profile from structural + historical signals."""
    if scan.security_surface:
        profile = "critical"
    elif scan.file_count > 300 or _premium_fraction(history) >= 0.5:
        profile = "balanced"
    elif scan.file_count <= 60 and len(scan.langs) <= 2:
        profile = "simple"
    else:
        profile = "balanced"

    prof = ProjectProfile(
        profile=profile,
        default_provider=cheap[0] if profile == "simple" else "",
        default_model=cheap[1] if profile == "simple" else "",
        escalate_paths=dict(_ESCALATE_PATHS),
        meta=_evidence(scan, history, profile),
    )
    return prof


def _evidence(scan: ProjectScan, history: dict[str, float], profile: str) -> dict:
    langs = ",".join(sorted(scan.langs)) or "none"
    top = max(history, key=history.get) if history else "n/a"
    return {
        "generated_by": "/route-eval",
        "evidence": (f"{scan.file_count} files, langs={langs}, "
                     f"security_surface={len(scan.security_surface)}, "
                     f"history_top_tier={top} → {profile}"),
    }


def _run(argv: list[str]) -> int:
    cmd = argv[0] if argv else "plan"
    cwd = _arg(argv, "--cwd", str(Path.cwd()))
    model = _arg(argv, "--model", "glm-5.2")
    scan = scan_project(cwd)
    prof = recommend(scan, history_signal(), cheap=("glm", model))
    if cmd == "apply":
        path = save_project_profile(prof, cwd)
        print(f"wrote {path}")
    else:
        print(json.dumps({"profile": prof.profile, "default_model": prof.default_model,
                          "escalate_paths": prof.escalate_paths, "_meta": prof.meta}, indent=2))
    return 0


def _arg(argv: list[str], flag: str, default: str) -> str:
    return argv[argv.index(flag) + 1] if flag in argv and argv.index(flag) + 1 < len(argv) else default


if __name__ == "__main__":  # pragma: no cover
    sys.exit(_run(sys.argv[1:]))
