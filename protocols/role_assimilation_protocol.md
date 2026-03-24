---
protocol_id: OP-AGENT-ASSIMILATE
structure_status: HARDENED
target_audience: Verification_Agent, Orchestrator_Agent
assigned_role: System
purpose: **DEPRECATED** | Superseded by OP-SUBSTRATE-ASSIMILATE. This protocol has been absorbed into the universal substrate hardening layer.
version: 1.0.0
status: DEPRECATED
date_created: 2026-03-03
date_modified: 2026-03-03
supersedes: []
---

# [DEPRECATED] Operational Protocol: Role Assimilation (OP-AGENT-ASSIMILATE)

**Context:** This protocol is NO LONGER AUTHORITATIVE. 
Please refer to [OP-SUBSTRATE-ASSIMILATE](file:///home/jwils/GoogleDrive1TB/PapiBobes/.blueprints/protocols/substrate_assimilation_protocol.md) for all role and protocol reformatting cycles.

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
