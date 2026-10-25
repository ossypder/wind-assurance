"""Vercel entrypoint: serves the FastAPI app as a serverless function.

Vercel's filesystem is read-only (except /tmp) and ephemeral between cold
starts, so the checked-in SQLite snapshot is copied once per instance to
/tmp and data re-ingestion from Elexon is disabled.
"""
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "backend"))

_SNAPSHOT = _ROOT / "backend" / "data" / "bmrs.sqlite3"
_TMP_DB = Path("/tmp") / "bmrs.sqlite3"

if _SNAPSHOT.exists():
    if not _TMP_DB.exists():
        shutil.copy(_SNAPSHOT, _TMP_DB)
    os.environ.setdefault("DATA_DIR", "/tmp")
    os.environ.setdefault("INGEST_ON_START", "0")

from app.main import app  # noqa: E402
