# =====================================================
# FILE: real_time_collaborator.py
# NAME: real_time_collaborator.py
# PURPOSE: WebSocket sync for agents and human browser.
# DETAILS: Subscribes to communication_bus.
# VERSION: 1.0.1
# =====================================================

"""Real-Time Collaborator – live sync for frontend agents."""

import sys
import asyncio
from pathlib import Path
from typing import Dict
from fastapi import FastAPI, WebSocket

# Path injection
BLUEPRINT_ROOT = Path(__file__).parent.parent
if str(BLUEPRINT_ROOT) not in sys.path:
    sys.path.append(str(BLUEPRINT_ROOT))

try:
    from .communication_bus import bus
    from .security_gateway import validate_request
except ImportError:
    # Handle direct execution if needed
    pass

app = FastAPI(title="Agentic Frontend Collaborator")
connected = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected.append(websocket)
    try:
        while True:
            # Heartbeat logic could go here
            await asyncio.sleep(10)
    finally:
        connected.remove(websocket)

def broadcast(event: Dict):
    """Secure broadcast to all connected clients."""
    for ws in connected[:]:
        try:
            # Optional: validate_request here if specific user scopes required
            asyncio.create_task(ws.send_json(event))
        except:
            pass

def on_bus_message(msg: Dict):
    broadcast(msg)

# Global subscriptions
bus.subscribe("intake.*", on_bus_message)
bus.subscribe("planning.*", on_bus_message)
bus.subscribe("interactive.*", on_bus_message)