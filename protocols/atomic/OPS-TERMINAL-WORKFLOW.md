---
protocol_id: OPS-TERMINAL-WORKFLOW
structure_status: HARDENED
target_audience: Verification_Agent, Orchestrator_Agent
assigned_role: System
purpose: Atomic tool for maximizing terminal efficiency with chained commands and logging.
version: 1.1.0
status: ACTIVE
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Operational Protocol: Terminal Workflow (OPS-TERMINAL-WORKFLOW)

## 1. Core Function & Rationale
This protocol provides the terminal execution standard for the agentic substrate, ensuring command chaining, environment isolation, and mandatory logging.

## 2. Universal Logic Frame (UOL)

### Phase 1: Input Validation
- YOU MUST verify that all required environment parameters are present.
- YOU MUST explicitly compare `date_created` strings of all merge or override candidates; the Senior artifact (oldest date) MUST be the implementation target.
- **Birthdate Authority:** The `date_created` field MUST be derived from the automated filesystem metadata (via `OPS-YAML-CREATED`).
- YOU MUST verify the presence of `<PROJECT_ROOT>` and `<VENV_PATH>`.
- YOU MUST verify the presence of a writable `<LOG_PATH>`.
- YOU MUST identify if the command is "Destructive" (e.g., `rm`, `sed`).

### Phase 2: Tool/Script Execution
- **Command Construction:** YOU MUST number every command and provide full chains using `&&`.
- **Environment Isolation:** YOU MUST start with `cd <PROJECT_ROOT> && source <VENV_PATH>/bin/activate`.
- **Mandatory Timeout (Layer 2):** YOU MUST prefix EVERY command with `timeout 60s` (Max 300s).
- **Safe Execution:** YOU MUST use `--dry-run` for all destructive operations.
- **Logging:** YOU MUST append output to the log file via `2>&1 | tee -a <LOG_PATH>`.

### Phase 3: Rigid Output Emission
- YOU MUST echo a standard completion message: `$(date) | [COMMAND_NAME] COMPLETED`.
- YOU MUST update the `MANIFEST_STATE.json` with the latest system information (OS, Python Version, Disk Usage).
- YOU MUST emit the final execution status (SUCCESS/FAILURE) to the `Orchestrator_Agent`.

## 3. Atomic Error Handling
- **Failure:** IF a command in a chain fails, YOU MUST echo "Error..." and halt the chain to prevent cascading breakage.
- **Recovery:** Provide a diagnostic command (e.g., `ls -R`, `tail -n 50 <LOG_PATH>`) to investigate environment state.

---
