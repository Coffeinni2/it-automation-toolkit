#!/usr/bin/env python3
"""
Network Checker: diagnose basic network connectivity issues.

Checks:
- Local gateway (hardcoded as 192.168.1.1 — adjust if needed)
- DNS resolution (google.com)
- ICMP ping to 8.8.8.8
- HTTP access to https://google.com

Compatible with Python 3.9+ (including macOS system Python).
Clean output, no emojis — suitable for logs and automation.
"""

import subprocess
import socket
import sys
from typing import Optional

import requests

# Configuration — adjust if your network uses a different gateway
GATEWAY = "192.168.1.1"
DNS_HOST = "google.com"
PING_TARGET = "8.8.8.8"
HTTP_URL = "https://google.com"

def ping(host, count=1, timeout=2):
    """
    Ping a host using the system 'ping' command.
    Returns True if host responds, False otherwise.
    """
    try:
        result = subprocess.run(
            ["ping", "-c", str(count), "-W", str(timeout), host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception:
        return False

def resolve_dns(hostname):
    """
    Resolve a hostname to an IP address using DNS.
    Returns IP as string, or None if resolution fails.
    """
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None

def check_http(url):
    """
    Check if a web page is accessible via HTTP(S).
    Returns True if status code is 200, False otherwise.
    """
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def main():
    print("Network Diagnostics")
    issues = 0

    # 1. Gateway check
    print(f"   Checking gateway: {GATEWAY}")
    if ping(GATEWAY):
        print(f"   Gateway ({GATEWAY}): OK")
    else:
        print(f"   Gateway ({GATEWAY}): FAILED")
        issues += 1

    # 2. DNS check
    print(f"   Resolving DNS: {DNS_HOST}")
    ip = resolve_dns(DNS_HOST)
    if ip:
        print(f"   DNS ({DNS_HOST}): Resolved to {ip}")
    else:
        print(f"   DNS ({DNS_HOST}): FAILED")
        issues += 1

    # 3. Ping check
    print(f"   Pinging: {PING_TARGET}")
    if ping(PING_TARGET):
        print(f"   Ping ({PING_TARGET}): OK")
    else:
        print(f"   Ping ({PING_TARGET}): FAILED")
        issues += 1

    # 4. HTTP check
    print(f"   HTTP request: {HTTP_URL}")
    if check_http(HTTP_URL):
        print(f"   HTTP ({HTTP_URL}): Status 200")
    else:
        print(f"   HTTP ({HTTP_URL}): FAILED")
        issues += 1

    # Final summary
    print()
    if issues == 0:
        print("All network checks passed.")
        sys.exit(0)
    else:
        print(f"{issues} network check(s) failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()