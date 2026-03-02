# Blueprint Notes: Codebase Core Components

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