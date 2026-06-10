#!/usr/bin/env python3
"""
NetCert Pro — Auto-Grading Script
Micro-Lab 01: JunOS CLI Basics

This script connects to the lab devices via SSH and verifies
that the student has completed all tasks correctly.

Usage:
    python3 grade.py --r1-ip 172.100.1.2 --r2-ip 172.100.1.3

Returns JSON with task-by-task scoring.
"""

import argparse
import json
import re
import sys
from typing import Dict, List, Optional, Tuple


try:
    from scrapli.driver.core import JunosSCRAPLIDriver
except ImportError:
    import paramiko
    import time

    class JunosSCRAPLIDriver:
        """JunOS SSH driver using paramiko invoke_shell() for persistent sessions."""

        def __init__(self, host: str, auth_username: str, auth_password: str, port: int = 22):
            self.host = host
            self.port = port
            self.auth_username = auth_username
            self.auth_password = auth_password
            self.client = None
            self.shell = None

        def open(self):
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                self.host,
                port=self.port,
                username=self.auth_username,
                password=self.auth_password,
                look_for_keys=False,
                allow_agent=False,
                timeout=30
            )
            # Use invoke_shell for persistent session (supports configure mode)
            self.shell = self.client.invoke_shell(term='vt100', width=200, height=50)
            self.shell.settimeout(15)
            time.sleep(2)
            self._drain()

        def send_command(self, command: str) -> str:
            if not self.shell:
                return "ERROR: Shell not initialized"
            try:
                self.shell.send(command + "\n")
                time.sleep(1.5)
                output = self._drain()
                return output if output else "(no output)"
            except Exception as e:
                return f"ERROR: {e}"

        def _drain(self) -> str:
            """Read all available data from the shell."""
            output = b""
            time.sleep(0.5)
            try:
                while self.shell.recv_ready():
                    data = self.shell.recv(65536)
                    if data:
                        output += data
                    else:
                        break
            except:
                pass
            return output.decode('utf-8', errors='replace')

        def close(self):
            if self.shell:
                self.shell.close()
            if self.client:
                self.client.close()


# Scoring configuration
MAX_SCORE = 100
TASKS = {
    "task1_explore": {"max": 15, "description": "Explore operational mode"},
    "task2_description": {"max": 20, "description": "Configure interface description"},
    "task3_hostname": {"max": 20, "description": "Change hostname on R2"},
    "task4_ping": {"max": 25, "description": "Verify connectivity via ping"},
    "task5_save": {"max": 20, "description": "Save configuration to file"},
}


def run_show_command(device, command: str) -> str:
    """Execute a show command and return the output."""
    result = device.send_command(command)
    return result


def check_interfaces_terse(device, expected_interfaces: List[str]) -> Tuple[bool, str]:
    """Check that expected interfaces are up."""
    output = run_show_command(device, "show interfaces terse | no-more")
    up_interfaces = []
    for line in output.split("\n"):
        for iface in expected_interfaces:
            if iface in line and "up" in line:
                up_interfaces.append(iface)

    all_up = all(iface in up_interfaces for iface in expected_interfaces)
    return all_up, f"Interfaces up: {up_interfaces} / expected: {expected_interfaces}"


def check_interface_description(device, interface: str, expected_text: Optional[str] = None) -> Tuple[bool, str]:
    """Check if description is set on an interface."""
    output = run_show_command(device, "show interfaces description | no-more")
    has_desc = interface in output
    detail = f"Description on {interface}: {'found' if has_desc else 'not found'}"
    return has_desc, detail


def check_hostname(device, expected_hostname: str) -> Tuple[bool, str]:
    """Check if hostname was changed."""
    output = run_show_command(device, "show configuration system host-name | no-more")
    current_hostname = output.strip().strip('"')
    match = current_hostname == expected_hostname
    return match, f"Hostname: {current_hostname} (expected: {expected_hostname})"


def check_ping(device, target_ip: str, count: int = 5) -> Tuple[bool, str]:
    """Check ping success rate."""
    output = run_show_command(device, f"ping {target_ip} count {count} rapid | no-more")
    success_match = re.search(r'(\d+)\s+packets received', output)
    loss_match = re.search(r'(\d+)%\s+packet loss', output)

    received = int(success_match.group(1)) if success_match else 0
    loss = int(loss_match.group(1)) if loss_match else 100

    success = loss == 0 and received == count
    return success, f"Ping {target_ip}: {received}/{count} received, {loss}% loss"


def check_file_saved(device, filename: str) -> Tuple[bool, str]:
    """Check if configuration file was saved."""
    output = run_show_command(device, f"file show {filename} | no-more")
    file_exists = len(output.strip()) > 50 and "error" not in output.lower()
    return file_exists, f"File {filename}: {'saved' if file_exists else 'not found or empty'}"


def grade_lab(r1_ip: str, r2_ip: str, username: str = "admin",
              password: str = "NetCert123", port: int = 22) -> Dict:
    """Grade the micro-lab and return results."""
    results = {
        "lab": "01-junos-cli-basics",
        "title": "JunOS CLI Basics",
        "level": "JNCIA",
        "max_score": MAX_SCORE,
        "total_score": 0,
        "tasks": {},
        "passed": False,
    }

    # Connect to devices
    r1 = JunosSCRAPLIDriver(
        host=r1_ip, port=port,
        auth_username=username, auth_password=password
    )
    r2 = JunosSCRAPLIDriver(
        host=r2_ip, port=port,
        auth_username=username, auth_password=password
    )

    try:
        r1.open()
        r2.open()

        # Task 1: Explore operational mode — check interfaces are up
        interfaces_ok, detail = check_interfaces_terse(r1, ["ge-0/0/0", "lo0"])
        results["tasks"]["task1_explore"] = {
            "score": TASKS["task1_explore"]["max"] if interfaces_ok else 0,
            "max_score": TASKS["task1_explore"]["max"],
            "passed": interfaces_ok,
            "detail": detail,
        }

        # Task 2: Interface description on R1
        desc_ok, detail = check_interface_description(r1, "ge-0/0/0")
        results["tasks"]["task2_description"] = {
            "score": TASKS["task2_description"]["max"] if desc_ok else 0,
            "max_score": TASKS["task2_description"]["max"],
            "passed": desc_ok,
            "detail": detail,
        }

        # Task 3: Hostname change on R2
        hostname_ok, detail = check_hostname(r2, "R2-Core-1")
        results["tasks"]["task3_hostname"] = {
            "score": TASKS["task3_hostname"]["max"] if hostname_ok else 0,
            "max_score": TASKS["task3_hostname"]["max"],
            "passed": hostname_ok,
            "detail": detail,
        }

        # Task 4: Ping from R1 to R2
        ping_ok, detail = check_ping(r1, "10.0.12.2")
        results["tasks"]["task4_ping"] = {
            "score": TASKS["task4_ping"]["max"] if ping_ok else 0,
            "max_score": TASKS["task4_ping"]["max"],
            "passed": ping_ok,
            "detail": detail,
        }

        # Task 5: Save configuration
        save_ok, detail = check_file_saved(r1, "/tmp/my-config.txt")
        results["tasks"]["task5_save"] = {
            "score": TASKS["task5_save"]["max"] if save_ok else 0,
            "max_score": TASKS["task5_save"]["max"],
            "passed": save_ok,
            "detail": detail,
        }

    finally:
        r1.close()
        r2.close()

    # Sum total score
    results["total_score"] = sum(
        t["score"] for t in results["tasks"].values()
    )
    results["passed"] = results["total_score"] >= (MAX_SCORE * 0.7)  # 70% threshold

    return results


def main():
    parser = argparse.ArgumentParser(description="NetCert — Micro-Lab 01 Grading")
    parser.add_argument("--r1-ip", required=True, help="R1 management IP address")
    parser.add_argument("--r2-ip", required=True, help="R2 management IP address")
    parser.add_argument("--username", default="admin", help="SSH username")
    parser.add_argument("--password", default="NetCert123", help="SSH password")
    parser.add_argument("--port", type=int, default=22, help="SSH port")
    parser.add_argument("--output", choices=["json", "human"], default="human",
                        help="Output format")

    args = parser.parse_args()
    results = grade_lab(args.r1_ip, args.r2_ip, args.username, args.password, args.port)

    if args.output == "json":
        print(json.dumps(results, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"  Lab: {results['title']} ({results['lab']})")
        print(f"  Level: {results['level']}")
        print(f"{'='*60}")
        print(f"\n  Total Score: {results['total_score']}/{results['max_score']}")
        print(f"  Status: {'✅ PASSED' if results['passed'] else '❌ FAILED'}")
        print(f"\n  {'─'*60}")
        for task_id, task_data in results["tasks"].items():
            status = "✅" if task_data["passed"] else "❌"
            print(f"  {status} {task_id}: {task_data['score']}/{task_data['max_score']}")
            print(f"    {task_data['detail']}")
        print(f"  {'─'*60}")

    sys.exit(0 if results["passed"] else 1)


if __name__ == "__main__":
    main()
