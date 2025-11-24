#!/usr/bin/env python3
"""
Disk Monitor: checks free disk space and alerts if usage exceeds threshold.

This script is designed for system administrators and IT support staff
to monitor disk usage on critical systems. It returns a non-zero exit code
when disk usage is above the threshold, making it suitable for cron jobs
or monitoring pipelines.

Usage:
    python3 disk_monitor.py
    python3 disk_monitor.py --path /var --threshold 85
"""

import shutil
import sys
import argparse
import os

def get_disk_usage(path: str) -> tuple[int, int, int]:
    """
    Get disk usage statistics for the given path.

    Args:
        path (str): Filesystem path to check

    Returns:
        tuple: (total_bytes, used_bytes, free_bytes)

    Raises:
        FileNotFoundError: If the path does not exist
        PermissionError: If access to the path is denied
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path does not exist: {path}")
    total, used, free = shutil.disk_usage(path)
    return total, used, free

def format_bytes(bytes_value: int) -> str:
    """Convert bytes to human-readable string (GB)."""
    gb = bytes_value / (1024 ** 3)
    return f"{gb:.2f} GB"

def check_disk_usage(path: str = "/", threshold: int = 90) -> bool:
    """
    Check if disk usage exceeds the warning threshold.

    Args:
        path (str): Path to monitor (default: root '/')
        threshold (int): Usage percentage that triggers alert (default: 90)

    Returns:
        bool: True if usage is within limits, False if above threshold
    """
    try:
        total, used, free = get_disk_usage(path)
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    usage_percent = (used / total) * 100
    is_safe = usage_percent <= threshold

    # Output
    print(f"Path: {path}")
    print(f"Total: {format_bytes(total)}")
    print(f"Used:  {format_bytes(used)} ({usage_percent:.1f}%)")
    print(f"Free:  {format_bytes(free)}")

    if not is_safe:
        print(f"WARNING: Disk usage ({usage_percent:.1f}%) exceeds threshold ({threshold}%)", file=sys.stderr)
        return False

    print("Disk usage is within acceptable limits.")
    return True

def main():
    parser = argparse.ArgumentParser(description="Monitor disk usage and alert on high consumption.")
    parser.add_argument("--path", "-p", default="/", help="Filesystem path to check (default: /)")
    parser.add_argument("--threshold", "-t", type=int, default=90, help="Usage percent threshold (default: 90)")
    args = parser.parse_args()

    success = check_disk_usage(path=args.path, threshold=args.threshold)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()