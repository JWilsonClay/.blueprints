```yaml
# global class at project root
# lives in .blueprints/Universal_Protocol_Header.md
```

# Standard: Universal Protocol Header (UPH)

**Version:** 1.0.0
**Status:** CANONICAL
**Date Created:** 2026-03-03

---

## 1. Mandatory Frontmatter Fields

Every authoritative Agent Role and Operational Protocol MUST lead with this exact YAML structure:

```yaml
---
protocol_id: [ID or "N/A (Agent Role)"]
structure_status: [DRAFT | HARDENED]
target_audience: [List of primary consumers]
assigned_role: [Owner Role]
purpose: [One-sentence mission statement]
version: [X.Y.Z]
status: [ACTIVE | DEPRECATED]
date_created: [ISO-8601]
date_modified: [ISO-8601]
supersedes: [List of legacy Protocol IDs absorbed by this artifact]
---
```

## 2. Field Definitions

| Field | Requirement | Definition |
|---|---|---|
| `protocol_id` | Mandatory | The unique identifier (e.g., OP-RISK-AUDIT). Use "N/A (Agent Role)" for role artifacts. |
| `structure_status` | Mandatory | `DRAFT` for new artifacts, `HARDENED` after first successful audit. |
| `target_audience` | Mandatory | Explicit list of roles/users that ingest this document. |
| `assigned_role` | Mandatory | The primary role responsible for executing or maintaining the artifact. |
| `purpose` | Mandatory | Replicates the "Purpose" section of the document in a machine-readable field. |
| `supersedes` | Optional | A list of older protocol identities that were fully absorbed into this protocol. Used for obsolete file hygiene. |

## 3. Example (Orchestrator Role)

```yaml
---
role: Orchestrator_Agent
protocol_id: N/A (Agent Role)
structure_status: HARDENED
target_audience: Genesis, Verification, Deployment Agents, and System Architects
assigned_role: Orchestrator_Agent
purpose: Prevent infinite agentic loops, manage compute budgets, and sequence the .blueprints substrate.
protocol_dependencies:
  - OP-ORCHESTRATE-META@1.0.0
version: 1.0.0
status: ACTIVE
date_created: 2026-03-02
date_modified: 2026-03-03
---
```
