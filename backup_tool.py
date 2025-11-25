#!/usr/bin/env python3
"""
Backup Tool: create timestamped backups of files or directories.

Usage:
  python3 backup_tool.py document.txt
  python3 backup_tool.py /path/to/project

Creates:
  document.txt.backup_20251122_103045
  project.backup_20251122_103045/
"""

import argparse
import shutil
import sys
import os
from datetime import datetime

def create_backup(source_path):
    """
    Create a backup of a file or directory with a timestamped suffix.
    Returns True on success, False on failure.
    """
    if not os.path.exists(source_path):
        print(f"Error: Source '{source_path}' does not exist.")
        return False

    # Generate timestamp: YYYYMMDD_HHMMSS
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{source_path}.backup_{timestamp}"

    try:
        if os.path.isfile(source_path):
            shutil.copy2(source_path, backup_name)
        elif os.path.isdir(source_path):
            shutil.copytree(source_path, backup_name)
        else:
            print(f"Error: '{source_path}' is neither a file nor a directory.")
            return False

        print(f"Backup created: {backup_name}")
        return True
    except Exception as e:
        print(f"Error during backup: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Create a timestamped backup of a file or directory.")
    parser.add_argument("source", help="Path to the file or directory to back up")
    args = parser.parse_args()

    success = create_backup(args.source)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()