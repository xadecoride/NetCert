export interface GuideSection {
  title: string;
  content: string;
  type: "text" | "code" | "command" | "note" | "tip" | "warning";
}

export interface TechnologyGuide {
  id: string;
  technology: string;
  title: string;
  level: string;
  track: string;
  summary: string;
  sections: GuideSection[];
}

export interface CommandRef {
  category: string;
  commands: { cmd: string; description: string }[];
}

export interface StudyContent {
  guides: TechnologyGuide[];
  quickReference: Record<string, CommandRef[]>;
  labels: {
    note: string;
    tip: string;
    warning: string;
  };
}

const enGuides: TechnologyGuide[] = [
  {
    id: "junos-cli",
    technology: "junos-cli",
    title: "JunOS CLI Basics",
    level: "JNCIA",
    track: "junos-ent",
    summary: "Navigate the JunOS CLI: operational vs configuration mode, show commands, and configuration management.",
    sections: [
      {
        title: "Operational Mode",
        type: "text",
        content:
          "When you log in to a JunOS device, you enter operational mode (prompt >). This is where you run show, ping, traceroute, and monitoring commands.",
      },
      {
        title: "Entering Configuration Mode",
        type: "command",
        content: "user@router> configure\nuser@router#",
      },
      {
        title: "Basic show Commands",
        type: "code",
        content: "show interfaces terse             # Brief interface info\nshow configuration                # Current configuration\nshow route                        # Routing table\nshow arp                          # ARP table\nshow log messages                 # System logs",
      },
      {
        title: "Configuration Management",
        type: "code",
        content: "show | compare                   # Show pending changes\ncommit                            # Apply changes\ncommit check                      # Validate without applying\nrollback 0                        # Roll back to previous\nrun show configuration            # Run a show command from config mode",
      },
      {
        title: "Tip",
        type: "tip",
        content: "Use `show configuration | display set` to view config as set commands — convenient for copy-paste into automation.",
      },
    ],
  },
  {
    id: "ospf",
    technology: "ospf",
    title: "OSPF Configuration Guide",
    level: "JNCIA",
    track: "junos-ent",
    summary: "Configure OSPFv2 on JunOS: areas, interfaces, passive interfaces, and neighbor verification.",
    sections: [
      {
        title: "Basic OSPF Configuration",
        type: "command",
        content: "set protocols ospf area 0 interface ge-0/0/0.0\nset protocols ospf area 0 interface ge-0/0/1.0\nset protocols ospf area 0 interface lo0.0 passive",
      },
      {
        title: "Verifying OSPF",
        type: "code",
        content: "show ospf neighbor                # Neighbors (State: Full/DOWN)\nshow ospf interface               # OSPF-enabled interfaces\nshow route protocol ospf          # Routes learned via OSPF\nshow ospf database                # LSDB\nshow ospf neighbor detail         # DR/BDR, Priority, Dead timer",
      },
      {
        title: "OSPF States",
        type: "text",
        content:
          "Down → Attempt → Init → 2-Way → ExStart → Exchange → Loading → Full.\n- Down: neighbor is unavailable\n- Init: Hello received, but neighbor does not see us\n- 2-Way: bidirectional communication (on broadcast networks — DR/BDR election)\n- ExStart: master/slave negotiation for DD packets\n- Exchange: LSA exchange\n- Loading: requesting missing LSAs\n- Full: full adjacency",
      },
      {
        title: "DR/BDR Election",
        type: "note",
        content: "On broadcast networks (Ethernet), a DR and BDR are elected. DR = highest priority (default 128), then highest Router ID. BDR = second highest priority. All others are DROther (2-Way).",
      },
      {
        title: "Troubleshooting",
        type: "warning",
        content: "If a neighbor does not come up:\n1. Check IP addresses (must be in the same subnet)\n2. Check MTU — must match on both sides\n3. Check firewall (ACL) — is OSPF (IP 89) blocked?\n4. Check area ID — must match\n5. `clear ospf neighbor` — restart adjacency",
      },
    ],
  },
  {
    id: "bgp",
    technology: "bgp",
    title: "BGP Configuration Guide",
    level: "JNCIP",
    track: "junos-ent",
    summary: "Configure EBGP and IBGP on JunOS: peer groups, policies, attributes, and verification.",
    sections: [
      {
        title: "EBGP Peering (External BGP)",
        type: "command",
        content: "set protocols bgp group EBGP type external\nset protocols bgp group EBGP peer-as 65002\nset protocols bgp group EBGP neighbor 10.0.12.2\nset protocols bgp group EBGP export EXPORT-DIRECT",
      },
      {
        title: "IBGP Peering (Internal BGP)",
        type: "command",
        content: "set protocols bgp group IBGP type internal\nset protocols bgp group IBGP local-address 1.1.1.1\nset protocols bgp group IBGP neighbor 2.2.2.2\nset protocols bgp group IBGP neighbor 3.3.3.3",
      },
      {
        title: "BGP Policy Example",
        type: "code",
        content: "policy-statement EXPORT-LOOPBACK {\n    term LOOPBACK {\n        from {\n            protocol direct;\n            route-filter 1.1.1.1/32 exact;\n        }\n        then accept;\n    }\n    then reject;\n}",
      },
      {
        title: "Verifying BGP",
        type: "code",
        content: "show bgp summary                   # Neighbors (Established/Active/Idle)\nshow bgp neighbor 10.0.12.2      # Adjacency details\nshow route protocol bgp          # BGP routes\nshow route advertising-protocol bgp 10.0.12.2  # What we advertise\nshow route receive-protocol bgp 10.0.12.2       # What we receive",
      },
      {
        title: "BGP States",
        type: "text",
        content:
          "Idle → Connect → Active → OpenSent → OpenConfirm → Established.\n- Idle: initial state\n- Connect: waiting for TCP connection (port 179)\n- Active: retrying TCP connection\n- OpenSent: OPEN sent\n- OpenConfirm: OPEN received, waiting for Keepalive\n- Established: BGP peering is up",
      },
      {
        title: "Important",
        type: "warning",
        content: "BGP does not advertise routes without an export policy! Even connected routes. Always create a policy-statement and reference it in export.",
      },
    ],
  },
  {
    id: "isis",
    technology: "isis",
    title: "IS-IS Configuration Guide",
    level: "JNCIP",
    track: "junos-ent",
    summary: "Configure IS-IS on JunOS: NET, level-1/level-2, adjacency, and verification.",
    sections: [
      {
        title: "Network Entity Title (NET)",
        type: "text",
        content:
          "NET = Area ID + System ID + N-Selector (00).\nFormat: XX.XXXX.XXXX.XXXX.XX\nExample: 49.0001.0010.0100.1001.00\n- 49.0001 — Area ID\n- 0010.0100.1001 — System ID (usually from MAC or loopback)\n- 00 — N-Selector (always 00 for routers)",
      },
      {
        title: "IS-IS Configuration",
        type: "command",
        content: "set interfaces lo0 unit 0 family iso address 49.0001.0010.0100.1001.00\nset interfaces ge-0/0/0 unit 0 family iso\nset protocols isis level 2\nset protocols isis interface ge-0/0/0.0\nset protocols isis interface lo0.0 passive",
      },
      {
        title: "Verifying IS-IS",
        type: "code",
        content: "show isis adjacency                 # Neighbors (Up/Down)\nshow isis adjacency detail         # DIS, Priority, Level\nshow isis database                 # LSPDB\nshow route protocol isis          # IS-IS routes\nshow isis hostname                 # Hostname → System ID mapping",
      },
      {
        title: "DIS Election",
        type: "note",
        content: "DIS (Designated IS) is the OSPF DR equivalent. Elected on broadcast segments by highest priority (default 64) and MAC. The DIS sends CSNP every 10 seconds.",
      },
    ],
  },
  {
    id: "mpls",
    technology: "mpls",
    title: "MPLS & LDP Guide",
    level: "JNCIP",
    track: "junos-ent",
    summary: "Configure MPLS and LDP: family mpls, MPLS interfaces, LSP verification, and labels.",
    sections: [
      {
        title: "Basic MPLS/LDP Configuration",
        type: "command",
        content: "# Enable MPLS on interfaces\nset interfaces ge-0/0/0 unit 0 family mpls\nset interfaces ge-0/0/1 unit 0 family mpls\n\n# Enable MPLS protocol\nset protocols mpls interface ge-0/0/0.0\nset protocols mpls interface ge-0/0/1.0\n\n# Enable LDP\nset protocols ldp interface ge-0/0/0.0\nset protocols ldp interface ge-0/0/1.0",
      },
      {
        title: "Verifying MPLS/LDP",
        type: "code",
        content: "show mpls lsp                       # LSPs (Ingress/Transit/Egress)\nshow mpls interface                # MPLS interfaces\nshow ldp session                   # LDP sessions\nshow ldp neighbor                  # LDP neighbors\nshow route table inet.3            # MPLS labels (inet.3)\nshow route 3.3.3.3                # Labeled path",
      },
      {
        title: "Label Operations",
        type: "text",
        content:
          "Ingress LSR: Push — adds a label\nTransit LSR: Swap — replaces the label\nEgress LSR: Pop — removes the label (PHP — Penultimate Hop Popping)\n\nLDP uses UDP 646 (discovery, multicast 224.0.0.2) and TCP 646 (session).",
      },
      {
        title: "Important",
        type: "tip",
        content: "Before MPLS/LDP, an IGP (OSPF or IS-IS) must be working. MPLS is built on top of IGP routes. Verify that all loopbacks are reachable via IGP before configuring MPLS.",
      },
    ],
  },
  {
    id: "vlan",
    technology: "junos-cli",
    title: "VLAN Configuration on JunOS",
    level: "JNCIA",
    track: "junos-ent",
    summary: "Configure VLANs on JunOS (EX series): tagged/untagged, IRB, and L3 interfaces.",
    sections: [
      {
        title: "VLAN Configuration (Access Port)",
        type: "command",
        content: "set vlans VLAN10 vlan-id 10\nset interfaces ge-0/0/0 unit 0 family ethernet-switching interface-mode access\nset interfaces ge-0/0/0 unit 0 family ethernet-switching vlan members VLAN10",
      },
      {
        title: "VLAN Configuration (Trunk Port)",
        type: "command",
        content: "set interfaces ge-0/0/1 unit 0 family ethernet-switching interface-mode trunk\nset interfaces ge-0/0/1 unit 0 family ethernet-switching vlan members [ VLAN10 VLAN20 ]",
      },
      {
        title: "IRB (L3 Interface)",
        type: "command",
        content: "set interfaces irb unit 10 family inet address 10.0.10.1/24\nset vlans VLAN10 l3-interface irb.10",
      },
      {
        title: "Verifying VLANs",
        type: "code",
        content: "show vlans                         # VLANs and ports\nshow ethernet-switching table      # MAC table\nshow interfaces irb                # IRB interfaces\nshow ethernet-switching interface  # Port status",
      },
    ],
  },
  {
    id: "firewall-filters",
    technology: "srx-policies",
    title: "Firewall Filters & Security Policies",
    level: "JNCIA",
    track: "junos-sec",
    summary: "Configure firewall filters and security policies on SRX: zones, policies, and screens.",
    sections: [
      {
        title: "Firewall Filter (Transit Traffic)",
        type: "command",
        content: "set firewall family inet filter PROTECT term ALLOW-ICMP from protocol icmp\nset firewall family inet filter PROTECT term ALLOW-ICMP then accept\nset firewall family inet filter PROTECT term REJECT then discard\nset interfaces lo0 unit 0 family inet filter input PROTECT",
      },
      {
        title: "Security Zones & Policies (SRX)",
        type: "command",
        content: "set security zones security-zone TRUST interfaces ge-0/0/0.0\nset security zones security-zone UNTRUST interfaces ge-0/0/1.0\n\nset security policies from-zone TRUST to-zone UNTRUST policy OUTBOUND\nset security policies from-zone TRUST to-zone UNTRUST policy OUTBOUND match source-address any\nset security policies from-zone TRUST to-zone UNTRUST policy OUTBOUND match destination-address any\nset security policies from-zone TRUST to-zone UNTRUST policy OUTBOUND match application any\nset security policies from-zone TRUST to-zone UNTRUST policy OUTBOUND then permit",
      },
      {
        title: "Screen (IDS/IPS)",
        type: "command",
        content: "set security screen ids-option UNTRUST-SCREEN icmp flood threshold 500\nset security screen ids-option UNTRUST-SCREEN tcp syn-flood alarm-threshold 1024\nset security screen ids-option UNTRUST-SCREEN tcp syn-flood attack-threshold 200\nset security zones security-zone UNTRUST screen UNTRUST-SCREEN",
      },
      {
        title: "Verification",
        type: "code",
        content: "show security policies              # Security policies\nshow security zones                 # Zones\nshow security flow session          # Active sessions\nshow security screen statistics     # Screen statistics\nshow log security                   # Security logs",
      },
    ],
  },
  {
    id: "evpn-vxlan",
    technology: "evpn-vxlan",
    title: "EVPN-VXLAN Guide",
    level: "JNCIP",
    track: "junos-dc",
    summary: "Configure EVPN-VXLAN on JunOS: route-distinguisher, route-target, VLAN-aware bundle, VXLAN encapsulation, and verification.",
    sections: [
      {
        title: "EVPN-VXLAN Concept",
        type: "text",
        content:
          "EVPN (Ethernet VPN) carries L2 traffic over an L3 network using BGP. VXLAN is an encapsulation using UDP (port 4789) to tunnel Ethernet frames. Together they replace traditional STP and VLAN trunking, enabling large data-center fabrics with multitenancy and anycast gateways.",
      },
      {
        title: "Basic EVPN Configuration on JunOS",
        type: "command",
        content: "# Enable IGP (OSPF/IS-IS) and BGP for Underlay\nset protocols bgp group UNDERLAY type internal\nset protocols bgp group UNDERLAY local-address 1.1.1.1\nset protocols bgp group UNDERLAY family inet unicast\nset protocols bgp group UNDERLAY neighbor 2.2.2.2\nset protocols bgp group UNDERLAY neighbor 3.3.3.3\n\n# Enable BGP EVPN\nset protocols bgp group EVPN type internal\nset protocols bgp group EVPN local-address 1.1.1.1\nset protocols bgp group EVPN family evpn signaling\nset protocols bgp group EVPN neighbor 2.2.2.2\nset protocols bgp group EVPN neighbor 3.3.3.3",
      },
      {
        title: "VXLAN and VLAN-aware Bundle Configuration",
        type: "command",
        content: "# Create switch-options for EVPN\nset switch-options route-distinguisher 1.1.1.1:100\nset switch-options vrf-target target:100:100\nset switch-options vrf-target auto\n\n# VLAN-aware bundle (VLAN-Bundle)\nset vlans VLAN100 vlan-id 100\nset vlans VLAN100 vxlan vni 10100\nset vlans VLAN100 vxlan ingress-node-replication\n\nset vlans VLAN200 vlan-id 200\nset vlans VLAN200 vxlan vni 10200\nset vlans VLAN200 vxlan ingress-node-replication\n\n# IRB (Anycast Gateway)\nset interfaces irb unit 100 family inet address 10.0.100.1/24\nset interfaces irb unit 100 virtual-gateway-accept-data\nset vlans VLAN100 l3-interface irb.100\n\nset interfaces irb unit 200 family inet address 10.0.200.1/24\nset interfaces irb unit 200 virtual-gateway-accept-data\nset vlans VLAN200 l3-interface irb.200",
      },
      {
        title: "Verifying EVPN-VXLAN",
        type: "code",
        content: "show evpn instance                       # EVPN instances (Type)\nshow evpn database                       # EVPN database (MAC/VNI)\nshow evpn l3-context                     # L3 context\nshow ethernet-switching table            # MAC table\nshow interfaces vxlan                    # VXLAN interfaces\nshow route table evpn.0                  # EVPN routes (Type-2, Type-3)\nshow route table inet.0 protocol evpn    # EVPN symmetric IRB\nshow bgp summary                         # BGP neighbors (EVPN family)",
      },
      {
        title: "EVPN Route Types",
        type: "text",
        content:
          "Type 1 — Ethernet Auto-Discovery (AD): PE discovery, duplicate MAC protection\nType 2 — MAC/IP Advertisement: MAC address advertisement (optionally with IP)\nType 3 — Inclusive Multicast Ethernet Tag: IMET, for BUM traffic\nType 4 — Ethernet Segment: for multi-homing (ESI)\nType 5 — IP Prefix: for L3 routes over EVPN (aka EVPN-Prefix)",
      },
      {
        title: "Tip",
        type: "tip",
        content: "Use `vrf-target auto` to automatically form RT from VNI — this simplifies configuration. For symmetric IRB (Type-5), you must specify the EVPN L3 context.",
      },
    ],
  },
  {
    id: "ipsec-vpn",
    technology: "srx-policies",
    title: "IPsec VPN Configuration Guide",
    level: "JNCIP",
    track: "junos-sec",
    summary: "Configure Site-to-Site IPsec VPN on SRX: IKE, IPsec proposal, security associations, and tunnel interface.",
    sections: [
      {
        title: "IPsec Concept on SRX",
        type: "text",
        content:
          "IPsec VPN on Juniper SRX consists of two phases:\n- Phase 1 (IKE): authentication and ISAKMP SA establishment\n- Phase 2 (Quick mode): IPsec SA negotiation and traffic encryption\n\nMain components:\n- IKE Proposal — encryption, authentication, DH group\n- IKE Policy — proposal binding, mode (main/aggressive), pre-shared key\n- IPsec Policy — transforms (ESP/AH, encryption, authentication)\n- IPsec VPN — IKE + IPsec + gateway binding\n- Secure Tunnel (st0.x) — virtual tunnel interface",
      },
      {
        title: "IKE Phase 1 Configuration",
        type: "command",
        content: "# IKE Proposal\nset security ike proposal IKE-PROP authentication-method pre-shared-keys\nset security ike proposal IKE-PROP dh-group group14\nset security ike proposal IKE-PROP authentication-algorithm sha-256\nset security ike proposal IKE-PROP encryption-algorithm aes-256-cbc\nset security ike proposal IKE-PROP lifetime-seconds 28800\n\n# IKE Policy\nset security ike policy IKE-POL mode main\nset security ike policy IKE-POL proposals IKE-PROP\nset security ike policy IKE-POL pre-shared-key ascii-text \"$trongK3y!\"\n\n# IKE Gateway\nset security ike gateway GW-REMOTE ike-policy IKE-POL\nset security ike gateway GW-REMOTE address 203.0.113.1\nset security ike gateway GW-REMOTE external-interface ge-0/0/1.0\nset security ike gateway GW-REMOTE version v2-only\nset security ike gateway GW-REMOTE local-address 198.51.100.1",
      },
      {
        title: "IPsec Phase 2 Configuration",
        type: "command",
        content: "# IPsec Proposal\nset security ipsec proposal IPSEC-PROP protocol esp\nset security ipsec proposal IPSEC-PROP authentication-algorithm hmac-sha-256-128\nset security ipsec proposal IPSEC-PROP encryption-algorithm aes-256-cbc\nset security ipsec proposal IPSEC-PROP lifetime-seconds 3600\n\n# IPsec Policy\nset security ipsec policy IPSEC-POL proposals IPSEC-PROP\n\n# IPsec VPN\nset security ipsec vpn VPN-TO-REMOTE bind-interface st0.100\nset security ipsec vpn VPN-TO-REMOTE ike gateway GW-REMOTE\nset security ipsec vpn VPN-TO-REMOTE ike ipsec-policy IPSEC-POL\nset security ipsec vpn VPN-TO-REMOTE establish-tunnels immediately",
      },
      {
        title: "Tunnel Interface and Security Policy",
        type: "command",
        content: "# Tunnel Interface\nset interfaces st0 unit 100 description \"VPN to Remote-Office\"\nset interfaces st0 unit 100 family inet address 10.0.1.1/30\n\n# Security Zone for VPN\nset security zones security-zone VPN-V4\nset security zones security-zone VPN-V4 interfaces st0.100\n\n# Security Policies (allow traffic through VPN)\nset security policies from-zone TRUST to-zone VPN-V4 policy VPN-OUT\nset security policies from-zone TRUST to-zone VPN-V4 policy VPN-OUT match source-address any\nset security policies from-zone TRUST to-zone VPN-V4 policy VPN-OUT match destination-address any\nset security policies from-zone TRUST to-zone VPN-V4 policy VPN-OUT match application any\nset security policies from-zone TRUST to-zone VPN-V4 policy VPN-OUT then permit\n\n# Route to remote subnet via st0\nset routing-options static route 10.0.2.0/24 next-hop 10.0.1.2",
      },
      {
        title: "Verifying IPsec VPN",
        type: "code",
        content: "show security ike security-associations    # IKE SA (UP/DOWN)\nshow security ipsec security-associations   # IPsec SA (UP/DOWN)\nshow security ike statistics                # IKE statistics\nshow security ipsec statistics              # IPsec statistics\nshow security flow session interface st0.100  # Sessions through tunnel\nshow security ipsec vpn                     # VPN status\nshow interfaces st0.100                     # Tunnel interface status\nshow security ipsec sa detail               # SA details (bytes, packets)",
      },
      {
        title: "IPsec Troubleshooting",
        type: "warning",
        content: "If the VPN does not come up:\n1. Check that external IPs are reachable (ping, traceroute)\n2. Check firewall — is UDP 500 (IKE), UDP 4500 (NAT-T), ESP (IP 50) blocked?\n3. Check that pre-shared keys match on both sides\n4. Check IKE proposal compatibility (encryption, DH group, auth algorithm)\n5. Enable `traceoptions security ike` for detailed logs\n6. Check that NAT does not break IPsec (NAT-T should activate automatically)",
      },
    ],
  },
  {
    id: "vrf",
    technology: "bgp",
    title: "VRF & MPLS L3VPN Guide",
    level: "JNCIP",
    track: "junos-sp",
    summary: "Configure VRF and MPLS L3VPN on JunOS: route-distinguisher, route-target, VRF tables, and BGP VPNv4.",
    sections: [
      {
        title: "VRF Concept",
        type: "text",
        content:
          "VRF (Virtual Routing and Forwarding) is a virtual routing table. Each VRF has:\n- Its own RIB (Routing Information Base) — Customer VPN table\n- Route Distinguisher (RD) — makes routes unique globally\n- Route Target (RT) — BGP extended community for import/export\n- Its own interfaces (Customer Edge attachment)\n\nMPLS L3VPN uses BGP to carry VPNv4 routes between PE routers.",
      },
      {
        title: "VRF Configuration on JunOS",
        type: "command",
        content: "# Create VRF (CUSTOMER-A)\nset routing-instances CUSTOMER-A instance-type vrf\nset routing-instances CUSTOMER-A interface ge-0/0/0.100\nset routing-instances CUSTOMER-A interface ge-0/0/1.100\nset routing-instances CUSTOMER-A route-distinguisher 1.1.1.1:100\nset routing-instances CUSTOMER-A vrf-target target:65000:100\n\n# VRF with different RT for import/export\nset routing-instances CUSTOMER-B instance-type vrf\nset routing-instances CUSTOMER-B interface ge-0/0/2.200\nset routing-instances CUSTOMER-B route-distinguisher 1.1.1.1:200\nset routing-instances CUSTOMER-B vrf-import IMPORT-CUST-B\nset routing-instances CUSTOMER-B vrf-export EXPORT-CUST-B\n\n# BGP in VRF for CE-PE\nset routing-instances CUSTOMER-A protocols bgp group CE type external\nset routing-instances CUSTOMER-A protocols bgp group CE peer-as 65100\nset routing-instances CUSTOMER-A protocols bgp group CE local-as 65000\nset routing-instances CUSTOMER-A protocols bgp group CE neighbor 10.100.1.2\n\n# Or static route in VRF\nset routing-instances CUSTOMER-A routing-options static route 10.100.0.0/16 next-hop 10.100.1.2",
      },
      {
        title: "BGP VPNv4 (Between PEs)",
        type: "command",
        content: "# VPNv4 BGP (on each PE)\nset protocols bgp group VPN type internal\nset protocols bgp group VPN local-address 1.1.1.1\nset protocols bgp group VPN family inet-vpn unicast\nset protocols bgp group VPN family inet6-vpn unicast\nset protocols bgp group VPN neighbor 2.2.2.2\nset protocols bgp group VPN neighbor 3.3.3.3\n\n# Route Target Policy (optional)\nset policy-options community CUST-A-IMPORT members target:65000:100\nset policy-options community CUST-A-EXPORT members target:65000:100\n\npolicy-statement VPN-IMPORT {\n    term A {\n        from community CUST-A-IMPORT;\n        then accept;\n    }\n    then reject;\n}",
      },
      {
        title: "Verifying VRF and L3VPN",
        type: "code",
        content: "show route instance                   # All VRF instances\nshow route instance CUSTOMER-A        # VRF details\nshow route table CUSTOMER-A.inet.0     # VRF table\nshow route table bgp.l3vpn.0          # Global VPNv4 table\nshow route table CUSTOMER-A.inet.0 protocol bgp  # BGP routes in VRF\nshow bgp summary                      # BGP neighbors (regular + VPNv4)\nping routing-instance CUSTOMER-A 10.100.1.2   # Ping from VRF",
      },
      {
        title: "Important",
        type: "note",
        content: "For MPLS L3VPN, IGP reachability between PE loopbacks, configured MPLS/LDP, and the `inet-vpn unicast` family in BGP are mandatory. JunOS automatically creates the `bgp.l3vpn.0` table when the family is added to BGP.",
      },
    ],
  },
  {
    id: "bgp-lu",
    technology: "bgp",
    title: "BGP Labeled Unicast Guide",
    level: "JNCIP",
    track: "junos-sp",
    summary: "Configure BGP Labeled Unicast (BGP-LU): BGP labels, inter-AS MPLS, and SR-MPLS segment routing.",
    sections: [
      {
        title: "BGP-LU Concept",
        type: "text",
        content:
          "BGP Labeled Unicast (BGP-LU, RFC 8277) is a technology where BGP distributes routes along with MPLS labels. Unlike LDP, labels are carried with NLRI in BGP UPDATE. BGP-LU is used:\n- For MPLS in Inter-AS Option C (BGP-free core)\n- As an alternative to LDP/RSVP\n- In Segment Routing (SR-MPLS) with BGP Prefix-SID\n- For label-unicast on ASBR/PE",
      },
      {
        title: "BGP-LU Configuration on JunOS",
        type: "command",
        content: "# Enable inet-labeled-unicast family\nset protocols bgp group BGP-LU type internal\nset protocols bgp group BGP-LU local-address 1.1.1.1\nset protocols bgp group BGP-LU family inet-labeled-unicast rib inet.3\nset protocols bgp group BGP-LU neighbor 2.2.2.2\nset protocols bgp group BGP-LU neighbor 3.3.3.3\n\n# BGP-LU for EBGP (inter-AS Option C)\nset protocols bgp group EBGP-LU type external\nset protocols bgp group EBGP-LU family inet-labeled-unicast\nset protocols bgp group EBGP-LU peer-as 65002\nset protocols bgp group EBGP-LU export EXPORT-BGP-LU\nset protocols bgp group EBGP-LU neighbor 10.0.12.2",
      },
      {
        title: "Export Policy for BGP-LU",
        type: "code",
        content: "policy-statement EXPORT-BGP-LU {\n    term LOOPBACK {\n        from {\n            protocol direct;\n            route-filter 1.1.1.1/32 exact;\n        }\n        then {\n            community add NO-EXPORT;\n            accept;\n        }\n    }\n    then reject;\n}",
      },
      {
        title: "Verifying BGP-LU",
        type: "code",
        content: "show bgp summary                        # Neighbors (inet-labeled-unicast)\nshow route protocol bgp table inet.3   # BGP-LU labels in inet.3\nshow route table inet.3                # MPLS Label table\nshow bgp neighbor 2.2.2.2              # BGP-LU details (received prefixes)\nshow route 3.3.3.3 detail             # Path with label\nshow mpls lsp                          # MPLS LSP",
      },
      {
        title: "Tip",
        type: "tip",
        content: "Specify `rib inet.3` when configuring BGP-LU so labels are written to inet.3 (MPLS table), not inet.0. This allows MPLS forwarding to work correctly. If labels do not appear, check that the next-hop is reachable via IGP.",
      },
    ],
  },
  {
    id: "multicast",
    technology: "multicast",
    title: "Multicast Guide (PIM-SM & IGMP)",
    level: "JNCIP",
    track: "junos-ent",
    summary: "Configure multicast on JunOS: PIM-SM, IGMP/MLD, RP, rendezvous point, and group membership.",
    sections: [
      {
        title: "Multicast Concept on JunOS",
        type: "text",
        content:
          "Multicast — traffic delivery from one source to a group of receivers using a group address.\n\nJunOS main components:\n- IGMP (Internet Group Management Protocol) — receiver-side group subscription\n- PIM (Protocol Independent Multicast) — builds (S,G) and (*,G) trees\n- PIM-SM (Sparse Mode) — RP-based, tree is built toward RP\n- PIM-SSM (Source-Specific Multicast) — (S,G) without RP, with IGMPv3\n- RP (Rendezvous Point) — central point for PIM-SM\n- MSDP — active-source exchange between RPs of different domains",
      },
      {
        title: "IGMP Configuration",
        type: "command",
        content: "# Enable IGMP on receiver-facing interface\nset protocols igmp interface ge-0/0/1.0\nset protocols igmp interface ge-0/0/1.0 version 3\nset protocols igmp interface ge-0/0/2.0\n\n# IGMP Static Join (for testing)\nset protocols igmp interface ge-0/0/2.0 static group 239.0.1.1\n\n# IGMP Snooping (switching part)\nset vlans VLAN100 igmp-snooping",
      },
      {
        title: "PIM-SM Configuration",
        type: "command",
        content: "# Enable PIM on interfaces\nset protocols pim interface lo0.0\nset protocols pim interface ge-0/0/0.0\nset protocols pim interface ge-0/0/1.0 mode sparse\nset protocols pim interface ge-0/0/2.0 mode sparse\n\n# Static RP\nset protocols pim rp static address 1.1.1.1\nset protocols pim rp static address 1.1.1.1 group-rp ff00::/8\nset protocols pim rp static address 2.2.2.2 group-rp 239.0.0.0/8\n\n# Bootstrap RP (BSR — dynamic RP)\nset protocols pim rp local address 1.1.1.1\nset protocols pim rp local group-ranges 224.0.0.0/4\nset protocols pim bsr-candidate interface lo0.0 priority 200\nset protocols pim rp-candidate interface lo0.0",
      },
      {
        title: "Verifying Multicast",
        type: "code",
        content: "show pim neighbors                     # PIM neighbors (Up/Down)\nshow pim interfaces                    # PIM interfaces\nshow pim rp                             # RP information\nshow pim join                           # (S,G) and (*,G) joins\nshow multicast route                    # Multicast routing table\nshow igmp groups                       # IGMP groups\nshow igmp interface                    # IGMP interfaces\nping multicast 239.0.1.1               # Multicast ping",
      },
      {
        title: "(S,G) vs (*,G)",
        type: "text",
        content:
          "(S,G) — Source-Specific Tree (SPT). Path from source to receivers, optimal route.\n(*,G) — Shared Tree (RPT). Tree through RP: \"from any source to group G, via RP\".\n\nPIM-SM: receiver sends (*,G) Join to RP. RP receives traffic from source via (S,G) registration. After the first packet, the last hop may switch to (S,G) SPT.\n\nPIM-SSM: only (S,G), no RP, with IGMPv3 — receiver explicitly specifies source.",
      },
      {
        title: "Troubleshooting",
        type: "warning",
        content: "If multicast does not work:\n1. Check that PIM neighbors are Up: `show pim neighbors`\n2. Check RP: `show pim rp` — RP must be active\n3. Check RP reachability: ping to RP\n4. Check that IGP is routing (not BGP) — PIM does not work over EBGP without configuration\n5. Check firewall — is IGMP (IP 2) and PIM (IP 103) blocked?\n6. Check TTL of multicast packets (must be >= number of hops)\n7. Enable `traceoptions pim` for detailed logging",
      },
    ],
  },
];

const enQuickReference: Record<string, CommandRef[]> = {
  "junos-ent": [
    {
      category: "System",
      commands: [
        { cmd: "show version", description: "JunOS version" },
        { cmd: "show system uptime", description: "System uptime" },
        { cmd: "show system storage", description: "Disk usage" },
        { cmd: "show system processes extensive", description: "Processes" },
        { cmd: "request system reboot", description: "Reboot" },
      ],
    },
    {
      category: "Interfaces",
      commands: [
        { cmd: "show interfaces terse", description: "Brief interface summary" },
        { cmd: "show interfaces ge-0/0/0 extensive", description: "Interface details" },
        { cmd: "show interfaces diagnostics optics ge-0/0/0", description: "Optics (SFP)" },
        { cmd: "monitor interface traffic", description: "Real-time traffic" },
        { cmd: "show configuration interfaces", description: "Interface config" },
      ],
    },
    {
      category: "Routing",
      commands: [
        { cmd: "show route", description: "Routing table" },
        { cmd: "show route protocol ospf", description: "OSPF routes" },
        { cmd: "show route protocol bgp", description: "BGP routes" },
        { cmd: "show route 10.0.0.0/8", description: "Route lookup" },
        { cmd: "show route table inet.3", description: "MPLS labels (inet.3)" },
        { cmd: "show route forwarding-table", description: "FIB" },
      ],
    },
    {
      category: "OSPF",
      commands: [
        { cmd: "show ospf neighbor", description: "OSPF neighbors" },
        { cmd: "show ospf interface", description: "OSPF interfaces" },
        { cmd: "show ospf database", description: "LSDB" },
        { cmd: "show ospf statistics", description: "OSPF statistics" },
        { cmd: "clear ospf neighbor", description: "Reset adjacency" },
      ],
    },
    {
      category: "BGP",
      commands: [
        { cmd: "show bgp summary", description: "BGP neighbors" },
        { cmd: "show bgp neighbor 10.0.12.2", description: "Adjacency details" },
        { cmd: "show route advertising-protocol bgp 10.0.12.2", description: "Advertised" },
        { cmd: "show route receive-protocol bgp 10.0.12.2", description: "Received" },
        { cmd: "clear bgp neighbor 10.0.12.2", description: "Reset adjacency" },
      ],
    },
    {
      category: "IS-IS",
      commands: [
        { cmd: "show isis adjacency", description: "IS-IS neighbors" },
        { cmd: "show isis database", description: "LSDB" },
        { cmd: "show isis hostname", description: "Hostname map" },
        { cmd: "show isis spf log", description: "SPF logs" },
      ],
    },
    {
      category: "MPLS/LDP",
      commands: [
        { cmd: "show mpls lsp", description: "MPLS LSP" },
        { cmd: "show mpls interface", description: "MPLS interfaces" },
        { cmd: "show ldp session", description: "LDP sessions" },
        { cmd: "show ldp database", description: "LDP label database" },
      ],
    },
    {
      category: "Multicast",
      commands: [
        { cmd: "show pim neighbors", description: "PIM neighbors" },
        { cmd: "show pim rp", description: "RP information" },
        { cmd: "show pim join", description: "(S,G) and (*,G) joins" },
        { cmd: "show multicast route", description: "Multicast routing table" },
        { cmd: "show igmp groups", description: "IGMP groups" },
        { cmd: "ping multicast 239.0.1.1", description: "Multicast ping" },
      ],
    },
  ],
  "junos-sp": [
    {
      category: "MPLS",
      commands: [
        { cmd: "show mpls lsp", description: "LSP" },
        { cmd: "show mpls lsp name LSP-PE1-PE2", description: "LSP by name" },
        { cmd: "show mpls lsp statistics", description: "LSP statistics" },
        { cmd: "show mpls path", description: "MPLS paths (RSVP)" },
        { cmd: "show rsvp session", description: "RSVP sessions" },
      ],
    },
    {
      category: "MPLS L3VPN",
      commands: [
        { cmd: "show route table VPN-A.inet.0", description: "VRF table" },
        { cmd: "show route instance CUSTOMER-A", description: "VRF details" },
        { cmd: "show route protocol bgp table bgp.l3vpn.0", description: "VPNv4 routes" },
        { cmd: "ping routing-instance CUSTOMER-A 10.0.0.1", description: "Ping from VRF" },
      ],
    },
    {
      category: "BGP-LU (Labeled Unicast)",
      commands: [
        { cmd: "show route protocol bgp table inet.3", description: "BGP-LU labels" },
        { cmd: "show route table inet.3", description: "MPLS Label table" },
        { cmd: "show bgp neighbor 2.2.2.2", description: "BGP-LU details" },
        { cmd: "show mpls lsp", description: "MPLS LSP" },
      ],
    },
  ],
  "junos-sec": [
    {
      category: "Security Policies",
      commands: [
        { cmd: "show security policies", description: "All policies" },
        { cmd: "show security policies from-zone TRUST to-zone UNTRUST", description: "Inter-zone policies" },
        { cmd: "show security zones", description: "Security zones" },
        { cmd: "show security zones terse", description: "Zones summary" },
      ],
    },
    {
      category: "Sessions & NAT",
      commands: [
        { cmd: "show security flow session", description: "Active sessions" },
        { cmd: "show security flow session summary", description: "Session summary" },
        { cmd: "show security nat source", description: "Source NAT" },
        { cmd: "show security nat destination", description: "Destination NAT" },
        { cmd: "clear security flow session", description: "Clear all sessions" },
      ],
    },
    {
      category: "IPsec VPN",
      commands: [
        { cmd: "show security ike security-associations", description: "IKE SA (UP/DOWN)" },
        { cmd: "show security ipsec security-associations", description: "IPsec SA (UP/DOWN)" },
        { cmd: "show security ipsec vpn", description: "VPN status" },
        { cmd: "show security flow session interface st0.100", description: "Sessions through tunnel" },
        { cmd: "clear security ike security-associations", description: "Reset IKE SA" },
      ],
    },
  ],
  "junos-dc": [
    {
      category: "EVPN/VXLAN",
      commands: [
        { cmd: "show evpn instance", description: "EVPN instances" },
        { cmd: "show evpn database", description: "EVPN database (MAC/VNI)" },
        { cmd: "show evpn l3-context", description: "L3 context" },
        { cmd: "show ethernet-switching table", description: "MAC table" },
        { cmd: "show interfaces vxlan", description: "VXLAN interfaces" },
        { cmd: "show route table evpn.0", description: "EVPN routes (Type-2/3/5)" },
        { cmd: "show route table inet.0 protocol evpn", description: "EVPN symmetric IRB" },
      ],
    },
    {
      category: "LAG/MC-LAG",
      commands: [
        { cmd: "show lacp interfaces", description: "LACP" },
        { cmd: "show lacp statistics interfaces ae0", description: "LACP statistics" },
        { cmd: "show interfaces ae0", description: "AE interface" },
        { cmd: "show configuration interfaces ae0", description: "AE config" },
      ],
    },
  ],
  "junos-aut": [
    {
      category: "PyEZ",
      commands: [
        { cmd: "from jnpr.junos import Device", description: "Import Device" },
        { cmd: "dev = Device(host='10.0.0.1', user='admin')", description: "Connect" },
        { cmd: "dev.open()", description: "Open connection" },
        { cmd: "dev.facts['hostname']", description: "Device facts" },
        { cmd: "dev.rpc.get_interface_information()", description: "RPC call" },
        { cmd: "dev.close()", description: "Close connection" },
      ],
    },
    {
      category: "Ansible",
      commands: [
        { cmd: "ansible-playbook -i inventory deploy.yml", description: "Run playbook" },
        { cmd: "ansible all -m juniper_junos_command -a \"commands='show version'\"", description: "Run command" },
        { cmd: "ansible all -m juniper_junos_config -a \"src=config.conf\"", description: "Apply config" },
        { cmd: "ansible-inventory -i inventory --list", description: "Check inventory" },
      ],
    },
  ],
};

// Russian content mirrors the original study page content.
const ruGuides: TechnologyGuide[] = [
  {
    id: "junos-cli",
    technology: "junos-cli",
    title: "JunOS CLI Basics",
    level: "JNCIA",
    track: "junos-ent",
    summary: "Навигация по JunOS CLI: operational vs configuration mode, команды show, управление конфигурацией.",
    sections: [
      {
        title: "Operational Mode",
        type: "text",
        content:
          "При входе на устройство JunOS вы попадаете в operational mode (приглашение >). Здесь выполняются команды show, ping, traceroute, мониторинг.",
      },
      {
        title: "Переход в Configuration Mode",
        type: "command",
        content: "user@router> configure\nuser@router#",
      },
      {
        title: "Базовые show-команды",
        type: "code",
        content: "show interfaces terse             # Краткая информация об интерфейсах\nshow configuration                # Текущая конфигурация\nshow route                        # Таблица маршрутизации\nshow arp                          # ARP-таблица\nshow log messages                 # Системные логи",
      },
      {
        title: "Управление конфигурацией",
        type: "code",
        content: "show | compare                   # Показать изменения\ncommit                            # Применить изменения\ncommit check                      # Проверить без применения\nrollback 0                        # Откатить до предыдущей\nrun show configuration            # Из конфигурационного режима",
      },
      {
        title: "Совет",
        type: "tip",
        content: "Используйте `show configuration | display set` для отображения конфигурации в формате set-команд — это удобно для copy-paste в автоматизации.",
      },
    ],
  },
  {
    id: "ospf",
    technology: "ospf",
    title: "OSPF Configuration Guide",
    level: "JNCIA",
    track: "junos-ent",
    summary: "Настройка OSPFv2 на JunOS: area, интерфейсы, пассивные интерфейсы, проверка соседства.",
    sections: [
      {
        title: "Базовая настройка OSPF",
        type: "command",
        content: "set protocols ospf area 0 interface ge-0/0/0.0\nset protocols ospf area 0 interface ge-0/0/1.0\nset protocols ospf area 0 interface lo0.0 passive",
      },
      {
        title: "Проверка OSPF",
        type: "code",
        content: "show ospf neighbor                # Соседи (State: Full/DOWN)\nshow ospf interface               # OSPF-интерфейсы\nshow route protocol ospf          # Маршруты, полученные по OSPF\nshow ospf database                # LSDB\nshow ospf neighbor detail         # DR/BDR, Priority, Dead timer",
      },
      {
        title: "OSPF States",
        type: "text",
        content:
          "Down → Attempt → Init → 2-Way → ExStart → Exchange → Loading → Full.\n- Down: сосед недоступен\n- Init: получен Hello, но сосед не видит нас\n- 2-Way: двухсторонняя связь (на broadcast — выбор DR/BDR)\n- ExStart: мастер/слейв, DD-пакеты\n- Exchange: обмен LSA\n- Loading: запрос недостающих LSA\n- Full: полная смежность",
      },
      {
        title: "DR/BDR Election",
        type: "note",
        content: "На broadcast-сетях (Ethernet) выбирается DR и BDR. DR = highest priority (по умолчанию 128), затем highest Router ID. BDR = второй по приоритету. Все остальные — DROther (2-Way).",
      },
      {
        title: "Траблшутинг",
        type: "warning",
        content: "Если сосед не поднимается:\n1. Проверьте IP-адреса (должны быть в одной подсети)\n2. Проверьте MTU — должен совпадать на обоих сторонах\n3. Проверьте firewall (ACL) — не блокирует ли OSPF (IP 89)\n4. Проверьте area ID — должен совпадать\n5. `clear ospf neighbor` — перезапустить соседство",
      },
    ],
  },
  {
    id: "bgp",
    technology: "bgp",
    title: "BGP Configuration Guide",
    level: "JNCIP",
    track: "junos-ent",
    summary: "Настройка EBGP и IBGP на JunOS: peer groups, policy, атрибуты, проверка.",
    sections: [
      {
        title: "EBGP Peering (External BGP)",
        type: "command",
        content: "set protocols bgp group EBGP type external\nset protocols bgp group EBGP peer-as 65002\nset protocols bgp group EBGP neighbor 10.0.12.2\nset protocols bgp group EBGP export EXPORT-DIRECT",
      },
      {
        title: "IBGP Peering (Internal BGP)",
        type: "command",
        content: "set protocols bgp group IBGP type internal\nset protocols bgp group IBGP local-address 1.1.1.1\nset protocols bgp group IBGP neighbor 2.2.2.2\nset protocols bgp group IBGP neighbor 3.3.3.3",
      },
      {
        title: "BGP Policy Example",
        type: "code",
        content: "policy-statement EXPORT-LOOPBACK {\n    term LOOPBACK {\n        from {\n            protocol direct;\n            route-filter 1.1.1.1/32 exact;\n        }\n        then accept;\n    }\n    then reject;\n}",
      },
      {
        title: "Проверка BGP",
        type: "code",
        content: "show bgp summary                   # Соседи (Established/Active/Idle)\nshow bgp neighbor 10.0.12.2      # Детали соседства\nshow route protocol bgp          # BGP-маршруты\nshow route advertising-protocol bgp 10.0.12.2  # Что анонсируем\nshow route receive-protocol bgp 10.0.12.2       # Что получаем",
      },
      {
        title: "BGP States",
        type: "text",
        content:
          "Idle → Connect → Active → OpenSent → OpenConfirm → Established.\n- Idle: начальное состояние\n- Connect: ожидание TCP-соединения (порт 179)\n- Active: повтор TCP-соединения\n- OpenSent: отправлен OPEN\n- OpenConfirm: получен OPEN, ожидание Keepalive\n- Established: BGP-соседство установлено",
      },
      {
        title: "Важно",
        type: "warning",
        content: "BGP не анонсирует маршруты без export policy! Даже connected маршруты. Всегда создавайте policy-statement и указывайте его в export.",
      },
    ],
  },
  {
    id: "isis",
    technology: "isis",
    title: "IS-IS Configuration Guide",
    level: "JNCIP",
    track: "junos-ent",
    summary: "Настройка IS-IS на JunOS: NET, level-1/level-2, adjacency, проверка.",
    sections: [
      {
        title: "Network Entity Title (NET)",
        type: "text",
        content:
          "NET = Area ID + System ID + N-Selector (00).\nФормат: XX.XXXX.XXXX.XXXX.XX\nПример: 49.0001.0010.0100.1001.00\n- 49.0001 — Area ID\n- 0010.0100.1001 — System ID (обычно из MAC или loopback)\n- 00 — N-Selector (всегда 00 для routers)",
      },
      {
        title: "Настройка IS-IS",
        type: "command",
        content: "set interfaces lo0 unit 0 family iso address 49.0001.0010.0100.1001.00\nset interfaces ge-0/0/0 unit 0 family iso\nset protocols isis level 2\nset protocols isis interface ge-0/0/0.0\nset protocols isis interface lo0.0 passive",
      },
      {
        title: "Проверка IS-IS",
        type: "code",
        content: "show isis adjacency                 # Соседи (Up/Down)\nshow isis adjacency detail         # DIS, Priority, Level\nshow isis database                 # LSPDB\nshow route protocol isis          # Маршруты IS-IS\nshow isis hostname                 # Карта hostname → System ID",
      },
      {
        title: "DIS Election",
        type: "note",
        content: "DIS (Designated IS) — аналог DR в OSPF. Выбирается на broadcast-сегментах по highest priority (по умолч. 64) и MAC. DIS отправляет CSNP каждые 10 секунд.",
      },
    ],
  },
  {
    id: "mpls",
    technology: "mpls",
    title: "MPLS & LDP Guide",
    level: "JNCIP",
    track: "junos-ent",
    summary: "Настройка MPLS и LDP: family mpls, MPLS-интерфейсы, проверка LSP и меток.",
    sections: [
      {
        title: "Базовая настройка MPLS/LDP",
        type: "command",
        content: "# Включить MPLS на интерфейсах\nset interfaces ge-0/0/0 unit 0 family mpls\nset interfaces ge-0/0/1 unit 0 family mpls\n\n# Включить MPLS протокол\nset protocols mpls interface ge-0/0/0.0\nset protocols mpls interface ge-0/0/1.0\n\n# Включить LDP\nset protocols ldp interface ge-0/0/0.0\nset protocols ldp interface ge-0/0/1.0",
      },
      {
        title: "Проверка MPLS/LDP",
        type: "code",
        content: "show mpls lsp                       # LSP (Ingress/Transit/Egress)\nshow mpls interface                # MPLS-интерфейсы\nshow ldp session                   # LDP-сессии\nshow ldp neighbor                  # LDP-соседи\nshow route table inet.3            # MPLS-метки (inet.3)\nshow route 3.3.3.3                # Путь с меткой",
      },
      {
        title: "Label Operations",
        type: "text",
        content:
          "Ingress LSR: Push — добавляет метку\nTransit LSR: Swap — заменяет метку\nEgress LSR: Pop — удаляет метку (PHP — Penultimate Hop Popping)\n\nLDP использует UDP 646 (discovery, multicast 224.0.0.2) и TCP 646 (session).",
      },
      {
        title: "Важно",
        type: "tip",
        content: "Перед MPLS/LDP должен работать IGP (OSPF или IS-IS). MPLS строится поверх IGP-маршрутов. Проверьте, что все loopback достижимы через IGP, прежде чем настраивать MPLS.",
      },
    ],
  },
  {
    id: "vlan",
    technology: "junos-cli",
    title: "VLAN Configuration on JunOS",
    level: "JNCIA",
    track: "junos-ent",
    summary: "Настройка VLAN на JunOS (EX-серия): tagged/untagged, IRB, L3-интерфейсы.",
    sections: [
      {
        title: "Настройка VLAN (Access Port)",
        type: "command",
        content: "set vlans VLAN10 vlan-id 10\nset interfaces ge-0/0/0 unit 0 family ethernet-switching interface-mode access\nset interfaces ge-0/0/0 unit 0 family ethernet-switching vlan members VLAN10",
      },
      {
        title: "Настройка VLAN (Trunk Port)",
        type: "command",
        content: "set interfaces ge-0/0/1 unit 0 family ethernet-switching interface-mode trunk\nset interfaces ge-0/0/1 unit 0 family ethernet-switching vlan members [ VLAN10 VLAN20 ]",
      },
      {
        title: "IRB (L3 Interface)",
        type: "command",
        content: "set interfaces irb unit 10 family inet address 10.0.10.1/24\nset vlans VLAN10 l3-interface irb.10",
      },
      {
        title: "Проверка VLAN",
        type: "code",
        content: "show vlans                         # VLANs и порты\nshow ethernet-switching table      # MAC-таблица\nshow interfaces irb                # IRB-интерфейсы\nshow ethernet-switching interface  # Статус портов",
      },
    ],
  },
  {
    id: "firewall-filters",
    technology: "srx-policies",
    title: "Firewall Filters & Security Policies",
    level: "JNCIA",
    track: "junos-sec",
    summary: "Настройка firewall filter и security policies на SRX: zones, policies, screens.",
    sections: [
      {
        title: "Firewall Filter (на транзитный трафик)",
        type: "command",
        content: "set firewall family inet filter PROTECT term ALLOW-ICMP from protocol icmp\nset firewall family inet filter PROTECT term ALLOW-ICMP then accept\nset firewall family inet filter PROTECT term REJECT then discard\nset interfaces lo0 unit 0 family inet filter input PROTECT",
      },
      {
        title: "Security Zones & Policies (SRX)",
        type: "command",
        content: "set security zones security-zone TRUST interfaces ge-0/0/0.0\nset security zones security-zone UNTRUST interfaces ge-0/0/1.0\n\nset security policies from-zone TRUST to-zone UNTRUST policy OUTBOUND\nset security policies from-zone TRUST to-zone UNTRUST policy OUTBOUND match source-address any\nset security policies from-zone TRUST to-zone UNTRUST policy OUTBOUND match destination-address any\nset security policies from-zone TRUST to-zone UNTRUST policy OUTBOUND match application any\nset security policies from-zone TRUST to-zone UNTRUST policy OUTBOUND then permit",
      },
      {
        title: "Screen (IDS/IPS)",
        type: "command",
        content: "set security screen ids-option UNTRUST-SCREEN icmp flood threshold 500\nset security screen ids-option UNTRUST-SCREEN tcp syn-flood alarm-threshold 1024\nset security screen ids-option UNTRUST-SCREEN tcp syn-flood attack-threshold 200\nset security zones security-zone UNTRUST screen UNTRUST-SCREEN",
      },
      {
        title: "Проверка",
        type: "code",
        content: "show security policies              # Политики безопасности\nshow security zones                 # Зоны\nshow security flow session          # Активные сессии\nshow security screen statistics     # Screen-статистика\nshow log security                   # Security-логи",
      },
    ],
  },
  {
    id: "evpn-vxlan",
    technology: "evpn-vxlan",
    title: "EVPN-VXLAN Guide",
    level: "JNCIP",
    track: "junos-dc",
    summary: "Настройка EVPN-VXLAN на JunOS: route-distinguisher, route-target, VLAN-aware bundle, VXLAN encapsulation, проверка.",
    sections: [
      {
        title: "Концепция EVPN-VXLAN",
        type: "text",
        content:
          "EVPN (Ethernet VPN) — это технология для передачи L2-трафика через L3-сеть с помощью BGP. VXLAN — инкапсуляция, использующая UDP (порт 4789) для туннелирования Ethernet-кадров. Вместе они заменяют традиционные STP и VLAN Trunking, позволяя строить гигантские Data Center fabrics с мульти-арендой и anycast-шлюзами.",
      },
      {
        title: "Базовая настройка EVPN на JunOS",
        type: "command",
        content: "# Включить IGP (OSPF/IS-IS) и BGP для Underlay\nset protocols bgp group UNDERLAY type internal\nset protocols bgp group UNDERLAY local-address 1.1.1.1\nset protocols bgp group UNDERLAY family inet unicast\nset protocols bgp group UNDERLAY neighbor 2.2.2.2\nset protocols bgp group UNDERLAY neighbor 3.3.3.3\n\n# Включить BGP EVPN\nset protocols bgp group EVPN type internal\nset protocols bgp group EVPN local-address 1.1.1.1\nset protocols bgp group EVPN family evpn signaling\nset protocols bgp group EVPN neighbor 2.2.2.2\nset protocols bgp group EVPN neighbor 3.3.3.3",
      },
      {
        title: "Настройка VXLAN и VLAN-aware Bundle",
        type: "command",
        content: "# Создать switch-options для EVPN\nset switch-options route-distinguisher 1.1.1.1:100\nset switch-options vrf-target target:100:100\nset switch-options vrf-target auto\n\n# VLAN-aware bundle (VLAN-Bundle)\nset vlans VLAN100 vlan-id 100\nset vlans VLAN100 vxlan vni 10100\nset vlans VLAN100 vxlan ingress-node-replication\n\nset vlans VLAN200 vlan-id 200\nset vlans VLAN200 vxlan vni 10200\nset vlans VLAN200 vxlan ingress-node-replication\n\n# IRB (Anycast Gateway)\nset interfaces irb unit 100 family inet address 10.0.100.1/24\nset interfaces irb unit 100 virtual-gateway-accept-data\nset vlans VLAN100 l3-interface irb.100\n\nset interfaces irb unit 200 family inet address 10.0.200.1/24\nset interfaces irb unit 200 virtual-gateway-accept-data\nset vlans VLAN200 l3-interface irb.200",
      },
      {
        title: "Проверка EVPN-VXLAN",
        type: "code",
        content: "show evpn instance                       # EVPN-инстансы (Type)\nshow evpn database                       # EVPN-база (MAC/VNI)\nshow evpn l3-context                     # L3-контекст\nshow ethernet-switching table            # MAC-таблица\nshow interfaces vxlan                    # VXLAN-интерфейсы\nshow route table evpn.0                  # EVPN-маршруты (Type-2, Type-3)\nshow route table inet.0 protocol evpn    # EVPN-симметричный IRB\nshow bgp summary                         # BGP-соседи (EVPN family)",
      },
      {
        title: "EVPN Route Types",
        type: "text",
        content:
          "Type 1 — Ethernet Auto-Discovery (AD): обнаружение PE, защита от дублей MAC\nType 2 — MAC/IP Advertisement: анонс MAC-адреса (опционально с IP)\nType 3 — Inclusive Multicast Ethernet Tag: IMET, для BUM-трафика\nType 4 — Ethernet Segment: для multi-homing (ESI)\nType 5 — IP Prefix: для передачи L3-маршрутов поверх EVPN (aka EVPN-Prefix)",
      },
      {
        title: "Совет",
        type: "tip",
        content: "Используйте `vrf-target auto` для автоматического формирования RT по VNI — это упрощает конфигурацию. Для симметричного IRB (Type-5) нужно указывать L3-контекст EVPN.",
      },
    ],
  },
  {
    id: "ipsec-vpn",
    technology: "srx-policies",
    title: "IPsec VPN Configuration Guide",
    level: "JNCIP",
    track: "junos-sec",
    summary: "Настройка Site-to-Site IPsec VPN на SRX: IKE, IPsec proposal, security associations, tunnel interface.",
    sections: [
      {
        title: "Концепция IPsec на SRX",
        type: "text",
        content:
          "IPsec VPN на Juniper SRX состоит из двух фаз:\n- Phase 1 (IKE): аутентификация и установка ISAKMP SA\n- Phase 2 (Quick mode): согласование IPsec SA и шифрование трафика\n\nОсновные компоненты:\n- IKE Proposal — шифрование, аутентификация, DH-группа\n- IKE Policy — привязка proposal, режим (main/aggressive), pre-shared key\n- IPsec Policy — transforms (ESP/AH, шифрование, аутентификация)\n- IPsec VPN — связка IKE + IPsec + gateway\n- Secure Tunnel (st0.x) — виртуальный туннельный интерфейс",
      },
      {
        title: "Настройка IKE Phase 1",
        type: "command",
        content: "# IKE Proposal\nset security ike proposal IKE-PROP authentication-method pre-shared-keys\nset security ike proposal IKE-PROP dh-group group14\nset security ike proposal IKE-PROP authentication-algorithm sha-256\nset security ike proposal IKE-PROP encryption-algorithm aes-256-cbc\nset security ike proposal IKE-PROP lifetime-seconds 28800\n\n# IKE Policy\nset security ike policy IKE-POL mode main\nset security ike policy IKE-POL proposals IKE-PROP\nset security ike policy IKE-POL pre-shared-key ascii-text \"$trongK3y!\"\n\n# IKE Gateway\nset security ike gateway GW-REMOTE ike-policy IKE-POL\nset security ike gateway GW-REMOTE address 203.0.113.1\nset security ike gateway GW-REMOTE external-interface ge-0/0/1.0\nset security ike gateway GW-REMOTE version v2-only\nset security ike gateway GW-REMOTE local-address 198.51.100.1",
      },
      {
        title: "Настройка IPsec Phase 2",
        type: "command",
        content: "# IPsec Proposal\nset security ipsec proposal IPSEC-PROP protocol esp\nset security ipsec proposal IPSEC-PROP authentication-algorithm hmac-sha-256-128\nset security ipsec proposal IPSEC-PROP encryption-algorithm aes-256-cbc\nset security ipsec proposal IPSEC-PROP lifetime-seconds 3600\n\n# IPsec Policy\nset security ipsec policy IPSEC-POL proposals IPSEC-PROP\n\n# IPsec VPN\nset security ipsec vpn VPN-TO-REMOTE bind-interface st0.100\nset security ipsec vpn VPN-TO-REMOTE ike gateway GW-REMOTE\nset security ipsec vpn VPN-TO-REMOTE ike ipsec-policy IPSEC-POL\nset security ipsec vpn VPN-TO-REMOTE establish-tunnels immediately",
      },
      {
        title: "Tunnel Interface и Security Policy",
        type: "command",
        content: "# Tunnel Interface\nset interfaces st0 unit 100 description \"VPN to Remote-Office\"\nset interfaces st0 unit 100 family inet address 10.0.1.1/30\n\n# Security Zone для VPN\nset security zones security-zone VPN-V4\nset security zones security-zone VPN-V4 interfaces st0.100\n\n# Security Policies (разрешаем трафик через VPN)\nset security policies from-zone TRUST to-zone VPN-V4 policy VPN-OUT\nset security policies from-zone TRUST to-zone VPN-V4 policy VPN-OUT match source-address any\nset security policies from-zone TRUST to-zone VPN-V4 policy VPN-OUT match destination-address any\nset security policies from-zone TRUST to-zone VPN-V4 policy VPN-OUT match application any\nset security policies from-zone TRUST to-zone VPN-V4 policy VPN-OUT then permit\n\n# Route to remote subnet через st0\nset routing-options static route 10.0.2.0/24 next-hop 10.0.1.2",
      },
      {
        title: "Проверка IPsec VPN",
        type: "code",
        content: "show security ike security-associations    # IKE SA (UP/DOWN)\nshow security ipsec security-associations   # IPsec SA (UP/DOWN)\nshow security ike statistics                # IKE-статистика\nshow security ipsec statistics              # IPsec-статистика\nshow security flow session interface st0.100  # Сессии через туннель\nshow security ipsec vpn                     # VPN-статус\nshow interfaces st0.100                     # Статус tunnel-интерфейса\nshow security ipsec sa detail               # Детали SA (bytes, packets)",
      },
      {
        title: "Траблшутинг IPsec",
        type: "warning",
        content: "Если VPN не встаёт:\n1. Проверьте, что внешние IP доступны (ping, traceroute)\n2. Проверьте firewall — не блокирует ли UDP 500 (IKE), UDP 4500 (NAT-T), ESP (IP 50)\n3. Проверьте, что pre-shared key совпадают на обоих сторонах\n4. Проверьте IKE proposal на совместимость (шифрование, DH-группа, auth-алгоритм)\n5. Включите `traceoptions security ike` для детального лога\n6. Проверьте, что NAT не сбивает IPsec (NAT-T должен включиться автоматически)",
      },
    ],
  },
  {
    id: "vrf",
    technology: "bgp",
    title: "VRF & MPLS L3VPN Guide",
    level: "JNCIP",
    track: "junos-sp",
    summary: "Настройка VRF и MPLS L3VPN на JunOS: route-distinguisher, route-target, VRF-таблицы, BGP VPNv4.",
    sections: [
      {
        title: "Концепция VRF",
        type: "text",
        content:
          "VRF (Virtual Routing and Forwarding) — виртуальная таблица маршрутизации. Каждый VRF имеет:\n- Свой RIB (Routing Information Base) — Customer VPN-таблица\n- Route Distinguisher (RD) — делает маршруты уникальными в глобальной таблице\n- Route Target (RT) — BGP extended community для импорта/экспорта\n- Свои интерфейсы (Customer Edge attachment)\n\nMPLS L3VPN использует BGP для передачи VPNv4-маршрутов между PE-роутерами.",
      },
      {
        title: "Настройка VRF на JunOS",
        type: "command",
        content: "# Создание VRF (CUSTOMER-A)\nset routing-instances CUSTOMER-A instance-type vrf\nset routing-instances CUSTOMER-A interface ge-0/0/0.100\nset routing-instances CUSTOMER-A interface ge-0/0/1.100\nset routing-instances CUSTOMER-A route-distinguisher 1.1.1.1:100\nset routing-instances CUSTOMER-A vrf-target target:65000:100\n\n# VRF с разными RT для импорта/экспорта\nset routing-instances CUSTOMER-B instance-type vrf\nset routing-instances CUSTOMER-B interface ge-0/0/2.200\nset routing-instances CUSTOMER-B route-distinguisher 1.1.1.1:200\nset routing-instances CUSTOMER-B vrf-import IMPORT-CUST-B\nset routing-instances CUSTOMER-B vrf-export EXPORT-CUST-B\n\n# BGP в VRF для CE-PE\nset routing-instances CUSTOMER-A protocols bgp group CE type external\nset routing-instances CUSTOMER-A protocols bgp group CE peer-as 65100\nset routing-instances CUSTOMER-A protocols bgp group CE local-as 65000\nset routing-instances CUSTOMER-A protocols bgp group CE neighbor 10.100.1.2\n\n# Или статический маршрут в VRF\nset routing-instances CUSTOMER-A routing-options static route 10.100.0.0/16 next-hop 10.100.1.2",
      },
      {
        title: "BGP VPNv4 (для передачи между PE)",
        type: "command",
        content: "# VPNv4 BGP (на каждом PE)\nset protocols bgp group VPN type internal\nset protocols bgp group VPN local-address 1.1.1.1\nset protocols bgp group VPN family inet-vpn unicast\nset protocols bgp group VPN family inet6-vpn unicast\nset protocols bgp group VPN neighbor 2.2.2.2\nset protocols bgp group VPN neighbor 3.3.3.3\n\n# Route Target Policy (опционально)\nset policy-options community CUST-A-IMPORT members target:65000:100\nset policy-options community CUST-A-EXPORT members target:65000:100\n\npolicy-statement VPN-IMPORT {\n    term A {\n        from community CUST-A-IMPORT;\n        then accept;\n    }\n    then reject;\n}",
      },
      {
        title: "Проверка VRF и L3VPN",
        type: "code",
        content: "show route instance                   # Все VRF-инстансы\nshow route instance CUSTOMER-A        # Детали VRF\nshow route table CUSTOMER-A.inet.0     # VRF-таблица\nshow route table bgp.l3vpn.0          # Глобальная VPNv4-таблица\nshow route table CUSTOMER-A.inet.0 protocol bgp  # BGP-маршруты в VRF\nshow bgp summary                      # BGP-соседи (обычные + VPNv4)\nping routing-instance CUSTOMER-A 10.100.1.2   # Ping из VRF",
      },
      {
        title: "Важно",
        type: "note",
        content: "Для работы MPLS L3VPN обязательна IGP reachability между loopback PE-роутеров, настроенный MPLS/LDP и семейство `inet-vpn unicast` в BGP. JunOS автоматически создаёт таблицу `bgp.l3vpn.0` при включении семейства к BGP.",
      },
    ],
  },
  {
    id: "bgp-lu",
    technology: "bgp",
    title: "BGP Labeled Unicast Guide",
    level: "JNCIP",
    track: "junos-sp",
    summary: "Настройка BGP Labeled Unicast (BGP-LU): BGP-метки, inter-AS MPLS, сегментная маршрутизация SR-MPLS.",
    sections: [
      {
        title: "Концепция BGP-LU",
        type: "text",
        content:
          "BGP Labeled Unicast (BGP-LU, RFC 8277) — технология, при которой BGP распространяет не только маршруты, но и MPLS-метки. В отличие от LDP, метки передаются вместе с NLRI в BGP UPDATE. BGP-LU используется:\n- Для MPLS в Inter-AS Option C (BGP-free core)\n- Как альтернатива LDP/RSVP\n- В Segment Routing (SR-MPLS) с BGP Prefix-SID\n- Для label-unicast на ASBR/PE",
      },
      {
        title: "Настройка BGP-LU на JunOS",
        type: "command",
        content: "# Включить семейство inet-labeled-unicast\nset protocols bgp group BGP-LU type internal\nset protocols bgp group BGP-LU local-address 1.1.1.1\nset protocols bgp group BGP-LU family inet-labeled-unicast rib inet.3\nset protocols bgp group BGP-LU neighbor 2.2.2.2\nset protocols bgp group BGP-LU neighbor 3.3.3.3\n\n# BGP-LU для EBGP (inter-AS Option C)\nset protocols bgp group EBGP-LU type external\nset protocols bgp group EBGP-LU family inet-labeled-unicast\nset protocols bgp group EBGP-LU peer-as 65002\nset protocols bgp group EBGP-LU export EXPORT-BGP-LU\nset protocols bgp group EBGP-LU neighbor 10.0.12.2",
      },
      {
        title: "Export Policy для BGP-LU",
        type: "code",
        content: "policy-statement EXPORT-BGP-LU {\n    term LOOPBACK {\n        from {\n            protocol direct;\n            route-filter 1.1.1.1/32 exact;\n        }\n        then {\n            community add NO-EXPORT;\n            accept;\n        }\n    }\n    then reject;\n}",
      },
      {
        title: "Проверка BGP-LU",
        type: "code",
        content: "show bgp summary                        # Соседи (inet-labeled-unicast)\nshow route protocol bgp table inet.3   # BGP-LU метки в inet.3\nshow route table inet.3                # MPLS Label table\nshow bgp neighbor 2.2.2.2              # Детали BGP-LU (received prefixes)\nshow route 3.3.3.3 detail             # Путь с меткой\nshow mpls lsp                          # MPLS LSP",
      },
      {
        title: "Совет",
        type: "tip",
        content: "Указывайте `rib inet.3` при настройке BGP-LU, чтобы метки записывались в inet.3 (MPLS-таблица), а не в inet.0. Это позволяет MPLS-коммутации работать корректно. Если метки не появляются — проверьте, что next-hop достижим через IGP.",
      },
    ],
  },
  {
    id: "multicast",
    technology: "multicast",
    title: "Multicast Guide (PIM-SM & IGMP)",
    level: "JNCIP",
    track: "junos-ent",
    summary: "Настройка мультикаста на JunOS: PIM-SM, IGMP/MLD, RP, rendezvous point, group membership.",
    sections: [
      {
        title: "Концепция Multicast на JunOS",
        type: "text",
        content:
          "Multicast — передача трафика от одного источника (Source) группе получателей (Receivers) через групповой адрес.\n\nОсновные компоненты JunOS:\n- IGMP (Internet Group Management Protocol) — на стороне получателя, подписка на группу\n- PIM (Protocol Independent Multicast) — построение (S,G) и (*,G) деревьев\n- PIM-SM (Sparse Mode) — RP-based, дерево строится от RP\n- PIM-SSM (Source-Specific Multicast) — (S,G) без RP, с IGMPv3\n- RP (Rendezvous Point) — центральная точка для PIM-SM\n- MSDP — обмен информацией об active sources между RP разных доменов",
      },
      {
        title: "Настройка IGMP",
        type: "command",
        content: "# Включить IGMP на интерфейсе к получателям\nset protocols igmp interface ge-0/0/1.0\nset protocols igmp interface ge-0/0/1.0 version 3\nset protocols igmp interface ge-0/0/2.0\n\n# IGMP Static Join (для тестирования)\nset protocols igmp interface ge-0/0/2.0 static group 239.0.1.1\n\n# IGMP Snooping (в свитчевой части)\nset vlans VLAN100 igmp-snooping",
      },
      {
        title: "Настройка PIM-SM",
        type: "command",
        content: "# Включить PIM на интерфейсах\nset protocols pim interface lo0.0\nset protocols pim interface ge-0/0/0.0\nset protocols pim interface ge-0/0/1.0 mode sparse\nset protocols pim interface ge-0/0/2.0 mode sparse\n\n# Static RP\nset protocols pim rp static address 1.1.1.1\nset protocols pim rp static address 1.1.1.1 group-rp ff00::/8\nset protocols pim rp static address 2.2.2.2 group-rp 239.0.0.0/8\n\n# Bootstrap RP (BSR — динамический RP)\nset protocols pim rp local address 1.1.1.1\nset protocols pim rp local group-ranges 224.0.0.0/4\nset protocols pim bsr-candidate interface lo0.0 priority 200\nset protocols pim rp-candidate interface lo0.0",
      },
      {
        title: "Проверка Multicast",
        type: "code",
        content: "show pim neighbors                     # PIM-соседи (Up/Down)\nshow pim interfaces                    # PIM-интерфейсы\nshow pim rp                             # RP-информация\nshow pim join                           # (S,G) и (*,G) join-состояния\nshow multicast route                    # Multicast routing table\nshow igmp groups                       # IGMP-группы\nshow igmp interface                    # IGMP-интерфейсы\nping multicast 239.0.1.1               # Мультикаст ping",
      },
      {
        title: "(S,G) vs (*,G)",
        type: "text",
        content:
          "(S,G) — Source-Specific Tree (SPT). Путь от источника к получателям, оптимальный маршрут.\n(*,G) — Shared Tree (RPT). Дерево через RP: \"от любого источника к группе G, через RP\".\n\nPIM-SM: получатель отправляет (*,G) Join к RP. RP получает трафик от источника по (S,G) регистрации. После первого пакета последний хоп может переключиться на (S,G) SPT (switchover).\n\nPIM-SSM: только (S,G), без RP, с IGMPv3 — получатель явно указывает источник.",
      },
      {
        title: "Траблшутинг",
        type: "warning",
        content: "Если мультикаст не работает:\n1. Проверьте, что PIM соседства Up: `show pim neighbors`\n2. Проверьте RP: `show pim rp` — RP должен быть active\n3. Проверьте RP reachability: ping до RP\n4. Проверьте, что IGP маршрутирует (не BGP) — PIM не работает поверх EBGP без настройки\n5. Проверьте firewall — не блокирует ли IGMP (IP 2) и PIM (IP 103)\n6. Проверьте TTL multicast-пакетов (должен быть >= количество хопов)\n7. Включите `traceoptions pim` для детального логирования",
      },
    ],
  },
];

const ruQuickReference: Record<string, CommandRef[]> = {
  "junos-ent": [
    {
      category: "System",
      commands: [
        { cmd: "show version", description: "Версия JunOS" },
        { cmd: "show system uptime", description: "Аптайм системы" },
        { cmd: "show system storage", description: "Использование диска" },
        { cmd: "show system processes extensive", description: "Процессы" },
        { cmd: "request system reboot", description: "Перезагрузка" },
      ],
    },
    {
      category: "Interfaces",
      commands: [
        { cmd: "show interfaces terse", description: "Кратко по всем интерфейсам" },
        { cmd: "show interfaces ge-0/0/0 extensive", description: "Детально по интерфейсу" },
        { cmd: "show interfaces diagnostics optics ge-0/0/0", description: "Оптика (SFP)" },
        { cmd: "monitor interface traffic", description: "Трафик в реальном времени" },
        { cmd: "show configuration interfaces", description: "Конфиг интерфейсов" },
      ],
    },
    {
      category: "Routing",
      commands: [
        { cmd: "show route", description: "Таблица маршрутизации" },
        { cmd: "show route protocol ospf", description: "OSPF-маршруты" },
        { cmd: "show route protocol bgp", description: "BGP-маршруты" },
        { cmd: "show route 10.0.0.0/8", description: "Поиск маршрута" },
        { cmd: "show route table inet.3", description: "MPLS-метки (inet.3)" },
        { cmd: "show route forwarding-table", description: "FIB" },
      ],
    },
    {
      category: "OSPF",
      commands: [
        { cmd: "show ospf neighbor", description: "OSPF-соседи" },
        { cmd: "show ospf interface", description: "OSPF-интерфейсы" },
        { cmd: "show ospf database", description: "LSDB" },
        { cmd: "show ospf statistics", description: "Статистика OSPF" },
        { cmd: "clear ospf neighbor", description: "Сброс соседства" },
      ],
    },
    {
      category: "BGP",
      commands: [
        { cmd: "show bgp summary", description: "BGP-соседи" },
        { cmd: "show bgp neighbor 10.0.12.2", description: "Детали соседства" },
        { cmd: "show route advertising-protocol bgp 10.0.12.2", description: "Анонсы" },
        { cmd: "show route receive-protocol bgp 10.0.12.2", description: "Полученные" },
        { cmd: "clear bgp neighbor 10.0.12.2", description: "Сброс соседства" },
      ],
    },
    {
      category: "IS-IS",
      commands: [
        { cmd: "show isis adjacency", description: "IS-IS соседи" },
        { cmd: "show isis database", description: "LSDB" },
        { cmd: "show isis hostname", description: "Карта hostname" },
        { cmd: "show isis spf log", description: "SPF-логи" },
      ],
    },
    {
      category: "MPLS/LDP",
      commands: [
        { cmd: "show mpls lsp", description: "MPLS LSP" },
        { cmd: "show mpls interface", description: "MPLS-интерфейсы" },
        { cmd: "show ldp session", description: "LDP-сессии" },
        { cmd: "show ldp database", description: "LDP-база меток" },
      ],
    },
    {
      category: "Multicast",
      commands: [
        { cmd: "show pim neighbors", description: "PIM-соседи" },
        { cmd: "show pim rp", description: "RP-информация" },
        { cmd: "show pim join", description: "(S,G) и (*,G) join" },
        { cmd: "show multicast route", description: "Multicast routing table" },
        { cmd: "show igmp groups", description: "IGMP-группы" },
        { cmd: "ping multicast 239.0.1.1", description: "Мультикаст ping" },
      ],
    },
  ],
  "junos-sp": [
    {
      category: "MPLS",
      commands: [
        { cmd: "show mpls lsp", description: "LSP" },
        { cmd: "show mpls lsp name LSP-PE1-PE2", description: "LSP по имени" },
        { cmd: "show mpls lsp statistics", description: "Статистика LSP" },
        { cmd: "show mpls path", description: "MPLS-пути (для RSVP)" },
        { cmd: "show rsvp session", description: "RSVP-сессии" },
      ],
    },
    {
      category: "MPLS L3VPN",
      commands: [
        { cmd: "show route table VPN-A.inet.0", description: "VRF-таблица" },
        { cmd: "show route instance CUSTOMER-A", description: "Детали VRF" },
        { cmd: "show route protocol bgp table bgp.l3vpn.0", description: "VPNv4-маршруты" },
        { cmd: "ping routing-instance CUSTOMER-A 10.0.0.1", description: "Ping из VRF" },
      ],
    },
    {
      category: "BGP-LU (Labeled Unicast)",
      commands: [
        { cmd: "show route protocol bgp table inet.3", description: "BGP-LU метки" },
        { cmd: "show route table inet.3", description: "MPLS Label table" },
        { cmd: "show bgp neighbor 2.2.2.2", description: "Детали BGP-LU" },
        { cmd: "show mpls lsp", description: "MPLS LSP" },
      ],
    },
  ],
  "junos-sec": [
    {
      category: "Security Policies",
      commands: [
        { cmd: "show security policies", description: "Все политики" },
        { cmd: "show security policies from-zone TRUST to-zone UNTRUST", description: "Политики между зонами" },
        { cmd: "show security zones", description: "Зоны безопасности" },
        { cmd: "show security zones terse", description: "Зоны кратко" },
      ],
    },
    {
      category: "Sessions & NAT",
      commands: [
        { cmd: "show security flow session", description: "Активные сессии" },
        { cmd: "show security flow session summary", description: "Кратко по сессиям" },
        { cmd: "show security nat source", description: "Source NAT" },
        { cmd: "show security nat destination", description: "Destination NAT" },
        { cmd: "clear security flow session", description: "Сброс всех сессий" },
      ],
    },
    {
      category: "IPsec VPN",
      commands: [
        { cmd: "show security ike security-associations", description: "IKE SA (UP/DOWN)" },
        { cmd: "show security ipsec security-associations", description: "IPsec SA (UP/DOWN)" },
        { cmd: "show security ipsec vpn", description: "VPN-статус" },
        { cmd: "show security flow session interface st0.100", description: "Сессии через туннель" },
        { cmd: "clear security ike security-associations", description: "Сброс IKE SA" },
      ],
    },
  ],
  "junos-dc": [
    {
      category: "EVPN/VXLAN",
      commands: [
        { cmd: "show evpn instance", description: "EVPN-инстансы" },
        { cmd: "show evpn database", description: "EVPN-база (MAC/VNI)" },
        { cmd: "show evpn l3-context", description: "L3-контекст" },
        { cmd: "show ethernet-switching table", description: "MAC-таблица" },
        { cmd: "show interfaces vxlan", description: "VXLAN-интерфейсы" },
        { cmd: "show route table evpn.0", description: "EVPN-маршруты (Type-2/3/5)" },
        { cmd: "show route table inet.0 protocol evpn", description: "EVPN-симметричный IRB" },
      ],
    },
    {
      category: "LAG/MC-LAG",
      commands: [
        { cmd: "show lacp interfaces", description: "LACP" },
        { cmd: "show lacp statistics interfaces ae0", description: "LACP-статистика" },
        { cmd: "show interfaces ae0", description: "AE-интерфейс" },
        { cmd: "show configuration interfaces ae0", description: "Конфиг агрегации" },
      ],
    },
  ],
  "junos-aut": [
    {
      category: "PyEZ",
      commands: [
        { cmd: "from jnpr.junos import Device", description: "Импорт Device" },
        { cmd: "dev = Device(host='10.0.0.1', user='admin')", description: "Подключение" },
        { cmd: "dev.open()", description: "Открыть соединение" },
        { cmd: "dev.facts['hostname']", description: "Факты об устройстве" },
        { cmd: "dev.rpc.get_interface_information()", description: "RPC-вызов" },
        { cmd: "dev.close()", description: "Закрыть соединение" },
      ],
    },
    {
      category: "Ansible",
      commands: [
        { cmd: "ansible-playbook -i inventory deploy.yml", description: "Запуск playbook" },
        { cmd: "ansible all -m juniper_junos_command -a \"commands='show version'\"", description: "Выполнить команду" },
        { cmd: "ansible all -m juniper_junos_config -a \"src=config.conf\"", description: "Применить конфиг" },
        { cmd: "ansible-inventory -i inventory --list", description: "Проверить inventory" },
      ],
    },
  ],
};

export const studyEn: StudyContent = {
  guides: enGuides,
  quickReference: enQuickReference,
  labels: { note: "Note", tip: "Tip", warning: "Warning" },
};

export const studyRu: StudyContent = {
  guides: ruGuides,
  quickReference: ruQuickReference,
  labels: { note: "Примечание", tip: "Совет", warning: "Внимание" },
};
