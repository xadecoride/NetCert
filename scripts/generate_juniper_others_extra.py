#!/usr/bin/env python3
"""
NetCert — additional questions for Juniper remaining exams.
Targets JNCIA-SP/SEC/DC/AUT and JNCIP-SEC/DC/AUT to reach 30-50+ questions each.
Adds subnetting, troubleshooting, and CLI-focused questions.
"""
import hashlib
import json
import random
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
    return str(uuid.uuid5(uuid.NAMESPACE_OID, f"{exam}-extra:{seed}"))


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


def generate_subnetting(exam: str, count: int) -> list[dict]:
    out = []
    random.seed(hash(exam) % 2**32)
    for _ in range(count):
        network = random.choice(["10.0", "172.16", "192.168", "203.0.113"])
        host = random.randint(1, 240)
        prefix = random.choice([24, 25, 26, 27, 28, 29, 30])
        block = 2 ** (32 - prefix)
        net = (host // block) * block
        bcast = net + block - 1
        first = net + 1
        last = bcast - 1
        qtype = random.choice(["first", "last", "bcast", "hosts"])
        if qtype == "first":
            body = f"What is the first valid host address in {network}.{host}/{prefix}?"
            correct = f"{network}.{first}"
            opts = [f"{network}.{net}", f"{network}.{first}", f"{network}.{last}", f"{network}.{bcast}"]
        elif qtype == "last":
            body = f"What is the last valid host address in {network}.{host}/{prefix}?"
            correct = f"{network}.{last}"
            opts = [f"{network}.{net}", f"{network}.{first}", f"{network}.{last}", f"{network}.{bcast}"]
        elif qtype == "bcast":
            body = f"What is the broadcast address for {network}.{host}/{prefix}?"
            correct = f"{network}.{bcast}"
            opts = [f"{network}.{net}", f"{network}.{first}", f"{network}.{last}", f"{network}.{bcast}"]
        else:
            hosts = block - 2
            body = f"How many usable host addresses are in a /{prefix} subnet?"
            correct = str(hosts)
            opts = [str(hosts - 1), str(hosts), str(hosts + 1), str(block)]
        random.shuffle(opts)
        options = [(o, o == correct) for o in opts]
        explanation = f"For /{prefix}, block size is {block}; network={network}.{net}, broadcast={network}.{bcast}, usable hosts={block-2}."
        out.append(make_q(exam, body, options, explanation, "Subnetting", 10.0, 2, "apply"))
    random.seed()
    return out


def generate_all() -> list[dict]:
    questions: list[dict] = []

    # Subnetting for all JNCIA exams
    for exam in ["jncia-sp", "jncia-sec", "jncia-dc", "jncia-aut"]:
        questions += generate_subnetting(exam, 8)

    # JNCIA-SP additional
    questions += [
        make_q("jncia-sp", "Which command displays the IS-IS routing table?",
               [("show isis route", True), ("show route isis", False), ("show isis database", False), ("show isis topology", False)],
               "'show isis route' displays the IS-IS routing table.", "IGP Fundamentals", 20.0, 1, "apply"),
        make_q("jncia-sp", "Which BGP message opens the peer session?",
               [("Open", True), ("Update", False), ("Keepalive", False), ("Notification", False)],
               "BGP Open messages establish the session and exchange parameters.", "BGP Fundamentals", 20.0, 1, "remember"),
        make_q("jncia-sp", "Which command shows RSVP session details?",
               [("show rsvp session", True), ("show rsvp neighbor", False), ("show mpls rsvp", False), ("show rsvp lsp", False)],
               "'show rsvp session' displays RSVP-signaled sessions including LSPs.", "MPLS Fundamentals", 20.0, 2, "apply"),
        make_q("jncia-sp", "Which Junos command verifies LDP interface status?",
               [("show ldp interface", True), ("show ldp session", False), ("show mpls ldp", False), ("show interface ldp", False)],
               "'show ldp interface' displays interfaces where LDP is enabled.", "MPLS Fundamentals", 20.0, 1, "apply"),
        make_q("jncia-sp", "Which multicast protocol is router-to-router?",
               [("IGMP", False), ("PIM", True), ("MSDP", False), ("MBGP", False)],
               "PIM is used between routers to build multicast distribution trees.", "Multicast", 10.0, 1, "remember"),
        make_q("jncia-sp", "Which command displays the forwarding table?",
               [("show route forwarding-table", True), ("show forwarding-table", False), ("show route table", False), ("show fpc table", False)],
               "'show route forwarding-table' displays the forwarding table.", "Troubleshooting", 10.0, 1, "apply"),
        make_q("jncia-sp", "Which OSPF state indicates bidirectional communication?",
               [("Init", False), ("2-Way", True), ("Exchange", False), ("Full", False)],
               "2-Way state means the router has received a Hello from the neighbor.", "IGP Fundamentals", 20.0, 2, "understand"),
    ]

    # JNCIA-SEC additional
    questions += [
        make_q("jncia-sec", "Which SRX feature matches traffic to applications for policy enforcement?",
               [("AppID", True), ("IDP", False), ("Screens", False), ("UTM", False)],
               "AppID identifies applications and enables application-based security policies.", "Advanced Security", 25.0, 2, "understand"),
        make_q("jncia-sec", "Which command shows security policy counters?",
               [("show security policies", True), ("show security flow session", False), ("show security zones", False), ("show security match", False)],
               "'show security policies' displays policies and hit counts.", "Security Policies", 25.0, 1, "apply"),
        make_q("jncia-sec", "Which NAT type maps multiple private IPs to one public IP?",
               [("Static NAT", False), ("Source NAT with PAT", True), ("Destination NAT", False), ("Twice NAT", False)],
               "Source NAT with PAT uses port numbers to share a single public IP.", "NAT", 25.0, 2, "understand"),
        make_q("jncia-sec", "Which command displays active VPN tunnels?",
               [("show security ipsec security-associations", True), ("show ike sa", False), ("show vpn tunnel", False), ("show security vpn", False)],
               "'show security ipsec security-associations' displays active IPsec SAs.", "IPsec VPNs", 25.0, 2, "apply"),
        make_q("jncia-sec", "Which Screen option detects IP spoofing?",
               [("IP spoofing", True), ("Land", False), ("Teardrop", False), ("Ping of Death", False)],
               "The IP spoofing Screen option detects packets with invalid source addresses.", "Screens", 25.0, 2, "remember"),
        make_q("jncia-sec", "Which logging severity is most critical?",
               [("Error", False), ("Critical", False), ("Alert", False), ("Emergency", True)],
               "Syslog severity 0 is Emergency, the most critical.", "Troubleshooting", 10.0, 1, "remember"),
        make_q("jncia-sec", "Which command shows interface status including zone?",
               [("show interfaces terse", True), ("show security zones", False), ("show configuration interfaces", False), ("show interface zone", False)],
               "'show interfaces terse' shows interface status and IP addresses.", "Troubleshooting", 10.0, 1, "apply"),
    ]

    # JNCIA-DC additional
    questions += [
        make_q("jncia-dc", "Which protocol auto-discovers switch neighbors in a data center?",
               [("CDP", False), ("LLDP", True), ("VTP", False), ("DTP", False)],
               "LLDP is an IEEE standard for neighbor discovery.", "DC Architecture", 25.0, 1, "remember"),
        make_q("jncia-dc", "Which command shows Virtual Chassis member status?",
               [("show virtual-chassis", True), ("show chassis vc", False), ("show vc members", False), ("show virtual-chassis status", False)],
               "'show virtual-chassis' displays VC member roles and states.", "DC Platforms", 25.0, 2, "apply"),
        make_q("jncia-dc", "Which feature bundles multiple physical links into one logical link?",
               [("VRRP", False), ("LACP", True), ("RSTP", False), ("VXLAN", False)],
               "LACP bundles multiple links into an aggregated Ethernet interface.", "Layer 2", 25.0, 1, "understand"),
        make_q("jncia-dc", "Which command displays VLANs on a QFX switch?",
               [("show vlans", True), ("show vlan", False), ("show ethernet-switching vlans", False), ("show bridge vlans", False)],
               "'show vlans' displays configured VLANs and member interfaces.", "Layer 2", 25.0, 1, "apply"),
        make_q("jncia-dc", "Which VXLAN element identifies a Layer 2 segment?",
               [("VTEP", False), ("VNI", True), ("Bridge domain", False), ("VLAN", False)],
               "VXLAN Network Identifier (VNI) identifies a Layer 2 segment.", "Overlays", 25.0, 2, "understand"),
        make_q("jncia-dc", "Which command shows interface errors on QFX?",
               [("show interfaces extensive", True), ("show interfaces terse", False), ("show ethernet-switching errors", False), ("show interface errors", False)],
               "'show interfaces extensive' displays detailed error counters.", "Troubleshooting", 10.0, 1, "apply"),
        make_q("jncia-dc", "Which protocol assigns IP addresses automatically?",
               [("DNS", False), ("DHCP", True), ("NTP", False), ("SNMP", False)],
               "DHCP assigns IP addresses dynamically.", "DC Platforms", 25.0, 1, "remember"),
    ]

    # JNCIA-AUT additional
    questions += [
        make_q("jncia-aut", "Which protocol does Ansible use to connect to Junos?",
               [("SSH/NETCONF", True), ("SNMP", False), ("Telnet", False), ("REST API only", False)],
               "Ansible connects to Junos via SSH and NETCONF.", "Automation Tools", 25.0, 2, "understand"),
        make_q("jncia-aut", "Which data format is native to NETCONF?",
               [("JSON", False), ("YAML", False), ("XML", True), ("CSV", False)],
               "NETCONF uses XML encoding by default.", "NETCONF/YANG", 25.0, 1, "remember"),
        make_q("jncia-aut", "Which HTTP method retrieves data?",
               [("GET", True), ("POST", False), ("PUT", False), ("DELETE", False)],
               "GET retrieves resources from a REST API.", "REST APIs", 25.0, 1, "remember"),
        make_q("jncia-aut", "Which YANG statement references another module's definitions?",
               [("include", False), ("import", True), ("uses", False), ("augment", False)],
               "'import' brings in definitions from another YANG module.", "YANG", 25.0, 2, "remember"),
        make_q("jncia-aut", "Which Junos script runs automatically on configuration commit?",
               [("Op script", False), ("Event script", False), ("Commit script", True), ("SNMP script", False)],
               "Commit scripts execute during the commit process.", "On-box Automation", 25.0, 2, "understand"),
        make_q("jncia-aut", "Which REST API status means resource not found?",
               [("400", False), ("401", False), ("403", False), ("404", True)],
               "HTTP 404 Not Found means the requested resource does not exist.", "REST APIs", 25.0, 1, "remember"),
        make_q("jncia-aut", "Which tool uses playbooks written in YAML?",
               [("Ansible", True), ("Terraform", False), ("PyEZ", False), ("Chef", False)],
               "Ansible uses YAML playbooks.", "Automation Tools", 25.0, 1, "remember"),
    ]

    # JNCIP-SEC additional
    questions += [
        make_q("jncip-sec", "Which SRX feature provides application-based firewall rules?",
               [("AppFW", True), ("Screens", False), ("IDP", False), ("UTM", False)],
               "AppFW uses AppID to enforce application-based firewall policies.", "Advanced Security", 15.0, 2, "understand"),
        make_q("jncip-sec", "Which command shows chassis cluster interfaces?",
               [("show chassis cluster interfaces", True), ("show cluster interfaces", False), ("show redundancy interfaces", False), ("show interfaces cluster", False)],
               "'show chassis cluster interfaces' displays cluster interface states.", "High Availability", 15.0, 2, "apply"),
        make_q("jncip-sec", "Which IPsec protocol provides encryption?",
               [("AH", False), ("ESP", True), ("IKE", False), ("ISAKMP", False)],
               "ESP (Encapsulating Security Payload) provides encryption and authentication.", "IPsec VPNs", 15.0, 1, "remember"),
        make_q("jncip-sec", "Which command displays security zones and policies?",
               [("show security zones", True), ("show zones", False), ("show security policies", False), ("show configuration security", False)],
               "'show security zones' displays zones and associated interfaces.", "Security Policies", 15.0, 1, "apply"),
        make_q("jncip-sec", "Which feature filters URLs by category on SRX?",
               [("Antivirus", False), ("Web filtering", True), ("Antispam", False), ("AppFW", False)],
               "Web filtering controls access based on URL categories.", "UTM", 10.0, 1, "understand"),
        make_q("jncip-sec", "Which command shows active IPsec VPN tunnels?",
               [("show security ipsec security-associations", True), ("show ike sa", False), ("show vpn status", False), ("show security vpn", False)],
               "'show security ipsec security-associations' displays active IPsec SAs.", "IPsec VPNs", 15.0, 2, "apply"),
        make_q("jncip-sec", "Which high-availability mode has both nodes actively forwarding?",
               [("Active/Passive", False), ("Active/Active", True), ("Cold standby", False), ("Hot standby", False)],
               "Active/Active chassis cluster allows both nodes to forward traffic.", "High Availability", 15.0, 2, "understand"),
        make_q("jncip-sec", "Which command shows User Firewall authenticated users?",
               [("show security user-identification authentication-table", True), ("show user firewall", False), ("show auth users", False), ("show security policies users", False)],
               "'show security user-identification authentication-table' displays authenticated users.", "Access Control", 15.0, 2, "apply"),
        make_q("jncip-sec", "Which logging destination stores messages in RAM?",
               [("Buffered", True), ("Console", False), ("Syslog server", False), ("File", False)],
               "Buffered logging stores syslog messages in device RAM.", "Management", 15.0, 2, "understand"),
        make_q("jncip-sec", "Which command displays active alarms?",
               [("show system alarms", True), ("show chassis alarms", False), ("show alarms", False), ("show log alarms", False)],
               "'show system alarms' displays active alarms.", "Troubleshooting", 10.0, 1, "apply"),
    ]

    # JNCIP-DC additional
    questions += [
        make_q("jncip-dc", "Which EVPN route type advertises Ethernet auto-discovery?",
               [("Type 1", True), ("Type 2", False), ("Type 3", False), ("Type 4", False)],
               "EVPN Type 1 routes are Ethernet Auto-Discovery routes.", "EVPN", 15.0, 2, "remember"),
        make_q("jncip-dc", "Which command shows EVPN MAC table?",
               [("show evpn mac-table", True), ("show ethernet-switching table", False), ("show evpn route", False), ("show route evpn", False)],
               "'show evpn mac-table' displays MAC addresses in EVPN instances.", "EVPN", 15.0, 2, "apply"),
        make_q("jncip-dc", "Which protocol commonly serves as underlay in EVPN-VXLAN?",
               [("OSPF", False), ("IS-IS", False), ("EBGP", True), ("RIP", False)],
               "EBGP is commonly used as the underlay routing protocol.", "Underlay", 15.0, 2, "understand"),
        make_q("jncip-dc", "Which feature enables active-active multihoming in EVPN?",
               [("All-active ES", True), ("Single-active ES", False), ("VRRP", False), ("MC-LAG only", False)],
               "All-active Ethernet segment allows multiple PEs to forward simultaneously.", "EVPN Multihoming", 15.0, 3, "understand"),
        make_q("jncip-dc", "Which command displays VXLAN tunnels?",
               [("show vxlan tunnel", True), ("show evpn vxlan", False), ("show route vxlan", False), ("show interfaces vxlan", False)],
               "'show vxlan tunnel' displays VXLAN tunnel endpoints.", "VXLAN", 15.0, 2, "apply"),
        make_q("jncip-dc", "Which data center topology connects every leaf to every spine?",
               [("Three-tier", False), ("Spine-leaf", True), ("Collapsed core", False), ("Bus", False)],
               "Spine-leaf topology has full mesh connectivity between leaf and spine layers.", "DC Architecture", 15.0, 2, "understand"),
        make_q("jncip-dc", "Which command shows EVPN instance overview?",
               [("show evpn overview", True), ("show evpn summary", False), ("show evpn instance", False), ("show bgp evpn summary", False)],
               "'show evpn overview' displays EVPN instance state and neighbors.", "EVPN", 15.0, 2, "apply"),
        make_q("jncip-dc", "Which VXLAN component terminates VXLAN tunnels?",
               [("VTEP", True), ("VNI", False), ("Bridge domain", False), ("VLAN", False)],
               "VTEP (VXLAN Tunnel Endpoint) terminates VXLAN tunnels.", "VXLAN", 15.0, 2, "understand"),
        make_q("jncip-dc", "Which command shows interface statistics on QFX?",
               [("show interfaces extensive", True), ("show interfaces terse", False), ("show ethernet-switching statistics", False), ("show port statistics", False)],
               "'show interfaces extensive' displays detailed interface statistics.", "Troubleshooting", 10.0, 1, "apply"),
        make_q("jncip-dc", "Which protocol advertises VTEP reachability in EVPN-VXLAN?",
               [("BGP EVPN", True), ("LDP", False), ("RSVP", False), ("IS-IS", False)],
               "BGP EVPN advertises MAC/IP and VTEP reachability.", "EVPN", 15.0, 2, "understand"),
    ]

    # JNCIP-AUT additional
    questions += [
        make_q("jncip-aut", "Which NETCONF capability allows rolling back a commit if not confirmed?",
               [(":confirmed-commit", True), (":rollback-on-error", False), (":validate", False), (":candidate", False)],
               "The :confirmed-commit capability supports automatic rollback unless confirmed.", "NETCONF", 15.0, 3, "understand"),
        make_q("jncip-aut", "Which YANG statement creates a reusable group of nodes?",
               [("container", False), ("grouping", True), ("list", False), ("leaf", False)],
               "A 'grouping' defines reusable nodes that can be included with 'uses'.", "YANG", 15.0, 3, "understand"),
        make_q("jncip-aut", "Which HTTP method deletes a resource?",
               [("GET", False), ("POST", False), ("PUT", False), ("DELETE", True)],
               "DELETE removes a resource.", "REST APIs", 15.0, 1, "remember"),
        make_q("jncip-aut", "Which tool uses state files for infrastructure management?",
               [("Ansible", False), ("Terraform", True), ("PyEZ", False), ("NETCONF", False)],
               "Terraform maintains state files tracking managed infrastructure.", "Off-box Automation", 15.0, 2, "understand"),
        make_q("jncip-aut", "Which NETCONF operation copies one datastore to another?",
               [("<edit-config>", False), ("<copy-config>", True), ("<get-config>", False), ("<delete-config>", False)],
               "<copy-config> copies the contents of one datastore to another.", "NETCONF", 15.0, 2, "remember"),
        make_q("jncip-aut", "Which Junos feature runs scripts triggered by syslog events?",
               [("Op scripts", False), ("Event scripts", True), ("Commit scripts", False), ("SNMP scripts", False)],
               "Event scripts trigger on system events such as syslog messages.", "On-box Automation", 15.0, 2, "understand"),
        make_q("jncip-aut", "Which data format uses key-value pairs and lists?",
               [("XML", False), ("JSON", True), ("CSV", False), ("Protobuf", False)],
               "JSON uses key-value pairs, arrays, and objects.", "REST APIs", 15.0, 1, "remember"),
        make_q("jncip-aut", "Which YANG statement extends another module's data model?",
               [("import", False), ("augment", True), ("include", False), ("uses", False)],
               "'augment' adds nodes to another module's data model hierarchy.", "YANG", 15.0, 3, "understand"),
        make_q("jncip-aut", "Which HTTP status indicates server error?",
               [("400", False), ("401", False), ("404", False), ("500", True)],
               "HTTP 500 Internal Server Error indicates a server-side problem.", "REST APIs", 15.0, 1, "remember"),
        make_q("jncip-aut", "Which protocol does NETCONF use by default?",
               [("TCP", False), ("UDP", False), ("SSH", True), ("TLS", False)],
               "NETCONF runs over SSH port 830 by default.", "NETCONF", 15.0, 1, "remember"),
    ]

    return questions


def questions_to_sql(questions: list[dict]) -> str:
    exam_ids = ",".join(f"'{EXAMS[e]['exam_id']}'" for e in EXAMS)
    lines = [
        "-- +goose Up",
        "-- +goose StatementBegin",
        "",
        "-- Juniper remaining exams extra question bank",
        f"-- Generated {len(questions)} additional blueprint-aligned single-choice questions",
        "",
        f"DELETE FROM questions WHERE exam_id IN ({exam_ids}) AND id LIKE '________-____-____-____-____________';",
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
        f"DELETE FROM questions WHERE exam_id IN ({exam_ids}) AND content_hash LIKE 'extra%';",
        "",
        "-- +goose StatementEnd",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    questions = generate_all()
    print(questions_to_sql(questions))
