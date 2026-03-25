---
protocol_id: SEQ-SUBSTRATE-ASSIMILATE
structure_status: HARDENED
target_audience: Genesis_Agent, Orchestrator_Agent, Verification_Agent
assigned_role: Genesis_Agent
purpose: Methodically reformat Junior Agent Roles and Junior Protocols to match the UPH Anchor.
version: 1.1.0
status: ACTIVE
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Sequential Protocol: Substrate Assimilation (SEQ-SUBSTRATE-ASSIMILATE)

## 1. Core Function & Rationale
This protocol ensures all roles and protocols adhere to a singular structural anchor (UPH) and follow the Universal Agent Logic (UAL) flow.

## 2. Universal Logic Frame (USL)

### Phase 1: Stage Initialization
- YOU MUST establish the "Orchestration Frame" by verifying the seniority validator result.
- YOU MUST initialize the `PIPELINE_STACK` with current state before reformatting.
- YOU MUST identify target artifacts in `@roles/` or `@protocols/`.

### Phase 2: Multi-Stage Execution
- **Cycle 1: UPH Injection:** YOU MUST inject or remap frontmatter to match the `Universal_Protocol_Header.md` standard.
- **Cycle 2: Logical Re-sequencing:** YOU MUST enforce the "Preparation -> Safety -> Action" sequence.
- **Cycle 3: Logic Anchor Injection:** YOU MUST inject UOL/USL Phase 1/2/3 logic frames into the target artifact.
- YOU MUST update `MANIFEST_STATE.json` upon completion of each reformatting cycle.

### Phase 3: Recursive Refinement (Cleanup)
- YOU MUST execute a "Final Integrity Audit" (via `OPS-RISK-AUDIT`) on the reformatted document.
- **Substrate Hygiene:**
  - YOU MUST perform "Substrate Hygiene" by purging legacy artifacts and outdated headers.
  - **Pre-emptive Purge:** YOU MUST identify the source Gap Report or Audit document that triggered this assimilation and, if fully implemented, move it to `docs/archived/` or purge it pursuant to [SEQ-SUBSTRATE-HYGIENE](file:///home/jwils/.blueprints/governance/protocols/sequential/SEQ-SUBSTRATE-HYGIENE.md).
- YOU MUST resume the original task from the `PIPELINE_STACK`.

## 3. State Handoff
- Upon completion, YOU MUST notify the `Orchestrator_Agent` to clear the `ASSIMILATION_REQUIRED` flag.

---
