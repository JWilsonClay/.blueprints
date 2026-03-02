# VARIABLES_CHECKLIST.md

| [Name]            | [Description]                                                         | [File Name]            | [Line Numbers] | [Logging Integration] |
| ---               | ---                                                                   | ---                    | ---            | ---                   |
| DEFAULT_TAB_WIDTH | Standard visual width for tab expansion calculations (set to 4).      | checklist_formatter.py | 16             | None                  |
| EXCLUDED_DIRS     | Set of directory names ignored during recursive file traversal.       | checklist_formatter.py | 18-22          | None                  |
| exclude_dirs      | Local set of directories excluded from codebase aggregation.          | search_copy.py         | 18-19          | None                  |
| lang_extensions   | Dictionary mapping language names to their supported file extensions. | search_copy.py         | 21-42          | None                  |
| ext_to_lang       | Inverted mapping of file extensions to language names.                | search_copy.py         | 45-48          | None                  |