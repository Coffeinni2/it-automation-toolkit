#!/usr/bin/env python3
"""
Log Analyzer: count occurrences of keywords in log files with optional time filtering.

Supports log lines in format:
  [2025-11-22T10:30:45] ERROR: Message here

Usage:
  python3 log_analyzer.py app.log ERROR
  python3 log_analyzer.py app.log WARNING --hours 24
"""

import argparse
import re
from datetime import datetime, timedelta
import sys
import os

def parse_timestamp(line):
    """
    Extract datetime from log line like '[2025-11-22T10:30:45] ...'.
    Returns datetime object or None if not found or invalid.
    """
    match = re.search(r'\[(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\]', line)
    if match:
        try:
            return datetime.strptime(match.group(1), "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return None
    return None

def count_matches(filename, keyword, hours=None):
    """
    Count lines containing 'keyword' in file.
    If 'hours' is given, filter by timestamp (last N hours).
    """
    count = 0
    if hours is not None:
        cutoff_time = datetime.now() - timedelta(hours=hours)
    else:
        cutoff_time = None

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if keyword in line:
                if cutoff_time is None:
                    count += 1
                else:
                    log_time = parse_timestamp(line)
                    if log_time and log_time >= cutoff_time:
                        count += 1
    return count

def main():
    parser = argparse.ArgumentParser(description="Analyze log files for keywords with optional time filtering.")
    parser.add_argument("logfile", help="Path to the log file")
    parser.add_argument("keyword", help="Keyword to search for (e.g., ERROR, WARNING)")
    parser.add_argument("--hours", type=int, help="Only analyze entries from the last N hours")
    args = parser.parse_args()

    if not os.path.exists(args.logfile):
        print(f"Error: File '{args.logfile}' not found.")
        sys.exit(1)

    try:
        count = count_matches(args.logfile, args.keyword, args.hours)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    print(f"Log Analysis: {args.logfile}")
    print(f"  Keyword: {args.keyword}")
    if args.hours is not None:
        print(f"  Time window: last {args.hours} hours")
    else:
        print("  Time window: all entries")
    print(f"  Matches found: {count}")
    print("Analysis complete.")

if __name__ == "__main__":
    main()