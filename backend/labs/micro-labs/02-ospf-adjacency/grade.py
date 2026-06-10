#!/usr/bin/env python3
"""
NetCert Pro — Auto-Grading Script
Micro-Lab 02: OSPF Adjacency

Verifies OSPF neighbor states, routes, DR/BDR election, and connectivity.
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

        def __init__(self, host, auth_username, auth_password, port=22):
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
                self.host, port=self.port,
                username=self.auth_username, password=self.auth_password,
                look_for_keys=False, allow_agent=False, timeout=30
            )
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
                return self._drain() or "(no output)"
            except Exception as e:
                return f"ERROR: {e}"

        def _drain(self) -> str:
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


MAX_SCORE = 100
TASKS = {
    "ospf_neighbors_full": {"max": 25, "description": "All OSPF neighbors in Full state"},
    "ospf_routes": {"max": 25, "description": "OSPF routes for all loopbacks visible"},
    "dr_bdr_elected": {"max": 20, "description": "DR and BDR elected on broadcast segment"},
    "ping_all_loopbacks": {"max": 20, "description": "Ping all loopbacks successful"},
    "ospf_interfaces_up": {"max": 10, "description": "All OSPF interfaces active"},
}


def send_cmd(device, cmd: str) -> str:
    return device.send_command(cmd + " | no-more")


def count_ospf_neighbors_full(device) -> Tuple[int, List[str]]:
    """Count OSPF neighbors in Full state."""
    output = send_cmd(device, "show ospf neighbor")
    full_neighbors = []
    for line in output.split("\n"):
        if "Full" in line:
            full_neighbors.append(line.strip())
    return len(full_neighbors), full_neighbors


def check_ospf_routes(device, expected_prefixes: List[str]) -> Tuple[bool, str]:
    """Check that OSPF routes exist for expected prefixes."""
    output = send_cmd(device, "show route protocol ospf")
    found = []
    missing = []
    for prefix in expected_prefixes:
        if prefix in output:
            found.append(prefix)
        else:
            missing.append(prefix)
    return len(missing) == 0, f"Found: {found}, Missing: {missing}"


def check_dr_bdr(device) -> Tuple[bool, str]:
    """Check that DR and BDR are elected."""
    output = send_cmd(device, "show ospf neighbor detail")
    has_dr = "DR" in output and "BDR" in output
    dr_addr = re.search(r'DR\s+(\d+\.\d+\.\d+\.\d+)', output)
    bdr_addr = re.search(r'BDR\s+(\d+\.\d+\.\d+\.\d+)', output)
    detail = f"DR: {dr_addr.group(1) if dr_addr else 'N/A'}, BDR: {bdr_addr.group(1) if bdr_addr else 'N/A'}"
    return has_dr, detail


def check_ping(device, target_ip: str) -> Tuple[bool, str]:
    output = send_cmd(device, f"ping {target_ip} count 3 rapid")
    loss_match = re.search(r'(\d+)%\s+packet loss', output)
    loss = int(loss_match.group(1)) if loss_match else 100
    return loss == 0, f"Ping {target_ip}: {100-loss}% success"


def check_ospf_interfaces(device, expected_count: int) -> Tuple[bool, str]:
    output = send_cmd(device, "show ospf interface")
    active = 0
    for line in output.split("\n"):
        if "up" in line.lower() and ("ge-" in line or "lo0" in line):
            active += 1
    return active >= expected_count, f"Active OSPF interfaces: {active}/{expected_count}"


def grade_lab(devices: Dict[str, str], username: str = "admin",
              password: str = "NetCert123", port: int = 22) -> Dict:
    results = {
        "lab": "02-ospf-adjacency",
        "title": "OSPF Adjacency",
        "level": "JNCIA/JNCIS",
        "max_score": MAX_SCORE,
        "total_score": 0,
        "tasks": {},
        "passed": False,
    }

    conns = {}
    try:
        for name, ip in devices.items():
            d = JunosSCRAPLIDriver(host=ip, port=port, auth_username=username, auth_password=password)
            d.open()
            conns[name] = d

        # Task 1: OSPF neighbors in Full state on all routers
        r1_full, r1_neighbors = count_ospf_neighbors_full(conns["r1"])
        r2_full, _ = count_ospf_neighbors_full(conns["r2"])
        r3_full, _ = count_ospf_neighbors_full(conns["r3"])
        all_full = r1_full >= 2 and r2_full >= 2 and r3_full >= 2
        results["tasks"]["ospf_neighbors_full"] = {
            "score": TASKS["ospf_neighbors_full"]["max"] if all_full else max(0, (r1_full + r2_full + r3_full) * 4),
            "max_score": TASKS["ospf_neighbors_full"]["max"],
            "passed": all_full,
            "detail": f"Full neighbors: R1={r1_full}, R2={r2_full}, R3={r3_full}",
        }

        # Task 2: OSPF routes visible on R1
        routes_ok, detail = check_ospf_routes(conns["r1"], ["2.2.2.2", "3.3.3.3"])
        results["tasks"]["ospf_routes"] = {
            "score": TASKS["ospf_routes"]["max"] if routes_ok else 0,
            "max_score": TASKS["ospf_routes"]["max"],
            "passed": routes_ok,
            "detail": detail,
        }

        # Task 3: DR/BDR elected
        dr_ok, detail = check_dr_bdr(conns["r1"])
        results["tasks"]["dr_bdr_elected"] = {
            "score": TASKS["dr_bdr_elected"]["max"] if dr_ok else 0,
            "max_score": TASKS["dr_bdr_elected"]["max"],
            "passed": dr_ok,
            "detail": detail,
        }

        # Task 4: Ping all loopbacks
        ping_ok = True
        ping_detail = []
        for target in ["2.2.2.2", "3.3.3.3"]:
            ok, d = check_ping(conns["r1"], target)
            ping_ok = ping_ok and ok
            ping_detail.append(d)
        results["tasks"]["ping_all_loopbacks"] = {
            "score": TASKS["ping_all_loopbacks"]["max"] if ping_ok else 0,
            "max_score": TASKS["ping_all_loopbacks"]["max"],
            "passed": ping_ok,
            "detail": "; ".join(ping_detail),
        }

        # Task 5: OSPF interfaces up
        iface_ok, detail = check_ospf_interfaces(conns["r1"], expected_count=3)
        results["tasks"]["ospf_interfaces_up"] = {
            "score": TASKS["ospf_interfaces_up"]["max"] if iface_ok else 0,
            "max_score": TASKS["ospf_interfaces_up"]["max"],
            "passed": iface_ok,
            "detail": detail,
        }

    finally:
        for d in conns.values():
            d.close()

    results["total_score"] = sum(t["score"] for t in results["tasks"].values())
    results["passed"] = results["total_score"] >= (MAX_SCORE * 0.7)
    return results


def main():
    parser = argparse.ArgumentParser(description="NetCert — Micro-Lab 02 Grading")
    parser.add_argument("--r1-ip", required=True)
    parser.add_argument("--r2-ip", required=True)
    parser.add_argument("--r3-ip", required=True)
    parser.add_argument("--username", default="admin")
    parser.add_argument("--password", default="NetCert123")
    parser.add_argument("--port", type=int, default=22)
    parser.add_argument("--output", choices=["json", "human"], default="human")
    args = parser.parse_args()

    devices = {"r1": args.r1_ip, "r2": args.r2_ip, "r3": args.r3_ip}
    results = grade_lab(devices, args.username, args.password, args.port)

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
