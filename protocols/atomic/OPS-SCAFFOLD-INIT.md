---
protocol_id: OPS-SCAFFOLD-INIT
structure_status: HARDENED
target_audience: Genesis_Agent, Orchestrator_Agent
assigned_role: System
purpose: Atomic protocol for initializing substrate scaffolding based on templates.
behavior_dependencies:
  - "[BEH-AUDIT-DIMENSIONS-01](file:///home/jwils/.blueprints/governance/behaviors/BEH-AUDIT-DIMENSIONS-01.yaml) -- Purpose: Structural generation compliance."
version: 1.1.0
status: ACTIVE
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Operational Protocol: Scaffold Initialization (OPS-SCAFFOLD-INIT)

## 1. Core Function & Rationale
This protocol generates the foundational directory structures and file scaffolding for new agentic substrates, ensuring UAL and UPH compliance from birth.

## 2. Universal Logic Frame (UOL)

### Phase 1: Input Validation
- YOU MUST verify the presence of `ARCHITECTURE_REQUIREMENTS`.
- YOU MUST explicitly compare `date_created` strings of all merge or override candidates; the Senior artifact (oldest date) MUST be the implementation target.
- **Birthdate Authority:** The `date_created` field MUST be derived from the automated filesystem metadata (via `OPS-YAML-CREATED`).

### Phase 2: Tool Execution
- YOU MUST invoke `toolkits/dependency/file_generator.py` to expand templates.
- YOU MUST enforce strict compliance with [Universal Protocol Header (UPH)].

### Phase 3: Rigid Output Emission
- YOU MUST emit verifiable `<DOC_DIFF>` blocks showing the generated scaffolding.
- **Orchestrational Transparency:** All calls MUST include the purpose summary from the YAML header.

---
