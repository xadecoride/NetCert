#!/usr/bin/env python3
"""
NetCert Pro — Auto-Grading Script
Micro-Lab 04: IS-IS Single-Level

Verifies IS-IS adjacencies, hostnames, routes, and connectivity.
"""

import argparse
import json
import re
import sys
import time
from typing import Dict, Tuple

try:
    from scrapli.driver.core import JunosSCRAPLIDriver
except ImportError:
    import paramiko
    class JunosSCRAPLIDriver:
        def __init__(self, host, auth_username, auth_password, port=22):
            self.host = host; self.port = port
            self.auth_username = auth_username; self.auth_password = auth_password
            self.client = None
        def open(self):
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.host, self.port, self.auth_username, self.auth_password,
                                look_for_keys=False, allow_agent=False, timeout=10)
        def send_command(self, c):
            chan = self.client.invoke_shell()
            time.sleep(0.3); chan.send(c + ' | no-more\n'); time.sleep(1.0)
            out = b''
            while chan.recv_ready(): out += chan.recv(65535)
            chan.close()
            return out.decode('utf-8', errors='replace')
        def close(self):
            if self.client: self.client.close()


MAX_SCORE = 100
TASKS = {
    "isis_adjacencies_up": {"max": 25, "description": "All IS-IS adjacencies in Up state"},
    "isis_hostnames": {"max": 20, "description": "IS-IS hostname exchange working"},
    "isis_routes": {"max": 30, "description": "All loopback routes via IS-IS"},
    "ping_connectivity": {"max": 25, "description": "End-to-end ping across IS-IS domain"},
}


def cmd(dev, c):
    return dev.send_command(c)


def count_isis_adjacencies(device) -> Tuple[int, int]:
    """Returns (up, total)."""
    output = cmd(device, "show isis adjacency")
    up = len(re.findall(r'Up', output))
    total = len(re.findall(r'^\S+\s+', output, re.MULTILINE))
    # Filter header line
    total = max(0, total - 1)
    return up, total


def check_isis_hostnames(device, expected_names: list) -> bool:
    output = cmd(device, "show isis hostname")
    return all(name in output for name in expected_names)


def check_isis_route(device, prefix: str) -> bool:
    output = cmd(device, f"show route {prefix} protocol isis")
    return prefix in output


def check_ping(device, target: str) -> bool:
    output = cmd(device, f"ping {target} count 3 rapid")
    loss = re.search(r'(\d+)%', output)
    return loss is None or int(loss.group(1)) == 0


def grade_lab(devices: Dict[str, str], username="admin", password="NetCert123", port=22) -> Dict:
    results = {
        "lab": "04-isis-single-level",
        "title": "IS-IS Single-Level",
        "level": "JNCIS/JNCIP",
        "max_score": MAX_SCORE, "total_score": 0, "tasks": {}, "passed": False,
    }

    conns = {}
    try:
        for name, ip in devices.items():
            d = JunosSCRAPLIDriver(host=ip, port=port, auth_username=username, auth_password=password)
            d.open(); conns[name] = d

        # Task 1: IS-IS adjacencies Up
        r1_up, r1_total = count_isis_adjacencies(conns["r1"])
        r2_up, _ = count_isis_adjacencies(conns["r2"])
        r3_up, _ = count_isis_adjacencies(conns["r3"])
        all_up = r1_up >= 2 and r2_up >= 2 and r3_up >= 2
        results["tasks"]["isis_adjacencies_up"] = {
            "score": TASKS["isis_adjacencies_up"]["max"] if all_up else 0,
            "max_score": TASKS["isis_adjacencies_up"]["max"],
            "passed": all_up,
            "detail": f"Adjacencies Up: R1={r1_up}/{r1_total}, R2={r2_up}, R3={r3_up}",
        }

        # Task 2: IS-IS hostnames
        hostnames_ok = check_isis_hostnames(conns["r1"], ["R2", "R3"])
        results["tasks"]["isis_hostnames"] = {
            "score": TASKS["isis_hostnames"]["max"] if hostnames_ok else 0,
            "max_score": TASKS["isis_hostnames"]["max"],
            "passed": hostnames_ok,
            "detail": f"Hostnames visible from R1: {'OK' if hostnames_ok else 'Missing'}",
        }

        # Task 3: IS-IS routes on R1
        r1_routes = check_isis_route(conns["r1"], "2.2.2.2") and check_isis_route(conns["r1"], "3.3.3.3")
        results["tasks"]["isis_routes"] = {
            "score": TASKS["isis_routes"]["max"] if r1_routes else 0,
            "max_score": TASKS["isis_routes"]["max"],
            "passed": r1_routes,
            "detail": f"IS-IS routes on R1: {'All found' if r1_routes else 'Missing routes'}",
        }

        # Task 4: Ping
        ping_ok = check_ping(conns["r1"], "2.2.2.2") and check_ping(conns["r1"], "3.3.3.3") and check_ping(conns["r3"], "1.1.1.1")
        results["tasks"]["ping_connectivity"] = {
            "score": TASKS["ping_connectivity"]["max"] if ping_ok else 0,
            "max_score": TASKS["ping_connectivity"]["max"],
            "passed": ping_ok,
            "detail": f"Ping R1→2.2.2.2: {'OK' if check_ping(conns['r1'], '2.2.2.2') else 'FAIL'} | R1→3.3.3.3: {'OK' if check_ping(conns['r1'], '3.3.3.3') else 'FAIL'}",
        }

    finally:
        for d in conns.values(): d.close()

    results["total_score"] = sum(t["score"] for t in results["tasks"].values())
    results["passed"] = results["total_score"] >= (MAX_SCORE * 0.7)
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--r1-ip", required=True); parser.add_argument("--r2-ip", required=True)
    parser.add_argument("--r3-ip", required=True); parser.add_argument("--username", default="admin")
    parser.add_argument("--password", default="NetCert123"); parser.add_argument("--port", type=int, default=22)
    parser.add_argument("--output", choices=["json", "human"], default="human")
    args = parser.parse_args()

    devices = {"r1": args.r1_ip, "r2": args.r2_ip, "r3": args.r3_ip}
    results = grade_lab(devices, args.username, args.password, args.port)

    if args.output == "json":
        print(json.dumps(results, indent=2))
    else:
        status = "✅ PASSED" if results["passed"] else "❌ FAILED"
        print(f"\n{'='*60}\n  Lab: {results['title']}\n{'='*60}")
        print(f"  Score: {results['total_score']}/{results['max_score']} — {status}")
        for tid, td in results["tasks"].items():
            s = "✅" if td["passed"] else "❌"
            print(f"  {s} {tid}: {td['score']}/{td['max_score']} — {td['detail']}")

    sys.exit(0 if results["passed"] else 1)


if __name__ == "__main__":
    main()
