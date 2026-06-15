#!/usr/bin/env python3
"""
NetCert — JNCIA-Junos (JN0-106) question generator.
Aligned with official Juniper JN0-106 exam objectives.
"""
import hashlib
import json
import random
import uuid

# Exam/track UUIDs from 027_seed_tracks_exams.sql
EXAM_ID = "b0000000-0000-0000-0000-000000000001"
TRACK_ID = "a0000000-0000-0000-0000-000000000001"


def qid(seed: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_OID, f"jncia-junos:{seed}"))


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
        "exam_id": EXAM_ID,
        "track_id": TRACK_ID,
        "question_type": "single-choice",
        "difficulty": difficulty,
        "bloom_level": bloom,
        "body": body,
        "options": opts,
        "explanation": explanation,
        "reference_urls": urls or ["https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-junos.html"],
        "blueprint_section": section,
        "blueprint_weight": weight,
        "content_hash": content_hash(body, correct_letter),
        "is_active": True,
    }


def generate_questions() -> list[dict]:
    questions: list[dict] = []

    # ═══════════════════════════════════════════════════════════════════════
    # 1. Networking Fundamentals
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("Which device operates at Layer 3 and forwards packets based on IP addresses?",
               [("Hub", False), ("Switch", False), ("Router", True), ("Bridge", False)],
               "Routers operate at Layer 3 and make forwarding decisions based on IP addresses. Switches and bridges operate at Layer 2, hubs at Layer 1.",
               "1.0 Networking Fundamentals", 14.0, 1, "remember"),
        make_q("What is a collision domain?",
               [("A group of devices that share the same IP subnet", False),
                ("A network segment where frames can collide with each other", True),
                ("A Layer 3 broadcast boundary", False), ("A VLAN", False)],
               "A collision domain is a network segment where frames can collide. Switches break up collision domains; routers break up broadcast domains.",
               "1.0 Networking Fundamentals", 14.0, 1, "understand"),
        make_q("Which statement describes a broadcast domain?",
               [("The area where frames can collide", False),
                ("The logical division where broadcast frames are forwarded", True),
                ("A single switch port", False), ("A physical cable segment", False)],
               "A broadcast domain is the logical area where broadcast frames propagate. VLANs and routers create separate broadcast domains.",
               "1.0 Networking Fundamentals", 14.0, 1, "understand"),
        make_q("What is the primary function of a switch?",
               [("To route packets between networks", False),
                ("To forward frames based on MAC addresses", True),
                ("To convert analog to digital signals", False), ("To assign IP addresses", False)],
               "Switches forward frames based on destination MAC addresses. Routers route packets based on IP addresses.",
               "1.0 Networking Fundamentals", 14.0, 1, "remember"),
        make_q("Which protocol resolves an IPv4 address to a MAC address?",
               [("DNS", False), ("DHCP", False), ("ARP", True), ("ICMP", False)],
               "ARP (Address Resolution Protocol) maps IPv4 addresses to MAC addresses on the local segment.",
               "1.0 Networking Fundamentals", 14.0, 1, "remember"),
        make_q("Which protocol performs the same function as ARP in IPv6?",
               [("DHCPv6", False), ("NDP", True), ("ICMPv6", False), ("MLD", False)],
               "IPv6 Neighbor Discovery Protocol (NDP) replaces ARP and resolves IPv6 addresses to link-layer addresses.",
               "1.0 Networking Fundamentals", 14.0, 2, "remember"),
        make_q("Which IPv4 address range is defined as private in RFC 1918?",
               [("100.64.0.0/10", False), ("192.168.0.0/16", True), ("169.254.0.0/16", False), ("224.0.0.0/4", False)],
               "RFC 1918 private ranges are 10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16.",
               "1.0 Networking Fundamentals", 14.0, 1, "remember"),
        make_q("What is the purpose of a subnet mask?",
               [("To encrypt IP traffic", False),
                ("To determine the network and host portions of an IP address", True),
                ("To resolve names to IP addresses", False), ("To establish a TCP connection", False)],
               "A subnet mask separates the network portion from the host portion of an IPv4 address.",
               "1.0 Networking Fundamentals", 14.0, 1, "understand"),
        make_q("Which characteristic describes TCP?",
               [("Connectionless", False), ("Unreliable", False), ("Connection-oriented", True), ("No sequencing", False)],
               "TCP is connection-oriented, reliable, and provides sequencing and flow control. UDP is connectionless and unreliable.",
               "1.0 Networking Fundamentals", 14.0, 1, "remember"),
        make_q("Which protocol uses port 23 by default?",
               [("SSH", False), ("Telnet", True), ("FTP", False), ("SNMP", False)],
               "Telnet uses TCP port 23. SSH uses 22, FTP uses 20/21, and SNMP uses 161/162.",
               "1.0 Networking Fundamentals", 14.0, 1, "remember"),
        make_q("What does 'longest prefix match' mean in routing?",
               [("The route with the lowest metric is chosen", False),
                ("The most specific route matching the destination is chosen", True),
                ("The route with the lowest AD is chosen", False), ("The first route in the table is chosen", False)],
               "Longest prefix match selects the route with the longest matching prefix (most specific subnet) for a destination.",
               "1.0 Networking Fundamentals", 14.0, 2, "understand"),
        make_q("Which address is an IPv6 link-local address?",
               [("2001::1", False), ("fe80::1", True), ("ff02::1", False), ("::1", False)],
               "fe80::/10 addresses are IPv6 link-local. 2001::/3 is global unicast, ff00::/8 is multicast, and ::1 is loopback.",
               "1.0 Networking Fundamentals", 14.0, 1, "remember"),
        make_q("What is the purpose of Class of Service (CoS)?",
               [("To encrypt traffic", False), ("To prioritize certain types of traffic", True),
                ("To assign IP addresses", False), ("To prevent MAC flooding", False)],
               "CoS prioritizes traffic such as voice and video to provide better service quality.",
               "1.0 Networking Fundamentals", 14.0, 2, "understand"),
        make_q("Which statement compares connection-oriented and connectionless protocols correctly?",
               [("TCP is connectionless; UDP is connection-oriented", False),
                ("TCP provides reliability; UDP does not", True),
                ("UDP provides sequencing; TCP does not", False), ("Both TCP and UDP are connectionless", False)],
               "TCP is connection-oriented and reliable. UDP is connectionless and best-effort.",
               "1.0 Networking Fundamentals", 14.0, 1, "understand"),
        make_q("How many usable host addresses are in a /30 IPv4 subnet?",
               [("2", True), ("4", False), ("6", False), ("8", False)],
               "A /30 subnet has 4 addresses total. Subtract network and broadcast to get 2 usable host addresses.",
               "1.0 Networking Fundamentals", 14.0, 2, "apply"),
        make_q("Which Ethernet feature allows full-duplex communication without collisions?",
               [("CSMA/CD", False), ("Full-duplex operation with dedicated send/receive pairs", True),
                ("Half-duplex hubs", False), ("Repeaters", False)],
               "Full-duplex Ethernet uses separate paths for sending and receiving, eliminating collisions. CSMA/CD is used in half-duplex.",
               "1.0 Networking Fundamentals", 14.0, 2, "understand"),
        make_q("What is the purpose of the Ethernet trailer (FCS)?",
               [("To identify the source MAC", False), ("To detect frame corruption", True),
                ("To indicate the VLAN", False), ("To set the frame size", False)],
               "The Frame Check Sequence (FCS) is used to detect errors/corruption in an Ethernet frame.",
               "1.0 Networking Fundamentals", 14.0, 2, "remember"),
        make_q("Which IPv6 address type represents one-to-nearest communication?",
               [("Unicast", False), ("Multicast", False), ("Anycast", True), ("Broadcast", False)],
               "Anycast delivers traffic to the nearest interface in a group. IPv6 does not use broadcast.",
               "1.0 Networking Fundamentals", 14.0, 2, "remember"),
        make_q("What is the first step in converting a decimal IP octet to binary?",
               [("Divide by 256", False), ("Compare against powers of 2", True),
                ("Multiply by 16", False), ("Add 128", False)],
               "Decimal-to-binary conversion for IP addresses uses powers of 2 (128, 64, 32, 16, 8, 4, 2, 1).",
               "1.0 Networking Fundamentals", 14.0, 2, "apply"),
        make_q("Which statement about IPv6 is true?",
               [("IPv6 addresses are 32 bits", False), ("IPv6 uses broadcasts", False),
                ("IPv6 addresses are 128 bits", True), ("IPv6 uses NAT by default", False)],
               "IPv6 addresses are 128 bits. IPv4 addresses are 32 bits. IPv6 uses multicast and anycast, not broadcast.",
               "1.0 Networking Fundamentals", 14.0, 1, "remember"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # 2. Junos OS Fundamentals
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("Which Junos OS component is responsible for running routing protocols?",
               [("Packet Forwarding Engine", False), ("Routing Engine", True),
                ("PIC", False), ("FPC", False)],
               "The Routing Engine (RE) runs the control plane, including routing protocols and the Junos OS kernel. The Packet Forwarding Engine (PFE) handles data plane forwarding.",
               "2.0 Junos OS Fundamentals", 14.0, 1, "remember"),
        make_q("What is the primary role of the Packet Forwarding Engine (PFE)?",
               [("To run routing protocols", False), ("To forward transit traffic at line rate", True),
                ("To store the configuration file", False), ("To manage user sessions", False)],
               "The PFE forwards transit traffic using the forwarding table programmed by the RE. It operates in the data plane.",
               "2.0 Junos OS Fundamentals", 14.0, 1, "understand"),
        make_q("Which traffic type is processed by the Routing Engine rather than the PFE?",
               [("Transit traffic", False), ("Exception traffic", True), ("Label-switched traffic", False), ("Forwarded traffic", False)],
               "Exception traffic, such as packets destined to the router itself or packets requiring special handling, is punted to the RE.",
               "2.0 Junos OS Fundamentals", 14.0, 2, "understand"),
        make_q("Which statement best describes the Junos OS software architecture?",
               [("Monolithic kernel with integrated data plane", False),
                ("Modular design with separate control and forwarding planes", True),
                ("Single-process operating system", False), ("Proprietary hardware with no virtualization", False)],
               "Junos OS uses a modular design with a clear separation between the control plane (RE) and forwarding plane (PFE).",
               "2.0 Junos OS Fundamentals", 14.0, 2, "understand"),
        make_q("What is transit traffic?",
               [("Traffic destined to the router itself", False),
                ("Traffic passing through the router from one interface to another", True),
                ("Traffic dropped by a firewall filter", False), ("Traffic generated by the RE", False)],
               "Transit traffic enters one interface and exits another, forwarded by the PFE based on the forwarding table.",
               "2.0 Junos OS Fundamentals", 14.0, 1, "understand"),
        make_q("Which hardware component provides the physical network interfaces on a Junos device?",
               [("Routing Engine", False), ("FPC", True), ("RE-S", False), ("SSD", False)],
               "Flexible PIC Concentrators (FPCs) house the Physical Interface Cards (PICs) or interfaces on modular Junos platforms.",
               "2.0 Junos OS Fundamentals", 14.0, 2, "remember"),
        make_q("Which process on the Routing Engine builds and maintains the routing table?",
               [("kmd", False), ("rpd", True), ("chassisd", False), ("pfed", False)],
               "The routing protocol daemon (rpd) runs on the RE and manages routing protocols and the routing table.",
               "2.0 Junos OS Fundamentals", 14.0, 2, "remember"),
        make_q("What happens to transit traffic when the routing table changes?",
               [("It is queued until the RE processes it", False),
                ("The RE updates the forwarding table, which programs the PFE", True),
                ("It is converted to exception traffic", False), ("It is dropped until convergence", False)],
               "The RE computes routes, installs the best paths into the forwarding table, and programs the PFE so transit traffic is forwarded correctly.",
               "2.0 Junos OS Fundamentals", 14.0, 2, "understand"),
        make_q("Which statement about the control plane is true?",
               [("It forwards packets at wire speed", False),
                ("It handles routing protocols, system management, and configuration", True),
                ("It is implemented entirely in hardware", False), ("It has no interaction with the forwarding plane", False)],
               "The control plane handles routing protocols, management, and configuration. It programs the forwarding plane but does not forward transit traffic at line rate.",
               "2.0 Junos OS Fundamentals", 14.0, 2, "understand"),
        make_q("Which component stores the active configuration and route tables?",
               [("PFE", False), ("RE", True), ("MIC", False), ("PIC", False)],
               "The Routing Engine stores the active configuration, runs processes, and maintains routing and forwarding tables.",
               "2.0 Junos OS Fundamentals", 14.0, 1, "remember"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # 3. User Interfaces
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("Which CLI mode allows you to make configuration changes?",
               [("Operational mode", False), ("Configuration mode", True), ("Monitor mode", False), ("Shell mode", False)],
               "Configuration mode (prompt ending in #) is used to modify the candidate configuration. Operational mode (>) is used for monitoring.",
               "3.0 User Interfaces", 14.0, 1, "remember"),
        make_q("Which command enters configuration mode on a Junos device?",
               [("enable", False), ("configure", True), ("config terminal", False), ("edit", False)],
               "The 'configure' command enters configuration mode on Junos. Cisco IOS uses 'configure terminal'.",
               "3.0 User Interfaces", 14.0, 1, "apply"),
        make_q("Which command shows the active configuration in set format?",
               [("show configuration", False), ("show | display set", True),
                ("show config set", False), ("display set configuration", False)],
               "'show | display set' displays the configuration as a series of set commands. 'show configuration' displays it in hierarchical format.",
               "3.0 User Interfaces", 14.0, 2, "apply"),
        make_q("What is the difference between candidate and active configuration?",
               [("They are the same thing", False),
                ("Candidate is the proposed config; active is the committed config", True),
                ("Candidate is read-only; active is editable", False), ("Active is stored on the PFE", False)],
               "Junos maintains a candidate configuration that you edit. Changes are not active until you commit them.",
               "3.0 User Interfaces", 14.0, 1, "understand"),
        make_q("Which command commits the candidate configuration?",
               [("apply", False), ("save", False), ("commit", True), ("activate", False)],
               "The 'commit' command validates and applies the candidate configuration as the active configuration.",
               "3.0 User Interfaces", 14.0, 1, "apply"),
        make_q("Which command allows you to quickly return to the previous committed configuration?",
               [("rollback 1", True), ("rollback 0", False), ("revert", False), ("undo", False)],
               "'rollback 1' loads the previous committed configuration as the candidate. 'rollback 0' loads the current active config.",
               "3.0 User Interfaces", 14.0, 2, "apply"),
        make_q("Which command loads a rescue configuration?",
               [("load rescue", True), ("rollback rescue", False), ("commit rescue", False), ("load factory-default", False)],
               "'load rescue' loads the previously saved rescue configuration into the candidate config.",
               "3.0 User Interfaces", 14.0, 2, "apply"),
        make_q("How do you filter command output to show only lines containing 'ge-0/0/0'?",
               [("| except ge-0/0/0", False), ("| match ge-0/0/0", True), ("| find ge-0/0/0", False), ("| grep ge-0/0/0", False)],
               "Junos uses pipe filters. '| match' displays only lines matching the expression. '| except' excludes matches, '| find' starts at the first match.",
               "3.0 User Interfaces", 14.0, 2, "apply"),
        make_q("Which CLI help feature displays all commands starting with a given string?",
               [("?", True), ("help", False), ("tab", False), ("space", False)],
               "Typing '?' at the prompt or after a command displays available commands or options. Tab completes commands.",
               "3.0 User Interfaces", 14.0, 1, "remember"),
        make_q("Which command compares the candidate configuration with the active configuration?",
               [("show | compare", True), ("show diff", False), ("compare config", False), ("show configuration diff", False)],
               "'show | compare' displays the differences between the candidate configuration and the active configuration.",
               "3.0 User Interfaces", 14.0, 2, "apply"),
        make_q("What is J-Web?",
               [("Junos command-line interface", False), ("Junos web-based management interface", True),
                ("Junos scripting language", False), ("Junos hardware diagnostic tool", False)],
               "J-Web is the web-based graphical user interface for managing Junos devices.",
               "3.0 User Interfaces", 14.0, 1, "remember"),
        make_q("Which command exits configuration mode and returns to operational mode?",
               [("exit", True), ("quit", False), ("end", False), ("disable", False)],
               "In Junos, 'exit' or 'quit' exits configuration mode. 'end' is not used.",
               "3.0 User Interfaces", 14.0, 1, "apply"),
        make_q("Which command displays the contents of a configuration file on the local disk?",
               [("file show", True), ("show file", False), ("cat", False), ("display file", False)],
               "'file show /path/to/file' displays the contents of a file on the Junos device.",
               "3.0 User Interfaces", 14.0, 2, "apply"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # 4. Configuration Basics
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("Which command returns a Junos device to factory-default settings?",
               [("load factory-default", True), ("set factory-default", False),
                ("reset config", False), ("delete configuration", False)],
               "'load factory-default' replaces the candidate configuration with the factory-default configuration.",
               "4.0 Configuration Basics", 14.0, 2, "apply"),
        make_q("Which command configures a login class that allows only read-only access?",
               [("set system login class readonly permissions all", False),
                ("set system login class readonly permissions read-only", True),
                ("set system login class readonly access read", False),
                ("set system login user readonly class read-only", False)],
               "Login classes are configured under 'set system login class <name> permissions ...'. 'read-only' is a valid permission.",
               "4.0 Configuration Basics", 14.0, 2, "apply"),
        make_q("Which authentication method uses a RADIUS server to validate user credentials?",
               [("Local password", False), ("RADIUS", True), ("Rescue config", False), ("SSH keys only", False)],
               "RADIUS and TACACS+ are external authentication methods. Local authentication uses the local password database.",
               "4.0 Configuration Basics", 14.0, 1, "remember"),
        make_q("Which Junos configuration element allows you to apply common settings to multiple interfaces?",
               [("Apply-groups", True), ("Configuration templates", False), ("Interface ranges only", False), ("Macros", False)],
               "Apply-groups let you define a common configuration and apply it to multiple hierarchies, such as interfaces.",
               "4.0 Configuration Basics", 14.0, 2, "understand"),
        make_q("Which command configures an IPv4 address on interface ge-0/0/0?",
               [("set interface ge-0/0/0 ip address 192.168.1.1/24", False),
                ("set interfaces ge-0/0/0 unit 0 family inet address 192.168.1.1/24", True),
                ("set interfaces ge-0/0/0 address 192.168.1.1 255.255.255.0", False),
                ("set ge-0/0/0 ip 192.168.1.1/24", False)],
               "Junos configures IP addresses under 'unit 0 family inet address'. IPv6 uses 'family inet6'.",
               "4.0 Configuration Basics", 14.0, 2, "apply"),
        make_q("Which command enables SSH access on a Junos device?",
               [("set system services ssh", True), ("set services ssh enable", False),
                ("set system ssh enable", False), ("set service ssh", False)],
               "SSH is enabled under 'set system services ssh'. Telnet is similarly 'set system services telnet'.",
               "4.0 Configuration Basics", 14.0, 1, "apply"),
        make_q("What is the purpose of NTP on a Junos device?",
               [("To resolve hostnames", False), ("To synchronize system time", True),
                ("To back up configurations", False), ("To encrypt management traffic", False)],
               "NTP synchronizes the device clock with time servers, which is critical for logging and certificates.",
               "4.0 Configuration Basics", 14.0, 1, "remember"),
        make_q("Which command configures SNMP community 'public' with read-only access?",
               [("set snmp community public authorization read-only", False),
                ("set snmp community public access read-only", False),
                ("set snmp community public", True), ("set snmp public read-only", False)],
               "In Junos, 'set snmp community public' creates a community. Authorization can be further restricted with client lists and access levels.",
               "4.0 Configuration Basics", 14.0, 2, "apply"),
        make_q("What is a rescue configuration?",
               [("The factory-default configuration", False),
                ("A user-saved fallback configuration", True),
                ("The last committed configuration", False), ("The candidate configuration", False)],
               "A rescue configuration is a special configuration saved by the administrator that can be loaded when the device is inaccessible.",
               "4.0 Configuration Basics", 14.0, 2, "understand"),
        make_q("Which command saves the current candidate configuration as the rescue configuration?",
               [("save rescue", False), ("request system configuration rescue save", True),
                ("commit rescue", False), ("set rescue-configuration", False)],
               "'request system configuration rescue save' saves the current active configuration as the rescue configuration.",
               "4.0 Configuration Basics", 14.0, 2, "apply"),
        make_q("Which command archives the configuration to a remote URL?",
               [("set system archival configuration transfer-interval", False),
                ("set system archival configuration archive-sites", True),
                ("set system backup configuration", False), ("set system config-archive", False)],
               "'set system archival configuration archive-sites' configures destinations for automatic configuration archival.",
               "4.0 Configuration Basics", 14.0, 3, "apply"),
        make_q("Which login class permission allows a user to enter configuration mode?",
               [("view", False), ("control", True), ("read-only", False), ("super-user", False)],
               "The 'control' permission allows configuration mode access. 'super-user' is a predefined class with all permissions.",
               "4.0 Configuration Basics", 14.0, 2, "remember"),
        make_q("Which command enables syslog to a remote server at 10.0.0.5?",
               [("set system syslog host 10.0.0.5 any any", True),
                ("set system syslog server 10.0.0.5", False),
                ("set system logging remote 10.0.0.5", False), ("set syslog 10.0.0.5", False)],
               "Junos syslog remote hosts are configured under 'set system syslog host <ip> facility severity'.",
               "4.0 Configuration Basics", 14.0, 2, "apply"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # 5. Operational Monitoring and Maintenance
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("Which command displays interface status and IP addresses?",
               [("show interfaces terse", True), ("show route", False),
                ("show configuration interfaces", False), ("show system interfaces", False)],
               "'show interfaces terse' displays a summary of interfaces, admin/link states, and IP addresses.",
               "5.0 Operational Monitoring and Maintenance", 14.0, 1, "apply"),
        make_q("Which command displays the routing table?",
               [("show route", True), ("show interfaces", False),
                ("show configuration protocols", False), ("show system users", False)],
               "'show route' displays the routing table. 'show route forwarding-table' shows the forwarding table.",
               "5.0 Operational Monitoring and Maintenance", 14.0, 1, "apply"),
        make_q("Which command continuously monitors interface traffic in real time?",
               [("show interfaces statistics", False), ("monitor interface", True),
                ("trace interface", False), ("watch interface", False)],
               "'monitor interface' displays real-time interface statistics, similar to top for interfaces.",
               "5.0 Operational Monitoring and Maintenance", 14.0, 2, "apply"),
        make_q("Which command verifies Layer 3 reachability to a remote host?",
               [("traceroute", False), ("ping", True), ("telnet", False), ("show arp", False)],
               "'ping' tests Layer 3 reachability using ICMP echo requests. 'traceroute' shows the path/route taken.",
               "5.0 Operational Monitoring and Maintenance", 14.0, 1, "apply"),
        make_q("Which command displays the Junos OS version?",
               [("show version", True), ("show system version", False),
                ("show os", False), ("show software", False)],
               "'show version' displays the Junos OS version, hardware model, and uptime.",
               "5.0 Operational Monitoring and Maintenance", 14.0, 1, "apply"),
        make_q("Which command displays system alarms?",
               [("show alarms", False), ("show system alarms", True),
                ("show chassis alarms", False), ("show error", False)],
               "'show system alarms' displays active red and yellow alarms on the device.",
               "5.0 Operational Monitoring and Maintenance", 14.0, 1, "apply"),
        make_q("Which command is used to upgrade Junos OS from a package file?",
               [("request system software add", True), ("load software", False),
                ("install package", False), ("upgrade system", False)],
               "'request system software add <package>' installs or upgrades the Junos OS image.",
               "5.0 Operational Monitoring and Maintenance", 14.0, 2, "apply"),
        make_q("Which command safely powers off a Junos device?",
               [("request system halt", True), ("shutdown now", False),
                ("power off", False), ("request chassis power-off", False)],
               "'request system halt' gracefully shuts down the device. 'request system reboot' restarts it.",
               "5.0 Operational Monitoring and Maintenance", 14.0, 2, "apply"),
        make_q("Which command recovers a lost root password on a Junos device?",
               [("request system password-reset", False), ("Boot into single-user mode and use recovery procedure", True),
                ("login root with blank password", False), ("delete system root-authentication", False)],
               "Root password recovery requires interrupting the boot process and entering single-user/recovery mode.",
               "5.0 Operational Monitoring and Maintenance", 14.0, 2, "understand"),
        make_q("Which command displays logged CLI commands executed by users?",
               [("show log messages", False), ("show log interactive-commands", True),
                ("show system history", False), ("show cli log", False)],
               "'show log interactive-commands' displays the audit log of CLI commands entered by users.",
               "5.0 Operational Monitoring and Maintenance", 14.0, 2, "apply"),
        make_q("Which command shows CPU and memory usage of the Routing Engine?",
               [("show chassis routing-engine", True), ("show system processes", False),
                ("show route summary", False), ("show chassis fpc", False)],
               "'show chassis routing-engine' displays RE CPU, memory, and uptime information.",
               "5.0 Operational Monitoring and Maintenance", 14.0, 2, "apply"),
        make_q("Which command captures live packets on an interface for troubleshooting?",
               [("monitor traffic", True), ("capture packets", False),
                ("show traffic", False), ("trace traffic", False)],
               "'monitor traffic interface <name>' captures packets on an interface, similar to tcpdump.",
               "5.0 Operational Monitoring and Maintenance", 14.0, 2, "apply"),
        make_q("What information does 'show chassis hardware' provide?",
               [("Active routing protocols", False), ("Hardware inventory including FPCs and PICs", True),
                ("Interface IP addresses", False), ("System users", False)],
               "'show chassis hardware' displays the hardware inventory, including FPCs, PICs, and serial numbers.",
               "5.0 Operational Monitoring and Maintenance", 14.0, 2, "understand"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # 6. Routing Fundamentals
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("Which table does Junos use to make forwarding decisions for transit traffic?",
               [("Routing table", False), ("Forwarding table", True),
                ("ARP table", False), ("MAC table", False)],
               "The forwarding table is derived from the routing table and is used by the PFE to forward transit traffic.",
               "6.0 Routing Fundamentals", 14.0, 2, "understand"),
        make_q("What is route preference in Junos?",
               [("The metric used by a protocol", False),
                ("The administrative distance used to select between routes from different protocols", True),
                ("The cost of an interface", False), ("The BGP local preference", False)],
               "Route preference is Junos' term for administrative distance. Lower preference values are preferred.",
               "6.0 Routing Fundamentals", 14.0, 2, "understand"),
        make_q("Which route preference value is used for directly connected networks?",
               [("0", True), ("1", False), ("5", False), ("10", False)],
               "Directly connected routes have a preference of 0, static routes 5, OSPF internal 10, IS-IS level 1 15.",
               "6.0 Routing Fundamentals", 14.0, 1, "remember"),
        make_q("Which route preference value is used for OSPF internal routes?",
               [("5", False), ("10", True), ("15", False), ("20", False)],
               "OSPF internal routes have a default preference of 10. IS-IS level 1 is 15, IS-IS level 2 is 18, RIP is 100.",
               "6.0 Routing Fundamentals", 14.0, 1, "remember"),
        make_q("Which command displays the forwarding table?",
               [("show route", False), ("show route forwarding-table", True),
                ("show forwarding", False), ("show fpc forwarding", False)],
               "'show route forwarding-table' displays the forwarding table used by the PFE.",
               "6.0 Routing Fundamentals", 14.0, 2, "apply"),
        make_q("What is the purpose of a routing instance?",
               [("To increase interface speed", False),
                ("To create separate routing tables and forwarding domains", True),
                ("To encrypt routing updates", False), ("To disable dynamic routing", False)],
               "Routing instances create separate routing and forwarding tables, used for VPNs, virtualization, and separation.",
               "6.0 Routing Fundamentals", 14.0, 2, "understand"),
        make_q("Which command configures a default static route with next-hop 10.1.1.1?",
               [("set routing-options static route 0.0.0.0/0 next-hop 10.1.1.1", True),
                ("set static route 0.0.0.0 0.0.0.0 10.1.1.1", False),
                ("set ip route 0.0.0.0/0 10.1.1.1", False), ("set route 0.0.0.0 next-hop 10.1.1.1", False)],
               "Junos static routes are configured under 'routing-options static route <prefix> next-hop <address>'.",
               "6.0 Routing Fundamentals", 14.0, 2, "apply"),
        make_q("Which dynamic routing protocol uses hop count as its metric?",
               [("OSPF", False), ("IS-IS", False), ("RIP", True), ("BGP", False)],
               "RIP uses hop count as its metric. OSPF uses cost, IS-IS uses default metric, and BGP uses path attributes.",
               "6.0 Routing Fundamentals", 14.0, 1, "remember"),
        make_q("Which command displays route preference and protocol information?",
               [("show route detail", True), ("show route summary", False),
                ("show route protocol", False), ("show route table", False)],
               "'show route detail' shows detailed route information including protocol, preference, metric, and next-hop.",
               "6.0 Routing Fundamentals", 14.0, 2, "apply"),
        make_q("What is the default route preference for a static route?",
               [("0", False), ("5", True), ("10", False), ("100", False)],
               "Static routes have a default preference of 5 in Junos. Directly connected routes are 0.",
               "6.0 Routing Fundamentals", 14.0, 1, "remember"),
    ]

    # ═══════════════════════════════════════════════════════════════════════
    # 7. Routing Policy and Firewall Filters
    # ═══════════════════════════════════════════════════════════════════════
    questions += [
        make_q("What is the default OSPF export policy in Junos?",
               [("Reject all routes", False), ("Accept and export all active routes", True),
                ("Accept only directly connected routes", False), ("Export nothing", False)],
               "Junos default export policies for protocols like OSPF and IS-IS accept and redistribute all active routes. Import policies may differ.",
               "7.0 Routing Policy and Firewall Filters", 16.0, 2, "understand"),
        make_q("Which statement describes a routing policy in Junos?",
               [("It filters transit packets", False),
                ("It controls which routes are accepted, rejected, or modified", True),
                ("It encrypts routing updates", False), ("It assigns IP addresses", False)],
               "Routing policies control route advertisement and acceptance between protocols and routing tables.",
               "7.0 Routing Policy and Firewall Filters", 16.0, 1, "understand"),
        make_q("Which configuration hierarchy defines a routing policy?",
               [("policy-options policy-statement", True), ("routing-options policy", False),
                ("firewall policy", False), ("protocols policy", False)],
               "Routing policies are defined under 'policy-options policy-statement <name>'.",
               "7.0 Routing Policy and Firewall Filters", 16.0, 2, "apply"),
        make_q("Which routing policy term action rejects a route without propagating it?",
               [("accept", False), ("reject", True), ("next term", False), ("modify", False)],
               "The 'reject' action stops processing and does not advertise or install the route. 'accept' permits it.",
               "7.0 Routing Policy and Firewall Filters", 16.0, 2, "remember"),
        make_q("Which command applies a routing policy to BGP export?",
               [("set protocols bgp export POLICY", True),
                ("set policy-options bgp export POLICY", False),
                ("set routing-options bgp policy POLICY", False), ("set protocols bgp import POLICY", False)],
               "Routing policies are applied to protocols with 'set protocols <protocol> export <policy>' or 'import <policy>'.",
               "7.0 Routing Policy and Firewall Filters", 16.0, 2, "apply"),
        make_q("What is a firewall filter in Junos?",
               [("A routing policy that filters routes", False),
                ("A packet filter that controls traffic based on match conditions", True),
                ("A NAT configuration", False), ("A QoS policy", False)],
               "Firewall filters match packets and take actions such as accept, discard, reject, or count.",
               "7.0 Routing Policy and Firewall Filters", 16.0, 1, "understand"),
        make_q("Where are firewall filters configured in Junos?",
               [("policy-options", False), ("firewall filter", True),
                ("security policies", False), ("routing-options", False)],
               "Firewall filters are configured under 'firewall filter <name>' and applied to interfaces.",
               "7.0 Routing Policy and Firewall Filters", 16.0, 2, "apply"),
        make_q("Which firewall filter action silently drops a packet?",
               [("reject", False), ("discard", True), ("accept", False), ("drop", False)],
               "'discard' silently drops the packet. 'reject' drops and sends an ICMP error. 'accept' forwards the packet.",
               "7.0 Routing Policy and Firewall Filters", 16.0, 2, "remember"),
        make_q("Which firewall filter action drops a packet and sends an ICMP message?",
               [("discard", False), ("reject", True), ("deny", False), ("drop", False)],
               "'reject' drops the packet and sends an ICMP unreachable message to the source.",
               "7.0 Routing Policy and Firewall Filters", 16.0, 2, "remember"),
        make_q("What is unicast reverse-path forwarding (uRPF) used for?",
               [("To forward multicast traffic", False),
                ("To prevent spoofed source IP addresses", True),
                ("To encrypt traffic", False), ("To balance traffic across equal-cost paths", False)],
               "uRPF checks whether the source IP address of a packet is reachable through the incoming interface, helping prevent spoofing.",
               "7.0 Routing Policy and Firewall Filters", 16.0, 2, "understand"),
        make_q("Which match condition in a firewall filter checks the source IP address?",
               [("source-port", False), ("source-address", True), ("destination-address", False), ("protocol", False)],
               "'source-address' matches the source IP. 'destination-address' matches the destination, and 'source-port' matches the L4 source port.",
               "7.0 Routing Policy and Firewall Filters", 16.0, 1, "apply"),
        make_q("Which term in a routing policy causes the router to continue evaluating the next term if the current term matches?",
               [("accept", False), ("reject", False), ("next term", True), ("skip", False)],
               "'next term' continues policy evaluation. 'accept' and 'reject' terminate evaluation for that route.",
               "7.0 Routing Policy and Firewall Filters", 16.0, 2, "remember"),
        make_q("Which command applies a firewall filter to an interface input direction?",
               [("set interfaces ge-0/0/0 unit 0 family inet filter input FILTER", True),
                ("set firewall interface ge-0/0/0 input FILTER", False),
                ("set interfaces ge-0/0/0 filter FILTER", False),
                ("set firewall filter FILTER interface ge-0/0/0", False)],
               "Firewall filters are applied under the interface family: 'set interfaces ... family inet filter input <name>'.",
               "7.0 Routing Policy and Firewall Filters", 16.0, 2, "apply"),
    ]

    # Deduplicate by body within this exam
    seen = set()
    unique = []
    for q in questions:
        if q["body"] not in seen:
            seen.add(q["body"])
            unique.append(q)
    return unique


def questions_to_sql(questions: list[dict]) -> str:
    lines = [
        "-- +goose Up",
        "-- +goose StatementBegin",
        "",
        "-- JNCIA-Junos (JN0-106) question bank",
        f"-- Generated {len(questions)} blueprint-aligned single-choice questions",
        "",
        "DELETE FROM questions WHERE exam_id = 'b0000000-0000-0000-0000-000000000001';",
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
        "DELETE FROM questions WHERE exam_id = 'b0000000-0000-0000-0000-000000000001';",
        "",
        "-- +goose StatementEnd",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    questions = generate_questions()
    print(questions_to_sql(questions))
