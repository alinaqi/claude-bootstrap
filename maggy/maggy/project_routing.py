"""Per-project routing profiles — private, per-machine.

A project's profile lives at ``~/.claude/projects/<encoded-cwd>/routing.yaml``
(never committed) and overrides the global ``~/.maggy/routing.yaml`` for work in
that project. The runtime decision function ``decide_model`` implements the
"simple → one model, but escalate security" contract; ``balanced``/``critical``
fall through to the normal complexity ladder in model_router.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path

import yaml

_PROJECTS_DIR = Path.home() / ".claude" / "projects"
_SECURITY_TYPES = {"security", "auth", "billing"}


@dataclass
class ProjectProfile:
    """A per-project routing profile (see module docstring)."""

    profile: str = "balanced"  # simple | balanced | critical | custom
    default_provider: str = ""  # for 'simple': the one model's provider
    default_model: str = ""
    escalate_security_to: str = "claude"
    escalate_complexity_above: int = 8
    escalate_paths: dict[str, str] = field(default_factory=dict)  # glob -> model
    providers: dict[str, dict] = field(default_factory=dict)  # extra provider defs
    meta: dict = field(default_factory=dict)


@dataclass
class TaskContext:
    """The task attributes routing cares about (bundled to keep arity low)."""

    task_type: str = "general"
    security_sensitive: bool = False
    complexity: int = 0
    changed_paths: tuple[str, ...] = ()


@dataclass
class RouteChoice:
    """Outcome of a profile decision. ``use_ladder`` defers to model_router."""

    model: str = ""
    provider: str = ""
    escalated: bool = False
    use_ladder: bool = False
    reason: str = ""


def encode_project_path(cwd: str) -> str:
    """Encode an absolute cwd into the ~/.claude/projects dir name (slash→dash)."""
    return cwd.replace("/", "-")


def project_profile_path(cwd: str, base: Path | None = None) -> Path:
    """Location of a project's private routing.yaml."""
    root = base or _PROJECTS_DIR
    return root / encode_project_path(cwd) / "routing.yaml"


def _profile_to_dict(prof: ProjectProfile) -> dict:
    return {
        "profile": prof.profile,
        "default": {"provider": prof.default_provider, "model": prof.default_model},
        "escalate": {
            "security": prof.escalate_security_to,
            "complexity_above": prof.escalate_complexity_above,
            "paths": dict(prof.escalate_paths),
        },
        "providers": dict(prof.providers),
        "_meta": dict(prof.meta),
    }


def _profile_from_dict(raw: dict) -> ProjectProfile:
    default = raw.get("default") or {}
    esc = raw.get("escalate") or {}
    return ProjectProfile(
        profile=raw.get("profile", "balanced"),
        default_provider=default.get("provider", ""),
        default_model=default.get("model", ""),
        escalate_security_to=esc.get("security", "claude"),
        escalate_complexity_above=int(esc.get("complexity_above", 8)),
        escalate_paths=dict(esc.get("paths") or {}),
        providers=dict(raw.get("providers") or {}),
        meta=dict(raw.get("_meta") or {}),
    )


def load_project_profile(cwd: str, base: Path | None = None) -> ProjectProfile | None:
    """Load a project's profile, or None if it has none / is unreadable."""
    path = project_profile_path(cwd, base)
    if not path.exists():
        return None
    try:
        raw = yaml.safe_load(path.read_text()) or {}
    except Exception:
        return None
    return _profile_from_dict(raw)


def save_project_profile(prof: ProjectProfile, cwd: str, base: Path | None = None) -> Path:
    """Write a project's profile to its private path; returns the path."""
    path = project_profile_path(cwd, base)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.dump(_profile_to_dict(prof), default_flow_style=False, sort_keys=False))
    return path


def _security_target(prof: ProjectProfile, ctx: TaskContext) -> str:
    """The escalation model if this task is security-sensitive, else ''."""
    for path in ctx.changed_paths:
        for pattern, model in prof.escalate_paths.items():
            if fnmatch(path, pattern):
                return model
    if ctx.security_sensitive or ctx.task_type in _SECURITY_TYPES:
        return prof.escalate_security_to
    return ""


def decide_model(prof: ProjectProfile, ctx: TaskContext) -> RouteChoice:
    """Apply the project profile to a task. Security always escalates first."""
    target = _security_target(prof, ctx)
    if target:
        return RouteChoice(model=target, escalated=True, reason=f"security → {target}")
    if prof.profile == "simple":
        return RouteChoice(
            model=prof.default_model, provider=prof.default_provider,
            reason="simple profile → default model",
        )
    return RouteChoice(use_ladder=True, reason=f"{prof.profile} profile → complexity ladder")
