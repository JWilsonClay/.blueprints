# Gap Report: Methodical Role Assimilation Protocol (OP-AGENT-ASSIMILATE)

## 1. Executive Summary
**Status:** REQUIRED (Architectural Hardening)
**Objective:** To establish a dedicated protocol that methodically reformats newer (Junior) Agent Role files to match the structural patterns of established (Senior) files. This prevents "Format Corruption" where new, loosely formatted roles inadvertently signal a change in direction to the LLM, causing it to degrade the quality of senior substrate files.

## 2. Identified Gap: The "Assimilation Vacuum"
While **OP-RISK-AUDIT (Dimension 08: Seniority)** acts as a passive safeguard (identifying corruption), and **Dimension 07.5 (ABSORB)** determines the integration route, there is no active mechanism to *force* a non-compliant junior file into the senior mold via methodical re-sequencing.

### Severity: High (Structural Risk)
Without this protocol, the ecosystem's "Canonical Pattern" is vulnerable to drift. As more agents are added, the LLM may begin to default to the shortest/simplest role format it sees, effectively "forgetting" the senior constraints of the Orchestrator or Verification agent.

## 3. Implementation Requirements (Architecture)

### A. The Seniority Trigger (The Wire)
The protocol MUST be wired to **OP-RISK-AUDIT (D8)**. 
- **Detection:** During a Tier 2 (Directory) or Tier 3 (Workspace) audit, the LLM MUST call [toolkits/audit_onboarding/role_seniority_validator.py](file:///home/jwils/GoogleDrive1TB/PapiBobes/.blueprints/toolkits/audit_onboarding/role_seniority_validator.py) to compare a flagged Junior file against a hardened Senior file.
- **Rule:** The `ASSIMILATION_REQUIRED` flag is strictly contingent on the Python script returning a `REFORMAT_REQUIRED: True` result. 
- **Hallucination Defense:** If the LLM perceives a mismatch but the script validates the dates/structure as compliant, the flag MUST NOT be raised. This ensures empirical grounding.
- **Trigger:** Flagged by the Verification Agent (12).

### B. The Orchestrator Handoff
Pursuant to **OP-ORCHESTRATE-META**, the Orchestrator MUST:
1. Halt the primary development pipeline.
2. Ingest the Junior file as the "Patient" and the Senior Role (e.g., 00 Orchestrator) as the "Template".
3. Invoke the new **OP-AGENT-ASSIMILATE** protocol.

### C. The Assimilation Loop (Safe Re-integration)
The protocol MUST execute up to three (3) cycles of reformatting:
1. **Cycle 1: Structural Injection.** Injects missing mandatory headers (Target Audience, Required Attributes, Flow Labels).
2. **Cycle 2: Logical Re-sequencing.** Re-orders itemized resources to match the Preparation -> Safety -> Action flow defined in the senior substrate.
3. **Cycle 3: Verification Audit.** Re-runs `OP-RISK-AUDIT` on the patient. If D8 variance persists, escalate to `OP-MANUAL-REPAIR` (The Precision Agent).

## 4. Integration with ABSORB (Dimension 07.5)
The safest route for assimilation utilizes **Dimension 07.5 Logic**:
- **Condition:** "Merge into Existing Artifact" MUST be avoided if the Junior file represents a new Agent Role. 
- **Action:** Instead, "Create New Substrate Artifact" logic is modified to "Hardened/Reformatted Role Generation," ensuring the new file is essentially a *New* file with the *Old* intention, effectively purging the un-audited format from the history.

## 5. Success Metrics
- 100% adherence to the "Ventilated Prose" rule.
- 0% Ghost Reference drift between Senior and Junior roles.
- Mandatory presence of the 7 Robustness Attributes in all role files.
- Identical Markdown Hierarchy (H1 Agent, H2 sections) across all files in `.blueprints/roles/`.

## 6. Execution Directives for Genesis Agent
1. Scaffold `protocols/role_assimilation_protocol.md` (OP-AGENT-ASSIMILATE).
2. Assign Primary Role: **Verification_Agent** (12).
3. Assign Secondary Orchestration: **Orchestrator_Agent** (00).
4. Update **Wiring_Diagram_v1.0.md** to include the "Assimilation Loop" as a sub-routine of the Safety Layer.
