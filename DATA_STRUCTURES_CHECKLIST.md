# DATA_STRUCTURES_CHECKLIST.md

| [Name]          | [Description]                                                             | [File Name]            | [Line Numbers] | [Logging Integration] |
| ---             | ---                                                                       | ---                    | ---            | ---                   |
| EXCLUDED_DIRS   | Set containing protected directories that must not be traversed.          | checklist_formatter.py | 18-22          | None                  |
| checklists      | List of Path objects for found checklist files in the tree.               | checklist_formatter.py | 286, 303       | None                  |
| files_by_lang   | defaultdict of lists used to aggregate code content by language.          | search_copy.py         | 51, 73         | None                  |
| lang_volumes    | Dictionary storing total character counts per language for sorting.       | search_copy.py         | 79, 82         | None                  |
| lang_extensions | Immutable-style dictionary for mapping language categories to extensions. | search_copy.py         | 21-42          | None                  |