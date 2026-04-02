---
protocol_id: SEQ-SUBSTRATE-COMP
structure_status: HARDENED
target_audience: Verification_Agent, Orchestrator_Agent
assigned_role: System
purpose: Enforce a standardized, 12-checklist schema for substrate auditing and mapping.
version: 1.1.0
status: ACTIVE
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Sequential Protocol: Substrate Core Components (SEQ-SUBSTRATE-COMP)

## 1. Core Function & Rationale
This protocol mandates the generation of 12 distinct checklist files, ensuring exhaustive mapping of all mechanical and logical components within the substrate.

## 2. Universal Logic Frame (USL)

### Phase 1: Stage Initialization
- YOU MUST establish the "Orchestration Frame" by ingesting the source manifest.
- YOU MUST verify target directory `docs/checklists/` exists and is writable.
- YOU MUST initialize the `CHECKLIST_MEMORY` to track mapping completion.

### Phase 2: Multi-Stage Execution
- **Step 1: Element Mapping:** YOU MUST systematically map manifest elements to the relevant `*_CHECKLIST.md` file (Features, Functions, Classes, etc.).
- **Step 2: Table Formating:** YOU MUST execute `table_formatter.py` to ensure Ventilated Prose and row alignment.
- **Step 3: State Injection:** YOU MUST update the `MANIFEST_STATE.json` with the current project and architecture metadata.
- YOU MUST update `MANIFEST_STATE.json` after the successful generation of all 12 checklists.

### Phase 3: Recursive Refinement (Cleanup)
- YOU MUST execute an "Audit of Trivialities" to ensure every function/variable/class has been mapped.
- YOU MUST purge ad-hoc mapping notes and temporary table row fragments.

## 3. Negative Constraints
- **Do Not Hallucinate**: If logging is missing, write "None".
- **Do Not Consolidate**: Each logical entity must occupy exactly one physical line.
- **Do Not Redefine Formatting**: Adhere strictly to the standard USL tabular schema.

---
