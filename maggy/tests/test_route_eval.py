"""Tests for the /route-eval project+history evaluator."""

from __future__ import annotations


class TestScanProject:
    def _mk(self, tmp_path, files):
        for rel, body in files.items():
            p = tmp_path / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(body)
        return tmp_path

    def test_counts_files_and_langs(self, tmp_path):
        from maggy.route_eval import scan_project
        self._mk(tmp_path, {"a.py": "x=1\n", "b.py": "y=2\n", "c.ts": "const z=3\n"})
        scan = scan_project(str(tmp_path))
        assert scan.file_count == 3
        assert scan.langs.get("py") == 2
        assert scan.langs.get("ts") == 1

    def test_detects_tests(self, tmp_path):
        from maggy.route_eval import scan_project
        self._mk(tmp_path, {"src/a.py": "x=1\n", "tests/test_a.py": "def test_x(): pass\n"})
        assert scan_project(str(tmp_path)).has_tests is True

    def test_detects_security_surface(self, tmp_path):
        from maggy.route_eval import scan_project
        self._mk(tmp_path, {"src/auth/login.py": "pw=1\n", "src/ui.py": "x=1\n"})
        surface = scan_project(str(tmp_path)).security_surface
        assert any("auth" in s for s in surface)

    def test_no_security_surface_when_clean(self, tmp_path):
        from maggy.route_eval import scan_project
        self._mk(tmp_path, {"src/ui.py": "x=1\n", "README.md": "hi\n"})
        assert scan_project(str(tmp_path)).security_surface == []


class TestHistorySignal:
    def test_missing_log_is_empty(self, tmp_path):
        from maggy.route_eval import history_signal
        assert history_signal(tmp_path / "nope.jsonl") == {}

    def test_tier_fractions(self, tmp_path):
        from maggy.route_eval import history_signal
        log = tmp_path / "routing-log.jsonl"
        log.write_text(
            '{"tier":"QWEN"}\n{"tier":"QWEN"}\n{"tier":"CLAUDE"}\n{"bad json"\n'
        )
        sig = history_signal(log)
        assert round(sig["QWEN"], 2) == 0.67
        assert round(sig["CLAUDE"], 2) == 0.33


class TestRecommend:
    def _scan(self, **kw):
        from maggy.route_eval import ProjectScan
        base = dict(langs={"py": 10}, file_count=20, loc=800,
                    has_tests=True, security_surface=[], dep_files=[])
        base.update(kw)
        return ProjectScan(**base)

    def test_small_clean_project_is_simple(self):
        from maggy.route_eval import recommend
        prof = recommend(self._scan(), {"QWEN": 0.8, "CLAUDE": 0.2})
        assert prof.profile == "simple"
        assert prof.default_model == "glm-5.2"
        # security still escalates even on a simple project
        assert prof.escalate_security_to == "claude"
        assert "**/auth/**" in prof.escalate_paths

    def test_security_surface_forces_critical(self):
        from maggy.route_eval import recommend
        prof = recommend(self._scan(security_surface=["src/auth/login.py"]),
                         {"QWEN": 0.9})
        assert prof.profile == "critical"

    def test_large_project_not_simple(self):
        from maggy.route_eval import recommend
        prof = recommend(self._scan(file_count=500), {"QWEN": 0.9})
        assert prof.profile in ("balanced", "critical")

    def test_claude_heavy_history_not_simple(self):
        from maggy.route_eval import recommend
        prof = recommend(self._scan(), {"CLAUDE": 0.7, "QWEN": 0.3})
        assert prof.profile != "simple"

    def test_recommend_records_evidence(self):
        from maggy.route_eval import recommend
        prof = recommend(self._scan(), {"QWEN": 0.9})
        assert prof.meta.get("evidence")
        assert prof.meta.get("generated_by") == "/route-eval"
