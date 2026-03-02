# Implementation Plan: `.blueprints` Workspace Remediation

**References:** Gap Analysis Report (`gap_analysis_report.md`)
**Goal:** Surgically repair the 17 identified gaps to harden the Blueprint against AI misinterpretation, hallucination, and tooling errors.

---

## Phase 1 · Blueprint Document Restructure (Critical Gaps)

**Addresses:** GAP-01, GAP-02, GAP-03, GAP-04, GAP-05, GAP-06, GAP-07, GAP-16

The `Codebase_Core_Componentsv0.2.md` document must be restructured to be **machine-legible first, human-legible second**.

---

### [MODIFY] [Codebase_Core_Componentsv0.2.md](file:///home/jwils/GoogleDrive1TB/PapiBobes/.blueprints/Codebase_Core_Componentsv0.2.md)

**Change 1.1 — Separate the Preamble from the Executable Body (GAP-01)**
Move all `In the works:` editorial text to a dedicated file named `BLUEPRINT_NOTES.md`. The `v0.2.md` document should begin with a formal machine-readable header block.

```markdown
---
# BLUEPRINT: Codebase Core Components
version: v0.2
date: 2026-03-01
changelog:
  - v0.2: Added "Logging Integration" column. Aligned with table_formatter.py.
  - v0.1: Initial schema definition.
canonical_tool: table_formatter.py
output_dir: "[TARGET_PROJECT_ROOT]/docs/checklists/"
---
```

**Change 1.2 — Promote the Execution Prompt to the Top (GAP-03)**
Move the `### Prompt to Execute this Document` section (currently Lines 346–396) to **immediately after the front matter header**, before any prose. AI agents must receive the executable instructions before illustrative examples.

**Change 1.3 — Move Illustrative Examples into a Separate File (GAP-03)**
Extract all illustrative table examples (e.g., `User Login` in `src/auth.js`) into a separate file named `EXAMPLES.md`. Add a clear preamble to each example: `> NOTE: The following is a hypothetical example. Do not use these file paths or names in actual output.`

**Change 1.4 — Harden the Table Schema (GAP-04)**
Expand the Table Template section with explicit structural rules:

```markdown
## Table Schema Rules
- RULE-S1: Every table MUST have exactly one header row.
- RULE-S2: Every table MUST have exactly one separator row immediately following the header. The separator row MUST use `---` per column and MUST NOT contain other content.
- RULE-S3: Every data row MUST have the same number of columns as the header row.
- RULE-S4: Every row MUST be terminated with a literal newline character (`\n`). Row consolidation is a fatal violation.
- RULE-S5: Pipe characters (`|`) within cell content MUST be escaped as `\|`.
- RULE-S6: File paths are relative to the TARGET project root, not to the `.blueprints` directory.
```

**Change 1.5 — Resolve "every" vs. Exclusion Contradiction (GAP-05)**
Replace "map every element" with: `"Map every element EXCEPT those explicitly excluded by the Negative Constraints below."` Add a cross-reference pointer from the OBJECTIVE to the NEGATIVE CONSTRAINTS section.

**Change 1.6 — Add Changelog and Anchor IDs (GAP-06, GAP-07)**
Add the changelog to the YAML front matter (Change 1.1) and prepend section anchors:
```markdown
## [Rule-1] Features
## [Rule-2] Functions
...
```

**Change 1.7 — Define Output Location (GAP-16)**
Add to the CONTEXT section: `Output Directory: Checklist files will be written to [TARGET_PROJECT_ROOT]/docs/checklists/ unless overridden.`

---

## Phase 2 · Script Consolidation and Pipeline Documentation (High Gaps)

**Addresses:** GAP-02, GAP-08, GAP-09, GAP-10, GAP-11, GAP-15

### [DELETE] [checklist_formatter.py](file:///home/jwils/GoogleDrive1TB/PapiBobes/.blueprints/checklist_formatter.py)

`checklist_formatter.py` is superseded by `table_formatter.py`. It should be deleted to eliminate operationally divergent duplicates. A deprecation commit message should record the reason.

---

### [MODIFY] [search_copy.py](file:///home/jwils/GoogleDrive1TB/PapiBobes/.blueprints/search_copy.py)

**Change 2.1 — Add CLI via argparse (GAP-09)**
```python
parser = argparse.ArgumentParser(description="Aggregate project source into a codebase manifest.")
parser.add_argument("--root", default=".", help="Target project root directory.")
parser.add_argument("--output", default=None, help="Output manifest filename.")
args = parser.parse_args()
```

**Change 2.2 — Add Markdown to Tracked Extensions (GAP-10)**
```python
'Markdown': ['.md'],
```

**Change 2.3 — Replace Silent Exception Swallowing (GAP-11)**
```python
except Exception as e:
    print(f"[WARN] Skipped {file_path}: {e}", file=sys.stderr)
```

---

### [NEW] [PIPELINE.md](file:///home/jwils/GoogleDrive1TB/PapiBobes/.blueprints/PIPELINE.md)

Document the three-step pipeline explicitly so AI agents can understand the workflow context:
```markdown
# .blueprints Audit Pipeline

## Step 1: Generate Codebase Manifest
python3 .blueprints/search_copy.py --root ./[TARGET_PROJECT]

## Step 2: Execute AI Audit
[Provide manifest + v0.2 Blueprint to AI. Run prompt from v0.2.md EXECUTION section.]

## Step 3: Align Checklist Tables
python3 .blueprints/table_formatter.py --pattern "*_CHECKLIST.md"
```

---

## Phase 3 · Schema Hardening and Validation (Medium Gaps)

**Addresses:** GAP-12, GAP-13, GAP-14, GAP-17

### [MODIFY] [table_formatter.py](file:///home/jwils/GoogleDrive1TB/PapiBobes/.blueprints/table_formatter.py)

**Change 3.1 — Replace `pickle` with `tempfile.SpooledTemporaryFile` (GAP-12)**
Use a text-mode spooled buffer instead of `pickle` for transparent, human-debuggable intermediate state.

**Change 3.2 — Detect and Skip Separator Rows (GAP-14)**
Add a separator row detector that bypasses the width-padding logic for rows that match `|---` patterns, preserving their idiomatic compact form.

```python
def is_separator_row(line: str) -> bool:
    """Returns True if line is a Markdown table separator row."""
    stripped = line.strip().strip('|').strip()
    return all(c in '-: ' for c in stripped) and '-' in stripped
```

---

### [NEW] [validate_checklists.py](file:///home/jwils/GoogleDrive1TB/PapiBobes/.blueprints/validate_checklists.py)

A new post-generation validation script that verifies:
1. Every checklist file has at least a header row, separator row, and one data row.
2. All rows have consistent column counts.
3. No row consolidation (single-line tables) has occurred.
4. No rows contain placeholder file paths from the Blueprint examples (e.g., `src/auth.js`).

---

## Verification Plan

### Automated Tests
- Run `validate_checklists.py` after each audit to confirm structural integrity.
- Grep each generated checklist for hallucinated placeholder paths:
  ```bash
  grep -rn "src/auth.js\|src/search.py" .blueprints/*.md && echo "HALLUCINATION DETECTED"
  ```

### Manual Verification
- Re-run the full pipeline against a sample project using the updated Blueprint.
- Confirm the output directory is correctly placed at `[TARGET_PROJECT_ROOT]/docs/checklists/`.
- Confirm `checklist_formatter.py` is absent from the directory.
