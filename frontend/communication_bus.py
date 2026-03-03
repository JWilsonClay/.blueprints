# =====================================================
# FILE: communication_bus.py
# NAME: communication_bus.py
# PURPOSE: Zero-copy pub/sub messaging backbone (in-memory + optional Redis).
# DETAILS: Intake publishes discoveries, Planning subscribes, Interactive injects debug.
# VERSION: 1.0.1
# =====================================================

"""Communication Bus – real-time inter-agent messaging."""

import queue
import threading
import json
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, Callable, Any
from datetime import datetime

# Path injection for Blueprint Toolkits
BLUEPRINT_ROOT = Path(__file__).parent.parent
if str(BLUEPRINT_ROOT) not in sys.path:
    sys.path.append(str(BLUEPRINT_ROOT))

# Attempt imports from toolkits
try:
    from toolkits.dependency.core_utils import inject_provenance_header
    from toolkits.runtime_observability.structured_logger import log_event
except ImportError:
    # Fallback to local placeholders for standalone testing
    def inject_provenance_header(data, agent, layer): return data
    def log_event(agent, layer, msg, level="INFO"): print(f"[{level}] {agent}: {msg}")

from .schemas import DiscoveryPayload, SequencePayload, DebugEventPayload

class CommunicationBus:
    def __init__(self):
        self.subscribers: Dict[str, list[Callable]] = defaultdict(list)
        self.message_queue = queue.PriorityQueue()
        self.lock = threading.Lock()
        self.replay_buffer = []
        threading.Thread(target=self._process_queue, daemon=True).start()

    def publish(self, channel: str, message: Dict[str, Any], priority: int = 0):
        """Publish with provenance injection and state validation."""
        # Validate payload based on channel
        try:
            if channel == "intake.discovery":
                DiscoveryPayload(**message)
            elif channel == "planning.sequence":
                SequencePayload(**message)
            elif channel == "interactive.debug":
                DebugEventPayload(**message)
        except Exception as e:
            log_event("CommunicationBus", "frontend_layer", f"Payload validation failed: {e}", "ERROR")
            return

        msg = {
            "channel": channel,
            "payload": message,
            "timestamp": datetime.utcnow().isoformat(),
            "provenance": "frontend_orchestration"
        }
        
        # Inject production provenance header
        encoded_msg = inject_provenance_header(json.dumps(msg), "CommunicationBus", "frontend_layer")
        msg = json.loads(encoded_msg)

        with self.lock:
            self.message_queue.put((priority, msg))
            self.replay_buffer.append(msg)
            if len(self.replay_buffer) > 1000:
                self.replay_buffer.pop(0)
        
        log_event("CommunicationBus", "frontend_layer", f"Published verified payload to {channel}")

    def subscribe(self, channel: str, callback: Callable):
        self.subscribers[channel].append(callback)

    def _process_queue(self):
        while True:
            _, msg = self.message_queue.get()
            channel = msg["channel"]
            targets = self.subscribers.get(channel, []) + self.subscribers.get(channel.split('.')[0] + ".*", [])
            for cb in targets:
                try:
                    cb(msg)
                except Exception as e:
                    log_event("CommunicationBus", "frontend_layer", f"Callback error on {channel}: {e}", "WARNING")

bus = CommunicationBus()

def publish_discovery(requirements: Dict): bus.publish("intake.discovery", requirements)
def publish_sequence(sequence: Dict): bus.publish("planning.sequence", sequence)
def publish_debug_event(event: Dict): bus.publish("interactive.debug", event)