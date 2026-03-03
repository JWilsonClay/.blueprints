#!/usr/bin/env python3
import os
import sys
import yaml
import re
import difflib
from datetime import datetime

# ==================== CONFIGURE THIS ====================
VARIANCE_THRESHOLD = 10.0          # % structural difference to trigger assimilation
CREATED_FIELD = "date_created"     # must match your birthmark script
# =======================================================

def extract_frontmatter_and_body(content: str):
    """Robust extraction used by your birthmark verifier."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}, content
    yaml_content = match.group(1)
    body = content[match.end():]
    try:
        data = yaml.safe_load(yaml_content) or {}
    except yaml.YAMLError:
        data = {}
    return data, body

def get_date_created(filepath: str) -> str | None:
    """Returns date_created or None."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        data, _ = extract_frontmatter_and_body(content)
        return data.get(CREATED_FIELD)
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
        return None

def calculate_structural_variance(content1: str, content2: str) -> float:
    """Variance on body only (ignores frontmatter and whitespace)."""
    _, body1 = extract_frontmatter_and_body(content1)
    _, body2 = extract_frontmatter_and_body(content2)
    
    # Normalize whitespace for fair comparison
    body1 = ' '.join(body1.strip().split())
    body2 = ' '.join(body2.strip().split())
    
    seq = difflib.SequenceMatcher(None, body1, body2)
    return (1.0 - seq.ratio()) * 100

def validate_seniority(senior_path: str, junior_path: str, threshold: float = VARIANCE_THRESHOLD):
    """
    Returns: (reformat_required: bool, rationale: str)
    """
    if not os.path.exists(senior_path) or not os.path.exists(junior_path):
        return False, "One or both files do not exist."

    senior_date_str = get_date_created(senior_path)
    junior_date_str = get_date_created(junior_path)

    if not senior_date_str or not junior_date_str:
        return False, f"Missing {CREATED_FIELD} in one or both files."

    try:
        senior_dt = datetime.strptime(str(senior_date_str), '%Y-%m-%d')
        junior_dt = datetime.strptime(str(junior_date_str), '%Y-%m-%d')
    except ValueError as e:
        return False, f"Date parse error: {e}"

    # Junior must be strictly younger to be a candidate for assimilation
    if junior_dt <= senior_dt:
        return False, f"Bypass: Junior ({junior_date_str}) is not younger than Senior ({senior_date_str})."

    # --- Dynamic Seniority Weighting Logic ---
    age_delta = (junior_dt - senior_dt).days
    
    # 1. Peer Tolerance: Both are hardened, suppress reformat for minor differences
    if age_delta < 30:
        actual_threshold = 20.0
        reason_prefix = "Peer Tolerance Applied (<30d delta)"
    # 2. Anchor Enforcement: Senior is an ancient anchor, enforce strict compliance
    elif age_delta > 60:
        actual_threshold = 5.0
        reason_prefix = "Anchor Enforcement Applied (>60d delta)"
    # 3. Standard
    else:
        actual_threshold = threshold
        reason_prefix = "Standard Threshold Applied"

    variance = calculate_structural_variance(
        open(senior_path, encoding='utf-8').read(),
        open(junior_path, encoding='utf-8').read()
    )

    if variance > actual_threshold:
        return True, (f"ASSIMILATE: {reason_prefix}. Junior ({junior_date_str}) is younger than Senior ({senior_date_str}) "
                     f"with {variance:.2f}% structural variance (threshold {actual_threshold}%).")
    else:
        return False, (f"Bypass: {reason_prefix}. Junior is younger but variance ({variance:.2f}%) "
                       f"is below threshold ({actual_threshold}%). Safe to keep separate.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 role_seniority_validator.py <senior_file.md> <junior_file.md>")
        sys.exit(1)

    reformat_required, rationale = validate_seniority(sys.argv[1], sys.argv[2])
    
    print(f"REFORMAT_REQUIRED: {reformat_required}")
    print(f"RATIONALE: {rationale}")
    
    # Exit 1 = agent should trigger assimilation/refinement
    # Exit 0 = safe to leave as-is
    sys.exit(1 if reformat_required else 0)