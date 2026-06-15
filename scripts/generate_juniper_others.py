#!/usr/bin/env python3
"""
NetCert — Juniper remaining exams question generator.
Covers JNCIA-SP, JNCIA-SEC, JNCIA-DC, JNCIA-AUT, JNCIP-SEC, JNCIP-DC, JNCIP-AUT.
Generates realistic, single-choice questions aligned with each track's focus.
"""
import hashlib
import json
import uuid

EXAMS = {
    "jncia-sp":   {"exam_id": "b0000000-0000-0000-0000-000000000002", "track_id": "a0000000-0000-0000-0000-000000000002", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-junos.html"},
    "jncia-sec":  {"exam_id": "b0000000-0000-0000-0000-000000000022", "track_id": "a0000000-0000-0000-0000-000000000003", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-sec.html"},
    "jncia-dc":   {"exam_id": "b0000000-0000-0000-0000-000000000020", "track_id": "a0000000-0000-0000-0000-000000000004", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-dc.html"},
    "jncia-aut":  {"exam_id": "b0000000-0000-0000-0000-000000000021", "track_id": "a0000000-0000-0000-0000-000000000005", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-automation.html"},
    "jncip-sec":  {"exam_id": "b0000000-0000-0000-0000-000000000024", "track_id": "a0000000-0000-0000-0000-000000000003", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-sec.html"},
    "jncip-dc":   {"exam_id": "b0000000-0000-0000-0000-000000000026", "track_id": "a0000000-0000-0000-0000-000000000004", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-dc.html"},
    "jncip-aut":  {"exam_id": "b0000000-0000-0000-0000-000000000028", "track_id": "a0000000-0000-0000-0000-000000000005", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-automation.html"},
}


def qid(exam: str, seed: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_OID, f"{exam}:{seed}"))


def content_hash(body: str, correct: str) -> str:
    return hashlib.sha256(f"{body}::{correct}".encode()).hexdigest()[:16]


def make_q(exam: str, body: str, options: list[tuple[str, bool]], explanation: str,
           section: str, weight: float, difficulty: int = 2,
           bloom: str = "understand") -> dict:
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
        "question_type": "single-choice",
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
    # JNCIA-SP
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncia-sp", "Which protocol dynamically assigns labels in an MPLS network without traffic engineering?",
               [("RSVP", False), ("LDP", True), ("BGP", False), ("IS-IS", False)],
               "LDP distributes labels for MPLS forwarding without requiring traffic engineering extensions.",
               "MPLS Fundamentals", 20.0, 2, "understand"),
        make_q("jncia-sp", "Which BGP attribute influences inbound traffic from neighboring autonomous systems?",
               [("Local Preference", False), ("MED", True), ("Origin", False), ("Next Hop", False)],
               "MED is advertised to external peers and influences how they send traffic into your AS.",
               "BGP Fundamentals", 20.0, 2, "understand"),
        make_q("jncia-sp", "What is the purpose of MPLS PHP?",
               [("To add a second label", False),
                ("To remove the top label before the egress router", True),
                ("To encrypt MPLS traffic", False), ("To enable RSVP", False)],
               "Penultimate Hop Popping removes the MPLS label one hop before the egress router to reduce its processing.",
               "MPLS Fundamentals", 20.0, 2, "understand"),
        make_q("jncia-sp", "Which OSPF area type accepts a default route but no external LSAs?",
               [("Standard", False), ("Stub", True), ("Backbone", False), ("Transit", False)],
               "Stub areas block Type 5 external LSAs and use a default route for external destinations.",
               "IGP Fundamentals", 20.0, 2, "understand"),
        make_q("jncia-sp", "Which command displays BGP neighbors on a Junos device?",
               [("show bgp summary", True), ("show route bgp", False),
                ("show protocols bgp", False), ("show bgp database", False)],
               "'show bgp summary' displays BGP peer sessions, AS numbers, and message counts.",
               "BGP Fundamentals", 20.0, 1, "apply"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIA-SEC
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncia-sec", "Which SRX feature inspects traffic at Layer 7 to identify applications?",
               [("Packet mode", False), ("AppSecure/AppID", True), ("NAT", False), ("VLAN tagging", False)],
               "AppID/AppSecure identifies applications using Layer 7 inspection and signatures.",
               "Security Policies", 25.0, 2, "understand"),
        make_q("jncia-sec", "Which zone type on SRX is typically used for untrusted networks?",
               [("Trust", False), ("Untrust", True), ("DMZ", False), ("Mgmt", False)],
               "The Untrust zone represents untrusted networks such as the Internet on SRX devices.",
               "Zones", 25.0, 1, "remember"),
        make_q("jncia-sec", "Which NAT type translates many private addresses to one public IP using ports?",
               [("Static NAT", False), ("Destination NAT", False), ("Source NAT with PAT", True), ("Twice NAT", False)],
               "Source NAT with port address translation maps many private addresses to a single public IP.",
               "NAT", 25.0, 2, "understand"),
        make_q("jncia-sec", "Which Screen option protects against SYN flood attacks?",
               [("IP spoofing", False), ("SYN flood protection", True), ("Port scan", False), ("Session limit", False)],
               "The SYN flood Screen option detects and mitigates TCP SYN flood attacks.",
               "Screens", 25.0, 2, "understand"),
        make_q("jncia-sec", "Which command shows active security policies on an SRX?",
               [("show security policies", True), ("show firewall", False),
                ("show configuration security policies", False), ("show security zones", False)],
               "'show security policies' displays active security policies and hit counts.",
               "Security Policies", 25.0, 1, "apply"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIA-DC
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncia-dc", "Which Juniper data center switching platform runs Junos OS Evolved?",
               [("EX Series", False), ("QFX Series", True), ("SRX Series", False), ("MX Series", False)],
               "QFX Series switches are designed for data center deployments and run Junos OS or Junos OS Evolved.",
               "DC Platforms", 25.0, 1, "remember"),
        make_q("jncia-dc", "Which protocol is commonly used for data center overlay networks?",
               [("STP", False), ("VXLAN", True), ("RSTP", False), ("VTP", False)],
               "VXLAN is a data center overlay technology that extends Layer 2 segments over Layer 3 networks.",
               "Overlays", 25.0, 2, "understand"),
        make_q("jncia-dc", "Which feature allows multiple physical links to act as a single logical link?",
               [("VLAN", False), ("LAG/MC-LAG", True), ("VRRP", False), ("OSPF", False)],
               "Link Aggregation Groups (LAG) and Multi-Chassis LAG bundle multiple links for redundancy and bandwidth.",
               "Layer 2", 25.0, 2, "understand"),
        make_q("jncia-dc", "Which routing protocol is often used as the underlay in a data center EVPN-VXLAN fabric?",
               [("RIP", False), ("EBGP", True), ("IS-IS", False), ("Either EBGP or IS-IS", False)],
               "EBGP is commonly used as the underlay routing protocol in EVPN-VXLAN data center fabrics due to its simplicity.",
               "Underlay", 25.0, 2, "understand"),
        make_q("jncia-dc", "Which command displays EVPN routes on a QFX switch?",
               [("show evpn route", True), ("show bgp evpn", False),
                ("show route evpn", False), ("show ethernet-switching evpn", False)],
               "'show evpn route' displays EVPN MAC/IP routes and their next-hops on Junos EVPN-enabled devices.",
               "EVPN", 25.0, 2, "apply"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIA-AUT
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncia-aut", "Which Junos automation tool uses YAML-based playbooks?",
               [("Ansible", True), ("Chef", False), ("Puppet", False), ("Terraform", False)],
               "Ansible uses YAML playbooks to automate device configuration and orchestration.",
               "Automation Tools", 25.0, 1, "remember"),
        make_q("jncia-aut", "Which protocol uses YANG data models for configuration and state retrieval?",
               [("SNMP", False), ("NETCONF", True), ("Syslog", False), ("SSH", False)],
               "NETCONF uses YANG data models to provide structured configuration and state retrieval.",
               "NETCONF/YANG", 25.0, 2, "understand"),
        make_q("jncia-aut", "Which data format is native to NETCONF?",
               [("JSON", False), ("YAML", False), ("XML", True), ("CSV", False)],
               "NETCONF messages are encoded in XML by default.",
               "NETCONF/YANG", 25.0, 1, "remember"),
        make_q("jncia-aut", "Which Junos feature allows executing operational commands and collecting data using Python?",
               [("PyEZ", True), ("Junos Space", False), ("J-Web", False), ("Ansible", False)],
               "PyEZ is a Python library that enables automation of Junos devices, including RPC calls and configuration changes.",
               "Automation Tools", 25.0, 2, "understand"),
        make_q("jncia-aut", "Which REST API HTTP method retrieves data from a device?",
               [("POST", False), ("PUT", False), ("GET", True), ("DELETE", False)],
               "HTTP GET requests retrieve data. POST creates, PUT updates, DELETE removes.",
               "REST API", 25.0, 1, "remember"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIP-SEC
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncip-sec", "Which SRX feature provides centralized management and logging for multiple devices?",
               [("J-Web", False), ("Junos Space Security Director", True), ("CLI", False), ("SYSLOG", False)],
               "Junos Space Security Director provides centralized policy management, logging, and monitoring for SRX devices.",
               "Management", 15.0, 2, "understand"),
        make_q("jncip-sec", "Which IPsec mode encrypts the entire original IP packet?",
               [("Transport mode", False), ("Tunnel mode", True), ("AH mode", False), ("ESP mode", False)],
               "IPsec tunnel mode encapsulates and encrypts the entire original IP packet. Transport mode encrypts only the payload.",
               "IPsec VPNs", 15.0, 2, "understand"),
        make_q("jncip-sec", "Which SRX feature provides high availability by synchronizing sessions between nodes?",
               [("JSRP", True), ("VRRP", False), ("LACP", False), ("OSPF", False)],
               "Juniper SRX redundancy protocol (JSRP) enables chassis cluster high availability and session synchronization.",
               "High Availability", 15.0, 2, "remember"),
        make_q("jncip-sec", "Which VPN topology connects every site to every other site directly?",
               [("Hub-and-spoke", False), ("Full mesh", True), ("Point-to-point", False), ("Remote access", False)],
               "A full-mesh VPN topology has direct tunnels between every pair of sites.",
               "IPsec VPNs", 15.0, 2, "understand"),
        make_q("jncip-sec", "Which security feature authenticates users before allowing network access?",
               [("Firewall filter", False), ("802.1X", True), ("NAT", False), ("VLAN", False)],
               "802.1X provides port-based network access control, authenticating users or devices before granting access.",
               "Access Control", 15.0, 2, "understand"),
        make_q("jncip-sec", "Which SRX feature provides intrusion detection and prevention?",
               [("AppID", False), ("IDP", True), ("UTM", False), ("Screens", False)],
               "Intrusion Detection and Prevention (IDP) inspects traffic for known attacks and takes action.",
               "Advanced Security", 15.0, 2, "remember"),
        make_q("jncip-sec", "Which authentication protocol is commonly used with 802.1X?",
               [("RADIUS", True), ("TACACS+", False), ("LDAP", False), ("SNMP", False)],
               "RADIUS is the most common authentication server protocol used with 802.1X.",
               "Access Control", 15.0, 2, "understand"),
        make_q("jncip-sec", "What does UTM stand for in SRX?",
               [("Unified Threat Management", True), ("Universal Traffic Monitoring", False),
                ("Unified Traffic Manager", False), ("User Threat Management", False)],
               "UTM (Unified Threat Management) includes antivirus, antispam, and web filtering features on SRX.",
               "UTM", 10.0, 1, "remember"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIP-DC
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncip-dc", "Which EVPN route type advertises MAC/IP reachability?",
               [("Type 1", False), ("Type 2", True), ("Type 3", False), ("Type 4", False)],
               "EVPN Type 2 routes advertise MAC and IP reachability information.",
               "EVPN", 15.0, 2, "remember"),
        make_q("jncip-dc", "Which protocol is typically used as the overlay encapsulation in EVPN-VXLAN fabrics?",
               [("MPLS", False), ("VXLAN", True), ("GRE", False), ("IPsec", False)],
               "VXLAN is the common encapsulation for EVPN data center overlays.",
               "VXLAN", 15.0, 2, "understand"),
        make_q("jncip-dc", "Which feature prevents Layer 2 loops in an EVPN-VXLAN fabric?",
               [("STP", False), ("Split horizon", True), ("VRRP", False), ("OSPF", False)],
               "EVPN uses split-horizon and designated forwarder election to prevent Layer 2 loops, reducing reliance on STP.",
               "EVPN", 15.0, 3, "understand"),
        make_q("jncip-dc", "Which Junos feature provides active-active multihoming in EVPN?",
               [("Single-homed ES", False), ("All-active multihoming", True), ("VRRP", False), ("MC-LAG only", False)],
               "EVPN all-active multihoming allows multiple PEs to forward traffic simultaneously for an Ethernet segment.",
               "EVPN Multihoming", 15.0, 3, "understand"),
        make_q("jncip-dc", "Which command displays VXLAN tunnel endpoints?",
               [("show vxlan tunnel", True), ("show evpn vxlan", False),
                ("show route vxlan", False), ("show ethernet-switching vxlan", False)],
               "'show vxlan tunnel' displays VXLAN tunnel endpoint information on Junos devices.",
               "VXLAN", 15.0, 2, "apply"),
        make_q("jncip-dc", "Which data center architecture uses leaf switches connected to every spine switch?",
               [("Three-tier", False), ("Spine-leaf", True), ("Core-aggregation", False), ("Hub-and-spoke", False)],
               "Spine-leaf topology has every leaf connected to every spine, providing predictable latency and scalability.",
               "DC Architecture", 15.0, 2, "understand"),
        make_q("jncip-dc", "Which protocol is used for underlay routing in a BGP-based EVPN fabric?",
               [("OSPF", False), ("IS-IS", False), ("EBGP", True), ("RIP", False)],
               "EBGP is commonly used for the underlay in EVPN-VXLAN fabrics due to simple peer relationships and rich policy.",
               "Underlay", 15.0, 2, "understand"),
        make_q("jncip-dc", "Which Junos command displays the EVPN database?",
               [("show evpn database", True), ("show route evpn", False),
                ("show bgp evpn", False), ("show ethernet-switching table", False)],
               "'show evpn database' displays the EVPN MAC and IP database on Junos.",
               "EVPN", 15.0, 2, "apply"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIP-AUT
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncip-aut", "Which Junos automation feature allows on-box scripts written in Python?",
               [("SLAX", False), ("XSLT", False), ("Python op scripts", True), ("Ansible", False)],
               "Junos supports Python op/event/commit scripts that run directly on the device.",
               "On-box Automation", 15.0, 2, "understand"),
        make_q("jncip-aut", "Which YANG statement defines a configurable parameter?",
               [("leaf", True), ("container", False), ("list", False), ("augment", False)],
               "A 'leaf' statement defines a scalar value, which can be configurable (config true) or state data.",
               "YANG", 15.0, 3, "understand"),
        make_q("jncip-aut", "Which NETCONF operation replaces the entire configuration?",
               [("<merge>", False), ("<edit-config> with merge", False),
                ("<edit-config> with replace", True), ("<copy-config>", False)],
               "<edit-config> with the replace operation replaces the specified configuration hierarchy.",
               "NETCONF", 15.0, 3, "understand"),
        make_q("jncip-aut", "Which Junos XML tag wraps RPC requests?",
               [("<rpc-reply>", False), ("<rpc>", True), ("<config>", False), ("<operation>", False)],
               "NETCONF RPC requests are wrapped in <rpc> tags; replies are in <rpc-reply>.",
               "NETCONF", 15.0, 2, "remember"),
        make_q("jncip-aut", "Which off-box tool is best for declarative infrastructure provisioning?",
               [("Ansible", False), ("Terraform", True), ("PyEZ", False), ("NETCONF", False)],
               "Terraform uses declarative HCL to provision infrastructure, including Junos devices via providers.",
               "Off-box Automation", 15.0, 2, "understand"),
        make_q("jncip-aut", "Which Junos commit script can enforce configuration rules?",
               [("Op script", False), ("Event script", False), ("Commit script", True), ("SNMP script", False)],
               "Commit scripts run during the commit process and can enforce rules, emit warnings, or modify the configuration.",
               "On-box Automation", 15.0, 2, "understand"),
        make_q("jncip-aut", "Which data format is commonly used by REST APIs?",
               [("XML", False), ("YAML", False), ("JSON", True), ("CSV", False)],
               "JSON is the most common data format for REST APIs due to its lightweight and readable structure.",
               "REST APIs", 15.0, 1, "remember"),
        make_q("jncip-aut", "Which HTTP status code indicates a successful resource creation?",
               [("200", False), ("201", True), ("204", False), ("400", False)],
               "HTTP 201 Created indicates a resource was successfully created, typically in response to POST.",
               "REST APIs", 15.0, 1, "remember"),

        # Extended JNCIA-SP
        make_q("jncia-sp", "Which MPLS label distribution protocol uses UDP hello and TCP session?",
               [("LDP", True), ("RSVP", False), ("BGP", False), ("IS-IS", False)],
               "LDP uses UDP hellos for neighbor discovery and TCP for reliable session establishment.",
               "MPLS Fundamentals", 20.0, 2, "understand"),
        make_q("jncia-sp", "Which BGP path attribute is used to influence outbound traffic within an AS?",
               [("Local Preference", True), ("MED", False), ("AS Path", False), ("Origin", False)],
               "Local Preference influences outbound traffic path selection within an autonomous system.",
               "BGP Fundamentals", 20.0, 2, "understand"),
        make_q("jncia-sp", "Which command displays the MPLS forwarding table?",
               [("show route forwarding-table", True), ("show mpls forwarding", False),
                ("show mpls table", False), ("show route mpls", False)],
               "'show route forwarding-table' displays the MPLS forwarding table used by the PFE.",
               "MPLS Fundamentals", 20.0, 2, "apply"),
        make_q("jncia-sp", "Which OSPF LSA type describes routes external to the OSPF domain?",
               [("Type 3", False), ("Type 4", False), ("Type 5", True), ("Type 7", False)],
               "Type 5 LSAs describe external routes redistributed into OSPF by an ASBR.",
               "IGP Fundamentals", 20.0, 2, "remember"),
        make_q("jncia-sp", "Which command shows the BGP routing table?",
               [("show route protocol bgp", True), ("show bgp routes", False),
                ("show route table bgp", False), ("show bgp table", False)],
               "'show route protocol bgp' displays routes learned via BGP.",
               "BGP Fundamentals", 20.0, 1, "apply"),
        make_q("jncia-sp", "Which RSVP object reserves bandwidth for an LSP?",
               [("SENDER_TSPEC", False), ("FLOWSPEC", True), ("LABEL_REQUEST", False), ("EXPLICIT_ROUTE", False)],
               "The RSVP FLOWSPEC object reserves resources such as bandwidth for the LSP.",
               "MPLS Fundamentals", 20.0, 3, "understand"),
        make_q("jncia-sp", "Which command verifies LDP neighbor state?",
               [("show ldp neighbor", True), ("show ldp session", False),
                ("show mpls ldp neighbor", False), ("show ldp interface", False)],
               "'show ldp neighbor' displays LDP neighbors and their states.",
               "MPLS Fundamentals", 20.0, 1, "apply"),
        make_q("jncia-sp", "Which multicast address range is administratively scoped?",
               [("224.0.0.0/8", False), ("232.0.0.0/8", False), ("239.0.0.0/8", True), ("233.0.0.0/8", False)],
               "239.0.0.0/8 is administratively scoped for private multicast use.",
               "Multicast", 10.0, 2, "remember"),
        make_q("jncia-sp", "Which command displays MPLS LSPs and their states?",
               [("show mpls lsp", True), ("show rsvp session", False),
                ("show ldp session", False), ("show route mpls", False)],
               "'show mpls lsp' displays signaled MPLS LSPs and their operational states.",
               "MPLS Fundamentals", 20.0, 1, "apply"),
        make_q("jncia-sp", "Which protocol is used between RPs in different PIM domains?",
               [("IGMP", False), ("MSDP", True), ("PIM", False), ("MBGP", False)],
               "MSDP exchanges source information between RPs in different PIM domains.",
               "Multicast", 10.0, 2, "remember"),

        # Extended JNCIA-SEC
        make_q("jncia-sec", "Which SRX feature inspects traffic for known attack signatures?",
               [("AppID", False), ("IDP", True), ("UTM", False), ("Screens", False)],
               "IDP (Intrusion Detection and Prevention) inspects traffic for known attack signatures.",
               "Advanced Security", 25.0, 2, "understand"),
        make_q("jncia-sec", "Which NAT type maps a public IP to a private IP one-to-one?",
               [("Source NAT", False), ("Static NAT", True), ("Destination NAT", False), ("PAT", False)],
               "Static NAT maps a public IP address to a private IP address one-to-one.",
               "NAT", 25.0, 2, "understand"),
        make_q("jncia-sec", "Which zone is typically used for public-facing servers?",
               [("Trust", False), ("Untrust", False), ("DMZ", True), ("Mgmt", False)],
               "The DMZ zone is commonly used for public-facing servers that need restricted access.",
               "Zones", 25.0, 1, "understand"),
        make_q("jncia-sec", "Which command shows active NAT translations?",
               [("show security nat source pool", False), ("show security flow session", True),
                ("show security nat rules", False), ("show nat translations", False)],
               "'show security flow session' displays active flow sessions including NAT translations.",
               "NAT", 25.0, 2, "apply"),
        make_q("jncia-sec", "Which Screen option detects land attacks?",
               [("IP spoofing", False), ("Land", True), ("Teardrop", False), ("Ping of Death", False)],
               "The Land screen option detects packets with identical source and destination IP addresses.",
               "Screens", 25.0, 2, "remember"),
        make_q("jncia-sec", "Which authentication method uses a local password database?",
               [("RADIUS", False), ("TACACS+", False), ("Local", True), ("LDAP", False)],
               "Local authentication validates credentials against the local device database.",
               "Access Control", 25.0, 1, "remember"),
        make_q("jncia-sec", "Which command shows security zones and interfaces?",
               [("show security zones", True), ("show zones security", False),
                ("show configuration security zones", False), ("show security interfaces", False)],
               "'show security zones' displays configured zones and their associated interfaces.",
               "Zones", 25.0, 1, "apply"),
        make_q("jncia-sec", "Which Junos feature provides antivirus protection on SRX?",
               [("IDP", False), ("UTM Antivirus", True), ("Screens", False), ("AppSecure", False)],
               "UTM Antivirus provides antivirus scanning of traffic on SRX devices.",
               "UTM", 25.0, 1, "remember"),
        make_q("jncia-sec", "Which VPN mode encrypts only the payload, leaving the original IP header?",
               [("Tunnel mode", False), ("Transport mode", True), ("AH mode", False), ("ESP mode", False)],
               "IPsec transport mode encrypts only the payload and leaves the original IP header intact.",
               "IPsec VPNs", 25.0, 2, "understand"),
        make_q("jncia-sec", "Which command displays IPsec security associations?",
               [("show security ipsec security-associations", True), ("show ipsec sa", False),
                ("show security vpn sa", False), ("show ike sa", False)],
               "'show security ipsec security-associations' displays active IPsec SAs on SRX.",
               "IPsec VPNs", 25.0, 2, "apply"),

        # Extended JNCIA-DC
        make_q("jncia-dc", "Which QFX feature virtualizes the network to create multiple tenant networks?",
               [("VXLAN", False), ("Virtual Chassis", False), ("Routing instances", True), ("VLANs", False)],
               "Routing instances create separate routing tables, enabling multi-tenant network virtualization.",
               "DC Platforms", 25.0, 2, "understand"),
        make_q("jncia-dc", "Which protocol provides neighbor discovery in a data center fabric?",
               [("CDP", False), ("LLDP", True), ("VTP", False), ("DTP", False)],
               "LLDP discovers directly connected neighbors and their capabilities in a data center fabric.",
               "DC Architecture", 25.0, 1, "remember"),
        make_q("jncia-dc", "Which feature allows a switch to appear as a single logical device?",
               [("Virtual Chassis", True), ("VRRP", False), ("LACP", False), ("MSTP", False)],
               "Virtual Chassis allows multiple Junos switches to operate and manage as a single logical device.",
               "DC Platforms", 25.0, 2, "understand"),
        make_q("jncia-dc", "Which command shows VLAN membership on a QFX switch?",
               [("show vlans", True), ("show vlan", False),
                ("show ethernet-switching vlan", False), ("show bridge vlan", False)],
               "'show vlans' displays VLAN membership and associated interfaces on Junos.",
               "Layer 2", 25.0, 1, "apply"),
        make_q("jncia-dc", "Which overlay technology uses UDP port 4789?",
               [("GRE", False), ("VXLAN", True), ("MPLS", False), ("IPsec", False)],
               "VXLAN encapsulates Layer 2 frames in UDP packets using destination port 4789.",
               "Overlays", 25.0, 2, "remember"),
        make_q("jncia-dc", "Which command displays interfaces and their VLAN tagging mode?",
               [("show interfaces terse", False), ("show ethernet-switching interfaces", True),
                ("show vlans detail", False), ("show interfaces extensive", False)],
               "'show ethernet-switching interfaces' displays switching interfaces and their VLAN modes.",
               "Layer 2", 25.0, 2, "apply"),
        make_q("jncia-dc", "Which data center design principle reduces failure domains?",
               [("Large Layer 2 domains", False), ("Small, modular pods", True),
                ("Single-homed servers", False), ("Flat networks", False)],
               "Small, modular pods reduce failure domains and improve scalability.",
               "DC Architecture", 25.0, 2, "understand"),
        make_q("jncia-dc", "Which protocol is used to automatically assign IP addresses to servers?",
               [("DNS", False), ("DHCP", True), ("NTP", False), ("SNMP", False)],
               "DHCP automatically assigns IP addresses and configuration to servers.",
               "DC Platforms", 25.0, 1, "remember"),
        make_q("jncia-dc", "Which command shows the Virtual Chassis status?",
               [("show virtual-chassis", True), ("show chassis vc", False),
                ("show vc status", False), ("show virtual-chassis status", False)],
               "'show virtual-chassis' displays the status and roles of members in a Virtual Chassis.",
               "DC Platforms", 25.0, 2, "apply"),
        make_q("jncia-dc", "Which Junos feature provides redundant gateway functionality for servers?",
               [("VRRP", True), ("LACP", False), ("RSTP", False), ("VXLAN", False)],
               "VRRP provides redundant default gateway functionality for servers.",
               "DC Architecture", 25.0, 2, "understand"),

        # Extended JNCIA-AUT
        make_q("jncia-aut", "Which automation tool uses a push-based agentless architecture?",
               [("Ansible", True), ("Puppet", False), ("Chef", False), ("SaltStack", False)],
               "Ansible uses SSH/NETCONF and is agentless and push-based.",
               "Automation Tools", 25.0, 2, "understand"),
        make_q("jncia-aut", "Which language are Junos commit/op/event scripts traditionally written in?",
               [("Python", False), ("SLAX", True), ("YAML", False), ("Ruby", False)],
               "Junos traditionally supports SLAX and XSLT for on-box scripts. Python is also supported.",
               "On-box Automation", 25.0, 2, "remember"),
        make_q("jncia-aut", "Which NETCONF operation modifies configuration data?",
               [("<get-config>", False), ("<edit-config>", True), ("<copy-config>", False), ("<close-session>", False)],
               "<edit-config> modifies the device configuration.",
               "NETCONF/YANG", 25.0, 1, "remember"),
        make_q("jncia-aut", "Which data format uses indentation for structure and is human-readable?",
               [("XML", False), ("JSON", False), ("YAML", True), ("CSV", False)],
               "YAML uses indentation and is commonly used for Ansible playbooks.",
               "Automation Tools", 25.0, 1, "remember"),
        make_q("jncia-aut", "Which REST API method updates an existing resource?",
               [("GET", False), ("POST", False), ("PUT", True), ("DELETE", False)],
               "PUT updates existing resources. POST creates, GET retrieves, DELETE removes.",
               "REST APIs", 25.0, 1, "remember"),
        make_q("jncia-aut", "Which Junos feature triggers scripts based on system events?",
               [("Op scripts", False), ("Event scripts", True), ("Commit scripts", False), ("SNMP scripts", False)],
               "Event scripts are triggered by system events such as syslog messages or SNMP traps.",
               "On-box Automation", 25.0, 2, "understand"),
        make_q("jncia-aut", "Which Python library is commonly used to automate Junos devices?",
               [("Netmiko", False), ("PyEZ", True), ("NAPALM", False), ("Paramiko", False)],
               "PyEZ is the official Juniper Python library for automating Junos devices.",
               "Automation Tools", 25.0, 1, "remember"),
        make_q("jncia-aut", "Which YANG statement groups related leafs into a named container?",
               [("leaf", False), ("container", True), ("list", False), ("module", False)],
               "A 'container' groups related nodes in YANG without implying presence in data.",
               "YANG", 25.0, 2, "understand"),
        make_q("jncia-aut", "Which HTTP status code indicates an unauthorized request?",
               [("401", True), ("403", False), ("404", False), ("500", False)],
               "HTTP 401 Unauthorized indicates authentication is required or failed.",
               "REST APIs", 25.0, 1, "remember"),
        make_q("jncia-aut", "Which operation retrieves operational state data via NETCONF?",
               [("<get-config>", False), ("<get>", True), ("<edit-config>", False), ("<copy-config>", False)],
               "<get> retrieves operational state data, while <get-config> retrieves configuration.",
               "NETCONF/YANG", 25.0, 2, "remember"),

        # Extended JNCIP-SEC
        make_q("jncip-sec", "Which SRX feature provides centralized logging and reporting?",
               [("J-Web", False), ("Junos Space Security Director", True), ("CLI", False), ("Syslog", False)],
               "Junos Space Security Director provides centralized logging, reporting, and policy management.",
               "Management", 15.0, 2, "understand"),
        make_q("jncip-sec", "Which IKE phase negotiates IPsec SAs?",
               [("Phase 1", False), ("Phase 2", True), ("Phase 3", False), ("Quick mode", False)],
               "IKE Phase 2 negotiates IPsec SAs and security parameters. Phase 1 establishes the IKE SA.",
               "IPsec VPNs", 15.0, 2, "understand"),
        make_q("jncip-sec", "Which SRX high-availability mode synchronizes all sessions?",
               [("Active/Passive", False), ("Active/Active full mesh", False), ("Active/Active", True), ("Standalone", False)],
               "Active/Active chassis cluster synchronizes sessions and allows both nodes to forward traffic.",
               "High Availability", 15.0, 3, "understand"),
        make_q("jncip-sec", "Which command shows chassis cluster status?",
               [("show chassis cluster status", True), ("show cluster status", False),
                ("show high-availability status", False), ("show redundancy", False)],
               "'show chassis cluster status' displays node status, priority, and redundancy group states.",
               "High Availability", 15.0, 2, "apply"),
        make_q("jncip-sec", "Which UTM feature filters websites by category?",
               [("Antivirus", False), ("Web filtering", True), ("Antispam", False), ("IDP", False)],
               "Web filtering controls access to websites based on categories and reputation.",
               "UTM", 10.0, 1, "understand"),
        make_q("jncip-sec", "Which security policy action allows traffic?",
               [("deny", False), ("permit", True), ("reject", False), ("discard", False)],
               "The 'permit' action allows traffic matching a security policy.",
               "Security Policies", 15.0, 1, "remember"),
        make_q("jncip-sec", "Which feature authenticates users before applying security policies?",
               [("User Firewall", True), ("Screens", False), ("NAT", False), ("VPN", False)],
               "User Firewall integrates with Active Directory or other identity sources to authenticate users.",
               "Access Control", 15.0, 2, "understand"),
        make_q("jncip-sec", "Which command displays IKE security associations?",
               [("show security ike security-associations", True), ("show ike sa", False),
                ("show security ipsec sa", False), ("show vpn ike", False)],
               "'show security ike security-associations' displays active IKE Phase 1 SAs.",
               "IPsec VPNs", 15.0, 2, "apply"),
        make_q("jncip-sec", "Which Junos feature provides geolocation-based policy enforcement?",
               [("AppID", False), ("GeoIP", True), ("UTM", False), ("IDP", False)],
               "GeoIP identifies traffic by source/destination country and enables location-based policies.",
               "Advanced Security", 15.0, 2, "understand"),
        make_q("jncip-sec", "Which command shows security policy hit counts?",
               [("show security policies hit-count", True), ("show security hit-count", False),
                ("show policy hits", False), ("show security flow hits", False)],
               "'show security policies hit-count' displays how many times each policy matched traffic.",
               "Security Policies", 15.0, 2, "apply"),

        # Extended JNCIP-DC
        make_q("jncip-dc", "Which EVPN route type provides inclusive multicast for BUM traffic?",
               [("Type 1", False), ("Type 2", False), ("Type 3", True), ("Type 4", False)],
               "EVPN Type 3 routes carry inclusive multicast routes for BUM traffic forwarding.",
               "EVPN", 15.0, 2, "remember"),
        make_q("jncip-dc", "Which VXLAN component maps VNIs to VLANs?",
               [("VTEP", False), ("VNID", False), ("VLAN-to-VNI mapping", True), ("Bridge domain", False)],
               "VXLAN VLAN-to-VNI mapping associates customer VLANs with VXLAN Network Identifiers.",
               "VXLAN", 15.0, 2, "understand"),
        make_q("jncip-dc", "Which protocol is commonly used for underlay routing in data center fabrics?",
               [("OSPF", False), ("IS-IS", False), ("EBGP", True), ("RIP", False)],
               "EBGP is commonly used for underlay routing in EVPN-VXLAN data center fabrics.",
               "Underlay", 15.0, 2, "understand"),
        make_q("jncip-dc", "Which command displays EVPN neighbors?",
               [("show evpn neighbors", False), ("show evpn instance", False),
                ("show bgp summary", False), ("show evpn overview", True)],
               "'show evpn overview' displays EVPN instance state and neighbor information.",
               "EVPN", 15.0, 2, "apply"),
        make_q("jncip-dc", "Which feature provides redundant active-active gateway for EVPN?",
               [("VRRP", False), ("EVPN multihoming", True), ("MC-LAG", False), ("RSTP", False)],
               "EVPN multihoming provides all-active redundant gateway functionality.",
               "EVPN Multihoming", 15.0, 2, "understand"),
        make_q("jncip-dc", "Which command shows VXLAN interface statistics?",
               [("show interfaces vxlan statistics", True), ("show vxlan statistics", False),
                ("show route vxlan", False), ("show evpn vxlan", False)],
               "'show interfaces vxlan statistics' displays packet counters on VXLAN interfaces.",
               "VXLAN", 15.0, 2, "apply"),
        make_q("jncip-dc", "Which data center switching feature allows remote management out-of-band?",
               [("RE management interface", True), ("Console port", False), ("FPC", False), ("PIC", False)],
               "The dedicated management interface (fxp0 or em0) provides out-of-band management.",
               "DC Platforms", 15.0, 1, "understand"),
        make_q("jncip-dc", "Which protocol discovers VTEP tunnel endpoints in EVPN-VXLAN?",
               [("BGP EVPN", True), ("LDP", False), ("RSVP", False), ("IS-IS", False)],
               "BGP EVPN advertises MAC/IP reachability and VTEP information for VXLAN tunnels.",
               "EVPN", 15.0, 2, "understand"),
        make_q("jncip-dc", "Which command displays the MAC table in an EVPN instance?",
               [("show evpn mac-table", True), ("show ethernet-switching table", False),
                ("show route evpn", False), ("show evpn route", False)],
               "'show evpn mac-table' displays MAC addresses learned in EVPN instances.",
               "EVPN", 15.0, 2, "apply"),
        make_q("jncip-dc", "Which feature reduces STP dependency in modern data center fabrics?",
               [("EVPN split horizon", True), ("VTP", False), ("DTP", False), ("PAgP", False)],
               "EVPN split horizon and all-active multihoming reduce the need for STP in data center fabrics.",
               "EVPN", 15.0, 2, "understand"),

        # Extended JNCIP-AUT
        make_q("jncip-aut", "Which NETCONF capability supports confirmed commits?",
               [(":candidate", False), (":confirmed-commit", True), (":rollback-on-error", False), (":validate", False)],
               "The :confirmed-commit capability allows a commit to be automatically rolled back unless confirmed.",
               "NETCONF", 15.0, 3, "understand"),
        make_q("jncip-aut", "Which YANG statement defines a list of entries with keys?",
               [("container", False), ("leaf", False), ("list", True), ("grouping", False)],
               "A YANG 'list' defines a sequence of entries identified by keys.",
               "YANG", 15.0, 2, "understand"),
        make_q("jncip-aut", "Which Junos automation tool uses declarative HCL?",
               [("Ansible", False), ("Terraform", True), ("PyEZ", False), ("SaltStack", False)],
               "Terraform uses HashiCorp Configuration Language (HCL) for declarative infrastructure provisioning.",
               "Off-box Automation", 15.0, 1, "remember"),
        make_q("jncip-aut", "Which REST API status code indicates a bad request?",
               [("401", False), ("403", False), ("404", False), ("400", True)],
               "HTTP 400 Bad Request indicates the server cannot process the request due to client error.",
               "REST APIs", 15.0, 1, "remember"),
        make_q("jncip-aut", "Which NETCONF operation validates configuration without applying it?",
               [("<validate>", True), ("<commit>", False), ("<edit-config>", False), ("<copy-config>", False)],
               "<validate> checks configuration correctness without committing it.",
               "NETCONF", 15.0, 2, "remember"),
        make_q("jncip-aut", "Which Python library abstracts multiple network vendors?",
               [("PyEZ", False), ("NAPALM", True), ("Netmiko", False), ("Paramiko", False)],
               "NAPALM provides a vendor-abstracted API for managing network devices from multiple vendors.",
               "Off-box Automation", 15.0, 2, "understand"),
        make_q("jncip-aut", "Which YANG statement imports definitions from another module?",
               [("include", False), ("import", True), ("uses", False), ("augment", False)],
               "The 'import' statement brings in definitions from another YANG module.",
               "YANG", 15.0, 3, "remember"),
        make_q("jncip-aut", "Which REST API method partially updates a resource?",
               [("PUT", False), ("PATCH", True), ("POST", False), ("DELETE", False)],
               "PATCH applies partial modifications to a resource.",
               "REST APIs", 15.0, 2, "remember"),
        make_q("jncip-aut", "Which Junos feature allows scripts to run in response to configuration commits?",
               [("Op scripts", False), ("Event scripts", False), ("Commit scripts", True), ("SNMP scripts", False)],
               "Commit scripts run during the commit process and can modify or validate configuration.",
               "On-box Automation", 15.0, 2, "understand"),
        make_q("jncip-aut", "Which protocol does NETCONF run over by default?",
               [("TCP", False), ("UDP", False), ("SSH", True), ("TLS", False)],
               "NETCONF typically runs over SSH on port 830 by default.",
               "NETCONF", 15.0, 1, "remember"),
    ]

    # Add extra questions from companion generator
    from generate_juniper_others_extra import generate_all as generate_extra
    questions += generate_extra()

    return questions


def questions_to_sql(questions: list[dict]) -> str:
    exam_ids = ",".join(f"'{EXAMS[e]['exam_id']}'" for e in EXAMS)
    lines = [
        "-- +goose Up",
        "-- +goose StatementBegin",
        "",
        "-- Juniper remaining exams question bank",
        f"-- Generated {len(questions)} blueprint-aligned single-choice questions",
        "",
        f"DELETE FROM questions WHERE exam_id IN ({exam_ids});",
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
        f"DELETE FROM questions WHERE exam_id IN ({exam_ids});",
        "",
        "-- +goose StatementEnd",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    questions = generate_all()
    print(questions_to_sql(questions))
