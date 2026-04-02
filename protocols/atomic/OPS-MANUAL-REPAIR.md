---
protocol_id: OPS-MANUAL-REPAIR
structure_status: HARDENED
target_audience: Verification_Agent, Orchestrator_Agent
assigned_role: System
purpose: Atomic tool for precision repair of logical errors and hallucinations.
version: 1.2.0
status: ACTIVE
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Operational Protocol: Manual/Precision Repair (OPS-MANUAL-REPAIR)

## 1. Core Function & Rationale
This protocol governs the interactive repair of logical errors and hallucinations, prioritizing surgical precision over broad refactoring to minimize side effects.

## 2. Universal Logic Frame (UOL)

### Phase 1: Input Validation
- YOU MUST verify the presence of all required error context parameters.
- YOU MUST explicitly compare `date_created` strings of all merge or override candidates; the Senior artifact (oldest date) MUST be the implementation target.
- **Birthdate Authority:** The `date_created` field MUST be derived from the automated filesystem metadata (via `OPS-YAML-CREATED`).
- YOU MUST verify the specific `TARGET_FILENAME`, `ERROR_LOG`, and `ORIGINAL_INTENT`.
- YOU MUST verify that the target file is writable and not locked by another process.
- IF the request is for a broad refactor (> 50 lines), YOU MUST dissent and redirect to `SEQ-PRECISION-SURGERY`.

### Phase 2: Tool/Script Execution
- **Surgical Edit:** YOU MUST execute the edit using a single, atomic `<DOC_DIFF>` block.
- **De-Duplication:** IF removing redundant code, YOU MUST provide the original reference block for grounding.
- YOU MUST publish debug events via `communication_bus.publish_debug_event`.
- YOU MUST prefix terminal commands with `timeout` as per `OPS-TERMINAL-WORKFLOW`.

### Phase 3: Rigid Output Emission
- YOU MUST provide exactly one fix per interaction cycle.
- YOU MUST emit the corrected `<DOC_DIFF>` strictly to the `Precision_Agent` for verification.
- YOU MUST provide a "Dissent" flag if a repair request violates system integrity.

## 3. Atomic Error Handling
- **Failure:** If the diff application fails, emit `REPAIR_FAIL.json` and restore the file from `BACKUP_STATE`.
- **Recovery:** Re-audit the error log and seek human intervention if logic collisions persist.

---
