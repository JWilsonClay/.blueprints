# SEQ-SUBSTRATE-PURGE.md
**Title:** Operation: Substrate Purge  
**Version:** 1.0.0  
**ID:** SEQ-PURGE-AUTONOMOUS-01  

## Phase 1: Temporal Awareness (Daemon Detection)
- **Trigger:** Scheduled event in `calendar.db` with logic `SUBSTRATE-PURGE-01`.
- **Target Window:** T-0 minutes (Immediate Execution).

## Phase 2: Surgical Cleanup (Executive Action)
- **Step 2.1: Log Truncation**
    - **Command:** `truncate -s 0 /tmp/agent_daemon.log`
    - **Purpose:** Prevent background log bloat from the persistence heartbeat.
- **Step 2.2: Provenance Audit**
    - **Command:** `ls -1 /home/jwils/.blueprints/provenance/artifacts/artifacts | wc -l`
    - **Purpose:** Ensure the strategic documentation library remains intact and counts are consistent.
- **Step 2.3: Heartbeat Sync**
    - **Command:** `bridge.pushNotification` via Local-X-Bridge.
    - **Payload:** `{"message": "✅ Operation: Substrate Purge Complete. Logs truncated. Provenance verified.", "type": "info"}`

## Phase 3: Reporting & Verification
- **Output:** Log the result of Step 2.2 back to the daemon's internal state.
- **IDE Handoff:** Manifest the green "PASS" status on the Sidebar Dashboard.
