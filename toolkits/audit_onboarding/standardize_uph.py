#!/usr/bin/env python3
import os
import re
import glob
import yaml

ROLES_DIR = "/home/jwils/GoogleDrive1TB/PapiBobes/.blueprints/roles/*.md"
PROTO_DIR = "/home/jwils/GoogleDrive1TB/PapiBobes/.blueprints/protocols/*.md"

def update_file(filepath):
    # Skip temporary/artifact files
    if "temp_" in os.path.basename(filepath) or "substrate_assimilation_protocol" in filepath:
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract YAML frontmatter
    match = re.search(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        print(f"Skipping {filepath}, no YAML frontmatter detected.")
        return
    
    yaml_content = match.group(1)
    body = match.group(2)
    
    try:
        data = yaml.safe_load(yaml_content) or {}
    except Exception as e:
        print(f"Failed to parse YAML in {filepath}: {e}")
        return
        
    new_data = {}
    is_role = 'roles/' in filepath
    
    # 1. Base UPH Standards Injection
    if is_role:
        new_data['protocol_id'] = "N/A (Agent Role)"
    else:
        new_data['protocol_id'] = data.get('protocol_id', os.path.basename(filepath).replace('.md', '').upper())
        
    new_data['structure_status'] = data.get('structure_status', 'HARDENED')
    
    # Smart Audience inferencing
    if 'target_audience' in data:
        new_data['target_audience'] = data['target_audience']
    else:
        new_data['target_audience'] = 'Verification_Agent, Orchestrator_Agent'
        
    # Smart Role inferencing
    if 'assigned_role' in data:
        new_data['assigned_role'] = data['assigned_role']
    elif 'role' in data:
        new_data['assigned_role'] = data['role']
    else:
        new_data['assigned_role'] = 'System'

    # Smart Purpose inferencing (looks at existing purpose or first sentence)
    if 'purpose' in data:
        new_data['purpose'] = data['purpose']
    else:
        purpose_match = re.search(r'Purpose:\s*(.+)', body, re.IGNORECASE)
        if purpose_match:
            new_data['purpose'] = purpose_match.group(1).strip()
        else:
            new_data['purpose'] = 'Execute designated protocol or role functions within the substrate.'

    # Standard metrics
    new_data['version'] = data.get('version', '1.0.0')
    new_data['status'] = data.get('status', 'ACTIVE')
    new_data['date_created'] = data.get('date_created', '2026-03-02')
    new_data['date_modified'] = data.get('date_modified', '2026-03-03')
    
    # 2. Preserve other custom fields like `role`, `protocol_dependencies`, `supersedes`
    for k, v in data.items():
        if k not in new_data:
            new_data[k] = v
            
    # 3. Order the output to visually match UPH cleanly
    ordered_keys = ['role', 'protocol_id', 'structure_status', 'target_audience', 'assigned_role', 'purpose', 'protocol_dependencies', 'version', 'status', 'date_created', 'date_modified']
    
    final_yaml = []
    
    for k in ordered_keys:
        if k in new_data:
            val = new_data[k]
            if isinstance(val, str) and '\n' not in val:
                final_yaml.append(f"{k}: {val}")
            else:
                final_yaml.append(yaml.dump({k: val}, default_flow_style=False).strip())
                
    for k, v in new_data.items():
        if k not in ordered_keys:
            final_yaml.append(yaml.dump({k: v}, default_flow_style=False).strip())
            
    final_content = "---\n" + "\n".join(final_yaml) + "\n---\n" + body
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print(f"Updated: {os.path.basename(filepath)}")

def main():
    print("--- Injecting UPH to Substrate Roles ---")
    for filepath in glob.glob(ROLES_DIR):
        update_file(filepath)
        
    print("\n--- Injecting UPH to Substrate Protocols ---")
    for filepath in glob.glob(PROTO_DIR):
        update_file(filepath)
        
    print("\n[SUCCESS] UPH standardization complete.")

if __name__ == "__main__":
    main()
