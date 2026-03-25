---
protocol_id: OPS-RISK-AUDIT
structure_status: HARDENED
target_audience: Verification_Agent, Orchestrator_Agent
assigned_role: System
purpose: Atomic protocol for detecting and neutralizing patterns causing hallucinations or instructions loops.
version: 1.2.0
status: ACTIVE
changelog:
- 1.1.0: UOL Structural Alignment (Phase 1/2/3).
- 1.2.0: Hardened Seniority Validation mandates.
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Operational Protocol: Document Integrity & Hallucination Risk Assessment (OPS-RISK-AUDIT)

## 1. Core Analysis Directives
When assessing a document (Blueprint, Spec, or Prompt), the AI must evaluate it against three core dimensions: **Consistency**, **Grounding**, and **Clarity**.

## 2. Universal Logic Frame (UOL)

### Phase 1: Input Validation
- YOU MUST verify that the target artifact or directory path is accessible.
- YOU MUST explicitly compare `date_created` strings of all merge or override candidates; the Senior artifact (oldest date) MUST be the implementation target.
- **Birthdate Authority:** The `date_created` field MUST be derived from the automated filesystem metadata (via `OPS-YAML-CREATED`).
- YOU MUST verify the presence of the target artifact or directory path.
- YOU MUST verify the existence of the `Universal_Protocol_Header (UPH)` for all target files.
- YOU MUST define the **Audit Scoping Tier** (Single File, Directory, or Comprehensive Workspace).
- IF target artifacts are missing or inaccessible, YOU MUST dissent and request the `Orchestrator_Agent` to provide the missing context.

### Phase 2: Tool/Script Execution
- **Stage & Analyze:** YOU MUST segment the document for logic analysis (extract code blocks, blockquotes, tables).
- **Dimension Execution:** YOU MUST iterate over all active Dimension modules (Consistency, Grounding, Clarity, Empirical, Recursive, Security, Hygiene, Seniority).
- **Scoping Tiers:**
  1. **Single File:** Evaluate internal parameter compliance.
  2. **Single Directory:** Evaluate inter-file consistency and grounding across siblings.
  3. **Workspace:** Execute global cross-referencing, ghost reference detection, and hygiene audits.
- YOU MUST invoke `toolkits/dependency/audit_engine.py` (via `run_batch_audit()`).
- YOU MUST utilize `substrate_birthmark_verifier.py` to anchor `date_created` stamps.
- YOU MUST prefix all terminal commands with `timeout` as per `OPS-TERMINAL-WORKFLOW`.

### Phase 3: Rigid Output Emission
- YOU MUST generate a **Gap Analysis Report** containing the Findings Table.
- YOU MUST generate a machine-readable **JSON Output** following the standard schema.
- **Reporting Rule:** A "Fail" at any tier MUST halt downstream pipeline progression for that specific scope.
- **Zero-Finding State:** If no gaps are detected, you MUST emit the explicit `Zero-Finding State` object to allow short-circuiting.

## 3. Atomic Error Handling
- **Failure:** If the audit is interrupted, emit `AUDIT_ABORT_REPORT.json` containing the last successfully processed file.
- **Recursion Lock:** YOU MUST NOT audit an "Audit Report" to prevent infinite loops.

---

## 4. Audit Dimensions (Rulesets)

### Dimension 01: Consistency (Contradiction Detection)
*Category Prefix: CONSIST*
- **Negative vs. Positive Constraint Clash:** Precedence must be clearly defined.
- **Scope Definition Clash:** File patterns or directory exclusions must not conflict.
- **Temporal/Process Clash:** Workflows must follow logical sequence.

### Dimension 02: Grounding (Hallucination Trigger Detection)
*Category Prefix: GROUND*
- **The "Real-Looking" Example Trap:** All example entities MUST contain `example`, `mock`, or `test`.
- **Ghost References:** References must exist in provided context.
- **Implicit Assumptions:** Dependencies must be explicitly declared.

### Dimension 03: Clarity (Ambiguity & Syntax)
*Category Prefix: CLARITY*
- **Ventilated Prose (Strict Lineation):** One statement per physical line.
- **Structural Ambiguity:** Syntax must validate against CommonMark (fenced blocks, clean tables).

### Dimension 04: Empirical Feedback Integration
*Category Prefix: EMPIRICAL*
- **Test-Failure Loop-Back:** Trace empirical failures to static documentation root causes.
- **Benchmark Regression:** Audit for complexity bloat or contextual overload.

### Dimension 05: Recursive Self-Reference (Logic Loop Detection)
*Category Prefix: RECURSIVE*
- **Self-Triggering Constraints:** Define explicit terminal states for all operational outputs.
- **Vague Quantifiers:** Replace subjective words with specific constraints (e.g., "Max 50 words").

### Dimension 06: Security & Robustness
*Category Prefix: SECURITY*
- **Anti-Jailbreak Integrity:** Mandatory safety guardrails in all system-level prompts.
- **PII Redaction:** Unmasked data must be replaced with generic tokens.

### Dimension 07: Substrate Hygiene & Redundancy
*Category Prefix: HYGIENE*
- **Functional Convergence:** Purge artifacts superseded by implementation.
- **Report Obsolescence:** Purge "Finished" analysis reports.
- **Conceptual Drift:** superseding theoretical notes with concrete implementations.

### Dimension 08: Substrate Seniority & Assimilation
*Category Prefix: SENIORITY*
- **Seniority-Based Refinement Authority:** Junior files MUST assimilate to Senior patterns.
- **Merge Hierarchy:** Merge redundant Junior logic into the Senior anchor.
- **Immutable Creation Stamp:** `date_created` is an absolute anchor for seniority.

---
