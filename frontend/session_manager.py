# =====================================================
# FILE: session_manager.py
# NAME: session_manager.py
# PURPOSE: Per-user/session persistent store (SQLite + optional Redis).
# DETAILS: Intake stores requirements, Planning stores sequences, Interactive stores debug.
# VERSION: 1.0.1
# =====================================================

"""Session Manager – persistent context for front-end agents."""

import sqlite3
import json
import hashlib
import sys
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

# Path injection
BLUEPRINT_ROOT = Path(__file__).parent.parent
if str(BLUEPRINT_ROOT) not in sys.path:
    sys.path.append(str(BLUEPRINT_ROOT))

try:
    from toolkits.dependency.core_utils import AtomicFileWriter
except ImportError:
    class AtomicFileWriter:
        def __init__(self, path): self.path = path
        def write(self, content, role, protocol):
            with open(self.path, "w") as f: f.write(content)
        def __enter__(self): return self
        def __exit__(self, *args): pass

from .schemas import SessionState

DB_PATH = Path("frontend_sessions.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS sessions (
        user_id TEXT PRIMARY KEY,
        data TEXT,
        hash TEXT,
        updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()

init_db()

def get_session(user_id: str) -> Dict:
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("SELECT data, hash FROM sessions WHERE user_id=?", (user_id,)).fetchone()
    if row:
        data = json.loads(row[0])
        # verify hash integrity
        calculated_hash = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
        if calculated_hash == row[1]:
            return data
    return {"requirements": [], "sequence": [], "debug_log": []}

def update_session(user_id: str, delta: Dict):
    """Atomic update with Pydantic validation."""
    current = get_session(user_id)
    current.update(delta)
    current["user_id"] = user_id
    current["last_updated"] = datetime.utcnow().isoformat()
    
    # Validate against schema
    state = SessionState(**current)
    data_str = state.json(sort_keys=True)
    h = hashlib.sha256(data_str.encode()).hexdigest()
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("REPLACE INTO sessions (user_id, data, hash) VALUES (?, ?, ?)", (user_id, data_str, h))
    conn.commit()
    
    # Also backup to atomic file for extra durability
    backup_path = Path(f"backups/session_{user_id}.json")
    backup_path.parent.mkdir(exist_ok=True)
    with AtomicFileWriter(str(backup_path)) as afw:
        afw.write(data_str, "Orchestrator_Agent", "OP-SCAFFOLD-BUILD@1.0.0")