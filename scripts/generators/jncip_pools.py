"""Content pools for JNCIP-ENT and JNCIP-SP question generation."""

JNCIP_ENT_SECTIONS = {
    "1.0 IGP": ("1.0 IGP", 10.0),
    "1.1 OSPF": ("1.0 IGP", 10.0),
    "1.2 IS-IS": ("1.0 IGP", 10.0),
    "2.0 BGP": ("2.0 BGP", 15.0),
    "2.1 BGP basics": ("2.0 BGP", 15.0),
    "2.2 BGP attributes": ("2.0 BGP", 15.0),
    "2.3 BGP scaling": ("2.0 BGP", 15.0),
    "3.0 IP Multicast": ("3.0 IP Multicast", 10.0),
    "4.0 Ethernet Switching": ("4.0 Ethernet Switching", 10.0),
    "5.0 CoS": ("5.0 CoS", 10.0),
    "6.0 EVPN": ("6.0 EVPN", 10.0),
    "7.0 Layer 3 VPN": ("7.0 Layer 3 VPN", 10.0),
    "8.0 Layer 2 VPN": ("8.0 Layer 2 VPN", 10.0),
    "9.0 High Availability": ("9.0 High Availability", 5.0),
}

JNCIP_SP_SECTIONS = {
    "1.0 OSPF": ("1.0 OSPF", 15.0),
    "2.0 IS-IS": ("2.0 IS-IS", 15.0),
    "3.0 BGP": ("3.0 BGP", 15.0),
    "4.0 MPLS": ("4.0 MPLS", 15.0),
    "5.0 L3VPN": ("5.0 L3VPN", 15.0),
    "6.0 L2VPN": ("6.0 L2VPN", 10.0),
    "7.0 Multicast": ("7.0 Multicast", 10.0),
    "8.0 CoS": ("8.0 CoS", 5.0),
}

JNCIP_ENT_TERMS = [
    # IGP
    ("OSPF area", "A logical grouping of OSPF routers sharing a link-state database.", "1.1 OSPF"),
    ("OSPF neighbor", "Two routers that have established bidirectional communication.", "1.1 OSPF"),
    ("OSPF adjacency", "A relationship where two neighbors exchange LSAs.", "1.1 OSPF"),
    ("Designated Router", "An OSPF router elected to reduce adjacency count on broadcast segments.", "1.1 OSPF"),
    ("Backup Designated Router", "The OSPF router that takes over if the DR fails.", "1.1 OSPF"),
    ("Link-state advertisement", "An OSPF packet describing router or network state.", "1.1 OSPF"),
    ("Link-state database", "The database of LSAs used to calculate shortest paths.", "1.1 OSPF"),
    ("OSPF cost", "The metric derived from interface bandwidth.", "1.1 OSPF"),
    ("Stub area", "An OSPF area that does not accept external AS routes.", "1.1 OSPF"),
    ("Totally stubby area", "An OSPF area that blocks external and inter-area routes.", "1.1 OSPF"),
    ("NSSA", "A not-so-stubby area that can originate Type 7 LSAs.", "1.1 OSPF"),
    ("Virtual link", "A logical OSPF link used to connect an area to the backbone.", "1.1 OSPF"),
    ("IS-IS", "Intermediate System to Intermediate System link-state protocol.", "1.2 IS-IS"),
    ("IS-IS Level 1", "IS-IS routing within an area.", "1.2 IS-IS"),
    ("IS-IS Level 2", "IS-IS routing between areas.", "1.2 IS-IS"),
    ("IS-IS LSP", "Link-State PDU containing topology information.", "1.2 IS-IS"),
    ("IS-IS DIS", "Designated Intermediate System elected on broadcast subnets.", "1.2 IS-IS"),
    ("IS-IS NET", "Network Entity Title identifying an IS-IS router.", "1.2 IS-IS"),
    ("IS-IS metric", "Cost used to calculate the shortest path.", "1.2 IS-IS"),
    ("Wide metrics", "IS-IS metrics using 24-bit values for large networks.", "1.2 IS-IS"),
    ("Overload bit", "An IS-IS bit that prevents transit traffic through a router.", "1.2 IS-IS"),
    ("Attached bit", "An IS-IS bit set by L1/L2 routers to provide default route.", "1.2 IS-IS"),

    # BGP
    ("BGP", "Border Gateway Protocol, a path-vector EGP.", "2.0 BGP"),
    ("AS_PATH", "BGP attribute listing autonomous systems traversed.", "2.2 BGP attributes"),
    ("NEXT_HOP", "BGP attribute indicating the next-hop IP address.", "2.2 BGP attributes"),
    ("LOCAL_PREF", "BGP attribute influencing outbound path selection.", "2.2 BGP attributes"),
    ("MED", "BGP attribute influencing inbound path selection.", "2.2 BGP attributes"),
    ("ORIGIN", "BGP attribute describing how a route was originated.", "2.2 BGP attributes"),
    ("Community", "A BGP transitive attribute for route grouping.", "2.2 BGP attributes"),
    ("Extended community", "A BGP community with a 64-bit value.", "2.2 BGP attributes"),
    ("Route reflector", "An iBGP peer that reflects routes to clients.", "2.3 BGP scaling"),
    ("Route reflector client", "An iBGP peer receiving reflected routes.", "2.3 BGP scaling"),
    ("Confederation", "A set of sub-ASes appearing as a single AS externally.", "2.3 BGP scaling"),
    ("eBGP", "BGP session between different autonomous systems.", "2.1 BGP basics"),
    ("iBGP", "BGP session within the same autonomous system.", "2.1 BGP basics"),
    ("BGP peer group", "A template simplifying configuration of multiple BGP peers.", "2.1 BGP basics"),
    ("Multihop eBGP", "An eBGP session between non-directly connected peers.", "2.1 BGP basics"),
    ("BGP damping", "Penalty-based suppression of unstable routes.", "2.0 BGP"),
    ("Route flap", "Repeated route withdrawals and re-advertisements.", "2.0 BGP"),

    # Multicast
    ("IGMP", "Internet Group Management Protocol for host membership.", "3.0 IP Multicast"),
    ("PIM", "Protocol Independent Multicast for multicast routing.", "3.0 IP Multicast"),
    ("PIM sparse mode", "PIM mode using a rendezvous point.", "3.0 IP Multicast"),
    ("PIM dense mode", "PIM mode flooding and pruning multicast traffic.", "3.0 IP Multicast"),
    ("Rendezvous point", "A router where sources and receivers meet in PIM-SM.", "3.0 IP Multicast"),
    ("Source-specific multicast", "Multicast delivery from a specific source.", "3.0 IP Multicast"),
    ("Multicast group", "An IP address identifying a multicast destination.", "3.0 IP Multicast"),
    ("Reverse path forwarding", "A multicast loop prevention check.", "3.0 IP Multicast"),

    # Ethernet Switching
    ("VLAN", "A logical Layer 2 broadcast domain.", "4.0 Ethernet Switching"),
    ("IRB", "Integrated Routing and Bridging interface.", "4.0 Ethernet Switching"),
    ("Bridge domain", "A Junos forwarding entity for a set of VLANs.", "4.0 Ethernet Switching"),
    ("Storm control", "A feature limiting broadcast, multicast, and unknown unicast.", "4.0 Ethernet Switching"),
    ("Spanning Tree", "A loop-prevention protocol for Layer 2.", "4.0 Ethernet Switching"),
    ("RSTP", "Rapid Spanning Tree Protocol.", "4.0 Ethernet Switching"),
    ("MSTP", "Multiple Spanning Tree Protocol.", "4.0 Ethernet Switching"),
    ("VSTP", "VLAN Spanning Tree Protocol on Junos.", "4.0 Ethernet Switching"),
    ("LAG", "Link Aggregation Group.", "4.0 Ethernet Switching"),
    ("MC-LAG", "Multi-Chassis Link Aggregation Group.", "4.0 Ethernet Switching"),

    # CoS
    ("Classifier", "A Junos feature mapping traffic to forwarding classes.", "5.0 CoS"),
    ("Rewrite rule", "A Junos feature changing DSCP/CoS markings.", "5.0 CoS"),
    ("Scheduler", "A Junos feature defining bandwidth and priority.", "5.0 CoS"),
    ("Forwarding class", "A traffic class in Junos CoS.", "5.0 CoS"),
    ("Loss priority", "A marking used for drop probability.", "5.0 CoS"),
    ("Policer", "A rate-limiting feature.", "5.0 CoS"),
    ("Shaper", "A feature smoothing traffic to a configured rate.", "5.0 CoS"),
    ("RED", "Random Early Detection drop profile.", "5.0 CoS"),
    ("WRED", "Weighted Random Early Detection.", "5.0 CoS"),

    # EVPN
    ("EVPN", "Ethernet VPN for multipoint Layer 2 services.", "6.0 EVPN"),
    ("VXLAN", "Virtual Extensible LAN encapsulation.", "6.0 EVPN"),
    ("Type 1 route", "EVPN Ethernet Auto-Discovery route.", "6.0 EVPN"),
    ("Type 2 route", "EVPN MAC/IP advertisement route.", "6.0 EVPN"),
    ("Type 3 route", "EVPN inclusive multicast Ethernet tag route.", "6.0 EVPN"),
    ("Type 4 route", "EVPN Ethernet segment route.", "6.0 EVPN"),
    ("Type 5 route", "EVPN IP prefix route.", "6.0 EVPN"),
    ("All-active multihoming", "EVPN where all PEs forward traffic.", "6.0 EVPN"),
    ("Single-active multihoming", "EVPN where one PE forwards traffic.", "6.0 EVPN"),

    # Layer 3 VPN
    ("VRF", "Virtual Routing and Forwarding instance.", "7.0 Layer 3 VPN"),
    ("Route distinguisher", "A value making VPN prefixes unique.", "7.0 Layer 3 VPN"),
    ("Route target", "A BGP extended community controlling VPN import/export.", "7.0 Layer 3 VPN"),
    ("PE router", "Provider Edge router connected to CEs.", "7.0 Layer 3 VPN"),
    ("CE router", "Customer Edge router connected to a PE.", "7.0 Layer 3 VPN"),
    ("P router", "Provider core router without VPN awareness.", "7.0 Layer 3 VPN"),
    ("Hub-and-spoke VPN", "A VPN topology where spokes communicate through a hub.", "7.0 Layer 3 VPN"),
    ("Full-mesh VPN", "A VPN topology where all sites exchange routes.", "7.0 Layer 3 VPN"),

    # Layer 2 VPN
    ("L2VPN", "A point-to-point Layer 2 MPLS service.", "8.0 Layer 2 VPN"),
    ("VPLS", "Virtual Private LAN Service for multipoint Layer 2.", "8.0 Layer 2 VPN"),
    ("VPWS", "Virtual Private Wire Service for point-to-point Layer 2.", "8.0 Layer 2 VPN"),
    ("Pseudowire", "An emulated circuit over a packet-switched network.", "8.0 Layer 2 VPN"),
    ("Martini signaling", "LDP-based signaling for pseudowires.", "8.0 Layer 2 VPN"),
    ("Kompella signaling", "BGP-based signaling for Layer 2 VPNs.", "8.0 Layer 2 VPN"),
    ("Site ID", "Identifier for a CE site in Kompella L2VPN.", "8.0 Layer 2 VPN"),

    # High Availability
    ("GRES", "Graceful Routing Engine Switchover.", "9.0 High Availability"),
    ("NSR", "Nonstop Routing for control-plane redundancy.", "9.0 High Availability"),
    ("NSF", "Nonstop Forwarding for data-plane redundancy.", "9.0 High Availability"),
    ("Graceful restart", "A protocol mechanism for control-plane restart.", "9.0 High Availability"),
    ("BFD", "Bidirectional Forwarding Detection for fast failure detection.", "9.0 High Availability"),
    ("VRRP", "Virtual Router Redundancy Protocol.", "9.0 High Availability"),
]

JNCIP_SP_TERMS = [
    # OSPF
    ("OSPF area", "A logical grouping of OSPF routers sharing a link-state database.", "1.0 OSPF"),
    ("OSPFv3", "OSPF for IPv6 networks.", "1.0 OSPF"),
    ("Stub area", "An OSPF area that does not accept external routes.", "1.0 OSPF"),
    ("NSSA", "A not-so-stubby area that can originate Type 7 LSAs.", "1.0 OSPF"),
    ("Virtual link", "A logical OSPF link connecting an area to Area 0.", "1.0 OSPF"),
    ("Sham link", "A logical OSPF link inside an MPLS VPN to prevent backdoor routes.", "1.0 OSPF"),
    # IS-IS
    ("IS-IS Level 1", "IS-IS routing within an area.", "2.0 IS-IS"),
    ("IS-IS Level 2", "IS-IS routing between areas.", "2.0 IS-IS"),
    ("IS-IS DIS", "Designated Intermediate System elected on broadcast subnets.", "2.0 IS-IS"),
    ("IS-IS NET", "Network Entity Title identifying an IS-IS router.", "2.0 IS-IS"),
    ("Overload bit", "An IS-IS bit that prevents transit traffic.", "2.0 IS-IS"),
    # BGP
    ("AS_PATH", "BGP attribute listing traversed autonomous systems.", "3.0 BGP"),
    ("LOCAL_PREF", "BGP attribute influencing outbound path selection.", "3.0 BGP"),
    ("MED", "BGP attribute influencing inbound path selection.", "3.0 BGP"),
    ("Community", "A BGP attribute for grouping routes.", "3.0 BGP"),
    ("Route reflector", "An iBGP peer reflecting routes to clients.", "3.0 BGP"),
    ("Confederation", "A set of sub-ASes appearing as one AS externally.", "3.0 BGP"),
    ("BGP damping", "Suppression of unstable BGP routes.", "3.0 BGP"),
    # MPLS
    ("MPLS", "Multiprotocol Label Switching for fast packet forwarding.", "4.0 MPLS"),
    ("Label", "A short identifier used to forward MPLS packets.", "4.0 MPLS"),
    ("LSR", "Label Switching Router.", "4.0 MPLS"),
    ("Ingress LER", "Label Edge Router adding labels at the network edge.", "4.0 MPLS"),
    ("Egress LER", "Label Edge Router removing labels at the network edge.", "4.0 MPLS"),
    ("PHP", "Penultimate Hop Popping to reduce label lookups.", "4.0 MPLS"),
    ("LDP", "Label Distribution Protocol.", "4.0 MPLS"),
    ("RSVP", "Resource Reservation Protocol for MPLS traffic engineering.", "4.0 MPLS"),
    ("RSVP LSP", "Label-switched path signaled by RSVP.", "4.0 MPLS"),
    ("Fast reroute", "A protection mechanism for MPLS LSPs.", "4.0 MPLS"),
    ("Link protection", "Fast reroute protecting a single link.", "4.0 MPLS"),
    ("Node protection", "Fast reroute protecting against node failure.", "4.0 MPLS"),
    ("Traffic engineering", "Optimizing network resource use with RSVP-TE.", "4.0 MPLS"),
    # L3VPN
    ("VRF", "Virtual Routing and Forwarding instance.", "5.0 L3VPN"),
    ("Route distinguisher", "A value making VPN prefixes unique.", "5.0 L3VPN"),
    ("Route target", "A BGP extended community controlling VPN import/export.", "5.0 L3VPN"),
    ("PE router", "Provider Edge router.", "5.0 L3VPN"),
    ("CE router", "Customer Edge router.", "5.0 L3VPN"),
    ("P router", "Provider core router without VPN awareness.", "5.0 L3VPN"),
    ("Hub-and-spoke", "A VPN topology with communication through a hub.", "5.0 L3VPN"),
    # L2VPN
    ("VPLS", "Virtual Private LAN Service.", "6.0 L2VPN"),
    ("VPWS", "Virtual Private Wire Service.", "6.0 L2VPN"),
    ("Pseudowire", "An emulated circuit over MPLS.", "6.0 L2VPN"),
    ("Martini", "LDP-signaled pseudowire.", "6.0 L2VPN"),
    ("Kompella", "BGP-signaled Layer 2 VPN.", "6.0 L2VPN"),
    # Multicast
    ("PIM-SM", "PIM sparse mode using a rendezvous point.", "7.0 Multicast"),
    ("PIM-SSM", "PIM source-specific multicast.", "7.0 Multicast"),
    ("Rendezvous point", "A router where sources and receivers meet.", "7.0 Multicast"),
    ("MSDP", "Multicast Source Discovery Protocol for inter-domain multicast.", "7.0 Multicast"),
    ("RPF", "Reverse Path Forwarding check.", "7.0 Multicast"),
    # CoS
    ("Classifier", "Maps traffic to forwarding classes.", "8.0 CoS"),
    ("Forwarding class", "A traffic class in CoS.", "8.0 CoS"),
    ("Scheduler", "Defines bandwidth and priority.", "8.0 CoS"),
    ("Policer", "Rate-limiting feature.", "8.0 CoS"),
]

JNCIP_ENT_COMMANDS = [
    ("show ospf neighbor", "displays OSPF neighbors", "1.1 OSPF"),
    ("show ospf interface", "displays OSPF interface state", "1.1 OSPF"),
    ("show ospf database", "displays the OSPF LSDB", "1.1 OSPF"),
    ("show isis adjacency", "displays IS-IS adjacencies", "1.2 IS-IS"),
    ("show isis database", "displays the IS-IS link-state database", "1.2 IS-IS"),
    ("show bgp summary", "displays BGP peer summary", "2.1 BGP basics"),
    ("show bgp neighbor", "displays BGP neighbor details", "2.1 BGP basics"),
    ("show route protocol bgp", "displays BGP routes in the routing table", "2.1 BGP basics"),
    ("show multicast route", "displays multicast routing table", "3.0 IP Multicast"),
    ("show pim neighbors", "displays PIM neighbors", "3.0 IP Multicast"),
    ("show ethernet-switching table", "displays MAC table on Junos", "4.0 Ethernet Switching"),
    ("show configuration class-of-service", "displays CoS configuration", "5.0 CoS"),
    ("show evpn overview", "displays EVPN instance overview", "6.0 EVPN"),
    ("show evpn database", "displays EVPN MAC database", "6.0 EVPN"),
    ("show route instance", "displays routing instances", "7.0 Layer 3 VPN"),
    ("show route table", "displays a specific routing table", "7.0 Layer 3 VPN"),
    ("show l2vpn connections", "displays Layer 2 VPN connections", "8.0 Layer 2 VPN"),
    ("show system switchover", "displays GRES status", "9.0 High Availability"),
]

JNCIP_SP_COMMANDS = [
    ("show ospf neighbor", "displays OSPF neighbors", "1.0 OSPF"),
    ("show ospf database", "displays the OSPF LSDB", "1.0 OSPF"),
    ("show isis adjacency", "displays IS-IS adjacencies", "2.0 IS-IS"),
    ("show isis database", "displays the IS-IS LSDB", "2.0 IS-IS"),
    ("show bgp summary", "displays BGP peer summary", "3.0 BGP"),
    ("show route protocol bgp", "displays BGP routes", "3.0 BGP"),
    ("show mpls lsp", "displays MPLS LSPs", "4.0 MPLS"),
    ("show mpls interface", "displays MPLS-enabled interfaces", "4.0 MPLS"),
    ("show ldp neighbor", "displays LDP neighbors", "4.0 MPLS"),
    ("show rsvp neighbor", "displays RSVP neighbors", "4.0 MPLS"),
    ("show route instance", "displays routing instances", "5.0 L3VPN"),
    ("show route table", "displays a specific routing table", "5.0 L3VPN"),
    ("show l2vpn connections", "displays Layer 2 VPN connections", "6.0 L2VPN"),
    ("show pim neighbors", "displays PIM neighbors", "7.0 Multicast"),
    ("show multicast route", "displays multicast routes", "7.0 Multicast"),
    ("show class-of-service", "displays CoS configuration", "8.0 CoS"),
]

JNCIP_ENT_SCENARIOS = [
    ("An OSPF router receives two paths to the same destination.", "One path is intra-area and the other is inter-area.", "The intra-area path is preferred regardless of cost.", "1.1 OSPF"),
    ("An IS-IS router has the overload bit set.", "Transit traffic arrives at the router.", "The router avoids transit paths and is used only for directly connected destinations.", "1.2 IS-IS"),
    ("A BGP router receives a route with no LOCAL_PREF attribute.", "The route is received from an eBGP peer.", "LOCAL_PREF is not present on eBGP-learned routes by default.", "2.2 BGP attributes"),
    ("A route reflector client advertises a route to its route reflector.", "The route reflector reflects the route to other clients.", "The next-hop remains unchanged unless 'neighbor next-hop-self' is configured.", "2.3 BGP scaling"),
    ("A PIM-SM receiver joins a multicast group.", "No active source exists yet.", "The receiver's DR sends a (*,G) join toward the RP.", "3.0 IP Multicast"),
    ("An EVPN PE receives a Type 2 route for a MAC address.", "The MAC is reachable via a remote PE.", "The local PE installs the MAC in its bridge domain forwarding table.", "6.0 EVPN"),
    ("A Layer 3 VPN site advertises a route with route target 65000:100.", "The receiving PE has a VRF importing 65000:100.", "The route is installed into the matching VRF routing table.", "7.0 Layer 3 VPN"),
    ("A Layer 2 VPN pseudowire is signaled using LDP.", "The remote PE is unreachable.", "The pseudowire remains down until LDP session to the remote PE is established.", "8.0 Layer 2 VPN"),
    ("A router's Routing Engine fails.", "GRES and NSR are configured.", "Forwarding continues using the backup RE with no protocol disruption.", "9.0 High Availability"),
]

JNCIP_SP_SCENARIOS = [
    ("An MPLS LSP uses RSVP with fast reroute enabled.", "A protected link fails.", "Traffic is rerouted along the bypass LSP within tens of milliseconds.", "4.0 MPLS"),
    ("A BGP route has a shorter AS_PATH but lower LOCAL_PREF.", "All higher attributes are equal except LOCAL_PREF and AS_PATH.", "LOCAL_PREF is evaluated before AS_PATH; the higher LOCAL_PREF route wins.", "3.0 BGP"),
    ("An L3VPN CE advertises a default route to the PE.", "The PE exports the default route with route target 65000:1.", "Other VRFs importing 65000:1 receive the default route.", "5.0 L3VPN"),
    ("A VPLS site uses BGP signaling (Kompella).", "A new site is added.", "BGP advertises the new site ID and pseudowire labels to other PEs.", "6.0 L2VPN"),
    ("PIM-SM is deployed without any source.", "A receiver sends an IGMP join for group 239.1.1.1.", "The DR builds the shared tree toward the RP using (*,239.1.1.1).", "7.0 Multicast"),
    ("An IS-IS Level 1 router needs to reach a prefix in another area.", "The nearest L1/L2 router has the attached bit set.", "The L1 router installs a default route toward the L1/L2 router.", "2.0 IS-IS"),
]

JNCIP_ENT_SIMLETS = [
    (
        """user@PE1> show bgp summary
Groups: 1 Peers: 2 Down peers: 0
Peer                     AS      InPkt     OutPkt    OutQ   Flaps Last Up/Dwn State|#Active/Received/Accepted/Damped...
10.0.0.2              65002      1200       1200       0       0    1d 2:10:10 Establ
  inet.0: 50/50/50/0
10.0.0.3              65001      1100       1100       0       0    2d 1:05:00 Establ
  inet.0: 100/100/100/0""",
        "Which peer is an iBGP peer?",
        [("10.0.0.2 in AS 65002", False), ("10.0.0.3 in AS 65001", True), ("Both are iBGP peers", False), ("Neither is an iBGP peer", False)],
        "The local AS is 65001. 10.0.0.3 has the same AS, so it is iBGP.",
        "2.1 BGP basics",
    ),
    (
        """user@PE1> show ospf neighbor
Address          Interface              State     ID               Pri  Dead
10.1.1.2         ge-0/0/0.0             Full      2.2.2.2          128    33
10.1.1.3         ge-0/0/0.0             2Way      3.3.3.3            0    38""",
        "How many full adjacencies are on ge-0/0/0.0?",
        [("0", False), ("1", True), ("2", False), ("3", False)],
        "On a broadcast network, full adjacencies are formed only with DR/BDR. Only one neighbor is in Full state.",
        "1.1 OSPF",
    ),
    (
        """user@PE1> show route table vpn-a.inet.0

vpn-a.inet.0: 3 destinations, 3 routes (3 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

10.10.0.0/24     *[BGP/170] 00:05:12, localpref 100
                      AS path: I, validation-state: unverified
                    > to 10.0.0.4 via ge-0/0/1.0""",
        "Which protocol installed the route in the VPN routing table?",
        [("OSPF", False), ("Static", False), ("BGP", True), ("IS-IS", False)],
        "The route is marked [BGP/170], indicating it was learned via BGP.",
        "7.0 Layer 3 VPN",
    ),
]

JNCIP_SP_SIMLETS = [
    (
        """user@P> show mpls lsp
Ingress LSP: 1 sessions
To              From            State Rt P     ActivePath       LSPname
10.0.0.6        10.0.0.1        Up    0 *     primary          to-PE2""",
        "What is the state of the LSP to 10.0.0.6?",
        [("Down", False), ("Up", True), ("Active", False), ("Bypass", False)],
        "The State column shows Up.",
        "4.0 MPLS",
    ),
    (
        """user@PE> show route table vpn-a.inet.0 192.168.1.0/24

vpn-a.inet.0: 1 destinations, 1 routes (1 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

192.168.1.0/24   *[BGP/170] 00:10:22, localpref 100, from 10.0.0.5
                      AS path: I, validation-state: unverified
                    > to 10.0.0.5 via ge-0/0/2.0, label-switched-path to-PE2""",
        "How is traffic to 192.168.1.0/24 forwarded?",
        [("Via IP next-hop only", False), ("Via LSP to-PE2", True), ("Via default route", False), ("It is dropped", False)],
        "The route resolves to label-switched-path to-PE2.",
        "5.0 L3VPN",
    ),
    (
        """user@PE> show ldp neighbor
Address            Interface          Peer-id             Holdtime
10.1.1.2           ge-0/0/0.0         2.2.2.2:0           12
10.1.1.3           ge-0/0/0.0         3.3.3.3:0           11""",
        "How many LDP neighbors are established?",
        [("1", False), ("2", True), ("3", False), ("0", False)],
        "The output lists two LDP neighbors.",
        "4.0 MPLS",
    ),
]

JNCIP_ENT_MULTIPLE_CHOICE = [
    (
        "1.0 IGP",
        "Which OSPF LSA types are generated by ABRs? (Choose two.)",
        ["Type 3 Summary LSA", "Type 4 ASBR-Summary LSA"],
        ["Type 1 Router LSA", "Type 2 Network LSA", "Type 5 External LSA", "Type 7 NSSA External LSA"],
        "Type 3 and Type 4 LSAs are generated by ABRs. Type 1/2 by all routers/DRs, Type 5 by ASBRs, Type 7 by NSSA ASBRs.",
    ),
    (
        "2.0 BGP",
        "Which BGP attributes are well-known mandatory? (Choose two.)",
        ["AS_PATH", "NEXT_HOP"],
        ["LOCAL_PREF", "MED", "Community", "Originator ID"],
        "AS_PATH and NEXT_HOP are well-known mandatory. LOCAL_PREF is well-known discretionary. MED and Community are optional.",
    ),
    (
        "6.0 EVPN",
        "Which EVPN route types are used for MAC/IP advertisement? (Choose two.)",
        ["Type 2", "Type 5"],
        ["Type 1", "Type 3", "Type 4", "Type 6"],
        "Type 2 carries MAC/IP, Type 5 carries IP prefixes. Type 1 is Ethernet A-D, Type 3 inclusive multicast, Type 4 Ethernet segment.",
    ),
    (
        "1.0 IGP",
        "Which statements about IS-IS levels are true? (Choose two.)",
        ["Level 1 routers route within an area", "Level 2 routers route between areas"],
        ["Level 1 routers know all inter-area routes", "Level 2 routers never exchange Level 1 routes", "DIS is elected only on point-to-point links", "Wide metrics are required for Level 1"],
        "Level 1 is intra-area; Level 2 is inter-area. L1/L2 routers connect areas. DIS is elected on broadcast links.",
    ),
    (
        "2.0 BGP",
        "Which BGP scaling mechanisms reduce the need for a full iBGP mesh? (Choose two.)",
        ["Route reflectors", "Confederations"],
        ["Route damping", "Communities", "MED", "AS_PATH prepending"],
        "Route reflectors and confederations reduce iBGP mesh requirements. Damping, communities, MED, and prepending are policy/attributes.",
    ),
    (
        "4.0 Ethernet Switching",
        "Which statements about Junos bridge domains are true? (Choose two.)",
        ["A bridge domain is a Layer 2 forwarding entity", "IRB provides Layer 3 routing for a bridge domain"],
        ["Bridge domains replace routing tables", "IRB is only for MPLS", "Storm control is a Layer 3 feature", "VSTP is required for bridge domains"],
        "Bridge domains provide Layer 2 forwarding; IRB interfaces route between VLANs/bridge domains.",
    ),
    (
        "7.0 Layer 3 VPN",
        "Which statements about route distinguishers and route targets are true? (Choose two.)",
        ["RD makes VPN prefixes unique", "RT controls VPN import/export"],
        ["RD controls import/export", "RT makes prefixes unique", "RD and RT are the same", "RD is used only in EVPN"],
        "RD ensures unique VPN-IPv4/IPv6 prefixes; RT extended communities control which VRFs import/export routes.",
    ),
    (
        "5.0 CoS",
        "Which Junos CoS components can classify or mark traffic? (Choose two.)",
        ["Classifier", "Rewrite rule"],
        ["Scheduler", "Policer", "Buffer", "Queue"],
        "Classifiers map traffic to forwarding classes; rewrite rules change DSCP/CoS bits. Schedulers/policers manage bandwidth/drop.",
    ),
]

JNCIP_SP_MULTIPLE_CHOICE = [
    (
        "3.0 BGP",
        "Which BGP attributes are well-known mandatory? (Choose two.)",
        ["AS_PATH", "NEXT_HOP"],
        ["LOCAL_PREF", "MED", "Community", "Originator ID"],
        "AS_PATH and NEXT_HOP are well-known mandatory.",
    ),
    (
        "4.0 MPLS",
        "Which protocols can signal MPLS labels? (Choose two.)",
        ["LDP", "RSVP"],
        ["BGP", "OSPF", "IS-IS", "PIM"],
        "LDP and RSVP are MPLS label signaling protocols. BGP can signal VPN labels, but not transport labels by default.",
    ),
    (
        "5.0 L3VPN",
        "Which components are required for a Layer 3 VPN? (Choose two.)",
        ["Route distinguisher", "Route target"],
        ["IS-IS NET", "OSPF area ID", "PIM RP", "BFD"],
        "RD makes prefixes unique; RT controls import/export. IS-IS NET, OSPF area, PIM RP, BFD are not required for L3VPN itself.",
    ),
    (
        "4.0 MPLS",
        "Which statements about RSVP-TE are true? (Choose two.)",
        ["RSVP-TE can reserve bandwidth", "RSVP-TE supports explicit paths"],
        ["RSVP-TE uses LDP for label distribution", "RSVP-TE cannot use Fast Reroute", "RSVP-TE is only for L2VPN", "RSVP-TE does not support traffic engineering"],
        "RSVP-TE supports bandwidth reservation, explicit paths, and fast reroute. It does not use LDP.",
    ),
    (
        "5.0 L3VPN",
        "Which statements describe hub-and-spoke VPNs? (Choose two.)",
        ["Spokes exchange traffic through the hub", "The hub can apply policy to inter-spoke traffic"],
        ["Spokes communicate directly", "Full mesh of BGP sessions is required", "Each spoke imports all RTs", "Hub-and-spoke requires VPLS"],
        "In hub-and-spoke, all traffic passes through the hub, allowing policy enforcement. Spokes do not communicate directly.",
    ),
    (
        "6.0 L2VPN",
        "Which statements differentiate VPLS and VPWS? (Choose two.)",
        ["VPLS is multipoint", "VPWS is point-to-point"],
        ["VPLS is point-to-point", "VPWS requires BGP signaling", "VPLS uses pseudowires only", "VPWS supports MAC learning"],
        "VPLS provides multipoint Layer 2 LAN; VPWS provides point-to-point Layer 2 circuit.",
    ),
    (
        "7.0 Multicast",
        "Which statements about PIM sparse mode are true? (Choose two.)",
        ["Uses a rendezvous point", "Receivers join (*,G) toward the RP"],
        ["Floods traffic by default", "Does not use RP", "Source registers directly with receivers", "Only supports SSM"],
        "PIM-SM uses an RP; receivers join shared tree (*,G). SSM uses (S,G) without RP.",
    ),
    (
        "3.0 BGP",
        "Which actions influence inbound traffic with BGP? (Choose two.)",
        ["AS_PATH prepending", "MED"],
        ["LOCAL_PREF", "Weight", "Communities for outbound only", "Next-hop self"],
        "AS_PATH prepending and MED influence how external ASes send traffic inbound. LOCAL_PREF and Weight influence outbound.",
    ),
]


JNCIP_ENT_DRAG_DROP_POOLS = [
    (
        "1.0 IGP",
        "Match the OSPF LSA type to its description.",
        [
            ("Type 1", "Router LSA"),
            ("Type 2", "Network LSA"),
            ("Type 3", "Summary LSA"),
            ("Type 5", "External LSA"),
            ("Type 7", "NSSA External LSA"),
        ],
    ),
    (
        "2.0 BGP",
        "Order the BGP route selection steps from highest to lowest priority.",
        [
            ("Weight", "Highest priority Cisco attribute"),
            ("LOCAL_PREF", "Outbound preference"),
            ("AS_PATH", "Prefer shorter path"),
            ("MED", "Inbound preference"),
        ],
    ),
    (
        "4.0 Ethernet Switching",
        "Match the spanning-tree port role to its function.",
        [
            ("Root port", "Best path to root"),
            ("Designated port", "Forwards toward root on segment"),
            ("Alternate port", "Backup root path"),
            ("Backup port", "Backup on same segment"),
        ],
    ),
    (
        "6.0 EVPN",
        "Match the EVPN route type to its purpose.",
        [
            ("Type 1", "Ethernet Auto-Discovery"),
            ("Type 2", "MAC/IP advertisement"),
            ("Type 3", "Inclusive multicast"),
            ("Type 4", "Ethernet segment"),
            ("Type 5", "IP prefix"),
        ],
    ),
    (
        "5.0 CoS",
        "Match the CoS component to its function.",
        [
            ("Classifier", "Maps traffic to forwarding class"),
            ("Rewrite rule", "Changes DSCP/CoS bits"),
            ("Scheduler", "Defines bandwidth and priority"),
            ("Policer", "Rate limits traffic"),
        ],
    ),
]

JNCIP_SP_DRAG_DROP_POOLS = [
    (
        "3.0 BGP",
        "Order the BGP route selection attributes from highest to lowest priority.",
        [
            ("Weight", "Cisco local attribute"),
            ("LOCAL_PREF", "Outbound path preference"),
            ("AS_PATH", "Shorter is better"),
            ("MED", "Inbound path preference"),
        ],
    ),
    (
        "4.0 MPLS",
        "Match the MPLS label operation to its description.",
        [
            ("Push", "Add a label"),
            ("Pop", "Remove top label"),
            ("Swap", "Replace top label"),
            ("PHP", "Pop at penultimate hop"),
        ],
    ),
    (
        "5.0 L3VPN",
        "Match the VPN component to its function.",
        [
            ("Route distinguisher", "Makes prefixes unique"),
            ("Route target", "Controls import/export"),
            ("PE router", "Provider edge device"),
            ("CE router", "Customer edge device"),
        ],
    ),
    (
        "6.0 L2VPN",
        "Match the Layer 2 VPN technology to its topology.",
        [
            ("VPLS", "Multipoint"),
            ("VPWS", "Point-to-point"),
            ("Martini", "LDP-signaled pseudowire"),
            ("Kompella", "BGP-signaled L2VPN"),
        ],
    ),
    (
        "7.0 Multicast",
        "Match the PIM mode to its behavior.",
        [
            ("PIM-SM", "Uses rendezvous point"),
            ("PIM-SSM", "Source-specific"),
            ("PIM-DM", "Flood and prune"),
        ],
    ),
]

JNCIP_ENT_FILL_BLANK_POOLS = [
    ("1.1 OSPF", "In OSPF, the router elected on a broadcast segment to reduce adjacency count is the __________.", "DR", ["BDR", "ABR", "ASBR", "DRother"]),
    ("1.2 IS-IS", "An IS-IS router that prevents transit traffic by setting the __________ bit is used during maintenance.", "overload", ["attached", "metric", "level", "DIS"]),
    ("2.2 BGP attributes", "The BGP attribute that influences outbound path selection from the local AS is __________.", "LOCAL_PREF", ["MED", "AS_PATH", "NEXT_HOP", "ORIGIN"]),
    ("2.3 BGP scaling", "A BGP __________ reduces the need for a full iBGP mesh by reflecting routes to clients.", "route reflector", ["confederation", "peer group", "dampening", "community"]),
    ("3.0 IP Multicast", "In PIM sparse mode, sources register with the __________.", "rendezvous point", ["RP", "BSR", "MSDP", "DR"]),
    ("4.0 Ethernet Switching", "The Junos interface that routes for a bridge domain is called an __________.", "IRB", ["SVI", "BVI", "VLAN", "LAG"]),
    ("5.0 CoS", "The Junos feature that maps incoming traffic to a forwarding class is a __________.", "classifier", ["scheduler", "policer", "rewrite rule", "drop profile"]),
    ("6.0 EVPN", "The EVPN route type used to advertise MAC/IP reachability is Type __________.", "2", ["1", "3", "4", "5"]),
    ("7.0 Layer 3 VPN", "The BGP extended community that controls VPN route import/export is the __________.", "route target", ["route distinguisher", "site of origin", "cluster list", "originator ID"]),
    ("8.0 Layer 2 VPN", "A point-to-point Layer 2 MPLS service is called __________.", "VPWS", ["VPLS", "EVPN", "L3VPN", "PWE3"]),
    ("9.0 High Availability", "The feature that allows the backup Routing Engine to take over forwarding state without interruption is __________.", "GRES", ["NSR", "NSF", "BFD", "VRRP"]),
]

JNCIP_SP_FILL_BLANK_POOLS = [
    ("1.0 OSPF", "An OSPF __________ link connects a non-backbone area to Area 0.", "virtual", ["sham", "gre", "backdoor", "logical"]),
    ("2.0 IS-IS", "IS-IS Level __________ routers route between areas.", "2", ["1", "3", "0", "4"]),
    ("3.0 BGP", "The BGP attribute that lists autonomous systems traversed is the __________.", "AS_PATH", ["LOCAL_PREF", "MED", "NEXT_HOP", "COMMUNITY"]),
    ("4.0 MPLS", "The label distribution protocol that uses downstream-on-demand by default is __________.", "RSVP", ["LDP", "BGP", "OSPF", "IS-IS"]),
    ("4.0 MPLS", "Removing the label one hop before the egress LER is called __________.", "PHP", ["FRR", "LDP", "TE", "LSP"]),
    ("5.0 L3VPN", "The value that makes VPN-IPv4 prefixes unique is the __________.", "route distinguisher", ["route target", "VRF", "RD", "AS number"]),
    ("6.0 L2VPN", "A multipoint Layer 2 MPLS service is called __________.", "VPLS", ["VPWS", "L2TP", "GRE", "IPsec"]),
    ("7.0 Multicast", "PIM __________ mode does not use a rendezvous point.", "SSM", ["SM", "DM", "BIDIR", "ASM"]),
    ("8.0 CoS", "A Junos __________ limits traffic to a configured rate.", "policer", ["scheduler", "shaper", "classifier", "queue"]),
]

JNCIP_ENT_SIMLETS += [
    (
        """user@PE> show isis adjacency
Interface             System                L State        Hold (secs) SNPA
ge-0/0/0.0            R2                    2  Up                   24
ge-0/0/0.0            R3                    1  Up                   22
ge-0/0/1.0            R4                    2  Up                   20""",
        "How many Level 1 IS-IS adjacencies are present?",
        [("0", False), ("1", True), ("2", False), ("3", False)],
        "Only one adjacency shows Level 1 (L 1).",
        "1.2 IS-IS",
    ),
    (
        """user@PE> show configuration interfaces irb
unit 10 {
    family inet {
        address 10.10.10.1/24;
    }
}
unit 20 {
    family inet {
        address 10.20.20.1/24;
    }
}""",
        "How many IRB interfaces are configured?",
        [("1", False), ("2", True), ("3", False), ("0", False)],
        "IRB units 10 and 20 are configured.",
        "4.0 Ethernet Switching",
    ),
    (
        """user@PE> show configuration policy-options community VPN-CUSTOMERS
members target:65000:100;

user@PE> show configuration routing-instances VPN-A
instance-type vrf;
interface ge-0/0/2.0;
route-distinguisher 65000:1;
vrf-target target:65000:100;""",
        "Which route target is imported/exported by VPN-A?",
        [("65000:1", False), ("65000:100", True), ("target:65000:1", False), ("No RT configured", False)],
        "vrf-target target:65000:100 controls import/export.",
        "7.0 Layer 3 VPN",
    ),
]

JNCIP_SP_SIMLETS += [
    (
        """user@P> show rsvp session
Ingress RSVP: 1 sessions
To              From            State Rt Style Labelin Labelout LSPname
10.0.0.7        10.0.0.1        Up    0  1 SE  -       299808   to-PE3
Total 1 displayed, Up 1, Down 0""",
        "What is the outgoing label for the LSP to-PE3?",
        [("299808", True), ("10.0.0.7", False), ("10.0.0.1", False), ("No label", False)],
        "The Labelout column shows 299808.",
        "4.0 MPLS",
    ),
    (
        """user@PE> show l2vpn connections
Layer-2 VPN connections:

Legend for connection status (St)
EI -- encapsulation invalid      NC -- interface encapsulation not CCC/TCC/VPLS
EM -- encapsulation mismatch     WE -- interface and instance encaps not same
VC-Dn -- Virtual circuit down    NP -- hardware interface not present

Connection name             Site       St                  ID last up
ge-0/0/2.0                  1          DN                  --""",
        "What is the status of the L2VPN connection?",
        [("Up", False), ("Down", True), ("Partial", False), ("Unknown", False)],
        "The St column shows DN, which means down.",
        "6.0 L2VPN",
    ),
    (
        """user@PE> show multicast route
Family: INET

Group           Source          RP              Flags
239.1.1.1       10.0.0.10       10.0.0.5        SPT
239.2.2.2       *               10.0.0.5        RPT""",
        "Which group is using the shortest-path tree?",
        [("239.1.1.1", True), ("239.2.2.2", False), ("Both", False), ("Neither", False)],
        "The Flags column shows SPT for 239.1.1.1.",
        "7.0 Multicast",
    ),
]
