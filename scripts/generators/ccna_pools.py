"""Content pools for CCNA 200-301 v1.1 question generation."""

# Category names for section-based multiple-choice questions
CCNA_CATEGORIES = {
    "1.1 Network Components": "network devices",
    "1.2 Network Topology": "network topologies or deployment models",
    "1.3 Physical Interfaces": "cabling or interface technologies",
    "1.4 TCP/UDP": "TCP/UDP protocols or concepts",
    "1.5 IPv4/IPv6 Addressing": "IPv4/IPv6 addressing concepts",
    "2.1 Switching Concepts": "switching concepts",
    "2.2 VLANs": "VLAN concepts",
    "2.3 Inter-Switch Connectivity": "inter-switch connectivity technologies",
    "2.4 STP": "Spanning Tree Protocol concepts",
    "2.5 Wireless": "wireless networking concepts",
    "3.1 Routing Fundamentals": "routing fundamentals",
    "3.2 OSPF": "OSPF concepts",
    "3.3 EIGRP": "EIGRP concepts",
    "3.4 BGP": "BGP concepts",
    "4.1 NAT": "NAT concepts",
    "4.2 NTP/DHCP/DNS": "NTP, DHCP, or DNS concepts",
    "4.3 SNMP/Syslog/SSH": "SNMP, Syslog, or SSH concepts",
    "4.4 QoS": "QoS concepts",
    "5.1 Security Concepts": "security concepts",
    "5.2 Access Control": "access control features",
    "5.3 Wireless Security": "wireless security standards",
    "6.1 Automation": "automation or orchestration concepts",
    "6.2 APIs": "API or data format concepts",
    "6.3 AI/ML": "AI/ML or telemetry concepts",
}

CCNA_SECTIONS = {
    "1.0 Network Fundamentals": ("1.0 Network Fundamentals", 20.0),
    "1.1 Network Components": ("1.0 Network Fundamentals", 20.0),
    "1.2 Network Topology": ("1.0 Network Fundamentals", 20.0),
    "1.3 Physical Interfaces": ("1.0 Network Fundamentals", 20.0),
    "1.4 TCP/UDP": ("1.0 Network Fundamentals", 20.0),
    "1.5 IPv4/IPv6 Addressing": ("1.0 Network Fundamentals", 20.0),
    "2.0 Network Access": ("2.0 Network Access", 20.0),
    "2.1 Switching Concepts": ("2.0 Network Access", 20.0),
    "2.2 VLANs": ("2.0 Network Access", 20.0),
    "2.3 Inter-Switch Connectivity": ("2.0 Network Access", 20.0),
    "2.4 STP": ("2.0 Network Access", 20.0),
    "2.5 Wireless": ("2.0 Network Access", 20.0),
    "3.0 IP Connectivity": ("3.0 IP Connectivity", 25.0),
    "3.1 Routing Fundamentals": ("3.0 IP Connectivity", 25.0),
    "3.2 OSPF": ("3.0 IP Connectivity", 25.0),
    "3.3 EIGRP": ("3.0 IP Connectivity", 25.0),
    "3.4 BGP": ("3.0 IP Connectivity", 25.0),
    "4.0 IP Services": ("4.0 IP Services", 10.0),
    "4.1 NAT": ("4.0 IP Services", 10.0),
    "4.2 NTP/DHCP/DNS": ("4.0 IP Services", 10.0),
    "4.3 SNMP/Syslog/SSH": ("4.0 IP Services", 10.0),
    "4.4 QoS": ("4.0 IP Services", 10.0),
    "5.0 Security Fundamentals": ("5.0 Security Fundamentals", 15.0),
    "5.1 Security Concepts": ("5.0 Security Fundamentals", 15.0),
    "5.2 Access Control": ("5.0 Security Fundamentals", 15.0),
    "5.3 Wireless Security": ("5.0 Security Fundamentals", 15.0),
    "6.0 Automation and Programmability": ("6.0 Automation and Programmability", 10.0),
    "6.1 Automation": ("6.0 Automation and Programmability", 10.0),
    "6.2 APIs": ("6.0 Automation and Programmability", 10.0),
    "6.3 AI/ML": ("6.0 Automation and Programmability", 10.0),
}

# Structured protocol pool: name, port, transport, osi_layer, section_key
CCNA_PROTOCOLS = [
    ("SSH", "22", "TCP", "Application", "1.4 TCP/UDP"),
    ("Telnet", "23", "TCP", "Application", "1.4 TCP/UDP"),
    ("FTP control", "21", "TCP", "Application", "1.4 TCP/UDP"),
    ("FTP data", "20", "TCP", "Application", "1.4 TCP/UDP"),
    ("SFTP", "22", "TCP", "Application", "1.4 TCP/UDP"),
    ("TFTP", "69", "UDP", "Application", "1.4 TCP/UDP"),
    ("SNMP agent", "161", "UDP", "Application", "1.4 TCP/UDP"),
    ("SNMP trap", "162", "UDP", "Application", "1.4 TCP/UDP"),
    ("DNS", "53", "UDP/TCP", "Application", "1.4 TCP/UDP"),
    ("DHCP server", "67", "UDP", "Application", "1.4 TCP/UDP"),
    ("DHCP client", "68", "UDP", "Application", "1.4 TCP/UDP"),
    ("NTP", "123", "UDP", "Application", "1.4 TCP/UDP"),
    ("SMTP", "25", "TCP", "Application", "1.4 TCP/UDP"),
    ("POP3", "110", "TCP", "Application", "1.4 TCP/UDP"),
    ("IMAP", "143", "TCP", "Application", "1.4 TCP/UDP"),
    ("HTTP", "80", "TCP", "Application", "1.4 TCP/UDP"),
    ("HTTPS", "443", "TCP", "Application", "1.4 TCP/UDP"),
    ("BGP", "179", "TCP", "Application", "3.4 BGP"),
    ("Syslog", "514", "UDP", "Application", "4.3 SNMP/Syslog/SSH"),
    ("RIP", "520", "UDP", "Application", "3.1 Routing Fundamentals"),
    ("RADIUS", "1812/1813", "UDP", "Application", "5.2 Access Control"),
    ("TACACS+", "49", "TCP", "Application", "5.2 Access Control"),
    ("LDAP", "389", "TCP/UDP", "Application", "5.2 Access Control"),
    ("LDAPS", "636", "TCP", "Application", "5.2 Access Control"),
]

# Structured device pool: name, osi_layer, function, section_key
CCNA_DEVICES = [
    ("Hub", "Layer 1", "repeats electrical signals to all ports", "1.1 Network Components"),
    ("Switch", "Layer 2", "forwards frames based on MAC addresses", "1.1 Network Components"),
    ("Router", "Layer 3", "forwards packets based on IP addresses", "1.1 Network Components"),
    ("Firewall", "Layer 3-7", "filters traffic based on policy", "1.1 Network Components"),
    ("Access point", "Layer 2", "connects wireless clients to wired network", "1.1 Network Components"),
    ("Bridge", "Layer 2", "segments collision domains", "1.1 Network Components"),
    ("Load balancer", "Layer 4-7", "distributes traffic across servers", "1.1 Network Components"),
    ("Proxy server", "Layer 7", "intermediates client requests", "1.1 Network Components"),
    ("IDS", "Layer 1-7", "detects intrusions and alerts", "1.1 Network Components"),
    ("IPS", "Layer 1-7", "detects and blocks intrusions", "1.1 Network Components"),
    ("WLC", "Layer 2", "manages multiple access points", "1.1 Network Components"),
    ("Repeater", "Layer 1", "regenerates signals to extend distance", "1.1 Network Components"),
]

# Structured cable pool: type, max_speed, max_distance, category, section_key
CCNA_CABLES = [
    ("Cat 5e UTP", "1 Gbps", "100 m", "copper", "1.3 Physical Interfaces"),
    ("Cat 6 UTP", "10 Gbps", "55 m", "copper", "1.3 Physical Interfaces"),
    ("Cat 6a UTP", "10 Gbps", "100 m", "copper", "1.3 Physical Interfaces"),
    ("Cat 7 STP", "10 Gbps", "100 m", "copper", "1.3 Physical Interfaces"),
    ("Single-mode fiber", "100 Gbps+", "km", "fiber", "1.3 Physical Interfaces"),
    ("Multimode fiber", "10-100 Gbps", "up to 550 m", "fiber", "1.3 Physical Interfaces"),
    ("RG-6 coaxial", "1 Gbps+", "100 m", "copper", "1.3 Physical Interfaces"),
]

# Structured wireless standards: name, band, max_speed, section_key
CCNA_WIRELESS = [
    ("802.11a", "5 GHz", "54 Mbps", "2.5 Wireless"),
    ("802.11b", "2.4 GHz", "11 Mbps", "2.5 Wireless"),
    ("802.11g", "2.4 GHz", "54 Mbps", "2.5 Wireless"),
    ("802.11n", "2.4/5 GHz", "600 Mbps", "2.5 Wireless"),
    ("802.11ac", "5 GHz", "6.93 Gbps", "2.5 Wireless"),
    ("802.11ax", "2.4/5 GHz", "9.6 Gbps", "2.5 Wireless"),
]

# Term pool: (term, definition, section_key)
CCNA_TERMS = [
    # 1.1 Network Components
    ("Router", "A Layer 3 device that forwards packets based on IP addresses.", "1.1 Network Components"),
    ("Switch", "A Layer 2 device that forwards frames based on MAC addresses.", "1.1 Network Components"),
    ("Hub", "A Layer 1 device that repeats signals to all ports.", "1.1 Network Components"),
    ("Bridge", "A Layer 2 device that segments collision domains.", "1.1 Network Components"),
    ("Access point", "A device that connects wireless clients to a wired network.", "1.1 Network Components"),
    ("Firewall", "A security device that filters traffic based on rules.", "1.1 Network Components"),
    ("NGFW", "A firewall with deep packet inspection and application awareness.", "1.1 Network Components"),
    ("IDS", "A system that detects intrusions and alerts administrators.", "1.1 Network Components"),
    ("IPS", "A system that detects and actively blocks intrusions.", "1.1 Network Components"),
    ("Load balancer", "A device that distributes traffic across multiple servers.", "1.1 Network Components"),
    ("WLC", "A wireless LAN controller that manages multiple access points.", "1.1 Network Components"),
    ("Next-hop", "The next Layer 3 device toward a destination.", "1.1 Network Components"),
    ("Repeater", "A Layer 1 device that regenerates signals to extend distance.", "1.1 Network Components"),
    ("Modem", "A device that modulates/demodulates signals for WAN links.", "1.1 Network Components"),
    ("Proxy server", "An intermediary that handles requests on behalf of clients.", "1.1 Network Components"),

    # 1.2 Network Topology
    ("Two-tier", "A collapsed core/distribution design with access and core layers.", "1.2 Network Topology"),
    ("Three-tier", "A hierarchical design with access, distribution, and core layers.", "1.2 Network Topology"),
    ("Spine-leaf", "A two-layer data center fabric where every leaf connects to every spine.", "1.2 Network Topology"),
    ("SOHO", "A small office/home office network.", "1.2 Network Topology"),
    ("WAN", "A wide area network spanning large geographic areas.", "1.2 Network Topology"),
    ("MAN", "A metropolitan area network spanning a city.", "1.2 Network Topology"),
    ("LAN", "A local area network within a limited area.", "1.2 Network Topology"),
    ("WLAN", "A wireless local area network.", "1.2 Network Topology"),
    ("Public cloud", "Shared cloud infrastructure owned by a provider.", "1.2 Network Topology"),
    ("Private cloud", "Cloud infrastructure dedicated to a single organization.", "1.2 Network Topology"),
    ("Hybrid cloud", "A mix of public and private cloud resources.", "1.2 Network Topology"),
    ("On-premise", "Infrastructure located in the organization's own data center.", "1.2 Network Topology"),
    ("Edge computing", "Processing data near the source rather than in a central data center.", "1.2 Network Topology"),
    ("Campus network", "A network serving buildings in a limited geographic area.", "1.2 Network Topology"),
    ("Branch network", "A remote office connected to a central site.", "1.2 Network Topology"),

    # 1.3 Physical Interfaces
    ("UTP", "Unshielded twisted-pair copper cabling.", "1.3 Physical Interfaces"),
    ("STP", "Shielded twisted-pair copper cabling.", "1.3 Physical Interfaces"),
    ("Fiber optic", "Cabling that uses light for high-speed, long-distance links.", "1.3 Physical Interfaces"),
    ("Single-mode fiber", "Fiber that supports long distances using a single light mode.", "1.3 Physical Interfaces"),
    ("Multimode fiber", "Fiber that supports shorter distances using multiple light modes.", "1.3 Physical Interfaces"),
    ("Cat 5e", "UTP cable supporting up to 1 Gbps at 100 meters.", "1.3 Physical Interfaces"),
    ("Cat 6", "UTP cable supporting 1 Gbps and 10 Gbps at shorter distances.", "1.3 Physical Interfaces"),
    ("Cat 6a", "UTP cable supporting 10 Gbps at 100 meters.", "1.3 Physical Interfaces"),
    ("Cat 7", "STP cable supporting 10 Gbps with individual pair shielding.", "1.3 Physical Interfaces"),
    ("SFP", "Small form-factor pluggable transceiver.", "1.3 Physical Interfaces"),
    ("SFP+", "Enhanced SFP supporting 10 Gbps.", "1.3 Physical Interfaces"),
    ("QSFP", "Quad SFP transceiver for higher speeds.", "1.3 Physical Interfaces"),
    ("QSFP+", "Quad SFP+ supporting 40 Gbps.", "1.3 Physical Interfaces"),
    ("PoE", "Power over Ethernet delivering power over data cables.", "1.3 Physical Interfaces"),
    ("PoE+", "IEEE 802.3at PoE providing up to 30 W per port.", "1.3 Physical Interfaces"),
    ("PoE++", "IEEE 802.3bt PoE providing up to 90 W per port.", "1.3 Physical Interfaces"),
    ("RJ-45", "The standard connector for twisted-pair Ethernet.", "1.3 Physical Interfaces"),
    ("Duplex", "Communication in two directions.", "1.3 Physical Interfaces"),
    ("Auto-MDIX", "Feature that automatically detects cable type.", "1.3 Physical Interfaces"),

    # 1.4 TCP/UDP
    ("TCP", "Connection-oriented transport protocol with reliability and sequencing.", "1.4 TCP/UDP"),
    ("UDP", "Connectionless transport protocol with low overhead.", "1.4 TCP/UDP"),
    ("Three-way handshake", "TCP SYN, SYN-ACK, ACK sequence to establish a connection.", "1.4 TCP/UDP"),
    ("Windowing", "TCP flow control using a window size.", "1.4 TCP/UDP"),
    ("Sequence number", "A TCP field used to reorder segments.", "1.4 TCP/UDP"),
    ("Acknowledgment", "A TCP field confirming receipt of data.", "1.4 TCP/UDP"),
    ("Port", "A 16-bit identifier for an application or service.", "1.4 TCP/UDP"),
    ("Well-known port", "Ports 0–1023 assigned to common services.", "1.4 TCP/UDP"),
    ("Registered port", "Ports 1024–49151 registered with IANA.", "1.4 TCP/UDP"),
    ("Dynamic port", "Ports 49152–65535 used by client applications.", "1.4 TCP/UDP"),
    ("SSH", "Secure Shell using TCP port 22.", "1.4 TCP/UDP"),
    ("Telnet", "Unencrypted remote terminal using TCP port 23.", "1.4 TCP/UDP"),
    ("SFTP", "SSH File Transfer Protocol using TCP port 22.", "1.4 TCP/UDP"),
    ("FTP", "File Transfer Protocol using TCP ports 20 and 21.", "1.4 TCP/UDP"),
    ("TFTP", "Trivial File Transfer Protocol using UDP port 69.", "1.4 TCP/UDP"),
    ("SNMP", "Simple Network Management Protocol using UDP 161/162.", "1.4 TCP/UDP"),
    ("DNS", "Domain Name System using UDP/TCP port 53.", "1.4 TCP/UDP"),
    ("DHCP", "Dynamic Host Configuration Protocol using UDP 67/68.", "1.4 TCP/UDP"),
    ("NTP", "Network Time Protocol using UDP port 123.", "1.4 TCP/UDP"),
    ("SMTP", "Simple Mail Transfer Protocol using TCP port 25.", "1.4 TCP/UDP"),
    ("POP3", "Post Office Protocol v3 using TCP port 110.", "1.4 TCP/UDP"),
    ("IMAP", "Internet Message Access Protocol using TCP port 143.", "1.4 TCP/UDP"),
    ("HTTP", "Hypertext Transfer Protocol using TCP port 80.", "1.4 TCP/UDP"),
    ("HTTPS", "HTTP Secure using TCP port 443.", "1.4 TCP/UDP"),
    ("Syslog", "System logging protocol using UDP port 514.", "1.4 TCP/UDP"),
    ("RIP", "Routing Information Protocol using UDP port 520.", "1.4 TCP/UDP"),
    ("BGP", "Border Gateway Protocol using TCP port 179.", "1.4 TCP/UDP"),
    ("Retransmission", "Resending lost TCP segments.", "1.4 TCP/UDP"),
    ("Sliding window", "TCP mechanism to manage flow control.", "1.4 TCP/UDP"),
    ("MTU", "Maximum Transmission Unit, largest packet size.", "1.4 TCP/UDP"),
    ("MSS", "Maximum Segment Size, largest TCP payload.", "1.4 TCP/UDP"),

    # 1.5 IPv4/IPv6 Addressing
    ("IPv4", "A 32-bit network layer addressing scheme.", "1.5 IPv4/IPv6 Addressing"),
    ("IPv6", "A 128-bit network layer addressing scheme.", "1.5 IPv4/IPv6 Addressing"),
    ("Subnet mask", "A 32-bit value separating network and host portions.", "1.5 IPv4/IPv6 Addressing"),
    ("CIDR", "Classless Inter-Domain Routing notation (e.g., /24).", "1.5 IPv4/IPv6 Addressing"),
    ("Default gateway", "The router used to reach remote networks.", "1.5 IPv4/IPv6 Addressing"),
    ("Loopback", "A virtual interface used for testing and management (127.0.0.1, ::1).", "1.5 IPv4/IPv6 Addressing"),
    ("Link-local", "An IPv6 address valid only on the local segment (fe80::/10).", "1.5 IPv4/IPv6 Addressing"),
    ("Global unicast", "A routable IPv6 address (2000::/3).", "1.5 IPv4/IPv6 Addressing"),
    ("Unique local", "A private IPv6 address (fc00::/7).", "1.5 IPv4/IPv6 Addressing"),
    ("Multicast", "One-to-many communication (IPv4 224.0.0.0/4, IPv6 ff00::/8).", "1.5 IPv4/IPv6 Addressing"),
    ("Anycast", "One-to-nearest communication.", "1.5 IPv4/IPv6 Addressing"),
    ("Broadcast", "One-to-all communication on a subnet.", "1.5 IPv4/IPv6 Addressing"),
    ("APIPA", "Automatic Private IP Addressing (169.254.0.0/16).", "1.5 IPv4/IPv6 Addressing"),
    ("EUI-64", "A method to generate IPv6 interface identifiers from MAC addresses.", "1.5 IPv4/IPv6 Addressing"),
    ("SLAAC", "Stateless Address Autoconfiguration for IPv6.", "1.5 IPv4/IPv6 Addressing"),
    ("DHCPv6", "DHCP for IPv6 address assignment.", "1.5 IPv4/IPv6 Addressing"),
    ("Prefix length", "The number of network bits in an address (e.g., /24).", "1.5 IPv4/IPv6 Addressing"),
    ("Longest prefix match", "Selecting the most specific route for a destination.", "1.5 IPv4/IPv6 Addressing"),
    ("Network address", "The first address in a subnet identifying the network.", "1.5 IPv4/IPv6 Addressing"),
    ("Broadcast address", "The last address in a subnet used for broadcast.", "1.5 IPv4/IPv6 Addressing"),
    ("Host address", "An assignable address between network and broadcast.", "1.5 IPv4/IPv6 Addressing"),
    ("Default route", "A route to 0.0.0.0/0 or ::/0.", "1.5 IPv4/IPv6 Addressing"),
    ("Private IPv4", "RFC 1918 addresses not routable on the Internet.", "1.5 IPv4/IPv6 Addressing"),
    ("Public IPv4", "Globally routable address.", "1.5 IPv4/IPv6 Addressing"),
    ("Class A", "First IPv4 class with default /8 mask.", "1.5 IPv4/IPv6 Addressing"),
    ("Class B", "Second IPv4 class with default /16 mask.", "1.5 IPv4/IPv6 Addressing"),
    ("Class C", "Third IPv4 class with default /24 mask.", "1.5 IPv4/IPv6 Addressing"),
    ("Subnetting", "Dividing a network into smaller networks.", "1.5 IPv4/IPv6 Addressing"),
    ("VLSM", "Variable Length Subnet Masking.", "1.5 IPv4/IPv6 Addressing"),
    ("Summarization", "Advertising multiple routes as a single aggregate.", "1.5 IPv4/IPv6 Addressing"),

    # 2.1 Switching Concepts
    ("MAC address table", "A switch table mapping MAC addresses to ports.", "2.1 Switching Concepts"),
    ("Flooding", "Sending a frame out all ports except the source when destination is unknown.", "2.1 Switching Concepts"),
    ("Filtering", "Forwarding a frame only out the destination port.", "2.1 Switching Concepts"),
    ("Learning", "Recording source MAC addresses on incoming frames.", "2.1 Switching Concepts"),
    ("Aging", "Removing stale MAC addresses from the table.", "2.1 Switching Concepts"),
    ("Collision domain", "A segment where frames can collide.", "2.1 Switching Concepts"),
    ("Broadcast domain", "A logical area where broadcasts propagate.", "2.1 Switching Concepts"),
    ("Half duplex", "Communication in one direction at a time.", "2.1 Switching Concepts"),
    ("Full duplex", "Simultaneous two-way communication without collisions.", "2.1 Switching Concepts"),
    ("CAM table", "Content Addressable Memory table of MAC addresses.", "2.1 Switching Concepts"),
    ("Frame", "A Layer 2 protocol data unit.", "2.1 Switching Concepts"),
    ("Packet", "A Layer 3 protocol data unit.", "2.1 Switching Concepts"),
    ("Segment", "A Layer 4 protocol data unit.", "2.1 Switching Concepts"),
    ("Unicast", "One-to-one communication.", "2.1 Switching Concepts"),
    ("Microsegmentation", "Using switches to create dedicated collision-free segments.", "2.1 Switching Concepts"),

    # 2.2 VLANs
    ("VLAN", "A logical Layer 2 broadcast domain.", "2.2 VLANs"),
    ("Trunk", "A link carrying multiple VLANs with 802.1Q tags.", "2.2 VLANs"),
    ("Access port", "A switch port assigned to a single VLAN.", "2.2 VLANs"),
    ("802.1Q", "The IEEE VLAN tagging standard.", "2.2 VLANs"),
    ("Native VLAN", "The VLAN that carries untagged traffic on a trunk.", "2.2 VLANs"),
    ("DTP", "Cisco Dynamic Trunking Protocol.", "2.2 VLANs"),
    ("VTP", "Cisco VLAN Trunking Protocol.", "2.2 VLANs"),
    ("Inter-VLAN routing", "Routing traffic between VLANs using a Layer 3 device.", "2.2 VLANs"),
    ("SVI", "Switched Virtual Interface for Layer 3 VLAN routing.", "2.2 VLANs"),
    ("Voice VLAN", "A VLAN dedicated to VoIP traffic.", "2.2 VLANs"),
    ("VLAN ID", "A 12-bit identifier for a VLAN (1-4094).", "2.2 VLANs"),
    ("Tagged frame", "A frame with an 802.1Q VLAN header.", "2.2 VLANs"),
    ("Untagged frame", "A frame without a VLAN tag.", "2.2 VLANs"),
    ("Router-on-a-stick", "Inter-VLAN routing using a single trunk to a router.", "2.2 VLANs"),

    # 2.3 Inter-Switch Connectivity
    ("EtherChannel", "Bundling multiple physical links into one logical link.", "2.3 Inter-Switch Connectivity"),
    ("LACP", "Link Aggregation Control Protocol, IEEE 802.3ad.", "2.3 Inter-Switch Connectivity"),
    ("PAgP", "Cisco Port Aggregation Protocol.", "2.3 Inter-Switch Connectivity"),
    ("CDP", "Cisco Discovery Protocol for neighbor information.", "2.3 Inter-Switch Connectivity"),
    ("LLDP", "Link Layer Discovery Protocol, IEEE 802.1AB.", "2.3 Inter-Switch Connectivity"),
    ("UDLD", "Unidirectional Link Detection for fiber links.", "2.3 Inter-Switch Connectivity"),
    ("Port-channel", "A logical interface representing an EtherChannel.", "2.3 Inter-Switch Connectivity"),
    ("Load balancing", "Distributing traffic across multiple links.", "2.3 Inter-Switch Connectivity"),
    ("Active LACP mode", "LACP mode that actively negotiates aggregation.", "2.3 Inter-Switch Connectivity"),
    ("Passive LACP mode", "LACP mode that responds but does not initiate negotiation.", "2.3 Inter-Switch Connectivity"),

    # 2.4 STP
    ("STP", "Spanning Tree Protocol preventing Layer 2 loops.", "2.4 STP"),
    ("RSTP", "Rapid Spanning Tree Protocol with fast convergence.", "2.4 STP"),
    ("PVST+", "Cisco per-VLAN Spanning Tree Plus.", "2.4 STP"),
    ("Rapid PVST+", "Cisco per-VLAN Rapid Spanning Tree.", "2.4 STP"),
    ("MSTP", "Multiple Spanning Tree Protocol.", "2.4 STP"),
    ("Root bridge", "The spanning-tree root with lowest bridge ID.", "2.4 STP"),
    ("Root port", "The best path to the root bridge.", "2.4 STP"),
    ("Designated port", "The best port on a segment toward the root.", "2.4 STP"),
    ("Blocking", "An STP state that does not forward traffic.", "2.4 STP"),
    ("Listening", "An STP transitional state.", "2.4 STP"),
    ("Learning", "An STP state learning MAC addresses but not forwarding.", "2.4 STP"),
    ("Forwarding", "An STP state that forwards traffic.", "2.4 STP"),
    ("Disabled", "An administratively disabled STP port state.", "2.4 STP"),
    ("BPDU", "Bridge Protocol Data Unit used by STP.", "2.4 STP"),
    ("BPDU Guard", "Disables a port receiving BPDUs on a PortFast port.", "2.4 STP"),
    ("Root Guard", "Prevents a port from becoming root.", "2.4 STP"),
    ("Loop Guard", "Prevents loops when BPDUs stop arriving.", "2.4 STP"),
    ("PortFast", "Immediately transitions an access port to forwarding.", "2.4 STP"),
    ("UplinkFast", "Cisco feature for fast root port failover.", "2.4 STP"),
    ("BackboneFast", "Cisco feature for fast indirect link failure recovery.", "2.4 STP"),
    ("Bridge ID", "A combination of bridge priority and MAC address.", "2.4 STP"),
    ("Path cost", "A value used by STP to determine best path.", "2.4 STP"),

    # 2.5 Wireless
    ("SSID", "Service Set Identifier identifying a wireless network.", "2.5 Wireless"),
    ("BSSID", "Basic Service Set Identifier, the MAC of an AP.", "2.5 Wireless"),
    ("Beacon", "A frame advertising an AP's SSID and capabilities.", "2.5 Wireless"),
    ("Infrastructure mode", "AP-centric wireless connectivity.", "2.5 Wireless"),
    ("Ad-hoc mode", "Peer-to-peer wireless without an AP.", "2.5 Wireless"),
    ("2.4 GHz", "A longer-range, more crowded Wi-Fi band.", "2.5 Wireless"),
    ("5 GHz", "A shorter-range, less crowded Wi-Fi band.", "2.5 Wireless"),
    ("6 GHz", "A newer Wi-Fi band with more channels.", "2.5 Wireless"),
    ("Channel", "A specific frequency range used by Wi-Fi.", "2.5 Wireless"),
    ("Channel bonding", "Combining adjacent channels for higher throughput.", "2.5 Wireless"),
    ("MIMO", "Multiple-input multiple-output antenna technology.", "2.5 Wireless"),
    ("MU-MIMO", "Multi-user MIMO serving multiple clients simultaneously.", "2.5 Wireless"),
    ("OFDMA", "Orthogonal Frequency Division Multiple Access for efficiency.", "2.5 Wireless"),
    ("WPA2", "Wi-Fi security using AES-CCMP.", "2.5 Wireless"),
    ("WPA3", "Latest Wi-Fi security standard with SAE.", "2.5 Wireless"),
    ("WLC", "Wireless LAN controller.", "2.5 Wireless"),
    ("Lightweight AP", "An AP managed by a WLC.", "2.5 Wireless"),
    ("Autonomous AP", "A standalone AP without a controller.", "2.5 Wireless"),
    ("Site survey", "An analysis of RF coverage for wireless deployment.", "2.5 Wireless"),
    ("Roaming", "Moving between APs while maintaining connectivity.", "2.5 Wireless"),
    ("RSSI", "Received Signal Strength Indicator.", "2.5 Wireless"),
    ("SNR", "Signal-to-Noise Ratio.", "2.5 Wireless"),

    # 3.1 Routing Fundamentals
    ("Routing table", "A data structure storing known routes.", "3.1 Routing Fundamentals"),
    ("Forwarding table", "A data-plane table used to forward packets.", "3.1 Routing Fundamentals"),
    ("Administrative distance", "Trustworthiness rating of a routing source.", "3.1 Routing Fundamentals"),
    ("Metric", "A value used by a protocol to choose the best path.", "3.1 Routing Fundamentals"),
    ("Longest prefix match", "Selecting the most specific matching route.", "3.1 Routing Fundamentals"),
    ("Static route", "A manually configured route.", "3.1 Routing Fundamentals"),
    ("Default route", "A route to 0.0.0.0/0 used when no specific route matches.", "3.1 Routing Fundamentals"),
    ("Floating static route", "A backup static route with higher AD.", "3.1 Routing Fundamentals"),
    ("Equal-cost load balancing", "Using multiple paths with equal metric.", "3.1 Routing Fundamentals"),
    ("Unequal-cost load balancing", "Using paths with different metrics (EIGRP).", "3.1 Routing Fundamentals"),
    ("Recursive lookup", "Resolving a next-hop address to an egress interface.", "3.1 Routing Fundamentals"),
    ("Route lookup", "The process of finding the best matching route.", "3.1 Routing Fundamentals"),
    ("Routing protocol", "A protocol that dynamically learns network paths.", "3.1 Routing Fundamentals"),
    ("Routed protocol", "A protocol whose packets are forwarded by routers.", "3.1 Routing Fundamentals"),
    ("Gateway of last resort", "The default route used for unknown destinations.", "3.1 Routing Fundamentals"),

    # 3.2 OSPF
    ("OSPF", "Open Shortest Path First link-state IGP.", "3.2 OSPF"),
    ("LSA", "Link-State Advertisement containing topology info.", "3.2 OSPF"),
    ("LSDB", "Link-State Database storing LSAs.", "3.2 OSPF"),
    ("SPF", "Shortest Path First (Dijkstra) calculation.", "3.2 OSPF"),
    ("Area", "A grouping of OSPF routers.", "3.2 OSPF"),
    ("Backbone area", "OSPF Area 0 connecting all other areas.", "3.2 OSPF"),
    ("ABR", "Area Border Router connecting Area 0 to another area.", "3.2 OSPF"),
    ("ASBR", "Autonomous System Boundary Router redistributing external routes.", "3.2 OSPF"),
    ("DR", "Designated Router elected on multi-access segments.", "3.2 OSPF"),
    ("BDR", "Backup Designated Router.", "3.2 OSPF"),
    ("Hello packet", "OSPF packet used to discover/maintain neighbors.", "3.2 OSPF"),
    ("DBD", "Database Description packet summarizing LSAs.", "3.2 OSPF"),
    ("LSR", "Link-State Request packet.", "3.2 OSPF"),
    ("LSU", "Link-State Update packet carrying LSAs.", "3.2 OSPF"),
    ("Neighbor adjacency", "A relationship between two OSPF routers.", "3.2 OSPF"),
    ("Cost", "OSPF metric based on bandwidth.", "3.2 OSPF"),
    ("Stub area", "An OSPF area that does not accept external routes.", "3.2 OSPF"),
    ("Totally stubby area", "An OSPF area that blocks external and inter-area routes.", "3.2 OSPF"),
    ("NSSA", "Not-So-Stubby Area that can originate Type 7 LSAs.", "3.2 OSPF"),
    ("Router ID", "A 32-bit identifier for an OSPF router.", "3.2 OSPF"),
    ("Network type", "OSPF mode such as broadcast, point-to-point, NBMA.", "3.2 OSPF"),
    ("Point-to-point", "An OSPF network type with no DR/BDR election.", "3.2 OSPF"),

    # 3.3 EIGRP
    ("EIGRP", "Enhanced Interior Gateway Routing Protocol.", "3.3 EIGRP"),
    ("DUAL", "Diffusing Update Algorithm for loop-free paths.", "3.3 EIGRP"),
    ("Feasible successor", "A backup loop-free path in EIGRP.", "3.3 EIGRP"),
    ("Successor", "The best path to a destination in EIGRP.", "3.3 EIGRP"),
    ("Feasibility condition", "AD of candidate route < FD of successor.", "3.3 EIGRP"),
    ("Reported distance", "Metric advertised by a neighbor.", "3.3 EIGRP"),
    ("Feasible distance", "Best metric to a destination.", "3.3 EIGRP"),
    ("Composite metric", "EIGRP metric combining bandwidth, delay, load, reliability.", "3.3 EIGRP"),
    ("Autonomous system", "A group of EIGRP routers sharing the same AS number.", "3.3 EIGRP"),
    ("EIGRP neighbor table", "Table of EIGRP neighbors.", "3.3 EIGRP"),
    ("EIGRP topology table", "Table of all known EIGRP routes.", "3.3 EIGRP"),
    ("EIGRP packet", "Update, query, reply, hello packets.", "3.3 EIGRP"),
    ("Reliable Transport Protocol", "EIGRP transport ensuring ordered delivery.", "3.3 EIGRP"),
    ("Protocol-dependent module", "EIGRP component for IPv4 or IPv6.", "3.3 EIGRP"),

    # 3.4 BGP
    ("BGP", "Border Gateway Protocol, path-vector EGP.", "3.4 BGP"),
    ("AS_PATH", "BGP attribute listing autonomous systems in the path.", "3.4 BGP"),
    ("NEXT_HOP", "BGP attribute indicating the next-hop IP.", "3.4 BGP"),
    ("LOCAL_PREF", "BGP attribute influencing outbound path selection.", "3.4 BGP"),
    ("MED", "BGP attribute influencing inbound path selection.", "3.4 BGP"),
    ("ORIGIN", "BGP attribute describing route origin.", "3.4 BGP"),
    ("Weight", "Cisco-proprietary BGP attribute local to a router.", "3.4 BGP"),
    ("eBGP", "BGP between different autonomous systems.", "3.4 BGP"),
    ("iBGP", "BGP within the same autonomous system.", "3.4 BGP"),
    ("Route reflector", "An iBGP peer that reflects routes to clients.", "3.4 BGP"),
    ("Confederation", "Splitting a large AS into smaller sub-ASes.", "3.4 BGP"),
    ("BGP peer", "A neighbor configured for BGP sessions.", "3.4 BGP"),
    ("BGP path selection", "Algorithm selecting the best BGP route.", "3.4 BGP"),
    ("BGP update", "Message advertising or withdrawing routes.", "3.4 BGP"),
    ("Autonomous system", "A collection of networks under a single administrative domain.", "3.4 BGP"),
    ("Peering", "A relationship between two BGP ASes.", "3.4 BGP"),
    ("Transit", "An AS that carries traffic between other ASes.", "3.4 BGP"),

    # 4.1 NAT
    ("NAT", "Network Address Translation.", "4.1 NAT"),
    ("PAT", "Port Address Translation, many-to-one NAT.", "4.1 NAT"),
    ("Static NAT", "One-to-one address translation.", "4.1 NAT"),
    ("Dynamic NAT", "Many-to-many address translation from a pool.", "4.1 NAT"),
    ("Inside local", "Private IP address before NAT.", "4.1 NAT"),
    ("Inside global", "Public IP address after NAT.", "4.1 NAT"),
    ("Outside global", "Public IP of an external host.", "4.1 NAT"),
    ("Outside local", "Private IP of an external host after NAT.", "4.1 NAT"),
    ("NAT overload", "Another name for PAT.", "4.1 NAT"),
    ("NAT pool", "A range of public addresses used by dynamic NAT.", "4.1 NAT"),

    # 4.2 NTP/DHCP/DNS
    ("NTP", "Network Time Protocol synchronizing clocks.", "4.2 NTP/DHCP/DNS"),
    ("DHCP", "Dynamic Host Configuration Protocol assigning IP config.", "4.2 NTP/DHCP/DNS"),
    ("DNS", "Domain Name System resolving names to IPs.", "4.2 NTP/DHCP/DNS"),
    ("DORA", "DHCP Discover, Offer, Request, Ack process.", "4.2 NTP/DHCP/DNS"),
    ("DHCP relay", "Forwarding DHCP requests to a remote server.", "4.2 NTP/DHCP/DNS"),
    ("A record", "DNS record mapping hostname to IPv4.", "4.2 NTP/DHCP/DNS"),
    ("AAAA record", "DNS record mapping hostname to IPv6.", "4.2 NTP/DHCP/DNS"),
    ("CNAME record", "DNS alias record.", "4.2 NTP/DHCP/DNS"),
    ("MX record", "DNS mail exchange record.", "4.2 NTP/DHCP/DNS"),
    ("NS record", "DNS name server record.", "4.2 NTP/DHCP/DNS"),
    ("PTR record", "DNS pointer record for reverse lookups.", "4.2 NTP/DHCP/DNS"),
    ("SOA record", "DNS Start of Authority record.", "4.2 NTP/DHCP/DNS"),
    ("NTP stratum", "A level indicating distance from a reference clock.", "4.2 NTP/DHCP/DNS"),
    ("Lease time", "The duration for which a DHCP address is assigned.", "4.2 NTP/DHCP/DNS"),
    ("Reservation", "A fixed DHCP assignment for a specific MAC.", "4.2 NTP/DHCP/DNS"),

    # 4.3 SNMP/Syslog/SSH
    ("SNMP", "Simple Network Management Protocol.", "4.3 SNMP/Syslog/SSH"),
    ("MIB", "Management Information Base defining managed objects.", "4.3 SNMP/Syslog/SSH"),
    ("OID", "Object Identifier in a MIB tree.", "4.3 SNMP/Syslog/SSH"),
    ("Trap", "An unsolicited SNMP notification.", "4.3 SNMP/Syslog/SSH"),
    ("Inform", "An acknowledged SNMP notification.", "4.3 SNMP/Syslog/SSH"),
    ("Get", "SNMP operation to retrieve a value.", "4.3 SNMP/Syslog/SSH"),
    ("Set", "SNMP operation to change a value.", "4.3 SNMP/Syslog/SSH"),
    ("Walk", "SNMP operation to retrieve a subtree of OIDs.", "4.3 SNMP/Syslog/SSH"),
    ("Syslog", "System logging protocol.", "4.3 SNMP/Syslog/SSH"),
    ("SSH", "Secure Shell encrypted remote access.", "4.3 SNMP/Syslog/SSH"),
    ("Syslog severity", "Priority level from Emergency (0) to Debug (7).", "4.3 SNMP/Syslog/SSH"),
    ("Facility", "Syslog category identifying the source.", "4.3 SNMP/Syslog/SSH"),
    ("Public key", "A key used in asymmetric cryptography.", "4.3 SNMP/Syslog/SSH"),
    ("Private key", "A secret key used to decrypt data.", "4.3 SNMP/Syslog/SSH"),
    ("SCP", "Secure Copy Protocol over SSH.", "4.3 SNMP/Syslog/SSH"),

    # 4.4 QoS
    ("QoS", "Quality of Service prioritizing traffic.", "4.4 QoS"),
    ("DSCP", "Differentiated Services Code Point in IP header.", "4.4 QoS"),
    ("CoS", "Class of Service in 802.1Q tag.", "4.4 QoS"),
    ("Trust boundary", "Where QoS markings are trusted.", "4.4 QoS"),
    ("Classification", "Identifying traffic for QoS treatment.", "4.4 QoS"),
    ("Marking", "Setting DSCP/CoS values.", "4.4 QoS"),
    ("Policing", "Dropping or remarking excess traffic.", "4.4 QoS"),
    ("Shaping", "Buffering excess traffic to smooth the rate.", "4.4 QoS"),
    ("LLQ", "Low Latency Queue for voice.", "4.4 QoS"),
    ("CBWFQ", "Class-Based Weighted Fair Queuing.", "4.4 QoS"),
    ("Congestion avoidance", "Mechanisms like WRED to prevent tail drop.", "4.4 QoS"),
    ("Tail drop", "Dropping packets when a queue is full.", "4.4 QoS"),
    ("Bandwidth", "Guaranteed minimum rate for a traffic class.", "4.4 QoS"),
    ("Priority queue", "A queue serviced before others for delay-sensitive traffic.", "4.4 QoS"),

    # 5.1 Security Concepts
    ("DMZ", "Demilitarized zone hosting public-facing services.", "5.1 Security Concepts"),
    ("Firewall", "Device filtering traffic based on policy.", "5.1 Security Concepts"),
    ("Proxy", "An intermediary for client requests.", "5.1 Security Concepts"),
    ("VPN", "Virtual Private Network extending a private network.", "5.1 Security Concepts"),
    ("IPsec", "Suite of protocols securing IP communications.", "5.1 Security Concepts"),
    ("Malware", "Malicious software.", "5.1 Security Concepts"),
    ("Virus", "Malware requiring a host program.", "5.1 Security Concepts"),
    ("Worm", "Self-replicating malware.", "5.1 Security Concepts"),
    ("Trojan", "Malware disguised as legitimate software.", "5.1 Security Concepts"),
    ("Ransomware", "Malware encrypting data for ransom.", "5.1 Security Concepts"),
    ("Spyware", "Malware that secretly gathers information.", "5.1 Security Concepts"),
    ("Phishing", "Social engineering via fraudulent messages.", "5.1 Security Concepts"),
    ("Spear phishing", "Targeted phishing against specific individuals.", "5.1 Security Concepts"),
    ("DoS", "Denial of Service attack.", "5.1 Security Concepts"),
    ("DDoS", "Distributed Denial of Service attack.", "5.1 Security Concepts"),
    ("Spoofing", "Falsifying source identity.", "5.1 Security Concepts"),
    ("Man-in-the-middle", "Intercepting communications between parties.", "5.1 Security Concepts"),
    ("Social engineering", "Manipulating people into revealing information.", "5.1 Security Concepts"),
    ("Zero-day", "An exploit for a vulnerability not yet patched.", "5.1 Security Concepts"),
    ("Vulnerability", "A weakness that can be exploited.", "5.1 Security Concepts"),
    ("Exploit", "Code that takes advantage of a vulnerability.", "5.1 Security Concepts"),
    ("Threat", "A potential danger to network security.", "5.1 Security Concepts"),
    ("Risk", "Likelihood and impact of a threat exploiting a vulnerability.", "5.1 Security Concepts"),
    ("Least privilege", "Granting only the minimum access required.", "5.1 Security Concepts"),
    ("Defense in depth", "Layered security strategy.", "5.1 Security Concepts"),

    # 5.2 Access Control
    ("ACL", "Access Control List filtering traffic.", "5.2 Access Control"),
    ("Standard ACL", "ACL filtering by source IP only.", "5.2 Access Control"),
    ("Extended ACL", "ACL filtering by source/destination IP, port, protocol.", "5.2 Access Control"),
    ("DHCP snooping", "Validating DHCP messages to prevent rogue servers.", "5.2 Access Control"),
    ("DAI", "Dynamic ARP Inspection preventing ARP spoofing.", "5.2 Access Control"),
    ("IP Source Guard", "Filtering traffic based on DHCP bindings.", "5.2 Access Control"),
    ("Port security", "Limiting MAC addresses on a switch port.", "5.2 Access Control"),
    ("802.1X", "Port-based network access control.", "5.2 Access Control"),
    ("RADIUS", "AAA protocol using UDP.", "5.2 Access Control"),
    ("TACACS+", "Cisco AAA protocol using TCP.", "5.2 Access Control"),
    ("AAA", "Authentication, Authorization, Accounting.", "5.2 Access Control"),
    ("Authentication", "Verifying identity.", "5.2 Access Control"),
    ("Authorization", "Determining what an authenticated user can do.", "5.2 Access Control"),
    ("Accounting", "Tracking user activities and resource usage.", "5.2 Access Control"),
    ("Supplicant", "The client in an 802.1X exchange.", "5.2 Access Control"),
    ("Authenticator", "The network device in an 802.1X exchange.", "5.2 Access Control"),
    ("Certificate", "A digital document binding identity to a public key.", "5.2 Access Control"),

    # 5.3 Wireless Security
    ("WEP", "Wired Equivalent Privacy, weak wireless security.", "5.3 Wireless Security"),
    ("WPA", "Wi-Fi Protected Access using TKIP.", "5.3 Wireless Security"),
    ("WPA2", "Wi-Fi security using AES-CCMP.", "5.3 Wireless Security"),
    ("WPA3", "Latest Wi-Fi security standard with SAE.", "5.3 Wireless Security"),
    ("WPA2-Personal", "WPA2 with pre-shared key.", "5.3 Wireless Security"),
    ("WPA2-Enterprise", "WPA2 with 802.1X/RADIUS.", "5.3 Wireless Security"),
    ("PSK", "Pre-Shared Key authentication.", "5.3 Wireless Security"),
    ("EAP", "Extensible Authentication Protocol.", "5.3 Wireless Security"),
    ("Open authentication", "No encryption or authentication.", "5.3 Wireless Security"),
    ("Shared key authentication", "WEP-based shared key method.", "5.3 Wireless Security"),
    ("SAE", "Simultaneous Authentication of Equals used in WPA3.", "5.3 Wireless Security"),
    ("Forward secrecy", "Protecting past sessions even if keys are compromised.", "5.3 Wireless Security"),

    # 6.1 Automation
    ("Automation", "Using scripts/tools to manage network devices.", "6.1 Automation"),
    ("Orchestration", "Coordinating multiple automated tasks.", "6.1 Automation"),
    ("IaC", "Infrastructure as Code.", "6.1 Automation"),
    ("Ansible", "Agentless automation using YAML playbooks.", "6.1 Automation"),
    ("Puppet", "Declarative configuration management.", "6.1 Automation"),
    ("Chef", "Configuration management using cookbooks.", "6.1 Automation"),
    ("SaltStack", "Event-driven automation.", "6.1 Automation"),
    ("Terraform", "Declarative infrastructure provisioning.", "6.1 Automation"),
    ("SDN", "Software-Defined Networking with control/data plane separation.", "6.1 Automation"),
    ("Controller", "Centralized network management entity.", "6.1 Automation"),
    ("Underlay", "Physical network forwarding traffic.", "6.1 Automation"),
    ("Overlay", "Virtual network on top of the underlay.", "6.1 Automation"),
    ("Control plane", "Logic that decides how traffic is forwarded.", "6.1 Automation"),
    ("Data plane", "Hardware that actually forwards traffic.", "6.1 Automation"),
    ("Management plane", "Interfaces for device configuration and monitoring.", "6.1 Automation"),
    ("Day 0", "Initial device provisioning.", "6.1 Automation"),
    ("Day 1", "Initial configuration and deployment.", "6.1 Automation"),
    ("Day 2", "Ongoing operations and monitoring.", "6.1 Automation"),
    ("Configuration drift", "Unintended changes in device configurations.", "6.1 Automation"),
    ("Idempotency", "An operation that produces the same result when repeated.", "6.1 Automation"),

    # 6.2 APIs
    ("API", "Application Programming Interface.", "6.2 APIs"),
    ("REST", "Representational State Transfer using HTTP.", "6.2 APIs"),
    ("JSON", "JavaScript Object Notation data format.", "6.2 APIs"),
    ("XML", "Extensible Markup Language.", "6.2 APIs"),
    ("YAML", "Human-readable data serialization format.", "6.2 APIs"),
    ("HTTP GET", "Retrieves a resource.", "6.2 APIs"),
    ("HTTP POST", "Creates a resource.", "6.2 APIs"),
    ("HTTP PUT", "Updates/replaces a resource.", "6.2 APIs"),
    ("HTTP PATCH", "Partially updates a resource.", "6.2 APIs"),
    ("HTTP DELETE", "Removes a resource.", "6.2 APIs"),
    ("HTTP 200", "OK status code.", "6.2 APIs"),
    ("HTTP 201", "Created status code.", "6.2 APIs"),
    ("HTTP 204", "No Content status code.", "6.2 APIs"),
    ("HTTP 400", "Bad Request status code.", "6.2 APIs"),
    ("HTTP 401", "Unauthorized status code.", "6.2 APIs"),
    ("HTTP 403", "Forbidden status code.", "6.2 APIs"),
    ("HTTP 404", "Not Found status code.", "6.2 APIs"),
    ("HTTP 500", "Internal Server Error status code.", "6.2 APIs"),
    ("NETCONF", "Network configuration protocol using YANG/XML.", "6.2 APIs"),
    ("RESTCONF", "RESTful NETCONF over HTTP.", "6.2 APIs"),
    ("YANG", "Data modeling language for network config.", "6.2 APIs"),
    ("CRUD", "Create, Read, Update, Delete operations.", "6.2 APIs"),
    ("gRPC", "High-performance RPC framework.", "6.2 APIs"),
    ("WebSocket", "Persistent bidirectional communication over HTTP.", "6.2 APIs"),

    # 6.3 AI/ML
    ("Machine learning", "Algorithms learning patterns from data.", "6.3 AI/ML"),
    ("Supervised learning", "Training with labeled data.", "6.3 AI/ML"),
    ("Unsupervised learning", "Finding patterns without labeled data.", "6.3 AI/ML"),
    ("Reinforcement learning", "Learning through rewards/penalties.", "6.3 AI/ML"),
    ("Generative AI", "AI creating new content.", "6.3 AI/ML"),
    ("Telemetry", "Streaming operational data from devices.", "6.3 AI/ML"),
    ("Baseline", "Expected normal behavior for anomaly detection.", "6.3 AI/ML"),
    ("Anomaly detection", "Identifying deviations from normal behavior.", "6.3 AI/ML"),
    ("Predictive analytics", "Using data to forecast future events.", "6.3 AI/ML"),
    ("Chatbot", "An AI application that simulates conversation.", "6.3 AI/ML"),
]

# Commands: (command, description, section_key)
CCNA_COMMANDS = [
    ("show ip route", "displays the IPv4 routing table", "3.1 Routing Fundamentals"),
    ("show ipv6 route", "displays the IPv6 routing table", "3.1 Routing Fundamentals"),
    ("show ip ospf neighbor", "displays OSPF neighbor adjacencies", "3.2 OSPF"),
    ("show ip ospf database", "displays the OSPF link-state database", "3.2 OSPF"),
    ("show ip ospf interface", "displays OSPF interface status", "3.2 OSPF"),
    ("show ip eigrp neighbors", "displays EIGRP neighbors", "3.3 EIGRP"),
    ("show ip eigrp topology", "displays the EIGRP topology table", "3.3 EIGRP"),
    ("show ip eigrp interfaces", "displays EIGRP-enabled interfaces", "3.3 EIGRP"),
    ("show ip bgp summary", "displays BGP neighbor summary", "3.4 BGP"),
    ("show ip bgp", "displays the BGP table", "3.4 BGP"),
    ("show ip interface brief", "displays IP interface status summary", "1.1 Network Components"),
    ("show interfaces", "displays interface status and counters", "2.1 Switching Concepts"),
    ("show ip interface", "displays IP configuration of interfaces", "1.1 Network Components"),
    ("show vlan brief", "displays VLAN summary and port assignments", "2.2 VLANs"),
    ("show vlan", "displays VLAN details", "2.2 VLANs"),
    ("show spanning-tree", "displays spanning-tree topology", "2.4 STP"),
    ("show spanning-tree vlan", "displays per-VLAN spanning-tree", "2.4 STP"),
    ("show mac address-table", "displays the CAM table", "2.1 Switching Concepts"),
    ("show mac address-table dynamic", "displays dynamically learned MACs", "2.1 Switching Concepts"),
    ("show cdp neighbors", "displays CDP neighbor summary", "2.3 Inter-Switch Connectivity"),
    ("show cdp neighbors detail", "displays detailed CDP neighbor info", "2.3 Inter-Switch Connectivity"),
    ("show lldp neighbors", "displays LLDP neighbor summary", "2.3 Inter-Switch Connectivity"),
    ("show lldp neighbors detail", "displays detailed LLDP neighbor info", "2.3 Inter-Switch Connectivity"),
    ("show etherchannel summary", "displays EtherChannel status", "2.3 Inter-Switch Connectivity"),
    ("show ip nat translations", "displays active NAT translations", "4.1 NAT"),
    ("show ip nat statistics", "displays NAT statistics", "4.1 NAT"),
    ("show ip dhcp binding", "displays DHCP lease bindings", "4.2 NTP/DHCP/DNS"),
    ("show ip dhcp server statistics", "displays DHCP server statistics", "4.2 NTP/DHCP/DNS"),
    ("show ntp associations", "displays NTP peer associations", "4.2 NTP/DHCP/DNS"),
    ("show ntp status", "displays NTP synchronization status", "4.2 NTP/DHCP/DNS"),
    ("show snmp", "displays SNMP configuration", "4.3 SNMP/Syslog/SSH"),
    ("show snmp community", "displays configured SNMP communities", "4.3 SNMP/Syslog/SSH"),
    ("show logging", "displays syslog messages", "4.3 SNMP/Syslog/SSH"),
    ("show archive", "displays configuration archive", "6.1 Automation"),
    ("show ip access-lists", "displays configured access lists", "5.2 Access Control"),
    ("show access-lists", "displays all access lists", "5.2 Access Control"),
    ("show run", "displays the running configuration", "1.1 Network Components"),
    ("show startup-config", "displays the startup configuration", "1.1 Network Components"),
    ("show version", "displays IOS version, uptime, and hardware", "1.1 Network Components"),
    ("show clock", "displays system clock", "4.3 SNMP/Syslog/SSH"),
    ("show controllers", "displays physical layer interface info", "1.3 Physical Interfaces"),
    ("show processes cpu", "displays CPU utilization", "4.3 SNMP/Syslog/SSH"),
    ("show processes memory", "displays memory utilization", "4.3 SNMP/Syslog/SSH"),
    ("show policy-map interface", "displays QoS policy statistics", "4.4 QoS"),
    ("show class-map", "displays configured QoS class maps", "4.4 QoS"),
    ("show ip protocols", "displays configured routing protocols", "3.1 Routing Fundamentals"),
    ("debug ip ospf hello", "debugs OSPF hello packets", "3.2 OSPF"),
    ("debug ip rip", "debugs RIP updates", "3.1 Routing Fundamentals"),
    ("traceroute", "traces the path to a destination", "1.1 Network Components"),
    ("ping", "tests reachability to a destination", "1.1 Network Components"),
    ("telnet", "initiates an unencrypted remote session", "4.3 SNMP/Syslog/SSH"),
    ("ssh", "initiates an encrypted remote session", "4.3 SNMP/Syslog/SSH"),
]

# Comparisons: (concept_a, concept_b, differentiator, section_key)
CCNA_COMPARISONS = [
    ("TCP", "UDP", "TCP is connection-oriented and reliable; UDP is connectionless and best-effort.", "1.4 TCP/UDP"),
    ("Router", "Switch", "A router operates at Layer 3 using IP addresses; a switch operates at Layer 2 using MAC addresses.", "1.1 Network Components"),
    ("Hub", "Switch", "A hub repeats signals to all ports; a switch forwards frames only to the destination port.", "1.1 Network Components"),
    ("VLAN", "Subnet", "A VLAN is a Layer 2 broadcast domain; a subnet is a Layer 3 network range.", "2.2 VLANs"),
    ("Access port", "Trunk port", "An access port carries one VLAN; a trunk carries multiple VLANs with tags.", "2.2 VLANs"),
    ("STP", "RSTP", "STP converges slowly; RSTP converges rapidly using alternate/backup ports.", "2.4 STP"),
    ("OSPF", "EIGRP", "OSPF is standards-based link-state; EIGRP is Cisco-proprietary advanced distance-vector.", "3.2 OSPF"),
    ("Static route", "Dynamic route", "A static route is manually configured; a dynamic route is learned by a routing protocol.", "3.1 Routing Fundamentals"),
    ("Standard ACL", "Extended ACL", "Standard ACLs filter by source IP; extended ACLs filter by source/destination IP, port, and protocol.", "5.2 Access Control"),
    ("NAT", "PAT", "NAT translates addresses one-to-one or pool-based; PAT translates many private addresses to one public IP using ports.", "4.1 NAT"),
    ("RADIUS", "TACACS+", "RADIUS combines auth/authz and uses UDP; TACACS+ separates AAA and uses TCP.", "5.2 Access Control"),
    ("DHCP", "Static IP", "DHCP automatically assigns addressing; static IP is manually configured.", "4.2 NTP/DHCP/DNS"),
    ("IPv4", "IPv6", "IPv4 uses 32-bit addresses; IPv6 uses 128-bit addresses and has no broadcasts.", "1.5 IPv4/IPv6 Addressing"),
    ("Single-mode fiber", "Multimode fiber", "Single-mode supports long distances with laser; multimode supports shorter distances with LED.", "1.3 Physical Interfaces"),
    ("Hub-and-spoke", "Full-mesh", "Hub-and-spoke has a central site; full-mesh connects every site to every other site.", "1.2 Network Topology"),
    ("WPA2-Personal", "WPA2-Enterprise", "WPA2-Personal uses a pre-shared key; WPA2-Enterprise uses 802.1X/RADIUS per-user authentication.", "5.3 Wireless Security"),
    ("JSON", "XML", "JSON uses key-value pairs and arrays; XML uses nested tags.", "6.2 APIs"),
    ("Policing", "Shaping", "Policing drops or remarks excess traffic; shaping buffers excess traffic to smooth the rate.", "4.4 QoS"),
    ("Half duplex", "Full duplex", "Half duplex allows one direction at a time; full duplex allows simultaneous two-way communication.", "2.1 Switching Concepts"),
    ("eBGP", "iBGP", "eBGP runs between different autonomous systems; iBGP runs within the same AS.", "3.4 BGP"),
    ("IDS", "IPS", "IDS detects and alerts; IPS detects and actively blocks.", "1.1 Network Components"),
    ("STP blocking", "STP forwarding", "Blocking does not forward traffic; forwarding forwards traffic.", "2.4 STP"),
    ("SNMP trap", "SNMP inform", "A trap is unacknowledged; an inform requires acknowledgment.", "4.3 SNMP/Syslog/SSH"),
    ("2.4 GHz", "5 GHz", "2.4 GHz has longer range and more interference; 5 GHz has shorter range and more channels.", "2.5 Wireless"),
]

# Scenarios: (scenario, condition, result, section_key)
CCNA_SCENARIOS = [
    ("A switch receives a unicast frame with an unknown destination MAC.", "The destination MAC is not in the MAC address table.", "The switch floods the frame out all ports in the same VLAN except the ingress port.", "2.1 Switching Concepts"),
    ("Two switches are connected with an 802.1Q trunk.", "The native VLAN is mismatched between the two switches.", "Untagged traffic may leak between the two native VLANs.", "2.2 VLANs"),
    ("A switch port has port-security configured with maximum 2 MAC addresses.", "A third MAC address attempts to send traffic.", "The port triggers a security violation and may shut down or restrict.", "5.2 Access Control"),
    ("A router receives the same route from OSPF (AD 110) and EIGRP internal (AD 90).", "Both routes have the same prefix length.", "The EIGRP route is installed because it has the lower administrative distance.", "3.1 Routing Fundamentals"),
    ("A host sends a DHCP Discover message.", "The DHCP server is on a different subnet and no relay agent is configured.", "The host does not receive an IP address because broadcasts are not forwarded across subnets.", "4.2 NTP/DHCP/DNS"),
    ("An engineer configures a floating static route with AD 200.", "The same prefix is learned via OSPF with AD 110.", "The OSPF route is preferred; the static route appears only if OSPF route disappears.", "3.1 Routing Fundamentals"),
    ("A wireless client is associated to an AP on channel 1.", "A neighboring AP is also on channel 1 with overlapping coverage.", "Co-channel interference may degrade performance.", "2.5 Wireless"),
    ("A router interface is configured with ip nat inside but not ip nat outside.", "Traffic arrives from the inside interface destined to the Internet.", "NAT translation does not occur because the outside interface is not marked.", "4.1 NAT"),
    ("An attacker sends forged ARP replies mapping the default gateway IP to the attacker's MAC.", "Hosts update their ARP caches with the attacker's MAC.", "Traffic to the gateway is redirected through the attacker (ARP spoofing/MITM).", "5.1 Security Concepts"),
    ("A switch port is configured with BPDU Guard and PortFast.", "The port receives a BPDU from an accidentally connected switch.", "The port is placed into err-disabled state.", "2.4 STP"),
    ("A network uses WPA2-Enterprise with 802.1X.", "The RADIUS server becomes unreachable.", "New authentications fail; previously authenticated sessions may remain depending on configuration.", "5.3 Wireless Security"),
    ("An API client sends a POST request to a REST endpoint.", "The request body is valid JSON and the resource is created.", "The server returns HTTP 201 Created.", "6.2 APIs"),
    ("A user cannot reach a web server.", "A standard ACL is applied inbound on the router closest to the server and permits only the user's subnet.", "Traffic from the server back to the user is blocked because standard ACLs do not filter return traffic based on destination.", "5.2 Access Control"),
    ("An engineer configures two interfaces with the same IP address on a router.", "The network masks are different.", "The second interface may display an IP overlap error depending on IOS version.", "1.5 IPv4/IPv6 Addressing"),
    ("A router has OSPF enabled on an interface with no neighbors listed.", "The interface is administratively shut down.", "OSPF will not form adjacencies until the interface is no shutdown.", "3.2 OSPF"),
    ("A host is configured with IP 169.254.1.10/16.", "No DHCP server is reachable.", "The host uses APIPA and cannot communicate outside the local segment.", "4.2 NTP/DHCP/DNS"),
    ("A switch trunk is configured with allowed vlan 10,20.", "A frame tagged with VLAN 30 arrives on the trunk.", "The switch drops the frame because VLAN 30 is not allowed on the trunk.", "2.2 VLANs"),
    ("An EIGRP router loses its successor for a route but has a feasible successor.", "The feasible successor satisfies the feasibility condition.", "DUAL immediately promotes the feasible successor to successor without active querying.", "3.3 EIGRP"),
    ("A BGP router receives two paths for the same prefix.", "One path has a shorter AS_PATH.", "If all higher-priority attributes are equal, the path with the shorter AS_PATH is selected.", "3.4 BGP"),
    ("A network administrator applies an outbound ACL to deny Telnet.", "Users attempt to connect via Telnet to a server.", "Telnet sessions are blocked by the ACL.", "5.2 Access Control"),
    ("A switch has spanning-tree PortFast enabled on a trunk port.", "The trunk receives a BPDU.", "BPDU Guard may place the port into err-disabled state.", "2.4 STP"),
    ("A wireless network uses WPA3.", "A client supports only WPA2.", "The client may not be able to connect unless backward compatibility is enabled.", "5.3 Wireless Security"),
    ("A REST API client sends DELETE /api/devices/1.", "The device exists and the client is authorized.", "The server returns HTTP 204 No Content on success.", "6.2 APIs"),
    ("A router has ip helper-address configured on an interface.", "A host on that interface sends a DHCP Discover.", "The router forwards the Discover as a unicast to the DHCP server.", "4.2 NTP/DHCP/DNS"),
    ("A switch receives a broadcast frame on port Gi0/1.", "The switch has learned the source MAC on Gi0/1.", "The switch floods the frame out all ports in the same VLAN except Gi0/1.", "2.1 Switching Concepts"),
    ("A router interface is configured with 'ip nat inside' and 'ip nat outside'.", "A packet from the inside network has a source of 192.168.1.10 and destination 8.8.8.8.", "The router translates 192.168.1.10 to a public address before forwarding.", "4.1 NAT"),
    ("An OSPF router has two paths to 10.0.0.0/24.", "One path is intra-area with cost 20; the other is inter-area with cost 15.", "The router chooses the intra-area path because intra-area is preferred over inter-area regardless of cost.", "3.2 OSPF"),
    ("A network uses 802.1X port-based authentication.", "A non-802.1X device connects to a port in auto mode without a supplicant.", "The port remains in unauthorized state and blocks data traffic.", "5.2 Access Control"),
    ("A Cisco switch has DTP enabled on a port.", "The neighboring device is configured as 'switchport mode trunk'.", "The local port negotiates to trunking if in dynamic desirable or auto mode.", "2.2 VLANs"),
    ("An engineer runs 'show ip route' and sees two equal-cost paths to the same destination.", "The routing protocol supports equal-cost load balancing.", "The router uses both paths for traffic to that destination.", "3.1 Routing Fundamentals"),
    ("A switch port is configured with 'switchport port-security mac-address sticky'.", "A new host connects to the port.", "The switch dynamically learns and saves the MAC as a secure address.", "5.2 Access Control"),
    ("A BGP router receives a route with MED 50 from one peer and MED 100 from another.", "All higher-priority attributes are equal.", "The route with MED 50 is preferred because lower MED is preferred.", "3.4 BGP"),
    ("A wireless client roams from AP1 to AP2 in the same WLAN.", "The WLC manages both APs with fast roaming enabled.", "The client maintains connectivity with minimal interruption.", "2.5 Wireless"),
    ("An Ansible playbook is executed against a group of switches.", "The playbook uses the 'ios_config' module with a template.", "Ansible pushes the rendered configuration to each switch.", "6.1 Automation"),
    ("A router receives a packet destined to 224.0.0.5.", "The router is running OSPF on the ingress interface.", "The router processes the packet as an OSPF multicast.", "3.2 OSPF"),
    ("A switch has 'spanning-tree portfast default' enabled.", "A looped cable accidentally connects two access ports on the same switch.", "A temporary Layer 2 loop may form until STP converges; BPDU Guard can prevent it.", "2.4 STP"),
    ("A DNS client queries for www.example.com.", "The authoritative server responds with an A record.", "The client resolves the name to an IPv4 address.", "4.2 NTP/DHCP/DNS"),
    ("A network administrator enables 'ntp master 3' on a router.", "Other routers are configured with 'ntp server' pointing to it.", "The router acts as an NTP server with stratum 3.", "4.2 NTP/DHCP/DNS"),
    ("A Cisco router uses CBWFQ.", "One class exceeds its configured bandwidth.", "Excess traffic is queued and may be dropped if the queue overflows.", "4.4 QoS"),
    ("An attacker performs a MAC flooding attack.", "The switch MAC address table fills with bogus entries.", "The switch may flood traffic out all ports, enabling sniffing.", "5.1 Security Concepts"),
    ("A REST API client sends GET /api/devices.", "The server returns a list of devices in JSON.", "The response status code is 200 OK.", "6.2 APIs"),
    ("A host is configured with a /27 subnet mask on a /24 network.", "Other hosts use /24.", "The host may not communicate with hosts outside its /27 unless the router has correct routes.", "1.5 IPv4/IPv6 Addressing"),
    ("A switch port is set to 'switchport mode access' and assigned to VLAN 30.", "A frame without a VLAN tag arrives on the port.", "The switch associates the frame with VLAN 30.", "2.2 VLANs"),
    ("An OSPF DR fails on a broadcast segment.", "The BDR is functioning.", "The BDR takes over as the new DR and a new BDR is elected.", "3.2 OSPF"),
    ("A router has a static route pointing to a next-hop that is currently down.", "No other route to the destination exists.", "The static route disappears from the routing table.", "3.1 Routing Fundamentals"),
    ("An EIGRP router receives two paths to a destination with equal feasible distances.", "Both paths are feasible successors.", "The router performs equal-cost load balancing across both paths.", "3.3 EIGRP"),
    ("A switch receives a frame with a known destination MAC on a different port.", "The source MAC is already in the table.", "The switch forwards the frame only out the destination port.", "2.1 Switching Concepts"),
    ("A network administrator applies an extended ACL inbound on a router interface.", "The ACL permits HTTP but denies all other TCP traffic.", "HTTP sessions work, but other TCP applications are blocked.", "5.2 Access Control"),
    ("A wireless controller uses WPA2-Enterprise.", "A client fails 802.1X authentication.", "The client cannot associate and remains unauthenticated.", "5.3 Wireless Security"),
]

# Simlets: (cli_output, question, options, explanation, section_key)
CCNA_SIMLETS = [
    (
        """Router# show ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
Gateway of last resort is 10.1.1.1 to network 0.0.0.0

S*    0.0.0.0/0 [1/0] via 10.1.1.1
C      10.1.1.0/24 is directly connected, GigabitEthernet0/0
L      10.1.1.2/32 is directly connected, GigabitEthernet0/0
O      192.168.1.0/24 [110/2] via 10.1.1.1, 00:00:15, GigabitEthernet0/0""",
        "Which route will be used to reach 192.168.1.10?",
        [("The static default route", False), ("The directly connected route", False), ("The OSPF route 192.168.1.0/24", True), ("The local route 10.1.1.2/32", False)],
        "The destination 192.168.1.10 matches the OSPF route 192.168.1.0/24 with longest prefix match.",
        "3.1 Routing Fundamentals",
    ),
    (
        """Switch# show spanning-tree vlan 10

VLAN0010
  Spanning tree enabled protocol rstp
  Root ID    Priority    32778
             Address     0000.0c00.1111
             Cost        4
             Port        1 (GigabitEthernet0/0)
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    32778
             Address     0000.0c00.2222
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec""",
        "What is the role of this switch in VLAN 10 spanning tree?",
        [("Root bridge", False), ("Non-root bridge with root port Gi0/0", True), ("Designated bridge for all segments", False), ("Blocked bridge", False)],
        "The bridge has a root cost of 4 and root port Gi0/0, indicating it is not the root bridge.",
        "2.4 STP",
    ),
    (
        """Switch# show mac address-table
          Mac Address Table
-------------------------------------------
Vlan    Mac Address       Type        Ports
----    -----------       --------    -----
  10    0000.1111.2222    DYNAMIC     Gi0/1
  10    0000.3333.4444    DYNAMIC     Gi0/2
  20    0000.5555.6666    DYNAMIC     Gi0/3""",
        "On which port will the switch forward a frame destined to 0000.1111.2222 in VLAN 10?",
        [("Gi0/2", False), ("Gi0/1", True), ("Gi0/3", False), ("All ports in VLAN 10", False)],
        "The MAC table maps 0000.1111.2222 in VLAN 10 to port Gi0/1.",
        "2.1 Switching Concepts",
    ),
    (
        """Router# show ip ospf neighbor
Neighbor ID     Pri   State           Dead Time   Address         Interface
10.0.0.1          1   FULL/DR         00:00:35    10.1.1.1        GigabitEthernet0/0
10.0.0.2          1   FULL/BDR        00:00:38    10.1.1.2        GigabitEthernet0/0
10.0.0.3          1   2WAY/DROTHER    00:00:40    10.1.1.3        GigabitEthernet0/0""",
        "How many full adjacencies has this router formed on Gi0/0?",
        [("1", False), ("2", True), ("3", False), ("0", False)],
        "On a broadcast network, a router forms full adjacencies only with DR and BDR, not with DROTHERs.",
        "3.2 OSPF",
    ),
    (
        """Router# show ip bgp summary
BGP router identifier 192.168.1.1, local AS number 65001
Neighbor        V    AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
10.1.1.1        4 65002     120     125        5    0    0 01:23:45        150
10.1.1.5        4 65001     110     115        5    0    0 02:10:12        200""",
        "Which neighbor is an iBGP peer?",
        [("10.1.1.1 in AS 65002", False), ("10.1.1.5 in AS 65001", True), ("Both are iBGP peers", False), ("Neither is an iBGP peer", False)],
        "An iBGP peer has the same AS number as the local router. 10.1.1.5 is in AS 65001, matching the local AS.",
        "3.4 BGP",
    ),
    (
        """Router# show ip nat translations
Pro Inside global      Inside local       Outside local      Outside global
--- 203.0.113.10       192.168.1.10       ---                ---""",
        "What type of NAT translation is shown?",
        [("Dynamic NAT with overload", False), ("Static one-to-one NAT", True), ("PAT many-to-one", False), ("Destination NAT", False)],
        "A single inside global address is mapped to a single inside local address, indicating static NAT.",
        "4.1 NAT",
    ),
    (
        """Switch# show vlan brief
VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Gi0/0, Gi0/1
10   SALES                            active    Gi0/2, Gi0/3
20   ENGINEERING                      active    Gi0/4, Gi0/5
99   NATIVE_VLAN                      active""",
        "Which ports are members of VLAN 10?",
        [("Gi0/0 and Gi0/1", False), ("Gi0/2 and Gi0/3", True), ("Gi0/4 and Gi0/5", False), ("None; VLAN 10 is unused", False)],
        "The output shows VLAN 10 active on ports Gi0/2 and Gi0/3.",
        "2.2 VLANs",
    ),
    (
        """Router# show ip access-lists
Extended IP access list BLOCK_TELNET
    10 deny tcp any any eq 23
    20 permit ip any any""",
        "What traffic is blocked by this ACL?",
        [("All TCP traffic", False), ("Telnet traffic (TCP port 23)", True), ("SSH traffic (TCP port 22)", False), ("All IP traffic", False)],
        "Line 10 denies TCP traffic to port 23, which is Telnet.",
        "5.2 Access Control",
    ),
    (
        """Router# show ip dhcp binding
IP address      Client-ID/              Lease expiration        Type
                Hardware address
192.168.1.10    0000.1111.2222          Jun 17 2026 08:00 AM    Automatic
192.168.1.11    0000.3333.4444          Jun 17 2026 08:05 AM    Automatic
192.168.1.12    0000.5555.6666          Jun 17 2026 08:10 AM    Automatic""",
        "How many DHCP leases are currently active?",
        [("1", False), ("2", False), ("3", True), ("0", False)],
        "The output lists three active automatic leases.",
        "4.2 NTP/DHCP/DNS",
    ),
    (
        """Switch# show interfaces trunk
Port        Mode             Encapsulation  Status        Native vlan
Gi0/1       auto             802.1q         trunking      99
Gi0/2       auto             802.1q         trunking      1""",
        "What is the native VLAN on interface Gi0/1?",
        [("VLAN 1", False), ("VLAN 99", True), ("VLAN 100", False), ("Not configured", False)],
        "The Native vlan column for Gi0/1 shows 99.",
        "2.2 VLANs",
    ),
    (
        """Router# show ip ospf interface brief
Interface    PID   Area            IP Address/Mask    Cost  State Nbrs F/C
Gi0/0        1     0               10.1.1.1/24        1     DR    2/2
Gi0/1        1     0               10.1.2.1/24        1     BDR   1/1
Se0/0/0      1     0               10.1.3.1/30        64    P2P   0/0""",
        "Which interface is operating as the Designated Router?",
        [("Gi0/1", False), ("Gi0/0", True), ("Se0/0/0", False), ("None", False)],
        "The State column for Gi0/0 shows DR, Designated Router.",
        "3.2 OSPF",
    ),
    (
        """Switch# show spanning-tree vlan 20
VLAN0020
  Root ID    Priority    24596
             Address     0000.0c00.aaaa
             Cost        19
             Port        2 (Gi0/1)
             Hello Time   2 sec
  Bridge ID  Priority    32788
             Address     0000.0c00.bbbb""",
        "What can be concluded about this switch?",
        [("It is the root bridge", False), ("Gi0/1 is the root port", True), ("Gi0/1 is the designated port", False), ("VLAN 20 is not running STP", False)],
        "The switch has a root cost and a root port, so it is not the root bridge.",
        "2.4 STP",
    ),
    (
        """Router# show ip eigrp topology
EIGRP-IPv4 Topology Table for AS(100)/ID(192.168.1.1)
Codes: P - Passive, A - Active, U - Update, Q - Query, R - Reply
P 10.0.0.0/24, 1 successors, FD is 28160
        via 192.168.1.2 (28160/2816), Gi0/0""",
        "What is the feasible distance to 10.0.0.0/24?",
        [("2816", False), ("28160", True), ("192.168.1.2", False), ("Gi0/0", False)],
        "The FD is 28160; 2816 is the reported distance from the neighbor.",
        "3.3 EIGRP",
    ),
    (
        """Router# show ip interface brief
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     192.168.1.1     YES manual up                    up
GigabitEthernet0/1     unassigned      YES unset  administratively down down
Serial0/0/0            10.1.1.1        YES manual up                    up
Loopback0              1.1.1.1         YES manual up                    up""",
        "Which interface is administratively down?",
        [("GigabitEthernet0/0", False), ("GigabitEthernet0/1", True), ("Serial0/0/0", False), ("Loopback0", False)],
        "Gi0/1 status shows administratively down.",
        "1.1 Network Components",
    ),
    (
        """Router# show ip bgp
Network          Next Hop            Metric LocPrf Weight Path
*> 192.168.0.0     10.1.1.1               0             0 65002 i
*                   10.1.1.5               0             0 65003 i""",
        "Which path is selected for 192.168.0.0?",
        [("Path via 10.1.1.5 because it has lower metric", False), ("Path via 10.1.1.1 because it has the best weight", True), ("Both paths are used for load balancing", False), ("Neither; the route is not installed", False)],
        "Weight is the first attribute in BGP path selection; the path via 10.1.1.1 has weight 0 while the other also has 0, but the '>' indicates the selected path.",
        "3.4 BGP",
    ),
    (
        """Switch# show port-security interface gi0/1
Port Security              : Enabled
Port Status                : Secure-shutdown
Violation Mode             : Shutdown
Maximum MAC Addresses      : 2
Total MAC Addresses        : 3""",
        "Why is the port in secure-shutdown?",
        [("No MAC addresses were learned", False), ("The maximum number of secure MACs was exceeded", True), ("The port received a BPDU", False), ("DTP negotiation failed", False)],
        "Total MAC addresses (3) exceeds the maximum (2), triggering a violation and shutdown.",
        "5.2 Access Control",
    ),
    (
        """Router# show ip ospf database router
            OSPF Router with ID (1.1.1.1) (Process ID 1)
                Router Link States (Area 0)
  LS age: 120
  Options: (No TOS-capability, DC)
  LS Type: Router Links
  Link State ID: 1.1.1.1
  Advertising Router: 1.1.1.1""",
        "What type of LSA is shown?",
        [("Type 1 Router LSA", True), ("Type 2 Network LSA", False), ("Type 3 Summary LSA", False), ("Type 5 External LSA", False)],
        "LS Type 'Router Links' indicates a Type 1 Router LSA generated by every OSPF router.",
        "3.2 OSPF",
    ),
    (
        """Router# show access-lists
Standard IP access list 10
    10 permit 192.168.1.0, wildcard bits 0.0.0.255
    20 deny   any""",
        "Which statement describes ACL 10?",
        [("It is an extended ACL", False), ("It permits 192.168.1.0/24 and denies all other traffic", True), ("It denies 192.168.1.0/24", False), ("It is applied to an interface", False)],
        "Standard ACL 10 permits 192.168.1.0/24 and denies any other source.",
        "5.2 Access Control",
    ),
    (
        """Switch# show interfaces status
Port      Name               Status       Vlan       Duplex  Speed Type
Gi0/1                        connected    10         a-full  a-100 10/100/1000BaseTX
Gi0/2                        notconnect   1            auto   auto 10/100/1000BaseTX
Gi0/3                        connected    20         a-full  a-1000 10/100/1000BaseTX""",
        "Which port is operating at 1 Gbps?",
        [("Gi0/1", False), ("Gi0/2", False), ("Gi0/3", True), ("None", False)],
        "Gi0/3 shows speed a-1000 (1 Gbps).",
        "2.1 Switching Concepts",
    ),
    (
        """Router# show ip dhcp pool
Pool MYPOOL :
 Utilization mark (high/low)    : 100 / 0
 Subnet size (first/next)       : 0 / 0
 Total addresses                : 254
 Leased addresses               : 200
 Excluded addresses             : 2
 Pending event                  : none""",
        "How many addresses remain available in the pool?",
        [("254", False), ("200", False), ("52", True), ("256", False)],
        "254 total - 200 leased - 2 excluded = 52 available.",
        "4.2 NTP/DHCP/DNS",
    ),
    (
        """Router# show policy-map interface gi0/0
 Service-policy output: QOS_POLICY
   Class-map: VOICE (match-all)
     100 packets, 12000 bytes
     5 minute offered rate 0000 bps, drop rate 0000 bps
     Match: dscp ef (46)
     Queueing
       Strict Priority""",
        "Which QoS treatment is applied to voice traffic?",
        [("Best-effort queueing", False), ("Class-Based Weighted Fair Queuing", False), ("Low Latency Queueing (strict priority)", True), ("Traffic shaping", False)],
        "The output shows 'Strict Priority' for the VOICE class, indicating LLQ.",
        "4.4 QoS",
    ),
    (
        """Switch# show lldp neighbors
Capability codes: (R) Router, (B) Bridge, (T) Telephone, (C) DOCSIS Cable Device
Device ID        Local Intf     Hold-time  Capability      Port ID
Router1          Gi0/1          120        R               Gi0/0
Switch2          Gi0/2          120        B               Gi0/1""",
        "What type of device is connected to Gi0/1?",
        [("Bridge", False), ("Router", True), ("Telephone", False), ("Cable device", False)],
        "Capability 'R' indicates a Router connected to Gi0/1.",
        "2.3 Inter-Switch Connectivity",
    ),
]

# Drag-drop pools: (section_key, title, pairs)
CCNA_DRAG_DROP_POOLS = [
    (
        "1.4 TCP/UDP",
        "Match the protocol to its default transport-layer port.",
        [
            ("SSH", "TCP 22"),
            ("Telnet", "TCP 23"),
            ("FTP control", "TCP 21"),
            ("TFTP", "UDP 69"),
            ("DNS", "UDP/TCP 53"),
            ("DHCP server", "UDP 67"),
            ("SNMP", "UDP 161"),
            ("NTP", "UDP 123"),
        ],
    ),
    (
        "2.4 STP",
        "Match the STP port role to its function.",
        [
            ("Root port", "Best path to the root bridge"),
            ("Designated port", "Best port for a segment toward the root"),
            ("Alternate port", "Backup path to the root"),
            ("Backup port", "Backup for a designated port"),
        ],
    ),
    (
        "3.2 OSPF",
        "Match the OSPF neighbor state to its description.",
        [
            ("Init", "Hello received from neighbor"),
            ("2-Way", "Bidirectional communication established"),
            ("Exchange", "DBDs are being exchanged"),
            ("Loading", "LSRs/LSUs are exchanged"),
            ("Full", "Databases are synchronized"),
        ],
    ),
    (
        "3.4 BGP",
        "Order the BGP path-selection attributes from highest to lowest priority.",
        [
            ("1. Weight", "Locally significant Cisco attribute"),
            ("2. Local Preference", "Preferred exit point from AS"),
            ("3. Originated", "Routes originated locally"),
            ("4. AS Path", "Shortest path preferred"),
            ("5. MED", "Influences entry point"),
        ],
    ),
    (
        "4.2 NTP/DHCP/DNS",
        "Match the DNS record type to its purpose.",
        [
            ("A", "IPv4 address"),
            ("AAAA", "IPv6 address"),
            ("CNAME", "Canonical name alias"),
            ("MX", "Mail exchange"),
            ("NS", "Name server"),
            ("PTR", "Reverse lookup"),
        ],
    ),
    (
        "5.2 Access Control",
        "Match the Layer 2 security feature to its purpose.",
        [
            ("DHCP snooping", "Block rogue DHCP servers"),
            ("DAI", "Validate ARP packets"),
            ("IP Source Guard", "Filter based on DHCP bindings"),
            ("Port security", "Limit MAC addresses on a port"),
        ],
    ),
    (
        "6.2 APIs",
        "Match the HTTP method to its CRUD operation.",
        [
            ("POST", "Create"),
            ("GET", "Read"),
            ("PUT", "Update/Replace"),
            ("PATCH", "Partial Update"),
            ("DELETE", "Delete"),
        ],
    ),
    (
        "6.2 APIs",
        "Match the HTTP status code range to its meaning.",
        [
            ("2xx", "Success"),
            ("3xx", "Redirection"),
            ("4xx", "Client error"),
            ("5xx", "Server error"),
        ],
    ),
    (
        "1.3 Physical Interfaces",
        "Match the cable type to its typical characteristic.",
        [
            ("Cat 5e UTP", "1 Gbps up to 100 m"),
            ("Cat 6a UTP", "10 Gbps up to 100 m"),
            ("Single-mode fiber", "Long distance, laser"),
            ("Multimode fiber", "Short distance, LED"),
        ],
    ),
    (
        "4.4 QoS",
        "Match the QoS mechanism to its behavior.",
        [
            ("Policing", "Drop or remark excess traffic"),
            ("Shaping", "Buffer excess traffic"),
            ("Classification", "Identify traffic type"),
            ("Marking", "Set DSCP/CoS"),
        ],
    ),
    (
        "3.1 Routing Fundamentals",
        "Match the route source to its default administrative distance.",
        [
            ("Connected", "0"),
            ("Static", "1"),
            ("eBGP", "20"),
            ("EIGRP internal", "90"),
            ("OSPF", "110"),
            ("RIP", "120"),
        ],
    ),
    (
        "5.1 Security Concepts",
        "Match the attack type to its description.",
        [
            ("Phishing", "Fraudulent message to steal credentials"),
            ("DDoS", "Distributed Denial of Service"),
            ("Spoofing", "Falsifying source identity"),
            ("Man-in-the-middle", "Intercepting communications"),
            ("Ransomware", "Encrypting data for ransom"),
        ],
    ),
    (
        "1.5 IPv4/IPv6 Addressing",
        "Match the IPv6 address type to its prefix.",
        [
            ("Link-local", "fe80::/10"),
            ("Global unicast", "2000::/3"),
            ("Unique local", "fc00::/7"),
            ("Multicast", "ff00::/8"),
            ("Loopback", "::1"),
        ],
    ),
    (
        "2.2 VLANs",
        "Match the VLAN trunking concept to its meaning.",
        [
            ("Access port", "Single VLAN, no tag"),
            ("Trunk port", "Multiple VLANs, tagged"),
            ("Native VLAN", "Untagged traffic on trunk"),
            ("802.1Q", "VLAN tagging standard"),
        ],
    ),
]

# Fill-blank pools: (section_key, stem, correct, distractors)
CCNA_FILL_BLANK_POOLS = [
    ("2.2 VLANs", "To create VLAN 100 on a Cisco switch, use the command 'vlan __________' in global configuration mode.", "100", ["10", "20", "50", "99"]),
    ("2.2 VLANs", "On an 802.1Q trunk, untagged traffic belongs to the __________ VLAN.", "native", ["default", "management", "voice", "trunk"]),
    ("2.3 Inter-Switch Connectivity", "The IEEE standard for link aggregation is __________.", "LACP", ["PAgP", "DTP", "VTP", "STP"]),
    ("3.2 OSPF", "OSPF uses __________ as its metric, derived from interface bandwidth.", "cost", ["hop count", "delay", "bandwidth", "load"]),
    ("3.2 OSPF", "The OSPF backbone area number is __________.", "0", ["1", "10", "100", "255"]),
    ("3.3 EIGRP", "EIGRP uses the __________ algorithm to guarantee loop-free paths.", "DUAL", ["SPF", "Dijkstra", "Bellman-Ford", "LSA"]),
    ("4.1 NAT", "The NAT type that maps many internal addresses to one public IP using ports is called __________.", "PAT", ["static NAT", "dynamic NAT", "NAT overload", "destination NAT"]),
    ("4.2 NTP/DHCP/DNS", "NTP uses UDP port __________.", "123", ["53", "67", "161", "514"]),
    ("4.2 NTP/DHCP/DNS", "DHCP clients use UDP port __________ to send requests.", "68", ["67", "53", "69", "161"]),
    ("5.2 Access Control", "The command to apply an access list to a VTY line is 'access-class __________ in'.", "ACL_NUMBER", ["ip access-group", "line", "permit", "deny"]),
    ("6.2 APIs", "In REST APIs, the HTTP status code 201 means __________.", "Created", ["OK", "Accepted", "No Content", "Bad Request"]),
    ("1.4 TCP/UDP", "The TCP three-way handshake uses SYN, SYN-ACK, and __________.", "ACK", ["FIN", "RST", "PSH", "URG"]),
    ("2.4 STP", "The default STP bridge priority for VLAN 1 is __________.", "32769", ["32768", "4096", "0", "65535"]),
    ("3.1 Routing Fundamentals", "The default administrative distance of EIGRP internal routes is __________.", "90", ["110", "120", "100", "1"]),
    ("3.1 Routing Fundamentals", "The default administrative distance of OSPF is __________.", "110", ["90", "120", "100", "1"]),
    ("3.4 BGP", "The default administrative distance of eBGP is __________.", "20", ["200", "110", "90", "1"]),
    ("5.2 Access Control", "The IEEE standard for port-based network access control is __________.", "802.1X", ["802.1Q", "802.3ad", "802.11", "802.1AB"]),
    ("2.5 Wireless", "The 2.4 GHz band has __________ non-overlapping channels in North America.", "3", ["11", "6", "24", "12"]),
    ("1.5 IPv4/IPv6 Addressing", "The loopback IPv4 address is __________.", "127.0.0.1", ["0.0.0.0", "169.254.0.1", "192.168.0.1", "255.255.255.255"]),
    ("6.2 APIs", "RESTCONF uses __________ as its data modeling language.", "YANG", ["YAML", "XML", "JSON", "HTML"]),
]

# Multiple-choice pools: (section_key, question, correct_options, wrong_options, explanation)
CCNA_MULTIPLE_CHOICE_POOLS = [
    (
        "1.0 Network Fundamentals",
        "Which characteristics describe TCP? (Choose two.)",
        ["Connection-oriented", "Provides sequencing and acknowledgments"],
        ["Connectionless", "No retransmission", "Low overhead", "Unreliable delivery"],
        "TCP is connection-oriented, reliable, and uses sequencing and acknowledgments. UDP is connectionless and best-effort.",
    ),
    (
        "1.0 Network Fundamentals",
        "Which IPv4 addresses are defined as private by RFC 1918? (Choose three.)",
        ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"],
        ["100.64.0.0/10", "169.254.0.0/16", "224.0.0.0/4", "203.0.113.0/24"],
        "RFC 1918 private ranges are 10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16.",
    ),
    (
        "2.0 Network Access",
        "Which statements about VLAN trunks are true? (Choose two.)",
        ["A trunk can carry multiple VLANs", "802.1Q tags frames with VLAN information"],
        ["An access port carries all VLANs", "Trunks do not use VLAN tags", "Native VLAN traffic is always tagged", "VTP is required for trunks"],
        "Trunks carry multiple VLANs and use 802.1Q tagging. Access ports carry one VLAN. Native VLAN traffic is untagged by default.",
    ),
    (
        "2.0 Network Access",
        "Which STP features help protect against loops or rogue switches? (Choose three.)",
        ["BPDU Guard", "Root Guard", "Loop Guard"],
        ["PortFast", "EtherChannel", "DTP", "VTP"],
        "BPDU Guard, Root Guard, and Loop Guard are STP protection mechanisms. PortFast speeds up access port convergence but is not a protection feature by itself.",
    ),
    (
        "3.0 IP Connectivity",
        "Which factors are used by a router to select the best route? (Choose three.)",
        ["Longest prefix match", "Administrative distance", "Metric"],
        ["MAC address", "VLAN ID", "Hostname", "DNS name"],
        "Routers use longest prefix match, administrative distance, and metric to select the best route.",
    ),
    (
        "3.0 IP Connectivity",
        "Which conditions must match for OSPF neighbors to become fully adjacent on a broadcast network? (Choose two.)",
        ["Same area ID", "Same subnet and network mask"],
        ["Same router ID", "Same hostname", "Same process ID", "Same model of router"],
        "OSPF neighbors need matching area ID, subnet/mask, hello/dead timers, authentication, and network type. Router ID and process ID do not need to match.",
    ),
    (
        "4.0 IP Services",
        "Which protocols operate at the application layer? (Choose three.)",
        ["HTTP", "DNS", "SNMP"],
        ["TCP", "IP", "Ethernet", "ICMP"],
        "HTTP, DNS, and SNMP are application-layer protocols. TCP is transport, IP and ICMP are network, Ethernet is data link.",
    ),
    (
        "5.0 Security Fundamentals",
        "Which attacks target Layer 2 switches? (Choose three.)",
        ["MAC flooding", "ARP spoofing", "VLAN hopping"],
        ["DNS poisoning", "DDoS", "IP spoofing", "Phishing"],
        "MAC flooding, ARP spoofing, and VLAN hopping are Layer 2 attacks. DNS poisoning and phishing target higher layers or users.",
    ),
    (
        "6.0 Automation and Programmability",
        "Which are common data formats used in network automation? (Choose three.)",
        ["JSON", "YAML", "XML"],
        ["HTML", "JPEG", "CSV", "MPEG"],
        "JSON, YAML, and XML are common structured data formats in automation. HTML is for web pages, JPEG/MPEG are media formats.",
    ),
    (
        "1.0 Network Fundamentals",
        "Which layers of the OSI model operate at the network edge device? (Choose two.)",
        ["Layer 2", "Layer 3"],
        ["Layer 1 only", "Layer 4", "Layer 7 only", "Layer 5"],
        "A router/switch operates at Layer 2 and Layer 3.",
    ),
    (
        "2.0 Network Access",
        "Which statements about EtherChannel are true? (Choose two.)",
        ["It bundles multiple links into one logical link", "LACP is an IEEE standard"],
        ["It requires all links to be different speeds", "It increases the collision domain", "STP blocks all bundled links", "PAgP is an IEEE standard"],
        "EtherChannel bundles links and LACP is IEEE 802.3ad. Links should match speed/duplex, and STP sees the bundle as one link.",
    ),
    (
        "3.0 IP Connectivity",
        "Which BGP attributes are well-known mandatory? (Choose two.)",
        ["AS_PATH", "NEXT_HOP"],
        ["LOCAL_PREF", "MED", "Weight", "Community"],
        "AS_PATH and NEXT_HOP are well-known mandatory. LOCAL_PREF is well-known discretionary; MED and Community are optional transitive/non-transitive.",
    ),
    (
        "4.0 IP Services",
        "Which statements about DHCP are true? (Choose two.)",
        ["DHCP Discover is broadcast", "DHCP uses UDP"],
        ["DHCP uses TCP", "DHCP Offer is unicast always", "DHCP is a routing protocol", "DHCP assigns MAC addresses"],
        "DHCP uses UDP and Discover is broadcast. Offer can be unicast or broadcast depending on client capabilities.",
    ),
    (
        "5.0 Security Fundamentals",
        "Which are best practices for securing management access? (Choose two.)",
        ["Use SSH instead of Telnet", "Apply strong passwords"],
        ["Use SNMPv1 with default community", "Share enable passwords", "Disable logging", "Use HTTP for management"],
        "SSH and strong passwords improve management security. SNMPv1 default communities and HTTP are insecure.",
    ),
    (
        "6.0 Automation and Programmability",
        "Which are benefits of Infrastructure as Code? (Choose two.)",
        ["Repeatable deployments", "Version control of configurations"],
        ["Manual CLI changes per device", "No documentation needed", "Harder auditing", "Slower provisioning"],
        "IaC enables repeatable, version-controlled deployments that are easier to audit.",
    ),
    (
        "3.0 IP Connectivity",
        "Which statements about OSPF areas are true? (Choose two.)",
        ["Area 0 is the backbone", "ABRs connect Area 0 to other areas"],
        ["All areas can be stub areas", "ASBRs connect only non-backbone areas", "DRs are elected in point-to-point networks", "Virtual links are preferred over physical links"],
        "Area 0 is the backbone and ABRs connect it to other areas. ASBRs redistribute external routes. DRs are elected on multi-access networks.",
    ),
    (
        "3.0 IP Connectivity",
        "Which factors influence EIGRP metric calculation? (Choose two.)",
        ["Bandwidth", "Delay"],
        ["Hop count", "Area ID", "AS number", "Hello timer"],
        "EIGRP composite metric uses bandwidth and delay by default. Load and reliability can be configured but are not used by default.",
    ),
    (
        "3.0 IP Connectivity",
        "Which BGP path attributes are well-known? (Choose two.)",
        ["AS_PATH", "NEXT_HOP"],
        ["Weight", "MED", "Local Preference is well-known but listed as distractor", "Community"],
        "AS_PATH and NEXT_HOP are well-known mandatory. LOCAL_PREF is well-known discretionary. Weight is Cisco-proprietary.",
    ),
    (
        "2.0 Network Access",
        "Which are valid STP port states? (Choose two.)",
        ["Blocking", "Forwarding"],
        ["Learning", "Disabled", "Flooding", "Filtering"],
        "STP port states include blocking, listening, learning, forwarding, and disabled. Flooding and filtering are switch behaviors, not STP states.",
    ),
    (
        "2.0 Network Access",
        "Which statements about VLANs are true? (Choose two.)",
        ["A VLAN is a logical broadcast domain", "Trunks carry multiple VLANs"],
        ["VLANs require routers to communicate within the same VLAN", "Access ports carry all VLANs", "VLAN IDs range from 0 to 4095", "Native VLAN must be tagged"],
        "VLANs create logical broadcast domains and trunks carry multiple VLANs. Access ports carry one VLAN and native VLAN is untagged by default.",
    ),
    (
        "4.0 IP Services",
        "Which statements describe SNMPv3? (Choose two.)",
        ["Provides authentication", "Provides encryption"],
        ["Uses community strings", "Is less secure than SNMPv2c", "Requires NTP for all operations", "Only supports traps"],
        "SNMPv3 supports authentication, integrity, and encryption. SNMPv1/v2c use community strings.",
    ),
    (
        "4.0 IP Services",
        "Which are valid DHCP messages? (Choose two.)",
        ["Discover", "Offer"],
        ["Request", "Ack", "Hello", "Update"],
        "DHCP DORA process uses Discover, Offer, Request, and Ack. Hello and Update are not DHCP messages.",
    ),
    (
        "5.0 Security Fundamentals",
        "Which are functions of a firewall? (Choose two.)",
        ["Filter traffic based on rules", "Perform NAT"],
        ["Forward frames based on MAC", "Act as a DHCP server by default", "Provide wireless access", "Create VLANs"],
        "Firewalls filter traffic and often perform NAT. MAC forwarding is a switch function.",
    ),
    (
        "5.0 Security Fundamentals",
        "Which are examples of social engineering? (Choose two.)",
        ["Phishing", "Pretexting"],
        ["DDoS", "MAC flooding", "ARP spoofing", "IPsec"],
        "Phishing and pretexting are social engineering attacks. DDoS, MAC flooding, and ARP spoofing are technical attacks.",
    ),
    (
        "6.0 Automation and Programmability",
        "Which are components of SDN? (Choose two.)",
        ["Application plane", "Control plane"],
        ["Collision domain", "Broadcast domain", "MAC table", "VLAN tag"],
        "SDN separates application, control, and data planes. Collision/broadcast domains are Layer 2 concepts.",
    ),
    (
        "6.0 Automation and Programmability",
        "Which data formats are commonly used with REST APIs? (Choose two.)",
        ["JSON", "XML"],
        ["JPEG", "HTML", "MPEG", "YAML is also used but listed as distractor"],
        "REST APIs commonly use JSON and XML. YAML is used in config but less common for REST payloads.",
    ),
    (
        "2.0 Network Access",
        "Which statements about VLAN trunking are true? (Choose three.)",
        ["A trunk can carry multiple VLANs", "802.1Q adds a VLAN tag", "Native VLAN traffic is untagged by default"],
        ["Access ports carry multiple VLANs", "Trunks cannot carry VLAN 1", "DTP is required for trunks", "VTP creates VLANs automatically"],
        "Trunks carry multiple VLANs with 802.1Q tags. Access ports carry one VLAN. Native VLAN is untagged. VTP does not create VLANs automatically.",
    ),
    (
        "2.0 Network Access",
        "Which statements about RSTP are true? (Choose two.)",
        ["RSTP converges faster than STP", "RSTP uses alternate and backup port roles"],
        ["RSTP has the same port states as STP", "RSTP is proprietary to Cisco", "RSTP does not use BPDUs", "RSTP has a 50-second default convergence"],
        "RSTP converges faster using alternate/backup ports and has different port states than legacy STP.",
    ),
    (
        "3.0 IP Connectivity",
        "Which statements about OSPF neighbor adjacency are true? (Choose two.)",
        ["Matching area ID is required", "Matching hello and dead timers are required"],
        ["Same router ID is required", "Same hostname is required", "Same process ID is required", "Same model is required"],
        "OSPF neighbors need matching area ID, subnet/mask, hello/dead timers, authentication, and network type.",
    ),
    (
        "3.0 IP Connectivity",
        "Which statements about BGP route selection are true? (Choose two.)",
        ["Higher Weight is preferred", "Higher LOCAL_PREF is preferred"],
        ["Longer AS_PATH is preferred", "Higher MED is preferred", "eBGP routes are always preferred over iBGP", "Origin IGP is least preferred"],
        "Weight and LOCAL_PREF are higher-priority attributes. Shorter AS_PATH and lower MED are preferred. eBGP over iBGP is only after weight/LP.",
    ),
    (
        "4.0 IP Services",
        "Which protocols may use both TCP and UDP? (Choose two.)",
        ["DNS", "Syslog"],
        ["HTTP", "TFTP", "SNMP", "NTP"],
        "DNS uses TCP for zone transfers and UDP for queries. Syslog uses UDP by default but can use TCP. HTTP uses TCP, TFTP/SNMP/NTP use UDP.",
    ),
    (
        "5.0 Security Fundamentals",
        "Which are Layer 2 security best practices? (Choose two.)",
        ["Enable DHCP snooping", "Enable DAI"],
        ["Disable port security", "Use Telnet for management", "Disable spanning tree", "Use WEP for wireless"],
        "DHCP snooping and DAI protect against rogue DHCP and ARP spoofing. Port security should be enabled, Telnet and WEP are insecure.",
    ),
]
