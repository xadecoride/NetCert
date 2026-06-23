"""Content pools for CCNA 2.0 question generation.

Blueprint based on the updated CCNA 2.0 exam structure:
1. Network Fundamentals
2. Network Access
3. IP Connectivity
4. IP Services
5. Security & Automation Fundamentals
"""

CCNA_SECTIONS = {
    "1.1 Cable/interface diagnostics": ("1.0 Network Fundamentals", 14.29),
    "1.2 Virtualization": ("1.0 Network Fundamentals", 14.29),
    "1.3 IPv4 troubleshooting": ("1.0 Network Fundamentals", 14.29),
    "1.4 IPv6 troubleshooting": ("1.0 Network Fundamentals", 14.29),
    "1.5 Wireless principles": ("1.0 Network Fundamentals", 14.29),
    "1.6 Client connectivity": ("1.0 Network Fundamentals", 14.29),
    "1.7 DHCPv4": ("1.0 Network Fundamentals", 14.29),
    "2.1 Infrastructure connectivity": ("2.0 Network Access", 20.0),
    "2.2 Edge-host connectivity": ("2.0 Network Access", 20.0),
    "2.3 CDP/LLDP": ("2.0 Network Access", 20.0),
    "2.4 L2/L3 troubleshooting": ("2.0 Network Access", 20.0),
    "2.5 Rapid PVST+": ("2.0 Network Access", 20.0),
    "3.1 Routing table": ("3.0 IP Connectivity", 25.0),
    "3.2 Static routing": ("3.0 IP Connectivity", 25.0),
    "3.3 OSPF": ("3.0 IP Connectivity", 25.0),
    "3.4 FHRP": ("3.0 IP Connectivity", 25.0),
    "4.1 AAA": ("4.0 IP Services", 14.29),
    "4.2 SFTP/SCP": ("4.0 IP Services", 14.29),
    "4.3 NAT/PAT": ("4.0 IP Services", 14.29),
    "4.4 DNS records": ("4.0 IP Services", 14.29),
    "4.5 IPsec VPNs": ("4.0 IP Services", 14.29),
    "4.6 ACLs": ("4.0 IP Services", 14.29),
    "4.7 Layer 2 security": ("4.0 IP Services", 14.29),
    "5.1 Agentic AI": ("5.0 Security & Automation Fundamentals", 16.67),
    "5.2 Prompt engineering": ("5.0 Security & Automation Fundamentals", 16.67),
    "5.3 Management approaches": ("5.0 Security & Automation Fundamentals", 16.67),
    "5.4 SNMP": ("5.0 Security & Automation Fundamentals", 16.67),
    "5.5 Ansible": ("5.0 Security & Automation Fundamentals", 16.67),
    "5.6 Syslog": ("5.0 Security & Automation Fundamentals", 16.67),
}

CCNA_CATEGORIES = {
    "1.1 Cable/interface diagnostics": "cable and interface diagnostics concepts",
    "1.2 Virtualization": "virtualization concepts",
    "1.3 IPv4 troubleshooting": "IPv4 addressing and subnetting troubleshooting",
    "1.4 IPv6 troubleshooting": "IPv6 addressing and prefix sizing",
    "1.5 Wireless principles": "wireless networking principles",
    "1.6 Client connectivity": "wired and wireless client connectivity",
    "1.7 DHCPv4": "DHCPv4 client, server, and relay troubleshooting",
    "2.1 Infrastructure connectivity": "infrastructure connectivity configuration",
    "2.2 Edge-host connectivity": "edge-host Layer 2 port configuration",
    "2.3 CDP/LLDP": "CDP and LLDP documentation validation",
    "2.4 L2/L3 troubleshooting": "Layer 2 and Layer 3 troubleshooting",
    "2.5 Rapid PVST+": "Rapid PVST+ configuration",
    "3.1 Routing table": "routing table interpretation",
    "3.2 Static routing": "IPv4 and IPv6 static routing troubleshooting",
    "3.3 OSPF": "single-area OSPFv2/OSPFv3 configuration",
    "3.4 FHRP": "HSRP and VRRP operational status",
    "4.1 AAA": "AAA and local username configuration",
    "4.2 SFTP/SCP": "secure file transfer operations",
    "4.3 NAT/PAT": "NAT/PAT configuration",
    "4.4 DNS records": "DNS record diagnosis",
    "4.5 IPsec VPNs": "IPsec remote access and site-to-site VPNs",
    "4.6 ACLs": "IPv4 access control list configuration",
    "4.7 Layer 2 security": "Layer 2 security feature configuration",
    "5.1 Agentic AI": "agentic AI in network operations",
    "5.2 Prompt engineering": "generative AI prompt engineering",
    "5.3 Management approaches": "network management approaches",
    "5.4 SNMP": "SNMP in network operations",
    "5.5 Ansible": "Ansible configuration management",
    "5.6 Syslog": "syslog message interpretation",
}

CCNA_TERMS = [
    # 1.1 Cable/interface diagnostics
    ("Duplex mismatch", "A condition where connected interfaces use different duplex modes, causing collisions or errors.", "1.1 Cable/interface diagnostics"),
    ("CSMA/CD", "Carrier Sense Multiple Access with Collision Detection, used by half-duplex Ethernet.", "1.1 Cable/interface diagnostics"),
    ("CRC errors", "Cyclic redundancy check errors indicating frame corruption on the wire.", "1.1 Cable/interface diagnostics"),
    ("Runts", "Frames smaller than the minimum Ethernet frame size.", "1.1 Cable/interface diagnostics"),
    ("Giants", "Frames larger than the maximum Ethernet frame size.", "1.1 Cable/interface diagnostics"),
    ("Collisions", "Frames transmitted simultaneously on a shared half-duplex segment.", "1.1 Cable/interface diagnostics"),
    ("Late collisions", "Collisions occurring after the first 64 bytes, usually indicating duplex mismatch.", "1.1 Cable/interface diagnostics"),
    ("Signal attenuation", "Weakening of a signal over distance, especially in fiber or copper.", "1.1 Cable/interface diagnostics"),
    ("PoE", "Power over Ethernet, delivering power to endpoints over data cables.", "1.1 Cable/interface diagnostics"),
    ("Pinout", "The arrangement of wires in a cable connector.", "1.1 Cable/interface diagnostics"),
    ("Single-mode fiber", "Fiber optic cable using a single light path for long distances.", "1.1 Cable/interface diagnostics"),
    ("Multimode fiber", "Fiber optic cable using multiple light paths for shorter distances.", "1.1 Cable/interface diagnostics"),
    ("UTP", "Unshielded twisted-pair copper cable.", "1.1 Cable/interface diagnostics"),
    ("STP cable", "Shielded twisted-pair copper cable.", "1.1 Cable/interface diagnostics"),
    ("Straight-through cable", "A cable with identical pinouts on both ends, used for different device types.", "1.1 Cable/interface diagnostics"),
    ("Crossover cable", "A cable with reversed transmit/receive pairs, used for same device types.", "1.1 Cable/interface diagnostics"),
    ("Rollover cable", "A console cable with reversed pinout used for device management.", "1.1 Cable/interface diagnostics"),
    ("Optical power budget", "The maximum allowable signal loss in a fiber link.", "1.1 Cable/interface diagnostics"),
    # 1.2 Virtualization
    ("Hypervisor", "Software that creates and runs virtual machines.", "1.2 Virtualization"),
    ("Virtual machine", "An emulated computer system running on a host.", "1.2 Virtualization"),
    ("Container", "A lightweight isolated runtime environment sharing the host OS kernel.", "1.2 Virtualization"),
    ("Type 1 hypervisor", "A hypervisor that runs directly on hardware, also called bare-metal.", "1.2 Virtualization"),
    ("Type 2 hypervisor", "A hypervisor that runs on top of a host operating system.", "1.2 Virtualization"),
    ("vSwitch", "A virtual switch connecting virtual machines within a host.", "1.2 Virtualization"),
    ("vNIC", "A virtual network interface card presented to a VM or container.", "1.2 Virtualization"),
    ("Docker", "A platform for developing and running containerized applications.", "1.2 Virtualization"),
    ("Kubernetes", "An orchestration platform for containerized workloads.", "1.2 Virtualization"),
    # 1.3 IPv4 troubleshooting
    ("Subnet mask", "A 32-bit value that separates the network and host portions of an IPv4 address.", "1.3 IPv4 troubleshooting"),
    ("CIDR", "Classless Inter-Domain Routing notation for prefixes.", "1.3 IPv4 troubleshooting"),
    ("Default gateway", "The router used to reach destinations outside the local subnet.", "1.3 IPv4 troubleshooting"),
    ("Broadcast address", "The address used to send traffic to all hosts on a subnet.", "1.3 IPv4 troubleshooting"),
    ("Network address", "The address identifying the subnet itself.", "1.3 IPv4 troubleshooting"),
    ("Usable host range", "The range of assignable addresses in a subnet.", "1.3 IPv4 troubleshooting"),
    ("Private IPv4 address", "An address not routable on the public Internet.", "1.3 IPv4 troubleshooting"),
    ("Public IPv4 address", "A globally routable Internet address.", "1.3 IPv4 troubleshooting"),
    ("APIPA", "Automatic Private IP Addressing range 169.254.0.0/16.", "1.3 IPv4 troubleshooting"),
    ("Loopback address", "The 127.0.0.0/8 range used for local testing.", "1.3 IPv4 troubleshooting"),
    ("VLSM", "Variable Length Subnet Masking for efficient address allocation.", "1.3 IPv4 troubleshooting"),
    # 1.4 IPv6 troubleshooting
    ("IPv6 global unicast", "A globally routable IPv6 address.", "1.4 IPv6 troubleshooting"),
    ("IPv6 link-local", "An address used only on the local link, starting with FE80::/10.", "1.4 IPv6 troubleshooting"),
    ("IPv6 unique local", "A private IPv6 address range, FC00::/7.", "1.4 IPv6 troubleshooting"),
    ("Modified EUI-64", "A method to generate the interface identifier portion of an IPv6 address.", "1.4 IPv6 troubleshooting"),
    ("IPv6 prefix", "The network portion of an IPv6 address.", "1.4 IPv6 troubleshooting"),
    ("IPv6 prefix length", "The number of bits representing the network portion.", "1.4 IPv6 troubleshooting"),
    ("SLAAC", "Stateless Address Autoconfiguration for IPv6.", "1.4 IPv6 troubleshooting"),
    ("DHCPv6", "Stateful IPv6 address assignment.", "1.4 IPv6 troubleshooting"),
    ("IPv6 loopback", "The ::1 address.", "1.4 IPv6 troubleshooting"),
    ("Dual stack", "Running IPv4 and IPv6 simultaneously on a network.", "1.4 IPv6 troubleshooting"),
    # 1.5 Wireless principles
    ("SSID", "Service Set Identifier, the name of a wireless network.", "1.5 Wireless principles"),
    ("BSSID", "Basic Service Set Identifier, the MAC address of an access point.", "1.5 Wireless principles"),
    ("Channel", "A specific frequency range used by a wireless radio.", "1.5 Wireless principles"),
    ("Band", "A frequency range such as 2.4 GHz or 5 GHz.", "1.5 Wireless principles"),
    ("RSSI", "Received Signal Strength Indicator.", "1.5 Wireless principles"),
    ("SNR", "Signal-to-Noise Ratio.", "1.5 Wireless principles"),
    ("Attenuation", "Reduction in signal strength.", "1.5 Wireless principles"),
    ("Absorption", "Signal loss as RF passes through materials.", "1.5 Wireless principles"),
    ("Reflection", "RF bouncing off surfaces.", "1.5 Wireless principles"),
    ("Refraction", "RF bending when passing between mediums.", "1.5 Wireless principles"),
    ("Diffraction", "RF bending around obstacles.", "1.5 Wireless principles"),
    ("Scattering", "RF dispersing in multiple directions.", "1.5 Wireless principles"),
    ("WPA3", "Wi-Fi Protected Access 3 security protocol.", "1.5 Wireless principles"),
    ("WPA2", "Wi-Fi Protected Access 2 security protocol.", "1.5 Wireless principles"),
    ("Open authentication", "Wireless authentication without encryption.", "1.5 Wireless principles"),
    ("Co-channel interference", "Interference from APs on the same channel.", "1.5 Wireless principles"),
    ("Adjacent-channel interference", "Interference from overlapping channels.", "1.5 Wireless principles"),
    # 1.6 Client connectivity
    ("ipconfig", "Windows command to display IP configuration.", "1.6 Client connectivity"),
    ("ifconfig", "Legacy Unix command to display interface configuration.", "1.6 Client connectivity"),
    ("ip", "Linux command for network configuration.", "1.6 Client connectivity"),
    ("ping", "Tool to test reachability using ICMP echo.", "1.6 Client connectivity"),
    ("traceroute", "Tool to trace the path to a destination.", "1.6 Client connectivity"),
    ("tracert", "Windows traceroute command.", "1.6 Client connectivity"),
    ("nslookup", "Tool to query DNS.", "1.6 Client connectivity"),
    ("dig", "Advanced DNS lookup tool.", "1.6 Client connectivity"),
    ("netsh", "Windows network shell utility.", "1.6 Client connectivity"),
    ("Wireless profile", "Saved wireless network configuration on a client.", "1.6 Client connectivity"),
    # 1.7 DHCPv4
    ("DHCP discover", "The first DHCP message sent by a client seeking an address.", "1.7 DHCPv4"),
    ("DHCP offer", "A DHCP server response with a proposed lease.", "1.7 DHCPv4"),
    ("DHCP request", "A client message accepting a DHCP offer.", "1.7 DHCPv4"),
    ("DHCP ack", "The final DHCP message confirming the lease.", "1.7 DHCPv4"),
    ("DHCP relay", "A router/agent that forwards DHCP messages between subnets.", "1.7 DHCPv4"),
    ("ip helper-address", "Cisco command to forward DHCP broadcasts to a remote server.", "1.7 DHCPv4"),
    ("DHCP lease", "The time a client may use an assigned address.", "1.7 DHCPv4"),
    ("DHCP reservation", "A fixed address assignment based on MAC address.", "1.7 DHCPv4"),
    ("DHCP exclusion", "Addresses excluded from automatic assignment.", "1.7 DHCPv4"),
    # 2.1 Infrastructure connectivity
    ("Trunk", "A switch port carrying multiple VLANs.", "2.1 Infrastructure connectivity"),
    ("Access port", "A switch port assigned to a single VLAN.", "2.1 Infrastructure connectivity"),
    ("802.1Q", "The VLAN tagging standard.", "2.1 Infrastructure connectivity"),
    ("Native VLAN", "The VLAN on a trunk that carries untagged traffic.", "2.1 Infrastructure connectivity"),
    ("Allowed VLAN list", "The VLANs permitted on a trunk.", "2.1 Infrastructure connectivity"),
    ("LACP", "Link Aggregation Control Protocol for EtherChannel.", "2.1 Infrastructure connectivity"),
    ("PAgP", "Port Aggregation Protocol, Cisco proprietary EtherChannel protocol.", "2.1 Infrastructure connectivity"),
    ("EtherChannel", "Bundling multiple physical links into one logical link.", "2.1 Infrastructure connectivity"),
    ("SVI", "Switched Virtual Interface for Layer 3 routing on a switch.", "2.1 Infrastructure connectivity"),
    ("Routed port", "A switch port operating as a Layer 3 interface.", "2.1 Infrastructure connectivity"),
    # 2.2 Edge-host connectivity
    ("VLAN", "A logical Layer 2 broadcast domain.", "2.2 Edge-host connectivity"),
    ("Voice VLAN", "A VLAN dedicated to VoIP traffic.", "2.2 Edge-host connectivity"),
    ("Data VLAN", "A VLAN for user data traffic.", "2.2 Edge-host connectivity"),
    ("Port security", "A feature restricting MAC addresses on a port.", "2.2 Edge-host connectivity"),
    ("Sticky MAC", "A port security feature learning and saving MAC addresses.", "2.2 Edge-host connectivity"),
    ("PoE budget", "The total power available for PoE devices on a switch.", "2.2 Edge-host connectivity"),
    ("DTP", "Dynamic Trunking Protocol for Cisco switches.", "2.2 Edge-host connectivity"),
    # 2.3 CDP/LLDP
    ("CDP", "Cisco Discovery Protocol for neighbor discovery.", "2.3 CDP/LLDP"),
    ("LLDP", "Link Layer Discovery Protocol, vendor-neutral neighbor discovery.", "2.3 CDP/LLDP"),
    ("LLDP-MED", "LLDP extension for voice and video endpoints.", "2.3 CDP/LLDP"),
    ("Holdtime", "How long a CDP/LLDP neighbor entry is kept.", "2.3 CDP/LLDP"),
    ("Timer", "How often CDP/LLDP advertisements are sent.", "2.3 CDP/LLDP"),
    # 2.4 L2/L3 troubleshooting
    ("show interfaces", "Command displaying interface status and counters.", "2.4 L2/L3 troubleshooting"),
    ("show ip interface brief", "Command showing Layer 1/2/3 status of interfaces.", "2.4 L2/L3 troubleshooting"),
    ("show vlan", "Command displaying VLAN configuration.", "2.4 L2/L3 troubleshooting"),
    ("show mac address-table", "Command showing learned MAC addresses.", "2.4 L2/L3 troubleshooting"),
    ("show logging", "Command displaying system log messages.", "2.4 L2/L3 troubleshooting"),
    ("Extended ping", "A ping command with configurable source, size, and count.", "2.4 L2/L3 troubleshooting"),
    ("Packet capture", "Recording packets for analysis.", "2.4 L2/L3 troubleshooting"),
    # 2.5 Rapid PVST+
    ("Rapid PVST+", "Cisco per-VLAN rapid spanning tree implementation.", "2.5 Rapid PVST+"),
    ("Root bridge", "The spanning tree reference switch for a VLAN.", "2.5 Rapid PVST+"),
    ("Root port", "The port with the lowest cost path to the root bridge.", "2.5 Rapid PVST+"),
    ("Designated port", "The port forwarding traffic for a segment toward the root.", "2.5 Rapid PVST+"),
    ("Alternate port", "A blocked port providing an alternate path to the root.", "2.5 Rapid PVST+"),
    ("Backup port", "A blocked port providing a backup path on the same segment.", "2.5 Rapid PVST+"),
    ("PortFast", "A feature allowing access ports to transition immediately to forwarding.", "2.5 Rapid PVST+"),
    ("BPDU Guard", "A feature disabling a PortFast port receiving BPDUs.", "2.5 Rapid PVST+"),
    ("Root Guard", "A feature preventing an unauthorized switch from becoming root.", "2.5 Rapid PVST+"),
    ("Loop Guard", "A feature preventing alternate/root ports from becoming designated due to unidirectional links.", "2.5 Rapid PVST+"),
    ("BPDU", "Bridge Protocol Data Unit used by spanning tree.", "2.5 Rapid PVST+"),
    # 3.1 Routing table
    ("Routing table", "The control-plane table of known routes.", "3.1 Routing table"),
    ("Prefix", "The network address and mask of a route.", "3.1 Routing table"),
    ("Administrative distance", "The trustworthiness of a routing source.", "3.1 Routing table"),
    ("Metric", "The cost of a route within a routing protocol.", "3.1 Routing table"),
    ("Next hop", "The immediate router to reach a destination.", "3.1 Routing table"),
    ("Outgoing interface", "The interface used to forward traffic.", "3.1 Routing table"),
    ("Longest prefix match", "Selecting the most specific route.", "3.1 Routing table"),
    ("Default route", "The 0.0.0.0/0 route used when no specific route matches.", "3.1 Routing table"),
    ("Routing protocol code", "A letter identifying how a route was learned.", "3.1 Routing table"),
    # 3.2 Static routing
    ("Static route", "A manually configured route.", "3.2 Static routing"),
    ("Default static route", "A static route to 0.0.0.0/0.", "3.2 Static routing"),
    ("Host route", "A route to a single /32 address.", "3.2 Static routing"),
    ("Floating static route", "A backup static route with a higher administrative distance.", "3.2 Static routing"),
    ("Null0", "A logical interface used to discard traffic.", "3.2 Static routing"),
    ("Recursive static route", "A static route pointing to a next-hop resolved by another route.", "3.2 Static routing"),
    ("Directly attached static route", "A static route pointing to an outgoing interface.", "3.2 Static routing"),
    # 3.3 OSPF
    ("OSPF", "Open Shortest Path First link-state routing protocol.", "3.3 OSPF"),
    ("OSPFv2", "OSPF for IPv4.", "3.3 OSPF"),
    ("OSPFv3", "OSPF for IPv6.", "3.3 OSPF"),
    ("Area", "A logical grouping of OSPF routers.", "3.3 OSPF"),
    ("Backbone area", "OSPF Area 0.", "3.3 OSPF"),
    ("Router ID", "A 32-bit identifier for an OSPF router.", "3.3 OSPF"),
    ("Hello packet", "OSPF packet used to discover and maintain neighbors.", "3.3 OSPF"),
    ("Dead interval", "Time to wait before declaring an OSPF neighbor down.", "3.3 OSPF"),
    ("DR", "Designated Router elected on broadcast networks.", "3.3 OSPF"),
    ("BDR", "Backup Designated Router.", "3.3 OSPF"),
    ("LSA", "Link-State Advertisement.", "3.3 OSPF"),
    ("LSDB", "Link-State Database.", "3.3 OSPF"),
    ("Neighbor adjacency", "A relationship where OSPF routers exchange LSAs.", "3.3 OSPF"),
    ("Point-to-point", "An OSPF network type with no DR/BDR election.", "3.3 OSPF"),
    ("Broadcast network type", "An OSPF network type with DR/BDR election.", "3.3 OSPF"),
    ("OSPF cost", "The metric calculated from interface bandwidth.", "3.3 OSPF"),
    # 3.4 FHRP
    ("HSRP", "Hot Standby Router Protocol, Cisco proprietary first-hop redundancy.", "3.4 FHRP"),
    ("VRRP", "Virtual Router Redundancy Protocol, open standard first-hop redundancy.", "3.4 FHRP"),
    ("Virtual IP", "A shared IP address used by an FHRP group.", "3.4 FHRP"),
    ("Active router", "The FHRP router currently forwarding traffic.", "3.4 FHRP"),
    ("Standby router", "The FHRP router waiting to take over.", "3.4 FHRP"),
    ("Priority", "A value used to elect the active FHRP router.", "3.4 FHRP"),
    ("Preemption", "Allowing a higher-priority router to reclaim active status.", "3.4 FHRP"),
    # 4.1 AAA
    ("AAA", "Authentication, Authorization, and Accounting.", "4.1 AAA"),
    ("TACACS+", "Cisco protocol for authentication with command authorization.", "4.1 AAA"),
    ("RADIUS", "Standard protocol for authentication, authorization, and accounting.", "4.1 AAA"),
    ("Local username", "A user account configured directly on the device.", "4.1 AAA"),
    ("Method list", "A sequence of methods used for AAA.", "4.1 AAA"),
    ("Privilege level", "A Cisco user access level.", "4.1 AAA"),
    # 4.2 SFTP/SCP
    ("SFTP", "SSH File Transfer Protocol.", "4.2 SFTP/SCP"),
    ("SCP", "Secure Copy Protocol over SSH.", "4.2 SFTP/SCP"),
    ("TFTP", "Trivial File Transfer Protocol, unencrypted.", "4.2 SFTP/SCP"),
    ("FTP", "File Transfer Protocol, unencrypted.", "4.2 SFTP/SCP"),
    ("Running-config", "The currently active configuration.", "4.2 SFTP/SCP"),
    ("Startup-config", "The configuration loaded at boot.", "4.2 SFTP/SCP"),
    # 4.3 NAT/PAT
    ("NAT", "Network Address Translation.", "4.3 NAT/PAT"),
    ("PAT", "Port Address Translation, many-to-one NAT.", "4.3 NAT/PAT"),
    ("Static NAT", "One-to-one address translation.", "4.3 NAT/PAT"),
    ("Dynamic NAT", "Translation using a pool of public addresses.", "4.3 NAT/PAT"),
    ("Inside local", "The private IP address of an internal host.", "4.3 NAT/PAT"),
    ("Inside global", "The public IP address representing an internal host.", "4.3 NAT/PAT"),
    ("Outside global", "The public IP address of an external host.", "4.3 NAT/PAT"),
    ("Overload", "Enabling many translations to a single address.", "4.3 NAT/PAT"),
    # 4.4 DNS records
    ("A record", "DNS record mapping a name to an IPv4 address.", "4.4 DNS records"),
    ("AAAA record", "DNS record mapping a name to an IPv6 address.", "4.4 DNS records"),
    ("CNAME record", "DNS canonical name alias record.", "4.4 DNS records"),
    ("MX record", "Mail exchange record.", "4.4 DNS records"),
    ("NS record", "Name server record.", "4.4 DNS records"),
    ("PTR record", "Pointer record for reverse DNS.", "4.4 DNS records"),
    ("SOA record", "Start of authority record.", "4.4 DNS records"),
    ("TXT record", "Text record often used for SPF or verification.", "4.4 DNS records"),
    # 4.5 IPsec VPNs
    ("IPsec", "A suite of protocols for secure communications.", "4.5 IPsec VPNs"),
    ("AH", "Authentication Header, provides integrity but no encryption.", "4.5 IPsec VPNs"),
    ("ESP", "Encapsulating Security Payload, provides encryption and integrity.", "4.5 IPsec VPNs"),
    ("IKE", "Internet Key Exchange for IPsec key negotiation.", "4.5 IPsec VPNs"),
    ("Transport mode", "IPsec mode encrypting only the payload.", "4.5 IPsec VPNs"),
    ("Tunnel mode", "IPsec mode encrypting the entire original packet.", "4.5 IPsec VPNs"),
    ("Site-to-site VPN", "A VPN connecting two networks.", "4.5 IPsec VPNs"),
    ("Remote access VPN", "A VPN connecting individual clients to a network.", "4.5 IPsec VPNs"),
    # 4.6 ACLs
    ("ACL", "Access Control List.", "4.6 ACLs"),
    ("Standard ACL", "ACL filtering by source IP only.", "4.6 ACLs"),
    ("Extended ACL", "ACL filtering by source, destination, protocol, and ports.", "4.6 ACLs"),
    ("Named ACL", "An ACL identified by a name rather than a number.", "4.6 ACLs"),
    ("Implicit deny", "The default action at the end of an ACL.", "4.6 ACLs"),
    ("Wildcard mask", "An inverse mask used in ACLs and routing protocols.", "4.6 ACLs"),
    ("ACE", "Access Control Entry, a single line in an ACL.", "4.6 ACLs"),
    # 4.7 Layer 2 security
    ("DHCP snooping", "A feature trusting only specified DHCP ports.", "4.7 Layer 2 security"),
    ("Dynamic ARP inspection", "A feature validating ARP packets against DHCP snooping bindings.", "4.7 Layer 2 security"),
    ("Storm control", "A feature limiting broadcast, multicast, and unknown unicast.", "4.7 Layer 2 security"),
    ("RA guard", "A feature filtering IPv6 router advertisements.", "4.7 Layer 2 security"),
    ("Port security", "A feature limiting MAC addresses on a switch port.", "4.7 Layer 2 security"),
    ("Violation mode", "Action taken when port security is violated.", "4.7 Layer 2 security"),
    ("Protected port", "A private VLAN edge port that cannot communicate with other protected ports.", "4.7 Layer 2 security"),
    # 5.1 Agentic AI
    ("Agentic AI", "AI systems that can autonomously perform tasks and make decisions.", "5.1 Agentic AI"),
    ("LLM", "Large Language Model.", "5.1 Agentic AI"),
    ("Copilot", "An AI assistant supporting network operations.", "5.1 Agentic AI"),
    ("Observability", "Collecting and analyzing telemetry for AI-driven insights.", "5.1 Agentic AI"),
    ("AI-driven troubleshooting", "Using AI to identify and remediate network issues.", "5.1 Agentic AI"),
    # 5.2 Prompt engineering
    ("Prompt", "Input text instructing a generative AI model.", "5.2 Prompt engineering"),
    ("Persona", "The role assigned to the AI in a prompt.", "5.2 Prompt engineering"),
    ("Instructions", "Specific directions in a prompt.", "5.2 Prompt engineering"),
    ("Output format", "Desired structure for the AI response.", "5.2 Prompt engineering"),
    ("Data classification", "Labeling the sensitivity of data used in prompts.", "5.2 Prompt engineering"),
    ("Context", "Background information provided in a prompt.", "5.2 Prompt engineering"),
    # 5.3 Management approaches
    ("CLI", "Command Line Interface.", "5.3 Management approaches"),
    ("GUI", "Graphical User Interface.", "5.3 Management approaches"),
    ("Cloud management", "Managing devices through a cloud-hosted platform.", "5.3 Management approaches"),
    ("Controller-based", "Centralized management via a controller such as DNA Center or vManage.", "5.3 Management approaches"),
    ("Automation-based", "Managing devices through scripts and orchestration.", "5.3 Management approaches"),
    ("Infrastructure as Code", "Managing infrastructure through declarative code.", "5.3 Management approaches"),
    ("SDN", "Software-Defined Networking.", "5.3 Management approaches"),
    ("Intent-based networking", "A management approach aligning network state with business intent.", "5.3 Management approaches"),
    # 5.4 SNMP
    ("SNMP", "Simple Network Management Protocol.", "5.4 SNMP"),
    ("MIB", "Management Information Base.", "5.4 SNMP"),
    ("OID", "Object Identifier.", "5.4 SNMP"),
    ("Trap", "An asynchronous SNMP notification.", "5.4 SNMP"),
    ("Inform", "An acknowledged SNMP notification.", "5.4 SNMP"),
    ("Get", "An SNMP request for a specific value.", "5.4 SNMP"),
    ("Walk", "An SNMP request traversing a branch of the MIB.", "5.4 SNMP"),
    ("Community string", "A simple SNMP authentication string.", "5.4 SNMP"),
    ("SNMPv3", "SNMP version with authentication and encryption.", "5.4 SNMP"),
    # 5.5 Ansible
    ("Ansible", "An agentless automation tool using YAML playbooks.", "5.5 Ansible"),
    ("Playbook", "A YAML file defining Ansible tasks.", "5.5 Ansible"),
    ("Task", "A single action in an Ansible playbook.", "5.5 Ansible"),
    ("Module", "A reusable Ansible component for specific operations.", "5.5 Ansible"),
    ("Inventory", "A list of managed hosts.", "5.5 Ansible"),
    ("Ad-hoc command", "A single Ansible command run without a playbook.", "5.5 Ansible"),
    ("Idempotency", "A property where repeated executions produce the same result.", "5.5 Ansible"),
    # 5.6 Syslog
    ("Syslog", "A standard for logging messages.", "5.6 Syslog"),
    ("Severity level", "The importance of a syslog message.", "5.6 Syslog"),
    ("Facility", "The source category of a syslog message.", "5.6 Syslog"),
    ("Timestamp", "The date and time of a log event.", "5.6 Syslog"),
    ("MNEMONIC", "A short code describing a syslog message.", "5.6 Syslog"),
    ("Syslog server", "A centralized collector of syslog messages.", "5.6 Syslog"),
]


CCNA_COMMANDS = [
    ("show ip interface brief", "displays a summary of interface IP status", "2.4 L2/L3 troubleshooting"),
    ("show interfaces", "displays detailed interface statistics and errors", "2.4 L2/L3 troubleshooting"),
    ("show vlan brief", "displays VLAN assignments and status", "2.4 L2/L3 troubleshooting"),
    ("show mac address-table", "displays learned MAC addresses", "2.4 L2/L3 troubleshooting"),
    ("show spanning-tree", "displays spanning-tree topology", "2.5 Rapid PVST+"),
    ("show spanning-tree vlan 10", "displays spanning-tree for VLAN 10", "2.5 Rapid PVST+"),
    ("show cdp neighbors", "displays directly connected Cisco devices", "2.3 CDP/LLDP"),
    ("show lldp neighbors", "displays directly connected devices via LLDP", "2.3 CDP/LLDP"),
    ("show ip route", "displays the IPv4 routing table", "3.1 Routing table"),
    ("show ipv6 route", "displays the IPv6 routing table", "3.1 Routing table"),
    ("show ip ospf neighbor", "displays OSPF neighbors", "3.3 OSPF"),
    ("show ip ospf interface", "displays OSPF interface state", "3.3 OSPF"),
    ("show ip protocols", "displays active routing protocols", "3.3 OSPF"),
    ("show standby", "displays HSRP status", "3.4 FHRP"),
    ("show vrrp", "displays VRRP status", "3.4 FHRP"),
    ("show ip nat translations", "displays active NAT translations", "4.3 NAT/PAT"),
    ("show access-lists", "displays configured ACLs", "4.6 ACLs"),
    ("show ip dhcp pool", "displays DHCP pool usage", "1.7 DHCPv4"),
    ("show ip dhcp binding", "displays active DHCP leases", "1.7 DHCPv4"),
    ("show logging", "displays system log messages", "5.6 Syslog"),
    ("show snmp community", "displays SNMP community strings", "5.4 SNMP"),
    ("show controllers", "displays physical layer details", "1.1 Cable/interface diagnostics"),
    ("show ip arp", "displays the ARP table", "2.4 L2/L3 troubleshooting"),
    ("show ipv6 neighbors", "displays IPv6 neighbor entries", "2.4 L2/L3 troubleshooting"),
    ("show etherchannel summary", "displays EtherChannel status", "2.1 Infrastructure connectivity"),
    ("show port-security", "displays port security status", "4.7 Layer 2 security"),
    ("show dhcp snooping binding", "displays DHCP snooping bindings", "4.7 Layer 2 security"),
    ("show run", "displays the running configuration", "4.2 SFTP/SCP"),
    ("copy running-config startup-config", "saves the active configuration to NVRAM", "4.2 SFTP/SCP"),
    ("copy running-config scp:", "securely copies the running configuration via SCP", "4.2 SFTP/SCP"),
    ("copy scp: running-config", "securely copies a file from an SCP server to running-config", "4.2 SFTP/SCP"),
    ("ping", "tests reachability to a destination", "2.4 L2/L3 troubleshooting"),
    ("traceroute", "traces the path to a destination", "2.4 L2/L3 troubleshooting"),
    ("debug ip dhcp", "enables DHCP debugging", "1.7 DHCPv4"),
    ("terminal monitor", "copies debug/log output to the current terminal session", "2.4 L2/L3 troubleshooting"),
]

CCNA_COMPARISONS = [
    ("Straight-through cable", "Crossover cable", "Straight-through connects different device types; crossover connects similar device types."),
    ("Single-mode fiber", "Multimode fiber", "Single-mode travels farther with a single light path; multimode uses multiple paths for shorter distances."),
    ("Type 1 hypervisor", "Type 2 hypervisor", "Type 1 runs directly on hardware; Type 2 runs on a host OS."),
    ("VM", "Container", "VMs include a full guest OS; containers share the host OS kernel."),
    ("Access port", "Trunk port", "Access port carries one VLAN; trunk carries multiple VLANs with tags."),
    ("LACP", "PAgP", "LACP is IEEE standard; PAgP is Cisco proprietary."),
    ("CDP", "LLDP", "CDP is Cisco proprietary; LLDP is vendor-neutral."),
    ("OSPFv2", "OSPFv3", "OSPFv2 is for IPv4; OSPFv3 is for IPv6 and uses link-local addresses."),
    ("HSRP", "VRRP", "HSRP is Cisco proprietary; VRRP is an open standard."),
    ("Static NAT", "PAT", "Static NAT maps one private to one public address; PAT maps many to one using ports."),
    ("Standard ACL", "Extended ACL", "Standard ACL filters by source IP; extended ACL filters by source, destination, protocol, and ports."),
    ("AH", "ESP", "AH provides integrity; ESP provides encryption and integrity."),
    ("Transport mode", "Tunnel mode", "Transport mode encrypts the payload; tunnel mode encrypts the entire original packet."),
    ("Syslog", "SNMP", "Syslog is for logging; SNMP is for monitoring and traps."),
    ("Trap", "Inform", "Traps are unacknowledged; informs require acknowledgment."),
]

CCNA_SCENARIOS = [
    ("A user reports slow performance on a switch port.", "The port shows input errors and CRC errors incrementing.", "The issue is likely a cable fault, duplex mismatch, or bad transceiver.", "1.1 Cable/interface diagnostics"),
    ("A server virtual machine cannot reach its default gateway.", "The VM is connected to a vSwitch with the wrong VLAN.", "Move the VM to the correct VLAN or reconfigure the vSwitch port group.", "1.2 Virtualization"),
    ("A host is configured with IP 192.168.1.50/27 and gateway 192.168.1.33.", "The network is 192.168.1.32/27.", "The host IP and gateway are in the same subnet; verify routing and interface status.", "1.3 IPv4 troubleshooting"),
    ("A host autoconfigures an IPv6 address using SLAAC.", "The prefix is 2001:db8::/64 and the MAC is 00:1a:2b:3c:4d:5e.", "The host uses modified EUI-64 to derive the interface identifier.", "1.4 IPv6 troubleshooting"),
    ("An office deploys new access points on 2.4 GHz channel 6.", "Neighboring offices also use channel 6.", "Change to non-overlapping channels 1 or 11 to reduce co-channel interference.", "1.5 Wireless principles"),
    ("A Windows laptop cannot obtain an IP address.", "Running ipconfig shows 169.254.10.5.", "The laptop failed DHCP and used APIPA; check DHCP server and relay.", "1.6 Client connectivity"),
    ("A router is configured with 'ip helper-address 10.1.1.10' on a client VLAN interface.", "Clients in that VLAN cannot obtain DHCP leases.", "Verify the helper address, DHCP server reachability, and pool availability.", "1.7 DHCPv4"),
    ("An engineer configures a trunk between two switches.", "The trunk is not forming because one side is set to 'switchport mode access'.", "Set both sides to trunk mode or dynamic desirable to allow trunking.", "2.1 Infrastructure connectivity"),
    ("A phone and PC connect to the same switch port.", "The port must separate voice and data traffic.", "Configure a voice VLAN and data VLAN on the access port.", "2.2 Edge-host connectivity"),
    ("A network documentation audit reveals missing neighbor information.", "LLDP is enabled on all devices.", "Use 'show lldp neighbors detail' to validate topology documentation.", "2.3 CDP/LLDP"),
    ("A switch port connected to a server is err-disabled.", "The error log shows a port-security violation.", "Identify the violating MAC, clear the violation, and re-enable the port.", "2.4 L2/L3 troubleshooting"),
    ("A new switch is added to a topology with Rapid PVST+.", "The new switch has a lower bridge priority than the current root.", "The new switch becomes root unless Root Guard or a lower priority is configured on the intended root.", "2.5 Rapid PVST+"),
    ("A router has the following routes: 10.0.0.0/24 and 10.0.0.0/16.", "A packet arrives destined to 10.0.0.50.", "The router forwards using the /24 route because of longest prefix match.", "3.1 Routing table"),
    ("A floating static route is configured with AD 150.", "The primary route with AD 1 is reachable.", "The floating static route remains inactive while the primary route is present.", "3.2 Static routing"),
    ("Two OSPF routers on a broadcast segment are stuck in 2-WAY state.", "Neither is DR or BDR.", "On a broadcast segment, full adjacencies are only formed with DR/BDR; 2-WAY is normal for DROTHERs.", "3.3 OSPF"),
    ("An HSRP group has RouterA priority 110 and RouterB priority 100.", "Preemption is enabled on RouterA.", "RouterA becomes and remains active because it has the highest priority.", "3.4 FHRP"),
    ("A company wants centralized authentication and command authorization.", "The devices must remain manageable if the server is unreachable.", "Configure AAA with TACACS+ and a local fallback method list.", "4.1 AAA"),
    ("An engineer needs to back up the running configuration securely.", "TFTP is available but unencrypted.", "Use SCP or SFTP to copy the configuration to a secure server.", "4.2 SFTP/SCP"),
    ("An internal host with IP 192.168.1.10 accesses a public web server.", "PAT is configured on the edge router.", "The router translates the source IP/port to the public address and a unique source port.", "4.3 NAT/PAT"),
    ("A user cannot reach mail.example.com.", "An MX query returns no records.", "Without an MX record, mail servers cannot deliver email for the domain.", "4.4 DNS records"),
    ("A remote worker connects to corporate HQ over the Internet using IPsec.", "The VPN must encrypt the entire original IP packet.", "Use IPsec tunnel mode for site-to-site or remote access VPNs.", "4.5 IPsec VPNs"),
    ("An ACL is applied inbound on a router interface.", "The first line permits HTTP from any to 10.1.1.10; the rest deny all.", "Only HTTP traffic to 10.1.1.10 is allowed inbound; all other traffic is denied.", "4.6 ACLs"),
    ("A rogue DHCP server appears on a switch.", "DHCP snooping is enabled and the rogue port is untrusted.", "DHCP offers from the untrusted port are dropped.", "4.7 Layer 2 security"),
    ("An AI copilot suggests a configuration change based on telemetry.", "The engineer must decide whether to apply it.", "Agentic AI assists operations but human oversight remains critical.", "5.1 Agentic AI"),
    ("A prompt asks the AI to 'explain OSPF neighbors in one paragraph for a junior engineer'.", "The output must be concise and educational.", "The prompt includes instructions, output format, and persona for better results.", "5.2 Prompt engineering"),
    ("A company manages hundreds of branch routers.", "They want consistent, version-controlled configuration.", "Adopt Infrastructure as Code with Ansible and Git for configuration management.", "5.3 Management approaches"),
    ("An NMS polls interface counters from routers every 60 seconds.", "Traps are also sent for link down events.", "SNMP provides both polling and asynchronous notifications.", "5.4 SNMP"),
    ("An Ansible playbook sets NTP servers on all switches.", "It is run twice.", "The second run should be idempotent and make no changes if configuration is already correct.", "5.5 Ansible"),
    ("A syslog message shows '%SYS-5-CONFIG_I: Configured from console by admin'.", "The severity level is 5.", "Level 5 is a notification-level message indicating a configuration change.", "5.6 Syslog"),
    ("A router has two static routes: 'ip route 10.0.0.0 255.0.0.0 192.168.1.1' and 'ip route 10.0.0.0 255.0.0.0 192.168.1.2 150'.", "Both next-hops are reachable.", "The first route is installed because it has the lower administrative distance.", "3.2 Static routing"),
    ("A switch receives a frame with destination MAC unknown in the CAM table.", "The switch has no MAC entry for the destination.", "The switch floods the frame within the source VLAN.", "2.1 Infrastructure connectivity"),
    ("An OSPF broadcast segment has five routers.", "All routers have the same priority on the segment.", "The router with the highest router ID becomes the DR; the second highest becomes BDR.", "3.3 OSPF"),
    ("A DHCP server is on a different subnet from the clients.", "No helper address is configured on the client VLAN interface.", "Clients cannot obtain IP addresses because DHCP Discover broadcasts are not forwarded.", "1.7 DHCPv4"),
    ("A wireless network uses WPA2-Personal with a weak PSK.", "An attacker captures the 4-way handshake.", "The attacker can attempt offline brute-force against the PSK.", "1.5 Wireless principles"),
    ("A PC cannot reach a web server by name but can reach it by IP.", "Other hosts resolve the name correctly.", "The issue is likely with the PC's DNS configuration.", "4.4 DNS records"),
    ("An engineer configures 'ip nat inside source list 1 interface gig0/0 overload'.", "Hosts on the inside network have private addresses.", "Multiple inside hosts share the public IP of gig0/0 using PAT.", "4.3 NAT/PAT"),
    ("A port is configured with 'spanning-tree bpduguard enable'.", "A BPDU is received on the port.", "The port is err-disabled to prevent rogue switches.", "2.5 Rapid PVST+"),
    ("A router is configured for HSRP with priority 95 and no preemption.", "Another router joins the group with priority 105.", "The new router does not take over unless the active router fails, because preemption is disabled.", "3.4 FHRP"),
    ("A network uses Ansible to push SNMP community strings to switches.", "The playbook is run again with the same variables.", "No changes are made because Ansible is idempotent.", "5.5 Ansible"),
    ("A switch interface shows input errors incrementing rapidly.", "The duplex setting is full on one side and half on the other.", "The mismatch causes late collisions and CRC errors.", "1.1 Cable/interface diagnostics"),
    ("A VM cannot communicate with other VMs in the same VLAN.", "The VM is connected to a vSwitch port group assigned to a different VLAN.", "Move the VM to the correct port group or change the port group VLAN.", "1.2 Virtualization"),
    ("A host has IPv6 address 2001:db8::1/64 and default gateway fe80::1.", "The host cannot reach the Internet.", "Verify the link-local gateway is reachable and routing is configured for the global prefix.", "1.4 IPv6 troubleshooting"),
    ("A user reports intermittent wireless disconnections.", "The access point is on a channel with heavy neighboring traffic.", "Change to a less congested channel to reduce interference.", "1.5 Wireless principles"),
    ("A Linux host cannot reach the default gateway.", "Running 'ip addr' shows the IP is correctly configured.", "Check routing with 'ip route' and ARP with 'ip neigh'.", "1.6 Client connectivity"),
    ("A router is configured as a DHCP relay with 'ip helper-address 10.1.1.10'.", "DHCP clients still fail to receive leases.", "Verify the helper address, server reachability, and that the server has a scope for the client subnet.", "1.7 DHCPv4"),
    ("An engineer connects a router to a switch with a crossover cable.", "Both devices use Auto-MDIX.", "The link comes up regardless of cable type because Auto-MDIX adjusts.", "2.1 Infrastructure connectivity"),
    ("A switch port is configured with data VLAN 10 and voice VLAN 20.", "A phone connected to the port boots and obtains an IP from VLAN 20.", "The LLDP-MED or CDP negotiation placed the phone in the voice VLAN.", "2.2 Edge-host connectivity"),
    ("A network diagram lists a router with IP 10.1.1.1 on interface Gi0/0.", "'show cdp neighbors detail' shows a different IP for the same device.", "Update the documentation to match the actual configuration discovered via CDP/LLDP.", "2.3 CDP/LLDP"),
    ("A user cannot access a server across a Layer 3 switch.", "'show ip interface brief' shows the SVI is down/down.", "The VLAN may not exist, the SVI may be shut down, or no ports are assigned to the VLAN.", "2.4 L2/L3 troubleshooting"),
    ("A switch has Rapid PVST+ enabled and a new port is connected to a host.", "The port is not configured with PortFast.", "The port goes through listening and learning states before forwarding, causing temporary connectivity delay.", "2.5 Rapid PVST+"),
]

CCNA_SIMLETS = [
    (
        """Switch# show interfaces gigabitethernet0/1
GigabitEthernet0/1 is up, line protocol is up
  Hardware is Gigabit Ethernet, address is 001e.14a4.b201
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Full-duplex, 1000Mb/s, media type is 10/100/1000BaseTX
  input error 0, CRC 0, frame 0, overrun 0, ignored 0
  output error 0, collisions 0, interface resets 0""",
        "What is the operational status of Gi0/1?",
        [("Down/down", False), ("Up/up", True), ("Up/down", False), ("Administratively down", False)],
        "The first line shows 'is up, line protocol is up'.",
        "2.4 L2/L3 troubleshooting",
    ),
    (
        """Router# show ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
Gateway of last resort is 203.0.113.1 to network 0.0.0.0

S*    0.0.0.0/0 [1/0] via 203.0.113.1
      10.0.0.0/24 is subnetted, 1 subnets
C        10.0.0.0 is directly connected, GigabitEthernet0/0
L        10.0.0.1/32 is directly connected, GigabitEthernet0/0
O        10.1.1.0/24 [110/2] via 10.0.0.2, 00:05:12, GigabitEthernet0/0""",
        "Which route is used for traffic to 10.1.1.50?",
        [("Default route", False), ("Connected route 10.0.0.0/24", False), ("OSPF route 10.1.1.0/24", True), ("Local route 10.0.0.1/32", False)],
        "The OSPF route 10.1.1.0/24 is the most specific match.",
        "3.1 Routing table",
    ),
    (
        """Switch# show spanning-tree vlan 10

VLAN0010
  Spanning tree enabled protocol rstp
  Root ID    Priority    4096
             Address     0000.0c00.1111
             This bridge is the root
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    4096
             Address     0000.0c00.1111
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  300 sec""",
        "What is the role of this switch in VLAN 10?",
        [("Root bridge", True), ("Non-root bridge", False), ("Disabled", False), ("Backup root", False)],
        "The output states 'This bridge is the root'.",
        "2.5 Rapid PVST+",
    ),
    (
        """Router# show ip ospf neighbor
Neighbor ID     Pri   State           Dead Time   Address         Interface
2.2.2.2           1   FULL/BDR        00:00:35    10.1.1.2        GigabitEthernet0/0
3.3.3.3           1   FULL/DR         00:00:31    10.1.1.3        GigabitEthernet0/0""",
        "Which router is the Designated Router on this segment?",
        [("The local router", False), ("2.2.2.2", False), ("3.3.3.3", True), ("There is no DR", False)],
        "The neighbor with state FULL/DR is the Designated Router.",
        "3.3 OSPF",
    ),
    (
        """Router# show ip nat translations
Pro Inside global      Inside local       Outside local      Outside global
--- 203.0.113.5        192.168.1.10       ---                ---
tcp 203.0.113.5:51234  192.168.1.10:51234 8.8.8.8:443        8.8.8.8:443""",
        "What type of NAT is configured?",
        [("Static NAT", False), ("Dynamic NAT", False), ("PAT", True), ("No NAT", False)],
        "Multiple inside local addresses share a single inside global address with different ports, indicating PAT.",
        "4.3 NAT/PAT",
    ),
    (
        """Switch# show port-security interface gigabitethernet0/2
Port Security              : Enabled
Port Status                : Secure-shutdown
Violation Mode             : Shutdown
Maximum MAC Addresses      : 1
Total MAC Addresses        : 2
Configured MAC Addresses   : 0
Sticky MAC Addresses       : 1
Last Source Address:Vlan   : 0050.56c0.0008:10
Security Violation Count   : 1""",
        "Why is the port in secure-shutdown?",
        [("The port has no MAC addresses learned", False), ("A second MAC address was detected", True), ("The sticky MAC was removed", False), ("Port security is disabled", False)],
        "The maximum is 1 but total MAC addresses is 2, causing a violation.",
        "4.7 Layer 2 security",
    ),
    (
        """Switch# show vlan brief

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Gi0/3
10   DATA                             active    Gi0/1, Gi0/2
20   VOICE                            active    Gi0/1
30   GUEST                            active    Gi0/4""",
        "Which ports carry both VLAN 10 and VLAN 20 traffic?",
        [("Gi0/1", True), ("Gi0/2", False), ("Gi0/3", False), ("Gi0/4", False)],
        "Gi0/1 is assigned to both VLAN 10 (DATA) and VLAN 20 (VOICE), indicating a voice VLAN configuration.",
        "2.2 Edge-host connectivity",
    ),
    (
        """Router# show access-lists 100
Extended IP access list 100
    10 permit tcp any host 10.1.1.10 eq 80
    20 permit tcp any host 10.1.1.10 eq 443
    30 deny ip any any log""",
        "What traffic is permitted to 10.1.1.10?",
        [("Only HTTP", False), ("Only HTTPS", False), ("HTTP and HTTPS", True), ("All traffic", False)],
        "Lines 10 and 20 permit HTTP (80) and HTTPS (443).",
        "4.6 ACLs",
    ),
]

CCNA_DRAG_DROP_POOLS = [
    (
        "1.1 Cable/interface diagnostics",
        "Match the cable type to its typical use.",
        [
            ("Straight-through", "Switch to router"),
            ("Crossover", "Switch to switch"),
            ("Rollover", "PC to router console"),
            ("Single-mode fiber", "Long-distance campus link"),
        ],
    ),
    (
        "1.2 Virtualization",
        "Match the virtualization concept to its description.",
        [
            ("Hypervisor", "Runs virtual machines"),
            ("Container", "Shares host OS kernel"),
            ("vSwitch", "Connects VMs on a host"),
            ("vNIC", "Virtual network interface"),
        ],
    ),
    (
        "2.1 Infrastructure connectivity",
        "Match the trunking concept to its description.",
        [
            ("Access port", "Single VLAN, untagged"),
            ("Trunk port", "Multiple VLANs, tagged"),
            ("Native VLAN", "Untagged traffic on a trunk"),
            ("Allowed VLAN list", "Permitted VLANs on a trunk"),
        ],
    ),
    (
        "2.5 Rapid PVST+",
        "Order the Rapid PVST+ port roles from most preferred path to root to alternate.",
        [
            ("Root port", "Best path to root"),
            ("Designated port", "Forwards traffic for segment"),
            ("Alternate port", "Backup path to root"),
            ("Backup port", "Backup on same segment"),
        ],
    ),
    (
        "3.3 OSPF",
        "Match the OSPF network type to its DR/BDR behavior.",
        [
            ("Broadcast", "DR/BDR election"),
            ("Point-to-point", "No DR/BDR"),
            ("Loopback", "Advertised as /32"),
        ],
    ),
    (
        "4.4 DNS records",
        "Match the DNS record type to its purpose.",
        [
            ("A", "IPv4 address"),
            ("AAAA", "IPv6 address"),
            ("CNAME", "Alias"),
            ("MX", "Mail server"),
            ("PTR", "Reverse lookup"),
        ],
    ),
    (
        "4.6 ACLs",
        "Match the ACL type to its filtering capability.",
        [
            ("Standard ACL", "Source IP only"),
            ("Extended ACL", "Source, destination, protocol, port"),
            ("Named ACL", "Identified by a name"),
        ],
    ),
    (
        "4.7 Layer 2 security",
        "Match the Layer 2 security feature to its purpose.",
        [
            ("DHCP snooping", "Trust only authorized DHCP ports"),
            ("DAI", "Validate ARP packets"),
            ("Storm control", "Limit broadcast/multicast"),
            ("Port security", "Limit MAC addresses on a port"),
        ],
    ),
    (
        "5.6 Syslog",
        "Order syslog severity levels from most to least severe.",
        [
            ("Emergency", "Level 0"),
            ("Alert", "Level 1"),
            ("Critical", "Level 2"),
            ("Error", "Level 3"),
            ("Warning", "Level 4"),
            ("Notice", "Level 5"),
            ("Informational", "Level 6"),
            ("Debugging", "Level 7"),
        ],
    ),
]

CCNA_FILL_BLANK_POOLS = [
    ("1.1 Cable/interface diagnostics", "A cable with identical pinouts on both ends used for different device types is called a __________ cable.", "straight-through", ["crossover", "rollover", "console", "fiber"]),
    ("1.1 Cable/interface diagnostics", "Collisions occurring after the first 64 bytes usually indicate a __________ mismatch.", "duplex", ["speed", "VLAN", "IP", "MTU"]),
    ("1.2 Virtualization", "A __________ is a lightweight isolated runtime that shares the host OS kernel.", "container", ["virtual machine", "hypervisor", "vSwitch", "bare metal"]),
    ("1.3 IPv4 troubleshooting", "The 169.254.0.0/16 range used when DHCP fails is called __________.", "APIPA", ["DHCP", "loopback", "private", "multicast"]),
    ("1.4 IPv6 troubleshooting", "Link-local IPv6 addresses start with the prefix __________.", "FE80::/10", ["FC00::/7", "2000::/3", "FF02::/16", "::1/128"]),
    ("1.5 Wireless principles", "The Wi-Fi security protocol that provides Simultaneous Authentication of Equals is __________.", "WPA3", ["WPA2", "WEP", "802.1X", "Open"]),
    ("1.7 DHCPv4", "The Cisco command to forward DHCP broadcasts to a remote server is __________.", "ip helper-address", ["ip dhcp pool", "ip forward-protocol", "default-router", "dns-server"]),
    ("2.1 Infrastructure connectivity", "The IEEE standard for VLAN tagging is __________.", "802.1Q", ["ISL", "DTP", "LACP", "VTP"]),
    ("2.1 Infrastructure connectivity", "The protocol used to bundle switch links into an EtherChannel is __________.", "LACP", ["PAgP", "DTP", "VTP", "STP"]),
    ("2.2 Edge-host connectivity", "A switch port that carries traffic for a single VLAN is called an __________ port.", "access", ["trunk", "hybrid", "routed", "dynamic"]),
    ("2.3 CDP/LLDP", "The vendor-neutral protocol for neighbor discovery is __________.", "LLDP", ["CDP", "DTP", "VTP", "STP"]),
    ("2.5 Rapid PVST+", "The spanning-tree feature that immediately transitions access ports to forwarding is __________.", "PortFast", ["BPDU Guard", "Root Guard", "Loop Guard", "BackboneFast"]),
    ("3.1 Routing table", "The process of selecting the most specific route is called __________ match.", "longest prefix", ["shortest path", "administrative distance", "metric", "next hop"]),
    ("3.2 Static routing", "A backup static route with a higher administrative distance is called a __________ static route.", "floating", ["default", "summary", "recursive", "directly attached"]),
    ("3.3 OSPF", "The 32-bit identifier for an OSPF router is called the __________.", "router ID", ["area ID", "process ID", "neighbor ID", "DR ID"]),
    ("3.4 FHRP", "Cisco's proprietary first-hop redundancy protocol is __________.", "HSRP", ["VRRP", "GLBP", "BGP", "OSPF"]),
    ("4.3 NAT/PAT", "The type of NAT that maps many private addresses to one public address using ports is __________.", "PAT", ["static NAT", "dynamic NAT", "twice NAT", "NAT overload is also correct"]),
    ("4.4 DNS records", "The DNS record type used for reverse lookups is __________.", "PTR", ["A", "AAAA", "CNAME", "MX"]),
    ("4.6 ACLs", "The default action at the end of every ACL is an implicit __________.", "deny", ["permit", "log", "forward", "drop"]),
    ("4.7 Layer 2 security", "The feature that validates ARP packets against DHCP snooping bindings is __________.", "DAI", ["DHCP snooping", "storm control", "RA guard", "port security"]),
    ("5.5 Ansible", "The YAML file that defines a set of Ansible tasks is called a __________.", "playbook", ["inventory", "role", "module", "task"]),
    ("5.6 Syslog", "Syslog level 0 is called __________.", "emergency", ["alert", "critical", "error", "debugging"]),
]

CCNA_MULTIPLE_CHOICE_POOLS = [
    (
        "1.1 Cable/interface diagnostics",
        "Which issues can cause interface input errors? (Choose three.)",
        ["CRC errors", "Duplex mismatch", "Cable faults"],
        ["Correct VLAN assignment", "Full-duplex operation", "Proper pinout", "STP convergence"],
        "Input errors can be caused by CRC errors, duplex mismatch, and cable faults.",
    ),
    (
        "1.2 Virtualization",
        "Which statements describe containers? (Choose two.)",
        ["They share the host OS kernel", "They are lightweight compared to VMs"],
        ["They include a full guest OS", "They require a Type 1 hypervisor", "They cannot run on Linux", "They boot slowly"],
        "Containers share the host OS kernel and are lightweight compared to VMs.",
    ),
    (
        "1.3 IPv4 troubleshooting",
        "Which values are needed to determine if two hosts are on the same subnet? (Choose two.)",
        ["IP address", "Subnet mask"],
        ["Default gateway", "DNS server", "MAC address", "Hostname"],
        "The IP address and subnet mask determine the local subnet.",
    ),
    (
        "1.5 Wireless principles",
        "Which factors affect RF signal strength or quality? (Choose three.)",
        ["Absorption", "Reflection", "Interference"],
        ["Static VLAN assignment", "Subnet mask length", "Default gateway", "Full-duplex mode"],
        "Absorption, reflection, and interference affect RF propagation.",
    ),
    (
        "2.1 Infrastructure connectivity",
        "Which statements about 802.1Q trunks are true? (Choose three.)",
        ["They carry multiple VLANs", "They add a VLAN tag", "Native VLAN is untagged"],
        ["Access ports carry multiple VLANs", "All VLANs are tagged", "DTP is required", "Trunks cannot carry voice VLAN"],
        "Trunks carry multiple VLANs with tags; native VLAN is untagged.",
    ),
    (
        "2.2 Edge-host connectivity",
        "Which port attributes are commonly configured for edge hosts? (Choose two.)",
        ["Access VLAN", "Voice VLAN"],
        ["BGP peering", "OSPF area", "LACP negotiation", "DR election"],
        "Edge ports are configured with access VLAN and optionally voice VLAN.",
    ),
    (
        "2.5 Rapid PVST+",
        "Which features protect spanning-tree topology? (Choose two.)",
        ["BPDU Guard", "Root Guard"],
        ["PortFast", "EtherChannel", "VTP", "DTP"],
        "BPDU Guard and Root Guard protect the spanning-tree topology.",
    ),
    (
        "3.1 Routing table",
        "Which values are used to select the best route when multiple routes exist? (Choose two.)",
        ["Longest prefix match", "Administrative distance"],
        ["Hostname", "Interface MAC address", "DNS suffix", "VLAN ID"],
        "Longest prefix match and administrative distance determine the best route.",
    ),
    (
        "3.3 OSPF",
        "Which conditions must match for OSPF neighbors to form an adjacency? (Choose two.)",
        ["Area ID", "Hello and dead timers"],
        ["Router hostname", "Process ID", "Interface IP address in same subnet only", "Same model"],
        "OSPF neighbors need matching area ID, subnet/mask, hello/dead timers, and network type.",
    ),
    (
        "3.4 FHRP",
        "Which statements about HSRP are true? (Choose two.)",
        ["HSRP is Cisco proprietary", "The active router forwards traffic"],
        ["HSRP uses a real MAC only", "Preemption is always disabled", "VRRP is required with HSRP", "Only IPv6 is supported"],
        "HSRP is Cisco proprietary and uses active/standby routers.",
    ),
    (
        "4.1 AAA",
        "Which are components of AAA? (Choose three.)",
        ["Authentication", "Authorization", "Accounting"],
        ["Auditing", "Archiving", "Addressing", "Allocation"],
        "AAA stands for Authentication, Authorization, and Accounting.",
    ),
    (
        "4.3 NAT/PAT",
        "Which statements about PAT are true? (Choose two.)",
        ["Many internal addresses share one public address", "Port numbers differentiate sessions"],
        ["Each internal host gets a unique public address", "PAT does not translate ports", "Static NAT is required first", "PAT only works for TCP"],
        "PAT translates many private addresses to one public address using unique source ports.",
    ),
    (
        "4.6 ACLs",
        "Which statements about extended ACLs are true? (Choose two.)",
        ["They can filter by destination IP", "They can filter by TCP/UDP port"],
        ["They filter by source IP only", "They cannot be named", "They must be applied outbound only", "They use subnet masks instead of wildcard masks"],
        "Extended ACLs filter by source, destination, protocol, and port.",
    ),
    (
        "4.7 Layer 2 security",
        "Which features help secure a Layer 2 switch? (Choose three.)",
        ["DHCP snooping", "DAI", "Port security"],
        ["NAT overload", "OSPF authentication", "BGP dampening", "VTP pruning"],
        "DHCP snooping, DAI, and port security are Layer 2 security features.",
    ),
    (
        "5.3 Management approaches",
        "Which are examples of network management approaches? (Choose two.)",
        ["Controller-based", "Infrastructure as Code"],
        ["MAC flooding", "ARP spoofing", "DHCP starvation", "Port scanning"],
        "Controller-based management and Infrastructure as Code are valid approaches.",
    ),
    (
        "5.5 Ansible",
        "Which statements about Ansible are true? (Choose two.)",
        ["It uses YAML playbooks", "It is agentless"],
        ["It requires an agent on managed nodes", "It only supports Cisco devices", "It cannot run ad-hoc commands", "It uses JSON playbooks"],
        "Ansible uses YAML playbooks and is agentless.",
    ),
    (
        "1.1 Cable/interface diagnostics",
        "Which are valid Ethernet cable categories? (Choose two.)",
        ["Cat 5e", "Cat 6"],
        ["Cat 3 for Gigabit", "Cat 7 does not exist", "Fiber UTP", "Coax for Ethernet"],
        "Cat 5e and Cat 6 support Gigabit Ethernet. Cat 3 does not support Gigabit.",
    ),
    (
        "1.2 Virtualization",
        "Which statements describe a Type 1 hypervisor? (Choose two.)",
        ["Runs directly on hardware", "Also called bare-metal"],
        ["Requires a host OS", "Runs on top of Windows", "Is always slower than Type 2", "Cannot run multiple VMs"],
        "Type 1 hypervisors run directly on hardware; Type 2 run on a host OS.",
    ),
    (
        "1.6 Client connectivity",
        "Which Windows commands can display IP configuration? (Choose two.)",
        ["ipconfig", "netsh interface ip show config"],
        ["ifconfig", "ip addr", "dig", "traceroute"],
        "ipconfig and netsh are Windows utilities. ifconfig/ip/dig are Linux/Unix tools.",
    ),
    (
        "2.2 Edge-host connectivity",
        "Which features are commonly configured on an access port for a phone and PC? (Choose two.)",
        ["Access VLAN", "Voice VLAN"],
        ["BGP neighbor", "OSPF area", "LACP", "DR election"],
        "Access ports for phones/PCs use access VLAN for data and voice VLAN for VoIP.",
    ),
    (
        "2.4 L2/L3 troubleshooting",
        "Which tools can help troubleshoot Layer 3 reachability? (Choose two.)",
        ["ping", "traceroute"],
        ["show mac address-table", "show vlan", "CDP", "LLDP"],
        "ping and traceroute test Layer 3 reachability. CDP/LLDP and MAC/VLAN tables are Layer 2 tools.",
    ),
    (
        "3.2 Static routing",
        "Which statements about floating static routes are true? (Choose two.)",
        ["They have a higher administrative distance than the primary route", "They become active when the primary route fails"],
        ["They are installed before the primary route", "They use a lower AD", "They require dynamic routing", "They cannot use next-hop"],
        "Floating static routes use a higher AD as a backup; they activate when the primary route disappears.",
    ),
    (
        "3.3 OSPF",
        "Which OSPF neighbor states indicate progress toward full adjacency? (Choose two.)",
        ["2-Way", "Full"],
        ["Down", "Init", "Exchange", "Loading"],
        "2-Way and Full are valid neighbor states. Down/Init are earlier states; Exchange/Loading are intermediate.",
    ),
    (
        "4.2 SFTP/SCP",
        "Which statements about SFTP and SCP are true? (Choose two.)",
        ["They encrypt data in transit", "They run over SSH"],
        ["They use UDP", "They are unencrypted", "They require TFTP", "They use port 21"],
        "SFTP and SCP are secure file transfers over SSH. TFTP and FTP are unencrypted.",
    ),
    (
        "4.5 IPsec VPNs",
        "Which statements describe IPsec transport mode? (Choose two.)",
        ["Encrypts only the payload", "Used for host-to-host VPNs"],
        ["Encrypts the entire original packet", "Used for site-to-site VPNs", "Requires tunnel endpoints", "Adds a new IP header"],
        "Transport mode encrypts the payload and is used for host-to-host. Tunnel mode encrypts the entire packet.",
    ),
    (
        "5.1 Agentic AI",
        "Which are characteristics of agentic AI in network operations? (Choose two.)",
        ["Autonomous task execution", "Can analyze telemetry"],
        ["Requires no data", "Cannot make recommendations", "Replaces human oversight entirely", "Only follows predefined scripts"],
        "Agentic AI can autonomously execute tasks and analyze telemetry, but human oversight remains important.",
    ),
    (
        "5.4 SNMP",
        "Which SNMP versions support authentication and encryption? (Choose two.)",
        ["SNMPv3", "SNMPv3 only with authPriv"],
        ["SNMPv1", "SNMPv2c", "SNMPv2 with communities", "SNMPv1 with public string"],
        "SNMPv3 supports authentication and encryption. SNMPv1 and v2c use community strings without encryption.",
    ),
]

CCNA_SUBNETTING_POOLS = [
    {
        "section_key": "1.3 IPv4 troubleshooting",
        "question": "A host has IP address {ip}/{mask_len}. Which subnet does it belong to?",
        "answer_type": "network",
    },
    {
        "section_key": "1.3 IPv4 troubleshooting",
        "question": "Given network {network}/{mask_len}, what is the broadcast address?",
        "answer_type": "broadcast",
    },
    {
        "section_key": "1.3 IPv4 troubleshooting",
        "question": "How many usable host addresses are in a /{mask_len} subnet?",
        "answer_type": "hosts",
    },
    {
        "section_key": "1.3 IPv4 troubleshooting",
        "question": "What is the last usable host address in subnet {network}/{mask_len}?",
        "answer_type": "last_host",
    },
    {
        "section_key": "1.4 IPv6 troubleshooting",
        "question": "An IPv6 prefix is {ipv6_network}/{prefix_len}. How many /{sub_prefix_len} subnets can be created?",
        "answer_type": "ipv6_subnets",
    },
]
