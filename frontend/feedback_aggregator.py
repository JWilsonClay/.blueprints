# =====================================================
# FILE: feedback_aggregator.py
# NAME: feedback_aggregator.py
# PURPOSE: Collects success/failure signals and feeds to backend.
# DETAILS: Wired to session_manager for persistence.
# VERSION: 1.0.1
# =====================================================

"""Feedback Aggregator – cross-agent learning loop."""

import sys
from pathlib import Path
from typing import Dict
from collections import deque

# Path injection
BLUEPRINT_ROOT = Path(__file__).parent.parent
if str(BLUEPRINT_ROOT) not in sys.path:
    sys.path.append(str(BLUEPRINT_ROOT))

try:
    from toolkits.runtime_observability.metrics_collector import record_event
    from toolkits.runtime_observability.structured_logger import log_event
except ImportError:
    def record_event(**kwargs): pass
    def log_event(agent, layer, msg, level="INFO"): pass

from .session_manager import update_session

feedback_history = deque(maxlen=1000)

def record_feedback(user_id: str, agent: str, score: float, context: Dict):
    """Log feedback and persist to session."""
    entry = {"agent": agent, "score": score, "context": context, "timestamp": datetime.utcnow().isoformat()}
    feedback_history.append(entry)
    
    # Persist to session
    update_session(user_id, {"feedback_log": list(feedback_history)})
    
    avg = sum(f["score"] for f in feedback_history) / len(feedback_history)
    log_event("FeedbackAggregator", "frontend_layer", f"Updated learning loop. Avg: {avg:.2f}")
    record_event(success=score > 0.7, tokens=0)

from datetime import datetime

# API
def intake_feedback(uid: str, score: float, reqs: int): record_feedback(uid, "Intake", score, {"reqs": reqs})
def planning_feedback(uid: str, score: float, steps: int): record_feedback(uid, "Planning", score, {"steps": steps})
def interactive_feedback(uid: str, score: float, fixes: int): record_feedback(uid, "Interactive", score, {"fixes": fixes})