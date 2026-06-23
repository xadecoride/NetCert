#!/usr/bin/env python3
"""
NetCert — JNCIS (ENT, SP, SEC, DC, AUT) and JNCIA-Cloud question generator.
"""
import hashlib
import json
import uuid

EXAMS = {
    "jncis-ent": {"exam_id": "b0000000-0000-0000-0000-000000000012", "track_id": "a0000000-0000-0000-0000-000000000001", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-ent.html"},
    "jncis-sp":  {"exam_id": "b0000000-0000-0000-0000-000000000014", "track_id": "a0000000-0000-0000-0000-000000000002", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-sp.html"},
    "jncis-sec": {"exam_id": "b0000000-0000-0000-0000-000000000025", "track_id": "a0000000-0000-0000-0000-000000000003", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-sec.html"},
    "jncis-dc":  {"exam_id": "b0000000-0000-0000-0000-000000000027", "track_id": "a0000000-0000-0000-0000-000000000004", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-dc.html"},
    "jncis-aut": {"exam_id": "b0000000-0000-0000-0000-000000000029", "track_id": "a0000000-0000-0000-0000-000000000005", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncis-automation.html"},
    "jncia-cloud": {"exam_id": "b0000000-0000-0000-0000-000000000030", "track_id": "a0000000-0000-0000-0000-000000000007", "url": "https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-cloud.html"},
}


def qid(exam: str, seed: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_OID, f"{exam}:{seed}"))


def content_hash(body: str, correct: str) -> str:
    return hashlib.sha256(f"{body}::{correct}".encode()).hexdigest()[:16]


def make_q(exam: str, body: str, options: list[tuple[str, bool]], explanation: str,
           section: str, weight: float, difficulty: int = 2,
           bloom: str = "understand", qtype: str = "single-choice") -> dict:
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
        "question_type": qtype,
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
    # JNCIS-ENT
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncis-ent", "Which Junos protocol preference value is used for OSPF internal routes by default?",
               [("10", False), ("150", False), ("10", False), ("110", True)],
               "Junos default protocol preference for OSPF internal routes is 110.",
               "OSPF", 20.0, 2, "remember"),
        make_q("jncis-ent", "What is the default OSPF reference-bandwidth on Junos?",
               [("100 Mbps", True), ("1 Gbps", False), ("10 Gbps", False), ("100 Gbps", False)],
               "The default OSPF reference-bandwidth in Junos is 100 Mbps, which can cause incorrect cost on high-speed links.",
               "OSPF", 20.0, 2, "remember"),
        make_q("jncis-ent", "Which BGP well-known discretionary attribute is used to influence outbound traffic?",
               [("MED", False), ("Local Preference", True), ("Origin", False), ("AS Path", False)],
               "Local Preference is a well-known discretionary attribute that influences outbound traffic from an AS.",
               "BGP", 20.0, 2, "understand"),
        make_q("jncis-ent", "In Junos, which command displays the BGP routes received from a specific neighbor?",
               [("show route receive-protocol bgp <neighbor>", True),
                ("show bgp neighbor <neighbor> routes", False),
                ("show route protocol bgp", False),
                ("show bgp summary", False)],
               "'show route receive-protocol bgp <neighbor>' displays routes received from a specific BGP peer.",
               "BGP", 20.0, 2, "apply"),
        make_q("jncis-ent", "Which spanning-tree protocol is the IEEE standard that allows multiple spanning trees per VLAN?",
               [("RSTP", False), ("MSTP", True), ("VSTP", False), ("STP", False)],
               "MSTP (802.1s) maps VLANs to multiple spanning-tree instances. VSTP is Juniper per-VLAN.",
               "Layer 2", 15.0, 2, "understand"),
        make_q("jncis-ent", "In an EVPN-VXLAN campus fabric, which device typically acts as the VTEP?",
               [("Core router", False), ("Access switch or satellite device", True), ("DHCP server", False), ("Firewall", False)],
               "In EVPN-VXLAN fabrics, access switches or satellite devices commonly act as VTEPs.",
               "EVPN/VXLAN", 15.0, 3, "understand"),
        make_q("jncis-ent", "Which CoS scheduling method services queues in a strict priority order before others?",
               [("Weighted round-robin", False), ("Strict-high priority", True), ("Random early detection", False), ("Tail drop", False)],
               "Strict-high priority queues are serviced before other queues, useful for voice/video.",
               "CoS", 10.0, 2, "understand"),
        make_q("jncis-ent", "Which Junos command verifies which interfaces are participating in a LAG?",
               [("show lacp interfaces", True), ("show interfaces ae0 extensive", False),
                ("show ethernet-switching interfaces", False), ("show chassis cluster interfaces", False)],
               "'show lacp interfaces' displays LACP member interfaces and their states.",
               "Layer 2", 15.0, 2, "apply"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIS-SP
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncis-sp", "Which protocol distributes MPLS labels without traffic engineering extensions?",
               [("RSVP", False), ("LDP", True), ("BGP", False), ("IS-IS", False)],
               "LDP is used for label distribution in MPLS networks without TE.",
               "MPLS", 25.0, 2, "understand"),
        make_q("jncis-sp", "What is the purpose of Penultimate Hop Popping (PHP) in MPLS?",
               [("To add an additional label at the egress", False),
                ("To remove the outer label before the egress PE", True),
                ("To encrypt MPLS packets", False),
                ("To signal TE tunnels", False)],
               "PHP removes the MPLS label at the penultimate hop, reducing egress PE label lookup burden.",
               "MPLS", 25.0, 2, "understand"),
        make_q("jncis-sp", "Which RSVP object is used to reserve bandwidth along an LSP path?",
               [("Sender TSpec", True), ("Record Route", False), ("Session", False), ("Hello", False)],
               "The Sender TSpec object in RSVP Path messages describes traffic characteristics and bandwidth requirements.",
               "MPLS Traffic Engineering", 20.0, 3, "understand"),
        make_q("jncis-sp", "Which IS-IS TLV carries Segment Routing Global Block (SRGB) information?",
               [("IS reachability", False), ("Extended IP reachability", False), ("SR-Capability sub-TLV", True), ("Hostname", False)],
               "SR-Capability sub-TLV advertises SRGB and algorithms for Segment Routing.",
               "IS-IS / Segment Routing", 15.0, 3, "remember"),
        make_q("jncis-sp", "In BGP, which attribute is prepended to influence inbound traffic from peers?",
               [("Local Preference", False), ("MED", False), ("AS Path", True), ("Community", False)],
               "AS Path prepending makes routes less preferred for inbound traffic by making the AS path longer.",
               "BGP", 20.0, 2, "understand"),
        make_q("jncis-sp", "Which LDP neighbor discovery mode does not use multicast hello messages?",
               [("Basic discovery", False), ("Extended discovery", True), ("Targeted discovery", False), ("Passive discovery", False)],
               "LDP extended discovery uses targeted Hellos (unicast) to discover non-directly connected peers.",
               "MPLS", 20.0, 3, "understand"),
        make_q("jncis-sp", "What is the default IS-IS level on Junos for loopback and point-to-point interfaces?",
               [("Level 1 only", False), ("Level 2 only", False), ("Level 1/2", True), ("No level", False)],
               "Junos IS-IS interfaces are level 1/2 by default.",
               "IS-IS", 15.0, 2, "remember"),
        make_q("jncis-sp", "Which MPLS application uses BGP labeled unicast to build transport tunnels?",
               [("L2VPN", False), ("L3VPN", False), ("Segment Routing with BGP LU", True), ("VPLS", False)],
               "BGP labeled unicast (BGP-LU) advertises labeled prefixes for Segment Routing or inter-AS transport.",
               "MPLS", 20.0, 3, "understand"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIS-SEC
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncis-sec", "Which SRX feature identifies applications by inspecting Layer 7 traffic?",
               [("AppID", True), ("IPS", False), ("UTM", False), ("Screen", False)],
               "AppID identifies applications using Layer 7 signatures and heuristics.",
               "AppSecure", 15.0, 2, "understand"),
        make_q("jncis-sec", "In an SRX chassis cluster, which interface type is used for control-plane communication?",
               [("Fab", False), ("Control link", True), ("Data link", False), ("Management", False)],
               "The control link carries control-plane traffic between cluster nodes.",
               "High Availability", 15.0, 2, "remember"),
        make_q("jncis-sec", "Which Junos security policy action permits traffic and logs session close?",
               [("permit", False), ("deny", False), ("permit log", False), ("permit count", True)],
               "'permit count' permits traffic and counts/log session information. Logging options include session-init and session-close separately.",
               "Security Policies", 20.0, 3, "understand"),
        make_q("jncis-sec", "Which NAT type on SRX translates the source IP of many internal hosts to one external IP?",
               [("Static NAT", False), ("Destination NAT", False), ("Source NAT with PAT", True), ("Twice NAT", False)],
               "Source NAT with port translation (PAT) maps multiple private addresses to one public IP.",
               "NAT", 20.0, 2, "understand"),
        make_q("jncis-sec", "Which IPS action drops the current packet and all subsequent packets in the session?",
               [("Drop packet", False), ("Drop connection", True), ("Ignore", False), ("Mark DSCP", False)],
               "Drop connection blocks the entire session, not just the offending packet.",
               "IPS", 15.0, 2, "understand"),
        make_q("jncis-sec", "Which Screen option mitigates TCP SYN flood attacks?",
               [("IP spoofing", False), ("SYN flood protection", True), ("Port scan", False), ("Session limit", False)],
               "The SYN flood Screen option detects and mitigates TCP SYN flood attacks.",
               "Screens", 15.0, 2, "understand"),
        make_q("jncis-sec", "Which SSL proxy feature decrypts outbound HTTPS traffic for inspection?",
               [("SSL VPN", False), ("SSL Forward Proxy", True), ("Destination NAT", False), ("AppQoS", False)],
               "SSL Forward Proxy decrypts outbound SSL/TLS traffic for UTM/IPS inspection.",
               "SSL Proxy", 15.0, 3, "understand"),
        make_q("jncis-sec", "Which command displays current security policy hits on an SRX?",
               [("show security policies hit-count", True),
                ("show security flow session", False),
                ("show configuration security policies", False),
                ("show security zones", False)],
               "'show security policies hit-count' displays policy match counters.",
               "Security Policies", 15.0, 2, "apply"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIS-DC
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncis-dc", "Which EVPN route type is used for broadcast, unknown unicast, and multicast (BUM) traffic?",
               [("Type 1", True), ("Type 2", False), ("Type 3", False), ("Type 5", False)],
               "EVPN Type 1 routes carry Ethernet auto-discovery (A-D) per ES and per EVI, used for BUM split-horizon.",
               "EVPN", 20.0, 3, "understand"),
        make_q("jncis-dc", "In a VXLAN-EVPN fabric, what does the VNI identify?",
               [("A tenant VRF", False), ("A Layer 2 segment or Layer 3 VRF", True), ("A BGP neighbor", False), ("A physical link", False)],
               "VXLAN Network Identifier (VNI) identifies a Layer 2 segment (VLAN) or Layer 3 VRF in EVPN-VXLAN.",
               "VXLAN", 20.0, 2, "understand"),
        make_q("jncis-dc", "Which Junos feature provides active-active multihoming at the Layer 2 edge in EVPN?",
               [("MC-LAG", False), ("EVPN multihoming (EVI-ES)", True), ("VRRP", False), ("LACP", False)],
               "EVPN multihoming (All-Active) provides active-active L2 multihoming via Ethernet Segments.",
               "EVPN", 20.0, 3, "understand"),
        make_q("jncis-dc", "What is the primary control-plane protocol for EVPN route exchange?",
               [("OSPF", False), ("IS-IS", False), ("MP-BGP", True), ("LDP", False)],
               "EVPN routes are carried in BGP using MP_REACH_NLRI with EVPN address family.",
               "EVPN", 20.0, 2, "understand"),
        make_q("jncis-dc", "Which QFabric component acts as the central routing and switching backplane?",
               [("Node device", False), ("Interconnect device", True), ("Director group", False), ("Fabric manager", False)],
               "Interconnect devices in QFabric provide the central backplane fabric.",
               "QFabric", 10.0, 2, "remember"),
        make_q("jncis-dc", "In a Contrail SDN environment, which component stores the network state?",
               [("vRouter", False), ("Config node", False), ("Cassandra", True), ("OpenStack Nova", False)],
               "Contrail uses Cassandra as the NoSQL database for network state and analytics.",
               "Contrail", 10.0, 2, "remember"),
        make_q("jncis-dc", "Which protocol does Junos use for Zero Touch Provisioning (ZTP) in a data center?",
               [("NETCONF", False), ("DHCP/HTTP/FTP", True), ("TFTP only", False), ("SNMP", False)],
               "ZTP uses DHCP options to locate an image and configuration file via HTTP/FTP/TFTP.",
               "Provisioning", 10.0, 2, "understand"),
        make_q("jncis-dc", "Which feature allows two QFX switches to appear as a single logical device?",
               [("Virtual Chassis", True), ("MC-LAG", False), ("EVPN", False), ("VRF", False)],
               "Virtual Chassis combines multiple switches into one logical device with a single control plane.",
               "Virtual Chassis", 10.0, 2, "understand"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIS-AUT
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncis-aut", "Which Python library is commonly used for NETCONF connections to Junos?",
               [("Paramiko", False), ("ncclient", True), ("Requests", False), ("Scapy", False)],
               "ncclient is the standard Python library for NETCONF clients.",
               "NETCONF", 20.0, 1, "remember"),
        make_q("jncis-aut", "In Ansible, which module is used to deploy Junos configurations?",
               [("junos_config", True), ("ios_config", False), ("netconf_config", False), ("template", False)],
               "The junos_config module manages Junos configurations via NETCONF.",
               "Ansible", 20.0, 1, "remember"),
        make_q("jncis-aut", "Which data modeling language is used by NETCONF/RESTCONF for configuration?",
               [("JSON", False), ("XML", False), ("YANG", True), ("YAML", False)],
               "YANG is the data modeling language used with NETCONF and RESTCONF.",
               "Automation Concepts", 15.0, 1, "remember"),
        make_q("jncis-aut", "Which Junos command enters configuration mode and allows private candidate configuration?",
               [("configure", False), ("configure private", True), ("configure exclusive", False), ("edit", False)],
               "'configure private' creates a private candidate configuration without locking the global database.",
               "Junos Automation", 15.0, 2, "apply"),
        make_q("jncis-aut", "What is the default NETCONF port on Junos?",
               [("22", False), ("830", True), ("443", False), ("80", False)],
               "NETCONF over SSH uses port 830 by default on Junos.",
               "NETCONF", 20.0, 1, "remember"),
        make_q("jncis-aut", "In SaltStack, which component runs on the managed Junos device?",
               [("Master", False), ("Minion", False), ("Proxy minion", True), ("Syndic", False)],
               "Junos devices use Salt proxy minions because they cannot run a native minion.",
               "SaltStack", 10.0, 2, "understand"),
        make_q("jncis-aut", "Which REST API HTTP method is used to replace a complete resource?",
               [("POST", False), ("PUT", True), ("PATCH", False), ("GET", False)],
               "PUT replaces the entire resource, while PATCH applies partial updates.",
               "REST API", 10.0, 2, "understand"),
        make_q("jncis-aut", "Which Junos feature allows on-box scripts written in SLAX or XSLT?",
               [("Op scripts", True), ("Ansible playbooks", False), ("Python scripts", False), ("Event policies", False)],
               "Junos op scripts can be written in SLAX or XSLT and run on the device.",
               "Junos Automation", 10.0, 2, "understand"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # JNCIA-Cloud
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("jncia-cloud", "Which Juniper SDN controller is used to manage cloud and data center networks?",
               [("Junos Space", False), ("Contrail Networking", True), ("NorthStar", False), ("CSO", False)],
               "Contrail Networking is Juniper's SDN controller for cloud and data center.",
               "Contrail", 25.0, 1, "remember"),
        make_q("jncia-cloud", "What does NFV stand for?",
               [("Network Function Virtualization", True),
                ("Network Fabric Virtualization", False),
                ("Network Forwarding Virtualization", False),
                ("Node Function Virtualization", False)],
               "NFV virtualizes network functions such as firewalls, routers, and load balancers.",
               "Cloud Concepts", 20.0, 1, "remember"),
        make_q("jncia-cloud", "In a public cloud, who is responsible for securing the operating system on IaaS?",
               [("Cloud provider", False), ("Customer", True), ("Shared equally", False), ("Managed service provider", False)],
               "In IaaS, the customer is responsible for guest OS and application security (shared responsibility model).",
               "Cloud Concepts", 20.0, 2, "understand"),
        make_q("jncia-cloud", "Which protocol is commonly used for overlay networks in cloud data centers?",
               [("MPLS LDP", False), ("VXLAN", True), ("GRE", False), ("L2TP", False)],
               "VXLAN is widely used for Layer 2 overlay networks in cloud data centers.",
               "Overlay Networking", 20.0, 2, "understand"),
        make_q("jncia-cloud", "Which Contrail component runs as a virtual router on compute nodes?",
               [("vRouter", True), ("Config node", False), ("Control node", False), ("Analytics node", False)],
               "Contrail vRouter runs on compute nodes and forwards tenant traffic.",
               "Contrail", 15.0, 1, "remember"),
        make_q("jncia-cloud", "What is a tenant in a cloud environment?",
               [("A physical data center", False),
                ("An isolated logical grouping of resources", True),
                ("A single hypervisor", False),
                ("A management network", False)],
               "A tenant is a logical isolation boundary for resources in a multi-tenant cloud.",
               "Cloud Concepts", 10.0, 1, "understand"),
        make_q("jncia-cloud", "Which service model provides ready-to-use applications over the internet?",
               [("IaaS", False), ("PaaS", False), ("SaaS", True), ("DaaS", False)],
               "SaaS delivers complete applications to end users.",
               "Cloud Service Models", 10.0, 1, "remember"),
    ]

    return questions


def questions_to_sql(questions: list[dict]) -> str:
    exam_ids = ",".join(f"'{EXAMS[e]['exam_id']}'" for e in EXAMS)
    lines = [
        "-- +goose Up",
        "-- +goose StatementBegin",
        "",
        "-- JNCIS and JNCIA-Cloud question bank",
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
