"""Content pools for Juniper JNCIA-Junos JN0-106 question generation."""

JNCIA_SECTIONS = {
    "1.0 Junos OS Fundamentals": ("1.0 Junos OS Fundamentals", 16.67),
    "1.1 Software architecture": ("1.0 Junos OS Fundamentals", 16.67),
    "1.2 Control and forwarding planes": ("1.0 Junos OS Fundamentals", 16.67),
    "1.3 Traffic processing": ("1.0 Junos OS Fundamentals", 16.67),
    "2.0 User Interfaces": ("2.0 User Interfaces", 16.67),
    "2.1 CLI modes": ("2.0 User Interfaces", 16.67),
    "2.2 Help and navigation": ("2.0 User Interfaces", 16.67),
    "2.3 Configuration mode": ("2.0 User Interfaces", 16.67),
    "3.0 Configuration Basics": ("3.0 Configuration Basics", 16.67),
    "3.1 Factory-default config": ("3.0 Configuration Basics", 16.67),
    "3.2 Candidate vs active": ("3.0 Configuration Basics", 16.67),
    "3.3 Configuration statements": ("3.0 Configuration Basics", 16.67),
    "3.4 Rescue config": ("3.0 Configuration Basics", 16.67),
    "4.0 Operational Monitoring and Maintenance": ("4.0 Operational Monitoring and Maintenance", 16.67),
    "4.1 Monitoring commands": ("4.0 Operational Monitoring and Maintenance", 16.67),
    "4.2 Maintenance": ("4.0 Operational Monitoring and Maintenance", 16.67),
    "5.0 Routing Fundamentals": ("5.0 Routing Fundamentals", 16.67),
    "5.1 Routing concepts": ("5.0 Routing Fundamentals", 16.67),
    "5.2 Routing table": ("5.0 Routing Fundamentals", 16.67),
    "5.3 Static routes": ("5.0 Routing Fundamentals", 16.67),
    "6.0 Routing Policy and Firewall Filters": ("6.0 Routing Policy and Firewall Filters", 16.67),
    "6.1 Routing policy": ("6.0 Routing Policy and Firewall Filters", 16.67),
    "6.2 Firewall filters": ("6.0 Routing Policy and Firewall Filters", 16.67),
}

JNCIA_CATEGORIES = {
    "1.1 Software architecture": "Junos OS software architecture concepts",
    "1.2 Control and forwarding planes": "control or forwarding plane concepts",
    "1.3 Traffic processing": "traffic processing concepts",
    "2.1 CLI modes": "Junos CLI modes",
    "2.2 Help and navigation": "CLI help and navigation features",
    "2.3 Configuration mode": "configuration mode features",
    "3.1 Factory-default config": "factory-default configuration concepts",
    "3.2 Candidate vs active": "candidate versus active configuration concepts",
    "3.3 Configuration statements": "configuration statement concepts",
    "3.4 Rescue config": "rescue configuration concepts",
    "4.1 Monitoring commands": "operational monitoring commands",
    "4.2 Maintenance": "maintenance procedures",
    "5.1 Routing concepts": "routing fundamentals",
    "5.2 Routing table": "routing table concepts",
    "5.3 Static routes": "static routing concepts",
    "6.1 Routing policy": "routing policy concepts",
    "6.2 Firewall filters": "firewall filter concepts",
}

JNCIA_TERMS = [
    ("Junos OS", "The network operating system used on Juniper routers, switches, and firewalls.", "1.1 Software architecture"),
    ("RE", "Routing Engine; runs the control plane and maintains the routing table.", "1.2 Control and forwarding planes"),
    ("PFE", "Packet Forwarding Engine; handles packet forwarding in the data plane.", "1.2 Control and forwarding planes"),
    ("Control plane", "The logical plane that manages routing protocols and device management.", "1.2 Control and forwarding planes"),
    ("Forwarding plane", "The logical plane that forwards traffic based on the forwarding table.", "1.2 Control and forwarding planes"),
    ("JTAC", "Juniper Networks Technical Assistance Center.", "1.1 Software architecture"),
    ("J-Web", "Web-based graphical user interface for Junos devices.", "2.0 User Interfaces"),
    ("CLI", "Command Line Interface for Junos devices.", "2.0 User Interfaces"),
    ("Operational mode", "The default CLI mode for monitoring and troubleshooting.", "2.1 CLI modes"),
    ("Configuration mode", "The CLI mode for making configuration changes.", "2.1 CLI modes"),
    ("Root login", "The superuser account with full permissions.", "2.1 CLI modes"),
    ("Configuration candidate", "The uncommitted configuration being edited.", "3.2 Candidate vs active"),
    ("Active configuration", "The currently running configuration on the device.", "3.2 Candidate vs active"),
    ("Commit", "The process of activating the candidate configuration.", "3.2 Candidate vs active"),
    ("Rollback", "Restoring a previous configuration.", "3.2 Candidate vs active"),
    ("Rescue configuration", "A known-good configuration stored for emergencies.", "3.4 Rescue config"),
    ("Factory-default", "The original configuration shipped with the device.", "3.1 Factory-default config"),
    ("Hierarchy", "The tree-like structure of Junos configuration.", "3.3 Configuration statements"),
    ("Stanza", "A section of Junos configuration at a specific hierarchy level.", "3.3 Configuration statements"),
    ("Set command", "A CLI command to add or modify configuration.", "3.3 Configuration statements"),
    ("Delete command", "A CLI command to remove configuration.", "3.3 Configuration statements"),
    ("Deactivate", "To disable a configuration statement without deleting it.", "3.3 Configuration statements"),
    ("Protect", "To prevent a configuration statement from being deleted.", "3.3 Configuration statements"),
    ("Annotation", "A comment added to a configuration statement.", "3.3 Configuration statements"),
    ("Load merge", "Merging a configuration file with the candidate config.", "3.3 Configuration statements"),
    ("Load replace", "Replacing part of the candidate config with a file.", "3.3 Configuration statements"),
    ("Load override", "Replacing the entire candidate config with a file.", "3.3 Configuration statements"),
    ("Show configuration", "Command to display the active or candidate configuration.", "3.3 Configuration statements"),
    ("Commit confirmed", "A commit that automatically rolls back unless confirmed.", "3.2 Candidate vs active"),
    ("Commit synchronize", "Committing the configuration on both Routing Engines.", "3.2 Candidate vs active"),
    ("Commit and-quit", "Committing the configuration and exiting configuration mode.", "3.2 Candidate vs active"),
    ("Interface", "A network port on a Junos device.", "4.1 Monitoring commands"),
    ("Unit", "A logical subinterface on a Junos physical interface.", "4.1 Monitoring commands"),
    ("Family inet", "IPv4 protocol family on an interface.", "4.1 Monitoring commands"),
    ("Family inet6", "IPv6 protocol family on an interface.", "4.1 Monitoring commands"),
    ("Loopback interface", "Logical interface lo0 used for management and routing.", "4.1 Monitoring commands"),
    ("Management interface", "Out-of-band interface such as fxp0 or em0.", "4.1 Monitoring commands"),
    ("Traceoptions", "Junos feature for detailed protocol debugging.", "4.1 Monitoring commands"),
    ("Syslog", "System logging on Junos.", "4.1 Monitoring commands"),
    ("NTP", "Network Time Protocol configuration on Junos.", "4.2 Maintenance"),
    ("SNMP", "Simple Network Management Protocol on Junos.", "4.2 Maintenance"),
    ("Login class", "A user permission template on Junos.", "4.2 Maintenance"),
    ("User account", "Local login account on a Junos device.", "4.2 Maintenance"),
    ("Host-name", "The device name configured in Junos.", "4.2 Maintenance"),
    ("Name server", "DNS server configured on Junos.", "4.2 Maintenance"),
    ("Route", "A path to a destination network.", "5.1 Routing concepts"),
    ("Routing table", "The control-plane table of known routes.", "5.2 Routing table"),
    ("Forwarding table", "The data-plane table used to forward packets.", "5.2 Routing table"),
    ("RIB", "Routing Information Base; another name for the routing table.", "5.2 Routing table"),
    ("FIB", "Forwarding Information Base; another name for the forwarding table.", "5.2 Routing table"),
    ("Longest match", "Selecting the most specific route for a destination.", "5.1 Routing concepts"),
    ("Default route", "A route used when no more specific route matches.", "5.1 Routing concepts"),
    ("Static route", "A manually configured route.", "5.3 Static routes"),
    ("Aggregate route", "A summarized route in Junos.", "5.3 Static routes"),
    ("Generated route", "A route in Junos that depends on contributing routes.", "5.3 Static routes"),
    ("Martian address", "A route that Junos rejects by default.", "5.3 Static routes"),
    ("Routing instance", "A virtual router with its own routing tables.", "5.1 Routing concepts"),
    ("RIB group", "A Junos feature to share routes between routing tables.", "5.2 Routing table"),
    ("Routing policy", "Rules to control route advertisement and acceptance.", "6.1 Routing policy"),
    ("Import policy", "A policy applied to incoming routing information.", "6.1 Routing policy"),
    ("Export policy", "A policy applied to outgoing routing information.", "6.1 Routing policy"),
    ("Term", "A match/action block within a routing policy or firewall filter.", "6.1 Routing policy"),
    ("From", "Match conditions in a policy or filter term.", "6.1 Routing policy"),
    ("Then", "Action statements in a policy or filter term.", "6.1 Routing policy"),
    ("Accept", "Action to permit a route or packet.", "6.1 Routing policy"),
    ("Reject", "Action to discard a route or packet.", "6.1 Routing policy"),
    ("Next policy", "Action to continue evaluating subsequent policy terms.", "6.1 Routing policy"),
    ("Next term", "Action to continue to the next term in a policy.", "6.1 Routing policy"),
    ("Default policy", "The implicit policy at the end of a policy chain.", "6.1 Routing policy"),
    ("Prefix list", "A list of IP prefixes used in policies or filters.", "6.1 Routing policy"),
    ("AS path", "The sequence of autonomous systems a BGP route traversed.", "6.1 Routing policy"),
    ("Community", "A BGP attribute used to group routes.", "6.1 Routing policy"),
    ("Firewall filter", "A Junos packet filter applied to interfaces.", "6.2 Firewall filters"),
    ("Filter term", "A match/action block within a firewall filter.", "6.2 Firewall filters"),
    ("Input filter", "A firewall filter applied to incoming packets.", "6.2 Firewall filters"),
    ("Output filter", "A firewall filter applied to outgoing packets.", "6.2 Firewall filters"),
    ("Loss priority", "A firewall filter action marking traffic for drop priority.", "6.2 Firewall filters"),
    ("Forwarding-class", "A firewall filter action assigning traffic to a class.", "6.2 Firewall filters"),
    ("Policer", "A Junos feature limiting traffic rate.", "6.2 Firewall filters"),
    ("Classifier", "A Junos feature mapping traffic to forwarding classes.", "6.2 Firewall filters"),
]

JNCIA_COMMANDS = [
    ("show version", "displays Junos OS version and hardware details", "4.1 Monitoring commands"),
    ("show chassis hardware", "displays hardware inventory", "4.1 Monitoring commands"),
    ("show interfaces", "displays interface status and statistics", "4.1 Monitoring commands"),
    ("show interfaces terse", "displays brief interface status", "4.1 Monitoring commands"),
    ("show route", "displays the routing table", "5.2 Routing table"),
    ("show route forwarding-table", "displays the forwarding table", "5.2 Routing table"),
    ("show configuration", "displays the active configuration", "3.3 Configuration statements"),
    ("show | compare", "displays differences between candidate and active config", "3.2 Candidate vs active"),
    ("configure", "enters configuration mode", "2.1 CLI modes"),
    ("edit", "navigates to a configuration hierarchy level", "2.3 Configuration mode"),
    ("up", "moves up one configuration hierarchy level", "2.3 Configuration mode"),
    ("top", "moves to the top of the configuration hierarchy", "2.3 Configuration mode"),
    ("exit", "exits the current mode or hierarchy level", "2.2 Help and navigation"),
    ("commit", "activates the candidate configuration", "3.2 Candidate vs active"),
    ("commit confirmed", "commits with automatic rollback if not confirmed", "3.2 Candidate vs active"),
    ("rollback", "loads a previous configuration as the candidate", "3.2 Candidate vs active"),
    ("rollback rescue", "loads the rescue configuration", "3.4 Rescue config"),
    ("request system reboot", "reboots the device", "4.2 Maintenance"),
    ("request system halt", "powers off the device", "4.2 Maintenance"),
    ("request system snapshot", "backs up the system to alternate media", "4.2 Maintenance"),
    ("load merge", "merges a configuration file into the candidate", "3.3 Configuration statements"),
    ("load replace", "replaces a configuration hierarchy from a file", "3.3 Configuration statements"),
    ("load override", "replaces the entire candidate config from a file", "3.3 Configuration statements"),
    ("save", "saves the candidate configuration to a file", "3.3 Configuration statements"),
    ("set", "adds or modifies a configuration statement", "3.3 Configuration statements"),
    ("delete", "removes a configuration statement", "3.3 Configuration statements"),
    ("deactivate", "disables a configuration statement", "3.3 Configuration statements"),
    ("activate", "re-enables a deactivated configuration statement", "3.3 Configuration statements"),
    ("protect", "prevents a configuration statement from being deleted", "3.3 Configuration statements"),
    ("unprotect", "allows a protected statement to be deleted", "3.3 Configuration statements"),
    ("show log messages", "displays system log messages", "4.1 Monitoring commands"),
    ("monitor interface", "monitors real-time interface statistics", "4.1 Monitoring commands"),
    ("ping", "tests reachability to a destination", "4.1 Monitoring commands"),
    ("traceroute", "traces the path to a destination", "4.1 Monitoring commands"),
    ("show system uptime", "displays system uptime", "4.1 Monitoring commands"),
    ("show system processes", "displays running processes", "4.1 Monitoring commands"),
    ("show system storage", "displays file system usage", "4.2 Maintenance"),
    ("request support information", "collects support information", "4.2 Maintenance"),
]

JNCIA_COMPARISONS = [
    ("Operational mode", "Configuration mode", "Operational mode is for monitoring; configuration mode is for editing the candidate config.", "2.1 CLI modes"),
    ("Control plane", "Forwarding plane", "The control plane builds routing tables; the forwarding plane forwards packets.", "1.2 Control and forwarding planes"),
    ("Candidate config", "Active config", "Candidate config is being edited; active config is currently running.", "3.2 Candidate vs active"),
    ("Set command", "Delete command", "Set adds configuration; delete removes configuration.", "3.3 Configuration statements"),
    ("Rollback", "Commit", "Rollback restores a previous config; commit activates the candidate config.", "3.2 Candidate vs active"),
    ("Routing table", "Forwarding table", "The routing table is control-plane; the forwarding table is data-plane.", "5.2 Routing table"),
    ("Import policy", "Export policy", "Import policy filters received routes; export policy filters advertised routes.", "6.1 Routing policy"),
    ("Accept", "Reject", "Accept permits a route/packet; reject discards it.", "6.1 Routing policy"),
    ("Static route", "Aggregate route", "A static route is manually configured; an aggregate route summarizes multiple routes.", "5.3 Static routes"),
    ("Input filter", "Output filter", "Input filter processes incoming packets; output filter processes outgoing packets.", "6.2 Firewall filters"),
]

JNCIA_SCENARIOS = [
    ("An engineer enters configuration mode and makes several changes.", "The engineer wants to verify the changes before committing.", "Use 'show | compare' to display differences between candidate and active config.", "3.2 Candidate vs active"),
    ("A Junos device loses network connectivity after a recent configuration change.", "The previous configuration was known-good.", "Load and commit a rescue configuration or rollback to a previous commit.", "3.4 Rescue config"),
    ("A router receives a packet destined to 203.0.113.50.", "The routing table has 203.0.113.0/24 and 203.0.113.0/26.", "The router uses the /26 route because it has the longest match.", "5.1 Routing concepts"),
    ("An engineer configures a static route with next-hop 10.1.1.1.", "The next-hop is not reachable.", "The static route remains inactive until the next-hop becomes reachable.", "5.3 Static routes"),
    ("A routing policy has multiple terms.", "A route matches the first term's from conditions.", "The then action of the first matching term is applied.", "6.1 Routing policy"),
    ("A firewall filter is applied to an interface as input.", "A packet matches a term with action 'discard'.", "The packet is silently discarded.", "6.2 Firewall filters"),
    ("An engineer wants to temporarily disable an interface configuration.", "The configuration should remain in the config file.", "Use the 'deactivate' command on the interface.", "3.3 Configuration statements"),
    ("A configuration change must be tested remotely.", "If the change causes a disconnect, the device should revert automatically.", "Use 'commit confirmed' with a timeout.", "3.2 Candidate vs active"),
    ("A Junos device has two Routing Engines.", "A configuration change is committed.", "Use 'commit synchronize' to apply the config to both Routing Engines.", "3.2 Candidate vs active"),
    ("An operator wants to see only IPv4 routes in the routing table.", "The command 'show route' displays all routes.", "Use 'show route table inet.0' or 'show route protocol static'.", "5.2 Routing table"),
    ("A packet arrives on an interface with a firewall filter.", "The packet does not match any term in the filter.", "The default action at the end of the filter is applied.", "6.2 Firewall filters"),
    ("An engineer configures 'set system syslog file messages any info'.", "A message with severity notice is generated.", "The message is logged to /var/log/messages because notice is more severe than info.", "4.1 Monitoring commands"),
]

JNCIA_SIMLETS = [
    (
        """user@router> show route
inet.0: 4 destinations, 4 routes (4 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

10.0.0.0/24        *[Static/5] 00:10:12
                    > to 192.168.1.1 via ge-0/0/0.0
192.168.1.0/24     *[Direct/0] 00:15:30
                    > via ge-0/0/0.0
192.168.1.10/32    *[Local/0] 00:15:30
                      Local via ge-0/0/0.0
0.0.0.0/0          *[Static/5] 00:10:12
                    > to 192.168.1.1 via ge-0/0/0.0""",
        "What is the next-hop for traffic destined to 10.0.0.50?",
        [("192.168.1.1", True), ("10.0.0.1", False), ("192.168.1.10", False), ("0.0.0.0", False)],
        "The 10.0.0.0/24 static route points to next-hop 192.168.1.1.",
        "5.3 Static routes",
    ),
    (
        """user@router> show configuration interfaces ge-0/0/0
unit 0 {
    family inet {
        address 192.168.1.10/24;
    }
}""",
        "Which IP address is configured on ge-0/0/0.0?",
        [("192.168.1.0/24", False), ("192.168.1.10/24", True), ("192.168.1.10/32", False), ("10.0.0.1/24", False)],
        "The interface is configured with address 192.168.1.10/24.",
        "4.1 Monitoring commands",
    ),
    (
        """user@router> show configuration policy-options policy-statement EXPORT
term ACCEPT-STATIC {
    from protocol static;
    then accept;
}
term REJECT-ALL {
    then reject;
}""",
        "What happens to a directly connected route in this policy?",
        [("It is accepted", False), ("It is rejected by REJECT-ALL", True), ("It is accepted by default", False), ("The policy returns an error", False)],
        "Only static routes match ACCEPT-STATIC. Directly connected routes do not match and fall through to REJECT-ALL.",
        "6.1 Routing policy",
    ),
    (
        """user@router> show system uptime
current time: 2026-06-17 11:00:00 UTC
System booted: 2026-06-10 09:00:00 UTC (7d 02:00 ago)
Protocols started: 2026-06-10 09:05:00 UTC (7d 01:55 ago)""",
        "How long ago did the system boot?",
        [("1 hour", False), ("7 days 2 hours", True), ("7 days 1 hour 55 minutes", False), ("10 days", False)],
        "The output shows 'System booted: ... (7d 02:00 ago)'.",
        "4.1 Monitoring commands",
    ),
    (
        """user@router> show firewall
Filter: BLOCK-TELNET
Counters:
Name                                                Bytes              Packets
term-deny                                              0                    0
Policers:
Name                                                Bytes              Packets
telnet-policer                                         0                    0""",
        "Which feature is being shown?",
        [("A routing policy", False), ("A firewall filter", True), ("An interface queue", False), ("A syslog configuration", False)],
        "The output shows a firewall filter named BLOCK-TELNET with counters and policers.",
        "6.2 Firewall filters",
    ),
    (
        """user@router> show route forwarding-table
Routing table: default.inet
Internet:
Destination        Type RtRef Next hop           Type Index NhRef Netif
default            user     0 192.168.1.1        ucst     5     2 ge-0/0/0.0
10.0.0.0/24        user     0 192.168.1.1        ucst     5     2 ge-0/0/0.0
192.168.1.0/24     user     0 192.168.1.1        ucst     5     2 ge-0/0/0.0
192.168.1.10/32    intf     0 192.168.1.10       locl     4     2 ge-0/0/0.0""",
        "Which next-hop is used for traffic to 10.0.0.50?",
        [("192.168.1.10", False), ("192.168.1.1", True), ("10.0.0.1", False), ("default", False)],
        "The forwarding table shows 10.0.0.0/24 uses next-hop 192.168.1.1.",
        "5.2 Routing table",
    ),
]

JNCIA_DRAG_DROP_POOLS = [
    (
        "2.1 CLI modes",
        "Match the Junos CLI mode to its prompt symbol.",
        [
            ("Operational mode", "user@router>"),
            ("Configuration mode", "user@router#"),
            ("Configuration mode below top", "[edit]") ,
        ],
    ),
    (
        "3.2 Candidate vs active",
        "Order the Junos configuration commit rollback numbers from newest to oldest.",
        [
            ("0", "Current active config"),
            ("1", "One commit ago"),
            ("2", "Two commits ago"),
            ("49", "Oldest stored rollback"),
        ],
    ),
    (
        "5.2 Routing table",
        "Match the Junos routing table name to its purpose.",
        [
            ("inet.0", "IPv4 unicast"),
            ("inet.3", "IPv4 MPLS"),
            ("inet6.0", "IPv6 unicast"),
            ("mpls.0", "MPLS label switching"),
        ],
    ),
    (
        "6.1 Routing policy",
        "Match the routing policy action to its effect.",
        [
            ("accept", "Permit the route"),
            ("reject", "Discard the route"),
            ("next policy", "Evaluate next policy"),
            ("next term", "Evaluate next term"),
        ],
    ),
]

JNCIA_FILL_BLANK_POOLS = [
    ("2.1 CLI modes", "To enter configuration mode from operational mode, use the __________ command.", "configure", ["edit", "commit", "set", "show"]),
    ("3.2 Candidate vs active", "To activate the candidate configuration, use the __________ command.", "commit", ["apply", "save", "rollback", "load"]),
    ("3.2 Candidate vs active", "A commit that automatically rolls back unless confirmed is called __________.", "commit confirmed", ["commit synchronize", "commit and-quit", "rollback", "rescue"]),
    ("3.4 Rescue config", "To load the known-good emergency configuration, use rollback __________.", "rescue", ["0", "1", "49", "factory-default"]),
    ("3.3 Configuration statements", "The command to add a configuration statement in configuration mode is __________.", "set", ["get", "put", "delete", "show"]),
    ("4.1 Monitoring commands", "The command to display brief interface status is show interfaces __________.", "terse", ["detail", "extensive", "brief", "media"]),
    ("5.2 Routing table", "The Junos IPv4 unicast routing table is named __________.", "inet.0", ["inet.3", "inet6.0", "mpls.0", "iso.0"]),
    ("5.3 Static routes", "A static route with a next-hop that is not reachable appears as __________ in the routing table.", "inactive", ["active", "hidden", "holddown", "resolved"]),
    ("6.1 Routing policy", "In a policy term, match conditions are configured under the __________ statement.", "from", ["then", "to", "where", "match"]),
    ("6.1 Routing policy", "In a policy term, actions are configured under the __________ statement.", "then", ["from", "when", "if", "action"]),
    ("6.2 Firewall filters", "A firewall filter applied to incoming packets is an __________ filter.", "input", ["output", "ingress", "egress", "forward"]),
]

JNCIA_MULTIPLE_CHOICE_POOLS = [
    (
        "1.0 Junos OS Fundamentals",
        "Which components are part of the Junos OS control plane? (Choose two.)",
        ["Routing Engine", "Routing protocols"],
        ["Packet Forwarding Engine", "Interface queues", "ASICs", "Physical ports"],
        "The Routing Engine runs the control plane, including routing protocols. The PFE is the data plane.",
    ),
    (
        "2.0 User Interfaces",
        "Which methods can be used to access a Junos device? (Choose two.)",
        ["SSH", "J-Web"],
        ["Telnet if enabled", "Console", "SNMP only", "BGP"],
        "Junos devices can be accessed via SSH, Telnet, console, and J-Web.",
    ),
    (
        "3.0 Configuration Basics",
        "Which statements are true about the Junos candidate configuration? (Choose two.)",
        ["It is edited in configuration mode", "It is activated by commit"],
        ["It is the currently running config", "It cannot be viewed", "It is stored in /var/tmp", "It is loaded with rollback"],
        "The candidate configuration is edited in configuration mode and activated with commit. The active configuration is currently running.",
    ),
    (
        "4.0 Operational Monitoring and Maintenance",
        "Which are valid Junos syslog severity levels? (Choose two.)",
        ["info", "notice"],
        ["normal", "high", "low", "debug is valid too"],
        "Junos syslog severities include any, debug, info, notice, warning, error, critical, alert, emergency.",
    ),
    (
        "5.0 Routing Fundamentals",
        "Which factors are used to select the active route in Junos? (Choose two.)",
        ["Route preference", "Metric"],
        ["Interface speed", "Hostname", "MAC address", "DNS name"],
        "Junos uses route preference (administrative distance) and metric to select active routes.",
    ),
    (
        "6.0 Routing Policy and Firewall Filters",
        "Which actions can be used in a routing policy then statement? (Choose two.)",
        ["accept", "reject"],
        ["forward", "drop", "permit", "deny"],
        "Routing policy actions include accept, reject, next policy, and next term. Forward/drop are firewall filter actions.",
    ),
]
