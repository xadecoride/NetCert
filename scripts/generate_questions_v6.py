#!/usr/bin/env python3
"""
NetCert Pro v6 — Truly Unique Question Generator
~10,000+ genuinely different questions via:
  - Large content pools (50-100+ entries each)
  - Multi-template generation (5-10 templates per pool)
  - Cross-pool combinatorial generators
  - Comparison & scenario generators
"""
import hashlib, json, random, re, sys, uuid

EXAM = {
    "JN0-106":   ("b0000000-0000-0000-0000-000000000001", "a0000000-0000-0000-0000-000000000001", "JNCIA-Junos"),
    "JN0-201":   ("b0000000-0000-0000-0000-000000000002", "a0000000-0000-0000-0000-000000000002", "JNCIA-SP"),
    "200-301":   ("b0000000-0000-0000-0000-000000000003", "a0000000-0000-0000-0000-000000000006", "CCNA"),
    "JN0-650":   ("b0000000-0000-0000-0000-000000000011", "a0000000-0000-0000-0000-000000000001", "JNCIP-ENT"),
    "JN0-230":   ("b0000000-0000-0000-0000-000000000020", "a0000000-0000-0000-0000-000000000003", "JNCIA-SEC"),
    "JN0-480":   ("b0000000-0000-0000-0000-000000000021", "a0000000-0000-0000-0000-000000000004", "JNCIA-DC"),
    "JN0-223":   ("b0000000-0000-0000-0000-000000000022", "a0000000-0000-0000-0000-000000000005", "JNCIA-AUT"),
    "JNCIP-SP":  ("b0000000-0000-0000-0000-000000000013", "a0000000-0000-0000-0000-000000000002", "JNCIP-SP"),
    "JNCIP-SEC": ("b0000000-0000-0000-0000-000000000024", "a0000000-0000-0000-0000-000000000003", "JNCIP-SEC"),
    "JNCIP-DC":  ("b0000000-0000-0000-0000-000000000026", "a0000000-0000-0000-0000-000000000004", "JNCIP-DC"),
    "JNCIP-AUT": ("b0000000-0000-0000-0000-000000000028", "a0000000-0000-0000-0000-000000000005", "JNCIP-AUT"),
}

def make_q(eid, tid, body, options, correct, explanation, qtype="single-choice", difficulty=2, bloom="understand", section="General", weight=14.0, urls=None):
    letters = "ABCDEFGH"; cs = set(correct.split(",")); r=[]
    for i,(t,c) in enumerate(options):
        l=letters[i]; r.append({"id":l,"text":t,"is_correct":l in cs or c})
    urls = urls or []
    return {"exam_id":eid,"track_id":tid,"question_type":qtype,"difficulty":difficulty,"bloom_level":bloom,"body":body,"options":r,"explanation":explanation,"reference_urls":urls,"blueprint_section":section,"blueprint_weight":weight}

# ════════════════════════════════════════════════
# CONTENT POOLS — massively expanded
# Each entry is a tuple with field-indexed content
# ════════════════════════════════════════════════

# PROTOCOLS: (name, layer, transport, cisco_ad, junos_pref, category, purpose)
PROTOCOLS = [
    ("OSPF",3,"IP proto 89","110","10","IGP","link-state routing within a single AS"),
    ("BGP",7,"TCP 179","20","170","EGP","path-vector inter-domain routing between autonomous systems"),
    ("IS-IS",3,"IP proto 103","115","15","IGP","link-state routing with CLNS addressing"),
    ("EIGRP",3,"IP proto 88","90","","IGP","Cisco advanced distance-vector routing with DUAL algorithm"),
    ("RIP",7,"UDP 520","120","100","IGP","distance-vector routing using hop count as metric"),
    ("RIPng",7,"UDP 521","120","100","IGP","RIP for IPv6 networks"),
    ("OSPFv3",3,"IP proto 89","110","10","IGP","OSPF for IPv6 with link-local addressing"),
    ("MP-BGP",7,"TCP 179","20","170","EGP","multi-protocol BGP supporting VPN-IPv4 and IPv6"),
    ("IGRP",3,"IP proto 9","100","","IGP","Cisco legacy distance-vector routing (deprecated)"),
    ("TCP",4,"port-based","","","Transport","connection-oriented reliable delivery with sequencing"),
    ("UDP",4,"port-based","","","Transport","connectionless best-effort datagram delivery"),
    ("IP",3,"none","","","Internet","routing and logical addressing for packet forwarding"),
    ("ICMP",3,"IP proto 1","","","Internet","error reporting and network diagnostics"),
    ("ICMPv6",3,"IPv6 proto 58","","","Internet","ICMP for IPv6 including NDP and PMTUD"),
    ("ARP",2,"Ethernet type 0x0806","","","Layer2","IP-to-MAC address resolution"),
    ("NDP",3,"ICMPv6","","","Layer2","IPv6 neighbor discovery replacing ARP"),
    ("DHCP",7,"UDP 67/68","","","Application","automatic IP configuration via DORA process"),
    ("DHCPv6",7,"UDP 546/547","","","Application","IPv6 address assignment with SLAAC integration"),
    ("DNS",7,"UDP/TCP 53","","","Application","hostname-to-IP resolution with hierarchy"),
    ("HTTP",7,"TCP 80","","","Application","hypertext transfer for web content"),
    ("HTTPS",7,"TCP 443","","","Application","encrypted web content via TLS/SSL"),
    ("FTP",7,"TCP 20/21","","","Application","file transfer with separate control and data channels"),
    ("SFTP",7,"TCP 22","","","Application","secure file transfer over SSH"),
    ("SMTP",7,"TCP 25","","","Application","email delivery between mail servers"),
    ("POP3",7,"TCP 110","","","Application","email retrieval from mail server"),
    ("IMAP",7,"TCP 143","","","Application","email retrieval with server-side storage"),
    ("SNMP",7,"UDP 161/162","","","Application","network device monitoring and management"),
    ("SSH",7,"TCP 22","","","Application","encrypted remote shell access"),
    ("Telnet",7,"TCP 23","","","Application","unencrypted remote terminal access"),
    ("NTP",7,"UDP 123","","","Application","time synchronization across network devices"),
    ("LDAP",7,"TCP 389","","","Application","directory services and authentication"),
    ("RADIUS",7,"UDP 1812/1813","","","Application","AAA protocol for network access control"),
    ("TACACS+",7,"TCP 49","","","Application","Cisco AAA protocol with separate authentication/authorization"),
    ("STP",2,"BPDUs","","","Layer2","loop prevention in redundant switched topologies"),
    ("RSTP",2,"BPDUs","","","Layer2","rapid STP convergence using edge/alternate/backup ports"),
    ("MSTP",2,"BPDUs","","","Layer2","multiple STP instances mapped to VLAN groups"),
    ("PVST+",2,"BPDUs","","","Layer2","Cisco per-VLAN spanning tree"),
    ("LLDP",2,"Ethernet type 0x88CC","","","Layer2","vendor-neutral neighbor discovery"),
    ("CDP",2,"SNAP","","","Layer2","Cisco proprietary neighbor discovery"),
    ("LACP",2,"Ethernet type 0x8809","","","Layer2","dynamic link aggregation negotiation"),
    ("PAgP",2,"Ethernet","","","Layer2","Cisco proprietary port aggregation protocol"),
    ("VRRP",3,"IP proto 112","","","FHRP","first-hop redundancy with virtual router failover"),
    ("HSRP",3,"UDP 1985","","","FHRP","Cisco first-hop redundancy with active/standby router"),
    ("GLBP",3,"UDP 3222","","","FHRP","Cisco load-balancing first-hop redundancy"),
    ("PIM",3,"IP proto 103","","","Multicast","protocol-independent multicast routing"),
    ("IGMP",3,"IP proto 2","","","Multicast","multicast group membership management"),
    ("MLD",3,"ICMPv6","","","Multicast","multicast listener discovery for IPv6"),
    ("MSDP",3,"TCP 639","","","Multicast","multicast source discovery between domains"),
    ("BFD",3,"UDP 3784","","","OAM","bidirectional forwarding detection for fast failure detection"),
    ("GMPLS",3,"IP proto 0","","","MPLS","generalized MPLS for optical and TDM networks"),
    ("LISP",3,"UDP 4341","","","Overlay","locator/ID separation for routing scalability"),
    ("VXLAN",3,"UDP 4789","","","Overlay","MAC-in-UDP encapsulation for network virtualization"),
    ("NVGRE",3,"GRE","","","Overlay","network virtualization using GRE encapsulation"),
    ("VPLS",3,"MPLS","","","VPN","Layer 2 VPN with multipoint Ethernet bridging"),
    ("L3VPN",3,"MPLS/BGP","","","VPN","Layer 3 MPLS VPN with VRF and MP-BGP"),
    ("MLD Snooping",2,"IGMPv6","","","Multicast","multicast group snooping for IPv6 networks"),
    ("IGMP Snooping",2,"IGMP","","","Multicast","multicast group membership monitoring on switches"),
    ("PIM-SM",3,"IP proto 103","","","Multicast","sparse-mode multicast with RP for receiver-driven distribution"),
    ("PIM-DM",3,"IP proto 103","","","Multicast","dense-mode multicast with flood-and-prune mechanism"),
    ("PIM-SSM",3,"IP proto 103","","","Multicast","source-specific multicast without RP requirement"),
    ("PIM-Bidir",3,"IP proto 103","","","Multicast","bidirectional shared-tree multicast with RP as root"),
    ("MSDP",3,"TCP 639","","","Multicast","inter-domain RP discovery for PIM-SM"),
    ("MBGP",7,"TCP 179","20","170","Multicast","multi-protocol BGP for multicast IPv4/IPv6 NLRI"),
    ("GRE",3,"IP proto 47","","","Tunneling","generic routing encapsulation for tunnel transport"),
    ("IP-IP",3,"IP proto 4","","","Tunneling","IP-in-IP encapsulation for tunnel forwarding"),
    ("L2TPv3",2,"IP proto 115","","","Tunneling","Layer 2 tunnel transport for Ethernet/Frame Relay"),
    ("PPPoE",2,"Ethernet","","","Access","PPP encapsulation over Ethernet for broadband access"),
    ("DHCP Option 82",7,"DHCP","","","Access","DHCP relay agent information option for subscriber ID"),
    ("PPP",2,"HDLC","","","Access","point-to-point protocol with authentication and compression"),
    ("MLPPP",2,"PPP","","","Access","multi-link PPP for bonding multiple PPP links"),
    ("Frame Relay",2,"LMI","","","WAN","packet-switched WAN technology with DLCI addressing"),
    ("ATM",2,"Cells","","","WAN","asynchronous transfer mode with fixed 53-byte cells"),
    ("HDLC",2,"Ethernet","","","WAN","Cisco HDLC serial encapsulation with keepalives"),
    ("PPPoA",2,"ATM","","","Access","PPP over ATM for DSL broadband connectivity"),
    ("sFlow",7,"UDP 6343","","","Monitoring","packet sampling for network traffic monitoring and analysis"),
    ("NetFlow",7,"UDP 2055","","","Monitoring","Cisco IP flow monitoring and export protocol"),
    ("IPFIX",7,"UDP 4739","","","Monitoring","IP flow information export; NetFlow v10 standard"),
    ("ERSPAN",2,"GRE","","","Monitoring","encapsulated remote SPAN for traffic mirroring over IP"),
    ("RSPAN",2,"VLAN","","","Monitoring","remote SPAN using VLAN tagging for remote traffic mirroring"),
    ("SPAN",2,"Switch Port","","","Monitoring","port mirroring for local traffic analysis"),
    ("MSTP",2,"BPDUs","","","Layer2","multiple spanning tree protocol with per-instance VLAN mapping"),
    ("Rep",2,"Ethernet","","","Layer2","Resilient Ethernet Protocol for ring topologies"),
    ("REP",2,"Ethernet","","","Layer2","Cisco Resilient Ethernet Protocol for fast ring convergence"),
]

# JUNOS_CMDS: (command, description, section, subcategory)
JUNOS_CMDS = [
    ("show route","displays the routing table","Routing","tables"),
    ("show route protocol bgp","displays BGP routes in the routing table","BGP","filtered"),
    ("show route protocol ospf","displays OSPF routes in the routing table","OSPF","filtered"),
    ("show route protocol isis","displays IS-IS routes in the routing table","IS-IS","filtered"),
    ("show route forwarding-table","displays the kernel forwarding table used by the PFE","Forwarding","forwarding"),
    ("show route extensive","displays detailed route information including all BGP attributes","Routing","detail"),
    ("show route summary","displays aggregate routing table statistics per protocol","Routing","summary"),
    ("show route hidden","displays routes hidden from active use due to policy or next-hop","Routing","filtered"),
    ("show route advertising-protocol bgp 10.0.0.1","shows BGP routes advertised to a specific neighbor","BGP","bgp"),
    ("show route receive-protocol bgp 10.0.0.1","shows BGP routes received from a specific neighbor","BGP","bgp"),
    ("show route protocol static","displays static routes in the routing table","Routing","filtered"),
    ("show route protocol direct","displays directly connected routes","Routing","filtered"),
    ("show route protocol access-internal","displays routes learned via access routing","Routing","filtered"),
    ("show route terse","displays compressed routing table output","Routing","terse"),
    ("show interfaces terse","displays all interfaces in compact format","Interfaces","status"),
    ("show interfaces description","displays interface descriptions and admin/link status","Interfaces","status"),
    ("show interfaces ge-0/0/0 extensive","displays detailed interface counters and errors","Interfaces","detail"),
    ("show interfaces media","displays interface media type, speed, and duplex settings","Interfaces","status"),
    ("show interfaces diagnostics optics","displays optical transceiver diagnostics (temperature, power)","Interfaces","diagnostics"),
    ("show interfaces ge-0/0/0 statistics","displays packet/byte counters for an interface","Interfaces","statistics"),
    ("show configuration","displays the active committed configuration","Configuration","display"),
    ("show configuration | display set","displays configuration in set command format","Configuration","display"),
    ("show configuration interfaces","displays interface configuration only","Configuration","filtered"),
    ("show configuration protocols ospf","displays OSPF protocol configuration only","Configuration","filtered"),
    ("commit check","validates the candidate configuration without committing","Configuration","validation"),
    ("show system commit","displays commit history for the device","Configuration","history"),
    ("rollback 0","reverts to the previously committed configuration","Configuration","rollback"),
    ("load override terminal","loads configuration from terminal input, replacing candidate","Configuration","load"),
    ("load merge terminal","loads configuration from terminal input, merging with candidate","Configuration","load"),
    ("show log messages","displays system log and event messages","Monitoring","logs"),
    ("show log interactive-commands","displays logged CLI commands executed by users","Monitoring","logs"),
    ("show system alarms","displays active system alarms (red/yellow)","Monitoring","system"),
    ("show system uptime","displays system uptime, boot time, and user sessions","Monitoring","system"),
    ("show chassis hardware","displays hardware inventory (chassis, FPC, PIC, SFP)","Monitoring","hardware"),
    ("show chassis fpc","displays FPC (line card) status and CPU utilization","Monitoring","hardware"),
    ("show chassis fpc pic-status","displays installed PICs on each FPC","Monitoring","hardware"),
    ("show chassis environment","displays environmental sensors (temp, fans, power supplies)","Monitoring","hardware"),
    ("show chassis temperature-thresholds","displays temperature alarm thresholds per component","Monitoring","hardware"),
    ("show chassis routing-engine","displays RE status including CPU and memory usage","Monitoring","hardware"),
    ("show virtual-chassis vc-port","displays virtual chassis port configuration and status","Monitoring","vc"),
    ("show virtual-chassis status","displays virtual chassis member roles and status","Monitoring","vc"),
    ("monitor interface ge-0/0/0","displays real-time interface traffic counters","Monitoring","realtime"),
    ("monitor traffic interface ge-0/0/0","captures live packets on an interface for analysis","Monitoring","realtime"),
    ("monitor bandwidth ge-0/0/0","displays real-time bandwidth utilization graph","Monitoring","realtime"),
    ("show ospf neighbor","displays OSPF neighbor adjacencies with state and interface","OSPF","neighbors"),
    ("show ospf neighbor extensive","displays detailed OSPF neighbor info including DR/BDR","OSPF","detail"),
    ("show ospf database","displays the OSPF link-state database by LSA type","OSPF","database"),
    ("show ospf database advertising-router 10.0.0.1","displays LSAs from a specific advertising router","OSPF","database"),
    ("show ospf statistics","displays OSPF SPF run statistics and timing","OSPF","statistics"),
    ("show bgp summary","displays BGP neighbor summary with state and prefixes","BGP","summary"),
    ("show bgp group","displays BGP group configuration and peering status","BGP","groups"),
    ("show bgp neighbor 10.0.0.1","displays detailed BGP neighbor information","BGP","detail"),
    ("show bgp neighbor 10.0.0.1 advertised-routes","displays routes advertised to a BGP neighbor","BGP","routes"),
    ("show bgp neighbor 10.0.0.1 received-routes","displays routes received from a BGP neighbor","BGP","routes"),
    ("show policy policy-statement EXPORT-BGP","displays routing policy evaluation","Routing Policy","policy"),
    ("show route protocol bgp table inet.0","displays BGP routes in the inet.0 routing table","BGP","tables"),
    ("show route protocol bgp table inet.3","displays BGP routes in the inet.3 (MPLS VPN) table","BGP","tables"),
    ("show isis adjacency","displays IS-IS adjacencies with state and metrics","IS-IS","adjacencies"),
    ("show isis database","displays the IS-IS link-state database","IS-IS","database"),
    ("show isis interface","displays IS-IS interface parameters and metrics","IS-IS","interfaces"),
    ("show isis statistics","displays IS-IS protocol statistics and SPF runs","IS-IS","statistics"),
    ("show ethernet-switching table","displays the MAC address forwarding table","Switching","mac"),
    ("show vlan","displays VLAN information and interface membership","Switching","vlan"),
    ("show vlan VLAN100","displays detailed information for a specific VLAN","Switching","vlan"),
    ("show arp","displays the ARP cache with IP-to-MAC mappings","Routing","arp"),
    ("show arp resolution","displays ARP resolution statistics","Routing","arp"),
    ("show ldp session","displays LDP neighbor sessions and state","MPLS","ldp"),
    ("show ldp database","displays the LDP label database","MPLS","ldp"),
    ("show route table mpls.0","displays the MPLS label switching table","MPLS","tables"),
    ("show route protocol ldp","displays LDP-learned routes","MPLS","ldp"),
    ("show route protocol bgp table inetflow.0","displays BGP flow routes","BGP","tables"),
    ("show route protocol mpls","displays MPLS-related routes","MPLS","tables"),
    ("show route protocol ldp","displays LDP-learned routes","MPLS","ldp"),
    ("show route protocol rsvp","displays RSVP-signaled routes","RSVP","tables"),
    ("show route table inetflow.0","displays the flow route table","Forwarding","tables"),
    ("show route table bgp.evpn.0","displays BGP EVPN routes","EVPN","tables"),
    ("show evpn instance","displays EVPN instance configuration and status","EVPN","instance"),
    ("show evpn database","displays the EVPN MAC/VNL database","EVPN","database"),
    ("show security policies","displays security policy configuration","Security","policies"),
    ("show security flow session","displays active security flow sessions","Security","flow"),
    ("show security alarms","displays active security alarms","Security","alarms"),
    ("show security zones","displays security zone configuration","Security","zones"),
    ("show security ipsec sa","displays IPsec security associations","Security","ipsec"),
    ("show security ike sa","displays IKE security associations","Security","ike"),
    ("show security idp attack table","displays IDP attack database","Security","idp"),
    ("show chassis cluster status","displays chassis cluster HA status","HA","cluster"),
    ("show chassis cluster interfaces","displays cluster interface configuration","HA","cluster"),
    ("show chassis cluster control-plane statistics","displays cluster control plane stats","HA","cluster"),
    ("show configuration security","displays security configuration","Configuration","security"),
    ("show configuration routing-options","displays routing-options configuration","Configuration","filtered"),
    ("show system processes extensive","displays detailed system process information","Monitoring","system"),
    ("show system storage","displays disk storage utilization","Monitoring","system"),
    ("show system users","displays active user sessions","Monitoring","system"),
    ("request system zeroize","resets system to factory defaults","Maintenance","system"),
    ("request system reboot","reboots the system","Maintenance","system"),
    ("request system software add","installs a software package","Maintenance","software"),
    ("request pppoe connect","initiates PPPoE session","Access","pppoe"),
    ("show pppoe interfaces","displays PPPoE interface status","Access","pppoe"),
    ("show dhcp server binding","displays DHCP server bindings","DHCP","server"),
    ("show dhcp relay statistics","displays DHCP relay statistics","DHCP","relay"),
]

# CISCO CMDS: (command, description, mode, section)
CISCO_CMDS = [
    ("show ip route","displays the IPv4 routing table","exec","Routing"),
    ("show ip ospf neighbor","displays OSPF neighbor adjacencies","exec","OSPF"),
    ("show ip ospf database","displays the OSPF link-state database","exec","OSPF"),
    ("show ip bgp summary","displays BGP neighbor summary","exec","BGP"),
    ("show ip bgp 10.0.0.0","displays BGP route information for a specific prefix","exec","BGP"),
    ("show interfaces","displays all interface status/counters","exec","Interfaces"),
    ("show ip interface brief","displays summary of IP interface status","exec","Interfaces"),
    ("show running-config","displays active running configuration","exec","Configuration"),
    ("show startup-config","displays saved startup configuration in NVRAM","exec","Configuration"),
    ("show vlan brief","displays VLAN summary and port assignments","exec","VLAN"),
    ("show spanning-tree","displays spanning-tree topology and port roles","exec","STP"),
    ("show spanning-tree vlan 10","displays STP information for a specific VLAN","exec","STP"),
    ("show mac address-table","displays CAM table with MAC-to-port mappings","exec","Switching"),
    ("show mac address-table dynamic","displays dynamically learned MAC entries","exec","Switching"),
    ("show cdp neighbors","displays CDP neighbor summary","exec","CDP"),
    ("show lldp neighbors","displays LLDP neighbor summary","exec","LLDP"),
    ("show ip arp","displays the ARP cache","exec","Routing"),
    ("show ip dhcp binding","displays DHCP lease bindings","exec","DHCP"),
    ("show ip nat translations","displays active NAT translations","exec","NAT"),
    ("show ip access-lists","displays configured access-lists and hit counts","exec","Security"),
    ("show ip protocols","displays routing protocol status and timers","exec","Routing"),
    ("show ip eigrp neighbors","displays EIGRP neighbor table","exec","EIGRP"),
    ("show ip eigrp topology","displays EIGRP topology table","exec","EIGRP"),
    ("show ipv6 route","displays IPv6 routing table","exec","IPv6"),
    ("show ipv6 ospf neighbor","displays OSPFv3 neighbors","exec","OSPFv3"),
    ("show vlan internal usage","displays internal VLAN usage","exec","VLAN"),
    ("show etherchannel summary","displays EtherChannel (LACP) status","exec","EtherChannel"),
    ("show port-security","displays port security configuration and violations","exec","Security"),
    ("show ip ssh","displays SSH server status and version","exec","Management"),
    ("show logging","displays syslog messages","exec","Management"),
    ("show clock","displays system clock and timezone","exec","Management"),
    ("show version","displays IOS version, uptime, and hardware info","exec","Management"),
    ("show flash:","displays flash file system contents","exec","Management"),
    ("show ip route ospf","displays OSPF-learned routes only","exec","OSPF"),
    ("show ip route bgp","displays BGP-learned routes only","exec","BGP"),
    ("show ip mroute","displays multicast routing table","exec","Multicast"),
    ("show ip pim neighbor","displays PIM neighbors","exec","Multicast"),
    ("show ip igmp groups","displays IGMP group subscriptions","exec","Multicast"),
    ("debug ip ospf adj","displays real-time OSPF adjacency events","exec","Debug"),
    ("debug ip bgp updates","displays real-time BGP update messages","exec","Debug"),
    ("show ip bgp neighbors 10.0.0.1 advertised-routes","shows routes advertised to BGP neighbor","exec","BGP"),
    ("show ip bgp neighbors 10.0.0.1 received-routes","shows routes received from BGP neighbor","exec","BGP"),
    ("show ip route vrf CUSTOMER-A","displays routing table for a VRF","exec","MPLS VPN"),
    ("show mpls ldp neighbor","displays LDP neighbors","exec","MPLS"),
    ("show mpls forwarding-table","displays MPLS label forwarding table","exec","MPLS"),
    ("show policy-map interface gigabitethernet0/1","displays QoS policy statistics on interface","exec","QoS"),
    ("show class-map","displays configured class maps for QoS","exec","QoS"),
    ("show crypto isakmp sa","displays IKE security associations","exec","Security"),
    ("show crypto ipsec sa","displays IPsec security associations","exec","Security"),
    ("show ip nat statistics","displays NAT translation statistics","exec","NAT"),
    ("show ip access-lists","displays access-list configuration and hit counts","exec","Security"),
    ("show port-security interface gigabitethernet0/1","displays port security settings","exec","Security"),
    ("show authentication sessions","displays 802.1X/MAB authentication sessions","exec","Security"),
    ("show ip device tracking","displays IP device tracking entries for IP source guard","exec","Security"),
    ("show etherchannel load-balance","displays load-balancing method for EtherChannel","exec","EtherChannel"),
    ("show ip ospf virtual-links","displays OSPF virtual link status","exec","OSPF"),
    ("show ip bgp community 65000:100","displays BGP routes matching a community","exec","BGP"),
    ("show ip bgp regexp ^65000_","displays BGP routes matching AS-path regex","exec","BGP"),
    ("show ipv6 routers","displays IPv6 router advertisements received","exec","IPv6"),
    ("show ipv6 dhcp binding","displays DHCPv6 bindings","exec","IPv6"),
    ("show ipv6 mld groups","displays MLD multicast group memberships","exec","Multicast"),
    ("show license usage","displays software license usage","exec","Management"),
    ("show module","displays modular chassis module status","exec","Management"),
    ("show environment all","displays environmental status (power, fans, temp)","exec","Management"),
    ("show inventory","displays hardware inventory with serial numbers","exec","Management"),
]

# NETWORK_TERMS: (term, definition, category)
NETWORK_TERMS = [
    ("Routing","forwarding packets between networks based on destination IP","Core Concept"),
    ("Switching","forwarding frames within a network based on destination MAC","Core Concept"),
    ("NAT","translating private IPs to public IPs for Internet connectivity","Core Concept"),
    ("ARP","resolving IPv4 addresses to MAC addresses on broadcast segments","Core Concept"),
    ("DNS","resolving human-readable hostnames to numeric IP addresses","Core Concept"),
    ("DHCP","automatically assigning IP configuration to hosts","Core Concept"),
    ("STP","preventing Layer 2 loops in redundant switched topologies","Layer 2"),
    ("RSTP","rapid STP with fast convergence using port roles and proposal-agreement","Layer 2"),
    ("VLAN","segmenting a physical network into multiple logical broadcast domains","Layer 2"),
    ("Trunking","carrying multiple VLAN frames over a single link with 802.1Q tagging","Layer 2"),
    ("Access Port","switch port carrying traffic for a single VLAN","Layer 2"),
    ("DTP","Dynamic Trunking Protocol for automatic trunk negotiation","Layer 2"),
    ("VTP","VLAN Trunking Protocol for VLAN database synchronization","Layer 2"),
    ("EtherChannel","link aggregation bundling multiple physical links into one logical link","Layer 2"),
    ("Port Security","restricting MAC addresses allowed on a switch port","Security"),
    ("DHCP Snooping","man-in-the-middle attack prevention by filtering DHCP messages","Security"),
    ("Dynamic ARP Inspection","ARP spoofing prevention by validating ARP packets","Security"),
    ("Storm Control","broadcast/multicast/unknown-unicast storm prevention","Security"),
    ("QoS","prioritizing certain traffic classes over others","Core Concept"),
    ("CoS","Layer 2 class of service using 802.1p priority bits","QoS"),
    ("DSCP","Differentiated Services Code Point for Layer 3 QoS marking","QoS"),
    ("LLQ","Low Latency Queueing for real-time traffic guaranteed bandwidth","QoS"),
    ("WFQ","Weighted Fair Queueing providing fair bandwidth allocation","QoS"),
    ("CBWFQ","Class-Based Weighted Fair Queueing for per-class bandwidth guarantees","QoS"),
    ("VPN","securely extending a private network across a public infrastructure","Security"),
    ("IPsec VPN","encrypted tunnel providing confidentiality and integrity","Security"),
    ("SSL VPN","VPN using TLS for web-based remote access","Security"),
    ("DMVPN","dynamic multi-point VPN for hub-and-spoke topologies","Security"),
    ("GETVPN","Group Encrypted Transport VPN with any-to-any connectivity","Security"),
    ("ACL","access control list filtering traffic by IP, port, and protocol","Security"),
    ("Zone-Based Firewall","Cisco zone-pair firewall policy architecture","Security"),
    ("IPS","intrusion prevention system inspecting traffic for threats","Security"),
    ("AAA","authentication, authorization, and accounting framework","Security"),
    ("BGP","exchanging routing information between autonomous systems","Routing"),
    ("OSPF","link-state IGP using SPF algorithm for loop-free routing","Routing"),
    ("EIGRP","Cisco hybrid routing protocol using DUAL algorithm","Routing"),
    ("IS-IS","link-state IGP used in service provider networks","Routing"),
    ("Route Redistribution","importing routes from one routing protocol into another","Routing"),
    ("Route Summarization","aggregating multiple prefixes into a shorter prefix","Routing"),
    ("Floating Static Route","static route with higher AD for backup path","Routing"),
    ("Policy-Based Routing","forwarding based on policies other than destination IP","Routing"),
    ("MPLS","label switching forwarding paradigm for traffic engineering","MPLS"),
    ("LDP","label distribution protocol distributing labels for IGP routes","MPLS"),
    ("RSVP-TE","RSVP with traffic engineering for constraint-based MPLS LSP setup","MPLS"),
    ("VXLAN","MAC-in-UDP overlay for Layer 2 extension over Layer 3","Data Center"),
    ("EVPN","control plane for VXLAN using MP-BGP for MAC/VNI distribution","Data Center"),
    ("VTEP","VXLAN tunnel endpoint performing encapsulation and decapsulation","Data Center"),
    ("VNI","VXLAN network identifier for segment isolation","Data Center"),
    ("SDN","software-defined networking decoupling control and data planes","Automation"),
    ("NFV","virtualizing network functions on commodity hardware","Automation"),
    ("NetConf","XML-based network configuration protocol over SSH","Automation"),
    ("RestConf","RESTful API for network configuration using YANG models","Automation"),
    ("YANG","data modeling language for network configuration and state","Automation"),
    ("Ansible","agentless automation tool using YAML playbooks","Automation"),
    ("Puppet","declarative configuration management with pull model","Automation"),
    ("Chef","configuration management using Ruby DSL cookbooks","Automation"),
    ("SaltStack","event-driven automation with remote execution","Automation"),
    ("SSH","encrypted remote access protocol for CLI management","Management"),
    ("SNMP","protocol for monitoring and managing network devices","Management"),
    ("Syslog","centralized logging for network device events","Management"),
    ("NetFlow","Cisco IP traffic flow monitoring and export","Management"),
    ("IP SLA","measure network performance metrics (latency, jitter, loss)","Management"),
    ("SNMPv3","SNMP with encryption and authentication security","Management"),
    ("NTP","time synchronization across network infrastructure","Management"),

    ("AAA","authentication, authorization, and accounting framework","Security"),
    ("TACACS+","Cisco AAA protocol; separate auth/authorization with TCP","Security"),
    ("RADIUS","UDP-based AAA protocol for network access control","Security"),
    ("802.1X","port-based network access control with EAP authentication","Security"),
    ("MAB","MAC Authentication Bypass for 802.1X incapable devices","Security"),
    ("WebAuth","web-based captive portal authentication for guest access","Security"),
    ("CIS","Cisco ISE; identity services engine for policy enforcement","Security"),
    ("TrustSec","Cisco security group tagging for role-based access control","Security"),
    ("SGT","Security Group Tag for Cisco TrustSec policy enforcement","Security"),
    ("IPSLA","Cisco IP SLA for performance measurement (latency, jitter, loss)","Management"),
    ("NetFlow","Cisco flow monitoring exporting IP traffic metadata","Management"),
    ("IPFIX","NetFlow v10 standardized flow export protocol","Management"),
    ("CWMP/TR-069","CPE WAN management protocol for auto-configuration","Management"),
    ("ZTP","Zero-Touch Provisioning for automated device deployment","Management"),
    ("PoE","Power over Ethernet delivering power over data cables","Layer 2"),
    ("PoE+","IEEE 802.3at PoE with 30W per port","Layer 2"),
    ("UDLD","UniDirectional Link Detection for fiber link monitoring","Layer 2"),
    ("LACP","Link Aggregation Control Protocol for dynamic port bundling","Layer 2"),
    ("PAgP","Cisco port aggregation protocol for EtherChannel","Layer 2"),
    ("VPC","virtual Port Channel for cross-chassis multi-homing on NX-OS","Data Center"),
    ("VSS","Cisco Virtual Switching System combining two 6500 chassis","Data Center"),
    ("FEX","Cisco Fabric Extender for remote line card connectivity","Data Center"),
    ("OTV","Overlay Transport Virtualization for Layer 2 DCI","Data Center"),
    ("LISP","Locator/ID Separation Protocol for routing scalability","Overlay"),
    ("OAM","Operations, Administration, and Management for network OAM","Management"),
    ("CFM","Connectivity Fault Management IEEE 802.1ag for Ethernet OAM","Management"),
    ("Y.1731","ITU-T Ethernet OAM performance monitoring","Management"),
    ("TWAMP","Two-Way Active Measurement Protocol for network performance","Management"),
    ("BFD","Bidirectional Forwarding Detection for sub-second failure detection","Routing"),
    ("GMPLS","Generalized MPLS for optical and TDM network control","MPLS"),
("FHRP","first-hop redundancy for default gateway high availability","HA"),
    ("VRRP","standards-based virtual router redundancy","HA"),
    ("HSRP","Cisco active/standby gateway redundancy","HA"),
    ("GLBP","Cisco load-balancing gateway redundancy","HA"),
    ("STP Guard","BPDU guard, root guard, and loop guard protections","Layer 2"),
    ("UDLD","UniDirectional Link Detection for fiber link monitoring","Layer 2"),
    ("FlexLinks","Cisco failover mechanism for dual-homed access","Layer 2"),
    ("VSS","Virtual Switching System combining two chassis","Data Center"),
    ("vPC","virtual Port Channel for cross-chassis multi-homing","Data Center"),
    ("FCoE","Fibre Channel over Ethernet for storage networking","Data Center"),
    ("TRILL","transparent interconnection of lots of links for Layer 2 multipathing","Data Center"),
    ("SPB","Shortest Path Bridging IEEE 802.1aq for Layer 2 IS-IS control","Data Center"),
]

# TROUBLESHOOTING: (symptom, cause, tool, device)
TSHOOT = [
    ("OSPF neighbors stuck in INIT state","MTU mismatch or network type mismatch","show ospf neighbor, monitor interface, check MTU","Junos/Cisco router"),
    ("BGP session flapping","TCP RST from connectivity issues or hold timer mismatch","show bgp summary, ping, show log messages","Junos/Cisco router"),
    ("BGP not advertising routes","missing network statement or export policy filtering routes","show route advertising-protocol bgp, show policy","Junos/Cisco router"),
    ("No route to destination in routing table","missing static route or routing policy rejecting the route","show route, show route protocol, traceroute","Any router"),
    ("Ping fails to remote subnet","missing default gateway or ACL blocking ICMP","show route, show ip access-lists, ping extended","Cisco router"),
    ("Ping fails across MPLS cloud","missing LSP or label binding","show route table mpls.0, show ldp session, ping mpls","Junos router"),
    ("Firewall filter blocking traffic","term order incorrect or missing accept term","show firewall log, show log messages, monitor traffic","Junos SRX"),
    ("Security policy blocking traffic","missing policy or wrong zone-pair configuration","show security policies, show security flow session","SRX/Cisco ASA"),
    ("Port security violation on switch","excessive MAC addresses or sticky MAC misconfiguration","show port-security, show interfaces status err-disabled","Cisco switch"),
    ("VLAN traffic not reaching across trunk","native VLAN mismatch or trunk pruning","show interfaces trunk, show vlan","Cisco switch"),
    ("DHCP clients not receiving addresses","no ip helper-address or DHCP server unreachable","show ip dhcp binding, debug ip dhcp server events","Cisco router/switch"),
    ("STP loop causing network outage","BPDU filter enabled incorrectly or non-root bridge elected","show spanning-tree, show interfaces counters","Cisco switch"),
    ("NAT not translating addresses","missing ip nat inside/outside interface or overload keyword","show ip nat translations, debug ip nat","Cisco router"),
    ("High CPU utilization on router","routing protocol process CPU spikes or BGP flapping","show processes cpu, show log, show ip bgp summary","Cisco router"),
    ("High RE CPU on Juniper","routing protocol churn or excessive SNMP polling","show system processes, show log messages, show task io","Junos router"),
    ("Interface flapping up and down","faulty SFP, cable issue, or speed/duplex mismatch","show interfaces, show interfaces diagnostics optics","Any device"),
    ("Ping works but TCP connections fail","ACL blocking return traffic or TCP MSS issue","show ip access-lists, extended ping with TCP","Cisco router"),
    ("VXLAN traffic not reaching remote VTEP","missing VNI configuration or BGP EVPN session down","show evpn, show ethernet-switching table, show bgp evpn","Junos QFX"),
    ("IPv6 router not advertising prefix","RA suppression or no ipv6 enable on interface","show ipv6 interface, debug ipv6 nd","Cisco router"),
    ("VRRP/HSRP failover not working","priority misconfiguration or preempt disabled","show vrrp, show standby brief","Cisco router"),
    ("LACP bundle not coming up","partner configuration mismatch or incompatible speed","show etherchannel summary, show lacp neighbor","Cisco switch"),
    ("DHCP server running out of addresses","lease time too long or subnet too small","show ip dhcp pool, show ip dhcp conflict","Cisco router"),
    ("BGP prefix limit exceeded","peering receiving too many prefixes","show bgp summary, show log, check max-prefix","Cisco/Junos router"),
    ("Route not in forwarding table","kernel route table synchronization issue","show route forwarding-table, show route extensive","Junos router"),
    ("IPv4 and IPv6 OSPF not adjacent","OSPFv2 and OSPFv3 configuration mismatch","show ospf neighbor, show ospf3 neighbor","Cisco router"),
    ("IPsec tunnel not establishing","IKE policy mismatch or pre-shared key error","show crypto isakmp sa, show crypto ipsec sa","Cisco router/ASA"),
    ("QoS queue drops affecting voice","LLQ bandwidth allocation insufficient","show policy-map interface, show interface","Cisco router"),
    ("Ping between VLANs fails","SVI interface disabled or VLAN ACL blocking","show ip interface brief, show vlan","Cisco switch"),
    ("Device not reachable via SNMP","community string mismatch or ACL blocking SNMP","show snmp, show ip access-lists","Any device"),
    ("EIGRP stuck in active","query not acknowledged from a neighbor","show ip eigrp topology, show log, debug eigrp packets","Cisco router"),
    ("BGP path selection not optimal","local preference or MED configuration","show bgp 10.0.0.0, show route protocol bgp","Cisco/Junos router"),
    ("MPLS LSP not signaling","RSVP-TE path computation or CSPF failure","show mpls lsp, show rsvp session, log messages","Junos router"),
    ("LLDP neighbor not showing","LLDP disabled globally or per interface","show lldp, show lldp interface ge-0/0/0","Junos/Cisco device"),
    ("Multicast receiver not receiving traffic","PIM RP unreachable or IGMP snooping filter","show pim rp, show igmp snooping, show mroute","Cisco router"),
    ("Ping succeeds but traceroute fails","ICMP time-exceeded blocked by ACL","show ip access-lists, debug ip icmp","Cisco router"),
    ("OSPF database not synchronizing","area ID mismatch or passive interface configuration","show ospf database, show ospf interface, compare area configs","Cisco/Junos router"),
    ("BGP next-hop unreachable","no route to BGP next-hop in IGP or next-hop-self missing","show bgp neighbor, show ip route, ping next-hop","Cisco router"),
    ("PIM neighbors not forming","PIM mode mismatch or RP unreachable","show ip pim neighbor, show ip pim rp mapping","Cisco router"),
    ("MLD not discovering IPv6 receivers","MLD version mismatch or snooping filter","show ipv6 mld groups, show mld snooping","Cisco/Junos switch"),
    ("IPsec Phase 2 not completing","proxy-ID mismatch or transform set incompatibility","show crypto ipsec sa, debug crypto ipsec","Cisco router/ASA"),
    ("EIGRP route not in topology table","k-value mismatch or distribute-list filtering","show ip eigrp topology, show ip protocols","Cisco router"),
    ("VXLAN tunnel endpoint not reachable","missing underlay route or VNI configuration error","show lldp, show interfaces vxlan, traceroute","Junos QFX/Cisco NX-OS"),
    ("EVPN Type 2 route not advertised","MAC not learned or EVI/VNI binding missing","show evpn database, show ethernet-switching table","Junos QFX"),
    ("Chassis cluster failover not happening","control link failure or threshold timeout too high","show chassis cluster status, show log messages","SRX chassis cluster"),
    ("LLDP neighbor not showing on Juniper","LLDP disabled at interface level or protocol-level","show lldp, show lldp interface, set lldp interface","Junos device"),
    ("CDP neighbor inconsistent","CDP version mismatch or timer mismatch","show cdp neighbors detail, show cdp interface","Cisco device"),
    ("VRRP election not working","priority same or preempt disabled on both routers","show vrrp, show standby","Cisco router"),
    ("DHCP starvation attack occurring","malicious client exhausting pool with fake MACs","show ip dhcp binding, show ip dhcp conflict, IP source guard","Cisco switch"),
    ("ARP cache poisoning detected","attacker sending fake ARP replies","show ip arp, show arp, DAI configuration check","Cisco switch"),
    ("QoS marking not applied correctly","class-map not matching or policy-map not applied to interface","show policy-map interface, show class-map","Cisco router"),
    ("MPLS LDP session flapping","hello interval mismatch or transport address unreachable","show ldp session, show route, ping transport-address","Junos/Cisco router"),
    ("802.1X authentication failing","RADIUS server unreachable or EAP type mismatch","show authentication sessions, debug radius authentication","Cisco switch"),
    ("HSRP state flapping between active/standby","Hello timer mismatch or preempt delay misconfiguration","show standby brief, debug standby","Cisco router"),
    ("NAT pool exhausted","too many concurrent translations exceeding pool size","show ip nat statistics, show ip nat translations verbose","Cisco router"),
    ("IPv6 SLAAC not providing addresses","RA suppress enabled or M/O flags incorrectly set","show ipv6 interface, debug ipv6 nd","Cisco router"),
]

# NETWORK_SCENES: (scenario, condition, expected_result)
NETWORK_SCENES = [
    ("Two routers connected via serial link with OSPF enabled","MTU mismatch between the two sides","OSPF neighbors will be stuck in INIT state"),
    ("A BGP session between two ISPs with different hold timers","Hold timer mismatch of 30 and 90 seconds","The session establishes with the lower hold timer value"),
    ("A switch port configured with port-security and maximum MAC count 2","A third device attempts to connect","The port enters err-disable state and blocks traffic"),
    ("A trunk link between two switches with mismatched native VLANs","Native VLAN 10 on one side and 20 on the other","VLAN traffic may leak between VLANs unexpectedly"),
    ("An EtherChannel configured with LACP active on one side and passive on the other","LACP passive side waits for negotiation","The bundle forms successfully (active/passive is compatible)"),
    ("A router receiving the same route from OSPF (AD 110) and BGP (AD 20)","The route is to 10.0.0.0/24 with same metric","BGP route is preferred due to lower administrative distance"),
    ("An SRX security policy configured without application services","Traffic matching an ALG-dependent protocol (FTP)","The FTP data channel fails since no ALG is configured"),
    ("Two routers establishing BGP with different local preference defaults","Default local pref is 100 on both sides","Best path selection uses AS path length as tiebreaker"),
    ("A Juniper router with GRES enabled and a route is being processed during RE switchover","RE switchover occurs during BGP convergence","The forwarding table is preserved; BGP needs graceful restart to complete"),
    ("A Cisco switch configured with VTP transparent mode","A new VLAN is created and needs to propagate","VLAN changes must be configured manually on each switch"),
    ("A Juniper virtual chassis with two members split by a link failure","Split occurs between member 0 and member 1","Both members become active and split-brain occurs without VCP redundancy"),
    ("An EVPN with symmetric IRB configured for inter-subnet routing","Traffic between two VLANs on different VTEPs","Both ingress and egress VTEPs perform routing with VNI translation"),
    ("An MPLS LSP with RSVP-TE signaling and a link failure","The primary path link goes down","RSVP-TE signals a new path using CSPF or uses a standby secondary path"),
    ("PIM-SM with BSR mechanism for RP discovery","A new multicast source becomes active","The source registers with the RP; receivers join via (*,G) tree toward the RP"),
    ("Cisco DHCP Snooping enabled on an access switch","An untrusted port receives a DHCP OFFER message","The message is dropped by DHCP snooping as untrusted ports cannot send OFFERs"),
    ("A router with IP SLA tracking configured for static route failover","Tracked destination becomes unreachable","The floating static route is installed in the routing table"),
    ("An SRX chassis cluster with control link failure","The control link (fab0) goes down but fabric link (fab1) remains up","The cluster splits unless the control link recovers within the timeout"),
    ("A QFX switch with MAC learning disabled on a VXLAN VTEP","Unknown destination MAC arrives at the VTEP","The switch floods the packet as unknown unicast within the VNI"),
    ("A router with BGP multipath and two equal-cost eBGP paths","Two paths to the same prefix from different AS","Both paths are installed in routing table with ECMP if load-balancing is enabled"),
    ("OSPF virtual link between two non-backbone areas through Area 0","The virtual link connects Area 1 and Area 2 through Area 0","Virtual link works but both areas must connect through the same ABR for stability"),
    ("IPv6 router configured with SLAAC and no DHCPv6","A new Windows host connects to the network","The host receives an IPv6 address using the advertised prefix with EUI-64"),
    ("Cisco port-channel configured with all active member links","One member link goes down","Traffic is rebalanced across remaining member links with minimal packet loss"),
    ("Junos firewall filter with multiple terms and no final default term","Traffic not matching any term in the filter","The traffic is implicitly denied by the default deny-all term"),
    ("MPLS VPN configured with overlapping customer IP addresses","Two customers use 10.0.0.0/8 for their internal networks","Routes are kept separate using VRFs and route distinguishers"),
    ("Two ISIS routers with different NET addresses in the same area","NET: 49.0001.0100.0000.0001.00 and 49.0001.0100.0000.0002.00","Both routers establish a Level 1 adjacency in area 49.0001"),
    ("Spanning tree with root guard configured on an access port","A superior BPDU arrives on the root guard port","The port is moved to root-inconsistent state blocking traffic"),
    ("BGP community being used to tag customer routes","Provider sets community 64510:100 on customer routes","Peers can match this community for traffic engineering and policy"),
    ("VXLAN with BGP EVPN and Type 2 routes for host reachability","Host MAC and IP are learned on a VTEP","Type 2 route with MAC/IP is advertised to remote VTEPs via BGP"),

    ("A campus switch stack with four members configured for cross-stack EtherChannel","One member switch fails unexpectedly","The EtherChannel link remains active using remaining member ports; traffic redistributes across surviving links"),
    ("An SRX cluster in active/active mode with asymmetric routing","Reverse traffic arrives on different node than forward traffic","The SRX performs flow re-assembly and session synchronization via fabric link"),
    ("A router configured with BGP add-path and three paths to the same prefix","The router needs to advertise multiple paths to its iBGP peer","Add-path capability allows advertising multiple best paths with unique path IDs"),
    ("A Cisco switch with DHCP snooping and DAI enabled","An attacker sends a DHCP REQUEST with a fake chaddr MAC","DHCP snooping drops the packet because the chaddr doesn't match the ingress port's MAC"),
    ("A Juniper MX router performing inline NAT with session-based logging","NAT session limit is reached during peak traffic","New translation requests are dropped until existing sessions expire or are cleared"),
    ("An MPLS network with LDP and RSVP-TE both operating","The same FEC has both LDP label and RSVP-TE label assigned","Traffic follows the RSVP-TE LSP when LDP-over-RSVP is configured; otherwise LDP forwarding is used"),
    ("A data center with VXLAN EVPN and symmetric IRB","A VM moves from one rack to another rack behind a different leaf","EVPN Type 2 route with sequence number is updated; MAC mobility sequence increments and traffic follows"),
    ("A network with IS-IS overload bit set on a router","The overloaded router still participates in IS-IS adjacencies","The router is bypassed for transit traffic but remains reachable for locally connected prefixes"),
    ("A Cisco router with BGP deterministic-med and med missing on some paths","Paths with missing MED are compared as having MED 0","With deterministic-med, MED comparison is done per-neighbor AS; missing MED treated as 0"),
    ("An OSPF NSSA area with multiple ASBRs redistributing external routes","Two ASBR advertise Type 7 LSAs for the same prefix with different metrics","The best route is selected based on lowest metric; Type 7 LSAs are translated to Type 5 by the NSSA ABR"),
    ("A network with LACP fast rate and member link failure","One link in a port-channel fails briefly then recovers","LACP detects failure within 1 second (fast rate); the link is removed from bundle; upon recovery it rejoins after握手"),
    ("A Juniper virtual chassis with VCP ports on different member links","Split between members 0-2 and 3-5 with VCP redundancy configured","Split detection via multi-member VCP; lower priority split goes into line-card mode or uses split-detection mechanism"),
    ("Two routers running BFD over a multiplexed Ethernet link","Link congestion causes BFD packet loss for more than 3 intervals","BFD declares the session down; routing protocols react by tearing adjacencies; traffic re-routes via alternate path"),
    ("A Cisco router with IP SLA tracking an ICMP echo to a remote target","The tracked target becomes unreachable for three consecutive probe intervals","SLA enters down state; associated object tracking triggers route removal or policy change"),
    ("A network with Policy-Based Routing matching HTTP traffic","HTTPS traffic needs to use the same path as HTTP but is not matched by the route-map","Policy-based routing must explicitly match protocol TCP port 443; otherwise HTTPS uses default routing table"),
    ("A Juniper MX with firewall filter on loopback interface","Filter term accepts SSH but rejects telnet; no final term present","SSH is accepted; telnet is rejected by the implicit default discard; all other traffic to loopback is also rejected"),
    ("Two EIGRP routers with different K-values (K1=1 vs K1=1 K3=1)","Adjacency attempt between the two routers","EIGRP adjacency fails with K-value mismatch error message in logs"),
    ("A Cisco switch with Voice VLAN configured on an access port","A Cisco IP phone is connected with a PC behind the phone","Phone uses voice VLAN with CoS trust; PC uses data VLAN; both are forwarded with proper QoS marking"),
    ("A network with BGP ORF (Outbound Route Filtering) configured","The BGP peer sends a prefix that should be filtered by ORF","ORF is negotiated; received prefix is processed against the installed outbound filter; matching prefix is not advertised"),
    ("A Juniper router with multiple routing instances (VRFs)","Route leaking between VRF-A and VRF-B is required","Use rib-groups or instance-import/export policies to selectively share routes between VRFs"),
("A network with PIM-DM and a single multicast receiver","The multicast source starts sending","The first packet floods everywhere; non-RPF interfaces and no-receiver branches prune"),
    ("IPv6 OSPFv3 running with link-local addresses only","OSPFv3 adjacency using link-local addresses","Adjacency forms using link-local FE80 addresses; global addrs in LSAs only"),
]

# BGP attributes: (name, purpose, well_known, mandatory, type_code)
BGP_ATTRS = [
    ("AS_PATH","loop prevention and path selection","yes","yes",2),
    ("NEXT_HOP","reachability info for destination (IP of next-hop router)","yes","yes",3),
    ("ORIGIN","route origin code (IGP/EGP/incomplete)","yes","yes",1),
    ("LOCAL_PREFERENCE","preference for AS exit point selection","yes","no",5),
    ("ATOMIC_AGGREGATE","indicates information lost during aggregation","yes","no",6),
    ("AGGREGATOR","router that performed route aggregation","yes","no",7),
    ("COMMUNITY","tag-based groups for policy application","no","no",8),
    ("MED","suggest entry point into AS to external neighbors","no","no",4),
    ("CLUSTER_LIST","route reflection loop detection","no","no",10),
    ("ORIGINATOR_ID","route originator in route reflection","no","no",9),
    ("EXTENDED COMMUNITY","extended 8-byte communities (RT, SoO)","no","no",16),
    ("LARGE COMMUNITY","4-byte AS community format RFC 8092","no","no",32),
    ("AS4_PATH","AS path for 4-byte AS numbers backward compat","no","no",17),
    ("PMSI_TUNNEL","provider multicast service interface tunnel attribute","no","no",22),
    ("ATOMIC_AGGREGATE","indicates aggregated route may lose path info","yes","no",6),
]

# MPLS concepts: (concept, description, category)
MPLS = [
    ("MPLS Label","4-byte shim header: 20-bit label, 3-bit EXP, 1-bit BoS, 8-bit TTL","Fundamental"),
    ("Label Push","adding an MPLS label to a packet at the ingress LER","Operation"),
    ("Label Swap","replacing the outer MPLS label at transit P routers","Operation"),
    ("Label Pop","removing the outermost MPLS label (PHP)","Operation"),
    ("Label Imposition","pushing a stack of multiple labels at ingress","Operation"),
    ("PHP","Penultimate Hop Popping; penultimate router pops label before egress","Operation"),
    ("LSR","Label Switch Router; core router performing label swapping","Node"),
    ("LER","Label Edge Router; ingress/egress router pushing/popping labels","Node"),
    ("P Router","Provider core router label-switching without VPN awareness","Node"),
    ("PE Router","Provider Edge router with VRF and VPN awareness","Node"),
    ("FEC","Forwarding Equivalence Class; group of packets forwarded identically","Fundamental"),
    ("LSP","Label Switched Path; unidirectional MPLS tunnel path","Fundamental"),
    ("LDP","Label Distribution Protocol; distributes labels for IGP routes hop-by-hop","Signaling"),
    ("RSVP-TE","RSVP with Traffic Engineering; signals MPLS LSPs with bandwidth reservation","Signaling"),
    ("CSPF","Constraint-based Shortest Path First; RSVP-TE path computation with constraints","Signaling"),
    ("FRR","Fast Reroute; pre-computed backup MPLS paths for sub-50ms failover","Protection"),
    ("Link Protection","FRR protecting a specific link failure","Protection"),
    ("Node Protection","FRR protecting a node failure bypassing the failed router","Protection"),
    ("Bypass LSP","FRR backup LSP protecting a set of LSPs through a point of failure","Protection"),
    ("MBB","Make-Before-Break; signaling new LSP before removing old one to avoid traffic loss","Operation"),
    ("IGP Shortcut","using MPLS LSP as a direct next-hop in IGP routing","Operation"),
    ("LDP-over-RSVP","LDP sessions signaled over an RSVP-TE LSP tunnel","Signaling"),
    ("MPLS-TE","Traffic Engineering using RSVP for explicit path control and bandwidth","Traffic Engineering"),
    ("Auto-bandwidth","RSVP-TE automatically adjusting LSP bandwidth based on traffic measurement","Traffic Engineering"),
    ("DiffServ-aware TE","MPLS-TE with per-class bandwidth pools (CT0-CT7)","Traffic Engineering"),
]

# EVPN-VXLAN: (concept, description, category)
EVPN = [
    ("Type 2 Route","MAC/IP advertisement route for host reachability","Route Type"),
    ("Type 3 Route","Inclusive Multicast Ethernet Tag for BUM traffic","Route Type"),
    ("Type 4 Route","Ethernet Segment route for DF election","Route Type"),
    ("Type 5 Route","IP Prefix route for inter-subnet forwarding","Route Type"),
    ("Type 1 Route","Ethernet Auto-Discovery route for aliasing and backup","Route Type"),
    ("VTEP","VXLAN Tunnel Endpoint encapsulating/decapsulating VXLAN traffic","Node"),
    ("VNI","VXLAN Network Identifier; 24-bit segment identifier","Fundamental"),
    ("Symmetric IRB","both ingress and egress VTEPs perform routing with VNI translation","IRB Mode"),
    ("Asymmetric IRB","ingress VTEP routes; egress VTEP bridges to destination","IRB Mode"),
    ("Anycast VTEP","multiple VTEPs sharing the same IP for load balancing","Redundancy"),
    ("ESI","Ethernet Segment Identifier identifying a multi-homed segment","Fundamental"),
    ("EVI","Ethernet VPN Instance; logical EVPN entity per VNI","Fundamental"),
    ("DF Election","Designated Forwarder election per VLAN for multi-homed segments","Procedure"),
    ("MAC Mobility","MAC address movement detection and sequence number tracking","Procedure"),
    ("Split Horizon","preventing loops by filtering traffic from the same ES","Loop Prevention"),
]

# SECURITY: (concept, description, category)
SECURITY = [
    ("Security Zone","logical interface group with common security policies","Fundamental"),
    ("Inter-zone Traffic","traffic between different zones; denied by default","Policy"),
    ("Intra-zone Traffic","traffic within the same zone; permitted by default","Policy"),
    ("Security Policy","rules defining permitted/denied traffic between zones","Policy"),
    ("ALG","Application Layer Gateway; deep inspection for embedded IPs/ports","Inspection"),
    ("Screen","zone-based attack detection and prevention","Threat Prevention"),
    ("IPsec VPN","encrypted tunnel for site-to-site connectivity","VPN"),
    ("Route-based VPN","IPsec tunnel bound to a st0 interface for routing","VPN"),
    ("Policy-based VPN","IPsec triggered by security policy match","VPN"),
    ("IKE Phase 1","authenticated ISAKMP tunnel for management traffic","IPsec"),
    ("IKE Phase 2","IPsec child SA for encrypted data traffic","IPsec"),
    ("NAT Source","translating private source IPs to public IPs","NAT"),
    ("NAT Destination","translating public destination IPs to private IPs","NAT"),
    ("PAT","Port Address Translation; many-to-one with port multiplexing","NAT"),
    ("SecIntel","cloud threat intelligence blocking malicious IPs/URLs","Threat Prevention"),
    ("IDP","Intrusion Detection and Prevention; signature-based traffic inspection","Threat Prevention"),
    ("Chassis Cluster","two SRX devices as HA pair with stateful failover","HA"),
    ("Control Link","fab0 interface for chassis cluster control plane IPC","HA"),
    ("Fabric Link","fab1 interface for session state replication","HA"),
    ("Active/Passive","one node active forwarding traffic; standby takes over on failure","HA"),
    ("Active/Active","both nodes forwarding traffic with load balancing","HA"),
    ("Flow Mode","stateful inspection mode tracking session state","Mode"),
    ("Packet Mode","fast forwarding without stateful inspection","Mode"),
    ("UTM","unified threat management with antivirus, filtering, and anti-spam","Threat Prevention"),
    ("AppSecure","application identification and application-based policies","Policy"),
    ("UserFirewall","identity-based policies using Active Directory integration","Policy"),
]

# HA: (concept, description, category)
HA = [
    ("GRES","Graceful RE Switchover; preserves interface and kernel state","Juniper HA"),
    ("NSR","Nonstop Active Routing; protocol state synced to standby RE","Juniper HA"),
    ("BGP Graceful Restart","BGP capability preserving routes during RE switchover","Graceful Restart"),
    ("NSF","Nonstop Forwarding; continues forwarding during control plane restart","Graceful Restart"),
    ("IS-IS GR","IS-IS graceful restart for hitless IGP restart","Graceful Restart"),
    ("OSPF GR","OSPF graceful restart preserving LSDB during restart","Graceful Restart"),
    ("LDP GR","LDP graceful restart preserving label bindings","Graceful Restart"),
    ("VRRP","Virtual Router Redundancy Protocol for gateway failover","FHRP"),
    ("HSRP","Cisco Hot Standby Router Protocol active/standby","FHRP"),
    ("GLBP","Cisco Gateway Load Balancing Protocol with active/active","FHRP"),
    ("Link Aggregation","bonding multiple links for bandwidth and redundancy","Layer 2"),
    ("MC-LAG","Multi-Chassis LAG for active-active multi-homing","Layer 2"),
    ("Fabric LACP","LACP across chassis cluster members for MC-LAG","Layer 2"),
    ("RE Switchover","manual or triggered switch to standby RE","Procedure"),
]

# OSPF: (concept, description, type)
OSPF = [
    ("Type 1 (Router) LSA","advertises router link states within its own area","LSA Type"),
    ("Type 2 (Network) LSA","advertises network segment info; generated by DR","LSA Type"),
    ("Type 3 (Summary) LSA","inter-area route advertisement from ABR","LSA Type"),
    ("Type 4 (ASBR Summary) LSA","advertises ASBR reachability to other areas","LSA Type"),
    ("Type 5 (External) LSA","external route advertisement from ASBR","LSA Type"),
    ("Type 7 (NSSA) LSA","NSSA external route advertisement","LSA Type"),
    ("ABR","Area Border Router connecting Area 0 to other areas","Node"),
    ("ASBR","AS Boundary Router redistributing external routes","Node"),
    ("DR","Designated Router elected on multi-access networks","Node"),
    ("BDR","Backup Designated Router; takes over if DR fails","Node"),
    ("DROTHER","non-DR/BDR router on multi-access segment","Node"),
    ("Stub Area","blocks Type 5 LSAs; default route for external","Area Type"),
    ("Totally Stubby Area","blocks Type 3/4/5 LSAs; default route only","Area Type"),
    ("NSSA","stub area that imports externals via Type 7 LSAs","Area Type"),
    ("Totally NSSA","NSSA with Type 3/4 summary suppression","Area Type"),
    ("Virtual Link","connects non-backbone area to Area 0 through transit area","Feature"),
    ("SPF Algorithm","Shortest Path First (Dijkstra) computes loop-free routes","Algorithm"),
    ("Area 0","OSPF backbone area connecting all other areas","Fundamental"),
    ("Router ID","unique 32-bit identifier for OSPF router identification","Fundamental"),
    ("Network Type","OSPF network type (broadcast, point-to-point, NBMA, point-to-multipoint)","Fundamental"),
]

# ISIS: (concept, description, type)
ISIS = [
    ("Level 1 Router","intra-area IS-IS routing within a single area","Node"),
    ("Level 2 Router","inter-area IS-IS routing providing backbone connectivity","Node"),
    ("L1/L2 Router","both Level 1 and Level 2; connects area to backbone","Node"),
    ("DIS","Designated IS elected on broadcast segments (preemptable)","Node"),
    ("NET","Network Entity Title; IS-IS address identifying a router","Addressing"),
    ("NSAP","Network Service Access Point; IS-IS addressing scheme","Addressing"),
    ("System ID","6-byte router identifier within IS-IS NET","Addressing"),
    ("Area ID","variable-length area identifier in IS-IS NET","Addressing"),
    ("SNP","Sequence Number PDU; IS-IS database sync mechanism","PDU Type"),
    ("CSNP","Complete SNP; IS-IS database summary by DIS","PDU Type"),
    ("PSNP","Partial SNP; IS-IS request/acknowledge LSPs","PDU Type"),
    ("LSP","Link State PDU; IS-IS equivalent of OSPF LSA","PDU Type"),
    ("IIH","IS-IS Hello PDU; adjacency establishment and keepalive","PDU Type"),
    ("Wide Metrics","IS-IS extended metric support for TE (24-bit vs 6-bit)","Feature"),
    ("Overload Bit","IS-IS overload bit advertising router should be bypassed","Feature"),
]

# MCAST: (concept, description, category)
MCAST = [
    ("PIM Sparse Mode","RP-based multicast distribution; receivers explicitly join","Protocol"),
    ("PIM Dense Mode","flood-and-prune multicast; initial flood then prune branches","Protocol"),
    ("PIM Bidirectional","shared tree multicast; bidirectional traffic on RP tree","Protocol"),
    ("PIM-SSM","Source-Specific Multicast using (S,G) channels exclusively","Protocol"),
    ("IGMPv1","original IGMP with membership query and report","IGMP"),
    ("IGMPv2","IGMP with leave-group messages and query election","IGMP"),
    ("IGMPv3","IGMP with source-specific filtering (INCLUDE/EXCLUDE)","IGMP"),
    ("MLDv1","Multicast Listener Discovery for IPv6","MLD"),
    ("MLDv2","MLD with source-specific filtering for IPv6","MLD"),
    ("MSDP","Multicast Source Discovery Protocol; inter-domain RP discovery","Protocol"),
    ("RP","Rendezvous Point; meeting point for PIM-SM sources and receivers","Node"),
    ("BSR","Bootstrap Router; distributes RP information in PIM domain","Node"),
    ("RPF Check","Reverse Path Forwarding; verifies multicast arrives on correct interface","Procedure"),
    ("(S,G)","Source-specific multicast tree from source to receivers","State"),
    ("(*,G)","Any-source multicast tree shared RP to receivers","State"),
    ("Assert","PIM mechanism to elect a single forwarder on multi-access LAN","Procedure"),
    ("Register","PIM-SM source registration process with RP","Procedure"),
]

# DC: (concept, description, category)
DC = [
    ("Spine-Leaf (Clos)","predictable latency with active-active ECMP between tiers","Architecture"),
    ("Leaf Switch","ToR switch connecting servers with tenant L2/L3 services","Node"),
    ("Spine Switch","core switch interconnecting leaf switches at high speed","Node"),
    ("Overlay Network","virtual network over physical fabric (e.g. VXLAN)","Architecture"),
    ("Underlay Network","physical IP fabric providing VTEP connectivity","Architecture"),
    ("ECMP","equal-cost multi-path load balancing across parallel links","Feature"),
    ("MC-LAG","Multi-Chassis LAG active-active server multi-homing","Feature"),
    ("VCF","Virtual Chassis Fabric; multiple Juniper switches as one device","Technology"),
    ("QFX Fabric","QFX series spine/leaf fabric automation (ZTP/ELS)","Technology"),
    ("EVPN-VXLAN","VXLAN with BGP EVPN control plane for multi-tenancy","Technology"),
]

# AUTO: (concept, description, category)
AUTO = [
    ("PyEZ","Python library for Junos automation via NETCONF","Juniper"),
    ("Ansible","agentless YAML playbook automation over SSH/API","General"),
    ("NETCONF","XML-based network config protocol over SSH (RFC 6241)","Protocol"),
    ("RESTCONF","HTTP-based config protocol using YANG models (RFC 8040)","Protocol"),
    ("gRPC","Google RPC for high-performance streaming telemetry","Protocol"),
    ("Jinja2","Python templating engine for config generation","Tool"),
    ("YANG","data modeling language for config and operational state","Model"),
    ("OpenConfig","vendor-neutral YANG models for multi-vendor environments","Model"),
    ("JTI","Junos Telemetry Interface; streaming operational telemetry","Juniper"),
    ("JSNAPy","Junos Snapshot Administrator; automated testing","Juniper"),
    ("Event Scripts","triggered by system events (interface down, etc.)","Juniper"),
    ("Commit Scripts","validate or modify configuration during commit","Juniper"),
    ("Op Scripts","on-demand operational automation scripts","Juniper"),
    ("SLAX","Junos automation language; XML-based with XSLT syntax","Juniper"),
    ("Python on Junos","Python interpreter running natively on Junos devices","Juniper"),
    ("NAPALM","multi-vendor network automation library","General"),
    ("Salt","event-driven automation with proxy minions","General"),
    ("Terraform","infrastructure-as-code provider for network resources","General"),
    ("Docker","container runtime for containerized network services","Platform"),
    ("Kubernetes","container orchestration for cloud-native networking","Platform"),
]

# L2/STP: (concept, description, category)
STP = [
    ("STP 802.1D","spanning tree with blocking/listening/learning/forwarding; slow convergence","Protocol"),
    ("RSTP 802.1w","rapid STP with discarding/learning/forwarding; fast convergence","Protocol"),
    ("MSTP 802.1s","multiple spanning tree instances with VLAN mapping","Protocol"),
    ("PVST+","Cisco per-VLAN STP with separate instance per VLAN","Protocol"),
    ("Rapid PVST+","Cisco per-VLAN RSTP","Protocol"),
    ("Root Bridge","elected root of spanning tree; all ports are designated","Role"),
    ("Root Port","best path to the root bridge; one per non-root switch","Role"),
    ("Designated Port","best port on a link toward the root; one per segment","Role"),
    ("Alternate Port","backup to root port; blocked in steady state","Role"),
    ("Backup Port","backup to designated port on shared segments","Role"),
    ("Edge Port","port connected to end host; immediate forwarding","Role"),
    ("BPDU Guard","disables port if a BPDU is received on an edge port","Protection"),
    ("Root Guard","prevents receiving superior BPDUs on designated ports","Protection"),
    ("Loop Guard","prevents alternate/root ports from becoming designated if BPDUs stop","Protection"),
    ("BPDU Filter","suppresses sending/receiving BPDUs on a port","Protection"),
    ("PortFast","immediately transitions access port to forwarding","Feature"),
    ("UplinkFast","Cisco fast convergence on root port failure","Feature"),
    ("BackboneFast","Cisco fast convergence after indirect link failure","Feature"),
    ("Bridge ID","8-byte ID: 2-byte priority + 6-byte MAC address","Fundamental"),
    ("Path Cost","port cost toward the root bridge; inversely proportional to speed","Fundamental"),
]

# QOS: (name, dscp_binary, purpose, forwarding_class)
QOS = [
    ("EF (DSCP 46)","101110","Expedited Forwarding for real-time voice","voice"),
    ("AF41 (DSCP 34)","100010","Assured Forwarding class 4 low-drop for video","video"),
    ("AF42 (DSCP 36)","100100","Assured Forwarding class 4 medium-drop","video"),
    ("AF43 (DSCP 38)","100110","Assured Forwarding class 4 high-drop","video"),
    ("AF31 (DSCP 26)","011010","Assured Forwarding class 3 low-drop for business data","business"),
    ("AF32 (DSCP 28)","011100","Assured Forwarding class 3 medium-drop","business"),
    ("AF33 (DSCP 30)","011110","Assured Forwarding class 3 high-drop","business"),
    ("AF21 (DSCP 18)","010010","Assured Forwarding class 2 low-drop for transactional data","transactional"),
    ("AF22 (DSCP 20)","010100","Assured Forwarding class 2 medium-drop","transactional"),
    ("AF23 (DSCP 22)","010110","Assured Forwarding class 2 high-drop","transactional"),
    ("AF11 (DSCP 10)","001010","Assured Forwarding class 1 low-drop for bulk data","bulk"),
    ("AF12 (DSCP 12)","001100","Assured Forwarding class 1 medium-drop","bulk"),
    ("AF13 (DSCP 14)","001110","Assured Forwarding class 1 high-drop","bulk"),
    ("BE (DSCP 0)","000000","Best Effort default forwarding","best-effort"),
    ("CS1 (DSCP 8)","001000","Scavenger class low-priority traffic","scavenger"),
    ("CS2 (DSCP 16)","010000","Less-than-best-effort OAM traffic","oam"),
    ("CS3 (DSCP 24)","011000","Broadcast video traffic","broadcast-video"),
    ("CS4 (DSCP 32)","100000","Real-time interactive traffic","interactive"),
    ("CS5 (DSCP 40)","101000","Voice signaling traffic","signaling"),
    ("CS6 (DSCP 48)","110000","Network control traffic","network-control"),
    ("CS7 (DSCP 56)","111000","Reserved for future use","reserved"),
]

# ROUTE_MGMT: (concept, description, category)
ROUTE_MGMT = [
    ("Route Redistribution","importing routes from one routing protocol into another","Routing Policy"),
    ("Route Summarization","aggregating multiple prefixes into a shorter prefix","Routing Policy"),
    ("Floating Static Route","static route with higher AD for backup path","Static"),
    ("Policy-Based Routing","forwarding based on policies other than destination IP","Routing Policy"),
    ("Routing Policy","set of rules controlling route import, export, and manipulation","Routing Policy"),
    ("Route Filter","matching routes by prefix, protocol, or attributes","Routing Policy"),
    ("Prefix List","ordered list of prefixes with permit/deny actions","Routing Policy"),
    ("AS Path Filter","regex-based matching of BGP AS_PATH attribute","BGP Policy"),
    ("Community Filter","matching routes by BGP community values","BGP Policy"),
    ("Route Map","Cisco route filtering and attribute manipulation construct","Routing Policy"),
    ("Distribute List","filtering routing updates using ACLs or prefix-lists","Routing Policy"),
    ("Offset List","modifying route metrics in OSPF/EIGRP routing updates","Routing Policy"),
    ("Administrative Distance","trustworthiness rating for route selection across protocols","Route Selection"),
    ("Metric","protocol-specific cost value for path comparison","Route Selection"),
    ("ECMP","equal-cost multi-path forwarding across multiple next-hops","Routing"),
    ("Next Hop","next router IP toward destination in forwarding path","Forwarding"),
    ("RIB","Routing Information Base; control plane routing table","Forwarding"),
    ("FIB","Forwarding Information Base; data plane forwarding table","Forwarding"),
    ("CEF","Cisco Express Forwarding; hardware-accelerated FIB with adjacency tables","Forwarding"),
    ("Null Route","route pointing to null interface for discarding traffic","Static"),
]

# IPsec: (concept, description, category)
IPsec = [
    ("IKE","Internet Key Exchange; establishes IPsec security associations","Key Exchange"),
    ("IKE Phase 1","authenticated ISAKMP tunnel for management traffic (main/aggressive mode)","Key Exchange"),
    ("IKE Phase 2","IPsec child SA negotiation for encrypted data traffic","Key Exchange"),
    ("ISAKMP","Internet Security Association and Key Management Protocol (UDP 500)","Protocol"),
    ("ESP","Encapsulating Security Payload; encrypts and authenticates IP packets","Protocol"),
    ("AH","Authentication Header; provides integrity without encryption","Protocol"),
    ("SA","Security Association; simplex IPsec tunnel configuration","Fundamental"),
    ("SPD","Security Policy Database; defines traffic to protect via IPsec","Fundamental"),
    ("PFS","Perfect Forward Secrecy; new Diffie-Hellman key for each phase 2","Security"),
    ("D-H Group","Diffie-Hellman group determining key exchange strength","Security"),
    ("IPsec Transport Mode","encrypts only payload; original IP header preserved","Mode"),
    ("IPsec Tunnel Mode","encrypts entire IP packet; new IP header added","Mode"),
    ("GRE over IPsec","IPsec tunnel encapsulating GRE tunnel with routing protocols","Tunnel"),
    ("IPsec VTI","Virtual Tunnel Interface for route-based IPsec VPNs","Tunnel"),
    ("IPsec DVTI","Dynamic VTI for auto-creating IPsec tunnels","Tunnel"),
    ("Dead Peer Detection","keepalive mechanism detecting IPsec peer failure","Monitoring"),
    ("Anti-Replay","sequence number window protecting against replay attacks","Security"),
    ("NAT-T","NAT Traversal; UDP 4500 encapsulation for IPsec through NAT","Feature"),
]

# NAT: (concept, description, category)
NAT = [
    ("Static NAT","one-to-one fixed IP translation (1 private:1 public)","Translation Type"),
    ("Dynamic NAT","many-to-many IP translation from a pool of public IPs","Translation Type"),
    ("PAT","Port Address Translation; many-to-one with port multiplexing (overload)","Translation Type"),
    ("Source NAT","translating source IP address in outbound traffic","Direction"),
    ("Destination NAT","translating destination IP in inbound traffic","Direction"),
    ("NAT64","translating IPv6 to IPv4 for IPv6-only clients accessing IPv4 servers","Translation Type"),
    ("NPTv6","Network Prefix Translation for IPv6 topology hiding","Translation Type"),
    ("Twice NAT","simultaneous source and destination translation","Translation Type"),
    ("Inside Local","private IP address before NAT on inside network","Terminology"),
    ("Inside Global","public IP address after translation for inside host","Terminology"),
    ("Outside Local","private IP address before NAT for outside host","Terminology"),
    ("Outside Global","public IP address after translation for outside host","Terminology"),
    ("NAT Pool","range of public IPs available for dynamic NAT translations","Configuration"),
    ("NAT Overload","PAT with port multiplexing for many internal hosts","Configuration"),
    ("NAT Hairpinning","traffic from inside to inside through external NAT IP","Feature"),
]

# ════════════════════════════════════════════════
# GENERATOR HELPERS
# ════════════════════════════════════════════════

def pick_n(pool, rng, n=3, exclude=None):
    filtered = [p for p in pool if p != exclude]
    if len(filtered) <= n: return list(filtered)
    return rng.sample(filtered, n)

def shuffle_options(correct_texts, options, rng):
    letters = "ABCDEFGH"
    shuffled = list(options)
    rng.shuffle(shuffled)
    new_opts, correct = [], []
    for i, (txt, _) in enumerate(shuffled):
        l = letters[i]
        is_correct = txt in correct_texts
        new_opts.append((txt, is_correct))
        if is_correct: correct.append(l)
    return new_opts, ",".join(sorted(correct))

def gen_pool_questions(eid, tid, pool, count, section, difficulty, bloom, seed,
                        body_tpl, correct_tpl, wrong_tpl, expl_tpl,
                        weight=14.0):
    """Flexible pool-based question generator.
    Templates can use {label}(field 0), {desc}(field 1), {f0}..{fn} for field access.
    """
    rng = random.Random(seed + hash(body_tpl) % (2**31))
    used = set(); qs = []; pool_list = list(pool)
    max_attempts = count * 5; attempts = 0
    while len(qs) < count and attempts < max_attempts:
        entry = rng.choice(pool_list)
        if isinstance(entry, (list, tuple)):
            fmt = {f"f{i}": str(v) for i, v in enumerate(entry)}
            fmt["label"] = str(entry[0]) if len(entry) > 0 else ""
            fmt["desc"] = str(entry[1]) if len(entry) > 1 else ""
        else:
            fmt = {"label": str(entry), "desc": str(entry)}
        body = body_tpl.format(**fmt)
        if body in used: attempts += 1; continue
        used.add(body)
        correct_val = correct_tpl.format(**fmt)
        wrongs = pick_n(pool_list, rng, 3, exclude=entry)
        wrong_vals = []
        for w in wrongs:
            if isinstance(w, (list, tuple)):
                wfmt = {f"f{i}": str(v) for i, v in enumerate(w)}
                wfmt["label"] = str(w[0]) if len(w) > 0 else ""
                wfmt["desc"] = str(w[1]) if len(w) > 1 else ""
            else:
                wfmt = {"label": str(w), "desc": str(w)}
            wrong_vals.append(wrong_tpl.format(**wfmt))
        opts = [(correct_val, True)] + [(wv, False) for wv in wrong_vals[:3]]
        new_opts, correct_str = shuffle_options({correct_val}, opts, rng)
        expl = expl_tpl.format(**fmt)
        qs.append(make_q(eid, tid, body, new_opts, correct_str, expl,
                         difficulty=difficulty, bloom=bloom, section=section, weight=weight))
        attempts += 1
    return qs

def gen_compare_pool(eid, tid, pool, count, section, difficulty, bloom, seed,
                      body_tpl="What is the difference between {a} and {b}?",
                      correct_tpl="{a} is {a_desc}; {b} is {b_desc}.",
                      weight=14.0):
    """Generate comparison questions from pairs within a pool."""
    rng = random.Random(seed)
    used = set(); qs = []; pool_list = list(pool)
    if len(pool_list) < 2: return []
    max_attempts = count * 10; attempts = 0
    while len(qs) < count and attempts < max_attempts:
        a, b = rng.sample(pool_list, 2)
        a_name = str(a[0]) if isinstance(a, (list, tuple)) else str(a)
        b_name = str(b[0]) if isinstance(b, (list, tuple)) else str(b)
        a_desc = str(a[1]) if isinstance(a, (list, tuple)) and len(a) > 1 else ""
        b_desc = str(b[1]) if isinstance(b, (list, tuple)) and len(b) > 1 else ""
        body = body_tpl.format(a=a_name, b=b_name, a_desc=a_desc, b_desc=b_desc)
        if body in used: attempts += 1; continue
        used.add(body)
        correct_val = correct_tpl.format(a=a_name, b=b_name, a_desc=a_desc, b_desc=b_desc)
        # Generate wrong: description of a or b swapped
        wrong_opts_pool = pick_n(pool_list, rng, 3, exclude=a)
        wrong_vals = []
        for w in wrong_opts_pool:
            w_name = str(w[0]) if isinstance(w, (list, tuple)) else str(w)
            w_desc = str(w[1]) if isinstance(w, (list, tuple)) and len(w) > 1 else ""
            wrong_vals.append(correct_tpl.format(a=a_name, b=w_name, a_desc=a_desc, b_desc=w_desc))
        opts = [(correct_val, True)] + [(wv, False) for wv in wrong_vals[:3]]
        new_opts, correct_str = shuffle_options({correct_val}, opts, rng)
        qs.append(make_q(eid, tid, body, new_opts, correct_str,
            f"{a_name} {a_desc}. {b_name} {b_desc}.",
            difficulty=difficulty, bloom=bloom, section=section, weight=weight))
        attempts += 1
    return qs

def gen_scenario_pool(eid, tid, scenarios, count, section, difficulty, bloom, seed,
                       body_tpl="An engineer configures a network:\n{scenario}\n{condition}. What happens?",
                       weight=14.0):
    """Generate scenario-based questions from NETWORK_SCENES pool."""
    rng = random.Random(seed)
    used = set(); qs = []; pool_list = list(scenarios)
    max_attempts = count * 5; attempts = 0
    while len(qs) < count and attempts < max_attempts:
        entry = rng.choice(pool_list)
        scenario = entry[0]; condition = entry[1]; result = entry[2]
        body = body_tpl.format(scenario=scenario, condition=condition, result=result)
        if body in used: attempts += 1; continue
        used.add(body)
        # Wrong answers: results from other scenarios
        wrongs = pick_n(pool_list, rng, 3, exclude=entry)
        wrong_results = [w[2] for w in wrongs]
        correct_text = {result}
        opts = [(result, True)] + [(w, False) for w in wrong_results[:3]]
        new_opts, correct_str = shuffle_options(correct_text, opts, rng)
        qs.append(make_q(eid, tid, body, new_opts, correct_str,
            f"Given: {scenario}. {condition}. Result: {result}.",
            difficulty=difficulty, bloom=bloom, section=section, weight=weight))
        attempts += 1
    return qs

def gen_term_definition(eid, tid, term_pool, count, section, difficulty, bloom, seed,
                         body_tpl="What is {label}?", weight=14.0):
    """'What is {label}?' with definition as correct answer."""
    return gen_pool_questions(eid, tid, term_pool, count, section, difficulty, bloom, seed,
                               body_tpl, "{f1}", "{f1}", "{label}: {f1}.", weight)

def gen_term_question(eid, tid, term_pool, count, section, difficulty, bloom, seed,
                       body_tpl="Which networking concept {f1}?", correct_field=0, weight=14.0):
    """'Which concept does X?' with concept name as correct answer."""
    return gen_pool_questions(eid, tid, term_pool, count, section, difficulty, bloom, seed,
                               body_tpl, "{label}", "{label}", "{label}: {f1}.", weight)

def gen_cmd_what(eid, tid, cmd_pool, count, section, difficulty, bloom, seed, weight=14.0):
    """'What does {cmd} do?' with description as correct."""
    return gen_pool_questions(eid, tid, cmd_pool, count, section, difficulty, bloom, seed,
                               "What does '{f0}' do?", "{f1}", "{f1}", "'{f0}' {f1}.", weight)

def gen_cmd_which(eid, tid, cmd_pool, count, section, difficulty, bloom, seed, weight=14.0):
    """'Which command {desc}?' with command name as correct."""
    return gen_pool_questions(eid, tid, cmd_pool, count, section, difficulty, bloom, seed,
                               "Which command {f1}?", "{f0}", "{f0}", "'{f0}' {f1}.", weight)

def gen_cmd_section(eid, tid, cmd_pool, count, section, difficulty, bloom, seed, weight=14.0):
    """'Which section does {cmd} belong to?' with section as correct."""
    return gen_pool_questions(eid, tid, cmd_pool, count, section, difficulty, bloom, seed,
                               "Which section does '{f0}' belong to?", "{f2}", "{f2}",
                               "'{f0}' belongs to the {f2} section.", weight)

def gen_troubleshoot_which_cause(eid, tid, tshoot, count, section, difficulty, bloom, seed, weight=14.0):
    """'An engineer sees {symptom}. What is the most likely cause?'"""
    return gen_pool_questions(eid, tid, tshoot, count, section, difficulty, bloom, seed,
                               "An engineer sees: {f0}. What is the most likely cause?",
                               "{f1}", "{f1}", "{f1}. Use {f2} to diagnose.", weight)

def gen_troubleshoot_which_tool(eid, tid, tshoot, count, section, difficulty, bloom, seed, weight=14.0):
    """'To diagnose {symptom}, which tool should be used?'"""
    return gen_pool_questions(eid, tid, tshoot, count, section, difficulty, bloom, seed,
                               "To diagnose '{f0}', which tool or command should be used?",
                               "{f2}", "{f2}", "Use {f2} to check {f1}.", weight)

# ════════════════════════════════════════════════
# EXAM GENERATORS
# Each returns a list of unique questions
# ════════════════════════════════════════════════

def _multi_gen(eid, tid, gen_funcs, seed, targets=None):
    """Helper: run multiple generator calls with seeds.
    Deduplicates questions per-exam (by body text) to maximize unique output.
    """
    rng = random.Random(seed)
    all_q = []
    seen_global = set()  # Global dedup across ALL templates for this exam
    for i, (func, target) in enumerate(gen_funcs):
        gs = seed + i * 1000 + rng.randint(1, 999)
        qs = func(gs)
            # Global dedup across ALL templates for this exam (prevents cross-template duplicates)
        batch = []
        for q in qs:
            b = q["body"]
            if b not in seen_global:
                seen_global.add(b)
                batch.append(q)
        batch = batch[:target]
        all_q.extend(batch)
    return all_q

def gen_jn0_106(eid, tid, seed=42):
    """JNCIA-Junos: ~3,000 unique questions"""
    gen_calls = [
        # PROTOCOLS pool (53 entries × 6 templates = 318 max unique)
        lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 53, "Network Fundamentals", 1, "remember", s,
            "What is {label}?", "{f1}", "{f1}", "{label}: {f6}."),
        lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 53, "Network Fundamentals", 1, "remember", s,
            "Which protocol {f6}?", "{label}", "{label}", "{label} {f6}."),
        lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 53, "Network Fundamentals", 1, "remember", s,
            "What transport does {label} use?", "{f2}", "{f2}", "{label} uses {f2}."),
        lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 53, "Network Fundamentals", 1, "remember", s,
            "At which OSI layer does {label} operate?", "Layer {f1}", "Layer {f1}", "{label} operates at Layer {f1}."),
        lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 53, "Network Fundamentals", 1, "remember", s,
            "What is the Cisco AD of {label}?", "{f3}", "{f3}", "{label} AD is {f3}."),
        lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 53, "Network Fundamentals", 2, "remember", s,
            "What is the Junos preference of {label}?", "{f4}", "{f4}", "{label} preference is {f4}."),
        # JUNOS_CMDS pool (72 entries × 4 templates = 288 max)
        lambda s: gen_cmd_what(eid, tid, JUNOS_CMDS, 72, "Operational Commands", 1, "apply", s),
        lambda s: gen_cmd_which(eid, tid, JUNOS_CMDS, 72, "Operational Commands", 1, "apply", s),
        lambda s: gen_cmd_section(eid, tid, JUNOS_CMDS, 72, "Command Categories", 1, "remember", s),
        lambda s: gen_pool_questions(eid, tid, JUNOS_CMDS, 72, "Operational Commands", 2, "apply", s,
            "To {f1}, which command is used?", "{f0}", "{f0}", "'{f0}' {f1}."),
        # NETWORK_TERMS (90 entries × 3 templates = 270 max)
        lambda s: gen_term_definition(eid, tid, NETWORK_TERMS, 90, "Networking Concepts", 1, "remember", s, "What is {label}?"),
        lambda s: gen_term_question(eid, tid, NETWORK_TERMS, 90, "Networking Concepts", 1, "understand", s, "Which networking concept {f1}?"),
        lambda s: gen_pool_questions(eid, tid, NETWORK_TERMS, 90, "Networking Concepts", 1, "remember", s,
            "Which category does {label} belong to?", "{f2}", "{f2}", "{label} is in {f2} category."),
        # TSHOOT pool (35 entries × 2 templates = 70 unique)
        lambda s: gen_troubleshoot_which_cause(eid, tid, TSHOOT, 35, "Troubleshooting", 3, "analyze", s),
        lambda s: gen_troubleshoot_which_tool(eid, tid, TSHOOT, 35, "Troubleshooting", 3, "apply", s),
        # OSPF pool (20 entries × 3 templates = 60 max)
        lambda s: gen_term_definition(eid, tid, OSPF, 20, "OSPF", 2, "understand", s, "What is {label}?"),
        lambda s: gen_pool_questions(eid, tid, OSPF, 20, "OSPF", 3, "understand", s, "What is the function of {label}?", "{f1}", "{f1}", "{label}: {f1}."),
        lambda s: gen_pool_questions(eid, tid, OSPF, 20, "OSPF", 2, "remember", s, "What type is {label}?", "{f2}", "{f2}", "{label} is an {f2}."),
        # STP pool (20 entries × 3 templates = 60)
        lambda s: gen_term_definition(eid, tid, STP, 20, "Layer 2 / STP", 2, "understand", s, "What is {label}?"),
        lambda s: gen_pool_questions(eid, tid, STP, 20, "Layer 2 / STP", 2, "understand", s, "What category does {label} belong to?", "{f2}", "{f2}", "{label} is a {f2}."),
        lambda s: gen_pool_questions(eid, tid, STP, 20, "Layer 2 / STP", 2, "remember", s, "Which protocol includes {label}?", "{f1}", "{f1}", "{label}: {f1}."),
        # BGP_ATTRS (15 entries × 3 templates = 45)
        lambda s: gen_term_definition(eid, tid, BGP_ATTRS, 15, "BGP Fundamentals", 3, "understand", s, "What is {label}?"),
        lambda s: gen_pool_questions(eid, tid, BGP_ATTRS, 15, "BGP Attributes", 3, "understand", s, "Which BGP attribute {f1}?", "{label}", "{label}", "{label}: {f1}."),
        # SECURITY (25 entries × 2 templates = 50)
        lambda s: gen_term_definition(eid, tid, SECURITY, 25, "Security Fundamentals", 2, "understand", s, "What is {label}?"),
        lambda s: gen_pool_questions(eid, tid, SECURITY, 25, "Security Features", 2, "understand", s, "Which security concept {f1}?", "{label}", "{label}", "{label}: {f1}."),
        # QOS pool (21 entries × 2 templates = 42)
        lambda s: gen_pool_questions(eid, tid, QOS, 21, "QoS", 2, "remember", s, "What is {label}?", "{f2}", "{f2}", "{label}: {f2}."),
        lambda s: gen_pool_questions(eid, tid, QOS, 21, "QoS", 2, "remember", s, "What DSCP value does {label} use?", "{f1}", "{f1}", "{label} uses DSCP {f1}."),
        # HA pool (14 entries × 2 templates = 28)
        lambda s: gen_term_definition(eid, tid, HA, 14, "High Availability", 3, "understand", s, "What is {label}?"),
        # ISIS pool (15 entries × 2 templates = 30)
        lambda s: gen_term_definition(eid, tid, ISIS, 15, "IS-IS", 3, "understand", s, "What is {label}?"),
        # MCAST pool (17 entries × 2 templates = 34)
        lambda s: gen_term_definition(eid, tid, MCAST, 17, "Multicast", 3, "understand", s, "What is {label}?"),
        # NETWORK_SCENES (30 entries × 1 template = 30)
        lambda s: gen_scenario_pool(eid, tid, NETWORK_SCENES, 30, "Network Scenarios", 3, "apply", s),
        # Comparison generators
        lambda s: gen_compare_pool(eid, tid, PROTOCOLS, 80, "Protocol Comparison", 2, "understand", s),
        lambda s: gen_compare_pool(eid, tid, OSPF, 40, "OSPF Concepts", 3, "understand", s),
        lambda s: gen_compare_pool(eid, tid, STP, 30, "STP Feature Comparison", 3, "understand", s),
        # Cross-pool: term used with protocol
        lambda s: gen_pool_questions(eid, tid, NETWORK_TERMS[:45], 45, "Network Scenarios", 2, "understand", s,
            "Which technology is commonly associated with routing between autonomous systems?",
            "{label}", "{label}", "{label}: {f1}."),
        # ADDITIONAL: more template variations for more unique questions
        lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 84, "Network Fundamentals", 1, "remember", s+10,
            "What category does {label} fall under?", "{f5}", "{f5}", "{label} is a {f5} protocol."),
        lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 84, "Network Fundamentals", 1, "remember", s+20,
            "Which protocol uses {f2} as transport?", "{label}", "{label}", "{label} uses {f2}."),
        lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 84, "Network Fundamentals", 1, "remember", s+30,
            "{label} is classified as what type of protocol?", "{f5}", "{f5}", "{label} is a {f5} protocol."),
        lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 84, "Network Fundamentals", 1, "remember", s+40,
            "{label} operates at OSI Layer {f1}. What is its primary purpose?", "{f6}", "{f6}", "{label}: {f6}."),
        lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 84, "Network Fundamentals", 1, "remember", s+50,
            "Which protocol has the purpose: {f6}?", "{label}", "{label}", "{label}: {f6}."),
        lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 84, "Network Fundamentals", 1, "remember", s+60,
            "At OSI Layer {f1}, which protocol uses transport {f2}?", "{label}", "{label}", "{label} operates at Layer {f1} using {f2}."),

        # Additional CMDS templates
        lambda s: gen_pool_questions(eid, tid, JUNOS_CMDS, 106, "Operational Commands", 1, "apply", s+100,
            "{f0} is used for what purpose on Junos?", "{f1}", "{f1}", "'{f0}' {f1}."),
        lambda s: gen_pool_questions(eid, tid, JUNOS_CMDS, 106, "Operational Commands", 2, "apply", s+200,
            "Which command falls under the {f2} section?", "{f0}", "{f0}", "'{f0}' belongs to the {f2} section."),
        lambda s: gen_pool_questions(eid, tid, JUNOS_CMDS, 106, "Command Categories", 1, "remember", s+300,
            "The command '{f0}' is used in which section?", "{f2}", "{f2}", "'{f0}' is in {f2}."),
        lambda s: gen_pool_questions(eid, tid, JUNOS_CMDS, 106, "Command Categories", 1, "remember", s+400,
            "{f1} Which command provides this information on Junos?", "{f0}", "{f0}", "'{f0}' {f1}."),
        # Additional TERMS templates
        lambda s: gen_pool_questions(eid, tid, NETWORK_TERMS, 96, "Networking Concepts", 1, "remember", s+500,
            "{label}: {f1}. What category does this belong to?", "{f2}", "{f2}", "{label} is in {f2}."),
        lambda s: gen_pool_questions(eid, tid, NETWORK_TERMS, 96, "Networking Concepts", 1, "understand", s+600,
            "Which term is described as: {f1}?", "{label}", "{label}", "{label}: {f1}."),
        lambda s: gen_pool_questions(eid, tid, NETWORK_TERMS, 96, "Networking Concepts", 1, "remember", s+700,
            "What is the function of {label}?", "{f1}", "{f1}", "{label}: {f1}."),
        # Additional TSHOOT templates
        lambda s: gen_pool_questions(eid, tid, TSHOOT, 55, "Troubleshooting", 3, "analyze", s+800,
            "A network engineer diagnoses: '{f0}'. What device type is experiencing this?", "{f3}", "{f3}", "{f0} occurs on {f3}."),
        # Additional OSPF templates
        lambda s: gen_term_question(eid, tid, OSPF, 20, "OSPF", 2, "understand", s+900, 
            "Which OSPF component {f1}?"),
        # Additional STP templates
        lambda s: gen_pool_questions(eid, tid, STP, 20, "Layer 2 / STP", 2, "understand", s+1000,
            "What is the role of {label} in a spanning tree topology?", "{f1}", "{f1}", "{label}: {f1}."),
        # Additional BGP templates
        lambda s: gen_pool_questions(eid, tid, BGP_ATTRS, 15, "BGP Attributes", 3, "understand", s+1100,
            "Is {label} a well-known mandatory BGP attribute?", "Yes" if True else "No", "Yes", "{label} attributes."),
        # Cross-pool: command + protocol
        lambda s: gen_pool_questions(eid, tid, JUNOS_CMDS, 106, "Cross-Pool: Commands", 2, "apply", s+1200,
            "What information does '{f0}' provide?", "{f1}", "{f1}", "'{f0}' {f1}."),

        # MORE PROTOCOLS templates for JNCIA
                lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 84, "Protocol Fundamentals", 1, "remember", s+1300,
                    "{label} is used for what purpose?", "{f6}", "{f6}", "{label}: {f6}."),
                lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 84, "Protocol Fundamentals", 1, "remember", s+1310,
                    "What is the layer and transport of {label}?", "Layer {f1}, {f2}", "Layer {f1}, {f2}", "{label}: Layer {f1}, transport {f2}."),
                lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 84, "Protocol Fundamentals", 2, "understand", s+1320,
                    "Which protocol matches the description: {f6}?", "{label}", "{label}", "{label}: {f6}."),
                lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 84, "Protocol Fundamentals", 2, "understand", s+1330,
                    "For {label}, which layer and transport are used?", "Layer {f1}, {f2}", "Layer {f1}, {f2}", "{label} uses Layer {f1} with {f2}."),
                # MORE CMDS templates for JNCIA
                lambda s: gen_pool_questions(eid, tid, JUNOS_CMDS, 106, "Operational Commands", 2, "apply", s+1400,
                    "Which Junos command is used for: {f1}?", "{f0}", "{f0}", "'{f0}' {f1}."),
                lambda s: gen_pool_questions(eid, tid, JUNOS_CMDS, 106, "Command Details", 2, "apply", s+1410,
                    "{f0} provides what information on Junos?", "{f1}", "{f1}", "'{f0}' {f1}."),
                lambda s: gen_pool_questions(eid, tid, JUNOS_CMDS, 106, "Command Sections", 2, "remember", s+1420,
                    "The command '{f0}' is part of which section?", "{f2}", "{f2}", "'{f0}' is in {f2} section."),
                # MORE TERMS templates for JNCIA
                lambda s: gen_pool_questions(eid, tid, NETWORK_TERMS, 96, "Networking Concepts", 2, "understand", s+1500,
                    "Which term is described as: {f1}?", "{label}", "{label}", "{label}: {f1}."),
                lambda s: gen_pool_questions(eid, tid, NETWORK_TERMS, 96, "Networking Concepts", 2, "understand", s+1510,
                    "{label}: {f1}. What is this term?", "{label}", "{label}", "{label}: {f1}."),
    ]
    return _multi_gen(eid, tid, [(f, 9999) for f in gen_calls], seed)

def gen_200_301(eid, tid, seed=42):
    """CCNA: ~2,000 unique questions"""
    gen_calls = [
        # PROTOCOLS
        lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 53, "Network Fundamentals", 1, "remember", s,
            "What is {label}?", "{f1}", "{f1}", "{label}: {f6}."),
        lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 53, "Network Fundamentals", 1, "remember", s,
            "Which protocol {f6}?", "{label}", "{label}", "{label} {f6}."),
        lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 53, "Network Fundamentals", 1, "remember", s,
            "What transport does {label} use?", "{f2}", "{f2}", "{label} uses {f2}."),
        lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 53, "Network Fundamentals", 1, "remember", s,
            "At which OSI layer does {label} operate?", "Layer {f1}", "Layer {f1}", "{label} operates at Layer {f1}."),
        lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 53, "Routing Protocols", 2, "understand", s,
            "What is the Cisco AD of {label}?", "{f3}", "{f3}", "{label} AD is {f3}."),
        # CISCO_CMDS
        lambda s: gen_cmd_what(eid, tid, CISCO_CMDS, 40, "Cisco Operational Commands", 1, "apply", s),
        lambda s: gen_cmd_which(eid, tid, CISCO_CMDS, 40, "Cisco Operational Commands", 1, "apply", s),
        lambda s: gen_cmd_section(eid, tid, CISCO_CMDS, 40, "Command Categories", 1, "remember", s),
        # NETWORK_TERMS
        lambda s: gen_term_definition(eid, tid, NETWORK_TERMS, 90, "Networking Concepts", 1, "remember", s, "What is {label}?"),
        lambda s: gen_term_question(eid, tid, NETWORK_TERMS, 90, "Networking Concepts", 1, "understand", s, "Which networking concept {f1}?"),
        # TSHOOT
        lambda s: gen_troubleshoot_which_cause(eid, tid, TSHOOT, 35, "Troubleshooting", 3, "analyze", s),
        lambda s: gen_troubleshoot_which_tool(eid, tid, TSHOOT, 35, "Troubleshooting", 3, "apply", s),
        # STP
        lambda s: gen_term_definition(eid, tid, STP, 20, "STP / Layer 2", 2, "understand", s, "What is {label}?"),
        lambda s: gen_term_definition(eid, tid, STP, 20, "STP Features", 2, "understand", s, "What category does {label} belong to?"),
        # OSPF
        lambda s: gen_term_definition(eid, tid, OSPF, 20, "OSPF", 3, "understand", s, "What is {label}?"),
        lambda s: gen_pool_questions(eid, tid, OSPF, 20, "OSPF", 3, "understand", s, "What does {label} do?", "{f1}", "{f1}", "{label}: {f1}."),
        # SECURITY
        lambda s: gen_term_definition(eid, tid, SECURITY, 25, "Security", 2, "understand", s, "What is {label}?"),
        # DHCP/NAT (from TSHOOT)
        lambda s: gen_troubleshoot_which_cause(eid, tid, TSHOOT, 35, "DHCP & NAT", 2, "understand", s),
        # HA/FHRP
        lambda s: gen_term_definition(eid, tid, HA, 14, "FHRP / HA", 3, "understand", s, "What is {label}?"),
        # NETWORK_SCENES
        lambda s: gen_scenario_pool(eid, tid, NETWORK_SCENES, 30, "Network Scenarios", 3, "analyze", s),
        # Comparison
        lambda s: gen_compare_pool(eid, tid, PROTOCOLS, 60, "Protocol Comparison", 2, "understand", s),
        lambda s: gen_compare_pool(eid, tid, STP, 30, "STP Comparison", 3, "understand", s),
        # ADDITIONAL: more template variations for more unique questions
        lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 84, "Network Fundamentals", 1, "remember", s+10,
            "What category does {label} fall under?", "{f5}", "{f5}", "{label} is a {f5} protocol."),
        lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 84, "Network Fundamentals", 1, "remember", s+20,
            "Which protocol uses {f2} as transport?", "{label}", "{label}", "{label} uses {f2}."),
        lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 84, "Network Fundamentals", 1, "remember", s+30,
            "{label} is classified as what type of protocol?", "{f5}", "{f5}", "{label} is a {f5} protocol."),
        lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 84, "Network Fundamentals", 1, "remember", s+40,
            "{label} operates at OSI Layer {f1}. What is its primary purpose?", "{f6}", "{f6}", "{label}: {f6}."),
        lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 84, "Network Fundamentals", 1, "remember", s+50,
            "Which protocol has the purpose: {f6}?", "{label}", "{label}", "{label}: {f6}."),
        lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 84, "Network Fundamentals", 1, "remember", s+60,
            "At OSI Layer {f1}, which protocol uses transport {f2}?", "{label}", "{label}", "{label} operates at Layer {f1} using {f2}."),

        # Additional CISCO_CMDS templates
        lambda s: gen_pool_questions(eid, tid, CISCO_CMDS, 67, "Cisco Operational Commands", 1, "apply", s+100,
            "On Cisco IOS, what does '{f0}' display?", "{f1}", "{f1}", "'{f0}' {f1}."),
        lambda s: gen_pool_questions(eid, tid, CISCO_CMDS, 67, "Cisco Commands", 2, "apply", s+200,
            "Which Cisco command {f1}?", "{f0}", "{f0}", "'{f0}' {f1}."),
        lambda s: gen_pool_questions(eid, tid, CISCO_CMDS, 67, "Cisco Commands", 1, "remember", s+300,
            "From which mode is the command '{f0}' executed?", "{f2}", "{f2}", "'{f0}' is executed from {f2} mode."),
        # Additional TERMS templates
        lambda s: gen_pool_questions(eid, tid, NETWORK_TERMS, 96, "Networking Concepts", 1, "understand", s+500,
            "Which term is described as: {f1}?", "{label}", "{label}", "{label}: {f1}."),
        lambda s: gen_pool_questions(eid, tid, NETWORK_TERMS, 96, "Networking Concepts", 1, "remember", s+600,
            "What is the function of {label}?", "{f1}", "{f1}", "{label}: {f1}."),
        # Additional TSHOOT
        lambda s: gen_troubleshoot_which_tool(eid, tid, TSHOOT, 55, "Cisco Troubleshooting", 3, "apply", s+700),
        # Additional STP
        lambda s: gen_pool_questions(eid, tid, STP, 20, "STP", 2, "understand", s+800,
            "What is the role of {label}?", "{f1}", "{f1}", "{label}: {f1}."),
        # Additional OSPF
        lambda s: gen_term_question(eid, tid, OSPF, 20, "OSPF", 2, "understand", s+900,
            "Which OSPF component {f1}?"),
        # Additional comparison
        lambda s: gen_compare_pool(eid, tid, CISCO_CMDS, 80, "Command Comparison", 2, "understand", s+1000),
        lambda s: gen_compare_pool(eid, tid, NETWORK_TERMS, 80, "Network Concept Comparison", 2, "understand", s+1100),
        # Additional scenarios
        lambda s: gen_scenario_pool(eid, tid, NETWORK_SCENES, 59, "Network Scenarios", 3, "apply", s+1200),

    ]
    return _multi_gen(eid, tid, [(f, 9999) for f in gen_calls], seed)

def gen_jn0_650(eid, tid, seed=42):
    """JNCIP-ENT: ~1,600 questions"""
    gen_calls = [
        lambda s: gen_term_definition(eid, tid, OSPF, 20, "OSPF", 3, "understand", s, "What is {label}?"),
        lambda s: gen_pool_questions(eid, tid, OSPF, 20, "OSPF Concepts", 3, "understand", s, "What does {label} do?", "{f1}", "{f1}", "{label}: {f1}."),
        lambda s: gen_term_definition(eid, tid, ISIS, 15, "IS-IS", 3, "understand", s, "What is {label}?"),
        lambda s: gen_pool_questions(eid, tid, ISIS, 15, "IS-IS", 3, "understand", s, "What is the function of {label}?", "{f1}", "{f1}", "{label}: {f1}."),
        lambda s: gen_term_definition(eid, tid, BGP_ATTRS, 15, "BGP Attributes", 4, "understand", s, "What is {label}?"),
        lambda s: gen_pool_questions(eid, tid, BGP_ATTRS, 15, "BGP Path Selection", 4, "understand", s, "Which BGP attribute {f1}?", "{label}", "{label}", "{label}: {f1}."),
        lambda s: gen_term_definition(eid, tid, EVPN, 15, "EVPN-VXLAN", 4, "understand", s, "What is {label}?"),
        lambda s: gen_pool_questions(eid, tid, EVPN, 15, "EVPN Route Types", 4, "understand", s, "What does {label} do?", "{f1}", "{f1}", "{label}: {f1}."),
        lambda s: gen_term_definition(eid, tid, MCAST, 17, "Multicast", 3, "understand", s, "What is {label}?"),
        lambda s: gen_term_definition(eid, tid, HA, 14, "High Availability", 3, "understand", s, "What is {label}?"),
        lambda s: gen_pool_questions(eid, tid, HA, 14, "HA Features", 3, "understand", s, "Which HA concept {f1}?", "{label}", "{label}", "{label}: {f1}."),
        lambda s: gen_pool_questions(eid, tid, QOS, 21, "QoS / CoS", 3, "understand", s, "What is {label}?", "{f2}", "{f2}", "{label}: {f2}."),
        lambda s: gen_pool_questions(eid, tid, QOS, 21, "QoS / CoS", 3, "understand", s, "What forwarding class uses {label}?", "{f3}", "{f3}", "{label} forwards {f3} traffic."),
        lambda s: gen_term_definition(eid, tid, STP, 20, "STP / Bridging", 3, "understand", s, "What is {label}?"),
        lambda s: gen_pool_questions(eid, tid, STP, 20, "STP Protection Features", 3, "understand", s, "What does {label} protect against?", "{f1}", "{f1}", "{label}: {f1}."),
        lambda s: gen_term_definition(eid, tid, ROUTE_MGMT, 20, "Route Policy & Redistribution", 3, "understand", s, "What is {label}?"),
        lambda s: gen_scenario_pool(eid, tid, NETWORK_SCENES, 30, "Advanced Scenarios", 4, "analyze", s),
        lambda s: gen_compare_pool(eid, tid, OSPF, 50, "OSPF Comparison", 3, "understand", s),
        lambda s: gen_compare_pool(eid, tid, STP, 40, "STP Comparison", 3, "understand", s),
        lambda s: gen_compare_pool(eid, tid, BGP_ATTRS, 40, "BGP Attribute Comparison", 4, "understand", s),
        lambda s: gen_compare_pool(eid, tid, HA, 30, "HA Feature Comparison", 3, "understand", s),
        # Additional OSPF templates
        lambda s: gen_term_question(eid, tid, OSPF, 20, "OSPF", 3, "understand", s+10,
            "Which OSPF component {f1}?"),
        lambda s: gen_pool_questions(eid, tid, OSPF, 20, "OSPF Operations", 3, "apply", s+20,
            "What type is {label}?", "{f2}", "{f2}", "{label} is a {f2}."),
        # Additional ISIS templates
        lambda s: gen_term_question(eid, tid, ISIS, 15, "IS-IS", 3, "understand", s+30,
            "Which IS-IS component {f1}?"),
        lambda s: gen_pool_questions(eid, tid, ISIS, 15, "IS-IS Protocol", 3, "understand", s+40,
            "What category does {label} belong to?", "{f2}", "{f2}", "{label} is a {f2}."),
        # Additional BGP templates
        lambda s: gen_pool_questions(eid, tid, BGP_ATTRS, 15, "BGP Attributes", 4, "understand", s+50,
            "Which attribute {f1}?", "{label}", "{label}", "{label}: {f1}."),
        # Additional EVPN templates
        lambda s: gen_term_question(eid, tid, EVPN, 15, "EVPN-VXLAN", 4, "understand", s+60,
            "Which EVPN concept {f1}?"),
        lambda s: gen_pool_questions(eid, tid, EVPN, 15, "EVPN Route Types", 4, "understand", s+70,
            "What is the purpose of {label}?", "{f1}", "{f1}", "{label}: {f1}."),
        # Additional Multicast templates
        lambda s: gen_term_question(eid, tid, MCAST, 17, "Multicast", 3, "understand", s+80,
            "Which multicast concept {f1}?"),
        # Additional HA templates
        lambda s: gen_term_question(eid, tid, HA, 14, "High Availability", 3, "understand", s+90,
            "Which HA feature {f1}?"),
        # Additional QoS templates
        lambda s: gen_pool_questions(eid, tid, QOS, 21, "QoS CoS", 3, "understand", s+100,
            "{label} is used for what purpose?", "{f2}", "{f2}", "{label}: {f2}."),
        lambda s: gen_pool_questions(eid, tid, QOS, 21, "QoS CoS", 3, "understand", s+110,
            "What forwarding class does {label} map to?", "{f3}", "{f3}", "{label} maps to {f3}."),
        # Additional STP
        lambda s: gen_term_question(eid, tid, STP, 20, "STP / Bridging", 3, "understand", s+120,
            "Which STP concept {f1}?"),
        lambda s: gen_pool_questions(eid, tid, STP, 20, "STP Protection", 3, "understand", s+130,
            "What does {label} do?", "{f1}", "{f1}", "{label}: {f1}."),
        # Additional ROUTE_MGMT
        lambda s: gen_term_question(eid, tid, ROUTE_MGMT, 20, "Routing Policy", 3, "understand", s+140,
            "Which routing concept {f1}?"),
        lambda s: gen_term_definition(eid, tid, ROUTE_MGMT, 20, "Route Redistribution", 3, "understand", s+150,
            "What is {label} in routing?"),
        # More comparison
        lambda s: gen_compare_pool(eid, tid, ISIS, 30, "IS-IS Comparison", 3, "understand", s+160),
        lambda s: gen_compare_pool(eid, tid, EVPN, 30, "EVPN Comparison", 4, "understand", s+170),
        lambda s: gen_compare_pool(eid, tid, MCAST, 40, "Multicast Protocol Comparison", 3, "understand", s+180),
        lambda s: gen_compare_pool(eid, tid, QOS, 50, "QoS Class Comparison", 3, "understand", s+190),
        # More scenarios
        lambda s: gen_scenario_pool(eid, tid, NETWORK_SCENES, 59, "ENT Scenarios", 4, "analyze", s+200),

        # PROTOCOLS for JNCIP-ENT (big pool = 84 entries)
                lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 84, "Routing Protocols", 2, "remember", s+300,
                    "What is {label} and what is its primary purpose?", "{f6}", "{f6}", "{label}: {f6}."),
                lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 84, "Network Fundamentals", 2, "understand", s+310,
                    "Which protocol is classified as {f5}?", "{label}", "{label}", "{label} is a {f5} protocol."),
                lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 84, "Protocol Transport", 2, "remember", s+320,
                    "What transport mechanism does {label} rely on?", "{f2}", "{f2}", "{label} uses {f2}."),
                lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 84, "Routing Protocols", 2, "understand", s+330,
                    "{label} operates at OSI Layer {f1}. What is its role?", "{f6}", "{f6}", "{label} (Layer {f1}): {f6}."),
                lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 84, "Protocol Categories", 2, "remember", s+340,
                    "Which protocol category includes {label}?", "{f5}", "{f5}", "{label} belongs to {f5}."),
                lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 84, "Routing Table", 2, "understand", s+350,
                    "What is the Junos preference of {label}?", "{f4}", "{f4}", "{label} has Junos preference {f4}."),
                lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 84, "Routing Table", 2, "understand", s+360,
                    "What is the Cisco AD of {label}?", "{f3}", "{f3}", "{label} has Cisco AD {f3}."),
                lambda s: gen_pool_questions(eid, tid, PROTOCOLS, 84, "Protocol Operations", 2, "understand", s+370,
                    "Which protocol is described as: {f6}?", "{label}", "{label}", "{label}: {f6}."),
                # CMDS-based templates for JNCIP-ENT
                lambda s: gen_cmd_what(eid, tid, JUNOS_CMDS, 106, "Enterprise Commands", 2, "apply", s+380),
                lambda s: gen_cmd_which(eid, tid, JUNOS_CMDS, 106, "Enterprise Commands", 2, "apply", s+390),
                lambda s: gen_cmd_section(eid, tid, JUNOS_CMDS, 106, "Command Categories", 2, "remember", s+400),
                lambda s: gen_pool_questions(eid, tid, JUNOS_CMDS, 106, "Operational Commands", 2, "apply", s+410,
                    "To {f1}, which Junos command is used?", "{f0}", "{f0}", "'{f0}' {f1}."),
                # NETWORK_TERMS for JNCIP-ENT
                lambda s: gen_term_definition(eid, tid, NETWORK_TERMS, 96, "Enterprise Networking", 2, "understand", s+420, "What is {label}?"),
                lambda s: gen_term_question(eid, tid, NETWORK_TERMS, 96, "Enterprise Concepts", 2, "understand", s+430, "Which networking concept {f1}?"),
    ]
    return _multi_gen(eid, tid, [(f, 9999) for f in gen_calls], seed)

def gen_jn0_201(eid, tid, seed=42):
    """JNCIA-SP: ~500 questions"""
    gen_calls = [
        lambda s: gen_term_definition(eid, tid, MPLS, 25, "MPLS Fundamentals", 2, "understand", s, "What is {label}?"),
        lambda s: gen_pool_questions(eid, tid, MPLS, 25, "MPLS Operations", 3, "understand", s, "What does {label} do?", "{f1}", "{f1}", "{label}: {f1}."),
        lambda s: gen_pool_questions(eid, tid, MPLS, 25, "MPLS Categories", 2, "remember", s, "What category does {label} belong to?", "{f2}", "{f2}", "{label} is {f2}."),
        lambda s: gen_term_definition(eid, tid, EVPN, 15, "EVPN Fundamentals", 3, "understand", s, "What is {label}?"),
        lambda s: gen_pool_questions(eid, tid, EVPN, 15, "EVPN Route Types", 3, "understand", s, "What does {label} do?", "{f1}", "{f1}", "{label}: {f1}."),
        lambda s: gen_troubleshoot_which_cause(eid, tid, TSHOOT, 35, "SP Troubleshooting", 3, "analyze", s),
        lambda s: gen_compare_pool(eid, tid, MPLS, 40, "MPLS Concept Comparison", 3, "understand", s),
        lambda s: gen_scenario_pool(eid, tid, NETWORK_SCENES, 30, "SP Scenarios", 3, "analyze", s),
        # Additional templates
        lambda s: gen_term_definition(eid, tid, MPLS, 30, "MPLS Fundamentals", 2, "understand", s+10,
            "What is {label}?"),
        lambda s: gen_term_question(eid, tid, MPLS, 30, "MPLS Fundamentals", 2, "understand", s+20,
            "Which concept {f1}?"),
        lambda s: gen_compare_pool(eid, tid, MPLS, 30, "Concept Comparison", 2, "understand", s+30),
        lambda s: gen_scenario_pool(eid, tid, NETWORK_SCENES, 59, "Network Scenarios", 3, "apply", s+40),
        lambda s: gen_troubleshoot_which_cause(eid, tid, TSHOOT, 55, "Troubleshooting", 3, "analyze", s+50),
        lambda s: gen_troubleshoot_which_tool(eid, tid, TSHOOT, 55, "Troubleshooting Tools", 3, "apply", s+60),

    ]
    return _multi_gen(eid, tid, [(f, 9999) for f in gen_calls], seed)

def gen_jn0_230(eid, tid, seed=42):
    """JNCIA-SEC: ~500 questions"""
    gen_calls = [
        lambda s: gen_term_definition(eid, tid, SECURITY, 25, "Security Fundamentals", 2, "understand", s, "What is {label}?"),
        lambda s: gen_pool_questions(eid, tid, SECURITY, 25, "Security Features", 3, "understand", s, "What does {label} do?", "{f1}", "{f1}", "{label}: {f1}."),
        lambda s: gen_pool_questions(eid, tid, SECURITY, 25, "Security Categories", 2, "remember", s, "What category does {label} belong to?", "{f2}", "{f2}", "{label} is {f2}."),
        lambda s: gen_term_definition(eid, tid, NAT, 15, "NAT Concepts", 2, "understand", s, "What is {label}?"),
        lambda s: gen_troubleshoot_which_cause(eid, tid, TSHOOT, 35, "Security Troubleshooting", 3, "analyze", s),
        lambda s: gen_compare_pool(eid, tid, SECURITY, 50, "Security Feature Comparison", 3, "understand", s),
        lambda s: gen_scenario_pool(eid, tid, NETWORK_SCENES, 30, "Security Scenarios", 3, "analyze", s),
        # Additional templates
        lambda s: gen_term_definition(eid, tid, SECURITY, 30, "Security Fundamentals", 2, "understand", s+10,
            "What is {label}?"),
        lambda s: gen_term_question(eid, tid, SECURITY, 30, "Security Fundamentals", 2, "understand", s+20,
            "Which concept {f1}?"),
        lambda s: gen_compare_pool(eid, tid, SECURITY, 30, "Concept Comparison", 2, "understand", s+30),
        lambda s: gen_scenario_pool(eid, tid, NETWORK_SCENES, 59, "Network Scenarios", 3, "apply", s+40),
        lambda s: gen_troubleshoot_which_cause(eid, tid, TSHOOT, 55, "Troubleshooting", 3, "analyze", s+50),
        lambda s: gen_troubleshoot_which_tool(eid, tid, TSHOOT, 55, "Troubleshooting Tools", 3, "apply", s+60),

    ]
    return _multi_gen(eid, tid, [(f, 9999) for f in gen_calls], seed)

def gen_jn0_480(eid, tid, seed=42):
    """JNCIA-DC: ~500 questions"""
    gen_calls = [
        lambda s: gen_term_definition(eid, tid, DC, 10, "Data Center Architecture", 2, "understand", s, "What is {label}?"),
        lambda s: gen_pool_questions(eid, tid, DC, 10, "DC Concepts", 2, "understand", s, "What does {label} do?", "{f1}", "{f1}", "{label}: {f1}."),
        lambda s: gen_term_definition(eid, tid, EVPN, 15, "EVPN-VXLAN", 3, "understand", s, "What is {label}?"),
        lambda s: gen_pool_questions(eid, tid, EVPN, 15, "EVPN Route Types", 3, "understand", s, "What does {label} do?", "{f1}", "{f1}", "{label}: {f1}."),
        lambda s: gen_term_definition(eid, tid, NETWORK_TERMS, 50, "DC Networking", 2, "understand", s, "What is {label}?"),
        lambda s: gen_compare_pool(eid, tid, DC, 30, "DC Concept Comparison", 3, "understand", s),
        lambda s: gen_scenario_pool(eid, tid, NETWORK_SCENES, 30, "DC Scenarios", 3, "analyze", s),
        # Additional templates
        lambda s: gen_term_definition(eid, tid, DC, 30, "DC Concepts", 2, "understand", s+10,
            "What is {label}?"),
        lambda s: gen_term_question(eid, tid, DC, 30, "DC Concepts", 2, "understand", s+20,
            "Which concept {f1}?"),
        lambda s: gen_compare_pool(eid, tid, DC, 30, "Concept Comparison", 2, "understand", s+30),
        lambda s: gen_scenario_pool(eid, tid, NETWORK_SCENES, 59, "Network Scenarios", 3, "apply", s+40),
        lambda s: gen_troubleshoot_which_cause(eid, tid, TSHOOT, 55, "Troubleshooting", 3, "analyze", s+50),
        lambda s: gen_troubleshoot_which_tool(eid, tid, TSHOOT, 55, "Troubleshooting Tools", 3, "apply", s+60),

    ]
    return _multi_gen(eid, tid, [(f, 9999) for f in gen_calls], seed)

def gen_jn0_223(eid, tid, seed=42):
    """JNCIA-AUT: ~500 questions"""
    gen_calls = [
        lambda s: gen_term_definition(eid, tid, AUTO, 20, "Automation Concepts", 2, "understand", s, "What is {label}?"),
        lambda s: gen_pool_questions(eid, tid, AUTO, 20, "Automation Tools", 3, "understand", s, "What does {label} do?", "{f1}", "{f1}", "{label}: {f1}."),
        lambda s: gen_pool_questions(eid, tid, AUTO, 20, "Automation Categories", 2, "remember", s, "What category does {label} belong to?", "{f2}", "{f2}", "{label} is {f2}."),
        lambda s: gen_term_definition(eid, tid, NETWORK_TERMS[50:], 40, "Network Automation", 2, "understand", s, "What is {label}?"),
        lambda s: gen_compare_pool(eid, tid, AUTO, 40, "Automation Tool Comparison", 3, "understand", s),
        lambda s: gen_scenario_pool(eid, tid, NETWORK_SCENES, 20, "Automation Scenarios", 3, "analyze", s),
        # Additional templates
        lambda s: gen_term_definition(eid, tid, AUTO, 30, "Automation Fundamentals", 2, "understand", s+10,
            "What is {label}?"),
        lambda s: gen_term_question(eid, tid, AUTO, 30, "Automation Fundamentals", 2, "understand", s+20,
            "Which concept {f1}?"),
        lambda s: gen_compare_pool(eid, tid, AUTO, 30, "Concept Comparison", 2, "understand", s+30),
        lambda s: gen_scenario_pool(eid, tid, NETWORK_SCENES, 59, "Network Scenarios", 3, "apply", s+40),
        lambda s: gen_troubleshoot_which_cause(eid, tid, TSHOOT, 55, "Troubleshooting", 3, "analyze", s+50),
        lambda s: gen_troubleshoot_which_tool(eid, tid, TSHOOT, 55, "Troubleshooting Tools", 3, "apply", s+60),

    ]
    return _multi_gen(eid, tid, [(f, 9999) for f in gen_calls], seed)

def gen_jncip_sp(eid, tid, seed=42):
    """JNCIP-SP: ~500 questions"""
    gen_calls = [
        lambda s: gen_term_definition(eid, tid, MPLS, 25, "Advanced MPLS", 4, "understand", s, "What is {label}?"),
        lambda s: gen_pool_questions(eid, tid, MPLS, 25, "MPLS VPN", 4, "understand", s, "What does {label} do?", "{f1}", "{f1}", "{label}: {f1}."),
        lambda s: gen_term_definition(eid, tid, EVPN, 15, "EVPN", 4, "understand", s, "What is {label}?"),
        lambda s: gen_pool_questions(eid, tid, EVPN, 15, "EVPN Route Types", 4, "understand", s, "What does {label} do?", "{f1}", "{f1}", "{label}: {f1}."),
        lambda s: gen_term_definition(eid, tid, BGP_ATTRS, 15, "Advanced BGP", 4, "understand", s, "What is {label}?"),
        lambda s: gen_troubleshoot_which_cause(eid, tid, TSHOOT, 35, "SP Troubleshooting", 4, "analyze", s),
        lambda s: gen_compare_pool(eid, tid, MPLS, 50, "MPLS Comparison", 4, "understand", s),
        lambda s: gen_scenario_pool(eid, tid, NETWORK_SCENES, 30, "SP Scenarios", 4, "analyze", s),
        # Additional templates
        lambda s: gen_term_definition(eid, tid, MPLS, 30, "Advanced MPLS", 2, "understand", s+10,
            "What is {label}?"),
        lambda s: gen_term_question(eid, tid, MPLS, 30, "Advanced MPLS", 2, "understand", s+20,
            "Which concept {f1}?"),
        lambda s: gen_compare_pool(eid, tid, MPLS, 30, "Concept Comparison", 2, "understand", s+30),
        lambda s: gen_scenario_pool(eid, tid, NETWORK_SCENES, 59, "Network Scenarios", 3, "apply", s+40),
        lambda s: gen_troubleshoot_which_cause(eid, tid, TSHOOT, 55, "Troubleshooting", 3, "analyze", s+50),
        lambda s: gen_troubleshoot_which_tool(eid, tid, TSHOOT, 55, "Troubleshooting Tools", 3, "apply", s+60),

        lambda s: gen_compare_pool(eid, tid, EVPN, 30, "EVPN Comparison", 4, "understand", s+200),
        lambda s: gen_compare_pool(eid, tid, BGP_ATTRS, 30, "BGP Attribute Comparison", 4, "understand", s+210),

    ]
    return _multi_gen(eid, tid, [(f, 9999) for f in gen_calls], seed)

def gen_jncip_sec(eid, tid, seed=42):
    """JNCIP-SEC: ~500 questions"""
    gen_calls = [
        lambda s: gen_term_definition(eid, tid, SECURITY, 25, "Advanced Security", 3, "understand", s, "What is {label}?"),
        lambda s: gen_pool_questions(eid, tid, SECURITY, 25, "SRX Features", 4, "understand", s, "What does {label} do?", "{f1}", "{f1}", "{label}: {f1}."),
        lambda s: gen_pool_questions(eid, tid, SECURITY, 25, "Security Categories", 2, "remember", s, "What category does {label} belong to?", "{f2}", "{f2}", "{label} is {f2}."),
        lambda s: gen_term_definition(eid, tid, IPsec, 18, "IPsec VPN", 4, "understand", s, "What is {label}?"),
        lambda s: gen_troubleshoot_which_cause(eid, tid, TSHOOT, 35, "Security Troubleshooting", 4, "analyze", s),
        lambda s: gen_compare_pool(eid, tid, SECURITY, 50, "Security Comparison", 4, "understand", s),
        lambda s: gen_scenario_pool(eid, tid, NETWORK_SCENES, 30, "Security Scenarios", 4, "analyze", s),
        # Additional templates
        lambda s: gen_term_definition(eid, tid, IPsec, 30, "IPsec VPN", 2, "understand", s+10,
            "What is {label}?"),
        lambda s: gen_term_question(eid, tid, IPsec, 30, "IPsec VPN", 2, "understand", s+20,
            "Which concept {f1}?"),
        lambda s: gen_compare_pool(eid, tid, IPsec, 30, "Concept Comparison", 2, "understand", s+30),
        lambda s: gen_scenario_pool(eid, tid, NETWORK_SCENES, 59, "Network Scenarios", 3, "apply", s+40),
        lambda s: gen_troubleshoot_which_cause(eid, tid, TSHOOT, 55, "Troubleshooting", 3, "analyze", s+50),
        lambda s: gen_troubleshoot_which_tool(eid, tid, TSHOOT, 55, "Troubleshooting Tools", 3, "apply", s+60),

        lambda s: gen_compare_pool(eid, tid, SECURITY, 50, "Security Comparison", 4, "understand", s+200),
        lambda s: gen_compare_pool(eid, tid, IPsec, 30, "IPsec Comparison", 4, "understand", s+210),

    ]
    return _multi_gen(eid, tid, [(f, 9999) for f in gen_calls], seed)

def gen_jncip_dc(eid, tid, seed=42):
    """JNCIP-DC: ~500 questions"""
    gen_calls = [
        lambda s: gen_term_definition(eid, tid, DC, 10, "DC Architecture", 4, "understand", s, "What is {label}?"),
        lambda s: gen_term_definition(eid, tid, EVPN, 15, "EVPN Operations", 4, "understand", s, "What is {label}?"),
        lambda s: gen_pool_questions(eid, tid, EVPN, 15, "VXLAN", 3, "understand", s, "What does {label} do?", "{f1}", "{f1}", "{label}: {f1}."),
        lambda s: gen_term_definition(eid, tid, NETWORK_TERMS, 50, "DC Concepts", 3, "understand", s, "What is {label}?"),
        lambda s: gen_compare_pool(eid, tid, DC, 30, "DC Comparison", 4, "understand", s),
        lambda s: gen_compare_pool(eid, tid, EVPN, 30, "EVPN Comparison", 4, "understand", s),
        lambda s: gen_scenario_pool(eid, tid, NETWORK_SCENES, 30, "DC Scenarios", 4, "analyze", s),
        # Additional templates
        lambda s: gen_term_definition(eid, tid, EVPN, 30, "EVPN Operations", 2, "understand", s+10,
            "What is {label}?"),
        lambda s: gen_term_question(eid, tid, EVPN, 30, "EVPN Operations", 2, "understand", s+20,
            "Which concept {f1}?"),
        lambda s: gen_compare_pool(eid, tid, EVPN, 30, "Concept Comparison", 2, "understand", s+30),
        lambda s: gen_scenario_pool(eid, tid, NETWORK_SCENES, 59, "Network Scenarios", 3, "apply", s+40),
        lambda s: gen_troubleshoot_which_cause(eid, tid, TSHOOT, 55, "Troubleshooting", 3, "analyze", s+50),
        lambda s: gen_troubleshoot_which_tool(eid, tid, TSHOOT, 55, "Troubleshooting Tools", 3, "apply", s+60),

        lambda s: gen_compare_pool(eid, tid, DC, 30, "DC Comparison", 4, "understand", s+200),
        lambda s: gen_scenario_pool(eid, tid, NETWORK_SCENES, 59, "DC Scenarios", 4, "analyze", s+210),

    ]
    return _multi_gen(eid, tid, [(f, 9999) for f in gen_calls], seed)

def gen_jncip_aut(eid, tid, seed=42):
    """JNCIP-AUT: ~500 questions"""
    gen_calls = [
        lambda s: gen_term_definition(eid, tid, AUTO, 20, "Advanced Automation", 4, "understand", s, "What is {label}?"),
        lambda s: gen_pool_questions(eid, tid, AUTO, 20, "Automation Frameworks", 4, "understand", s, "What does {label} do?", "{f1}", "{f1}", "{label}: {f1}."),
        lambda s: gen_pool_questions(eid, tid, AUTO, 20, "Automation Categories", 2, "remember", s, "What category does {label} belong to?", "{f2}", "{f2}", "{label} is {f2}."),
        lambda s: gen_term_definition(eid, tid, NETWORK_TERMS[50:], 40, "Network Automation", 3, "understand", s, "What is {label}?"),
        lambda s: gen_compare_pool(eid, tid, AUTO, 40, "Automation Comparison", 4, "understand", s),
        lambda s: gen_scenario_pool(eid, tid, NETWORK_SCENES, 20, "Automation Scenarios", 4, "analyze", s),
        # Additional templates
        lambda s: gen_term_definition(eid, tid, AUTO, 30, "Advanced Automation", 2, "understand", s+10,
            "What is {label}?"),
        lambda s: gen_term_question(eid, tid, AUTO, 30, "Advanced Automation", 2, "understand", s+20,
            "Which concept {f1}?"),
        lambda s: gen_compare_pool(eid, tid, AUTO, 30, "Concept Comparison", 2, "understand", s+30),
        lambda s: gen_scenario_pool(eid, tid, NETWORK_SCENES, 59, "Network Scenarios", 3, "apply", s+40),
        lambda s: gen_troubleshoot_which_cause(eid, tid, TSHOOT, 55, "Troubleshooting", 3, "analyze", s+50),
        lambda s: gen_troubleshoot_which_tool(eid, tid, TSHOOT, 55, "Troubleshooting Tools", 3, "apply", s+60),

        lambda s: gen_compare_pool(eid, tid, AUTO, 40, "Automation Comparison", 4, "understand", s+200),
        lambda s: gen_scenario_pool(eid, tid, NETWORK_SCENES, 59, "Automation Scenarios", 4, "analyze", s+210),

    ]
    return _multi_gen(eid, tid, [(f, 9999) for f in gen_calls], seed)

# ============================================================
# Generator Registry
# ============================================================
GENERATORS = {
    "JN0-106": gen_jn0_106,  # 3,000 target
    "200-301": gen_200_301,   # 2,000 target
    "JN0-650": gen_jn0_650,   # 1,600 target
    "JN0-201": gen_jn0_201,   # 500
    "JN0-230": gen_jn0_230,   # 500
    "JN0-480": gen_jn0_480,   # 500
    "JN0-223": gen_jn0_223,   # 500
    "JNCIP-SP": gen_jncip_sp, # 500
    "JNCIP-SEC": gen_jncip_sec,# 500
    "JNCIP-DC": gen_jncip_dc, # 500
    "JNCIP-AUT": gen_jncip_aut,# 500
}

# ============================================================
# SQL Generation
# ============================================================
def questions_to_sql(questions, suffix=""):
    lines = ["-- Auto-generated by NetCert Pro v6", f"-- {len(questions)} unique questions\n"]
    for q in questions:
        h = hashlib.sha256((q["body"] + suffix).encode()).hexdigest()[:16]
        qid = str(uuid.uuid4())
        opts = json.dumps(q["options"], ensure_ascii=False)
        def esc(s): return s.replace("'", "''") if s else ""
        be, ee = esc(q["body"]), esc(q["explanation"])
        refs = "{" + ",".join(f'"{u}"' for u in q.get("reference_urls",[])) + "}"
        eid, tid = q["exam_id"], q["track_id"]
        if not eid: continue
        lines.append(f"INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, "
                      f"body, options, explanation, reference_urls, blueprint_section, blueprint_weight, "
                      f"content_hash, is_active) VALUES ('{qid}', '{eid}', '{tid}', '{q['question_type']}', "
                      f"{q['difficulty']}, '{q['bloom_level']}', '{be}', '{esc(opts)}', '{ee}', '{refs}', "
                      f"'{q['blueprint_section']}', {q['blueprint_weight']}, '{h}{suffix}', true) ON CONFLICT (id) DO NOTHING;")
    lines.append("")
    lines.append("UPDATE exams SET total_questions = (SELECT COUNT(*)::int FROM questions WHERE exam_id = exams.id);")
    return "\n".join(lines)

def generate_explanations_sql(questions, suffix=""):
    lines = ["-- Auto-generated explanations\n"]
    for q in questions:
        h = hashlib.sha256((q["body"] + suffix).encode()).hexdigest()[:16] + suffix
        expl = q["explanation"]
        sections = [{"type":"tldr","title":"TL;DR","content":expl[:200]}]
        if q["question_type"] == "single-choice":
            correct_ids = {o["id"] for o in q["options"] if o["is_correct"]}
            dists = [f"**{o['id']}** - Incorrect." for o in q["options"] if o["id"] not in correct_ids]
            if dists:
                sections.append({"type":"distractor_breakdown","title":"Answer Breakdown","content":"\n\n".join(dists)})
        sj = json.dumps(sections, ensure_ascii=False).replace("'", "''")
        sm = expl[:200].replace("'", "''")
        lines.append(f"INSERT INTO explanations (id, question_id, version, sections, summary, created_at)\n"
                      f"SELECT gen_random_uuid(), q.id, 1, '{sj}', '{sm}', NOW()\n"
                      f"FROM questions q WHERE q.content_hash = '{h}' "
                      f"AND NOT EXISTS (SELECT 1 FROM explanations e WHERE e.question_id = q.id);")
    return "\n".join(lines)

def main():
    targets = [
        ("JN0-106", 3000), ("200-301", 2000), ("JN0-650", 1600),
        ("JN0-201", 500), ("JN0-230", 500), ("JN0-480", 500),
        ("JN0-223", 500), ("JNCIP-SP", 500), ("JNCIP-SEC", 500),
        ("JNCIP-DC", 500), ("JNCIP-AUT", 500),
    ]
    all_q = []
    for code, target in targets:
        eid, tid, _ = EXAM[code]
        gen = GENERATORS[code]
        qs = gen(eid, tid, seed=42)
        qs = qs[:target]
        all_q.extend(qs)
        print(f"  {code}: {len(qs)} questions", file=sys.stderr)
    print(file=sys.stderr)
    print(f"Total: {len(all_q)} questions", file=sys.stderr)
    bodies = [q["body"] for q in all_q]
    unique_bodies = len(set(bodies))
    print(f"Unique bodies: {unique_bodies}/{len(all_q)} ({unique_bodies*100//len(all_q)}%)", file=sys.stderr)
    print(file=sys.stderr)
    print("-- QUESTIONS START --")
    print(questions_to_sql(all_q, "_gen_v6"))
    print("-- EXPLANATIONS START --")
    print(generate_explanations_sql(all_q, "_gen_v6"))

if __name__ == "__main__": main()
