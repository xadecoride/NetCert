#!/usr/bin/env python3
"""
NetCert — CCNA 200-301 v1.1 question generator.
Generates realistic, blueprint-aligned single-choice questions.
Each question has exactly one correct answer, a detailed explanation,
and maps to an official CCNA 200-301 v1.1 exam topic.
"""
import hashlib
import json
import random
import uuid

# Exam/track UUIDs from 027_seed_tracks_exams.sql
CCNA_EXAM_ID = "b0000000-0000-0000-0000-000000000003"
CISCO_TRACK_ID = "a0000000-0000-0000-0000-000000000006"


def qid(seed: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_OID, f"ccna-v1.1:{seed}"))


def content_hash(body: str, correct: str) -> str:
    return hashlib.sha256(f"{body}::{correct}".encode()).hexdigest()[:16]


def make_q(body: str, options: list[tuple[str, bool]], explanation: str,
           section: str, weight: float, difficulty: int = 2,
           bloom: str = "understand", urls: list[str] | None = None) -> dict:
    assert sum(1 for _, c in options if c) == 1, f"exactly one correct option required: {body}"
    letters = "ABCDEF"
    opts = []
    for i, (text, correct) in enumerate(options):
        opts.append({"id": letters[i], "text": text, "is_correct": correct})
    correct_letter = next(letters[i] for i, (_, c) in enumerate(options) if c)
    return {
        "id": qid(body + correct_letter),
        "exam_id": CCNA_EXAM_ID,
        "track_id": CISCO_TRACK_ID,
        "question_type": "single-choice",
        "difficulty": difficulty,
        "bloom_level": bloom,
        "body": body,
        "options": opts,
        "explanation": explanation,
        "reference_urls": urls or ["https://learningcontent.cisco.com/documents/marketing/exam-topics/200-301-CCNA-v1.1.pdf"],
        "blueprint_section": section,
        "blueprint_weight": weight,
        "content_hash": content_hash(body, correct_letter),
        "is_active": True,
    }


SECTIONS = {
    "1.1 Network Components": ("1.0 Network Fundamentals", 20.0),
    "1.2 Network Topology": ("1.0 Network Fundamentals", 20.0),
    "1.3 Physical Interfaces": ("1.0 Network Fundamentals", 20.0),
    "1.4 TCP/UDP": ("1.0 Network Fundamentals", 20.0),
    "1.5 IPv4/IPv6 Addressing": ("1.0 Network Fundamentals", 20.0),
    "2.1 Switching Concepts": ("2.0 Network Access", 20.0),
    "2.2 VLANs": ("2.0 Network Access", 20.0),
    "2.3 Inter-Switch Connectivity": ("2.0 Network Access", 20.0),
    "2.4 STP": ("2.0 Network Access", 20.0),
    "2.5 Wireless": ("2.0 Network Access", 20.0),
    "3.1 Routing Fundamentals": ("3.0 IP Connectivity", 25.0),
    "3.2 OSPF": ("3.0 IP Connectivity", 25.0),
    "3.3 EIGRP": ("3.0 IP Connectivity", 25.0),
    "3.4 BGP": ("3.0 IP Connectivity", 25.0),
    "4.1 NAT": ("4.0 IP Services", 10.0),
    "4.2 NTP/DHCP/DNS": ("4.0 IP Services", 10.0),
    "4.3 SNMP/Syslog/SSH": ("4.0 IP Services", 10.0),
    "4.4 QoS": ("4.0 IP Services", 10.0),
    "5.1 Security Concepts": ("5.0 Security Fundamentals", 15.0),
    "5.2 Access Control": ("5.0 Security Fundamentals", 15.0),
    "5.3 Wireless Security": ("5.0 Security Fundamentals", 15.0),
    "6.1 Automation": ("6.0 Automation and Programmability", 10.0),
    "6.2 APIs": ("6.0 Automation and Programmability", 10.0),
    "6.3 AI/ML": ("6.0 Automation and Programmability", 10.0),
}


def section_key(name: str) -> str:
    return name


def generate_questions() -> list[dict]:
    questions: list[dict] = []

    # ═══════════════════════════════════════════════════════════════════════
    # 1.0 Network Fundamentals
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q(
            "Which device operates at Layer 3 of the OSI model and makes forwarding decisions based on IP addresses?",
            [("Layer 2 switch", False), ("Hub", False), ("Router", True), ("Access point", False)],
            "Routers operate at Layer 3 (Network layer) and forward packets based on destination IP addresses. Switches use MAC addresses (Layer 2), hubs repeat signals (Layer 1), and access points operate at Layer 2.",
            "1.1 Network Components", 20.0, 1, "remember"),
        make_q(
            "What is the primary purpose of a next-generation firewall (NGFW) compared to a traditional stateful firewall?",
            [("To provide Layer 2 switching", False), ("To perform deep packet inspection and application awareness", True),
             ("To replace wireless LAN controllers", False), ("To forward traffic based only on IP addresses", False)],
            "NGFWs add deep packet inspection, intrusion prevention, application awareness, and often threat intelligence to traditional stateful firewall capabilities.",
            "1.1 Network Components", 20.0, 2, "understand"),
        make_q(
            "Which network topology architecture uses a collapsed core/distribution layer into a single tier?",
            [("Three-tier", False), ("Spine-leaf", False), ("Two-tier", True), ("SOHO", False)],
            "A two-tier (collapsed core) design combines the core and distribution layers. Three-tier has access, distribution, and core. Spine-leaf is a two-layer data center fabric.",
            "1.2 Network Topology", 20.0, 2, "understand"),
        make_q(
            "Which cabling type is most suitable for a 10 Gb/s connection over 300 meters?",
            [("UTP Cat 5e", False), ("Multimode fiber", False), ("Single-mode fiber", True), ("Coaxial cable", False)],
            "Single-mode fiber supports the longest distances (kilometers) at high speeds. Multimode fiber is limited to shorter distances, and UTP Cat 5e/Cat 6 have much shorter reach.",
            "1.3 Physical Interfaces", 20.0, 2, "apply"),
        make_q(
            "What is a characteristic of TCP compared to UDP?",
            [("Connectionless communication", False), ("No reordering of packets", False), ("Connection-oriented with sequencing", True), ("Lower overhead", False)],
            "TCP is connection-oriented, provides reliable delivery, sequencing, flow control, and error recovery. UDP is connectionless with lower overhead.",
            "1.4 TCP/UDP", 20.0, 1, "remember"),
        make_q(
            "Which protocol uses port 22 by default?",
            [("Telnet", False), ("FTP", False), ("SSH", True), ("SNMP", False)],
            "SSH uses TCP port 23 is Telnet, 20/21 is FTP, and 161/162 is SNMP.",
            "1.4 TCP/UDP", 20.0, 1, "remember"),
        make_q(
            "Which IPv4 address range is reserved for private networks according to RFC 1918?",
            [("100.64.0.0/10", False), ("169.254.0.0/16", False), ("192.168.0.0/16", True), ("224.0.0.0/4", False)],
            "RFC 1918 private ranges are 10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16. 100.64.0.0/10 is CGNAT, 169.254.0.0/16 is link-local, and 224.0.0.0/4 is multicast.",
            "1.5 IPv4/IPv6 Addressing", 20.0, 1, "remember"),
        make_q(
            "What is the valid host range for the subnet 192.168.10.64/26?",
            [("192.168.10.65 - 192.168.10.126", True), ("192.168.10.64 - 192.168.10.127", False),
             ("192.168.10.64 - 192.168.10.126", False), ("192.168.10.65 - 192.168.10.127", False)],
            "/26 gives a block size of 64. Network address is 192.168.10.64, broadcast is 192.168.10.127. Valid hosts are 192.168.10.65 through 192.168.10.126.",
            "1.5 IPv4/IPv6 Addressing", 20.0, 3, "apply"),
        make_q(
            "Which IPv6 address type is automatically generated on every IPv6-enabled interface using the interface identifier?",
            [("Global unicast", False), ("Anycast", False), ("Link-local", True), ("Multicast", False)],
            "Every IPv6 interface auto-generates a link-local address (fe80::/10) using the interface identifier, typically via EUI-64 or randomized.",
            "1.5 IPv4/IPv6 Addressing", 20.0, 2, "understand"),
        make_q(
            "Which IPv6 address prefix is used for unique local addresses (ULA)?",
            [("2000::/3", False), ("fc00::/7", True), ("fe80::/10", False), ("ff00::/8", False)],
            "Unique local addresses use fc00::/7. 2000::/3 is global unicast, fe80::/10 is link-local, and ff00::/8 is multicast.",
            "1.5 IPv4/IPv6 Addressing", 20.0, 2, "remember"),
        make_q(
            "What is the function of the subnet mask in IPv4?",
            [("To encrypt traffic", False), ("To identify the network and host portions of an address", True),
             ("To resolve IP to MAC", False), ("To assign dynamic IP addresses", False)],
            "The subnet mask separates the network portion from the host portion of an IPv4 address, enabling routing and subnetting decisions.",
            "1.5 IPv4/IPv6 Addressing", 20.0, 1, "understand"),
        make_q(
            "Which command on a Windows host displays the IP configuration, including default gateway and DNS servers?",
            [("netstat -r", False), ("ipconfig /all", True), ("ifconfig -a", False), ("nslookup", False)],
            "ipconfig /all displays full IP configuration on Windows. ifconfig is used on Linux/macOS, netstat -r shows the routing table, and nslookup queries DNS.",
            "1.5 IPv4/IPv6 Addressing", 20.0, 2, "apply"),
        make_q(
            "Which wireless principle describes channels 1, 6, and 11 in the 2.4 GHz band?",
            [("They are overlapping channels", False), ("They are non-overlapping channels", True),
             ("They are 5 GHz channels", False), ("They require 80 MHz channel width", False)],
            "In the 2.4 GHz band, channels 1, 6, and 11 are the standard non-overlapping channels for 802.11 deployments.",
            "1.5 IPv4/IPv6 Addressing", 20.0, 2, "remember"),
        make_q(
            "Which cloud deployment model provides dedicated infrastructure for a single organization?",
            [("Public cloud", False), ("Hybrid cloud", False), ("Private cloud", True), ("Community cloud", False)],
            "A private cloud is dedicated to a single organization. Public cloud is shared, hybrid combines public and private, and community cloud is shared among organizations with common concerns.",
            "1.2 Network Topology", 20.0, 2, "understand"),
        make_q(
            "What is the maximum theoretical distance for 1000BASE-LX single-mode fiber?",
            [("100 m", False), ("550 m", False), ("5 km", True), ("100 m over UTP", False)],
            "1000BASE-LX over single-mode fiber can reach up to 5 km. Over multimode fiber it is typically 550 m, and 1000BASE-T over UTP is 100 m.",
            "1.3 Physical Interfaces", 20.0, 3, "remember"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # 2.0 Network Access
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q(
            "Which switch feature dynamically learns MAC addresses and builds a forwarding table?",
            [("VLAN tagging", False), ("MAC address table learning", True), ("Spanning Tree Protocol", False), ("Port security", False)],
            "Switches learn source MAC addresses on incoming frames and populate the MAC address table to make forwarding decisions.",
            "2.1 Switching Concepts", 20.0, 1, "understand"),
        make_q(
            "What is the purpose of a VLAN?",
            [("To increase collision domains", False), ("To logically segment a Layer 2 network", True),
             ("To route between IP subnets", False), ("To encrypt wireless traffic", False)],
            "VLANs create logical broadcast domains at Layer 2, allowing segmentation without physical separation. Routing between VLANs requires a Layer 3 device.",
            "2.2 VLANs", 20.0, 1, "understand"),
        make_q(
            "Which 802.1Q field is added to an Ethernet frame to identify VLAN membership?",
            [("FCS", False), ("Tag", True), ("Preamble", False), ("SFD", False)],
            "802.1Q inserts a 4-byte tag into the Ethernet frame containing the VLAN ID and priority. FCS is recalculated, preamble/SFD are not part of the tag.",
            "2.2 VLANs", 20.0, 2, "understand"),
        make_q(
            "Which trunking protocol is an IEEE standard and supports up to 4094 VLANs?",
            [("ISL", False), ("DTP", False), ("802.1Q", True), ("VTP", False)],
            "802.1Q is the IEEE standard trunking protocol. ISL is Cisco proprietary and deprecated. DTP negotiates trunks, and VTP manages VLAN databases.",
            "2.3 Inter-Switch Connectivity", 20.0, 1, "remember"),
        make_q(
            "What is the default behavior of a Cisco switch port regarding VLAN assignment?",
            [("It is assigned to VLAN 0", False), ("It is assigned to VLAN 1", True), ("It is a trunk port", False), ("It has no VLAN", False)],
            "By default, all Cisco switch ports are access ports in VLAN 1. VLAN 1 is also the default native VLAN on trunks.",
            "2.2 VLANs", 20.0, 1, "remember"),
        make_q(
            "Which Spanning Tree Protocol state can forward traffic but is still learning MAC addresses?",
            [("Blocking", False), ("Listening", False), ("Learning", False), ("Forwarding", True)],
            "In STP, the Forwarding state forwards traffic and continues to learn MAC addresses. Learning state learns MACs but does not forward user traffic.",
            "2.4 STP", 20.0, 2, "understand"),
        make_q(
            "Which Rapid PVST+ port role provides a redundant but blocked path to the root bridge?",
            [("Root port", False), ("Designated port", False), ("Alternate port", True), ("Edge port", False)],
            "Alternate ports provide a backup path to the root bridge and are discarding. Root ports face the root, designated ports forward for a segment, and edge ports connect to end hosts.",
            "2.4 STP", 20.0, 3, "understand"),
        make_q(
            "Which feature should be enabled on switch ports connected to end hosts to immediately transition them to forwarding in RSTP?",
            [("BPDU Guard", False), ("PortFast", True), ("Root Guard", False), ("Loop Guard", False)],
            "PortFast allows access ports to skip STP listening/learning and go directly to forwarding. BPDU Guard protects PortFast ports from receiving BPDUs.",
            "2.4 STP", 20.0, 2, "apply"),
        make_q(
            "Which wireless mode allows an access point to connect multiple wireless clients on the same radio?",
            [("Ad-hoc mode", False), ("Infrastructure mode", True), ("Monitor mode", False), ("Repeater mode", False)],
            "Infrastructure mode uses an AP to connect wireless clients. Ad-hoc is peer-to-peer without an AP. Monitor and repeater are specialized AP modes.",
            "2.5 Wireless", 20.0, 1, "understand"),
        make_q(
            "Which 802.11 standard operates in both 2.4 GHz and 5 GHz bands and supports channel bonding?",
            [("802.11b", False), ("802.11g", False), ("802.11n", True), ("802.11a", False)],
            "802.11n operates in both 2.4 GHz and 5 GHz and supports channel bonding (40 MHz). 802.11b/g are 2.4 GHz only; 802.11a is 5 GHz only.",
            "2.5 Wireless", 20.0, 2, "remember"),
        make_q(
            "Which wireless security protocol uses AES-CCMP encryption?",
            [("WEP", False), ("WPA", False), ("WPA2", True), ("Open authentication", False)],
            "WPA2 uses AES-CCMP encryption. WPA uses TKIP, WEP uses RC4, and open authentication has no encryption.",
            "2.5 Wireless", 20.0, 1, "remember"),
        make_q(
            "What is the purpose of the native VLAN on an 802.1Q trunk?",
            [("To encrypt traffic", False), ("To carry untagged traffic across the trunk", True),
             ("To disable STP on the trunk", False), ("To block all broadcast traffic", False)],
            "The native VLAN carries untagged traffic across an 802.1Q trunk. By default this is VLAN 1 and should be changed for security best practices.",
            "2.3 Inter-Switch Connectivity", 20.0, 2, "understand"),
        make_q(
            "Which switch security feature restricts the number of MAC addresses learned on a port?",
            [("DHCP snooping", False), ("Port security", True), ("Dynamic ARP inspection", False), ("IP Source Guard", False)],
            "Port security limits the number of MAC addresses on a switch port and can take action (shutdown/restrict) on violations. DHCP snooping, DAI, and IP Source Guard are other security features.",
            "2.1 Switching Concepts", 20.0, 2, "apply"),
        make_q(
            "Which action should be taken to mitigate VLAN hopping attacks?",
            [("Enable DTP on all ports", False), ("Disable unused ports and configure access ports explicitly", True),
             ("Use the default native VLAN", False), ("Enable trunking on all ports", False)],
            "VLAN hopping can be mitigated by disabling unused ports, setting ports to access mode explicitly, and changing the native VLAN from the default.",
            "2.2 VLANs", 20.0, 3, "analyze"),
        make_q(
            "In a spine-leaf topology, which statement is true?",
            [("Every leaf connects to every other leaf directly", False),
             ("Every leaf connects to every spine, and leaf switches connect endpoints", True),
             ("Spine switches connect endpoints directly", False),
             ("It is a three-tier hierarchical design", False)],
            "In spine-leaf, every leaf switch connects to every spine switch. Endpoints connect to leaf switches. This provides predictable latency and scalability.",
            "1.2 Network Topology", 20.0, 2, "understand"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # 3.0 IP Connectivity
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q(
            "What is the default administrative distance of OSPF on a Cisco router?",
            [("90", False), ("100", False), ("110", True), ("120", False)],
            "OSPF has an administrative distance of 110 on Cisco devices. EIGRP internal is 90, IS-IS is 115, RIP is 120, and directly connected is 0.",
            "3.2 OSPF", 25.0, 1, "remember"),
        make_q(
            "Which routing protocol uses DUAL to provide loop-free paths?",
            [("OSPF", False), ("BGP", False), ("EIGRP", True), ("RIP", False)],
            "EIGRP uses the Diffusing Update Algorithm (DUAL) to guarantee loop-free paths and compute successors/feasible successors.",
            "3.3 EIGRP", 25.0, 2, "understand"),
        make_q(
            "Which OSPF packet type is used to discover and maintain neighbor adjacencies?",
            [("LSU", False), ("LSR", False), ("Hello", True), ("DBD", False)],
            "OSPF Hello packets discover neighbors and maintain adjacencies. DBD describes the database, LSR requests LSAs, and LSU updates/floods LSAs.",
            "3.2 OSPF", 25.0, 1, "remember"),
        make_q(
            "Which OSPF neighbor state indicates that routers have exchanged DBDs and are fully synchronized?",
            [("Init", False), ("2-Way", False), ("Exchange", False), ("Full", True)],
            "The Full state means OSPF neighbors have completed database exchange and LSDBs are synchronized. 2-Way indicates bidirectional communication.",
            "3.2 OSPF", 25.0, 2, "understand"),
        make_q(
            "What is the purpose of the DR/BDR election in OSPF multi-access networks?",
            [("To encrypt OSPF updates", False), ("To reduce the number of adjacencies required", True),
             ("To assign IP addresses", False), ("To prevent route poisoning", False)],
            "DR/BDR election on multi-access networks reduces adjacency count from O(n²) to O(n). All routers form full adjacencies only with DR/BDR.",
            "3.2 OSPF", 25.0, 2, "understand"),
        make_q(
            "Which command displays the routing table on a Cisco router?",
            [("show ip route", True), ("show ip protocols", False), ("show interfaces", False), ("show cdp neighbors", False)],
            "show ip route displays the IPv4 routing table. show ip protocols shows configured routing protocols, and show interfaces displays interface status.",
            "3.1 Routing Fundamentals", 25.0, 1, "apply"),
        make_q(
            "Which route in the routing table has the longest prefix match for destination 10.1.1.1?",
            [("10.0.0.0/8", False), ("10.1.0.0/16", False), ("10.1.1.0/24", True), ("0.0.0.0/0", False)],
            "Longest prefix match selects the most specific route. /24 is more specific than /16, /8, and the default route.",
            "3.1 Routing Fundamentals", 25.0, 2, "apply"),
        make_q(
            "Which routing protocol is classified as path-vector and is used between autonomous systems?",
            [("OSPF", False), ("EIGRP", False), ("BGP", True), ("IS-IS", False)],
            "BGP is a path-vector EGP used for inter-domain routing between autonomous systems. OSPF, EIGRP, and IS-IS are IGPs.",
            "3.4 BGP", 25.0, 1, "remember"),
        make_q(
            "Which BGP attribute is used as the tiebreaker when all higher-priority attributes are equal?",
            [("AS_Path", False), ("Local Preference", False), ("MED", False), ("Router ID", True)],
            "BGP path selection considers weight, local preference, locally originated, AS_Path, origin, MED, eBGP/iBGP, IGP metric, and finally router ID as a tiebreaker.",
            "3.4 BGP", 25.0, 3, "understand"),
        make_q(
            "Which command would configure a router interface to participate in OSPF process 1 area 0?",
            [("router ospf 1", False), ("network 0.0.0.0 255.255.255.255 area 0", False),
             ("ip ospf 1 area 0", True), ("interface ospf 1 area 0", False)],
            "On modern Cisco IOS, ip ospf 1 area 0 is configured under the interface. The router ospf command enters routing process configuration.",
            "3.2 OSPF", 25.0, 2, "apply"),
        make_q(
            "What does a floating static route use to be installed only when the primary route fails?",
            [("A lower administrative distance", False), ("A higher administrative distance", True),
             ("A lower metric", False), ("A multicast next-hop", False)],
            "Floating static routes have a higher AD than the primary routing protocol route, so they are only used when the primary route disappears.",
            "3.1 Routing Fundamentals", 25.0, 2, "understand"),
        make_q(
            "Which EIGRP value must match between neighbors for an adjacency to form?",
            [("Router ID", False), ("Hello timer", False), ("Autonomous system number", True), ("Hold timer", False)],
            "EIGRP neighbors must be in the same autonomous system (AS). Timers and router ID do not need to match for EIGRP adjacency.",
            "3.3 EIGRP", 25.0, 2, "remember"),
        make_q(
            "In OSPF, which LSA type is generated by the DR on a multi-access segment and describes connected routers?",
            [("Type 1", False), ("Type 2", True), ("Type 3", False), ("Type 5", False)],
            "OSPF Type 2 LSAs (network LSAs) are generated by the DR on multi-access networks and describe all routers connected to the segment.",
            "3.2 OSPF", 25.0, 3, "remember"),
        make_q(
            "Which command displays OSPF neighbor relationships on a Cisco router?",
            [("show ip ospf database", False), ("show ip ospf neighbor", True), ("show ip route ospf", False), ("show ip protocols", False)],
            "show ip ospf neighbor displays OSPF neighbor table, states, and DR/BDR information.",
            "3.2 OSPF", 25.0, 1, "apply"),
        make_q(
            "What is the primary metric used by OSPF to calculate the best path?",
            [("Hop count", False), ("Bandwidth", False), ("Cost", True), ("Delay", False)],
            "OSPF uses cost as its metric, derived from interface bandwidth. Hop count is used by RIP, and bandwidth/delay are EIGRP metrics.",
            "3.2 OSPF", 25.0, 1, "understand"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # 4.0 IP Services
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q(
            "Which NAT type maps multiple private addresses to a single public IP address using different source ports?",
            [("Static NAT", False), ("Dynamic NAT", False), ("PAT", True), ("NAT overload", False)],
            "PAT (Port Address Translation), also called NAT overload, maps multiple private addresses to one public IP using unique source port numbers.",
            "4.1 NAT", 10.0, 2, "understand"),
        make_q(
            "What is the primary purpose of DHCP?",
            [("To resolve hostnames to IP addresses", False), ("To automatically assign IP configuration", True),
             ("To synchronize time across devices", False), ("To encrypt network traffic", False)],
            "DHCP automatically assigns IP addresses, subnet masks, default gateways, and DNS servers to clients. DNS resolves names, NTP synchronizes time.",
            "4.2 NTP/DHCP/DNS", 10.0, 1, "understand"),
        make_q(
            "Which protocol synchronizes time between network devices and uses UDP port 123?",
            [("SNMP", False), ("Syslog", False), ("NTP", True), ("DNS", False)],
            "NTP (Network Time Protocol) uses UDP port 123 to synchronize clocks. SNMP uses 161/162, Syslog uses 514, DNS uses 53.",
            "4.2 NTP/DHCP/DNS", 10.0, 1, "remember"),
        make_q(
            "Which protocol is used to collect and organize management information from network devices?",
            [("SSH", False), ("FTP", False), ("SNMP", True), ("TFTP", False)],
            "SNMP (Simple Network Management Protocol) collects and organizes device management information using MIBs and OIDs.",
            "4.3 SNMP/Syslog/SSH", 10.0, 1, "remember"),
        make_q(
            "Which syslog severity level is the most critical?",
            [("Warning", False), ("Error", False), ("Critical", False), ("Emergency", True)],
            "Syslog severity levels 0-7: Emergency (0), Alert, Critical, Error, Warning, Notice, Informational, Debug (7).",
            "4.3 SNMP/Syslog/SSH", 10.0, 2, "remember"),
        make_q(
            "Which feature prioritizes voice traffic over data traffic to reduce latency and jitter?",
            [("NAT", False), ("DHCP", False), ("QoS", True), ("SNMP", False)],
            "QoS (Quality of Service) prioritizes traffic such as voice and video to minimize latency, jitter, and packet loss.",
            "4.4 QoS", 10.0, 2, "understand"),
        make_q(
            "Which command configures a router interface as a DHCP relay agent?",
            [("ip helper-address", True), ("ip dhcp relay", False), ("dhcp relay-agent", False), ("ip forward-protocol", False)],
            "The ip helper-address command on a router interface forwards DHCP broadcasts to a specified DHCP server.",
            "4.2 NTP/DHCP/DNS", 10.0, 2, "apply"),
        make_q(
            "Which DNS record type maps a hostname to an IPv4 address?",
            [("AAAA", False), ("CNAME", False), ("A", True), ("MX", False)],
            "An A record maps a hostname to an IPv4 address. AAAA maps to IPv6, CNAME is an alias, and MX is for mail servers.",
            "4.2 NTP/DHCP/DNS", 10.0, 1, "remember"),
        make_q(
            "Which logging destination on a Cisco device stores messages locally in RAM?",
            [("Syslog server", False), ("Console", False), ("Buffered logging", True), ("SNMP trap", False)],
            "Buffered logging stores syslog messages in the device RAM. Console and terminal logging output to sessions, and SNMP traps send to managers.",
            "4.3 SNMP/Syslog/SSH", 10.0, 2, "apply"),
        make_q(
            "What does the Differentiated Services Code Point (DSCP) field in an IP header identify?",
            [("Source MAC address", False), ("QoS marking", True), ("Fragment offset", False), ("TTL value", False)],
            "DSCP is a 6-bit field in the IP header used for QoS classification and marking. It replaces the older IP precedence field.",
            "4.4 QoS", 10.0, 2, "understand"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # 5.0 Security Fundamentals
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q(
            "Which security feature prevents MAC flooding attacks by limiting MAC addresses on a switch port?",
            [("DHCP snooping", False), ("Port security", True), ("Dynamic ARP inspection", False), ("IP Source Guard", False)],
            "Port security limits the number of MAC addresses on a port, preventing MAC flooding and CAM table exhaustion attacks.",
            "5.2 Access Control", 15.0, 2, "apply"),
        make_q(
            "What is the purpose of a demilitarized zone (DMZ) in network design?",
            [("To encrypt all internal traffic", False), ("To host public-facing services between trusted and untrusted networks", True),
             ("To replace firewalls", False), ("To create a wireless guest network", False)],
            "A DMZ hosts public-facing services (web, email) between the internal trusted network and the untrusted Internet, limiting exposure.",
            "5.1 Security Concepts", 15.0, 2, "understand"),
        make_q(
            "Which type of attack involves sending forged ARP messages to associate the attacker's MAC with a legitimate IP?",
            [("VLAN hopping", False), ("ARP spoofing", True), ("DHCP starvation", False), ("STP manipulation", False)],
            "ARP spoofing sends falsified ARP messages to link the attacker's MAC address with a legitimate IP, enabling man-in-the-middle attacks.",
            "5.1 Security Concepts", 15.0, 2, "understand"),
        make_q(
            "Which switch feature validates ARP packets against a trusted DHCP binding database?",
            [("Port security", False), ("DHCP snooping", False), ("Dynamic ARP inspection", True), ("BPDU Guard", False)],
            "Dynamic ARP Inspection (DAI) intercepts ARP packets and validates them against the DHCP snooping binding table to prevent ARP spoofing.",
            "5.2 Access Control", 15.0, 3, "apply"),
        make_q(
            "Which access control method uses the principle of least privilege by default?",
            [("Permit all", False), ("Role-based access control", True), ("Anonymous access", False), ("Shared credentials", False)],
            "Role-based access control (RBAC) grants permissions based on job roles, following the principle of least privilege.",
            "5.2 Access Control", 15.0, 2, "understand"),
        make_q(
            "Which wireless security mode provides individual encryption keys for each user?",
            [("WPA-Personal", False), ("WPA2-Enterprise", True), ("WEP", False), ("Open", False)],
            "WPA2-Enterprise uses 802.1X authentication, providing unique credentials and encryption keys per user via a RADIUS server.",
            "5.3 Wireless Security", 15.0, 2, "understand"),
        make_q(
            "What does TACACS+ provide that RADIUS does not?",
            [("Combines authentication and accounting only", False), ("Separates authentication, authorization, and accounting", True),
             ("Uses UDP only", False), ("Encrypts only the password", False)],
            "TACACS+ separates AAA functions and encrypts the entire payload. RADIUS combines authentication and authorization and encrypts only the password.",
            "5.2 Access Control", 15.0, 3, "understand"),
        make_q(
            "Which security mechanism should be enabled on a switch to prevent rogue DHCP servers?",
            [("Port security", False), ("DHCP snooping", True), ("DAI", False), ("IP Source Guard", False)],
            "DHCP snooping classifies switch ports as trusted or untrusted, blocking rogue DHCP server replies on untrusted ports.",
            "5.2 Access Control", 15.0, 2, "apply"),
        make_q(
            "Which type of malware self-replicates across networks without user interaction?",
            [("Trojan", False), ("Virus", False), ("Worm", True), ("Ransomware", False)],
            "Worms self-replicate and spread across networks without requiring a host program or user action, unlike viruses.",
            "5.1 Security Concepts", 15.0, 1, "understand"),
        make_q(
            "Which command line should be used to secure remote management of a Cisco device?",
            [("transport input telnet", False), ("transport input ssh", True), ("transport input all", False), ("line vty 0 4 login local", False)],
            "Using transport input ssh on VTY lines allows only encrypted SSH access. Telnet sends credentials in plaintext.",
            "5.2 Access Control", 15.0, 2, "apply"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # 6.0 Automation and Programmability
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q(
            "Which protocol is commonly used by REST APIs to exchange data in a structured text format?",
            [("FTP", False), ("SSH", False), ("HTTP with JSON", True), ("Telnet", False)],
            "REST APIs typically use HTTP/HTTPS and exchange data encoded as JSON or XML. JSON is the most common modern choice.",
            "6.2 APIs", 10.0, 1, "remember"),
        make_q(
            "Which HTTP method is used to create a new resource in a REST API?",
            [("GET", False), ("PUT", False), ("POST", True), ("DELETE", False)],
            "POST creates resources, GET retrieves, PUT/PATCH updates, and DELETE removes resources.",
            "6.2 APIs", 10.0, 1, "remember"),
        make_q(
            "Which data format uses key-value pairs and is easily readable by humans?",
            [("XML", False), ("YAML", True), ("BSON", False), ("Protobuf", False)],
            "YAML uses indentation and key-value pairs, making it human-readable. JSON is also readable but uses braces. XML uses tags.",
            "6.1 Automation", 10.0, 1, "remember"),
        make_q(
            "Which Cisco platform provides centralized network management, automation, and assurance?",
            [("Cisco IOS", False), ("Cisco DNA Center", True), ("Cisco ASA", False), ("Cisco WLC", False)],
            "Cisco DNA Center provides intent-based networking, automation, assurance, and centralized management.",
            "6.1 Automation", 10.0, 2, "understand"),
        make_q(
            "Which term describes treating infrastructure configuration as version-controlled code?",
            [("Manual provisioning", False), ("Infrastructure as Code", True), ("Reactive monitoring", False), ("Hardware-defined networking", False)],
            "Infrastructure as Code (IaC) manages infrastructure through machine-readable configuration files stored in version control.",
            "6.1 Automation", 10.0, 2, "understand"),
        make_q(
            "Which configuration management tool uses playbooks written in YAML?",
            [("Puppet", False), ("Chef", False), ("Ansible", True), ("Terraform", False)],
            "Ansible uses YAML-based playbooks. Puppet uses its own DSL, Chef uses Ruby, and Terraform uses HCL.",
            "6.1 Automation", 10.0, 2, "remember"),
        make_q(
            "Which authentication method for REST APIs uses a token issued by an identity provider?",
            [("Basic auth", False), ("OAuth 2.0", True), ("Digest auth", False), ("Plain text", False)],
            "OAuth 2.0 uses access tokens issued by an authorization server/identity provider, enabling delegated and scoped access.",
            "6.2 APIs", 10.0, 2, "understand"),
        make_q(
            "What is the primary difference between machine learning (ML) and generative AI?",
            [("ML cannot process data", False), ("Generative AI creates new content, while ML typically predicts or classifies", True),
             ("Generative AI only uses rule-based logic", False), ("ML requires no training data", False)],
            "Machine learning models learn patterns to predict or classify. Generative AI models create new content such as text, images, or code.",
            "6.3 AI/ML", 10.0, 2, "understand"),
        make_q(
            "Which HTTP status code indicates a successful GET request?",
            [("200", True), ("201", False), ("404", False), ("500", False)],
            "HTTP 200 OK indicates success. 201 Created is for successful POST, 404 Not Found, 500 Internal Server Error.",
            "6.2 APIs", 10.0, 1, "remember"),
        make_q(
            "Which Cisco API provides model-driven programmatic interfaces for device configuration?",
            [("SNMP", False), ("NETCONF/YANG", True), ("Syslog", False), ("Telnet API", False)],
            "NETCONF uses YANG data models to provide structured, transactional device configuration and state retrieval.",
            "6.2 APIs", 10.0, 3, "understand"),
    ]

    # Additional CCNA v1.1 questions — expanded blueprint coverage
    questions += _generate_subnetting_questions(30)
    questions += _generate_switching_questions()
    questions += _generate_routing_questions()
    questions += _generate_security_automation_questions()

    # Deduplicate by body within this CCNA exam
    seen = set()
    unique = []
    for q in questions:
        if q["body"] not in seen:
            seen.add(q["body"])
            unique.append(q)
    return unique


def _generate_subnetting_questions(count: int) -> list[dict]:
    """Generate deterministic subnetting questions."""
    out = []
    random.seed(42)
    for _ in range(count):
        network = random.choice(["192.168", "10.0", "172.16", "203.0.113", "198.51.100"])
        host_octet = random.randint(1, 240)
        prefix = random.choice([24, 25, 26, 27, 28, 30])
        block = 2 ** (32 - prefix)
        network_addr = (host_octet // block) * block
        broadcast = network_addr + block - 1
        first = network_addr + 1
        last = broadcast - 1
        qtype = random.choice(["first", "last", "broadcast", "hosts"])
        if qtype == "first":
            body = f"What is the first valid host address in the subnet {network}.{host_octet}/{prefix}?"
            correct = f"{network}.{first}"
            opts = [f"{network}.{network_addr}", f"{network}.{first}", f"{network}.{last}", f"{network}.{broadcast}"]
            explanation = f"For /{prefix} the block size is {256 - (block if block <= 256 else 256)}. Network is {network}.{network_addr}, first host is {network}.{first}."
        elif qtype == "last":
            body = f"What is the last valid host address in the subnet {network}.{host_octet}/{prefix}?"
            correct = f"{network}.{last}"
            opts = [f"{network}.{network_addr}", f"{network}.{first}", f"{network}.{last}", f"{network}.{broadcast}"]
            explanation = f"For /{prefix} the block size is {256 - (block if block <= 256 else 256)}. Broadcast is {network}.{broadcast}, last host is {network}.{last}."
        elif qtype == "broadcast":
            body = f"What is the broadcast address for the subnet {network}.{host_octet}/{prefix}?"
            correct = f"{network}.{broadcast}"
            opts = [f"{network}.{network_addr}", f"{network}.{first}", f"{network}.{last}", f"{network}.{broadcast}"]
            explanation = f"For /{prefix} the next network is {network}.{network_addr + block}, so broadcast is {network}.{broadcast}."
        else:
            hosts = block - 2
            body = f"How many usable host addresses are available in a /{prefix} subnet?"
            correct = str(hosts)
            opts = [str(hosts - 1), str(hosts), str(hosts + 1), str(block)]
            explanation = f"A /{prefix} subnet has {block} total addresses. Subtract network and broadcast to get {hosts} usable hosts."
        random.shuffle(opts)
        options = [(o, o == correct) for o in opts]
        out.append(make_q(body, options, explanation, "1.5 IPv4/IPv6 Addressing", 20.0, 3, "apply"))
    random.seed()
    return out


def _generate_switching_questions() -> list[dict]:
    return [
        make_q("Which layer of the OSI model is primarily concerned with MAC addresses?",
               [("Layer 1", False), ("Layer 2", True), ("Layer 3", False), ("Layer 4", False)],
               "MAC addresses are Layer 2 (Data Link) identifiers used for local network delivery.",
               "2.1 Switching Concepts", 20.0, 1, "remember"),
        make_q("What happens when a switch receives a unicast frame and the destination MAC is unknown?",
               [("Drops the frame", False), ("Forwards it out all ports except the source", True),
                ("Sends it to the default gateway", False), ("Buffers it indefinitely", False)],
               "Unknown unicast frames are flooded out all ports in the same VLAN except the ingress port.",
               "2.1 Switching Concepts", 20.0, 2, "understand"),
        make_q("Which command creates VLAN 100 on a Cisco switch?",
               [("vlan database 100", False), ("vlan 100", True), ("create vlan 100", False), ("switchport vlan 100", False)],
               "In global configuration mode, 'vlan 100' creates VLAN 100 on most Cisco switches.",
               "2.2 VLANs", 20.0, 2, "apply"),
        make_q("Which switch port mode actively attempts to negotiate a trunk using DTP?",
               [("access", False), ("trunk", False), ("dynamic desirable", True), ("dynamic auto", False)],
               "dynamic desirable actively sends DTP frames to negotiate trunking. dynamic auto only responds.",
               "2.3 Inter-Switch Connectivity", 20.0, 3, "remember"),
        make_q("Which STP enhancement immediately disables a port that receives a BPDU when enabled?",
               [("BPDU Filter", False), ("BPDU Guard", True), ("Root Guard", False), ("Loop Guard", False)],
               "BPDU Guard disables a PortFast port if it receives a BPDU, protecting against accidental switch connections.",
               "2.4 STP", 20.0, 2, "understand"),
        make_q("Which wireless frame type is used to advertise an SSID?",
               [("Probe request", False), ("Beacon", True), ("Authentication", False), ("Association", False)],
               "APs send beacon frames to advertise their SSID and capabilities. Stations send probe requests.",
               "2.5 Wireless", 20.0, 2, "remember"),
        make_q("What is the maximum data rate of 802.11ac on a single 80 MHz channel with 3x3 MIMO?",
               [("54 Mbps", False), ("300 Mbps", False), ("1.3 Gbps", True), ("9.6 Gbps", False)],
               "802.11ac can reach ~1.3 Gbps with 3 spatial streams and 80 MHz channels. 802.11ax (Wi-Fi 6) reaches higher.",
               "2.5 Wireless", 20.0, 3, "remember"),
        make_q("Which command assigns a switch port to VLAN 50 as an access port?",
               [("switchport mode vlan 50", False), ("switchport access vlan 50", True),
                ("switchport trunk vlan 50", False), ("vlan 50 interface", False)],
               "'switchport access vlan 50' assigns an access port to VLAN 50. The port must also be set to access mode.",
               "2.2 VLANs", 20.0, 1, "apply"),
    ]


def _generate_routing_questions() -> list[dict]:
    return [
        make_q("Which routing protocol uses the Dijkstra SPF algorithm?",
               [("RIP", False), ("EIGRP", False), ("OSPF", True), ("BGP", False)],
               "OSPF uses Dijkstra's SPF algorithm to compute shortest paths from the LSDB.",
               "3.2 OSPF", 25.0, 1, "remember"),
        make_q("What is the default administrative distance of a directly connected route?",
               [("0", True), ("1", False), ("5", False), ("20", False)],
               "Directly connected routes have an AD of 0, static routes 1, eBGP 20, EIGRP internal 90.",
               "3.1 Routing Fundamentals", 25.0, 1, "remember"),
        make_q("Which command displays the IPv6 routing table?",
               [("show ip route", False), ("show ipv6 route", True), ("show route ipv6", False), ("show ip route v6", False)],
               "'show ipv6 route' displays the IPv6 routing table on Cisco IOS.",
               "3.1 Routing Fundamentals", 25.0, 1, "apply"),
        make_q("Which BGP path attribute is locally significant to a router and not advertised to peers?",
               [("AS_Path", False), ("Local Preference", False), ("Weight", True), ("MED", False)],
               "Weight is Cisco-proprietary, local to a router, and not advertised to BGP peers. Local Preference is advertised to iBGP peers.",
               "3.4 BGP", 25.0, 3, "understand"),
        make_q("Which OSPF area type does not accept external (Type 5) LSAs?",
               [("Standard area", False), ("Stub area", True), ("Backbone area", False), ("Totally NSSA", False)],
               "Stub areas block Type 5 external LSAs and use a default route. Totally stubby areas also block Type 3 summary LSAs.",
               "3.2 OSPF", 25.0, 3, "understand"),
        make_q("What is the purpose of a summary route?",
               [("To increase routing table size", False), ("To reduce routing table size", True),
                ("To disable routing updates", False), ("To encrypt routing traffic", False)],
               "Route summarization aggregates multiple routes into a single advertisement, reducing routing table size and update traffic.",
               "3.1 Routing Fundamentals", 25.0, 2, "understand"),
    ]


def _generate_security_automation_questions() -> list[dict]:
    return [
        make_q("Which AAA protocol encrypts the entire communication between client and server?",
               [("RADIUS", False), ("TACACS+", True), ("LDAP", False), ("Kerberos", False)],
               "TACACS+ encrypts the entire AAA payload. RADIUS encrypts only the password, and LDAP/Kerberos serve different purposes.",
               "5.2 Access Control", 15.0, 2, "remember"),
        make_q("Which feature prevents a DHCP starvation attack by limiting DHCP replies to trusted ports?",
               [("DAI", False), ("DHCP snooping", True), ("Port security", False), ("IP Source Guard", False)],
               "DHCP snooping marks ports as trusted or untrusted and drops DHCP server replies on untrusted ports.",
               "5.2 Access Control", 15.0, 2, "apply"),
        make_q("What does the command 'login block-for 120 attempts 3 within 60' do?",
               [("Blocks all logins for 120 seconds", False),
                ("Blocks login attempts for 120 seconds after 3 failed attempts within 60 seconds", True),
                ("Allows only 3 logins per minute", False), ("Disables console login", False)],
               "Login block-for implements quiet-mode access control: after the threshold of failed attempts is reached, logins are blocked for the specified time.",
               "5.2 Access Control", 15.0, 3, "apply"),
        make_q("Which REST API authentication method sends a username and password Base64-encoded in the header?",
               [("OAuth 2.0", False), ("Basic authentication", True), ("Token-based", False), ("Digest authentication", False)],
               "Basic authentication encodes the username:password string in Base64 and sends it in the Authorization header.",
               "6.2 APIs", 10.0, 2, "understand"),
        make_q("Which data serialization format is commonly used by REST APIs and resembles JavaScript object notation?",
               [("XML", False), ("YAML", False), ("JSON", True), ("HTML", False)],
               "JSON (JavaScript Object Notation) is lightweight, text-based, and the most common format for REST API payloads.",
               "6.2 APIs", 10.0, 1, "remember"),
        make_q("Which component of Cisco DNA Center provides predictive analytics and baselining?",
               [("Automation", False), ("Assurance", True), ("Fabric", False), ("Identity Services", False)],
               "Cisco DNA Center Assurance provides monitoring, baselining, and predictive analytics using telemetry.",
               "6.1 Automation", 10.0, 2, "understand"),
        make_q("What is the function of Terraform in network automation?",
               [("Monitor device health", False), ("Provision infrastructure using declarative code", True),
                ("Collect syslog messages", False), ("Authenticate API users", False)],
               "Terraform is an IaC tool that provisions and manages infrastructure using declarative configuration files.",
               "6.1 Automation", 10.0, 2, "understand"),
        make_q("Which type of machine learning generates new content such as text or code?",
               [("Supervised learning", False), ("Unsupervised learning", False), ("Reinforcement learning", False), ("Generative AI", True)],
               "Generative AI models create new content. Supervised, unsupervised, and reinforcement learning focus on prediction, grouping, and decision-making.",
               "6.3 AI/ML", 10.0, 1, "understand"),
    ]


def questions_to_sql(questions: list[dict]) -> str:
    lines = [
        "-- +goose Up",
        "-- +goose StatementBegin",
        "",
        "-- CCNA 200-301 v1.1 question bank",
        f"-- Generated {len(questions)} blueprint-aligned single-choice questions",
        "",
        "DELETE FROM questions WHERE exam_id = 'b0000000-0000-0000-0000-000000000003';",
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
        "DELETE FROM questions WHERE exam_id = 'b0000000-0000-0000-0000-000000000003';",
        "",
        "-- +goose StatementEnd",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    questions = generate_questions()
    print(questions_to_sql(questions))
