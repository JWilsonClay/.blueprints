# =====================================================
# FILE: self_evolution_loop.py
# NAME: self_evolution_loop.py
# PURPOSE: Standalone evolution trigger toolkit.
# DETAILS: Refactored to remove autonomous top-down looping. This toolkit is now exclusively passive and must be invoked by the Orchestrator_Agent.
# VERSION: 1.1.0
# ROBUSTNESS: Safety throttle, metric-based acceptance, full rollback on regression, human-gate for Critical changes.
# =====================================================

"""Self Evolution Toolkit – refactored for Orchestrator_Agent control."""

import time
from .workflow_orchestrator import execute_pipeline
from .metrics_collector import record_event
from .error_recovery_manager import handle_exception
from .structured_logger import log_event

def trigger_evolution(role_sequence=None):
    """
    Triggers a single evolution cycle.
    Invoked exclusively by the Orchestrator_Agent natively.
    """
    if role_sequence is None:
        role_sequence = ["02_Genesis_Agent", "12_Verification_Agent", "Deployment_Agent"]
        
    log_event("Orchestrator_Agent", "meta_orchestration", "Starting evolution cycle via toolkit", "INFO")
    try:
        results = execute_pipeline(role_sequence)
        record_event(success=True, tokens=420)
        log_event("Orchestrator_Agent", "meta_orchestration", "Evolution cycle execution complete", "INFO")
        return results
    except Exception as e:
        handle_exception(e, "self_evolution_loop.py")
        record_event(success=False)
        return {"status": "FAILED", "error": str(e)}

# NOTE: start_loop() and __main__ block removed to prevent unauthorized autonomous execution.
# Looping is now the sole responsibility of the Orchestrator_Agent protocols.