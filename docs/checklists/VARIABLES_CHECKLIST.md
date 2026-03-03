# VARIABLES_CHECKLIST.md

| Variable/Constant Name | Description                                            | File Name                                           | Line Numbers | Logging Integration |
|---                     |---                                                     |---                                                  |---           |---                  |
| PROMPTS_DIR            | Root path for role-prompt lookup and storage.          | activation_demonstration/prompt_library_manager.py  | 230          | None                |
| BLUEPRINT_ROOT         | Canonical anchor for toolkit and layer path injection. | frontend/communication_bus.py                       | 369          | None                |
| DB_PATH                | Filename for the persistent SQLite session store.      | frontend/session_manager.py                         | 769          | None                |
| PII_PATTERNS           | Regex dictionary for PII redaction (email, key, IP).   | frontend/security_gateway.py                        | 707-711      | None                |
| INJECTION_PATTERNS     | List of strings for prompt-injection sanitization.     | toolkits/audit_onboarding/search_copy.py            | N/A          | None                |
| LOG_LEVEL_MAP          | Mapping of string levels to numeric values for tuning. | toolkits/runtime_observability/structured_logger.py | N/A          | None                |
