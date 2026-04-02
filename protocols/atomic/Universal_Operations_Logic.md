---
protocol_id: N/A (Standard Anchor)
structure_status: CANONICAL
target_audience: All Agent Roles
assigned_role: System Architecture
purpose: Define the universal frontmatter and structural metadata standards for 
  atomic operations.
behavior_dependencies:
  - "[BEH-AUDIT-DIMENSIONS-01](file:///home/jwils/.blueprints/governance/behaviors/BEH-AUDIT-DIMENSIONS-01.yaml)
    -- Purpose: Architectural dimension compliance."
  - "[BEH-TERMINAL-TIMEOUT-01](file:///home/jwils/.blueprints/governance/behaviors/BEH-TERMINAL-TIMEOUT-01.yaml)
    -- Purpose: Mandatory terminal time-bounding."
protocol_dependencies:
  - "[UAL](file:///home/jwils/.blueprints/governance/roles/Universal_Agent_Logic.md)"
version: 1.1.0
status: ACTIVE
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Standard: Universal Operations Logic (UOL)

---

## 1. Definition of an Operation (OPS-XX-XX)

An **Operational Protocol** is a single-purpose, atomic unit of work within the agentic substrate. It is the "Action" component of the [Universal Agent Logic (UAL)](file:///home/jwils/.blueprints/governance/roles/Universal_Agent_Logic.md).

### 1.1 Atomic Scope
- **The 1:1 Rule (Quantum Atomicity):** An Operation MUST target exactly one (1) logical artifact or singular data transformation per execution. One protocol file MUST correspond to exactly one atomic action.
- **Behavioral Parity:** An Operation SHOULD implement logic defined in the [Behavioral Substrate](file:///home/jwils/.blueprints/governance/behaviors/) to ensure DRY compliance across role contexts.

## 2. Structural Requirements

Every `OPS-` protocol MUST adhere to the following logic frame:

### Phase 1: Input Validation
- YOU MUST verify that all required parameters (e.g., file paths, variables) are present in the input context.
- YOU MUST explicitly compare `date_created` strings of all merge or override candidates; the Senior artifact (oldest date) MUST be the implementation target.
- **Birthdate Authority:** The `date_created` field MUST be derived from the automated filesystem metadata (via `OPS-YAML-CREATED`). Manual overrides are forbidden.
- YOU MUST dissent and halt if input grounding is ambiguous or relies on "Ghost References".

### Phase 2: Tool/Script Execution
- YOU MUST execute the designated tool or terminal command pursuant to [OPS-TERMINAL-WORKFLOW](file:///home/jwils/.blueprints/governance/protocols/atomic/OPS-TERMINAL-WORKFLOW.md).
- YOU MUST enforce "Mandatory Timeout Prefixes" (Layer 2) for all raw terminal calls as defined in [BEH-TERMINAL-TIMEOUT-01](file:///home/jwils/.blueprints/governance/behaviors/BEH-TERMINAL-TIMEOUT-01.yaml).

### Phase 3: Rigid Output Emission
- YOU MUST emit the final state in one of two formats:
  - **Machine-Readable:** Structured JSON matching a predefined schema.
  - **Human-Readable:** Ventilated Prose (single statement per line) for markdown artifacts.
- **Orchestrational Transparency:** All calls to this protocol within a Sequence MUST be accompanied by the `purpose` summary from the YAML header.
- YOU MUST include the `protocol_id` and timestamp in the output metadata.

## 3. Atomic Error Handling
- **Failure:** If the operation fails, it MUST emit a standard `FAILURE_REPORT.json` containing the raw error log and current stack trace.
- **Retry Logic:** Internal retry logic is permitted ONLY for transient network/compute errors (max 3 attempts). Logical failures MUST be escalated to a Sequential supervisor.

---

## 4. Success Criteria for Atoms
1. **Idempotency:** Re-running the operation on the same input produces the exact same output.
2. **Side-Effect Isolation:** The operation only modifies the intended target; no global state shift occurs outside the `MANIFEST_STATE.json`.
