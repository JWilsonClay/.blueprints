---
protocol_id: OP-AGENT-ASSIMILATE
version: 1.0.0
status: ACTIVE
date_created: 2026-03-03
---
# Operational Protocol: Role Assimilation (OP-AGENT-ASSIMILATE)

**Purpose:** To methodically reformat "Junior" agent roles to match the structural patterns of "Senior" substrate anchors, preventing format pollution and logic drift.

## 1. Trigger Conditions
- Flagged by `Verification_Agent` (12) during context ingestion or workspace audit.
- Strictly contingent on `role_seniority_validator.py` returning `REFORMAT_REQUIRED: True`.

## 2. The 3-Cycle Reformatting Loop
The `Genesis_Agent` (or `Precision_Agent`) MUST execute these cycles sequentially:

### Cycle 1: Structural Injection
- **Check:** Compare headers against the Senior Template (e.g., Orchestrator/Verification Agent).
- **Mandatory Fields:** YAML Frontmatter (with `date_created`), Role Overview, Flow Labels, Interface Definitions.
- **Action:** Inject missing headers using the exact wording found in Senior files.

### Cycle 2: Logical Re-sequencing
- **Check:** Evaluate the order of operations.
- **Protocol:** Enforce the "Preparation -> Safety -> Action" sequence.
- **Action:** Re-order bullet points and paragraphs to ensure Safety constraints (e.g., "NEGATIVE CONSTRAINTS") are positioned before Action directives.

### Cycle 3: Verification & Grounding
- **Check:** Run `OP-RISK-AUDIT` on the reformatted candidate.
- **Action:** Verify that "Ventilated Prose" (single statement per line) is strictly enforced.
- **Termination:** If `OP-RISK-AUDIT` passes with zero Critical/High findings, the assimilation is complete.

## 3. Orchestration Handoff & Resumption
- Upon completion, `Orchestrator_Agent` MUST:
  1. Replace the legacy Junior file with the hardened version.
  2. Clear the `ASSIMILATION_REQUIRED` flag.
  3. **Resume Task:** Re-execute the original user command (from the saved context stack).
  4. Notify the user: "Substrate Seniority Gap remediated. Resuming [Original Task]..."
