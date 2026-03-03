# FUNCTIONS_CHECKLIST.md

| Function Name     | Description                                      | File Name                                          | Line Numbers | Logging Integration                       |
|---                |---                                               |---                                                 |---           |---                                        |
| main              | CLI entry point and command dispatcher.          | activation_demonstration/agentic_cli.py            | 37-71        | INFO on command; structured_logger        |
| bootstrap         | Creates project directories and initial files.   | activation_demonstration/system_bootstrapper.py    | 324-339      | INFO on setup; health_dashboard_generator |
| package           | Bundles files and generates provenance manifest. | activation_demonstration/production_packager.py    | 200-205      | INFO on completion; None                  |
| load_prompt       | Retrieves versioned prompts from library.        | activation_demonstration/prompt_library_manager.py | 232-236      | None                                      |
| trigger_evolution | Initiates a single evolution cycle.              | activation_demonstration/self_evolution_loop.py    | 268-285      | INFO on cycle; structured_logger          |
| publish           | Sends validated messages to the bus.             | frontend/communication_bus.py                      | 392-424      | INFO on payload; structured_logger        |
| subscribe         | Registers callbacks for specific channels.       | frontend/communication_bus.py                      | 425-426      | None                                      |
| deploy            | Rollout gatekeeper for production releases.      | frontend/deployment_orchestrator.py                | 481-504      | ERROR on block; structured_logger         |
| record_feedback   | Persists agent performance signals.              | frontend/feedback_aggregator.py                    | 543-553      | INFO on avg; metrics_collector            |
| sanitize_payload  | Scrubs PII from agent communications.            | frontend/security_gateway.py                       | 713-718      | None                                      |
| get_session       | Retrieves user state with hash verification.     | frontend/session_manager.py                        | 783-792      | None                                      |
| update_session    | Atomic state mutation for sessions.              | frontend/session_manager.py                        | 794-800      | None                                      |
| run_audit         | Main entry point for OP-RISK-AUDIT execution.    | toolkits/dependency/audit_engine.py                | N/A          | None                                      |
| atomic_write      | Context manager for safe file writes.            | toolkits/dependency/core_utils.py                  | N/A          | None                                      |
