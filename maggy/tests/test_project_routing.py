"""Tests for per-project routing profiles (private per-machine config)."""

from __future__ import annotations



class TestProfilePath:
    def test_encode_slashes_to_dashes(self):
        from maggy.project_routing import encode_project_path
        assert encode_project_path("/Users/x/proj") == "-Users-x-proj"

    def test_path_under_base(self, tmp_path):
        from maggy.project_routing import project_profile_path
        p = project_profile_path("/Users/x/proj", base=tmp_path)
        assert p == tmp_path / "-Users-x-proj" / "routing.yaml"


class TestLoadSave:
    def test_missing_returns_none(self, tmp_path):
        from maggy.project_routing import load_project_profile
        assert load_project_profile("/no/such/proj", base=tmp_path) is None

    def test_roundtrip(self, tmp_path):
        from maggy.project_routing import (
            ProjectProfile, save_project_profile, load_project_profile,
        )
        prof = ProjectProfile(
            profile="simple", default_provider="glm", default_model="glm-5.2",
            escalate_paths={"**/auth/**": "claude"},
        )
        save_project_profile(prof, "/Users/x/proj", base=tmp_path)
        got = load_project_profile("/Users/x/proj", base=tmp_path)
        assert got is not None
        assert got.profile == "simple"
        assert got.default_model == "glm-5.2"
        assert got.escalate_paths == {"**/auth/**": "claude"}


class TestDecideModel:
    def _simple(self):
        from maggy.project_routing import ProjectProfile
        return ProjectProfile(
            profile="simple", default_provider="glm", default_model="glm-5.2",
            escalate_security_to="claude",
            escalate_paths={"**/auth/**": "claude", "**/payments/**": "claude"},
        )

    def test_simple_routes_to_default(self):
        from maggy.project_routing import decide_model, TaskContext
        d = decide_model(self._simple(), TaskContext(task_type="feature", complexity=3))
        assert d.model == "glm-5.2"
        assert d.provider == "glm"
        assert d.escalated is False

    def test_security_flag_escalates(self):
        from maggy.project_routing import decide_model, TaskContext
        d = decide_model(self._simple(), TaskContext(security_sensitive=True))
        assert d.model == "claude"
        assert d.escalated is True

    def test_security_task_type_escalates(self):
        from maggy.project_routing import decide_model, TaskContext
        d = decide_model(self._simple(), TaskContext(task_type="auth"))
        assert d.model == "claude"
        assert d.escalated is True

    def test_changed_path_glob_escalates(self):
        from maggy.project_routing import decide_model, TaskContext
        ctx = TaskContext(task_type="feature", changed_paths=("src/auth/login.py",))
        d = decide_model(self._simple(), ctx)
        assert d.model == "claude"
        assert d.escalated is True

    def test_unmatched_path_stays_default(self):
        from maggy.project_routing import decide_model, TaskContext
        ctx = TaskContext(task_type="feature", changed_paths=("src/ui/button.tsx",))
        d = decide_model(self._simple(), ctx)
        assert d.model == "glm-5.2"

    def test_balanced_falls_through_to_ladder(self):
        from maggy.project_routing import ProjectProfile, decide_model, TaskContext
        prof = ProjectProfile(profile="balanced", escalate_security_to="claude")
        d = decide_model(prof, TaskContext(task_type="feature", complexity=5))
        assert d.use_ladder is True

    def test_balanced_still_escalates_security(self):
        from maggy.project_routing import ProjectProfile, decide_model, TaskContext
        prof = ProjectProfile(profile="balanced", escalate_security_to="claude")
        d = decide_model(prof, TaskContext(security_sensitive=True))
        assert d.model == "claude"
        assert d.use_ladder is False
