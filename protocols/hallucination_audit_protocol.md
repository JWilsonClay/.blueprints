---
protocol_id: OP-RISK-AUDIT
version: 1.0.0
status: ACTIVE
last_updated: 2026-03-01
changelog:
  - 1.0.0: Initial release.
---
# Operational Protocol: Document Integrity & Hallucination Risk Assessment

**Protocol ID:** OP-RISK-AUDIT
**Target Audience:** AI Agents, Prompt Engineers, QA Auditors
**Purpose:** To systematically detect and neutralize patterns in documentation that cause Large Language Models (LLMs) to hallucinate, misinterpret instructions, or enter logic loops.

## 1. Core Analysis Directives

When assessing a document (Blueprint, Spec, or Prompt), the AI must evaluate it against three dimensions: **Consistency**, **Grounding**, and **Clarity**.

### Ruleset Extensibility
The protocol supports modular rulesets natively.
Dimensions MUST be defined as independent modules that map to the execution workflow.
Custom auditing environments MAY append additional dimensions by providing a compatible schema matrix of `(Check, Trigger, Fix)`.

**Dimension Registration Schema:**
Custom dimensions MUST adhere to the following YAML-based schema, wrapped in a `yaml` fenced code block, to ensure structured dynamic parsing:
```yaml
example_dimension_id: [EXAMPLE_ID_NUMBER]
example_name: [mock_Name]
example_focus: [example_Focus]
example_category_prefix: [mock_PREFIX]
example_goal: [mock_Statement]
example_checks:
  - example_check_name: [mock_Check_Name]
    example_trigger: [mock_Definition]
    example_risk: [mock_Risk_Or_Rule]
    example_fix_example: [mock_Remediation]
```

### Dimension 01: Consistency (Contradiction Detection)
*Category Prefix: CONSIST*
*Goal: Ensure no two instructions compete for the same logical space.*

1.  **Negative vs. Positive Constraint Clash:**
    *   *Check:* Does one section say "Do X" and another "Never do X"?
    *   *Example:* "Map every [ITEM]" vs. "Exclude [EXTERNAL_SOURCE]".
    *   *Fix:* Explicitly define the precedence (e.g., "Except for...", "Subject to Negative Constraints").
2.  **Scope Definition Clash:**
    *   *Check:* Do file patterns or directory exclusions conflict?
    *   *Example:* "Scan all `.[EXTENSION]` files" vs. "Ignore `[DIRECTORY]/` directory" (where `.[EXTENSION]` files exist).
3.  **Temporal/Process Clash:**
    *   *Check:* Does the workflow require an output that hasn't been generated yet?
    *   *Example:* "Analyze the logs" appearing before "Run the tests".

### Dimension 02: Grounding (Hallucination Trigger Detection)
*Category Prefix: GROUND*
*Goal: Ensure the AI distinguishes between "Instructional Examples" and "Actual Context".*

1.  **The "Real-Looking" Example Trap:**
    *   *Trigger:* Any file path, variable, or data row in an example block that does NOT contain a mandatory safety token.
    *   *Protocol:* Enforce Strict Naming Conventions. All example entities MUST contain one of: `example`, `mock`, `test`, `placeholder`, or `foo/bar`.
    *   *Fix:* Rename `auth.js` to `mock_auth.js` or `example_auth.js`.
2.  **Ghost References:**
    *   *Trigger:* References to files, sections, or rules (e.g., "See Hypothetical Rule 5.2") that do not exist in the provided context.
    *   *Risk:* The AI invents the content of the missing reference.
3.  **Unanchored Preamble:**
    *   *Trigger:* Conversational text ("In the works...", "Thoughts:") mixed with executable instructions.
    *   *Risk:* The AI treats editorial commentary as strict rules or context.
4.  **Implicit Assumptions (Missing Dependencies):**
    *   *Trigger:* Executable instructions that rely on undeclared variables, uninstalled libraries, or undefined environment setups.
    *   *Protocol:* Enforce complete dependency declarations. 
        Every executable block MUST explicitly state prerequisites or link to an initialization step.
    *   *Fix:* Prepend instructions with explicit states, e.g., "Assuming `[DEPENDENCY]` is installed..." or provide an explicit installation command before usage.


### Dimension 03: Clarity (Ambiguity & Syntax)
*Category Prefix: CLARITY*
*Goal: Eliminate subjective interpretation.*

### Dimension 04: Recursive Self-Reference (Logic Loop Detection)
*Category Prefix: RECURSIVE*
*Goal: Ensure protocols do not mandate operations that infinitely trigger themselves.*

1.  **Self-Triggering Constraints:**
    *   *Check:* Does the protocol mandate an output that triggers its own evaluation without a termination condition?
    *   *Example:* "Auditing an audit report."
    *   *Fix:* Define explicit terminal states for outputs.

2.  **Vague Quantifiers:**
    *   *Trigger:* Words like "briefly", "appropriate", "standard", "etc.", "and so on".
    *   *Protocol:* Replace with specific constraints (e.g., "Max 50 words", "CommonMark compliant", "List exactly 5 items").
3.  **Structural Ambiguity:**
    *   *Trigger:* Missing headers, unclosed code blocks, or merged table rows.
    *   *Protocol:* Validate syntax strictly against the CommonMark specification. 
        Code blocks MUST be explicitly fenced with language identifiers, and table structures MUST parse cleanly via standard Markdown Abstract Syntax Tree (AST) parsers.
4.  **Ventilated Prose (Strict Lineation):**
    *   *Trigger:* Multiple instructions, rules, or data points consolidated onto a single physical line.
    *   *Protocol:* Enforce "One Statement Per Line" constraint. 
        A "Statement" is defined strictly as a single condition OR a single imperative instruction.
        Complex mandates MUST be grouped via bulleted lists.
        Each physical line MUST contain exactly one logical clause terminated by a literal newline (`\n`).
    *   *Exception:* **Markdown Table Rows.** Content within a table cell MUST remain on the same physical line as the row delimiters (`|`) to preserve valid Markdown syntax, even if the cell contains multiple logical clauses.

## 2. Execution Workflow

To execute this protocol, the AI Auditor performs the following pass:

1.  **Ingest & Segment:** 
    *   Functionally segment the document by identifying standard Markdown boundaries. 
    *   Extract all fenced code blocks (using triple backticks), blockquotes (`>`), and tables to isolate them from instructional prose. 
    *   Tag standard unstructured prose as "Instructional Blocks".
    *   Tag isolated content as "Example Blocks."
2.  **Targeted Logic Mapping:** 
    * Isolate sentences containing generalized global modifiers (e.g., "Always", "Never", "Must", "All"). 
    * Extract imperative verbs exclusively from these high-risk constraint blocks.
    * Extract all binding assertions simultaneously (Is, Are Not, Will, Shall Not).
    * Extract all passive structural constraints (Are to be, Must not be).
    * Generate a structured mapping for each extracted element: `(Element_Type, Primary_Target, Contextual_Scope, Violated_Rule)`. 
    * For constraint blocks, this maps to `("Imperative Constraint", Action, Target, Scope)`. 
    * For static examples, it maps to `("Example Block", Entity_Name, File_Context, N/A)`.
    * Flag any single line containing multiple imperative verbs or competing constraints as a violation of the active "Ventilated Prose" rule.
    * *Example:* `("Imperative", "Delete", "User Account", "Global / After 30 days")`
3.  **Dynamic Dimension Execution:** Iterate over all active Dimension modules successfully parsed from the document structure, remaining completely agnostic to their specific identifiers or customized origins.
4.  **Constraint vs. Rule Verification:** For each dimension, execute its specific mapping checks against the generated tuple AST (e.g., Conflict Scan for Consistency, Scope Verification for Custom Rules).
5.  **Syntax & Ambiguity Validation:** Verify the AST against the Clarity specifications, ensuring the "One Statement Per Line" constraint is validated across all instructional prose.

## 3. Output Artifact: Gap Analysis Report

The output of this protocol is a **Gap Analysis Report** containing a structured table of findings.

**Finding ID Taxonomy:**
All Finding IDs MUST explicitly trace back to the violated dimension for maintainability. 
Use the format `DIM-[CATEGORY]-[NUMBER]` (e.g., `DIM-CONSIST-01` for Consistency, `DIM-GROUND-01` for Grounding, `DIM-CLARITY-01` for Clarity).

**Severity Taxonomy:**
Auditors MUST classify findings using exclusively the following levels based on execution impact:
- **Critical:** Contradictions or logic loops that cause catastrophic failure, pipeline crashes, or full hallucination.
- **High:** Ambiguities or ghost references with a high probability of causing incorrect tool calls or data corruption.
- **Medium:** Missing dependencies or vague quantifiers that require LLM assumptions but might still succeed.
- **Low:** Minor formatting deviations or warnings that do not immediately threaten execution logic.

**Template:**
```markdown
# Gap Analysis Report: [Document Name]

## Executive Summary
[Assessment of critical gaps and pass/fail status]

## Findings Table
| ID | Type | Severity | Description | Location | Remediation |
|---|---|---|---|---|---|
| DIM-CONSIST-01 | Contradiction | Critical | "Rule A" conflicts with "Rule B" | Lines XX, YY | Add "Except" clause to Line XX |
| DIM-GROUND-01 | Hallucination | High | Example `[REAL_LOOKING_FILE]` looks real | Line ZZ | Rename to `[PLACEHOLDER]` |
| DIM-CLARITY-01 | Ambiguity | Low | "[SUBJECTIVE_PHRASE]" is subjective | Line AA | Define "[SPECIFIC_FORMAT]" format |
```

**Zero-Finding State:**
If no gaps are detected across all dimensions, the Findings Table must still be generated with a single row:
```markdown
| N/A | Pass | Info | No gaps detected. Document complies with OP-RISK-AUDIT. | N/A | N/A |
```
### 3.1 Machine-Readable Output (JSON)
For automated pipelines, the AI Auditor MUST generate the Gap Analysis Report as a structured JSON object.
**Template:**
```json
{
  "example_report_metadata": {
    "example_document_name": "[mock_Document_Name]",
    "example_protocol_applied": "OP-RISK-AUDIT",
    "example_protocol_version": "[mock_VERSION]",
    "example_audit_timestamp": "[mock_ISO-8601]",
    "example_status": "[mock_PASS_FAIL]",
    "example_extensions": {}
  },
  "example_findings": [
    {
      "example_id": "DIM-CONSIST-01",
      "example_type": "Contradiction",
      "example_severity": "Critical",
      "example_description": "\"mock_Rule A\" conflicts with \"mock_Rule B\"",
      "example_location": {
        "example_start_line": "mock_XX",
        "example_end_line": "mock_YY"
      },
      "example_remediation": "Add \"mock_Except\" clause to Line mock_XX"
    }
  ]
}
```

**Zero-Finding State (JSON):**
If no gaps are detected across all dimensions, the `findings` array MUST be strictly empty and the metadata status MUST indicate a pass.
```json
{
  "example_report_metadata": {
    "example_document_name": "[mock_Document_Name]",
    "example_protocol_applied": "OP-RISK-AUDIT",
    "example_protocol_version": "[mock_VERSION]",
    "example_audit_timestamp": "[mock_ISO-8601]",
    "example_status": "PASS",
    "example_extensions": {}
  },
  "example_findings": []
}
```
