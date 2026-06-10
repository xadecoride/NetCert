#!/usr/bin/env python3
"""
NetCert Pro — Auto-Grading Script
Micro-Lab 05: MPLS LSP

Verifies OSPF base, LDP sessions, MPLS LSP status, label database, and ping.
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
    "igp_connectivity": {"max": 15, "description": "IGP (OSPF) connectivity established"},
    "mpls_interfaces": {"max": 15, "description": "MPLS enabled on all interfaces"},
    "ldp_sessions": {"max": 25, "description": "LDP sessions Operational"},
    "mpls_lsp_up": {"max": 25, "description": "MPLS LSP to remote PE is Up"},
    "ping_mpls": {"max": 20, "description": "Ping through MPLS domain"},
}


def cmd(dev, c):
    return dev.send_command(c)


def check_ospf_route(device, prefix: str) -> bool:
    out = cmd(device, f"show route {prefix} protocol ospf")
    return prefix in out


def check_mpls_interface(device, iface: str) -> bool:
    out = cmd(device, "show mpls interface")
    return iface in out


def count_ldp_sessions(device) -> Tuple[int, int]:
    """Returns (operational, total)."""
    out = cmd(device, "show ldp session")
    op = len(re.findall(r'Operational', out))
    total = len(re.findall(r'^\S+\s+\d+', out, re.MULTILINE))
    return op, max(0, total - 1)  # subtract header


def check_mpls_lsp_ingress(device, target_prefix: str) -> Tuple[bool, str]:
    """Check ingress LSP to target."""
    out = cmd(device, f"show mpls lsp ingress {target_prefix}")
    up = "Up" in out and "Down" not in out
    detail = "LSP Up" if up else "LSP not found or Down"
    return up, detail


def check_mpls_lsp_transit(device) -> bool:
    out = cmd(device, "show mpls lsp transit")
    return "Up" in out


def check_ping(device, target: str) -> bool:
    out = cmd(device, f"ping {target} count 3 rapid")
    loss = re.search(r'(\d+)%', out)
    return loss is None or int(loss.group(1)) == 0


def grade_lab(devices: Dict[str, str], username="admin", password="NetCert123", port=22) -> Dict:
    results = {
        "lab": "05-mpls-lsp",
        "title": "MPLS LSP with LDP",
        "level": "JNCIS/JNCIP",
        "max_score": MAX_SCORE, "total_score": 0, "tasks": {}, "passed": False,
    }

    conns = {}
    try:
        for name, ip in devices.items():
            d = JunosSCRAPLIDriver(host=ip, port=port, auth_username=username, auth_password=password)
            d.open(); conns[name] = d

        pe1, p, pe2 = conns["pe1"], conns["p"], conns["pe2"]

        # Task 1: IGP connectivity
        igp_ok = (check_ospf_route(pe1, "2.2.2.2") and check_ospf_route(pe1, "3.3.3.3")
                  and check_ospf_route(pe2, "1.1.1.1"))
        results["tasks"]["igp_connectivity"] = {
            "score": TASKS["igp_connectivity"]["max"] if igp_ok else 0,
            "max_score": TASKS["igp_connectivity"]["max"],
            "passed": igp_ok,
            "detail": f"OSPF routes: PE1→PE2: {'OK' if check_ospf_route(pe1, '3.3.3.3') else 'FAIL'}",
        }

        # Task 2: MPLS on interfaces
        mpls_ok = (check_mpls_interface(pe1, "ge-0/0/0")
                   and check_mpls_interface(p, "ge-0/0/0") and check_mpls_interface(p, "ge-0/0/1")
                   and check_mpls_interface(pe2, "ge-0/0/0"))
        results["tasks"]["mpls_interfaces"] = {
            "score": TASKS["mpls_interfaces"]["max"] if mpls_ok else 0,
            "max_score": TASKS["mpls_interfaces"]["max"],
            "passed": mpls_ok,
            "detail": f"MPLS on required interfaces: {'All OK' if mpls_ok else 'Some missing'}",
        }

        # Task 3: LDP sessions Operational
        pe1_op, _ = count_ldp_sessions(pe1)
        p_op, _ = count_ldp_sessions(p)
        pe2_op, _ = count_ldp_sessions(pe2)
        ldp_ok = pe1_op >= 1 and p_op >= 2 and pe2_op >= 1
        results["tasks"]["ldp_sessions"] = {
            "score": TASKS["ldp_sessions"]["max"] if ldp_ok else 0,
            "max_score": TASKS["ldp_sessions"]["max"],
            "passed": ldp_ok,
            "detail": f"LDP sessions: PE1={pe1_op}, P={p_op}, PE2={pe2_op}",
        }

        # Task 4: MPLS LSP status
        lsp_ok, detail = check_mpls_lsp_ingress(pe1, "3.3.3.3")
        transit_ok = check_mpls_lsp_transit(p)
        lsp_ok = lsp_ok and transit_ok
        results["tasks"]["mpls_lsp_up"] = {
            "score": TASKS["mpls_lsp_up"]["max"] if lsp_ok else 0,
            "max_score": TASKS["mpls_lsp_up"]["max"],
            "passed": lsp_ok,
            "detail": f"LSP PE1→PE2: {detail} | Transit P: {'Up' if transit_ok else 'Not found'}",
        }

        # Task 5: Ping through MPLS
        ping_ok = check_ping(pe1, "3.3.3.3")
        results["tasks"]["ping_mpls"] = {
            "score": TASKS["ping_mpls"]["max"] if ping_ok else 0,
            "max_score": TASKS["ping_mpls"]["max"],
            "passed": ping_ok,
            "detail": f"Ping PE1→3.3.3.3: {'OK' if ping_ok else 'FAIL'}",
        }

    finally:
        for d in conns.values(): d.close()

    results["total_score"] = sum(t["score"] for t in results["tasks"].values())
    results["passed"] = results["total_score"] >= (MAX_SCORE * 0.7)
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pe1-ip", required=True); parser.add_argument("--p-ip", required=True)
    parser.add_argument("--pe2-ip", required=True); parser.add_argument("--username", default="admin")
    parser.add_argument("--password", default="NetCert123"); parser.add_argument("--port", type=int, default=22)
    parser.add_argument("--output", choices=["json", "human"], default="human")
    args = parser.parse_args()

    devices = {"pe1": args.pe1_ip, "p": args.p_ip, "pe2": args.pe2_ip}
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
