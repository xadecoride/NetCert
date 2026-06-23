#!/usr/bin/env python3
"""
NetCert — Juniper topology-based questions for ALL Juniper exams.
Guarantees at least 5 topology questions per exam attempt.
"""
import hashlib
import json
import uuid

EXAMS = {
    # JNCIA
    "jncia-junos": {"exam_id": "b0000000-0000-0000-0000-000000000001", "track_id": "a0000000-0000-0000-0000-000000000001", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-junos.html"},
    "jncia-sp":    {"exam_id": "b0000000-0000-0000-0000-000000000002", "track_id": "a0000000-0000-0000-0000-000000000002", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-junos.html"},
    "jncia-sec":   {"exam_id": "b0000000-0000-0000-0000-000000000022", "track_id": "a0000000-0000-0000-0000-000000000003", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-sec.html"},
    "jncia-dc":    {"exam_id": "b0000000-0000-0000-0000-000000000020", "track_id": "a0000000-0000-0000-0000-000000000004", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-dc.html"},
    "jncia-aut":   {"exam_id": "b0000000-0000-0000-0000-000000000021", "track_id": "a0000000-0000-0000-0000-000000000005", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-automation.html"},
    "jncia-cloud": {"exam_id": "b0000000-0000-0000-0000-000000000030", "track_id": "a0000000-0000-0000-0000-000000000007", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-cloud.html"},
    # JNCIS
    "jncis-ent":   {"exam_id": "b0000000-0000-0000-0000-000000000012", "track_id": "a0000000-0000-0000-0000-000000000001", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-ent.html"},
    "jncis-sp":    {"exam_id": "b0000000-0000-0000-0000-000000000014", "track_id": "a0000000-0000-0000-0000-000000000002", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-sp.html"},
    "jncis-sec":   {"exam_id": "b0000000-0000-0000-0000-000000000025", "track_id": "a0000000-0000-0000-0000-000000000003", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-sec.html"},
    "jncis-dc":    {"exam_id": "b0000000-0000-0000-0000-000000000027", "track_id": "a0000000-0000-0000-0000-000000000004", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-dc.html"},
    "jncis-aut":   {"exam_id": "b0000000-0000-0000-0000-000000000029", "track_id": "a0000000-0000-0000-0000-000000000005", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-automation.html"},
    # JNCIP
    "jncip-ent":   {"exam_id": "b0000000-0000-0000-0000-000000000011", "track_id": "a0000000-0000-0000-0000-000000000001", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-ent.html"},
    "jncip-sp":    {"exam_id": "b0000000-0000-0000-0000-000000000013", "track_id": "a0000000-0000-0000-0000-000000000002", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-sp.html"},
    "jncip-sec":   {"exam_id": "b0000000-0000-0000-0000-000000000024", "track_id": "a0000000-0000-0000-0000-000000000003", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-sec.html"},
    "jncip-dc":    {"exam_id": "b0000000-0000-0000-0000-000000000026", "track_id": "a0000000-0000-0000-0000-000000000004", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-dc.html"},
    "jncip-aut":   {"exam_id": "b0000000-0000-0000-0000-000000000028", "track_id": "a0000000-0000-0000-0000-000000000005", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-automation.html"},
}


def qid(exam: str, seed: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_OID, f"{exam}-topo:{seed}"))


def content_hash(body: str, correct: str) -> str:
    return hashlib.sha256(f"{body}::{correct}".encode()).hexdigest()[:16]


def make_q(exam: str, body: str, options: list[tuple[str, bool]], explanation: str,
           section: str, weight: float, difficulty: int = 3,
           bloom: str = "analyze") -> dict:
    assert sum(1 for _, c in options if c) == 1, f"exactly one correct option required: {body}"
    letters = "ABCDEF"
    opts = []
    for i, (text, correct) in enumerate(options):
        opts.append({"id": letters[i], "text": text, "is_correct": correct})
    correct_letter = next(letters[i] for i, (_, c) in enumerate(options) if c)
    meta = EXAMS[exam]
    return {
        "id": qid(exam, body + correct_letter),
        "exam_id": meta["exam_id"],
        "track_id": meta["track_id"],
        "question_type": "topology",
        "difficulty": difficulty,
        "bloom_level": bloom,
        "body": body,
        "options": opts,
        "explanation": explanation,
        "reference_urls": [meta["url"]],
        "blueprint_section": section,
        "blueprint_weight": weight,
        "content_hash": content_hash(body, correct_letter),
        "is_active": True,
    }


def generate_all() -> list[dict]:
    questions: list[dict] = []

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIA-Junos
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncia-junos",
               "Refer to the topology:\n\n"
               "      [R1] ge-0/0/0 --- ge-0/0/0 [R2]\n"
               "      10.1.12.0/24\n\n"
               "R1's ge-0/0/0 has IP 10.1.12.1/24. R2's ge-0/0/0 has IP 10.1.12.2/24.\n"
               "A ping from R1 to 10.1.12.2 succeeds. Which route appears in R1's routing table?",
               [("10.1.12.0/24 via ge-0/0/0.0", True),
                ("10.1.12.2/32 via ge-0/0/0.0", False),
                ("0.0.0.0/0 via 10.1.12.2", False),
                ("No route; directly connected hosts do not need routes", False)],
               "A directly connected network route is installed for 10.1.12.0/24 when the interface is configured.",
               "Routing Fundamentals", 20.0, 2, "understand"),
        make_q("jncia-junos",
               "Topology:\n\n"
               "   [PC1]---ge-0/0/1 [R1] ge-0/0/2---[PC2]\n"
               "   192.168.1.0/24    192.168.2.0/24\n\n"
               "R1 has no static routes. PC1 can reach R1's ge-0/0/1 but not PC2. What is missing?",
               [("A default route on PC1", False),
                ("A routing protocol on R1", False),
                ("Static routes or default gateways on PCs", True),
                ("A firewall policy", False)],
               "Each subnet is directly connected to R1, but PCs need a default gateway pointing to R1 to reach other subnets.",
               "Routing Fundamentals", 20.0, 3, "troubleshoot"),
        make_q("jncia-junos",
               "Refer to the topology:\n\n"
               "   [R1]---[R2]---[R3]\n"
               "   Area 0   Area 1\n\n"
               "R1 is in Area 0, R2 is an ABR, R3 is in Area 1. R3 advertises 10.3.3.0/24.\n"
               "What LSA type does R1 see for 10.3.3.0/24?",
               [("Type 1", False), ("Type 2", False), ("Type 3", True), ("Type 5", False)],
               "Inter-area routes are advertised as Type 3 Summary LSAs by ABRs.",
               "OSPF", 20.0, 3, "analyze"),
        make_q("jncia-junos",
               "Topology:\n\n"
               "   [R1]---ge-0/0/0   ge-0/0/0---[R2]\n"
               "   10.10.10.1/30      10.10.10.2/30\n\n"
               "Both interfaces are up but OSPF adjacency is stuck at 2-Way. What is the most likely cause?",
               [("MTU mismatch", False),
                ("Network type broadcast with no DR election on point-to-point", True),
                ("Area ID mismatch", False),
                ("Authentication mismatch", False)],
               "On a point-to-point link OSPF should use point-to-point network type to avoid 2-Way state.",
               "OSPF", 20.0, 3, "troubleshoot"),
        make_q("jncia-junos",
               "Refer to the topology:\n\n"
               "   [SW1]---[SW2]---[SW3]\n"
               "   All links are trunk\n\n"
               "SW1 is the root bridge. Which ports on SW2 are in a forwarding state?",
               [("Only the port toward SW1", False),
                ("The port toward SW1 and one port toward SW3", True),
                ("All ports", False),
                ("No ports", False)],
               "Root port faces root; one designated port forwards per segment. The other port is blocked.",
               "Layer 2", 20.0, 3, "analyze"),
        make_q("jncia-junos",
               "Topology:\n\n"
               "   [R1]---[R2]---[R3]\n"
               "   eBGP   iBGP\n\n"
               "R2 is a route reflector. R1 and R3 are clients. R1 advertises a route. How does R3 receive it?",
               [("Directly from R1 via eBGP", False),
                ("Reflected by R2", True),
                ("Via OSPF", False),
                ("It does not receive it", False)],
               "Route reflectors reflect routes between iBGP clients.",
               "BGP", 20.0, 2, "understand"),
        make_q("jncia-junos",
               "Refer to the topology:\n\n"
               "   [Host]---ge-0/0/1 [R1] ge-0/0/2---[Internet]\n\n"
               "A source NAT rule is configured on R1 for the Host subnet. Which address does the Internet see?",
               [("Host private IP", False),
                ("R1 ge-0/0/2 public IP", True),
                ("R1 ge-0/0/1 IP", False),
                ("No address; NAT breaks the connection", False)],
               "Source NAT translates private source addresses to the public address on the egress interface.",
               "NAT", 20.0, 2, "understand"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIA-SP
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncia-sp",
               "Refer to the MPLS topology:\n\n"
               "   CE1--PE1--P--PE2--CE2\n\n"
               "Which device assigns the VPN label for CE2's routes?",
               [("P", False), ("PE1", False), ("PE2", True), ("CE2", False)],
               "The egress PE assigns the VPN label for routes advertised to other PEs via MP-BGP.",
               "MPLS L3VPN", 25.0, 3, "understand"),
        make_q("jncia-sp",
               "Topology:\n\n"
               "   [R1]---[R2]---[R3]\n"
               "   LDP enabled on all links\n\n"
               "Which statement about LDP adjacencies is true?",
               [("LDP sessions are TCP-based between directly connected neighbors", True),
                ("LDP uses UDP only", False),
                ("LDP requires RSVP", False),
                ("LDP labels are only for BGP routes", False)],
               "LDP discovery uses UDP Hellos, but the session is TCP-based between neighbors.",
               "MPLS", 25.0, 2, "understand"),
        make_q("jncia-sp",
               "Refer to the topology:\n\n"
               "   [AS 65001]---[AS 65002]---[AS 65003]\n\n"
               "AS 65002 receives the same prefix from both neighbors. Which attribute influences inbound traffic?",
               [("Local Preference", False), ("MED", True), ("Origin", False), ("Next Hop", False)],
               "MED is advertised to external peers and influences how they send traffic into your AS.",
               "BGP", 25.0, 2, "understand"),
        make_q("jncia-sp",
               "Topology:\n\n"
               "   [R1]---Area 49.0001---[R2]---Area 49.0002---[R3]\n\n"
               "All routers are L1/L2. How does R3 learn R1's L1 routes?",
               [("R2 leaks them into L2", True),
                ("They are flooded natively", False),
                ("Via L1/L2 adjacency only", False),
                ("They are not reachable", False)],
               "L1/L2 routers leak L1 routes into the L2 backbone.",
               "IS-IS", 25.0, 3, "analyze"),
        make_q("jncia-sp",
               "Refer to the RSVP-TE topology:\n\n"
               "   [R1]---[R2]---[R3]---[R4]\n\n"
               "All links are 10 Gbps. An LSP from R1 to R4 requires 5 Gbps. What does CSPF do?",
               [("Chooses the path with lowest IGP metric", False),
                ("Chooses any path that satisfies bandwidth", True),
                ("Ignores bandwidth", False),
                ("Rejects the LSP", False)],
               "CSPF selects a path that satisfies constraints such as bandwidth.",
               "MPLS TE", 25.0, 2, "understand"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIA-SEC
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncia-sec",
               "Refer to the SRX topology:\n\n"
               "   [Untrust]---[SRX]---[Trust]---[Server]\n"
               "                |\n"
               "             [DMZ]---[Web]\n\n"
               "A security policy allows HTTP from Untrust to DMZ. Which zone is the source?",
               [("Trust", False), ("DMZ", False), ("Untrust", True), ("Server", False)],
               "The source zone in a security policy is where the traffic originates.",
               "Zones", 25.0, 1, "understand"),
        make_q("jncia-sec",
               "Topology:\n\n"
               "   [Host-A]---[SRX]---[Host-B]\n"
               "   10.1.1.0/24      203.0.113.0/24\n\n"
               "Host-A initiates a session to Host-B. Which NAT type translates Host-A's source address?",
               [("Static NAT", False), ("Destination NAT", False), ("Source NAT", True), ("Proxy ARP", False)],
               "Source NAT translates the source IP address of outgoing traffic.",
               "NAT", 25.0, 2, "understand"),
        make_q("jncia-sec",
               "Refer to the topology:\n\n"
               "   [Internet]---[SRX-1]====[SRX-2]---[Trust]\n"
               "                    Control Link   Data Link\n\n"
               "What is the purpose of the data link in a chassis cluster?",
               [("State synchronization", False),
                ("Forwarding traffic between nodes", True),
                ("Configuration management", False),
                ("Out-of-band management", False)],
               "The data/fabric link carries forwarded traffic between chassis cluster nodes.",
               "High Availability", 25.0, 2, "understand"),
        make_q("jncia-sec",
               "Topology:\n\n"
               "   [User]---[SRX]---[Web]\n\n"
               "A Screen option blocks a host that opens many TCP connections to many destination ports. Which option is it?",
               [("SYN flood", False), ("Port scan", True), ("IP spoofing", False), ("Session limit", False)],
               "The port scan Screen option detects hosts scanning many destination ports.",
               "Screens", 25.0, 2, "understand"),
        make_q("jncia-sec",
               "Refer to the topology:\n\n"
               "   [Branch]---VPN---[HQ]\n"
               "   10.1.0.0/16     10.2.0.0/16\n\n"
               "A route-based IPsec VPN is configured. What must exist for traffic to flow?",
               [("Proxy-ID matching all traffic", False),
                ("Routes pointing to the VPN tunnel interface", True),
                ("A security policy from Branch to Branch", False),
                ("NAT on both sides", False)],
               "Route-based VPNs require routes to direct traffic into the tunnel interface.",
               "VPN", 25.0, 3, "understand"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIA-DC
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncia-dc",
               "Refer to the EVPN-VXLAN topology:\n\n"
               "   [Leaf1]====[Spine]====[Leaf2]\n"
               "   VTEP       VTEP?       VTEP\n\n"
               "Which device is typically NOT a VTEP in a two-tier EVPN-VXLAN fabric?",
               [("Leaf switch", False), ("Spine switch", True), ("Border leaf", False), ("Hypervisor", False)],
               "Spine switches provide IP underlay; leaf switches act as VTEPs.",
               "VXLAN", 25.0, 2, "understand"),
        make_q("jncia-dc",
               "Topology:\n\n"
               "   [Server1]---[Leaf1]====[Leaf2]---[Server2]\n"
               "   VNI 10001             VNI 10001\n\n"
               "What identifies the Layer 2 segment that Server1 and Server2 share?",
               [("VLAN ID", False), ("VNI", True), ("Route Distinguisher", False), ("Loopback IP", False)],
               "VXLAN Network Identifier (VNI) identifies the Layer 2 overlay segment.",
               "VXLAN", 25.0, 2, "understand"),
        make_q("jncia-dc",
               "Refer to the topology:\n\n"
               "   [Server]---[Leaf1]====[Leaf2]---[Server]\n"
               "            ES-1         ES-1\n\n"
               "Both leaf switches are connected to the same server. What provides active-active multihoming?",
               [("MC-LAG", False), ("EVPN multihoming", True), ("VRRP", False), ("LACP", False)],
               "EVPN multihoming via Ethernet Segments provides active-active L2 multihoming.",
               "EVPN", 25.0, 3, "understand"),
        make_q("jncia-dc",
               "Topology:\n\n"
               "   [SW1]====[SW2]====[SW3]\n"
               "   Member   Member   Member\n\n"
               "What technology combines these switches into one logical control plane?",
               [("MC-LAG", False), ("Virtual Chassis", True), ("EVPN", False), ("VCF", False)],
               "Virtual Chassis combines multiple switches into a single logical device.",
               "Virtual Chassis", 25.0, 2, "understand"),
        make_q("jncia-dc",
               "Refer to the topology:\n\n"
               "   [Compute]---[vRouter]---[Underlay]---[vRouter]---[Compute]\n\n"
               "Which Contrail component runs on the compute node?",
               [("Config node", False), ("vRouter", True), ("Control node", False), ("Analytics node", False)],
               "Contrail vRouter runs on compute nodes and forwards tenant traffic.",
               "Contrail", 25.0, 2, "understand"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIA-AUT
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncia-aut",
               "Refer to the automation topology:\n\n"
               "   [Ansible]---NETCONF/SSH---[Junos]\n\n"
               "Which Ansible module is used to push configuration to Junos?",
               [("ios_config", False), ("junos_config", True), ("netconf_rpc", False), ("template", False)],
               "The junos_config module manages Junos configurations via NETCONF.",
               "Ansible", 25.0, 1, "remember"),
        make_q("jncia-aut",
               "Topology:\n\n"
               "   [Python]---NETCONF-830---[Junos]\n\n"
               "Which Python library is commonly used for this connection?",
               [("Paramiko", False), ("ncclient", True), ("Requests", False), ("Scapy", False)],
               "ncclient is the standard Python NETCONF client library.",
               "NETCONF", 25.0, 1, "remember"),
        make_q("jncia-aut",
               "Refer to the topology:\n\n"
               "   [Salt Master]---[Proxy Minion]---[Junos]\n\n"
               "Why is a proxy minion used?",
               [("Junos cannot run a native minion", True),
                ("It replaces the master", False),
                ("It is faster than a regular minion", False),
                ("Junos does not support Salt", False)],
               "Junos devices use Salt proxy minions because they cannot run a native minion.",
               "SaltStack", 25.0, 2, "understand"),
        make_q("jncia-aut",
               "Topology:\n\n"
               "   [Client]---HTTP---[Junos REST API]\n\n"
               "Which HTTP method replaces a complete resource?",
               [("POST", False), ("PUT", True), ("PATCH", False), ("GET", False)],
               "PUT replaces the entire resource, while PATCH applies partial updates.",
               "REST API", 25.0, 2, "understand"),
        make_q("jncia-aut",
               "Refer to the topology:\n\n"
               "   [Junos]--->[SYSLOG]--->[ collector ]\n\n"
               "Which on-box script type can parse syslog events and take action?",
               [("Op script", False), ("Event script", True), ("Commit script", False), ("SNMP script", False)],
               "Event scripts are triggered by syslog events and can take corrective actions.",
               "Junos Automation", 25.0, 2, "understand"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIA-Cloud
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncia-cloud",
               "Refer to the cloud topology:\n\n"
               "   [VPC-A]---[Contrail]---[VPC-B]\n\n"
               "Which protocol provides the overlay between VPCs?",
               [("MPLS", False), ("VXLAN", True), ("L2TP", False), ("PPPoE", False)],
               "VXLAN is commonly used as the overlay encapsulation in cloud fabrics.",
               "Overlay Networking", 25.0, 2, "understand"),
        make_q("jncia-cloud",
               "Topology:\n\n"
               "   [Tenant-A]---[vRouter]---[Underlay]---[vRouter]---[Tenant-B]\n\n"
               "Which component routes tenant traffic on the compute node?",
               [("Config node", False), ("vRouter", True), ("Control node", False), ("Analytics node", False)],
               "Contrail vRouter runs on compute nodes and forwards tenant traffic.",
               "Contrail", 25.0, 2, "understand"),
        make_q("jncia-cloud",
               "Refer to the topology:\n\n"
               "   [On-prem DC]---WAN---[Public Cloud IaaS]\n"
               "   10.0.0.0/16          172.16.0.0/16\n\n"
               "What is required for VMs in both locations to communicate privately?",
               [("NAT overload", False),
                ("IPsec/SD-WAN VPN", True),
                ("Public IP on every VM", False),
                ("Direct physical connection", False)],
               "A VPN or SD-WAN overlay connects private addresses across public networks.",
               "Cloud Connectivity", 25.0, 2, "understand"),
        make_q("jncia-cloud",
               "Topology:\n\n"
               "   [Users]---[SaaS App]---[Provider Data Center]\n\n"
               "Which cloud service model is shown?",
               [("IaaS", False), ("PaaS", False), ("SaaS", True), ("DaaS", False)],
               "SaaS delivers complete applications to end users.",
               "Cloud Service Models", 25.0, 1, "understand"),
        make_q("jncia-cloud",
               "Refer to the topology:\n\n"
               "   [Bare-metal]---[Hypervisor]---[VMs]---[Containers]\n\n"
               "What does NFV enable in this stack?",
               [("Virtualized network functions such as routers and firewalls", True),
                ("Physical cabling automation", False),
                ("Replacement of hypervisors", False),
                ("Bare-metal OS installation", False)],
               "NFV virtualizes network functions that traditionally ran on dedicated hardware.",
               "NFV", 25.0, 2, "understand"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIS-ENT
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncis-ent",
               "Refer to the BGP topology:\n\n"
               "   AS 65001 --- eBGP --- AS 65002 --- eBGP --- AS 65003\n\n"
               "AS 65002 receives a route from AS 65001 with Local Preference 200 and MED 50.\n"
               "The same route is received from AS 65003 with Local Preference 100 and MED 10.\n"
               "Which path does AS 65002 prefer?",
               [("Path through AS 65001", True),
                ("Path through AS 65003", False),
                ("Load-balance", False),
                ("Cannot decide", False)],
               "Local Preference is evaluated before MED. Higher LP wins.",
               "BGP", 20.0, 3, "analyze"),
        make_q("jncis-ent",
               "Topology:\n\n"
               "   [SW1]---[SW2]---[SW3] (triangle)\n\n"
               "Bridge IDs: SW1=4096.00:00:00:00:00:01, SW2=32768...02, SW3=32768...03.\n"
               "Which switch is root?",
               [("SW1", True), ("SW2", False), ("SW3", False), ("Cannot determine", False)],
               "Lowest bridge ID wins root election.",
               "Layer 2", 20.0, 2, "understand"),
        make_q("jncis-ent",
               "Refer to the CoS topology:\n\n"
               "   [Voice]---[EF Queue]---[Router]---[Best-Effort Queue]---[Data]\n\n"
               "Which scheduler treats the EF queue first?",
               [("Strict-high priority", True), ("WRR", False), ("RED", False), ("Tail drop", False)],
               "Strict-high priority queues are serviced before other queues.",
               "CoS", 15.0, 2, "understand"),
        make_q("jncis-ent",
               "Topology:\n\n"
               "   [R1]---Area 0---[R2]---Area 1---[R3]\n\n"
               "R1 advertises 10.1.1.0/24. What LSA type does R3 see?",
               [("Type 1", False), ("Type 2", False), ("Type 3", True), ("Type 5", False)],
               "Inter-area routes are Type 3 Summary LSAs.",
               "OSPF", 20.0, 3, "analyze"),
        make_q("jncis-ent",
               "Refer to the EVPN-VXLAN campus topology:\n\n"
               "   [Leaf1]====[Spine1]====[Leaf2]\n"
               "   VTEP                  VTEP\n\n"
               "Which device role typically is NOT a VTEP?",
               [("Access leaf", False), ("Spine", True), ("WAN edge", False), ("Core", False)],
               "Spine provides IP underlay only; leaves are VTEPs.",
               "EVPN/VXLAN", 20.0, 3, "understand"),
        make_q("jncis-ent",
               "Topology:\n\n"
               "   [PE1]---[P]---[PE2]\n"
               "   VPN-A     VPN-A\n\n"
               "Which protocol carries VPNv4 routes between PE1 and PE2?",
               [("OSPF", False), ("LDP", False), ("MP-BGP", True), ("RSVP", False)],
               "MP-BGP with VPNv4 address family exchanges customer routes between PEs.",
               "BGP/MPLS", 15.0, 3, "understand"),
        make_q("jncis-ent",
               "Refer to the multicast topology:\n\n"
               "   [Source]---[R1]---[R2]---[Receiver]\n"
               "              RP\n\n"
               "Which tree is initially built from source to RP in PIM-SM?",
               [("Shared tree (*,G)", False),
                ("Shortest-path tree (S,G)", True),
                ("Bidirectional tree", False),
                ("None", False)],
               "Source registers with RP and an SPT (S,G) is built from source to RP.",
               "Multicast", 10.0, 3, "understand"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIS-SP
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncis-sp",
               "Refer to the MPLS L3VPN topology:\n\n"
               "   CE1--PE1--P--PE2--CE2\n"
               "   VPN-A        VPN-A\n\n"
               "Which protocol carries VPNv4 routes between PE1 and PE2?",
               [("OSPF", False), ("LDP", False), ("MP-BGP", True), ("RSVP", False)],
               "MP-BGP with VPNv4 address family exchanges customer routes between PE routers.",
               "MPLS L3VPN", 25.0, 2, "understand"),
        make_q("jncis-sp",
               "Topology:\n\n"
               "   [R1]---[R2]---[R3]---[R4]\n"
               "   All 10 Gbps except R2-R3 1 Gbps\n\n"
               "An LSP from R1 to R4 needs 5 Gbps. Which path does CSPF choose?",
               [("R1-R2-R3-R4", False),
                ("Any path satisfying bandwidth", True),
                ("Lowest IGP metric path", False),
                ("CSPF ignores bandwidth", False)],
               "CSPF selects a path that meets bandwidth constraints.",
               "MPLS TE", 20.0, 3, "analyze"),
        make_q("jncis-sp",
               "Refer to the BGP route reflector topology:\n\n"
               "         [RR]\n"
               "        /    \\\n"
               "     [PE1]  [PE2]\n\n"
               "PE1 receives a VPNv4 route from a CE. How does PE2 learn it?",
               [("Directly from PE1", False),
                ("Reflected by RR", True),
                ("Via OSPF", False),
                ("Via LDP", False)],
               "Route reflectors reflect routes between iBGP clients.",
               "BGP", 20.0, 2, "understand"),
        make_q("jncis-sp",
               "Topology:\n\n"
               "   [R1]---[R2]---[R3]\n"
               "   SRGB 1000-2000 all nodes\n\n"
               "R1 sends traffic using explicit path 1002-1003. What does 1003 represent?",
               [("R3's prefix SID", True),
                ("R2's adjacency SID", False),
                ("R1's node SID", False),
                ("Service label", False)],
               "1003 is the prefix/node SID for R3 within the SRGB.",
               "Segment Routing", 15.0, 3, "understand"),
        make_q("jncis-sp",
               "Refer to the IS-IS topology:\n\n"
               "   [R1]---Area 49.0001---[R2]---Area 49.0002---[R3]\n\n"
               "All routers are L1/L2. Which statement is true?",
               [("R3 sees R1's L1 routes natively", False),
                ("R2 leaks L1 routes from Area 49.0001 into L2", True),
                ("IS-IS does not support route leaking", False),
                ("R3 must be L1 only", False)],
               "L1/L2 routers leak L1 routes into the L2 backbone.",
               "IS-IS", 15.0, 3, "analyze"),
        make_q("jncis-sp",
               "Topology:\n\n"
               "   [R1]---[R2]---[R3]\n"
               "   LDP enabled\n\n"
               "Which transport does LDP use for session establishment?",
               [("UDP only", False), ("TCP", True), ("SCTP", False), ("ICMP", False)],
               "LDP discovery uses UDP, but the session is TCP-based.",
               "MPLS", 15.0, 2, "understand"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIS-SEC
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncis-sec",
               "Refer to the SRX topology:\n\n"
               "   [Untrust]---[SRX]---[Trust]\n"
               "                |\n"
               "             [DMZ]\n\n"
               "A policy allows HTTP from Untrust to DMZ. What is the destination zone?",
               [("Untrust", False), ("Trust", False), ("DMZ", True), ("Any", False)],
               "The destination zone is where the target resource resides.",
               "Security Policies", 20.0, 2, "understand"),
        make_q("jncis-sec",
               "Topology:\n\n"
               "   [Branch]---VPN---[HQ]\n"
               "   10.1.0.0/16     10.2.0.0/16\n\n"
               "What is required for route-based VPN traffic?",
               [("Proxy-ID", False),
                ("Routes to tunnel interface", True),
                ("NAT on both sides", False),
                ("Same subnet", False)],
               "Route-based VPNs require routes to direct traffic into the tunnel.",
               "VPN", 20.0, 3, "understand"),
        make_q("jncis-sec",
               "Refer to the topology:\n\n"
               "   [User]---[SRX]---[Web]\n\n"
               "AppSecure identifies HTTPS traffic as a specific application. Which Layer does AppID inspect?",
               [("Layer 3", False), ("Layer 4", False), ("Layer 7", True), ("Layer 2", False)],
               "AppID performs Layer 7 inspection to identify applications.",
               "AppSecure", 20.0, 2, "understand"),
        make_q("jncis-sec",
               "Topology:\n\n"
               "   [Internet]---[SRX-1]====[SRX-2]---[Trust]\n\n"
               "Which link is used for state synchronization in a chassis cluster?",
               [("Control link", True), ("Data link", False), ("Management", False), ("Console", False)],
               "The control link carries state and configuration synchronization.",
               "High Availability", 20.0, 2, "understand"),
        make_q("jncis-sec",
               "Refer to the topology:\n\n"
               "   [Host-A]---[SRX]---[Host-B]\n"
               "   10.1.1.10      203.0.113.10\n\n"
               "Host-A browses to Host-B. Which NAT type translates Host-A's address?",
               [("Destination NAT", False), ("Source NAT", True), ("Static NAT", False), ("Twice NAT", False)],
               "Source NAT translates the source address of outgoing traffic.",
               "NAT", 20.0, 2, "understand"),
        make_q("jncis-sec",
               "Topology:\n\n"
               "   [Attacker]---[SRX]---[Server]\n\n"
               "Many SYN packets hit the Server with no corresponding ACKs. Which Screen option helps?",
               [("Port scan", False), ("SYN flood", True), ("IP spoofing", False), ("Session limit", False)],
               "The SYN flood Screen option detects and mitigates TCP SYN floods.",
               "Screens", 20.0, 2, "understand"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIS-DC
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncis-dc",
               "Refer to the EVPN topology:\n\n"
               "   [Leaf1]====[Spine]====[Leaf2]\n"
               "   VTEP                  VTEP\n\n"
               "Which device role is typically NOT a VTEP?",
               [("Leaf", False), ("Spine", True), ("Border leaf", False), ("Hypervisor", False)],
               "Spine provides IP underlay; leaves act as VTEPs.",
               "VXLAN", 20.0, 2, "understand"),
        make_q("jncis-dc",
               "Topology:\n\n"
               "   [Server1]---[Leaf1]====[Leaf2]---[Server2]\n"
               "   VNI 10001             VNI 10001\n\n"
               "What identifies the shared Layer 2 segment?",
               [("VLAN", False), ("VNI", True), ("RD", False), ("Loopback", False)],
               "The VNI identifies the Layer 2 overlay segment.",
               "VXLAN", 20.0, 2, "understand"),
        make_q("jncis-dc",
               "Refer to the topology:\n\n"
               "   [Server]---[Leaf1]====[Leaf2]---[Server]\n"
               "            ES-1         ES-1\n\n"
               "What provides active-active multihoming?",
               [("MC-LAG", False), ("EVPN multihoming", True), ("VRRP", False), ("LACP", False)],
               "EVPN multihoming provides active-active L2 multihoming via Ethernet Segments.",
               "EVPN", 20.0, 3, "understand"),
        make_q("jncis-dc",
               "Topology:\n\n"
               "   [SW1]====[SW2]====[SW3]\n"
               "   Member   Member   Member\n\n"
               "What combines them into one logical control plane?",
               [("MC-LAG", False), ("Virtual Chassis", True), ("EVPN", False), ("VCF", False)],
               "Virtual Chassis combines multiple switches into one logical device.",
               "Virtual Chassis", 15.0, 2, "understand"),
        make_q("jncis-dc",
               "Refer to the topology:\n\n"
               "   [Compute]---[vRouter]---[Underlay]---[vRouter]---[Compute]\n\n"
               "Which Contrail component runs on the compute node?",
               [("Config node", False), ("vRouter", True), ("Control node", False), ("Analytics node", False)],
               "Contrail vRouter runs on compute nodes and forwards tenant traffic.",
               "Contrail", 15.0, 2, "understand"),
        make_q("jncis-dc",
               "Topology:\n\n"
               "   [Spine1]====[Spine2]\n"
               "      ||        ||\n"
               "   [Leaf1]====[Leaf2]\n\n"
               "Which protocol carries EVPN routes between leaves and spines?",
               [("OSPF", False), ("IS-IS", False), ("MP-BGP", True), ("LDP", False)],
               "EVPN routes are exchanged via MP-BGP.",
               "EVPN", 15.0, 2, "understand"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIS-AUT
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncis-aut",
               "Refer to the automation topology:\n\n"
               "   [Ansible Control]---NETCONF/SSH---[Junos]\n\n"
               "Which module pushes config to Junos?",
               [("ios_config", False), ("junos_config", True), ("netconf_rpc", False), ("template", False)],
               "junos_config manages Junos configurations via NETCONF.",
               "Ansible", 20.0, 1, "remember"),
        make_q("jncis-aut",
               "Topology:\n\n"
               "   [Python]---NETCONF-830---[Junos]\n\n"
               "Which Python library is standard for this?",
               [("Paramiko", False), ("ncclient", True), ("Requests", False), ("Scapy", False)],
               "ncclient is the standard Python NETCONF client library.",
               "NETCONF", 20.0, 1, "remember"),
        make_q("jncis-aut",
               "Refer to the topology:\n\n"
               "   [NETCONF Client]---RPC---[Junos]---|configuration|\\--->[Candidate]\n\n"
               "Which operation loads config into the candidate database?",
               [("<get-config>", False), ("<edit-config>", True), ("<copy-config>", False), ("<delete-config>", False)],
               "<edit-config> loads configuration changes into the candidate database.",
               "NETCONF", 20.0, 2, "understand"),
        make_q("jncis-aut",
               "Topology:\n\n"
               "   [REST Client]---HTTP---[Junos REST API]\n\n"
               "Which method replaces a complete resource?",
               [("POST", False), ("PUT", True), ("PATCH", False), ("GET", False)],
               "PUT replaces the entire resource.",
               "REST API", 20.0, 2, "understand"),
        make_q("jncis-aut",
               "Refer to the topology:\n\n"
               "   [Junos]--->[SYSLOG]--->[Event Script]--->[Action]\n\n"
               "Which script type is triggered by syslog events?",
               [("Op script", False), ("Event script", True), ("Commit script", False), ("SNMP script", False)],
               "Event scripts are triggered by syslog events and can take corrective actions.",
               "Junos Automation", 20.0, 2, "understand"),
        make_q("jncis-aut",
               "Topology:\n\n"
               "   [Git]--->[CI/CD]--->[NETCONF]--->[Junos]\n\n"
               "What is the benefit of this pipeline?",
               [("Version-controlled, automated configuration deployment", True),
                ("Faster packet forwarding", False),
                ("Physical cabling automation", False),
                ("Removes need for routing protocols", False)],
               "CI/CD with NETCONF enables version-controlled and automated config deployment.",
               "Automation Concepts", 20.0, 2, "understand"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIP-ENT
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncip-ent",
               "Refer to the BGP topology:\n\n"
               "   AS 65001 --- eBGP --- AS 65002 --- eBGP --- AS 65003\n\n"
               "AS 65002 receives a route from AS 65001 with Local Preference 200 and MED 50.\n"
               "The same route is received from AS 65003 with Local Preference 100 and MED 10.\n"
               "Which path does AS 65002 prefer for outbound traffic?",
               [("Path through AS 65001", True),
                ("Path through AS 65003", False),
                ("It load-balances both paths", False),
                ("It cannot decide without AS Path length", False)],
               "Local Preference is evaluated before MED. Higher Local Preference wins.",
               "BGP", 25.0, 3, "analyze"),
        make_q("jncip-ent",
               "OSPF topology:\n\n"
               "        [R1]---Area 0---[R2]---Area 1---[R3]\n"
               "        10.1.1.0/24     10.2.2.0/24\n\n"
               "R1 advertises 10.1.1.0/24 into Area 0. What LSA type does R3 see for 10.1.1.0/24?",
               [("Type 1", False), ("Type 2", False), ("Type 3", True), ("Type 5", False)],
               "Inter-area routes are advertised as Type 3 Summary LSAs by ABRs.",
               "OSPF", 20.0, 3, "analyze"),
        make_q("jncip-ent",
               "EVPN-VXLAN campus topology:\n\n"
               "   [Leaf1]====[Spine1]====[Leaf2]\n"
               "   VTEP       VTEP?        VTEP\n\n"
               "Which device role is typically NOT a VTEP in a two-tier EVPN-VXLAN campus?",
               [("Access/Leaf switch", False),
                ("Distribution/Core switch", False),
                ("Spine switch", True),
                ("WAN edge router", False)],
               "In a two-tier campus fabric, leaf/access switches act as VTEPs; spine provides IP underlay.",
               "EVPN/VXLAN", 20.0, 3, "understand"),
        make_q("jncip-ent",
               "Multicast topology using PIM-SM:\n\n"
               "   [Source]---[R1]---[R2]---[Receiver]\n"
               "              RP\n\n"
               "Which tree is initially built from source to RP?",
               [("Shared tree (*,G)", False),
                ("Shortest-path tree (S,G)", True),
                ("Bidirectional tree", False),
                ("None; receivers join directly to source", False)],
               "In PIM-SM, the source registers with RP and an SPT (S,G) is built from source to RP.",
               "Multicast", 10.0, 3, "understand"),
        make_q("jncip-ent",
               "Refer to the CoS topology:\n\n"
               "   [Voice]---[EF Queue]---[Router]---[BE Queue]---[Data]\n\n"
               "Which scheduler services EF before BE?",
               [("WRR", False), ("Strict-high priority", True), ("RED", False), ("Tail drop", False)],
               "Strict-high priority queues are serviced before other queues.",
               "CoS", 15.0, 2, "understand"),
        make_q("jncip-ent",
               "Topology:\n\n"
               "   [PE1]---[P]---[PE2]\n"
               "   VPN-A     VPN-A\n\n"
               "Which protocol carries VPNv4 routes between PE1 and PE2?",
               [("OSPF", False), ("LDP", False), ("MP-BGP", True), ("RSVP", False)],
               "MP-BGP with VPNv4 address family exchanges customer routes between PEs.",
               "BGP/MPLS", 10.0, 3, "understand"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIP-SP
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncip-sp",
               "MPLS L3VPN topology:\n\n"
               "   CE1--PE1--P--PE2--CE2\n"
               "   VPN-A        VPN-A\n\n"
               "Which protocol carries VPNv4 routes between PE1 and PE2?",
               [("OSPF", False), ("LDP", False), ("MP-BGP", True), ("RSVP", False)],
               "MP-BGP with VPNv4 address family exchanges customer routes between PE routers.",
               "MPLS L3VPN", 25.0, 2, "understand"),
        make_q("jncip-sp",
               "RSVP-TE topology:\n\n"
               "   [R1]---[R2]---[R3]---[R4]\n"
               "   All links 10 Gbps except R2-R3 1 Gbps\n\n"
               "An LSP from R1 to R4 is signaled with bandwidth 5 Gbps. Which path is chosen by CSPF?",
               [("R1-R2-R3-R4", False),
                ("R1-R2-R3-R4 if it has lowest IGP metric", False),
                ("The path that satisfies 5 Gbps constraint", True),
                ("CSPF ignores bandwidth constraints", False)],
               "CSPF selects a path that meets bandwidth constraints; R2-R3 1 Gbps link cannot carry 5 Gbps LSP.",
               "MPLS TE", 20.0, 3, "analyze"),
        make_q("jncip-sp",
               "BGP topology with route reflectors:\n\n"
               "         [RR]\n"
               "        /    \\\n"
               "     [PE1]  [PE2]\n\n"
               "PE1 receives a VPNv4 route from a CE. How does PE2 learn it?",
               [("PE1 sends it directly to PE2", False),
                ("PE1 sends it to RR, which reflects to PE2", True),
                ("It is flooded via OSPF", False),
                ("It is learned via LDP", False)],
               "Route reflectors eliminate full-mesh iBGP by reflecting routes between clients.",
               "BGP", 20.0, 2, "understand"),
        make_q("jncip-sp",
               "IS-IS topology:\n\n"
               "   [R1]---Area 49.0001---[R2]---Area 49.0002---[R3]\n\n"
               "All routers are L1/L2. Which statement is true about L1 routes in Area 49.0002?",
               [("R3 sees R1's L1 routes natively", False),
                ("R2 leaks L1 routes from Area 49.0001 into Area 49.0002 as L2 routes", True),
                ("IS-IS does not support route leaking", False),
                ("R3 must run L1 only", False)],
               "L1/L2 routers leak L1 routes into the L2 backbone. By default, L2 routes are not leaked down to L1.",
               "IS-IS", 15.0, 3, "analyze"),
        make_q("jncip-sp",
               "Segment Routing topology:\n\n"
               "   [R1]---[R2]---[R3]\n"
               "   SRGB 1000-2000 on all nodes\n\n"
               "R1 wants to send traffic to R3 using explicit SR path 1002-1003. What does 1003 represent?",
               [("R3's prefix SID", True),
                ("R2's adjacency SID", False),
                ("R1's node SID", False),
                ("A service label", False)],
               "The prefix/node SID for R3 is 1003 within the SRGB.",
               "Segment Routing", 20.0, 3, "understand"),
        make_q("jncip-sp",
               "LDP topology:\n\n"
               "   [R1]---[R2]---[R3]\n\n"
               "LDP is enabled on all interfaces. Which statement is true?",
               [("LDP sessions are TCP-based and established between directly connected neighbors", True),
                ("LDP uses UDP only", False),
                ("LDP requires RSVP to be enabled", False),
                ("LDP labels are advertised only for BGP routes", False)],
               "LDP discovery uses UDP hello, but session is TCP-based between directly connected neighbors.",
               "MPLS", 20.0, 2, "understand"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIP-SEC
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncip-sec",
               "Refer to the SRX topology:\n\n"
               "   [Untrust]---[SRX Cluster]---[Trust]\n"
               "                |    |\n"
               "             Node0 Node1\n\n"
               "Which link is used for control-plane communication?",
               [("Fabric link", False), ("Control link", True), ("Data link", False), ("HA link", False)],
               "The control link carries control-plane and state synchronization traffic.",
               "High Availability", 20.0, 2, "understand"),
        make_q("jncip-sec",
               "Topology:\n\n"
               "   [User]---[SRX]---[Internet]\n\n"
               "SSL Forward Proxy is configured. What can be inspected?",
               [("Outbound HTTPS traffic", True),
                ("Inbound SSH traffic", False),
                ("Outgoing DNS queries only", False),
                ("Only unencrypted HTTP", False)],
               "SSL Forward Proxy decrypts outbound HTTPS traffic for UTM/IPS inspection.",
               "SSL Proxy", 20.0, 3, "understand"),
        make_q("jncip-sec",
               "Refer to the topology:\n\n"
               "   [Zone-A]---[SRX]---[Zone-B]\n"
               "   10.1.0.0/16      10.2.0.0/16\n\n"
               "A security policy allows traffic from Zone-A to Zone-B. What else is required for NAT?",
               [("Source NAT rule", True),
                ("Destination NAT rule", False),
                ("Static NAT rule", False),
                ("No NAT needed", False)],
               "Source NAT is typically required for outgoing traffic from private zones.",
               "NAT", 20.0, 3, "understand"),
        make_q("jncip-sec",
               "Topology:\n\n"
               "   [Branch]---IPsec---[HQ]\n"
               "   10.1.0.0/16      10.2.0.0/16\n\n"
               "Which IKE phase establishes the IPsec SA?",
               [("IKE Phase 1", False), ("IKE Phase 2", True), ("IKE Phase 3", False), ("Dead Peer Detection", False)],
               "IKE Phase 2 negotiates the IPsec SA and security parameters.",
               "VPN", 20.0, 3, "understand"),
        make_q("jncip-sec",
               "Refer to the topology:\n\n"
               "   [Internet]---[SRX]---[DMZ]---[Web Server]\n\n"
               "Which feature protects the Web Server from HTTP floods?",
               [("AppDoS", True), ("Source NAT", False), ("Route lookup", False), ("DNS proxy", False)],
               "AppDoS provides application-layer DoS protection.",
               "AppSecure", 20.0, 3, "understand"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIP-DC
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncip-dc",
               "Refer to the EVPN-VXLAN topology:\n\n"
               "   [Leaf1]====[Spine]====[Leaf2]\n"
               "   VTEP                  VTEP\n\n"
               "Which device typically does NOT run as a VTEP?",
               [("Leaf switch", False), ("Spine switch", True), ("Border leaf", False), ("Hypervisor", False)],
               "Spine switches provide IP underlay only; leaf switches act as VTEPs.",
               "VXLAN", 25.0, 2, "understand"),
        make_q("jncip-dc",
               "Topology:\n\n"
               "   [Server1]---[Leaf1]====[Leaf2]---[Server2]\n"
               "   VNI 10001             VNI 10001\n\n"
               "What identifies the shared Layer 2 segment?",
               [("VLAN ID", False), ("VNI", True), ("Route Distinguisher", False), ("Loopback IP", False)],
               "VXLAN Network Identifier (VNI) identifies the Layer 2 overlay segment.",
               "VXLAN", 25.0, 2, "understand"),
        make_q("jncip-dc",
               "Refer to the topology:\n\n"
               "   [Server]---[Leaf1]====[Leaf2]---[Server]\n"
               "            ES-1         ES-1\n\n"
               "What provides active-active multihoming?",
               [("MC-LAG", False), ("EVPN multihoming", True), ("VRRP", False), ("LACP", False)],
               "EVPN multihoming provides active-active L2 multihoming via Ethernet Segments.",
               "EVPN", 25.0, 3, "understand"),
        make_q("jncip-dc",
               "Topology:\n\n"
               "   [Spine1]====[Spine2]\n"
               "      ||        ||\n"
               "   [Leaf1]====[Leaf2]\n\n"
               "Which protocol carries EVPN routes?",
               [("OSPF", False), ("IS-IS", False), ("MP-BGP", True), ("LDP", False)],
               "EVPN routes are exchanged via MP-BGP.",
               "EVPN", 15.0, 2, "understand"),
        make_q("jncip-dc",
               "Refer to the topology:\n\n"
               "   [Tenant-A]---[vRouter]---[Underlay]---[vRouter]---[Tenant-B]\n\n"
               "Which Contrail component runs on the compute node?",
               [("Config node", False), ("vRouter", True), ("Control node", False), ("Analytics node", False)],
               "Contrail vRouter runs on compute nodes and forwards tenant traffic.",
               "Contrail", 15.0, 2, "understand"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIP-AUT
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncip-aut",
               "Refer to the automation topology:\n\n"
               "   [Ansible]---NETCONF---[Junos]\n\n"
               "Which module pushes configuration?",
               [("ios_config", False), ("junos_config", True), ("netconf_rpc", False), ("template", False)],
               "junos_config manages Junos configurations via NETCONF.",
               "Ansible", 25.0, 1, "remember"),
        make_q("jncip-aut",
               "Topology:\n\n"
               "   [NETCONF Client]---RPC---[Junos]\n\n"
               "Which RPC retrieves the candidate configuration?",
               [("<get-config>", True), ("<edit-config>", False), ("<copy-config>", False), ("<delete-config>", False)],
               "<get-config> retrieves configuration data from a datastore.",
               "NETCONF", 25.0, 2, "understand"),
        make_q("jncip-aut",
               "Refer to the topology:\n\n"
               "   [REST Client]---HTTPS---[Junos REST API]\n\n"
               "Which HTTP method partially updates a resource?",
               [("POST", False), ("PUT", False), ("PATCH", True), ("GET", False)],
               "PATCH applies partial updates to a resource.",
               "REST API", 25.0, 2, "understand"),
        make_q("jncip-aut",
               "Topology:\n\n"
               "   [Git]--->[CI/CD]--->[NETCONF]--->[Junos]\n\n"
               "What does this pipeline provide?",
               [("Version-controlled automated configuration deployment", True),
                ("Faster packet forwarding", False),
                ("Physical cabling automation", False),
                ("Removes need for routing protocols", False)],
               "CI/CD with NETCONF enables version-controlled and automated config deployment.",
               "Automation Concepts", 25.0, 2, "understand"),
        make_q("jncip-aut",
               "Refer to the topology:\n\n"
               "   [Junos]--->[SYSLOG]--->[Event Script]--->[Action]\n\n"
               "Which script type is triggered by syslog events?",
               [("Op script", False), ("Event script", True), ("Commit script", False), ("SNMP script", False)],
               "Event scripts are triggered by syslog events and can take corrective actions.",
               "Junos Automation", 25.0, 2, "understand"),
    ]

    return questions


def questions_to_sql(questions: list[dict]) -> str:
    ids = ",".join(f"'{q['id']}'" for q in questions)
    lines = [
        "-- +goose Up",
        "-- +goose StatementBegin",
        "",
        "-- Juniper topology-based questions for all exams",
        f"-- Generated {len(questions)} questions",
        "",
    ]
    for q in questions:
        options_json = json.dumps(q["options"], ensure_ascii=False)
        urls = "{" + ",".join(f'"{u}"' for u in q["reference_urls"]) + "}"
        lines.append(
            f"INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) VALUES ("
            f"'{q['id']}', "
            f"'{q['exam_id']}', "
            f"'{q['track_id']}', "
            f"'{q['question_type']}', "
            f"{q['difficulty']}, "
            f"'{q['bloom_level']}', "
            f"$${q['body']}$$::text, "
            f"$${options_json}$$::jsonb, "
            f"$${q['explanation']}$$::text, "
            f"$${urls}$$::text[], "
            f"$${q['blueprint_section']}$$::text, "
            f"{q['blueprint_weight']}, "
            f"'{q['content_hash']}', "
            f"{str(q['is_active']).lower()}"
            f") ON CONFLICT (id) DO NOTHING;"
        )
    lines += [
        "",
        "-- +goose StatementEnd",
        "",
        "-- +goose Down",
        "-- +goose StatementBegin",
        "",
        f"DELETE FROM questions WHERE id IN ({ids});",
        "",
        "-- +goose StatementEnd",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    questions = generate_all()
    print(questions_to_sql(questions))
