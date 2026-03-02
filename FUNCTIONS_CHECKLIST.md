# FUNCTIONS_CHECKLIST.md

| [Name]                     | [Description]                                                                  | [File Name]            | [Line Numbers] | [Logging Integration] |
| ---                        | ---                                                                            | ---                    | ---            | ---                   |
| get_visual_width           | Calculates visual width of strings, accounting for tab expansion.              | checklist_formatter.py | 24-33          | None                  |
| get_needed_tabs            | Calculates required tab count to reach a target visual width.                  | checklist_formatter.py | 35-42          | None                  |
| find_pipes                 | Locates pipe separators in Markdown, ignoring escaped or code-span pipes.      | checklist_formatter.py | 44-73          | None                  |
| process_table_block        | Aligns a contiguous block of Markdown table rows.                              | checklist_formatter.py | 75-124         | None                  |
| process_stream             | Sequentially processes file stream for table detection and alignment.          | checklist_formatter.py | 126-147        | None                  |
| align_checklist            | Entry point for aligning a specific file using temporary buffers.              | checklist_formatter.py | 149-176        | None                  |
| compact_table_row          | Removes excessive padding from table cells while preserving one-space padding. | checklist_formatter.py | 178-206        | None                  |
| undo_stream                | Processes file stream for table compaction.                                    | checklist_formatter.py | 207-218        | None                  |
| undo_checklist             | Entry point for compacting tables in a file.                                   | checklist_formatter.py | 220-246        | None                  |
| load_gitignore_exclusions  | Parses .gitignore to build a set of excluded directories.                      | checklist_formatter.py | 248-277        | None                  |
| find_checklists            | Recursively searches for *_CHECKLIST.md files with exclusion pruning.          | checklist_formatter.py | 279-295        | None                  |
| main                       | CLI entry point for the alignment utility.                                     | checklist_formatter.py | 297-327        | None                  |
| generate_codebase_markdown | Scans files and aggregates source code into a manifest.                        | search_copy.py         | 4-135          | None                  |
| create_ascii_box           | Generates centered ASCII boxes for visual organization.                        | search_copy.py         | 88-104         | None                  |