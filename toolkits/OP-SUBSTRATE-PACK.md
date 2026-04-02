# Workflow: Substrate Packaging & Migration (OP-SUBSTRATE-PACK)

**Status:** HARDENED
**Role:** Verification_Agent (12)
**Goal:** Ensure 100% integrity when moving the blueprint substrate across storage volumes.

---

## Step 1: Pre-Packaging Audit
- Ensure no active file locks are present.
- Verify `Universal_Protocol_Header` compliance (Zero-Finding State).

## Step 2: Atomic Compression
Execute the following command from the parent directory of `.blueprints`:

```bash
# Command to package and compress, excluding bulky/transient data
tar -cvpzf blueprints_backup_$(date +%F).tar.gz \
    --exclude='.venv' \
    --exclude='__pycache__' \
    --exclude='.pytest_cache' \
    .blueprints
```
- `-c`: Create archive.
- `-v`: Verbose (list files).
- `-p`: Preserve permissions.
- `-z`: Gzip compression.
- `-f`: Output file.

## Step 3: Integrity Verification (Checksum)
Immediately generate a checksum of the archive to verify success after the move:

```bash
sha256sum blueprints_backup_$(date +%F).tar.gz > blueprints_backup.sha256
```

## Step 4: Verification Post-Migration
After moving to the hard drive, run:

```bash
sha256sum -c blueprints_backup.sha256
```
- **Result:** `OK` indicates a flawless bit-for-bit migration.
- **Action:** If failure is detected, do NOT delete the source on Google Drive; re-attempt Step 2.
