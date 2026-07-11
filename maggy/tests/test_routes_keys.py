"""Tests for /api/keys — configure API keys from the Maggy UI (set/unset/list)."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path, monkeypatch):
    # Redirect the key store to a temp file so tests never touch ~/.maggy/.env
    import maggy.api.routes_keys as rk
    monkeypatch.setattr(rk, "ENV_PATH", tmp_path / ".env")
    from maggy.config import MaggyConfig
    from maggy.main import create_app
    app = create_app()
    app.state.cfg = MaggyConfig()
    return TestClient(app)


class TestListKeys:
    def test_lists_known_keys(self, client):
        resp = client.get("/api/keys")
        assert resp.status_code == 200
        names = {k["name"] for k in resp.json()["keys"]}
        assert "GLM_API_KEY" in names
        assert "OPENAI_API_KEY" in names

    def test_unset_by_default(self, client):
        entry = next(k for k in client.get("/api/keys").json()["keys"]
                     if k["name"] == "GLM_API_KEY")
        assert entry["set"] is False


class TestSetKey:
    def test_set_then_masked(self, client):
        r = client.post("/api/keys", json={"name": "GLM_API_KEY", "value": "sk-abcd1234"})
        assert r.status_code == 200
        entry = next(k for k in client.get("/api/keys").json()["keys"]
                     if k["name"] == "GLM_API_KEY")
        assert entry["set"] is True
        assert entry["masked"].endswith("1234")

    def test_response_never_echoes_value(self, client):
        r = client.post("/api/keys", json={"name": "GROQ_API_KEY", "value": "supersecret"})
        assert "supersecret" not in r.text

    def test_bad_name_rejected(self, client):
        r = client.post("/api/keys", json={"name": "bad name", "value": "x"})
        assert r.status_code == 400


class TestUnsetKey:
    def test_delete_removes(self, client):
        client.post("/api/keys", json={"name": "GLM_API_KEY", "value": "sk-abcd1234"})
        r = client.delete("/api/keys/GLM_API_KEY")
        assert r.status_code == 200
        entry = next(k for k in client.get("/api/keys").json()["keys"]
                     if k["name"] == "GLM_API_KEY")
        assert entry["set"] is False
