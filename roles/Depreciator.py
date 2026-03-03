import os
import zipfile
import shutil

# --- CONFIGURATION (Target these for template reuse) ---
TARGET_DIR = "/home/jwils/GoogleDrive1TB/PapiBobes/.blueprints/roles"
ARCHIVE_NAME = "deprecated_agents.zip"

FILES_TO_DEPRECATE = [
    "00_Protocol_Auditor",
    "02_Build_Agent.md",
    "03_Refinement_Agent.md",
    "11_Testing_Agent.md",
    "12_Integration_Agent.md",
    "13_Evaluation_Agent.md",
    "14_Documentation_Agent.md",
    "15_Optimization_Agent.md",
    "16_Orchestration_Agent.md"
]
# -------------------------------------------------------

def create_zip_archive(target_dir, files, archive_name):
    """Zips the specified files."""
    archive_path = os.path.join(target_dir, archive_name)
    print(f"[*] Creating archive: {archive_path}")
    
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            file_path = os.path.join(target_dir, file)
            if os.path.exists(file_path):
                print(f"    Adding: {file}")
                zipf.write(file_path, arcname=file)
            else:
                print(f"    Warning: {file} not found, skipping.")
                
    return archive_path

def verify_zip_integrity(archive_path):
    """Verifies that the generated zip file is not corrupted."""
    print(f"[*] Verifying integrity of: {archive_path}")
    try:
        with zipfile.ZipFile(archive_path, 'r') as zipf:
            if zipf.testzip() is None:
                print("    [+] Verification Successful: Archive is intact.")
                return True
            else:
                print("    [-] Verification Failed: Internal corruption detected.")
                return False
    except Exception as e:
        print(f"    [-] Verification Error: {e}")
        return False

def deprecate_files(target_dir, files):
    """Moves the original files to a simulated trash by appending a timestamp extension if a trash module isn't available."""
    print("[*] Archiving verified, removing original files...")
    
    # We create a local .trash directory inside the workspace to ensure consistent fallback across OS types.
    trash_dir = os.path.join(target_dir, ".trash")
    os.makedirs(trash_dir, exist_ok=True)

    for file in files:
        file_path = os.path.join(target_dir, file)
        if os.path.exists(file_path):
            try:
                # Move to a local .trash directory instead of strict system trash to avoid dependency (send2trash) issues.
                shutil.move(file_path, os.path.join(trash_dir, file))
                print(f"    [+] Trashed: {file}")
            except Exception as e:
                print(f"    [-] Error trashing {file}: {e}")

if __name__ == "__main__":
    print("-" * 50)
    print("Executing Depreciator Script...")
    print("-" * 50)
    
    archive_path = create_zip_archive(TARGET_DIR, FILES_TO_DEPRECATE, ARCHIVE_NAME)
    
    if verify_zip_integrity(archive_path):
        deprecate_files(TARGET_DIR, FILES_TO_DEPRECATE)
        print("\n[SUCCESS] Deprecation process completed seamlessly.")
    else:
        print("\n[CRITICAL ERROR] Archive verification failed. Origial files were NOT removed.")
        print("Please investigate the archive for corruption.")
