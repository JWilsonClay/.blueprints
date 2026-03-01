# Operational Protocols

## Operational Protocol: Terminal Workflow
**User Workflow:** The user's role is strictly mechanical: **Copy, Paste, and Upload Logs**.
To maximize efficiency and minimize workload, the AI must provide complete, chained commands that handle all logging and error reporting automatically. The user will simply execute the block and upload the resulting log file (defined in Global Project Context) for the AI to analyze.

**AI Command Generation Rules:**
1.  **Structure:** Numbered descriptive headers (e.g., 'Command 1: Verify Qwen Restore') followed by the full command as a single-line chained string using `&&` (ensure the footer executes by using `;` or `||` logic where appropriate).
2.  **Environment:** Start every command with `cd <PROJECT_ROOT> && source <VENV_PATH>/bin/activate &&`. (Exception: Skip this prefix for System Command 0, system information queries, or initial project creation commands where the folder/venv does not yet exist). **CRITICAL:** If `<PROJECT_ROOT>` or `<VENV_PATH>` are not defined in the Global Project Context, **STOP** and ask the user to provide them before generating commands. Do not output literal placeholders.
3.  **Logging:** *Mandatory* automatic logging.
    *   Append output: `2>&1 | tee -a <LOG_PATH>` (Ensure <LOG_PATH> is replaced by the value in Global Project Context)
    *   Footer: `echo "=== COMMAND NAME COMPLETED ===" 2>&1 | tee -a <LOG_PATH>`
    *   Iteration Start: `System Command 0` (and ONLY Command 0) must overwrite the log file (use `tee` instead of `tee -a`). This enforces the "Transient Log Workflow": logs are cleared at the start of every new AI-User iteration to prevent file bloat and ensure the AI analyzes only the most recent execution context.
4.  **Error Handling:** Include `|| echo "Error..."` chains to log failures without crashing the user's terminal experience.
5.  **Timestamps:** Prefix completion echoes with `$(date)`.
6.  **Estimates:** Include estimated execution time inline.
7.  **Safety:** Use dry-runs for destructive commands (sed, rm) first.
8.  **Timeouts:** Use `timeout` for long-running ops (default 5 mins) to prevent hangs.
9.  **Verification:** Log environment details (e.g., `python --version`, `pwd`) at the start.
10. **Verbosity:** Include verbose flags (`-v`) where appropriate, capturing output via `2>&1 | tee -a ...`.
11. **Noise Control:** As an exception to Rule 3, for noisy commands, redirect stdout to null (`> /dev/null`) but keep errors (`2>> <LOG_PATH>`). Ensure status is echoed separately (e.g., `echo "Status..." && cmd > /dev/null 2>> <LOG_PATH>`).

## Global Directives: Project Management
At the beginning, if I mention a new project or provide a tree structure (via command output or description), immediately suggest terminal commands to create the project folder (e.g., mkdir project_name && cd project_name) and organize it logically (e.g., subfolders like src, tests, docs, logs; use mv to relocate files if needed). 
Base organization on best practices: group code in src, tests in tests, configs in config, etc. If no tree is provided yet, ask for one via a tree command suggestion.
At the end of each development stage (e.g., after completing a feature, testing, or any milestone I indicate), automatically review the current folder structure (based on any provided tree output or descriptions). 
Suggest terminal commands to: reorganize files if messy (e.g., mv *.py src/), create missing folders (e.g., mkdir backups), clean up temporary files/logs (e.g., rm -rf pycache; truncate large logs with 'echo "" > log_file' or mv to archive), and ensure consistency (e.g., git init if not present, or add .gitignore). 
Explain suggestions briefly before commands.

Global definition Manual Commands
Global format for Manual Commands: markdown with code block
Example:
```bash
# [Description of Manual Command]
command_to_execute arguments
```

Global format for Code Updates (Diff/Patch):
1. **System Command:** Use `printf`, `echo`, or `sed` to write files directly (preferred for automation).
2. **Diff/Block:** Provide a Unified Diff or full code block if manual review is needed.

System Command 0: Iteration Start & Log Reset
Estimated Time: Instant. **Purpose:** Resets the transient log file. This is the ONLY command that uses `tee` (overwrite). All subsequent commands in this iteration MUST use `tee -a` (append). This prevents multi-GB log files and isolates the context for the current cycle.
```bash
echo "=== New Iteration: [Description] - $(date '+%Y-%m-%d %H:%M:%S') ===" 2>&1 | tee <LOG_PATH>
```

System Command: Display Comprehensive System Information
```bash
(uname -a && lsb_release -a && cat /proc/cpuinfo | grep -E 'model name|cpu cores' && free -h && lspci | grep -i vga && (nvidia-smi 2>/dev/null || echo "No NVIDIA GPU detected") && python --version 2>&1 && df -h && uptime && whoami && echo "Installed packages summary: $(dpkg --list | wc -l) (Debian-based) or equivalent" && lscpu && lsblk -f && ip addr show && swapon --show) 2>&1 | tee -a <LOG_PATH>; echo "=== SYSTEM INFO DISPLAYED ===" 2>&1 | tee -a <LOG_PATH>
```

# Development Pipeline - Blueprints v1

## Global Project Context (copy this into every stage prompt)
Project Name: 
Project Root Path: 
Virtual Env Path: 
Log File Path: ~/Desktop/terminal.log  #USER DEFINED SETTING
Overall Goal: 
Languages Used: 
Key Libraries/Frameworks: 
Database / Storage: 
Frontend / GUI (if any): 
Current Architecture Summary: 
Last Major Change: 

## Stage 0: Requirements & Planning (expanded for robustness)

Goal: Capture complete requirements, skill gaps, tech stack decisions, feasibility, risks, milestones, and success criteria before any code.

Template:
### STAGE 0: Requirements & Planning

Global Project Context:
[PASTE GLOBAL PROJECT CONTEXT DEFINED ABOVE]

What I Want to Build: 
User Skills Available: 
Skills/Tech Stack to Acquire: 
Known Constraints (time, budget, platform, etc.): 
Non-functional Requirements (performance, security level, offline support, etc.): 
Key Features (list prioritized): 
Success Metrics: 

[Optional: paste any initial research or sketches]


## Quick Iteration Mode <!-- User Note: Save separately as quick_iteration_mode.md -->
When working rapidly on the same file/module in one session, use this shortened version instead of full context:

### QUICK ITERATION - Stage #[STAGE_NUMBER]
Current File/Module: 
Specific Focus: 
Code Snippet: 
[PASTE CODE]

For Quick Iteration, leave the Global Project Context section blank or write 'Refer to previous context' (Only use 'Refer to previous context' if staying within the same active LLM chat session. If starting a new session, Context is mandatory).
## Stage 1: Code Structure & Style

Goal: Ensure code follows language conventions, is readable, modular, and maintainable. Catch style violations early.

Template:
### STAGE 1: Code Structure & Style

Global Project Context:
[PASTE GLOBAL PROJECT CONTEXT DEFINED ABOVE]

Code to Review (paste full module/file here):

Specific Style/Readability Concerns (optional):

Checklist:
- Updated Global Project Context?
- Provided refactored code (System Command or Diff)?
- Updated Last Major Change?
- Noted any new directives or decisions?

## Stage 2: Functional Correctness

Goal: Verify the code matches intended requirements and behaves correctly under normal conditions.

Template:
### STAGE 2: Functional Correctness

Global Project Context:
[PASTE GLOBAL PROJECT CONTEXT DEFINED ABOVE]

Intended Behavior / Requirements Summary:
Key Functions/Modules to Verify:

Code to Analyze:

Checklist:
- Updated Global Project Context?
- Provided corrected code (System Command or Diff)?
- Updated Last Major Change?
- Noted any requirement gaps found?

## Stage 3: Debugging / Specific Issues

Goal: Diagnose and fix targeted bugs or unexpected behavior.

Template:
### STAGE 3: Debugging / Specific Issues

Global Project Context:
[PASTE GLOBAL PROJECT CONTEXT DEFINED ABOVE]

Specific Issue:
Error Message: 
File/Line: 
Reproduction Steps: 
Expected Behavior: 
Actual Behavior: 

Code Snippet:

What I've Already Tried:

Checklist:
- Updated Global Project Context?
- Provided fixed code (System Command or Diff)?
- Updated Last Major Change?
- Reproduced fix locally?

## Stage 4: Security Audit

Goal: Identify vulnerabilities, data handling issues, and security best practices gaps.

Template:
### STAGE 4: Security Audit

Global Project Context:
[PASTE GLOBAL PROJECT CONTEXT DEFINED ABOVE]

Specific Security Focus Areas (e.g., input validation, auth, data storage):

Code / Modules Handling Sensitive Data:

Threat Model Notes:

Checklist:
- Updated Global Project Context?
- Provided security fixes (System Command or Diff)?
- Updated Last Major Change?
- Reviewed dependencies/vulnerabilities?

## Stage 5: Testing Strategy

Goal: Define and implement comprehensive tests (unit, integration, edge cases).

Template:
### STAGE 5: Testing Strategy

Global Project Context:
[PASTE GLOBAL PROJECT CONTEXT DEFINED ABOVE]

Key Functions/Modules to Test:
Test Types Needed (unit, integration, property-based, etc.):

Existing Tests (if any):

Checklist:
- Updated Global Project Context?
- Provided test code (System Command or Diff)?
- Updated Last Major Change?
- Ran tests successfully?

## Stage 6: Performance / Optimization

Goal: Identify bottlenecks, improve efficiency, and optimize resource usage.

Template:
### STAGE 6: Performance / Optimization

Global Project Context:
[PASTE GLOBAL PROJECT CONTEXT DEFINED ABOVE]

Known Performance Concerns or Hot Paths:
Benchmarks / Profiling Data (if available):

Code to Optimize:

Checklist:
- Updated Global Project Context?
- Provided optimized code (System Command or Diff)?
- Updated Last Major Change?
- Verified performance improvement?

## Stage 7: Documentation & Maintainability

Goal: Add comments, docstrings, README updates, type hints, and architectural notes.

Template:
### STAGE 7: Documentation & Maintainability

Global Project Context:
[PASTE GLOBAL PROJECT CONTEXT DEFINED ABOVE]

Files/Modules Needing Documentation:
Specific Documentation Needs:

Checklist:
- Updated Global Project Context?
- Provided documentation updates (System Command or Diff)?
- Updated Last Major Change?
- README current?

## Stage 8: Final Integration Review

Goal: Ensure the module integrates well with the overall architecture, check consistency, and prepare for next iteration.

Template:
### STAGE 8: Final Integration Review

Global Project Context:
[PASTE GLOBAL PROJECT CONTEXT DEFINED ABOVE]

Modules Affected by Recent Changes:
Integration Points / Dependencies:

Overall Concerns:

Checklist:
- Updated Global Project Context?
- Provided integration commands/diffs?
- Updated Last Major Change?
- Ready for next stage or release?
