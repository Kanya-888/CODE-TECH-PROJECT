import hashlib
import os
import json
import time

# File where hashes will be stored
HASH_RECORD_FILE = "file_hashes.json"

# Function to calculate SHA-256 hash of a file
def calculate_file_hash(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")
        return None

# Load stored hashes
def load_hashes():
    if os.path.exists(HASH_RECORD_FILE):
        with open(HASH_RECORD_FILE, "r") as file:
            return json.load(file)
    return {}

# Save hashes to file
def save_hashes(hashes):
    with open(HASH_RECORD_FILE, "w") as file:
        json.dump(hashes, file, indent=4)

# Check file integrity
def check_integrity(file_paths):
    stored_hashes = load_hashes()
    new_hashes = {}

    for file_path in file_paths:
        hash_value = calculate_file_hash(file_path)
        if hash_value is None:
            continue

        new_hashes[file_path] = hash_value

        if file_path in stored_hashes:
            if stored_hashes[file_path] != hash_value:
                print(f"[WARNING] File changed: {file_path}")
            else:
                print(f"[OK] File unchanged: {file_path}")
        else:
            print(f"[INFO] New file detected: {file_path}")

    # Update the stored hashes
    save_hashes(new_hashes)

# -----------------------------
# Example usage
# -----------------------------
if _name_ == "_main_":
    print("File Integrity Checker - Monitoring files...")

    # List of files to monitor
    files_to_monitor = [
        "example1.txt",  # Change this to your actual file paths
        "example2.txt"
    ]

    # Check integrity every 10 seconds (you can change interval)
    try:
        while True:
            print("\n[INFO] Running file integrity check...")
            check_integrity(files_to_monitor)
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n[INFO] Monitoring stopped by user.")