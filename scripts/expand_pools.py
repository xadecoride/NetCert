#!/usr/bin/env python3
"""Expand content pools in generate_questions_v6.py to reach 10,000+ unique questions."""
import re

with open('scripts/generate_questions_v6.py') as f:
    content = f.read()

# ============================================================
# 1. EXPAND PROTOCOLS pool: 84 → 140 entries
# ============================================================
# Find the last PROTOCOLS entry and insert before the closing ]
proto_new = r'''
    ("6LoWPAN",3,"IP ICMPv6","","","IoT","IPv6 over low-power wireless personal area networks"),
    ("CoAP",7,"UDP 5683","","","IoT","constrained application protocol for IoT devices"),
    ("MQTT",7,"TCP 1883","","","IoT","publish-subscribe messaging for IoT sensors"),
    ("gRPC",7,"HTTP/2","","","API","high-performance RPC using HTTP/2 and protobuf"),
    ("REST",7,"HTTP","","","API","representational state transfer API architecture"),
    ("GraphQL",7,"TCP 443","","","API","query language for APIs with schema-driven data fetching"),
    ("SR-MPLS",3,"MPLS","","","MPLS","segment routing over MPLS data plane"),
    ("SRv6",3,"IPv6","","","MPLS","segment routing over IPv6 with SRH extension header"),
    ("EVPN",3,"MP-BGP","","","Overlay","Ethernet VPN with MP-BGP control plane for VXLAN"),
    ("VXLAN",3,"UDP 4789","","","Overlay","MAC-in-UDP encapsulation for network virtualization overlays"),
    ("Geneve",3,"UDP 6081","","","Overlay","generic network virtualization encapsulation with variable-length options"),
    ("STP",2,"BPDUs","","","Layer2","spanning tree protocol for loop prevention"),
    ("RSTP",2,"BPDUs","","","Layer2","rapid spanning tree with fast convergence"),
    ("MSTP",2,"BPDUs","","","Layer2","multiple spanning tree with VLAN instance mapping"),
    ("PVST+",2,"BPDUs","","","Layer2","Cisco per-VLAN spanning tree plus"),
    ("LLDP",2,"Ethertype 0x88CC","","","Layer2","link layer discovery protocol for neighbor topology"),
    ("CDP",2,"SNAP","","","Layer2","Cisco discovery protocol for neighbor info"),
    ("LACP",2,"Ethertype 0x8809","","","Layer2","link aggregation control protocol"),
    ("PAgP",2,"Ethernet","","","Layer2","Cisco port aggregation protocol"),
    ("UDLD",2,"Ethernet","","","Layer2","unidirectional link detection for fiber monitoring"),
    ("DTP",2,"Ethernet","","","Layer2","dynamic trunking protocol for VLAN trunk negotiation"),
    ("VTP",2,"SNAP","","","Layer2","VLAN trunking protocol for VLAN database sync"),
    ("REP",2,"Ethernet","","","Layer2","resilient Ethernet protocol for ring topologies"),
    ("FlexLink",2,"Ethernet","","","Layer2","Cisco link failover for dual-homed access"),
    ("ERPS",2,"Ethernet","","","Layer2","Ethernet ring protection switching ITU-T G.8032"),
    ("MACsec",2,"Ethertype 0x88E5","","","Security","MAC security with 802.1AE encryption"),
    ("MAB",2,"Ethernet","","","Security","MAC authentication bypass for 802.1X"),
    ("WebAuth",7,"HTTP/HTTPS","","","Security","captive portal web authentication"),
    ("EAP",2,"EAPoL","","","Security","extensible authentication protocol for 802.1X"),
    ("EAP-TLS",2,"EAP","","","Security","EAP with TLS certificate mutual authentication"),
    ("PEAP",2,"EAP","","","Security","protected EAP with TLS tunnel for MSCHAPv2"),
    ("EAP-FAST",2,"EAP","","","Security","EAP flexible authentication via secure tunneling"),
    ("PAP",7,"PPP","","","Security","password authentication protocol (cleartext)"),
    ("CHAP",2,"PPP","","","Security","challenge handshake authentication protocol"),
    ("MSCHAPv2",2,"PPP","","","Security","Microsoft CHAP v2 with mutual authentication"),
    ("RADIUS",7,"UDP 1812/1813","","","AAA","remote authentication dial-in user service"),
    ("TACACS+",7,"TCP 49","","","AAA","terminal access controller access-control system plus"),
    ("DIAMETER",7,"TCP 3868","","","AAA","next-gen AAA protocol replacing RADIUS"),
    ("LDAP",7,"TCP 389","","","AAA","lightweight directory access protocol"),
    ("Kerberos",7,"UDP 88","","","AAA","network authentication using tickets and KDC"),
    ("SSO",7,"HTTP/SAML","","","AAA","single sign-on with SAML/OAuth tokens"),
    ("OAuth2",7,"HTTP/HTTPS","","","AAA","authorization framework with token-based grants"),
    ("OpenID",7,"HTTP/HTTPS","","","AAA","identity layer on top of OAuth2 for authentication"),
    ("SAML",7,"HTTP/HTTPS","","","AAA","security assertion markup language for SSO"),
    ("SCIM",7,"HTTP/HTTPS","","","AAA","system for cross-domain identity management"),
    ("IPFIX",7,"UDP 4739","","","Monitoring","IP flow information export; NetFlow v10"),
    ("sFlow",7,"UDP 6343","","","Monitoring","sampled flow monitoring for traffic analysis"),
    ("NetFlow",7,"UDP 2055","","","Monitoring","Cisco IP flow accounting and export"),
    ("jFlow",7,"UDP 2055","","","Monitoring","Juniper implementation of flow monitoring"),
    ("SNMP",7,"UDP 161/162","","","Monitoring","simple network management protocol"),
    ("RMON",7,"SNMP","","","Monitoring","remote monitoring MIB for network statistics"),
    ("Syslog",7,"UDP 514","","","Monitoring","system logging protocol for event messages"),
    ("CWMP",7,"HTTP/HTTPS","","","Management","CPE WAN management protocol TR-069"),
    ("NETCONF",7,"SSH","","","Management","network configuration protocol over SSH"),
    ("RESTCONF",7,"HTTP/HTTPS","","","Management","RESTful configuration protocol using YANG"),
    ("gNMI",7,"gRPC","","","Management","gRPC network management interface for streaming"),
    ("YANG",7,"N/A","","","Management","data modeling language for network config"),
    ("OpenConfig",7,"N/A","","","Management","vendor-neutral YANG models for multi-vendor"),
    ("BFD",3,"UDP 3784","","","OAM","bidirectional forwarding detection for fast failure"),
    ("CFM",2,"Ethernet","","","OAM","connectivity fault management IEEE 802.1ag"),
    ("Y.1731",2,"Ethernet","","","OAM","ITU-T Ethernet OAM performance monitoring"),
    ("TWAMP",7,"UDP 862","","","OAM","two-way active measurement protocol for performance"),
    ("OAM",2,"Ethernet","","","OAM","operations administration and management"),
    ("VXLAN-GPE",3,"UDP 4790","","","Overlay","VXLAN generic protocol extension with next-protocol"),
    ("NSH",3,"UDP 4790","","","Overlay","network service header for service function chaining"),
    ("SR-TE",3,"MPLS","","","MPLS","segment routing traffic engineering with PCEP/ BGP-LS"),
    ("PCEP",3,"TCP 4189","","","MPLS","path computation element protocol for SR-TE"),
    ("BGP-LS",7,"TCP 179","","","MPLS","BGP link-state for TE topology distribution"),
    ("Flowspec",3,"MP-BGP","","","Security","BGP flow specification for DDoS mitigation"),
    ("IPSLA",7,"UDP","","","Monitoring","Cisco IP SLA for performance measurement"),
    ("NQA",7,"UDP","","","Monitoring","Huawei network quality analyzer for performance"),
    ("TWAMP Light",7,"UDP","","","OAM","simplified TWAMP for performance monitoring"),
    ("BFD Multihop",3,"UDP 4784","","","OAM","BFD for multihop paths between non-adjacent routers"),
    ("SDP",7,"UDP 4569","","","Protocol","session description protocol for media sessions"),
    ("SIP",7,"TCP/UDP 5060","","","Protocol","session initiation protocol for VoIP/IMS"),
    ("RTP",7,"UDP 16384-32767","","","Protocol","real-time transport protocol for audio/video"),
    ("RTCP",7,"UDP","","","Protocol","RTP control protocol for QoS feedback"),
    ("H.323",7,"TCP 1720","","","Protocol","ITU-T standard for multimedia conferencing"),
    ("MGCP",7,"UDP 2427","","","Protocol","media gateway control protocol"),
    ("SIGTRAN",7,"SCTP","","","Protocol","SS7 signaling transport over IP"),
    ("SCTP",7,"IP proto 132","","","Transport","stream control transmission protocol with multi-homing"),
    ("DCCP",7,"IP proto 33","","","Transport","datagram congestion control protocol"),
    ("QUIC",7,"UDP 443","","","Transport","quick UDP internet connections; HTTP/3 transport"),
    ("HTTP/2",7,"TCP 443","","","Application","HTTP/2 with multiplexing and server push"),
    ("HTTP/3",7,"UDP 443","","","Application","HTTP/3 over QUIC with improved performance"),
    ("WebSocket",7,"HTTP/1.1","","","Application","full-duplex communication over TCP upgrade"),
    ("SSE",7,"HTTP","","","Application","server-sent events for real-time streaming"),
    ("mDNS",7,"UDP 5353","","","Protocol","multicast DNS for zero-configuration networking"),
    ("DNS-SD",7,"mDNS","","","Protocol","DNS service discovery for zero-config"),
    ("LLMNR",7,"UDP 5355","","","Protocol","link-local multicast name resolution"),
    ("DHCPv6 PD",7,"UDP 546/547","","","Protocol","DHCPv6 prefix delegation for CPE addressing"),
    ("IPv6 RA",3,"ICMPv6","","","Protocol","IPv6 router advertisement for SLAAC"),
    ("IPv6 NDP",3,"ICMPv6 type 135/136","","","Protocol","IPv6 neighbor discovery protocol"),
    ("IPv6 SEND",3,"ICMPv6","","","Security","secure neighbor discovery for IPv6"),
    ("CGA",3,"IPv6","","","Security","cryptographically generated addresses for SEND"),
    ("SEcNeX",3,"IPv6","","","Security","secure neighbor discovery extension for SEND"),
    ("HIT",3,"IPv6","","","Protocol","host identity tag for HIP protocol"),
    ("HIP",3,"IP proto 139","","","Protocol","host identity protocol separating ID from locator"),
    ("LISP",3,"UDP 4341/4342","","","Overlay","locator/ID separation protocol for routing"),
    ("RANGI",3,"IPv6","","","Protocol","routing architecture for next-generation internet"),
    ("ILNP",3,"IPv6","","","Protocol","identifier-locator network protocol"),
    ("EID",3,"LISP","","","Protocol","endpoint identifier in LISP architecture"),
    ("RLOC",3,"LISP","","","Protocol","routing locator in LISP architecture"),
    ("MSDP",3,"TCP 639","","","Multicast","multicast source discovery protocol for inter-domain"),
    ("MBGP",7,"TCP 179","","","Multicast","multiprotocol BGP for multicast NLRI"),
    ("IGMP Proxy",3,"IP proto 2","","","Multicast","IGMP proxying for subscriber access"),
    ("MLD Proxy",3,"ICMPv6","","","Multicast","MLD proxying for IPv6 multicast access"),
    ("CGMP",3,"IP proto 2","","","Multicast","Cisco group management protocol for multicast"),
    ("RGMP",3,"IP proto 2","","","Multicast","router-port group management protocol"),
    ("PIM Dense",3,"IP proto 103","","","Multicast","PIM dense mode flood-and-prune multicast"),
    ("PIM Sparse",3,"IP proto 103","","","Multicast","PIM sparse mode with RP for receiver-driven"),
    ("PIM SSM",3,"IP proto 103","","","Multicast","PIM source-specific multicast with (S,G) channels"),
    ("PIM Bidir",3,"IP proto 103","","","Multicast","PIM bidirectional shared tree multicast"),
    ("PIM Anycast-RP",3,"IP proto 103","","","Multicast","PIM anycast RP with MSDP or BSR for RP redundancy"),
    ("PIM Reliable",3,"IP proto 103","","","Multicast","PIM reliable transport for register messages"),
    ("MSDP SA",3,"TCP 639","","","Multicast","MSDP source-active cache for active sources"),
    ("RPF",3,"N/A","","","Multicast","reverse path forwarding check for multicast"),
    ("Assert",3,"PIM","","","Multicast","PIM assert mechanism for duplicate forwarder election"),
    ("DF Election",3,"PIM","","","Multicast","designated forwarder election in PIM bidir"),
    ("BSR",3,"IP proto 103","","","Multicast","bootstrap router for RP distribution in PIM"),
    ("Auto-RP",3,"IP proto 2","","","Multicast","Cisco auto-RP for RP discovery and mapping"),
    ("Static RP",3,"Static","","","Multicast","statically configured RP for PIM domain"),
    ("Embedded RP",3,"IPv6","","","Multicast","IPv6 embedded RP in multicast address"),
    ("P2P",2,"Ethernet","","","Topology","point-to-point link topology"),
    ("P2MP",2,"Ethernet","","","Topology","point-to-multipoint link topology"),
    ("Hub-and-Spoke",2,"Various","","","Topology","hub-and-spoke topology with central hub router"),
    ("Full Mesh",2,"Various","","","Topology","fully meshed topology with all-to-all connections"),
    ("Partial Mesh",2,"Various","","","Topology","partially meshed topology with selective connections"),
    ("Clos",3,"ECMP","","","Data Center","Clos spine-leaf topology with predictable latency"),
    ("Fat Tree",2,"Ethernet","","","Data Center","fat tree topology with increasing bandwidth up the tree"),
    ("3-Tier",2,"Ethernet","","","Topology","three-tier hierarchical network design"),
    ("Collapsed Core",2,"Ethernet","","","Topology","two-tier network combining core and distribution"),
]'''

# Find the closing bracket of PROTOCOLS
# The PROTOCOLS list ends with a line containing just ']' after all protocol entries
insertion_point = None
# Find 'REP' last entry and insert after it
last_entry_line = None
lines = content.split('\n')
for i, line in enumerate(lines):
    if '"REP"' in line and 'Resilient Ethernet Protocol' in line:
        last_entry_line = i
        
if last_entry_line:
    # Insert after this line
    indent = ' ' * 4  # 4 spaces
    # Add the new entries
    new_lines = []
    for entry_line in proto_new.strip().split('\n'):
        if entry_line.strip():
            new_lines.append(indent + entry_line)
        else:
            new_lines.append('')
    insert_lines = [''] + new_lines
    for j, nl in enumerate(reversed(insert_lines)):
        lines.insert(last_entry_line + 1, nl)
    print(f"Added {len(new_lines)} entries to PROTOCOLS pool after line {last_entry_line+1}")
else:
    print("Could not find PROTOCOLS closing bracket")

content = '\n'.join(lines)

# ============================================================
# 2. EXPAND NETWORK_TERMS: 96 → 140 entries
# ============================================================
terms_new = '''
    ("Two-Way Active Measurement", "measuring network latency and jitter", "OAM"),
    ("Performance Monitoring", "collecting network performance data", "OAM"),
    ("Telemetry", "streaming operational data from network devices", "Automation"),
    ("Model-Driven Telemetry", "subscription-based data streaming using YANG models", "Automation"),
    ("gRPC Telemetry", "high-performance streaming using gRPC protocol", "Automation"),
    ("OpenTelemetry", "open standard for observability data collection", "Automation"),
    ("Prometheus", "time-series monitoring and alerting toolkit", "Automation"),
    ("Grafana", "multi-platform analytics and visualization platform", "Automation"),
    ("Elastic Stack", "ELK stack for log management and analytics", "Automation"),
    ("Splunk", "machine data analytics platform for IT operations", "Automation"),
    ("AI Ops", "artificial intelligence for IT operations", "Automation"),
    ("ML Ops", "machine learning operations for model lifecycle", "Automation"),
    ("Intent Based Networking", "declarative network management driven by business intent", "Automation"),
    ("Controller Based Networking", "centralized SDN controller for network automation", "Automation"),
    ("Cisco DNA Center", "SDN controller for intent-based campus network", "Automation"),
    ("Juniper Mist", "AI-driven cloud management platform for wired/wireless", "Automation"),
    ("Apstra", "intent-based networking for data center fabric", "Automation"),
    ("NSO", "Cisco network services orchestrator for multi-vendor", "Automation"),
    ("SaltStack", "event-driven automation for remote execution", "Automation"),
    ("AWX", "Red Hat Ansible Tower for enterprise automation", "Automation"),
    ("Terraform", "infrastructure as code for multi-cloud networking", "Automation"),
    ("Pulumi", "modern IaC with real programming languages", "Automation"),
    ("Crossplane", "Kubernetes-native control plane for infrastructure", "Automation"),
    ("Helm", "Kubernetes package manager for application deployment", "Automation"),
    ("Kustomize", "Kubernetes native configuration customization", "Automation"),
    ("Istio", "service mesh for microservices traffic management", "Automation"),
    ("Calico", "Kubernetes networking and security policy", "Automation"),
    ("Cilium", "eBPF-based networking for Kubernetes", "Automation"),
    ("eBPF", "extended Berkeley Packet Filter for kernel-level networking", "Automation"),
    ("XDP", "eXpress Data Path for high-performance packet processing", "Automation"),
    ("DPDK", "data plane development kit for fast packet processing", "Automation"),
    ("VPP", "vector packet processing for high-performance forwarding", "Automation"),
    ("FD.io", "fast data I/O project for universal dataplane", "Automation"),
    ("OVS", "Open vSwitch for virtual switch in hypervisors", "Automation"),
    ("OVN", "Open Virtual Network for OVS orchestration", "Automation"),
    ("Contrail", "Junipers SDN controller for multi-cloud networking", "Automation"),
    ("VMware NSX", "network virtualization platform for data center", "Automation"),
    ("Nuage", "Nokia SDN platform for data center networking", "Automation"),
    ("ACI", "Cisco Application Centric Infrastructure SDN", "Data Center"),
    ("ACI Fabric", "Cisco ACI spine-leaf fabric with APIC controller", "Data Center"),
    ("EPG", "endpoint group in ACI for policy-based networking", "Data Center"),
    ("BD", "bridge domain in ACI for Layer 2/3 forwarding", "Data Center"),
    ("VRF in ACI", "tenant VRF context in Cisco ACI fabric", "Data Center"),
    ("L3Out", "external routed connection from ACI fabric", "Data Center"),
    ("L2Out", "external bridged connection from ACI fabric", "Data Center"),
    ("VMM", "virtual machine manager integration in ACI", "Data Center"),
    ("OpFlex", "Cisco policy protocol for ACI endpoint groups", "Data Center"),
    ("Group Policy", "declarative group-based policy model for SDN", "Data Center"),
    ("Microsegmentation", "fine-grained security between workloads within same subnet", "Data Center"),
    ("Hairpin NAT", "NAT hairpinning for internal traffic through external IP", "NAT"),
    ("Twice NAT", "simultaneous source and destination NAT translation", "NAT"),
    ("NAT64", "IPv6 to IPv4 translation for dual-stack networks", "NAT"),
    ("NAT46", "IPv4 to IPv6 translation for IPv6-only networks", "NAT"),
    ("NPTv6", "Network Prefix Translation for IPv6 topology hiding", "NAT"),
    ("DNS64", "DNS rewriting for NAT64 IPv6 to IPv4 resolution", "NAT"),
    ("464XLAT", "double NAT64 for IPv6-only to IPv4 connectivity", "NAT"),
    ("MAP-T", "Mapping of Address and Port using translation", "NAT"),
    ("MAP-E", "Mapping of Address and Port using encapsulation", "NAT"),
    ("LW4o6", "Lightweight 4over6 tunneling for IPv4 in IPv6", "NAT"),
    ("DS-Lite", "Dual-Stack Lite for IPv4 over IPv6 tunneling", "NAT"),
    ("CGNAT", "Carrier-Grade NAT for large-scale address sharing", "NAT"),
    ("LSN", "Large-Scale NAT for ISP shared address deployment", "NAT"),
    ("Port Block Allocation", "assigning port blocks for CGNAT subscribers", "NAT"),
    ("Stateful NAT64", "NAT64 with stateful translation table", "NAT"),
    ("Stateless NAT64", "NAT64 with 1:1 stateless IP translation", "NAT"),
    ("BIER", "Bit Index Explicit Replication for multicast", "Multicast"),
    ("BIER-TE", "BIER with traffic engineering for explicit paths", "Multicast"),
    ("mCAST", "multicast with BGP and MPLS for MVPN", "Multicast"),
    ("MVPN", "multicast VPN with BGP auto-discovery", "Multicast"),
    ("NG-MVPN", "next-gen multicast VPN with BGP control plane", "Multicast"),
    ("mLDP", "multicast LDP for P2MP LSP signaling", "Multicast"),
    ("P2MP RSVP-TE", "Point-to-multipoint RSVP-TE for multicast transport", "Multicast"),
    ("P2MP LSP", "point-to-multipoint label-switched path", "Multicast"),
    ("BGP MVPN", "BGP-based multicast VPN with auto-discovery", "Multicast"),
]

# Find insertion point after the last NETWORK_TERMS entry (before closing ])
lines = content.split('\n')
last_terms_line = None
for i, line in enumerate(lines):
    if '"Port Block Allocation"' in line or '"LSN"' in line:
        last_terms_line = i

if not last_terms_line:
    for i, line in enumerate(lines):
        if '"BIER"' in line and 'multicast' in line:
            last_terms_line = i

if last_terms_line:
    indent = ' ' * 4
    new_lines = []
    for entry_line in terms_new.strip().split('\n'):
        if entry_line.strip():
            new_lines.append(indent + entry_line)
        else:
            new_lines.append('')
    insert_lines = [''] + new_lines
    for j, nl in enumerate(reversed(insert_lines)):
        lines.insert(last_terms_line + 1, nl)
    print(f"Added {len(new_lines)} entries to NETWORK_TERMS pool")
else:
    print("Could not find NETWORK_TERMS closing bracket")

content = '\n'.join(lines)

# ============================================================
# Write the modified file
# ============================================================
with open('scripts/generate_questions_v6.py', 'w') as f:
    f.write(content)

print("Done! Pools expanded.")
