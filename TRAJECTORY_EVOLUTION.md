# Trajectory Evolution: .blueprints Workspace Roadmap

**Goal:** This document serves as the single authoritative roadmap for the `.blueprints` workspace, combining immediate remediation needs with long-term strategic evolution.

---

## Part 1: Immediate Remediation (Active)
*Source: Remediation Plan.md*

### Phase 1 · Blueprint Document Restructure (Critical Gaps)
- **Status:** In Progress
- **Objectives:** Harden the Blueprint against AI misinterpretation.
- **Key Changes:** 
    - Separate Preamble from Executable Body (`BLUEPRINT_NOTES.md`).
    - Promote Execution Prompt to immediately follow YAML header.
    - Extract illustrative examples to `EXAMPLES.md`.
    - Harden Table Schema with explicit structural rules.

### Phase 2 · Script Consolidation (High Gaps)
- **Status:** In Progress
- **Objectives:** Eliminate redundant and divergent tools.
- **Key Changes:**
    - Delete `checklist_formatter.py` (superseded by `table_formatter.py`).
    - Enhance `search_copy.py` with CLI arguments and Markdown support.
    - Document the Audit Pipeline in `PIPELINE.md`.

### Phase 3 · Schema Hardening and Validation (Medium Gaps)
- **Status:** Planned
- **Objectives:** Implement quality gates for generated output.
- **Key Changes:**
    - Enhance `table_formatter.py` with disk buffering and separator detection.
    - New `validate_checklists.py` script for post-generation verification.

---

## Part 2: Strategic Trajectories (Long-Term)
*Source: Trajectory Framework.md*

### [T-01] Formal Blueprint Versioning and Schema Registry
- **Importance:** Critical
- **Approach:** Introduce a YAML-based schema registry (`.blueprints/schemas/`) as the source of truth for Blueprint versions.

### [T-02] Explicit Pipeline Orchestration
- **Importance:** Critical
- **Approach:** Move from implicit documentation to an executable `pipeline.yaml` or `Makefile`.

### [T-03] Role-Specific Prompt Routing
- **Importance:** High
- **Approach:** Modularize role starters into `.blueprints/roles/` with formal handoff contracts.

### [T-04] Snapshot and Diff Tracking
- **Importance:** High
- **Approach:** Implement a `snapshots/` directory and `snapshot_diff.py` to track codebase evolution between audits.

### [T-05] Security Hardening
- **Importance:** Medium
- **Approach:** Add prompt injection sanitization to the manifest generation process.

---

## Part 3: Summary Matrix

| ID | Trajectory / Phase | Importance | Status |
|---|---|---|---|
| P-1 | Blueprint Restructure | Critical | In Progress |
| P-2 | Script Consolidation | High | In Progress |
| P-3 | Schema Hardening | Medium | Planned |
| T-01 | Versioning / Registry | Critical | Proposed |
| T-02 | Pipeline Orchestration | Critical | Proposed |
| T-03 | Role Routing | High | Proposed |
| T-04 | Snapshots / Diffing | High | Proposed |
| T-05 | Security Hardening | Medium | Proposed |

---
**Version:** v1.0.0
**Last Updated:** 2026-03-03
**Owner:** AI Engineering Governance Board
