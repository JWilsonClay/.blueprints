#!/usr/bin/env python3
"""
checklist_formatter.py
Aligns ALL *_CHECKLIST.md files in the entire project tree using space padding (CommonMark compliant).
Calculates column width and applies standard spacing.
Idempotent, safe, recursive.
"""

import os
from pathlib import Path
import sys
from typing import List, Set

DEFAULT_TAB_WIDTH = 4

EXCLUDED_DIRS = {
    '.git', 'node_modules', 'venv', '.venv', 'env', '.env', 
    'dist', 'build', 'target', '__pycache__', '.idea', '.vscode',
    'vendor', 'bin', 'obj'
}

def get_visual_width(s: str, tab_width: int = DEFAULT_TAB_WIDTH) -> int:
    """Calculates the visual width of a string, accounting for tab expansion."""
    width = 0
    for char in s:
        if char == '\t':
            # Advance to the next tab stop
            width += tab_width - (width % tab_width)
        else:
            width += 1
    return width

def get_needed_tabs(current_width: int, target_width: int, tab_width: int = DEFAULT_TAB_WIDTH) -> int:
    """Calculates how many tabs are needed to reach the target width from current width."""
    tabs = 0
    w = current_width
    while w < target_width:
        w += tab_width - (w % tab_width)
        tabs += 1
    return tabs

def find_pipes(line: str) -> List[int]:
    """
    Finds indices of pipes that act as column separators,
    ignoring escaped pipes (\|) and pipes within code spans (`...`).
    """
    indices = []
    i = 0
    n = len(line)
    in_code = False
    
    while i < n:
        char = line[i]
        
        if char == '\\':
            # Skip next char (escaped)
            i += 2
            continue
            
        if char == '`':
            # Toggle code state
            in_code = not in_code
            i += 1
            continue
            
        if char == '|' and not in_code:
            indices.append(i)
            
        i += 1
        
    return indices

def align_checklist(file_path: Path, tab_width: int = DEFAULT_TAB_WIDTH) -> bool:
    """Align one checklist file using spaces. Returns True if changes were made."""
    with open(file_path, 'r', encoding='utf-8', newline='') as f:
        lines = f.readlines()

    # Find the first real table row (the template/header line)
    table_start = None
    for i, line in enumerate(lines):
        # Heuristic: Starts with pipe and has at least 2 columns (3 pipes)
        if line.strip().startswith('|') and line.count('|') >= 3:
            table_start = i
            break
    if table_start is None:
        return False

    # Collect all consecutive table rows
    table_rows = []
    for i in range(table_start, len(lines)):
        line = lines[i]
        if not line.strip().startswith('|'):
            break
        table_rows.append((i, line))

    if not table_rows:
        return False

    # Template line tells us how many columns there are
    # We count pipes to determine columns.
    num_pipes = len(find_pipes(table_rows[0][1]))

    changed = False

    # Forward pass for every pipe column (first -> last) to ensure stability
    # We skip the first pipe (index 0) as it's the start of the line.
    # Range is 1-based index of pipes.
    for col in range(2, num_pipes + 1):
        # 1. Calculate visual positions and content width
        row_visual_data = [] # List of (pipe_string_index, visual_width, stripped_content)
        
        for _, line in table_rows:
            # Find all pipes
            pipes = find_pipes(line)
            
            if len(pipes) < col:
                row_visual_data.append(None)
                continue
            
            # Get the index of the pipe we are aligning
            pipe_idx = pipes[col - 1]
            
            # Calculate visual width of the content BEFORE this pipe
            content_before = line[:pipe_idx]
            # Strip trailing whitespace to standardize alignment
            stripped_content = content_before.rstrip()
            # We still use get_visual_width to account for any internal tabs in content
            v_width = get_visual_width(stripped_content, tab_width)
            
            row_visual_data.append((pipe_idx, v_width, stripped_content))

        # 2. Determine Benchmark (Max Visual Width)
        valid_data = [d for d in row_visual_data if d is not None]
        if not valid_data:
            continue
            
        max_width = max(d[1] for d in valid_data)
        
        # 3. Set Target: Max width + 1 space padding (Standard Markdown)
        target_v_width = max_width + 1

        # 4. Apply Alignment
        for j, (orig_idx, line) in enumerate(table_rows):
            data = row_visual_data[j]
            if data is None:
                continue
                
            pipe_idx, v_width, stripped_content = data
            
            needed = target_v_width - v_width
            if needed < 1: needed = 1
            
            new_segment = stripped_content + (' ' * needed)
            
            # Only update if the line segment actually changes
            if line[:pipe_idx] != new_segment:
                new_line = new_segment + line[pipe_idx:]
                
                lines[orig_idx] = new_line
                table_rows[j] = (orig_idx, new_line)
                changed = True

    if changed:
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            f.writelines(lines)
        return True
    return False

def undo_checklist(file_path: Path) -> bool:
    """Remove all tab characters from table lines in the file. Returns True if changes were made."""
    with open(file_path, 'r', encoding='utf-8', newline='') as f:
        lines = f.readlines()

    changed = False
    for i, line in enumerate(lines):
        if line.strip().startswith('|'):
            new_line = line.replace('\t', '')
            if new_line != line:
                lines[i] = new_line
                changed = True

    if changed:
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            f.writelines(lines)
        return True
    return False

def load_gitignore_exclusions(root: Path) -> Set[str]:
    """
    Parses .gitignore in the root directory to identify directories to exclude.
    """
    exclusions = set()
    gitignore_path = root / '.gitignore'
    
    if not gitignore_path.exists():
        return exclusions

    try:
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Normalize pattern to get directory name
                clean_name = line.strip('/')
                if '*' in clean_name: continue
                
                # If path is 'foo/bar', exclude 'bar' to align with name-based pruning
                if '/' in clean_name:
                    clean_name = clean_name.split('/')[-1]
                
                if clean_name:
                    exclusions.add(clean_name)
    except OSError:
        pass
    return exclusions

def find_checklists(root: Path, excluded_dirs: Set[str] = None) -> List[Path]:
    """
    Recursively finds *_CHECKLIST.md files, respecting excluded directories.
    """
    if excluded_dirs is None:
        excluded_dirs = EXCLUDED_DIRS

    checklists = []
    # Scalable traversal with exclusion pruning
    for dirpath, dirnames, filenames in os.walk(root):
        # Modify dirnames in-place to prevent traversing excluded directories
        dirnames[:] = [d for d in dirnames if d not in excluded_dirs]
        
        for f in filenames:
            if f.endswith("CHECKLIST.md"):
                checklists.append(Path(dirpath) / f)
    return checklists

def main():
    root = Path(".")
    
    # Load dynamic exclusions from .gitignore
    dynamic_exclusions = EXCLUDED_DIRS.union(load_gitignore_exclusions(root))
    
    checklists = find_checklists(root, excluded_dirs=dynamic_exclusions)

    if not checklists:
        print("No *CHECKLIST.md files found.")
        return
        
    if len(sys.argv) > 1 and sys.argv[1] == '--undo':
        print(f"Undo mode: Removing all tabs from {len(checklists)} checklist files...\n")
        for file in checklists:
            if undo_checklist(file):
                print(f"✓ Undid tabs -> {file.name}")
            else:
                print(f"✓ No tabs to undo -> {file.name}")
        print("\nAll tabs removed from checklists.")
        return

    print(f"Found {len(checklists)} checklist files. Starting alignment (Spaces)...\n")
    for file in checklists:
        if align_checklist(file, tab_width=DEFAULT_TAB_WIDTH):
            print(f"✓ Aligned -> {file.name}")
        else:
            print(f"✓ Already perfectly aligned -> {file.name}")

    print("\nAll checklists are now visually aligned.")

if __name__ == "__main__":
    main()
