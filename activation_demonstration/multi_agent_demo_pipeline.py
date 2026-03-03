# =====================================================
# FILE: multi_agent_demo_pipeline.py
# NAME: multi_agent_demo_pipeline.py
# PURPOSE: Passive multi-role demo toolkit.
# DETAILS: Refactored to remove top-down autonomous orchestration. Must be invoked by the Orchestrator_Agent.
# VERSION: 1.1.0
# ROBUSTNESS: Human-in-loop option; full audit at every step; uses all runtime toolkits.
# =====================================================

"""Multi-Agent Demo Toolkit – refactored for Orchestrator_Agent control."""

from .workflow_orchestrator import execute_pipeline
from .structured_logger import log_event

def run_demo(task: str = "Add long-term memory"):
    """
    Executes a demo pipeline.
    Invoked exclusively by the Orchestrator_Agent natively.
    """
    log_event("Orchestrator_Agent", "meta_orchestration", f"Starting demo task via toolkit: {task}")
    # Using official canonical role names
    results = execute_pipeline(["02_Genesis_Agent", "12_Verification_Agent", "Deployment_Agent"])
    print("🎬 Demo toolkit execution complete – results generated")
    return results

# NOTE: __main__ block removed to enforce protocol-centric orchestration.