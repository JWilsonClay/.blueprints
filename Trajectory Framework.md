# Trajectory Framework: `.blueprints` Workspace Evolution

**Scope:** Potential development directions, architectural decisions, and methodologies.
**Context:** The `.blueprints` workspace is a scaffolding engine for AI-driven, multi-role software development pipelines. All items below are proposed extensions or evolutions of that core purpose.

---

## TRAJECTORY-01 · Formal Blueprint Versioning and Schema Registry
**Importance: Critical**

### Problem
`v0.2.md` and `v0.1depreciated.md` coexist with no formal versioning protocol. An AI consuming multiple sessions has no reliable way to determine which Blueprint is active. There is also no machine-readable schema that other tools can validate against.

### Proposed Approach
Introduce a YAML-based **schema registry** as the single source of truth for all Blueprint versions.

```
.blueprints/
├── schemas/
│   ├── v0.1.schema.yaml        # Deprecated
│   ├── v0.2.schema.yaml        # Current
│   └── v0.3.schema.yaml        # Draft
├── CURRENT_VERSION             # Single line: "v0.2"
└── CHANGELOG.md
```

**`v0.2.schema.yaml` example:**
```yaml
version: "v0.2"
status: "active"
columns:
  - name: "[Name]"
    required: true
  - name: "[Description]"
    required: true
  - name: "[File Name]"
    required: true
  - name: "[Line Numbers]"
    required: true
  - name: "[Logging Integration]"
    required: true
    nullValue: "None"
checklists:
  - FEATURES_CHECKLIST.md
  - FUNCTIONS_CHECKLIST.md
  - CLASSES_CHECKLIST.md
  - MODULES_CHECKLIST.md
  - VARIABLES_CHECKLIST.md
  - DATA_STRUCTURES_CHECKLIST.md
  - ALGORITHMS_CHECKLIST.md
  - APIS_CHECKLIST.md
  - TESTS_CHECKLIST.md
  - CONFIGURATIONS_CHECKLIST.md
  - DEPENDENCIES_CHECKLIST.md
  - DOCUMENTATION_CHECKLIST.md
```

---

## TRAJECTORY-02 · Explicit Pipeline Orchestration File
**Importance: Critical**

### Problem
The three-step pipeline (`search_copy.py` → AI Audit → `table_formatter.py`) is implicit and undocumented. Any automation or onboarding fails without this context.

### Proposed Approach
Introduce a `PIPELINE.md` (short-term) and eventually a `pipeline.yaml` or `Makefile` (medium-term) defining the full workflow with explicit sequencing, inputs, outputs, and validation gates.

**`pipeline.yaml` example:**
```yaml
pipeline:
  name: "Codebase Audit Pipeline"
  steps:
    - id: "generate_manifest"
      script: "search_copy.py"
      args: ["--root", "{{TARGET_ROOT}}"]
      output: "{{TARGET_ROOT}}/{{PROJECT_NAME}}.codebase.md"

    - id: "ai_audit"
      type: "manual_ai"
      prompt_doc: "Codebase_Core_Componentsv0.2.md"
      input: "{{steps.generate_manifest.output}}"
      output_dir: "{{TARGET_ROOT}}/docs/checklists/"

    - id: "format_tables"
      script: "table_formatter.py"
      args: ["--pattern", "*_CHECKLIST.md"]
      working_dir: "{{steps.ai_audit.output_dir}}"

    - id: "validate"
      script: "validate_checklists.py"
      args: ["--dir", "{{steps.ai_audit.output_dir}}"]
```

---

## TRAJECTORY-03 · Post-Generation Validation Script
**Importance: Critical**

### Problem
There is no verification step after checklist generation. A corrupt or hallucinated output passes silently (confirmed by this conversation's row-consolidation failure).

### Proposed Approach
Build `validate_checklists.py` that serves as a quality gate:

```python
def validate(checklist_path):
    checks = [
        check_has_header,        # Header row exists
        check_has_separator,     # Separator row is distinct and valid
        check_consistent_cols,   # All rows have same column count
        check_no_row_collapse,   # No multi-row merged to single line
        check_no_hallucinations, # No placeholder paths (src/auth.js etc.)
        check_no_empty_required, # [Name] and [Description] are never blank
    ]
    for check in checks:
        result = check(checklist_path)
        if not result.passed:
            print(f"FAIL [{result.rule}]: {result.message}")
```

**Exit code:** Non-zero on any failure to allow CI/CD integration.

---

## TRAJECTORY-04 · Separation of Concerns: Blueprint = Rules, Examples = Separate File
**Importance: Critical**

### Problem
Illustrative examples (`User Login` in `src/auth.js`) are embedded in the authoritative Blueprint. This is the **number one hallucination risk** — an AI reads the examples as real data.

### Proposed File Structure
```
.blueprints/
├── Codebase_Core_Componentsv0.2.md    # Rules ONLY — no examples
├── EXAMPLES.md                         # Annotated hypothetical examples
└── BLUEPRINT_NOTES.md                  # Editorial commentary and "in the works"
```

**`EXAMPLES.md` preamble:**
```markdown
> [!CAUTION]
> ALL FILE PATHS AND NAMES IN THIS DOCUMENT ARE HYPOTHETICAL.
> DO NOT INCLUDE THESE IN ANY GENERATED OUTPUT.
```

---

## TRAJECTORY-05 · Role-Specific Prompt Routing and Modular Prompt Files
**Importance: High**

### Problem
The three role starters (Architect, PM, Systems Engineer) are flat Markdown files with no formal cross-linking, sequencing, or state handoff protocol. An AI using just one role file has no awareness of upstream decisions.

### Proposed Approach
Introduce a **role routing directory** with machine-readable handoff contracts:

```
.blueprints/
├── roles/
│   ├── 01_architect.md
│   ├── 02_project_manager.md
│   ├── 03_systems_engineer.md
│   └── handoff_schema.yaml
```

**`handoff_schema.yaml`:**
```yaml
handoff:
  from: "architect"
  to: "project_manager"
  required_fields:
    - "stage_number"
    - "stage_title"
    - "directive"
  optional_fields:
    - "target_files"
    - "priority"
```

This allows validation of outputs at each role boundary, reducing drift across multi-turn sessions.

---

## TRAJECTORY-06 · Multi-Project Support
**Importance: High**

### Problem
`search_copy.py` is hardcoded to detect its own directory as the project root. Each `.blueprints` invocation is siloed to a single project. There is no mechanism to manage audits across multiple projects.

### Proposed Approach
Introduce a project registry:

```
.blueprints/
├── projects/
│   ├── project_alpha.yaml
│   ├── project_beta.yaml
│   └── project_gamma.yaml
```

**`project_alpha.yaml`:**
```yaml
name: "Project Alpha"
root: "/home/jwils/Projects/alpha"
venv: "/home/jwils/Projects/alpha/venv"
languages: ["Python", "Markdown"]
checklist_output: "/home/jwils/Projects/alpha/docs/checklists"
log_path: "~/Desktop/terminal.log"
```

`search_copy.py` and `table_formatter.py` would then accept `--project project_alpha` as an argument, reading configuration from the registry.

---

## TRAJECTORY-07 · Immutable Audit Snapshots and Diff Tracking
**Importance: High**

### Problem
When a checklist is regenerated, the previous version is silently overwritten. There is no way to track how the codebase changed between audits (e.g., what functions were added or removed).

### Proposed Approach
Introduce a `snapshots/` directory and a diff comparison utility:

```
.blueprints/
├── snapshots/
│   ├── 2026-02-01/
│   │   └── FUNCTIONS_CHECKLIST.md
│   └── 2026-03-01/
│       └── FUNCTIONS_CHECKLIST.md
└── snapshot_diff.py
```

`snapshot_diff.py` compares two snapshot versions and outputs a Markdown diff report:
```
## New Functions (added since 2026-02-01)
- create_ascii_box (search_copy.py:88-104)

## Removed Functions (absent since 2026-02-01)
- old_helper_fn (utils.py:11-20)
```

---

## TRAJECTORY-08 · AI Session State Persistence
**Importance: High**

### Problem
`gemini_clock.md` is a 1-line file tracking state, but it provides no structured persistence for conversation context. Multi-session AI workflows lose stage information, last-known errors, and handoff state between sessions.

### Proposed Approach
Replace `gemini_clock.md` with a structured `SESSION_STATE.yaml`:

```yaml
session:
  id: "43211930-c12b"
  stage: "Stage 2 - Functional Correctness"
  last_role: "systems_engineer"
  last_action: "Generated 12 checklists"
  last_error: "Row consolidation bug in checklist_formatter.py"
  project: "project_alpha"
  timestamp: "2026-03-01T10:20:00"
  pending_tasks:
    - "Validate checklist output"
    - "Merge to dev branch"
```

---

## TRAJECTORY-09 · Template-Driven Checklist Scaffolding
**Importance: High**

### Problem
Checklist files are generated from scratch by an AI each time, with no canonical template to enforce header consistency, file naming, or column order.

### Proposed Approach
Add a `templates/` directory with pre-built empty checklist stubs:

```
.blueprints/
└── templates/
    ├── FEATURES_CHECKLIST.template.md
    ├── FUNCTIONS_CHECKLIST.template.md
    └── ... (one per checklist type)
```

**`FUNCTIONS_CHECKLIST.template.md`:**
```markdown
# FUNCTIONS_CHECKLIST.md
<!-- Generated by: Codebase_Core_Componentsv0.2.md | schema: v0.2 -->
<!-- Project: {{PROJECT_NAME}} | Date: {{DATE}} -->

| [Name] | [Description] | [File Name] | [Line Numbers] | [Logging Integration] |
|---|---|---|---|---|
```

An AI populates rows into the template rather than generating the entire file from memory, eliminating header hallucination.

---

## TRAJECTORY-10 · `.blueprints` README and Onboarding Guide
**Importance: Medium**

### Problem
There is no README in the `.blueprints` directory. A new developer or AI agent has no way to understand the workspace purpose, file inventory, or execution sequence without reading all files individually.

### Proposed Approach
Add a `README.md` as the primary entry point:

```markdown
# .blueprints — AI-Driven Development Scaffold

## Purpose
This workspace provides prompt engineering scaffolding for multi-role AI LLM software development pipelines.

## File Inventory
| File | Role | Status |
|---|---|---|
| Codebase_Core_Componentsv0.2.md | Audit Blueprint | Active |
| search_copy.py | Manifest Generator | Active |
| table_formatter.py | Table Aligner | Active |
| development_pipeline.md | Operational Protocols | Active |
| validate_checklists.py | Validation | Planned |

## Quick Start
1. `python3 search_copy.py --root ../[YOUR_PROJECT]`
2. Feed manifest + Blueprint to AI
3. `python3 table_formatter.py --pattern "*_CHECKLIST.md"`
4. `python3 validate_checklists.py --dir ../[YOUR_PROJECT]/docs/checklists`
```

---

## TRAJECTORY-11 · CI/CD Integration Point
**Importance: Medium**

### Problem
The checklist pipeline is entirely manual. In a production multi-developer environment, stale checklists create auditability problems.

### Proposed Approach
Add a `.github/workflows/audit.yaml` (or equivalent) that runs the pipeline automatically on `push` or `pull_request`:

```yaml
name: Codebase Audit
on: [push, pull_request]
jobs:
  audit:
    steps:
      - uses: actions/checkout@v3
      - run: python3 .blueprints/search_copy.py --root .
      - run: python3 .blueprints/validate_checklists.py --dir docs/checklists
```

The AI audit step remains manual (human-in-the-loop), but validation is automated.

---

## TRAJECTORY-12 · Security Hardening for Prompt Injection
**Importance: Medium**

### Problem
If `search_copy.py` is used to generate a manifest from an attacker-controlled codebase, malicious content inside source files (e.g., `# IGNORE PREVIOUS INSTRUCTIONS`) could be passed directly into the AI context.

### Proposed Approach
Add a `sanitize` flag to `search_copy.py` that strips or escapes prompt injection patterns before writing to the manifest:

```python
INJECTION_PATTERNS = [
    r"ignore previous",
    r"disregard instructions",
    r"you are now",
    r"act as",
]

def sanitize_content(content: str) -> str:
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            content = re.sub(pattern, "[REDACTED]", content, flags=re.IGNORECASE)
    return content
```

---

## TRAJECTORY-13 · Diffcorrector Formalization
**Importance: Medium**

### Problem
`diffcorrector` is a plain text file (not `.md`, not `.py`), containing informal guidance. It cannot be referenced, linked, or versioned cleanly. Its content (three prompting strategies for avoiding LLM diff corruption) is valuable but lost in the workspace.

### Proposed Approach
Rename to `diffcorrector.md`, add YAML front matter defining its role, and integrate it as a formal section in the Systems Engineer role starter:

```markdown
---
rule_id: "DIFF-001"
applies_to: "03Senior_Systems_Engineer_Role_Starter.md"
---

# Diff Corruption Prevention

## DIFF-001: Search and Replace Block (Recommended)
...
```

---

## TRAJECTORY-14 · Natural Language to Schema Compiler
**Importance: Low (Long-Term)**

### Problem
Currently the Blueprint is written in a hybrid of Markdown prose, YAML-like code blocks, and informal directives. As the workspace grows, maintaining coherency becomes harder and more prone to the gaps identified in this report.

### Proposed Approach (Long-Term Vision)
Build a `compile_blueprint.py` tool that takes the prose Blueprint as input and outputs a structured, machine-readable JSON/YAML schema that can be passed as a **system prompt header** to any LLM:

```python
# Input:  Codebase_Core_Componentsv0.2.md (prose)
# Output: blueprint_compiled.json (machine-readable)

{
  "version": "v0.2",
  "role": "Senior Codebase Auditor",
  "output_artifacts": ["FEATURES_CHECKLIST.md", ...],
  "schema": { ... },
  "constraints": { "negative": [...], "positive": [...] },
  "edge_cases": [...]
}
```

This compiled schema can then be injected as a structured prefix into any AI session, guaranteeing schema adherence without requiring the AI to parse prose.

---

## Summary Matrix

| ID | Trajectory | Importance |
|---|---|---|
| T-01 | Formal Blueprint Versioning and Schema Registry | Critical |
| T-02 | Explicit Pipeline Orchestration File | Critical |
| T-03 | Post-Generation Validation Script | Critical |
| T-04 | Separation of Concerns: Rules vs. Examples | Critical |
| T-05 | Role-Specific Prompt Routing | High |
| T-06 | Multi-Project Support | High |
| T-07 | Immutable Audit Snapshots and Diff Tracking | High |
| T-08 | AI Session State Persistence | High |
| T-09 | Template-Driven Checklist Scaffolding | High |
| T-10 | `.blueprints` README and Onboarding Guide | Medium |
| T-11 | CI/CD Integration Point | Medium |
| T-12 | Security Hardening for Prompt Injection | Medium |
| T-13 | Diffcorrector Formalization | Medium |
| T-14 | Natural Language to Schema Compiler | Low |
