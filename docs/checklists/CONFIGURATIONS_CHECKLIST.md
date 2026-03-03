# CONFIGURATIONS_CHECKLIST.md

| Config Name                | Description                                              | File Name                                      | Line Numbers | Logging Integration |
|---                         |---                                                       |---                                             |---           |---                  |
| environment_vars           | Global settings for DB_URL, LOG_LEVEL, and API_KEY.      | [TARGET_ROOT]/.env                             | N/A          | structured_logger   |
| role_definitions           | Behavior and dependency metadata for Macro-Agents.       | roles/*.md                                     | 1-11         | None                |
| protocol_operational_rules | Machine-readable constraints for workflows.              | protocols/*.md                                 | 1-6          | None                |
| prompt_library             | Versioned behavioral templates for agentic reasoning.    | prompt_library/*.txt                           | N/A          | None                |
| session_db                 | Persistent storage and runtime state for frontend users. | frontend_sessions.db                           | N/A          | None                |
| metrics_state              | Aggregated performance and token usage snapshots.        | toolkits/dependency/METRICS_STATE_PAYLOAD.json | N/A          | None                |
| audit_state                | Shared ground-truth findings from static analysis.       | toolkits/dependency/AUDIT_STATE_PAYLOAD.json   | N/A          | None                |
