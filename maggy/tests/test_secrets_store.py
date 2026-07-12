"""Tests for the central API-key store (~/.maggy/.env, chmod 600)."""

from __future__ import annotations

import stat

import pytest


class TestSetGetUnset:
    def test_set_then_present_and_masked(self, tmp_path):
        from maggy.secrets_store import set_key, list_keys
        p = tmp_path / ".env"
        set_key("GLM_API_KEY", "sk-1234567890abcd", path=p)
        entry = next(k for k in list_keys(path=p) if k["name"] == "GLM_API_KEY")
        assert entry["set"] is True
        assert entry["masked"].endswith("abcd")
        assert "1234567890" not in entry["masked"]  # never leak the full key

    def test_list_never_returns_raw_value(self, tmp_path):
        from maggy.secrets_store import set_key, list_keys
        p = tmp_path / ".env"
        set_key("GROQ_API_KEY", "supersecretvalue", path=p)
        for k in list_keys(path=p):
            assert "value" not in k
            assert "supersecretvalue" not in str(k)

    def test_unset_removes(self, tmp_path):
        from maggy.secrets_store import set_key, unset_key, list_keys
        p = tmp_path / ".env"
        set_key("GLM_API_KEY", "sk-abcd1234", path=p)
        unset_key("GLM_API_KEY", path=p)
        entry = next(k for k in list_keys(path=p) if k["name"] == "GLM_API_KEY")
        assert entry["set"] is False
        assert entry["masked"] == ""

    def test_unset_missing_is_noop(self, tmp_path):
        from maggy.secrets_store import unset_key
        unset_key("GLM_API_KEY", path=tmp_path / ".env")  # no raise

    def test_set_overwrites(self, tmp_path):
        from maggy.secrets_store import set_key, _read_raw
        p = tmp_path / ".env"
        set_key("GLM_API_KEY", "first", path=p)
        set_key("GLM_API_KEY", "second", path=p)
        assert _read_raw(p)["GLM_API_KEY"] == "second"


class TestValidation:
    def test_rejects_bad_name(self, tmp_path):
        from maggy.secrets_store import set_key
        with pytest.raises(ValueError):
            set_key("bad name; rm -rf", "x", path=tmp_path / ".env")

    def test_rejects_empty_value(self, tmp_path):
        from maggy.secrets_store import set_key
        with pytest.raises(ValueError):
            set_key("GLM_API_KEY", "", path=tmp_path / ".env")

    @pytest.mark.parametrize("bad", [
        "sk-abc\nPATH=/evil",   # newline injects a second env line
        "sk\r\nEVIL=1",         # CRLF
        "sk\x00trunc",          # NUL truncation
        "a\tb",                 # other control char
    ])
    def test_rejects_control_chars_in_value(self, tmp_path, bad):
        from maggy.secrets_store import set_key
        with pytest.raises(ValueError):
            set_key("GLM_API_KEY", bad, path=tmp_path / ".env")

    def test_injection_does_not_write_extra_line(self, tmp_path):
        # A rejected injection must not add a second key or mutate the good one.
        from maggy.secrets_store import set_key, _read_raw
        p = tmp_path / ".env"
        set_key("GLM_API_KEY", "sk-good", path=p)
        with pytest.raises(ValueError):
            set_key("GLM_API_KEY", "sk-x\nEVIL=1", path=p)
        data = _read_raw(p)
        assert "EVIL" not in data
        assert data["GLM_API_KEY"] == "sk-good"  # unchanged


class TestSecurity:
    def test_file_is_chmod_600(self, tmp_path):
        from maggy.secrets_store import set_key
        p = tmp_path / ".env"
        set_key("GLM_API_KEY", "sk-abcd1234", path=p)
        mode = stat.S_IMODE(p.stat().st_mode)
        assert mode == 0o600

    def test_preexisting_loose_file_is_tightened(self, tmp_path):
        # A file that already exists world-readable must end up 0600.
        from maggy.secrets_store import set_key
        p = tmp_path / ".env"
        p.write_text("OLD=1\n")
        p.chmod(0o644)
        set_key("GLM_API_KEY", "sk-abcd1234", path=p)
        assert stat.S_IMODE(p.stat().st_mode) == 0o600

    def test_parent_dir_is_0700(self, tmp_path):
        from maggy.secrets_store import set_key
        d = tmp_path / "maggydir"
        set_key("GLM_API_KEY", "sk-abcd1234", path=d / ".env")
        assert stat.S_IMODE(d.stat().st_mode) == 0o700

    def test_never_world_readable_midwrite(self, tmp_path, monkeypatch):
        # Capture the mode the credential bytes are first created with — must be 0600.
        import os
        from maggy import secrets_store
        seen = {}
        real_open = os.open

        def spy_open(path, flags, mode=0o777, *a, **k):
            fd = real_open(path, flags, mode, *a, **k)
            if flags & os.O_CREAT and (flags & os.O_WRONLY or flags & os.O_RDWR):
                seen["mode"] = stat.S_IMODE(os.fstat(fd).st_mode)
            return fd

        monkeypatch.setattr(os, "open", spy_open)
        secrets_store.set_key("GLM_API_KEY", "sk-abcd1234", path=tmp_path / ".env")
        assert seen.get("mode") == 0o600  # bytes never hit disk at looser perms


class TestLoadIntoEnv:
    def test_load_populates_environ(self, tmp_path, monkeypatch):
        from maggy.secrets_store import set_key, load_into_env
        p = tmp_path / ".env"
        set_key("GLM_API_KEY", "sk-loaded", path=p)
        monkeypatch.delenv("GLM_API_KEY", raising=False)
        load_into_env(path=p)
        import os
        assert os.environ["GLM_API_KEY"] == "sk-loaded"

    def test_load_does_not_overwrite_existing(self, tmp_path, monkeypatch):
        from maggy.secrets_store import set_key, load_into_env
        p = tmp_path / ".env"
        set_key("GLM_API_KEY", "from-file", path=p)
        monkeypatch.setenv("GLM_API_KEY", "from-shell")
        load_into_env(path=p)
        import os
        assert os.environ["GLM_API_KEY"] == "from-shell"  # shell wins


class TestKnownKeys:
    def test_lists_known_even_when_unset(self, tmp_path):
        from maggy.secrets_store import list_keys, KNOWN_KEYS
        names = {k["name"] for k in list_keys(path=tmp_path / "nope.env")}
        assert "GLM_API_KEY" in names
        assert set(KNOWN_KEYS).issubset(names)
