#!/usr/bin/env python3
import os
import sys
import subprocess
from datetime import datetime, timedelta

# Paths
TOOLKIT_DIR = "/home/jwils/GoogleDrive1TB/PapiBobes/.blueprints/toolkits/audit_onboarding"
VALIDATOR = os.path.join(TOOLKIT_DIR, "role_seniority_validator.py")
TMP_SENIOR = "/tmp/sim_senior_role.md"
TMP_JUNIOR = "/tmp/sim_junior_role.md"

def create_role(path, date, role_name, audience, has_flow=True):
    content = f"""---
role: {role_name}
date_created: {date}
---
# Role: {role_name}
"""
    if audience:
        content += f"Target Audience: {audience}\n"
    if has_flow:
        content += "## [Flow: Dimensional]\n- Prep -> Safety -> Action\n"
    else:
        content += "## [Chaos Flow]\n- Action -> Action -> Maybe Safety?\n"
    
    with open(path, 'w') as f:
        f.write(content)

def run_validator(senior, junior):
    result = subprocess.run(['python3', VALIDATOR, senior, junior], capture_output=True, text=True)
    return result.returncode, result.stdout

def simulate_orchestrator(original_task, junior_path):
    print(f"\n>>> ORCHESTRATOR: Starting task: '{original_task}'")
    print(f">>> ORCHESTRATOR: Loading context from {junior_path}...")
    
    # 1. Pre-Flight Interception Gate
    print(">>> VERIFICATION_AGENT: Executing Interception Gate (Pre-Flight Seniority Audit)...")
    exit_code, output = run_validator(TMP_SENIOR, junior_path)
    
    if exit_code == 1:
        print("!!! ALERT: SUBSTRATE_SENIORITY_GAP (ASSIMILATION_REQUIRED) !!!")
        print(f">>> RATIONALE: {output.strip()}")
        print(">>> ORCHESTRATOR: Saving state to PIPELINE_STACK. Halted main thread.")
        
        # 2. Simulate OP-AGENT-ASSIMILATE (3-Cycle Reformat)
        print(">>> GENESIS_AGENT: Starting OP-AGENT-ASSIMILATE (3-Cycle Reformat Loop)...")
        print("    Cycle 1: Structural Injection... Done.")
        print("    Cycle 2: Logical Re-sequencing... Done.")
        print("    Cycle 3: Verification Audit... PASSED.")
        
        print(">>> ORCHESTRATOR: Substrate hardened. Repairing Junior file...")
        # (In a real scenario, the file would be overwritten here)
        
        # 3. Resume original task
        print(f">>> ORCHESTRATOR: Restoring state. Resuming original task: '{original_task}'")
        print(">>> AGENT: Writing the poem...")
        print("    The moon hangs low in the velvet sky,\n    Watching the silent world go by.\n    The substrate is strong, the logic is clear,\n    No drift or corruption shall ever be here.")
        return True
    else:
        print(">>> VERIFICATION_AGENT: Gate Passed. Proceeding with task.")
        print(f">>> AGENT: Writing the poem about '{original_task}' context...")
        return False

def main():
    today = datetime.now()
    ancient_date = (today - timedelta(days=90)).strftime('%Y-%m-%d')
    peer_date = (today - timedelta(days=85)).strftime('%Y-%m-%d')
    junior_date = today.strftime('%Y-%m-%d')

    print("=== ASSIMILATION DRIFT SIMULATION ===")
    
    # Create Ancient Anchor (Senior)
    create_role(TMP_SENIOR, ancient_date, "Orchestrator_Agent", "All Macro-Agents")

    # Scenario 1: Peer Files (Both ancient/hardened, minor difference)
    print("\n--- TEST 1: Peer Files (Age Delta < 30d) ---")
    create_role(TMP_JUNIOR, peer_date, "Junior_Peer_Agent", "Macro-Agents", has_flow=False)
    simulate_orchestrator("Write a poem about the moon", TMP_JUNIOR)

    # Scenario 2: Anchor vs Junior (Major delta, structural drift)
    print("\n--- TEST 2: Anchor vs Junior (Age Delta > 60d) ---")
    create_role(TMP_JUNIOR, junior_date, "Junior_Drift_Agent", "", has_flow=False)
    simulate_orchestrator("Write a poem about the moon", TMP_JUNIOR)

if __name__ == "__main__":
    main()
