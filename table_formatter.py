#!/usr/bin/env python3
"""
table_formatter.py
Aligns ALL Markdown tables in matching files in the entire project tree using space padding.
Calculates column width and applies standard spacing.
Idempotent, safe, recursive.
"""

import argparse
import fnmatch
import pickle
import os
from pathlib import Path
import shutil
import sys
import tempfile
from dataclasses import dataclass, field
from typing import Iterable, Iterator, List, Set, Tuple

@dataclass
class FormatterConfig:
    tab_width: int = 4
    excluded_dirs: Set[str] = field(default_factory=lambda: {
        '.git', 'node_modules', 'venv', '.venv', 'env', '.env', 
        'dist', 'build', 'target', '__pycache__', '.idea', '.vscode',
        'vendor', 'bin', 'obj'
    })

def get_visual_width(s: str, tab_width: int = 4) -> int:
    """Calculates the visual width of a string, accounting for tab expansion."""
    width = 0
    for char in s:
        if char == '\t':
            # Advance to the next tab stop
            width += tab_width - (width % tab_width)
        else:
            width += 1
    return width

def get_needed_tabs(current_width: int, target_width: int, tab_width: int = 4) -> int:
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

def split_by_pipes(line: str) -> List[str]:
    """Splits a line into segments based on pipe delimiters."""
    pipes = find_pipes(line)
    if not pipes:
        return [line]
    
    segments = []
    last_idx = 0
    for idx in pipes:
        segments.append(line[last_idx:idx])
        last_idx = idx + 1
    segments.append(line[last_idx:])
    return segments

class TableFormatter:
    """
    Encapsulates logic for formatting Markdown tables.
    Decoupled from file I/O.
    """
    def __init__(self, tab_width: int = 4):
        self.tab_width = tab_width
        self.changed = False

    def process(self, lines: Iterable[str]) -> Iterator[str]:
        """
        Processes a stream of lines, buffering table blocks to disk to handle large tables.
        """
        in_table = False
        table_buffer = None
        max_widths = {}

        for line in lines:
            if line.strip().startswith('|'):
                segments = split_by_pipes(line)
                # A valid table row usually has at least 2 pipes (3 segments: empty, content, empty)
                if len(segments) < 3:
                    if in_table:
                        yield from self._flush_table(table_buffer, max_widths)
                        table_buffer.close()
                        table_buffer = None
                        in_table = False
                    yield line
                    continue

                if not in_table:
                    in_table = True
                    table_buffer = tempfile.TemporaryFile(mode='w+b')
                    max_widths = {}

                # Pass 1: Analyze widths and buffer to disk
                pickle.dump((line, segments), table_buffer)
                
                # Update widths for content segments (between pipes)
                for i in range(1, len(segments) - 1):
                    content = segments[i].rstrip()
                    w = get_visual_width(content, self.tab_width)
                    if w > max_widths.get(i, 0):
                        max_widths[i] = w
            else:
                if in_table:
                    yield from self._flush_table(table_buffer, max_widths)
                    table_buffer.close()
                    table_buffer = None
                    in_table = False
                yield line
        
        if in_table:
            yield from self._flush_table(table_buffer, max_widths)
            table_buffer.close()

    def _flush_table(self, buffer, max_widths):
        buffer.seek(0)
        while True:
            try:
                original_line, segments = pickle.load(buffer)
            except EOFError:
                break

            # Pass 2: Reconstruct with padding
            new_line = segments[0]
            for i in range(1, len(segments) - 1):
                new_line += "|"
                content = segments[i].rstrip()
                target_width = max_widths.get(i, 0)
                current_width = get_visual_width(content, self.tab_width)
                
                # Ensure at least 1 space padding
                padding = (target_width + 1) - current_width
                if padding < 1: padding = 1
                
                new_line += content + (" " * padding)
            
            if len(segments) > 1:
                new_line += "|" + segments[-1]

            if new_line != original_line:
                self.changed = True
            
            yield new_line

def process_stream(src, dst, tab_width: int) -> bool:
    """Helper to process the file stream for alignment."""
    formatter = TableFormatter(tab_width)
    for line in formatter.process(src):
        dst.write(line)
    return formatter.changed

def align_checklist(file_path: Path, tab_width: int = 4) -> bool:
    """Aligns tables in a checklist file using a temp file to reduce memory usage."""
    fd, temp_path = tempfile.mkstemp(dir=file_path.parent, text=True)
    os.close(fd)

    changed_file = False

    try:
        # Attempt 1: Try UTF-8
        try:
            with open(file_path, 'r', encoding='utf-8', newline='') as src, \
                 open(temp_path, 'w', encoding='utf-8', newline='') as dst:
                changed_file = process_stream(src, dst, tab_width)
        except UnicodeDecodeError:
            # Attempt 2: Fallback to Latin-1 (preserves bytes, converts to UTF-8)
            with open(file_path, 'r', encoding='latin-1', newline='') as src, \
                 open(temp_path, 'w', encoding='utf-8', newline='') as dst:
                changed_file = process_stream(src, dst, tab_width)
    except Exception:
        os.remove(temp_path)
        raise

    if changed_file:
        shutil.move(temp_path, file_path)
        return True
    else:
        os.remove(temp_path)
        return False

def compact_table_row(line: str) -> str:
    """
    Removes extra whitespace padding from a table row, preserving 1 space padding.
    """
    pipes = find_pipes(line)
    if not pipes:
        return line

    segments = []
    start = 0
    for i, p in enumerate(pipes):
        raw = line[start:p]
        if i == 0:
            # Preserve indentation
            segments.append(raw)
        else:
            # Compact cell content
            stripped = raw.strip()
            segments.append(f" {stripped} ")
        
        segments.append("|")
        start = p + 1
        
    # Handle trailing content (e.g. newline)
    trailing = line[start:]
    segments.append(trailing)
    
    return "".join(segments)

def undo_stream(src, dst) -> bool:
    """Helper to process the file stream for undoing alignment (compacting)."""
    changed = False
    for line in src:
        if line.strip().startswith('|'):
            new_line = compact_table_row(line)
            if new_line != line:
                changed = True
            dst.write(new_line)
        else:
            dst.write(line)
    return changed

def undo_checklist(file_path: Path) -> bool:
    """Compact table lines in the file using a temp file."""
    fd, temp_path = tempfile.mkstemp(dir=file_path.parent, text=True)
    os.close(fd)

    changed = False
    try:
        # Attempt 1: Try UTF-8
        try:
            with open(file_path, 'r', encoding='utf-8', newline='') as src, \
                 open(temp_path, 'w', encoding='utf-8', newline='') as dst:
                changed = undo_stream(src, dst)
        except UnicodeDecodeError:
            # Attempt 2: Fallback to Latin-1
            with open(file_path, 'r', encoding='latin-1', newline='') as src, \
                 open(temp_path, 'w', encoding='utf-8', newline='') as dst:
                changed = undo_stream(src, dst)
    except Exception:
        os.remove(temp_path)
        raise

    if changed:
        shutil.move(temp_path, file_path)
        return True
    else:
        os.remove(temp_path)
        return False

def load_gitignore_patterns(root: Path) -> List[str]:
    """
    Parses .gitignore in the root directory to identify patterns to exclude.
    Returns a list of glob patterns.
    """
    patterns = []
    gitignore_path = root / '.gitignore'
    
    if not gitignore_path.exists():
        return patterns

    try:
        with open(gitignore_path, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Normalize pattern: remove trailing slash (directory indicator)
                # to allow fnmatch to match against directory names.
                clean_pattern = line.rstrip('/')
                if clean_pattern:
                    patterns.append(clean_pattern)
    except OSError:
        pass
    return patterns

def find_checklists(root: Path, pattern: str = "*CHECKLIST.md", ignore_patterns: List[str] = None) -> List[Path]:
    """
    Recursively finds files matching the pattern, respecting excluded directories via glob patterns.
    """
    if ignore_patterns is None:
        ignore_patterns = list(FormatterConfig().excluded_dirs)

    checklists = []
    # Scalable traversal with exclusion pruning
    for dirpath, dirnames, filenames in os.walk(root):
        # Modify dirnames in-place to prevent traversing excluded directories
        # Identify directories that match any ignore pattern
        dirs_to_remove = []
        for d in dirnames:
            for p in ignore_patterns:
                if fnmatch.fnmatch(d, p):
                    dirs_to_remove.append(d)
                    break
        
        for d in dirs_to_remove:
            dirnames.remove(d)
        
        for f in filenames:
            if fnmatch.fnmatch(f, pattern):
                checklists.append(Path(dirpath) / f)
    return checklists

def main():
    parser = argparse.ArgumentParser(description="Aligns Markdown tables in project files (table_formatter).")
    parser.add_argument("--pattern", default="*CHECKLIST.md", help="File pattern to match (default: *CHECKLIST.md)")
    parser.add_argument("--undo", action="store_true", help="Remove alignment padding")
    args = parser.parse_args()

    root = Path(".")
    config = FormatterConfig()
    
    # Load dynamic exclusions from .gitignore and combine with defaults
    ignore_patterns = list(config.excluded_dirs)
    ignore_patterns.extend(load_gitignore_patterns(root))
    
    checklists = find_checklists(root, pattern=args.pattern, ignore_patterns=ignore_patterns)

    if not checklists:
        print(f"No files matching '{args.pattern}' found.")
        return
        
    if args.undo:
        print(f"Undo mode: Removing all tabs from {len(checklists)} files matching '{args.pattern}'...\n")
        for file in checklists:
            if undo_checklist(file):
                print(f"✓ Undid tabs -> {file.name}")
            else:
                print(f"✓ No tabs to undo -> {file.name}")
        print("\nAll tabs removed from checklists.")
        return

    print(f"Found {len(checklists)} files matching '{args.pattern}'. Starting alignment (Spaces)...\n")
    for file in checklists:
        if align_checklist(file, tab_width=config.tab_width):
            print(f"✓ Aligned -> {file.name}")
        else:
            print(f"✓ Already perfectly aligned -> {file.name}")

    print("\nAll checklists are now visually aligned.")

if __name__ == "__main__":
    main()
