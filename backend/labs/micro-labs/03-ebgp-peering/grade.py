#!/usr/bin/env python3
"""
NetCert Pro — Auto-Grading Script
Micro-Lab 03: EBGP Peering

Verifies EBGP sessions are Established, routes propagate
across AS boundaries with correct AS-path, and end-to-end ping works.
"""

import argparse
import json
import re
import sys
from typing import Dict, List, Tuple

try:
    from scrapli.driver.core import JunosSCRAPLIDriver
except ImportError:
    import paramiko
    import time

    class JunosSCRAPLIDriver:
        """JunOS SSH driver using paramiko invoke_shell() for persistent sessions."""
        def __init__(self, host, auth_username, auth_password, port=22):
            self.host = host; self.port = port
            self.auth_username = auth_username; self.auth_password = auth_password
            self.client = None; self.shell = None
        def open(self):
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.host, port=self.port, username=self.auth_username,
                                password=self.auth_password, look_for_keys=False, allow_agent=False, timeout=30)
            self.shell = self.client.invoke_shell(term='vt100', width=200, height=50)
            self.shell.settimeout(15)
            time.sleep(2)
            self._drain()
        def send_command(self, command: str) -> str:
            if not self.shell: return "ERROR: Shell not initialized"
            try:
                self.shell.send(command + "\n")
                time.sleep(1.5)
                return self._drain() or "(no output)"
            except Exception as e: return f"ERROR: {e}"
        def _drain(self):
            output = b""; time.sleep(0.5)
            try:
                while self.shell.recv_ready():
                    d = self.shell.recv(65536)
                    if d: output += d
                    else: break
            except: pass
            return output.decode('utf-8', errors='replace')
        def close(self):
            if self.shell: self.shell.close()
            if self.client: self.client.close()


MAX_SCORE = 100
TASKS = {
    "bgp_established": {"max": 25, "description": "All BGP sessions Established"},
    "loopback_routes": {"max": 25, "description": "All loopback routes in BGP table"},
    "as_path_correct": {"max": 25, "description": "AS-path shows correct AS hops"},
    "ping_across_as": {"max": 25, "description": "Ping across AS boundaries"},
}


def cmd(dev, c):
    return dev.send_command(c + " | no-more")


def count_established(device) -> Tuple[int, int]:
    """Returns (established, total_expected)."""
    output = cmd(device, "show bgp summary")
    established = len(re.findall(r'Establ', output))
    total = len(re.findall(r'\d+\.\d+\.\d+\.\d+\s+\d+\s+\d+', output))
    return established, total


def check_bgp_route(device, prefix: str) -> bool:
    """Check if a prefix exists in BGP table."""
    output = cmd(device, f"show route {prefix} protocol bgp")
    return prefix in output


def get_as_path(device, prefix: str) -> str:
    """Extract AS-path for a given prefix."""
    output = cmd(device, f"show route {prefix} protocol bgp")
    match = re.search(r'\[(\d+(?:\s+\d+)*)\]', output)
    return match.group(1) if match else ""


def check_ping(device, target: str) -> bool:
    output = cmd(device, f"ping {target} count 3 rapid")
    loss = re.search(r'(\d+)%', output)
    return loss is None or int(loss.group(1)) == 0


def grade_lab(devices: Dict[str, str], username="admin", password="NetCert123", port=22) -> Dict:
    results = {
        "lab": "03-ebgp-peering",
        "title": "EBGP Peering",
        "level": "JNCIS/JNCIP",
        "max_score": MAX_SCORE, "total_score": 0, "tasks": {}, "passed": False,
    }

    conns = {}
    try:
        for name, ip in devices.items():
            d = JunosSCRAPLIDriver(host=ip, port=port, auth_username=username, auth_password=password)
            d.open(); conns[name] = d

        # Task 1: BGP sessions Established
        r1_est, r1_total = count_established(conns["r1"])
        r2_est, _ = count_established(conns["r2"])
        r3_est, _ = count_established(conns["r3"])
        all_est = r1_est >= 1 and r2_est >= 2 and r3_est >= 1
        results["tasks"]["bgp_established"] = {
            "score": TASKS["bgp_established"]["max"] if all_est else 0,
            "max_score": TASKS["bgp_established"]["max"],
            "passed": all_est,
            "detail": f"Established sessions: R1={r1_est}, R2={r2_est}, R3={r3_est}",
        }

        # Task 2: All loopback routes in BGP table
        r1_routes = check_bgp_route(conns["r1"], "3.3.3.3") and check_bgp_route(conns["r1"], "2.2.2.2")
        r3_routes = check_bgp_route(conns["r3"], "1.1.1.1") and check_bgp_route(conns["r3"], "2.2.2.2")
        routes_ok = r1_routes and r3_routes
        results["tasks"]["loopback_routes"] = {
            "score": TASKS["loopback_routes"]["max"] if routes_ok else 0,
            "max_score": TASKS["loopback_routes"]["max"],
            "passed": routes_ok,
            "detail": f"R→R3 route: {'OK' if r1_routes else 'FAIL'}, R3→R1 route: {'OK' if r3_routes else 'FAIL'}",
        }

        # Task 3: AS-path correct
        path_r1_to_r3 = get_as_path(conns["r1"], "3.3.3.3")
        path_r3_to_r1 = get_as_path(conns["r3"], "1.1.1.1")
        as_ok = "65002" in path_r1_to_r3 and "65002" in path_r3_to_r1
        results["tasks"]["as_path_correct"] = {
            "score": TASKS["as_path_correct"]["max"] if as_ok else 0,
            "max_score": TASKS["as_path_correct"]["max"],
            "passed": as_ok,
            "detail": f"AS-path R1→3.3.3.3: [{path_r1_to_r3}], R3→1.1.1.1: [{path_r3_to_r1}]",
        }

        # Task 4: Ping across AS
        ping_ok = check_ping(conns["r1"], "3.3.3.3") and check_ping(conns["r3"], "1.1.1.1")
        results["tasks"]["ping_across_as"] = {
            "score": TASKS["ping_across_as"]["max"] if ping_ok else 0,
            "max_score": TASKS["ping_across_as"]["max"],
            "passed": ping_ok,
            "detail": f"Ping R1→3.3.3.3: {'OK' if check_ping(conns['r1'], '3.3.3.3') else 'FAIL'} | R3→1.1.1.1: {'OK' if check_ping(conns['r3'], '1.1.1.1') else 'FAIL'}",
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
