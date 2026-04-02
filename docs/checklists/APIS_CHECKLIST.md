# APIS_CHECKLIST.md

| API/Endpoint Name   | Description                                        | File Name                                          | Line Numbers | Logging Integration               |
|---                  |---                                                 |---                                                 |---           |---                                |
| /ws                 | WebSocket endpoint for real-time agent/human sync. | frontend/realtime_collaborator.py                  | 599-608      | None                              |
| CLI: bootstrap      | One-command system setup via agentic_cli.          | activation_demonstration/agentic_cli.py            | 56-57        | INFO; structured_logger           |
| CLI: run [scaffold] | Resource execution via agentic_cli.                | activation_demonstration/agentic_cli.py            | 58-59        | INFO; structured_logger           |
| CLI: health         | Real-time health dashboard display.                | activation_demonstration/agentic_cli.py            | 65-66        | None                              |
| load_prompt         | Versioned role prompt retrieval from library.      | activation_demonstration/prompt_library_manager.py | 232-236      | None                              |
| publish_discovery   | Requirements broadcast for Intake agents.          | frontend/communication_bus.py                      | 441          | INFO; structured_logger           |
| publish_sequence    | Sequence broadcast for Planning agents.            | frontend/communication_bus.py                      | 442          | INFO; structured_logger           |
| deploy              | Rollout trigger with safety gate validation.       | frontend/deployment_orchestrator.py                | 481-504      | ERROR on block; structured_logger |
| record_feedback     | Performance score ingestion for learning loops.    | frontend/feedback_aggregator.py                    | 543-553      | INFO; structured_logger           |
