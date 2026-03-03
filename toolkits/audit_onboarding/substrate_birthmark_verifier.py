#!/usr/bin/env python3
import os
import yaml
import datetime
import re
import subprocess
import json

# ==================== CONFIGURE THIS ====================
REMOTE_NAME = "gdrive1tb"
SUBSTRATE_ROOT = "/home/jwils/GoogleDrive1TB/PapiBobes/.blueprints"

# Optional: restrict to specific folders (set to [] to process EVERY .md file)
FOLDERS_TO_AUDIT = ['roles', 'protocols']

# ==================== DATE FIELDS TO MANAGE ====================
# The script will STRIP every occurrence of these keys, then re-insert
# the correct values at the very bottom of the frontmatter.
DATE_FIELDS_TO_MANAGE = [
    "date_created",     # seniority (btime)
    "date_modified",    # always updated
    "last_updated",     # clean up any old variants
]
CREATED_FIELD = "date_created"
MODIFIED_FIELD = "date_modified"   # ← change if you ever rename it
# ============================================================

def get_rclone_remote_root() -> str:
    return f"{REMOTE_NAME}:PapiBobes/.blueprints"

def build_metadata_map() -> dict[str, dict]:
    remote_root = get_rclone_remote_root()
    print(f"Fetching full metadata from Google Drive (one call for the entire vault)...")

    try:
        result = subprocess.run(
            ['rclone', 'lsjson', '-R', '--metadata', remote_root],
            capture_output=True,
            text=True,
            check=True,
            timeout=90
        )
        data = json.loads(result.stdout)
    except Exception as e:
        print(f"rclone bulk fetch failed: {e}")
        return {}

    meta_map = {}
    for entry in data:
        path = entry.get('Path', '')
        if not path.lower().endswith('.md'):
            continue

        metadata = entry.get('Metadata', {})
        btime = metadata.get('btime')
        mod_time = metadata.get('ModTime')

        created = datetime.datetime.now().strftime('%Y-%m-%d')
        if btime and not btime.startswith('1969'):
            clean = btime.split('.')[0].replace('Z', '+00:00')
            created = datetime.datetime.fromisoformat(clean).strftime('%Y-%m-%d')

        updated = datetime.datetime.now().strftime('%Y-%m-%d')
        if mod_time:
            clean = mod_time.split('.')[0].replace('Z', '+00:00')
            updated = datetime.datetime.fromisoformat(clean).strftime('%Y-%m-%d')

        meta_map[path] = {'created': created, 'updated': updated}

    print(f"Loaded metadata for {len(meta_map):,} files.")
    return meta_map

def get_file_metadata(filepath: str, meta_map: dict) -> dict:
    try:
        rel_path = os.path.relpath(filepath, SUBSTRATE_ROOT)
    except Exception:
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        return {'created': now, 'updated': now}
    return meta_map.get(rel_path) or {
        'created': datetime.datetime.now().strftime('%Y-%m-%d'),
        'updated': datetime.datetime.now().strftime('%Y-%m-%d')
    }

def verify_and_inject_seniority(filepath: str, meta_map: dict, force_correct: bool = False):
    if not filepath.endswith('.md'):
        return
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return

    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return
    yaml_content = match.group(1)
    body = content[match.end():]

    try:
        data = yaml.safe_load(yaml_content) or {}
    except yaml.YAMLError:
        return

    meta = get_file_metadata(filepath, meta_map)
    true_created = meta['created']
    true_updated = meta['updated']

    current_created = data.get(CREATED_FIELD)

    should_update_created = (current_created is None or current_created == "") or \
                            (force_correct and current_created != true_created)

    # Always update modified date
    if should_update_created or True:   # we always refresh modified
        lines = yaml_content.split('\n')
        new_lines = []

        # STRIP PHASE: remove every occurrence of any date field we manage
        for line in lines:
            stripped = line.strip()
            if any(stripped.startswith(f"{field}:") for field in DATE_FIELDS_TO_MANAGE):
                continue
            new_lines.append(line)

        # INSERT PHASE: add both fields at the VERY BOTTOM (clean & predictable)
        new_lines.append(f"{CREATED_FIELD}: {true_created}")
        new_lines.append(f"{MODIFIED_FIELD}: {true_updated}")

        new_yaml = '---\n' + '\n'.join(new_lines) + '\n---\n'

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_yaml + body)

        # Print status
        if should_update_created:
            print(f"Δ {os.path.basename(filepath)}: Updated {CREATED_FIELD} → {true_created}")
        print(f"Δ {os.path.basename(filepath)}: Updated {MODIFIED_FIELD} → {true_updated}")

    else:
        print(f"✓ {os.path.basename(filepath)} verified (created={current_created}, modified={data.get(MODIFIED_FIELD)})")

def run_seniority_audit(force: bool = False):
    meta_map = build_metadata_map()

    for root, dirs, files in os.walk(SUBSTRATE_ROOT):
        if FOLDERS_TO_AUDIT and not any(folder in root for folder in FOLDERS_TO_AUDIT):
            continue
        for file in files:
            if file.endswith('.md'):
                verify_and_inject_seniority(os.path.join(root, file), meta_map, force_correct=force)

if __name__ == "__main__":
    # Run once with force=True to clean up duplicates and set correct dates
    # Then switch to force=False for normal verification
    run_seniority_audit(force=False)