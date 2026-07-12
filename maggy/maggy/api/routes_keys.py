"""API-key REST endpoints — configure provider keys from the Maggy UI.

Set, list (masked), and unset keys in ~/.maggy/.env. Values are never returned;
the UI only ever sees presence + a masked tail.
"""

from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel

from .auth import check_auth
from maggy import secrets_store
from maggy.secrets_store import ENV_PATH

router = APIRouter(prefix="/api/keys", tags=["keys"])


class KeyUpdate(BaseModel):
    name: str
    value: str


@router.get("")
async def get_keys(request: Request, x_api_key: str | None = Header(None)) -> dict:
    """List all known keys with masked presence only (never the raw value)."""
    check_auth(request, x_api_key)
    return {"keys": secrets_store.list_keys(path=ENV_PATH)}


@router.post("")
async def set_key(
    request: Request, body: KeyUpdate, x_api_key: str | None = Header(None),
) -> dict:
    """Store or overwrite a provider key."""
    check_auth(request, x_api_key)
    try:
        secrets_store.set_key(body.name, body.value, path=ENV_PATH)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    entry = next(k for k in secrets_store.list_keys(path=ENV_PATH) if k["name"] == body.name)
    return {"ok": True, "key": entry}


@router.delete("/{name}")
async def unset_key(
    request: Request, name: str, x_api_key: str | None = Header(None),
) -> dict:
    """Remove a provider key."""
    check_auth(request, x_api_key)
    secrets_store.unset_key(name, path=ENV_PATH)
    return {"ok": True, "name": name}
