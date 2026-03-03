---
protocol_id: OP-TERMINAL-WORKFLOW
version: 1.0.0
status: ACTIVE
date_created: 2026-03-03
date_modified: 2026-03-03
---
# Operational Protocol: Terminal Workflow (OP-TERMINAL-WORKFLOW)

**Purpose:** To maximize execution efficiency and minimize user workload by providing complete, chained commands with automated logging.

## 1. AI Command Generation Rules

- You MUST number every command header (e.g., 'Command 1: [Task]').
- You MUST provide full commands as single-line chained strings using `&&`.
- You MUST execute footers using explicitly defined `;` or `||` logic.
- You MUST start every command with a directory check and environment activation:
  - `cd <PROJECT_ROOT> && source <VENV_PATH>/bin/activate &&`
  - (Exception: Initial project creation or system info queries).
- You MUST STOP and request `<PROJECT_ROOT>` or `<VENV_PATH>` if they are undefined.

## 2. Mandatory Logging Protocol

- You MUST append output using `2>&1 | tee -a <LOG_PATH>`.
- You MUST echo a completion message: `$(date) | echo "=== [COMMAND_NAME] COMPLETED ===" 2>&1 | tee -a <LOG_PATH>`.
- **System Command 0:** You MUST overwrite the log file using `tee` (not `-a`) to reset the iteration context.
- You MUST redirect stdout to `/dev/null` for explicitly noisy commands while keeping errors (`2>> <LOG_PATH>`).

## 3. Error Handling & Safety

- You MUST include `|| echo "Error..."` chains to log failures.
- You MUST use `timeout` for long-running operations (default: 5 mins).
- You MUST use dry-runs (`--dry-run`) for destructive commands (e.g., `rm`, `sed`).
- You MUST log environment details (`python --version`, `pwd`) at the start of every session.

- You MUST possesses a standard "System Information" command block to capture:
    - OS version, Hardware specs, GPU status, Python version, Disk usage, and Uptime.
- You MUST anchor all system captures directly to the `MANIFEST_STATE.json` schema.

*Ventilated Prose Enforced | Protocol: OP-TERMINAL-WORKFLOW*
