---
protocol_id: OP-SUBSTRATE-ASSIMILATE
structure_status: HARDENED
target_audience: Genesis_Agent, Orchestrator_Agent, Verification_Agent
assigned_role: Genesis_Agent
purpose: Methodically reformat both Junior Agent Roles and Junior Protocols to match the UPH Anchor.
version: 1.1.0
status: ACTIVE
date_created: 2026-03-03
date_modified: 2026-03-03
---
# Operational Protocol: Substrate Assimilation (OP-SUBSTRATE-ASSIMILATE)

**Context:** This protocol replaces the legacy `OP-AGENT-ASSIMILATE` by expanding the "Anti-Corruption" logic to the entire Protocol Substrate. It ensures all roles and protocols adhere to a singular structural anchor (UPH).

## 1. Trigger Conditions
- Flagged by `Verification_Agent` (12) during context ingestion or workspace audit.
- Intercepted by `Orchestrator_Agent` (00) during task assembly.
- Strictly contingent on `substrate_seniority_validator.py` (formerly `role_seniority_validator.py`) returning `REFORMAT_REQUIRED: True`.

## 2. The Universal 3-Cycle Reformatting Loop
The `Genesis_Agent` (10) MUST execute these cycles sequentially for ANY flagged `.md` file in `@roles/` or `@protocols/`:

### Cycle 1: Universal Protocol Header (UPH) Injection
- **Check:** Compare the document's frontmatter against the `Universal_Protocol_Header.md` standard.
- **Mandatory Fields:** `protocol_id`, `structure_status`, `target_audience`, `assigned_role`, `purpose`, `version`, `status`, `date_created`, `date_modified`.
- **Action:** Inject or remap missing/legacy headers. Use "N/A (Agent Role)" if mapping an agent role. Ensure `structure_status` is updated to `HARDENED` after processing.

### Cycle 2: Logical Re-sequencing
- **Check:** Evaluate the order of operations and structural components.
- **Protocol:** Enforce the "Preparation -> Safety -> Action" sequence where applicable.
- **Action:** Re-order bullet points and paragraphs. Move negative safety constraints (e.g., "NEGATIVE CONSTRAINTS") prior to active generative logic.

### Cycle 3: Verification & Grounding
- **Check:** Run `OP-RISK-AUDIT` on the reformatted candidate document.
- **Action:** Verify that "Ventilated Prose" (single statement per line) is strictly enforced for the main body.
- **Termination:** If `OP-RISK-AUDIT` passes with zero Critical/High findings, the assimilation is complete.

## 3. Orchestration State Handoff
- Upon completion, `Orchestrator_Agent` MUST:
  1. Overwrite the legacy Junior file with the hardened version.
  2. Clear the `ASSIMILATION_REQUIRED` flag.
  3. **Resume Task:** Restore from `PIPELINE_STACK` and re-execute the original user command.
  4. Notify Logs: "Substrate Hardening remediated. Resuming [Original Task]..."
