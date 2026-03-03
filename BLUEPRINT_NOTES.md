# Blueprint Notes: Substrate Core Components

## In the works:
1. Token Density & Conciseness
LLMs have context windows. "Fluff" or conversational filler dilutes the density of instructions.

Practice: Remove introductory paragraphs that explain "Why" unless they contain critical constraints.
Example: Instead of "To make this practical and actionable, I'll complete the list...", just start the list. The AI understands the list implies actionability.
2. Explicit Schemas over Prose
When defining the output format (the Checklists), prose descriptions can be ambiguous.

Practice: Define the target structure using a pseudo-schema or strict template.
Example: Instead of describing the columns in a paragraph, provide a JSON skeleton or a strict Markdown Table Template block.
3. Negative Constraints
LLMs are eager to please and may hallucinate features to be helpful.

Practice: Explicitly state what is out of scope.
Example: "Do not include hardware drivers. Do not include project management tools." (You already have some of this, but making it a bulleted "Constraints" section increases adherence).
4. Anchor Identifiers
Practice: Assign unique IDs or anchors to sections.
Benefit: Allows you to reference specific rules in future prompts (e.g., "Review code against [Rule 7.2]").
5. Versioning & Changelogs
Practice: Keep a compact changelog at the top of the file.
Benefit: Helps the AI understand the evolution of the document (e.g., "v0.2 added Logging"). This provides temporal context for why certain rules exist.

Cyclic prompt for Protocol_Auditor and Hallucination_Audit_Protocol.md

Follow the ROLE of Protocol_Auditor defined in 

00_Protocol_Auditor


For this specific task, execute OP-RISK-AUDIT within 

Hallucination_Audit_Protocol.md
.  Override the standard output format and instead produce ONLY a strategic GAP report on ONLY the two documents in reference 

Hallucination_Audit_Protocol.md
AND 

00_Protocol_Auditor
to ensure they are built correctly according to the required attributes: scalable, modular, comprehensive, verifiable, maintainable, adaptable, and efficient.

Itemize your findings in a numbered list.

For each item:

Provide a severity label (critical, high, medium, low) Describe the gap in detail, referencing specific sections, missing elements, or structural issues in the document and explaining the impact on one or more of the seven attributes Provide detailed instructions on how to implement the fix, including exact Markdown edits or new sections to add, concrete examples of revised text/code blocks, and the rationale for how the change achieves scalability/modularity/etc. Structure the entire response as this itemized strategic GAP report only. No executive summary, no table, no additional commentary, and no document edits. Print to the screen only.
