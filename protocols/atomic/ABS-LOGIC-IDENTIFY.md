---
protocol_id: ABS-LOGIC-IDENTIFY
structure_status: HARDENED
target_audience: Verification_Agent, Genesis_Agent
assigned_role: System
purpose: Atomic tool for identifying and extracting unique logic fragments from source documentation for substrate ingestion.
behavior_dependencies:
  - "[BEH-AUDIT-DIMENSIONS-01](file:///home/jwils/.blueprints/governance/behaviors/BEH-AUDIT-DIMENSIONS-01.yaml) -- Purpose: Architectural dimension compliance."
version: 1.1.0
status: ACTIVE
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Absorption Protocol: Logic Identification (ABS-LOGIC-IDENTIFY)

## 1. Core Function & Rationale
This protocol scans a source document and identifies unique, non-redundant instructions or constraints that are missing from the current Blueprint infrastructure.

## 2. Universal Logic Frame (UAL-ABS)

### Phase 1: Logic Verification
- YOU MUST verify that all required parameters (e.g., file paths) are present in the input context.
- YOU MUST explicitly compare `date_created` strings of all merge or override candidates; the Senior artifact (oldest date) MUST be the implementation target.
- **Birthdate Authority:** The `date_created` field MUST be derived from the automated filesystem metadata (via `OPS-YAML-CREATED`). Manual overrides are forbidden.
- YOU MUST ingest the source document and the `Global_Protocol_Inventory`.
- YOU MUST perform a redundancy check; logic already functionally active in the substrate is skipped.
- YOU MUST extract "Pure Logistics" (instructions) and discard "Ventilation Prose" (explanations) not required for execution.

### Phase 2: Surgical Integration
- YOU MUST stage the extracted logic fragments in the `LOGIC_BUFFER`.
- YOU MUST normalize the syntax to conform to the **Universal Agent Logic (UAL)** standards.

### Phase 3: Integrity Lock
- YOU MUST emit the `LOGIC_MANIFEST.json` for sequential processing.
- YOU MUST flag the source document for `CONVERGENCE_ASSESSMENT`.

---
