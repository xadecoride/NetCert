#!/usr/bin/env python3
"""
NetCert — CCNA 2.0 simlet and topology question generator.
Generates configuration-based simlets and topology-based questions.
"""
import hashlib
import json
import uuid

CCNA_EXAM_ID = "b0000000-0000-0000-0000-000000000003"
CISCO_TRACK_ID = "a0000000-0000-0000-0000-000000000006"
URL = "https://learningcontent.cisco.com/documents/marketing/exam-topics/200-301-CCNA-v1.1.pdf"


def qid(seed: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_OID, f"ccna2-simlet:{seed}"))


def content_hash(body: str, correct: str) -> str:
    return hashlib.sha256(f"{body}::{correct}".encode()).hexdigest()[:16]


def make_q(body: str, options: list[tuple[str, bool]], explanation: str,
           section: str, weight: float, difficulty: int = 3,
           bloom: str = "analyze", qtype: str = "simlet") -> dict:
    assert sum(1 for _, c in options if c) == 1, f"exactly one correct option required: {body}"
    # Diagram/topology-based items get their own question type
    if qtype == "simlet" and "topology" in body.lower():
        qtype = "topology"
    letters = "ABCDEF"
    opts = []
    for i, (text, correct) in enumerate(options):
        opts.append({"id": letters[i], "text": text, "is_correct": correct})
    correct_letter = next(letters[i] for i, (_, c) in enumerate(options) if c)
    return {
        "id": qid(body + correct_letter),
        "exam_id": CCNA_EXAM_ID,
        "track_id": CISCO_TRACK_ID,
        "question_type": qtype,
        "difficulty": difficulty,
        "bloom_level": bloom,
        "body": body,
        "options": opts,
        "explanation": explanation,
        "reference_urls": [URL],
        "blueprint_section": section,
        "blueprint_weight": weight,
        "content_hash": content_hash(body, correct_letter),
        "is_active": True,
    }


def generate_all() -> list[dict]:
    questions: list[dict] = []

    # VLAN / trunking simlets
    questions += [
        make_q(
            "Refer to the switch output:\n\n"
            "SW1# show interfaces trunk\n"
            "Port        Mode         Encapsulation  Status        Native vlan\n"
            "Gi0/1       on           802.1q         trunking      99\n"
            "Gi0/2       on           802.1q         trunking      99\n\n"
            "SW1# show vlan brief\n"
            "VLAN Name                             Status    Ports\n"
            "---- -------------------------------- --------- -------------------------------\n"
            "1    default                          active    Gi0/3, Gi0/4\n"
            "10   SALES                            active\n"
            "20   ENG                              active\n"
            "99   MGMT                             active\n\n"
            "Which ports carry traffic for VLAN 10?",
            [("Only Gi0/1 and Gi0/2", True),
             ("Only Gi0/3 and Gi0/4", False),
             ("Gi0/1, Gi0/2, Gi0/3, and Gi0/4", False),
             ("No ports carry VLAN 10", False)],
            "Trunk ports carry all active VLANs across the link. Access ports in VLAN 1 do not carry VLAN 10.",
            "2.0 Network Access", 20.0, 3, "analyze"),
        make_q(
            "A topology shows two switches SW1 and SW2 connected by Gi0/1 on both ends.\n"
            "SW1 is configured with:\n"
            " interface GigabitEthernet0/1\n"
            "  switchport mode trunk\n"
            "  switchport trunk allowed vlan 10,20\n"
            "SW2 is configured with:\n"
            " interface GigabitEthernet0/1\n"
            "  switchport mode dynamic desirable\n\n"
            "What is the resulting state of the link?",
            [("It becomes a trunk carrying VLANs 10 and 20", True),
             ("It remains an access link", False),
             ("It becomes a trunk carrying all VLANs", False),
             ("The link is administratively down", False)],
            "SW1 is statically configured as trunk; SW2 dynamic desirable will negotiate to trunk. The allowed VLAN list on SW1 restricts traffic to 10 and 20.",
            "2.0 Network Access", 20.0, 3, "analyze"),
        make_q(
            "Topology: PC1 is in VLAN 10 on SW1 port Fa0/1. PC2 is in VLAN 10 on SW2 port Fa0/1. "
            "The switches are connected via Gi0/1 trunk. A router-on-a-stick router R1 is connected to SW1 Gi0/2 trunk.\n"
            "PC1 cannot reach PC2, but both can reach their default gateway on R1. What is the most likely cause?",
            [("The native VLAN mismatch between SW1 and SW2", False),
             ("VLAN 10 is not allowed on the trunk between SW1 and SW2", True),
             ("R1 subinterface encapsulation is wrong", False),
             ("PC1 default gateway is missing", False)],
            "If both PCs can reach the gateway but not each other, inter-switch trunk is likely missing VLAN 10.",
            "2.0 Network Access", 20.0, 4, "troubleshoot"),
    ]

    # STP topology
    questions += [
        make_q(
            "Refer to the STP topology:\n\n"
            "       [SW1]  (Bridge ID: 32768.0000.0000.0001)\n"
            "      /     \\\n"
            "   [SW2]     [SW3]\n"
            "   (32768.0000.0000.0002)  (32768.0000.0000.0003)\n\n"
            "All links are GigabitEthernet with equal cost. Which switch is the root bridge?",
            [("SW1", True), ("SW2", False), ("SW3", False), ("Cannot determine", False)],
            "Lowest bridge ID wins root bridge election. SW1 has the lowest MAC portion.",
            "2.0 Network Access", 20.0, 2, "understand"),
        make_q(
            "In the same topology, SW1 is root. Which ports on SW2 and SW3 are root ports?",
            [("Both upstream ports toward SW1", True),
             ("Both downstream ports toward each other", False),
             ("All ports are root ports", False),
             ("No root ports exist on non-root switches", False)],
            "Each non-root switch selects one root port — the port with lowest cost to root, which faces upstream.",
            "2.0 Network Access", 20.0, 3, "analyze"),
    ]

    # OSPF / EIGRP topology
    questions += [
        make_q(
            "Topology: R1--(Area 0)--R2--(Area 1)--R3\n"
            "R1 has networks 10.1.1.0/24 and 10.1.2.0/24 in Area 0. R3 has 10.3.3.0/24 in Area 1.\n"
            "What LSA type does R1 receive for 10.3.3.0/24?",
            [("Type 1", False), ("Type 2", False), ("Type 3", True), ("Type 5", False)],
            "Type 3 summary LSAs are generated by ABRs to advertise inter-area routes.",
            "3.0 IP Connectivity", 25.0, 3, "analyze"),
        make_q(
            "Refer to the routing table:\n\n"
            "O   10.0.0.0/8 [110/2] via 192.168.1.1\n"
            "O   10.1.0.0/16 [110/3] via 192.168.1.2\n"
            "O   10.1.1.0/24 [110/4] via 192.168.1.3\n\n"
            "Which next-hop is used for traffic to 10.1.1.50?",
            [("192.168.1.1", False), ("192.168.1.2", False),
             ("192.168.1.3", True), ("Load-balanced across all three", False)],
            "Longest prefix match selects /24 route for 10.1.1.50.",
            "3.0 IP Connectivity", 25.0, 3, "apply"),
        make_q(
            "EIGRP topology:\n\n"
            "        [R1]\n"
            "      /      \\\n"
            "   [R2]      [R3]\n"
            "   FD=1000   FD=2000\n"
            "   AD=800    AD=1500\n\n"
            "From R1, what is the feasible successor to reach the destination behind R2/R3?",
            [("R2 because it has the lowest FD", False),
             ("R2 is the successor; R3 is not a feasible successor", False),
             ("R3 if its AD is less than the successor FD", True),
             ("Both R2 and R3 are feasible successors", False)],
            "Successor is R2 (lowest FD). Feasible successor must have AD < successor FD. R3 AD=1500 < 1000 is false, so R3 is not feasible.",
            "3.0 IP Connectivity", 25.0, 4, "analyze"),
    ]

    # NAT / ACL simlets
    questions += [
        make_q(
            "Router# show ip nat translations\n"
            "Pro Inside global      Inside local       Outside local      Outside global\n"
            "tcp 203.0.113.5:5001   192.168.1.10:5001  8.8.8.8:443        8.8.8.8:443\n"
            "tcp 203.0.113.5:5002   192.168.1.11:5002  8.8.8.8:443        8.8.8.8:443\n\n"
            "What type of NAT is shown?",
            [("Static NAT", False), ("Dynamic NAT", False), ("PAT / NAT overload", True), ("Dynamic PAT with pool", False)],
            "Multiple inside local addresses share one inside global address with unique source ports — PAT overload.",
            "4.0 IP Services", 15.0, 3, "analyze"),
        make_q(
            "The following ACL is applied inbound on R1 Gi0/0 facing the internal network:\n\n"
            "ip access-list extended BLOCK\n"
            " 10 permit tcp 10.1.1.0 0.0.0.255 any eq 80\n"
            " 20 deny ip 10.1.1.0 0.0.0.255 10.2.2.0 0.0.0.255\n"
            " 30 permit ip any any\n\n"
            "A host 10.1.1.50 sends TCP traffic to 10.2.2.10 port 80. What happens?",
            [("Permitted by line 10", True),
             ("Denied by line 20", False),
             ("Permitted by line 30", False),
             ("Dropped by implicit deny", False)],
            "ACLs process in order. Line 10 permits TCP from 10.1.1.0/24 to any port 80 before line 20 denies.",
            "5.0 Security Fundamentals", 15.0, 3, "analyze"),
    ]

    # DHCP / HSRP / EtherChannel
    questions += [
        make_q(
            "Topology shows a DHCP server at 10.1.1.10 and a client PC on a different subnet separated by a router.\n"
            "The client fails to obtain an IP address. Which router configuration is most likely missing?",
            [("ip helper-address 10.1.1.10 on the client-facing interface", True),
             ("ip address dhcp on the server-facing interface", False),
             ("A static route to 10.1.1.10", False),
             ("DHCP snooping on the switch", False)],
            "Routers do not forward DHCP broadcasts between subnets without an ip helper-address to relay to the DHCP server.",
            "4.0 IP Services", 15.0, 3, "troubleshoot"),
        make_q(
            "Two routers R1 and R2 run HSRP on VLAN 10. R1 has priority 110, R2 has priority 100.\n"
            "Preempt is configured on both. R1 reboots and comes back online. Which router becomes Active?",
            [("R1", True), ("R2", False), ("Neither", False), ("Both become Active", False)],
            "With preempt, the router with highest priority takes over as Active when it comes online.",
            "4.0 IP Services", 15.0, 2, "understand"),
        make_q(
            "Switch ports Gi0/1 and Gi0/2 are bundled into Port-channel 1 with mode active on both ends.\n"
            "The neighbor switch uses mode passive. What is the resulting negotiation state?",
            [("LACP forms the bundle because active and passive negotiate", True),
             ("PAgP forms the bundle", False),
             ("No bundle forms; both sides must be active", False),
             ("The ports become a static trunk", False)],
            "LACP active negotiates with LACP passive. PAgP is Cisco proprietary and requires PAgP modes.",
            "2.0 Network Access", 20.0, 3, "analyze"),
    ]

    # Wireless / Security
    questions += [
        make_q(
            "Topology: A small office uses a single AP on channel 6 in 2.4 GHz. Neighboring APs are detected on channels 4 and 8.\n"
            "What is the recommended channel change?",
            [("Channel 1 or 11", True), ("Channel 5", False), ("Channel 6 with higher power", False), ("Channel 9", False)],
            "Channels 1, 6, and 11 are the non-overlapping 2.4 GHz channels. Channel 4/8 overlap with 6.",
            "2.0 Network Access", 20.0, 2, "apply"),
        make_q(
            "Switch port security output:\n\n"
            "Port  Security  Violation  Action   Status\n"
            "Fa0/1 Enabled   Restrict   Restrict Secure-shutdown\n\n"
            "What caused the interface to enter err-disabled?",
            [("A MAC address violation with shutdown violation mode", True),
             ("A MAC address violation with restrict mode", False),
             ("DTP negotiation failure", False),
             ("A BPDU received on a PortFast port", False)],
            "Secure-shutdown/err-disabled occurs when port security violation mode is shutdown. Restrict mode increments counters but does not shut down.",
            "5.0 Security Fundamentals", 15.0, 3, "troubleshoot"),
    ]

    # IPv6 / subnetting topology
    questions += [
        make_q(
            "Topology shows a /64 IPv6 subnet 2001:db8:1:1::/64. Host A auto-configures with EUI-64 using MAC 00:1A:2B:3C:4D:5E.\n"
            "What is the host identifier portion?",
            [("021A:2BFF:FE3C:4D5E", True),
             ("001A:2B3C:4D5E", False),
             ("021A:2B3C:4D5E", False),
             ("FE80::021A:2BFF:FE3C:4D5E", False)],
            "EUI-64 inserts FF:FE in the middle and flips the U/L bit (02 instead of 00).",
            "1.0 Network Fundamentals", 15.0, 3, "apply"),
        make_q(
            "A router interface is configured with ip address 192.168.5.65 255.255.255.224.\n"
            "What is the broadcast address of this subnet?",
            [("192.168.5.95", True),
             ("192.168.5.64", False),
             ("192.168.5.96", False),
             ("192.168.5.127", False)],
            "/27 block size is 32. Network 192.168.5.64, broadcast 192.168.5.95, hosts .65-.94.",
            "1.0 Network Fundamentals", 15.0, 2, "apply"),
    ]

    # Automation / REST / JSON
    questions += [
        make_q(
            "A Python script uses requests to POST to https://router/restconf/data/Cisco-IOS-XE-native:native/interface.\n"
            "What type of API is being used?",
            [("NETCONF over SSH", False), ("RESTCONF", True), ("SOAP", False), ("gRPC", False)],
            "RESTCONF uses HTTP/REST methods and URIs based on YANG models.",
            "6.0 Automation and Programmability", 10.0, 2, "understand"),
        make_q(
            "An Ansible playbook targets switches with the ios_config module and a Jinja2 template.\n"
            "Which component supplies the per-device variables?",
            [("Inventory", True), ("Galaxy", False), ("Module index", False), ("Vault", False)],
            "Inventory files define hosts and host/group variables used by playbooks and templates.",
            "6.0 Automation and Programmability", 10.0, 2, "understand"),
    ]

    # Additional topology questions to guarantee >=15 topology items per CCNA 2.0 attempt
    questions += [
        make_q(
            "Topology: Three routers R1, R2, and R3 are connected in a full mesh using serial links.\n"
            "R1 has a single T1 link to R2 and a T3 link to R3. Which path will OSPF prefer to reach R3?",
            [("T1 path through R2 because it has lower bandwidth", False),
             ("Direct T3 path to R3 because it has lower cost", True),
             ("OSPF load-balances across both paths", False),
             ("The path with fewer hops", False)],
            "OSPF cost is based on bandwidth. T3 has higher bandwidth and lower cost than T1.",
            "3.0 IP Connectivity", 25.0, 3, "analyze"),
        make_q(
            "Refer to the topology:\n\n"
            "   [SW1]---[SW2]---[SW3]\n"
            "   VLAN 10 VLAN 10 VLAN 10\n\n"
            "All inter-switch links are trunks allowing VLAN 10. A host in VLAN 10 on SW1 cannot reach a host in VLAN 10 on SW3.\n"
            "What is the most likely cause?",
            [("VLAN 10 is not allowed on the SW2-SW3 trunk", True),
             ("Native VLAN mismatch on SW1-SW2 trunk", False),
             ("STP blocked all VLAN 10 ports", False),
             ("The hosts are in different subnets", False)],
            "If VLAN 10 is missing on one trunk segment, traffic cannot traverse the full Layer 2 path.",
            "2.0 Network Access", 20.0, 4, "troubleshoot"),
        make_q(
            "Topology:\n\n"
            "   [R1]---192.168.1.0/30---[R2]---192.168.2.0/30---[R3]\n\n"
            "R1 has a static route to 10.0.0.0/8 pointing to R2. R2 has a static route to 10.0.0.0/8 pointing to R3.\n"
            "Which routing problem is most likely if R2 loses its route to R3?",
            [("R1 will continue sending traffic to R2, creating a black hole", True),
             ("R1 will automatically reroute via a directly connected path", False),
             ("R2 will advertise the loss to R1 via OSPF", False),
             ("Static routes will converge in 30 seconds", False)],
            "Static routes do not dynamically adapt. R1 keeps forwarding to R2, which cannot reach the destination.",
            "3.0 IP Connectivity", 25.0, 3, "analyze"),
        make_q(
            "Refer to the wireless topology:\n\n"
            "   [AP1] <--channel 36--> [AP2] <--channel 44--> [AP3]\n\n"
            "All APs are in the 5 GHz band using 20 MHz channels. Which statement is true?",
            [("Channels 36, 40, 44, and 48 are all non-overlapping 20 MHz channels", False),
             ("AP1, AP2, and AP3 are all on non-overlapping channels", True),
             ("Channel 36 overlaps with channel 44", False),
             ("5 GHz channels never overlap", False)],
            "In 5 GHz, channels 36, 40, 44, 48 are non-overlapping when using 20 MHz widths.",
            "2.0 Network Access", 20.0, 3, "analyze"),
        make_q(
            "Topology: A router has two WAN links — a primary Ethernet circuit and a backup DSL circuit.\n"
            "A floating static route is configured for the backup with a higher administrative distance.\n"
            "Under what condition will the floating static route appear in the routing table?",
            [("When the primary route fails", True),
             ("When the primary route has a higher metric", False),
             ("When the backup link has lower bandwidth", False),
             ("Always, because it is a static route", False)],
            "A floating static route is installed only when the primary route (lower AD) is no longer available.",
            "3.0 IP Connectivity", 25.0, 3, "understand"),
        make_q(
            "Refer to the topology:\n\n"
            "   [PC]---[R1]---[R2]---[Server]\n"
            "   192.168.1.0/24  10.0.0.0/30  172.16.0.0/24\n\n"
            "The PC can ping R1 but not the Server. R1 has a route to 172.16.0.0/24 via R2. What is the most likely issue?",
            [("R2 does not have a return route to 192.168.1.0/24", True),
             ("The Server is powered off", False),
             ("R1 default gateway is wrong", False),
             ("PC subnet mask is incorrect", False)],
            "For end-to-end reachability, return traffic must have a route back to the source network.",
            "3.0 IP Connectivity", 25.0, 4, "troubleshoot"),
        make_q(
            "Topology:\n\n"
            "       [R1]\n"
            "      /    \\\n"
            "   [SW1]  [SW2]\n"
            "     |      |\n"
            "   [PC1]  [PC2]\n\n"
            "PC1 and PC2 are in the same VLAN and subnet. R1 provides a gateway for the VLAN.\n"
            "Which device breaks the broadcast domain between PC1 and PC2?",
            [("SW1", False), ("SW2", False), ("R1", True), ("No device; they are in the same VLAN", False)],
            "Routers break up broadcast domains. Switches in the same VLAN extend the broadcast domain.",
            "1.0 Network Fundamentals", 15.0, 2, "understand"),
        make_q(
            "Refer to the network topology:\n\n"
            "   [Internet]---[Firewall]---[Core]---[Access]---[Host]\n\n"
            "Which device is best placed to perform stateful packet inspection between the Internet and internal network?",
            [("Core switch", False), ("Access switch", False), ("Firewall", True), ("Host", False)],
            "A stateful firewall is the correct device to enforce security policies at the network edge.",
            "5.0 Security Fundamentals", 15.0, 1, "understand"),
        make_q(
            "Topology:\n\n"
            "   [R1]---[R2]---[R3]\n"
            "   10.1.1.0/30  10.1.2.0/30\n\n"
            "RIP is running on all routers. R1 advertises 192.168.1.0/24. How does R3 learn this route?",
            [("As a directly connected route", False),
             ("As a RIP route with hop count 2", True),
             ("As a static route", False),
             ("As an OSPF route", False)],
            "RIP increments hop count at each router. R1→R2→R3 is two hops.",
            "3.0 IP Connectivity", 25.0, 2, "understand"),
        make_q(
            "Refer to the IPv6 topology:\n\n"
            "   [R1]---[R2]---[R3]\n"
            "   2001:db8:1::/64  2001:db8:2::/64\n\n"
            "R1 wants to send a packet to R3's link-local address. Which address will R1 use as the destination?",
            [("2001:db8:2::3", False),
             ("fe80::3 on the outgoing interface", True),
             ("ff02::1", False),
             ("::1", False)],
            "Link-local addresses (fe80::/10) are used on the local link and must be scoped to the outgoing interface.",
            "1.0 Network Fundamentals", 15.0, 3, "apply"),
    ]

    return questions


def questions_to_sql(questions: list[dict]) -> str:
    exam_id = CCNA_EXAM_ID
    ids = ",".join(f"'{q['id']}'" for q in questions)
    lines = [
        "-- +goose Up",
        "-- +goose StatementBegin",
        "",
        f"-- CCNA 2.0 simlet and topology questions",
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
