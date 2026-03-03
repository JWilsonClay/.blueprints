# =====================================================
# FILE: agentic_cli.py
# NAME: agentic_cli.py
# PURPOSE: Passive entry-point CLI tool (python -m agentic_cli).
# DETAILS: Refactored to act as a command dispatcher for the Orchestrator_Agent.
# DETAILS: Removes autonomous decision-making.
# VERSION: 1.1.0
# ROBUSTNESS: Provenance-stamped.
# ROBUSTNESS: audited via audit_engine.py.
# ROBUSTNESS: logged via structured_logger.py.
# =====================================================

"""Agentic CLI – passive dispatcher toolkit."""

import argparse
import sys
from pathlib import Path
from .structured_logger import log_event
from .system_bootstrapper import bootstrap
from .self_monitor_dashboard import start_dashboard
from .agent_runner import run_scaffold
from .multi_agent_demo_pipeline import run_demo

def main():
    parser = argparse.ArgumentParser(
        prog="agentic_cli",
        description="Agentic AI Platform Toolkit"
    )
    sub = parser.add_subparsers(dest="command", required=True)
    
    sub.add_parser("bootstrap", help="One-command system setup")
    run_p = sub.add_parser("run", help="Run a scaffold")
    run_p.add_argument("scaffold", help="Path to scaffold file")
    sub.add_parser("monitor", help="Launch live dashboard")
    sub.add_parser("evolve", help="Trigger one evolution cycle")
    sub.add_parser("health", help="Show system health")
    
    args = parser.parse_args()
    
    # CLI now logs as a toolkit event on behalf of the Orchestrator_Agent
    log_event("Orchestrator_Agent", "meta_orchestration", f"CLI Toolkit invoked: {args.command}", "INFO")
    
    if args.command == "bootstrap":
        bootstrap()
    elif args.command == "run":
        run_scaffold(args.scaffold)
    elif args.command == "monitor":
        start_dashboard()
    elif args.command == "evolve":
        from .self_evolution_loop import trigger_evolution
        trigger_evolution()
    elif args.command == "health":
        print(Path("PROJECT_HEALTH.md").read_text(encoding="utf-8", errors="ignore"))
    else:
        print(f"✅ {args.command} execution complete")

if __name__ == "__main__":
    main()