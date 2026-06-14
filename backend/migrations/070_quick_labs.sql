-- +goose Up
-- +goose StatementBegin

-- ============================================================
-- Migration 070: Quick Labs Schema + Seed
-- ============================================================
-- Quick Labs are self-paced PNETlab-compatible exercises with
-- tasks, hints, answers, and explanations. No live containers.

CREATE TABLE IF NOT EXISTS quick_labs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    difficulty SMALLINT NOT NULL CHECK (difficulty >= 1 AND difficulty <= 5),
    estimated_minutes INT NOT NULL DEFAULT 15,
    level VARCHAR(20) NOT NULL DEFAULT 'JNCIA' CHECK (level IN ('JNCIA', 'JNCIP', 'JNCIE', 'CCNA', 'CCNP', 'CCIE')),
    technology VARCHAR(50) NOT NULL,
    topology_svg TEXT,
    pnetlab_instructions TEXT NOT NULL DEFAULT '',
    tasks JSONB NOT NULL DEFAULT '[]',
    hints JSONB NOT NULL DEFAULT '[]',
    answers JSONB NOT NULL DEFAULT '[]',
    explanations JSONB NOT NULL DEFAULT '[]',
    solution_commands JSONB NOT NULL DEFAULT '[]',
    prerequisite_topics TEXT[] DEFAULT '{}',
    track_id UUID REFERENCES tracks(id) ON DELETE SET NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_quick_labs_technology ON quick_labs(technology);
CREATE INDEX IF NOT EXISTS idx_quick_labs_level ON quick_labs(level);
CREATE INDEX IF NOT EXISTS idx_quick_labs_track_id ON quick_labs(track_id);
CREATE INDEX IF NOT EXISTS idx_quick_labs_difficulty ON quick_labs(difficulty);

-- ============================================================
-- SEED DATA: Quick Labs from Easy to Hard
-- ============================================================

-- Quick Lab 01: Interface Configuration (Difficulty 1, JNCIA)
INSERT INTO quick_labs (
    slug, title, description, difficulty, estimated_minutes, level, technology,
    topology_svg, pnetlab_instructions, tasks, hints, answers, explanations, solution_commands,
    prerequisite_topics, track_id
) VALUES (
    'ql-interface-config',
    'Interface Configuration Basics',
    'Learn to configure basic interface parameters on JunOS: IP addressing, descriptions, and status verification.',
    1, 10, 'JNCIA', 'junos-cli',
    '<svg viewBox="0 0 200 120" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="200" height="120" fill="var(--svg-bg)" rx="8"/><g transform="translate(70,30)"><rect x="0" y="0" width="60" height="40" rx="4" fill="var(--svg-device-router)" opacity="0.9"/><circle cx="15" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="30" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="45" cy="15" r="3" fill="var(--svg-line-warning)"/><text x="30" y="32" text-anchor="middle" fill="var(--svg-bg)" font-size="6" font-family="Geist Mono, monospace">R1</text></g><text x="100" y="100" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="5" font-family="Geist Mono, monospace">Single Router</text></svg>',
    '## PNETlab Setup
1. Create a new lab in PNETlab
2. Add one cRPD or vMX node
3. Connect to the node via SSH (root/NetCert123)
4. No additional nodes required',
    '[
  {"order":1,"title":"Configure Interface IP","description":"Configure ge-0/0/0.0 with IP 192.168.1.1/24 and add description ''LAN Segment''","verification_commands":["show interfaces ge-0/0/0 terse","show configuration interfaces ge-0/0/0"],"expected_output_summary":"Interface ge-0/0/0.0 should show up/up with IP 192.168.1.1/24 and description ''LAN Segment''"},
  {"order":2,"title":"Verify Interface Status","description":"Use operational mode commands to verify the interface is administratively up","verification_commands":["show interfaces ge-0/0/0.0"],"expected_output_summary":"Status should show ''Administratively up'' and Link ''up''"}
]'::jsonb,
    '[
  {"order":1,"title":"Configuration Mode","content":"Use ''configure'' to enter configuration mode. The prompt changes from > to #."},
  {"order":2,"title":"Interface Syntax","content":"JunOS interface syntax: set interfaces ge-0/0/0 unit 0 family inet address 192.168.1.1/24"}
]'::jsonb,
    '[
  {"order":1,"task_order":1,"content":"configure | set interfaces ge-0/0/0 unit 0 description ''LAN Segment'' | set interfaces ge-0/0/0 unit 0 family inet address 192.168.1.1/24 | commit and-quit"},
  {"order":2,"task_order":2,"content":"show interfaces ge-0/0/0.0 | match ''Admin|Link|Description''"}
]'::jsonb,
    '[
  {"order":1,"title":"Interface Configuration Explained","content":"In JunOS, interface configuration is hierarchical. The ''unit 0'' represents the logical interface (equivalent to subinterface .0). The ''family inet'' specifies IPv4 addressing. Descriptions help with documentation and troubleshooting."}
]'::jsonb,
    '[
  {"order":1,"task_order":1,"commands":["configure","set interfaces ge-0/0/0 unit 0 description ''LAN Segment''","set interfaces ge-0/0/0 unit 0 family inet address 192.168.1.1/24","commit and-quit"]},
  {"order":2,"task_order":2,"commands":["show interfaces ge-0/0/0.0"],"expected_output":"Administratively up, Link up"}
]'::jsonb,
    ARRAY['JunOS CLI Basics', 'Interface Configuration'],
    'a0000000-0000-0000-0000-000000000001'
)
ON CONFLICT (slug) DO NOTHING;

-- Quick Lab 02: Static Routing (Difficulty 1, JNCIA)
INSERT INTO quick_labs (
    slug, title, description, difficulty, estimated_minutes, level, technology,
    topology_svg, pnetlab_instructions, tasks, hints, answers, explanations, solution_commands,
    prerequisite_topics, track_id
) VALUES (
    'ql-static-routing',
    'Static Routing Fundamentals',
    'Configure static routes between two routers and verify reachability.',
    1, 15, 'JNCIA', 'routing',
    '<svg viewBox="0 0 300 120" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="300" height="120" fill="var(--svg-bg)" rx="8"/><g transform="translate(40,30)"><rect x="0" y="0" width="60" height="40" rx="4" fill="var(--svg-device-router)" opacity="0.9"/><circle cx="15" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="30" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="45" cy="15" r="3" fill="var(--svg-line-active)"/><text x="30" y="32" text-anchor="middle" fill="var(--svg-bg)" font-size="6" font-family="Geist Mono, monospace">R1</text></g><g transform="translate(200,30)"><rect x="0" y="0" width="60" height="40" rx="4" fill="var(--svg-device-router)" opacity="0.9"/><circle cx="15" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="30" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="45" cy="15" r="3" fill="var(--svg-line-warning)"/><text x="30" y="32" text-anchor="middle" fill="var(--svg-bg)" font-size="6" font-family="Geist Mono, monospace">R2</text></g><line x1="100" y1="50" x2="200" y2="50" stroke="var(--svg-line-active)" stroke-width="2.5" stroke-linecap="round"/><text x="150" y="45" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="4" font-family="Geist Mono, monospace">10.0.12.0/30</text><text x="150" y="100" text-anchor="middle" fill="var(--svg-text)" font-size="6" font-family="Geist, sans-serif" font-weight="600">Static Routing Lab</text></svg>',
    '## PNETlab Setup
1. Create a new lab
2. Add two cRPD nodes: R1 and R2
3. Connect ge-0/0/0 on R1 to ge-0/0/0 on R2
4. IPs: R1=10.0.12.1/30, R2=10.0.12.2/30
5. Add loopbacks: R1=1.1.1.1/32, R2=2.2.2.2/32',
    '[
  {"order":1,"title":"Configure Direct Connectivity","description":"Ensure R1 and R2 can ping each other on the directly connected link 10.0.12.0/30","verification_commands":["ping 10.0.12.2 count 5"],"expected_output_summary":"5 packets transmitted, 5 received, 0% packet loss"},
  {"order":2,"title":"Add Static Route on R1","description":"Configure a static route on R1 to reach R2 loopback (2.2.2.2/32) via next-hop 10.0.12.2","verification_commands":["show route 2.2.2.2","ping 2.2.2.2 count 5"],"expected_output_summary":"Route to 2.2.2.2/32 should show via 10.0.12.2 and ping should succeed"},
  {"order":3,"title":"Add Return Static Route on R2","description":"Configure reciprocal static route on R2 for R1 loopback (1.1.1.1/32)","verification_commands":["show route 1.1.1.1","ping 1.1.1.1 count 5 source 2.2.2.2"],"expected_output_summary":"Bidirectional reachability between loopbacks"}
]'::jsonb,
    '[
  {"order":1,"title":"Static Route Syntax","content":"JunOS: set routing-options static route DESTINATION next-hop NEXTHOP"},
  {"order":2,"title":"Route Verification","content":"Use ''show route PREFIX'' to verify a specific route exists in the routing table."},
  {"order":3,"title":"Ping Options","content":"Use ''ping COUNT 5'' to limit packets. Use ''source INTERFACE'' to specify source IP."}
]'::jsonb,
    '[
  {"order":1,"task_order":1,"content":"ping 10.0.12.2 count 5"},
  {"order":2,"task_order":2,"content":"configure | set routing-options static route 2.2.2.2/32 next-hop 10.0.12.2 | commit and-quit"},
  {"order":3,"task_order":3,"content":"configure | set routing-options static route 1.1.1.1/32 next-hop 10.0.12.1 | commit and-quit"}
]'::jsonb,
    '[
  {"order":1,"title":"Why Static Routes?","content":"Static routes are manually configured and have AD (Administrative Distance) of 5 in JunOS. They are simple but do not scale. Best used for default routes, stub networks, or when routing policy requires exact control."},
  {"order":2,"title":"Next-Hop Resolution","content":"JunOS validates next-hop reachability before installing static routes. If the next-hop is unreachable, the route stays hidden. Use ''show route hidden'' to see inactive routes."}
]'::jsonb,
    '[
  {"order":1,"task_order":1,"commands":["ping 10.0.12.2 count 5"],"expected_output":"0% packet loss"},
  {"order":2,"task_order":2,"commands":["configure","set routing-options static route 2.2.2.2/32 next-hop 10.0.12.2","commit and-quit"],"expected_output":"commit complete"},
  {"order":3,"task_order":3,"commands":["configure","set routing-options static route 1.1.1.1/32 next-hop 10.0.12.1","commit and-quit","ping 1.1.1.1 count 5 source 2.2.2.2"],"expected_output":"0% packet loss"}
]'::jsonb,
    ARRAY['IP Addressing', 'JunOS CLI', 'Basic Routing'],
    'a0000000-0000-0000-0000-000000000001'
)
ON CONFLICT (slug) DO NOTHING;

-- Quick Lab 03: OSPF Single Area (Difficulty 2, JNCIP)
INSERT INTO quick_labs (
    slug, title, description, difficulty, estimated_minutes, level, technology,
    topology_svg, pnetlab_instructions, tasks, hints, answers, explanations, solution_commands,
    prerequisite_topics, track_id
) VALUES (
    'ql-ospf-single-area',
    'OSPF Single-Area Troubleshooting',
    'Troubleshoot and fix OSPF adjacency issues in a 3-router topology. Identify missing configuration and verify LSDB synchronization.',
    2, 25, 'JNCIP', 'ospf',
    '<svg viewBox="0 0 400 200" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="400" height="200" fill="var(--svg-bg)" rx="8"/><g transform="translate(50,30)"><rect x="0" y="0" width="60" height="40" rx="4" fill="var(--svg-device-router)" opacity="0.9"/><circle cx="15" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="30" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="45" cy="15" r="3" fill="var(--svg-line-down)"/><text x="30" y="32" text-anchor="middle" fill="var(--svg-bg)" font-size="6" font-family="Geist Mono, monospace">R1</text></g><g transform="translate(170,30)"><rect x="0" y="0" width="60" height="40" rx="4" fill="var(--svg-device-router)" opacity="0.9"/><circle cx="15" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="30" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="45" cy="15" r="3" fill="var(--svg-line-active)"/><text x="30" y="32" text-anchor="middle" fill="var(--svg-bg)" font-size="6" font-family="Geist Mono, monospace">R2</text></g><g transform="translate(290,30)"><rect x="0" y="0" width="60" height="40" rx="4" fill="var(--svg-device-router)" opacity="0.9"/><circle cx="15" cy="15" r="3" fill="var(--svg-line-down)"/><circle cx="30" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="45" cy="15" r="3" fill="var(--svg-line-active)"/><text x="30" y="32" text-anchor="middle" fill="var(--svg-bg)" font-size="6" font-family="Geist Mono, monospace">R3</text></g><line x1="110" y1="50" x2="170" y2="50" stroke="var(--svg-line-active)" stroke-width="2.5" stroke-linecap="round"/><line x1="230" y1="50" x2="290" y2="50" stroke="var(--svg-line-active)" stroke-width="2.5" stroke-linecap="round"/><line x1="80" y1="70" x2="320" y2="70" stroke="var(--svg-line-down)" stroke-width="1.5" stroke-dasharray="6,4" stroke-linecap="round"/><text x="140" y="45" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="4" font-family="Geist Mono, monospace">10.0.12.0/30</text><text x="260" y="45" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="4" font-family="Geist Mono, monospace">10.0.23.0/30</text><text x="200" y="65" text-anchor="middle" fill="var(--svg-line-down)" font-size="4" font-family="Geist Mono, monospace">10.0.13.0/30 (DOWN)</text><text x="200" y="160" text-anchor="middle" fill="var(--svg-text)" font-size="7" font-family="Geist, sans-serif" font-weight="600">OSPF Troubleshooting Lab</text><text x="200" y="175" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="5" font-family="Geist Mono, monospace">Area 0 | Find the fault</text></svg>',
    '## PNETlab Setup
1. Create a new lab with 3 cRPD nodes: R1, R2, R3
2. Connect: R1-ge0/0/0 to R2-ge0/0/0 (10.0.12.0/30)
3. Connect: R2-ge0/0/1 to R3-ge0/0/0 (10.0.23.0/30)
4. Connect: R1-ge0/0/1 to R3-ge0/0/1 (10.0.13.0/30) - INTENTIONALLY BROKEN
5. Initial configs have a deliberate fault on the R1-R3 link',
    '[
  {"order":1,"title":"Identify OSPF Neighbors","description":"Check OSPF adjacencies on all routers. Determine which adjacency is missing.","verification_commands":["show ospf neighbor"],"expected_output_summary":"R1 should show 2 neighbors (R2 and R3), but R3 adjacency is missing or stuck in Init/ExStart"},
  {"order":2,"title":"Find the Fault","description":"Investigate why R1-R3 OSPF adjacency is not forming. Check interface configs, area assignments, and MTU.","verification_commands":["show configuration interfaces ge-0/0/1","show ospf interface ge-0/0/1.0 detail","show log messages | match ospf"],"expected_output_summary":"ge-0/0/1 on R1 is missing ''family inet'' or has wrong OSPF area assigned"},
  {"order":3,"title":"Fix and Verify","description":"Correct the configuration fault and verify all 3 routers have Full adjacencies and synchronized LSDB.","verification_commands":["show ospf neighbor","show ospf database","show route protocol ospf"],"expected_output_summary":"All neighbors Full, LSDB shows 3 router LSAs, all loopbacks reachable via OSPF"}
]'::jsonb,
    '[
  {"order":1,"title":"OSPF Neighbor States","content":"OSPF neighbor states: Down -> Init -> 2-Way -> ExStart -> Exchange -> Loading -> Full. Stuck in Init usually means unicast not reaching. Stuck in ExStart usually means MTU mismatch."},
  {"order":2,"title":"Interface Requirements","content":"OSPF requires ''family inet'' on the interface. Also check: interface must not be disabled, must have IP, and must be in the correct area."},
  {"order":3,"title":"LSDB Verification","content":"''show ospf database'' should show Router LSAs (Type 1) from all routers in the area. Each router generates one Router LSA."}
]'::jsonb,
    '[
  {"order":1,"task_order":1,"content":"show ospf neighbor (on all 3 routers)"},
  {"order":2,"task_order":2,"content":"show configuration interfaces ge-0/0/1 | display set (on R1) — missing family inet"},
  {"order":3,"task_order":3,"content":"configure | set interfaces ge-0/0/1 unit 0 family inet address 10.0.13.1/30 | set protocols ospf area 0 interface ge-0/0/1.0 | commit and-quit"}
]'::jsonb,
    '[
  {"order":1,"title":"Troubleshooting Methodology","content":"The systematic approach: 1) Verify physical/data-link layer, 2) Check IP connectivity (ping), 3) Verify OSPF interface config, 4) Check neighbor states, 5) Verify LSDB consistency. In this lab, R1 ge-0/0/1 lacked ''family inet'', so OSPF could not form adjacency over that interface."},
  {"order":2,"title":"MTU Mismatch","content":"Another common OSPF adjacency killer is MTU mismatch. JunOS checks MTU during ExStart. If MTUs differ, adjacency stays in ExStart. Fix with ''set protocols ospf interface IFACE mtu-ignore'' or match MTUs."}
]'::jsonb,
    '[
  {"order":1,"task_order":1,"commands":["show ospf neighbor"],"expected_output":"R2: Full, R3: missing or Init"},
  {"order":2,"task_order":2,"commands":["show configuration interfaces ge-0/0/1 | display set"],"expected_output":"missing ''set interfaces ge-0/0/1 unit 0 family inet''"},
  {"order":3,"task_order":3,"commands":["configure","set interfaces ge-0/0/1 unit 0 family inet address 10.0.13.1/30","set protocols ospf area 0 interface ge-0/0/1.0","commit and-quit","show ospf neighbor","show route protocol ospf"],"expected_output":"3 neighbors Full, loopbacks reachable"}
]'::jsonb,
    ARRAY['OSPF Theory', 'JunOS Interface Config', 'Troubleshooting'],
    'a0000000-0000-0000-0000-000000000001'
)
ON CONFLICT (slug) DO NOTHING;

-- Quick Lab 04: BGP Route Reflection (Difficulty 3, JNCIP)
INSERT INTO quick_labs (
    slug, title, description, difficulty, estimated_minutes, level, technology,
    topology_svg, pnetlab_instructions, tasks, hints, answers, explanations, solution_commands,
    prerequisite_topics, track_id
) VALUES (
    'ql-bgp-route-reflection',
    'BGP Route Reflection Cluster',
    'Configure iBGP full-mesh alternative using route reflectors. Set up a 4-router topology with one RR and three clients. Verify route propagation.',
    3, 30, 'JNCIP', 'bgp',
    '<svg viewBox="0 0 400 240" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="400" height="240" fill="var(--svg-bg)" rx="8"/><g transform="translate(170,30)"><rect x="0" y="0" width="60" height="40" rx="4" fill="var(--svg-device-router)" opacity="0.9"/><circle cx="15" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="30" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="45" cy="15" r="3" fill="var(--svg-line-active)"/><text x="30" y="32" text-anchor="middle" fill="var(--svg-bg)" font-size="6" font-family="Geist Mono, monospace">RR</text></g><g transform="translate(50,130)"><rect x="0" y="0" width="60" height="40" rx="4" fill="var(--svg-device-router)" opacity="0.9"/><circle cx="15" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="30" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="45" cy="15" r="3" fill="var(--svg-line-active)"/><text x="30" y="32" text-anchor="middle" fill="var(--svg-bg)" font-size="6" font-family="Geist Mono, monospace">R1</text></g><g transform="translate(170,130)"><rect x="0" y="0" width="60" height="40" rx="4" fill="var(--svg-device-router)" opacity="0.9"/><circle cx="15" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="30" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="45" cy="15" r="3" fill="var(--svg-line-active)"/><text x="30" y="32" text-anchor="middle" fill="var(--svg-bg)" font-size="6" font-family="Geist Mono, monospace">R2</text></g><g transform="translate(290,130)"><rect x="0" y="0" width="60" height="40" rx="4" fill="var(--svg-device-router)" opacity="0.9"/><circle cx="15" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="30" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="45" cy="15" r="3" fill="var(--svg-line-active)"/><text x="30" y="32" text-anchor="middle" fill="var(--svg-bg)" font-size="6" font-family="Geist Mono, monospace">R3</text></g><line x1="200" y1="70" x2="80" y2="130" stroke="var(--svg-line-active)" stroke-width="2.5" stroke-linecap="round"/><line x1="200" y1="70" x2="200" y2="130" stroke="var(--svg-line-active)" stroke-width="2.5" stroke-linecap="round"/><line x1="200" y1="70" x2="320" y2="130" stroke="var(--svg-line-active)" stroke-width="2.5" stroke-linecap="round"/><text x="200" y="200" text-anchor="middle" fill="var(--svg-text)" font-size="7" font-family="Geist, sans-serif" font-weight="600">BGP Route Reflector Cluster</text><text x="200" y="215" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="5" font-family="Geist Mono, monospace">AS65001 | Cluster-ID 1.1.1.1</text></svg>',
    '## PNETlab Setup
1. Create a 4-router topology: RR (Route Reflector), R1, R2, R3
2. Connect RR to all clients (R1, R2, R3) via ge-0/0/0
3. Use AS 65001 for all routers
4. Loopbacks: RR=1.1.1.1, R1=11.11.11.11, R2=22.22.22.22, R3=33.33.33.33
5. Configure OSPF as underlay first',
    '[
  {"order":1,"title":"Configure OSPF Underlay","description":"Set up OSPF Area 0 on all routers so loopbacks are reachable. This provides the BGP next-hop resolution.","verification_commands":["show ospf neighbor","show route 11.11.11.11","show route 22.22.22.22","show route 33.33.33.33"],"expected_output_summary":"All OSPF neighbors Full, all loopbacks reachable via OSPF"},
  {"order":2,"title":"Configure iBGP Peering to RR","description":"On R1, R2, R3: configure iBGP peering with RR loopback as neighbor. Use loopback as local-address.","verification_commands":["show bgp summary"],"expected_output_summary":"All clients show Established with RR (1.1.1.1)"},
  {"order":3,"title":"Configure Route Reflector","description":"On RR: configure iBGP peers for R1, R2, R3 and mark them as cluster clients with ''cluster'' statement.","verification_commands":["show bgp summary","show bgp group internal neighbor"],"expected_output_summary":"RR shows 3 Established peers. Neighbors marked as ''Route-Reflector Client''"},
  {"order":4,"title":"Advertise Routes and Verify Propagation","description":"On each client, configure a static route and advertise it via BGP using a policy. Verify all clients receive routes from other clients via RR.","verification_commands":["show route protocol bgp","show bgp neighbor 1.1.1.1 advertised-routes","show bgp neighbor 1.1.1.1 received-routes"],"expected_output_summary":"Each client sees routes from other 2 clients. RR reflects routes between clients."}
]'::jsonb,
    '[
  {"order":1,"title":"BGP Local-Address","content":"For iBGP over loopbacks, use ''local-address'' under the neighbor group to specify the loopback IP as the source."},
  {"order":2,"title":"Route Reflector Commands","content":"On RR: set protocols bgp group INTERNAL neighbor CLIENT-IP cluster 1.1.1.1. The cluster ID is usually the RR RID."},
  {"order":3,"title":"Next-Hop Self","content":"Routes reflected by RR retain original next-hop. Clients need reachability to that next-hop (via IGP). If not, add ''next-hop self'' on RR or use ''multihop''."}
]'::jsonb,
    '[
  {"order":1,"task_order":1,"content":"On all routers: configure OSPF Area 0 on all interfaces, set loopbacks passive"},
  {"order":2,"task_order":2,"content":"On clients (R1,R2,R3): set protocols bgp group INTERNAL type internal local-address LOOPBACK neighbor 1.1.1.1"},
  {"order":3,"task_order":3,"content":"On RR: set protocols bgp group INTERNAL type internal local-address 1.1.1.1 neighbor R1-IP cluster 1.1.1.1 (same for R2, R3)"},
  {"order":4,"task_order":4,"content":"On each client: create policy to export static/direct, apply to BGP group, add static routes for testing"}
]'::jsonb,
    '[
  {"order":1,"title":"Why Route Reflectors?","content":"iBGP requires full-mesh: n*(n-1)/2 sessions. With 4 routers that is 6 peers. Route Reflector reduces this to n-1 = 3 peers. RR breaks the iBGP split-horizon rule: it reflects routes between clients within the same cluster."},
  {"order":2,"title":"Cluster-ID and ORIGINATOR_ID","content":"The RR adds ORIGINATOR_ID (router that originated the route) to prevent loops. If a router sees its own ORIGINATOR_ID, it discards the route. CLUSTER_LIST tracks which clusters the route passed through."},
  {"order":3,"title":"Redundancy with Multiple RRs","content":"For production, use 2 RRs in different clusters or the same cluster (same cluster-id). Same cluster-id = load balancing. Different cluster-id = redundancy with longer CLUSTER_LIST."}
]'::jsonb,
    '[
  {"order":1,"task_order":1,"commands":["configure","set protocols ospf area 0 interface all","set protocols ospf area 0 interface lo0.0 passive","commit and-quit","show ospf neighbor"],"expected_output":"All neighbors Full"},
  {"order":2,"task_order":2,"commands":["configure","set protocols bgp group INTERNAL type internal","set protocols bgp group INTERNAL local-address 11.11.11.11","set protocols bgp group INTERNAL neighbor 1.1.1.1","commit and-quit","show bgp summary"],"expected_output":"1.1.1.1 Established"},
  {"order":3,"task_order":3,"commands":["configure","set protocols bgp group INTERNAL type internal","set protocols bgp group INTERNAL local-address 1.1.1.1","set protocols bgp group INTERNAL neighbor 11.11.11.11 cluster 1.1.1.1","set protocols bgp group INTERNAL neighbor 22.22.22.22 cluster 1.1.1.1","set protocols bgp group INTERNAL neighbor 33.33.33.33 cluster 1.1.1.1","commit and-quit","show bgp summary"],"expected_output":"3 Established peers"},
  {"order":4,"task_order":4,"commands":["configure","set policy-options policy-statement EXPORT-LOOPBACK term 1 from protocol direct","set policy-options policy-statement EXPORT-LOOPBACK term 1 from route-filter 11.11.11.11/32 exact","set policy-options policy-statement EXPORT-LOOPBACK term 1 then accept","set protocols bgp group INTERNAL export EXPORT-LOOPBACK","commit and-quit","show route protocol bgp"],"expected_output":"Routes from other clients visible"}
]'::jsonb,
    ARRAY['BGP Theory', 'iBGP', 'Route Reflection', 'OSPF Underlay'],
    'a0000000-0000-0000-0000-000000000001'
)
ON CONFLICT (slug) DO NOTHING;

-- Quick Lab 05: MPLS L3VPN (Difficulty 4, JNCIP)
INSERT INTO quick_labs (
    slug, title, description, difficulty, estimated_minutes, level, technology,
    topology_svg, pnetlab_instructions, tasks, hints, answers, explanations, solution_commands,
    prerequisite_topics, track_id
) VALUES (
    'ql-mpls-l3vpn',
    'MPLS L3VPN with VRF',
    'Build a complete MPLS L3VPN service across 4 routers: 2 PEs, 1 P, and 1 CE. Configure VRFs, RT/RD, MP-BGP, and verify VPNv4 route exchange.',
    4, 40, 'JNCIP', 'mpls',
    '<svg viewBox="0 0 500 240" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="500" height="240" fill="var(--svg-bg)" rx="8"/><g transform="translate(40,30)"><rect x="0" y="0" width="60" height="40" rx="4" fill="var(--svg-device-router)" opacity="0.9"/><circle cx="15" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="30" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="45" cy="15" r="3" fill="var(--svg-line-active)"/><text x="30" y="32" text-anchor="middle" fill="var(--svg-bg)" font-size="6" font-family="Geist Mono, monospace">CE1</text></g><g transform="translate(160,30)"><rect x="0" y="0" width="60" height="40" rx="4" fill="var(--svg-device-router)" opacity="0.9"/><circle cx="15" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="30" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="45" cy="15" r="3" fill="var(--svg-line-active)"/><text x="30" y="32" text-anchor="middle" fill="var(--svg-bg)" font-size="6" font-family="Geist Mono, monospace">PE1</text></g><g transform="translate(280,30)"><rect x="0" y="0" width="60" height="40" rx="4" fill="var(--svg-device-router)" opacity="0.9"/><circle cx="15" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="30" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="45" cy="15" r="3" fill="var(--svg-line-active)"/><text x="30" y="32" text-anchor="middle" fill="var(--svg-bg)" font-size="6" font-family="Geist Mono, monospace">P</text></g><g transform="translate(400,30)"><rect x="0" y="0" width="60" height="40" rx="4" fill="var(--svg-device-router)" opacity="0.9"/><circle cx="15" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="30" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="45" cy="15" r="3" fill="var(--svg-line-active)"/><text x="30" y="32" text-anchor="middle" fill="var(--svg-bg)" font-size="6" font-family="Geist Mono, monospace">PE2</text></g><g transform="translate(400,130)"><rect x="0" y="0" width="60" height="40" rx="4" fill="var(--svg-device-router)" opacity="0.9"/><circle cx="15" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="30" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="45" cy="15" r="3" fill="var(--svg-line-active)"/><text x="30" y="32" text-anchor="middle" fill="var(--svg-bg)" font-size="6" font-family="Geist Mono, monospace">CE2</text></g><line x1="100" y1="50" x2="160" y2="50" stroke="var(--svg-line-active)" stroke-width="2.5" stroke-linecap="round"/><line x1="220" y1="50" x2="280" y2="50" stroke="var(--svg-line-active)" stroke-width="2.5" stroke-linecap="round" class="traffic" stroke-dasharray="8,4"/><line x1="340" y1="50" x2="400" y2="50" stroke="var(--svg-line-active)" stroke-width="2.5" stroke-linecap="round" class="traffic" stroke-dasharray="8,4"/><line x1="430" y1="70" x2="430" y2="130" stroke="var(--svg-line-active)" stroke-width="2.5" stroke-linecap="round"/><text x="130" y="45" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="4" font-family="Geist Mono, monospace">ge-0/0/0</text><text x="250" y="45" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="4" font-family="Geist Mono, monospace">IS-IS L2</text><text x="370" y="45" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="4" font-family="Geist Mono, monospace">IS-IS L2</text><text x="440" y="100" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="4" font-family="Geist Mono, monospace">ge-0/0/1</text><rect x="170" y="80" width="40" height="18" rx="3" fill="var(--svg-highlight-bg)"/><text x="190" y="93" text-anchor="middle" fill="var(--svg-highlight)" font-size="5" font-family="Geist Mono, monospace">VRF: BLUE</text><rect x="410" y="80" width="40" height="18" rx="3" fill="var(--svg-highlight-bg)"/><text x="430" y="93" text-anchor="middle" fill="var(--svg-highlight)" font-size="5" font-family="Geist Mono, monospace">VRF: BLUE</text><text x="250" y="200" text-anchor="middle" fill="var(--svg-text)" font-size="7" font-family="Geist, sans-serif" font-weight="600">MPLS L3VPN Lab</text><text x="250" y="215" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="5" font-family="Geist Mono, monospace">VPNv4 | RD 65001:100 | RT 65001:100</text></svg>',
    '## PNETlab Setup
1. Create a 4-router topology: CE1, PE1, P, PE2, CE2
2. Core links: PE1-P (10.0.12.0/30), P-PE2 (10.0.23.0/30)
3. CE links: CE1-PE1 (10.0.1.0/30), CE2-PE2 (10.0.2.0/30)
4. Loopbacks: CE1=1.1.1.1, PE1=2.2.2.2, P=3.3.3.3, PE2=4.4.4.4, CE2=5.5.5.5
5. Use IS-IS as IGP in core. Run LDP on all core interfaces.',
    '[
  {"order":1,"title":"Configure IGP and LDP in Core","description":"Set up IS-IS Level 2 and LDP on PE1, P, and PE2. Ensure all core loopbacks are reachable via IS-IS with MPLS labels.","verification_commands":["show isis adjacency","show ldp session","show mpls lsp","show route 4.4.4.4"],"expected_output_summary":"IS-IS adjacencies Up, LDP sessions Operational, MPLS LSP to all PE loopbacks"},
  {"order":2,"title":"Configure MP-BGP Between PEs","description":"Set up iBGP between PE1 and PE2 using loopbacks. Enable address-family VPNv4 unicast.","verification_commands":["show bgp summary","show bgp group VPNv4"],"expected_output_summary":"PE1-PE2 iBGP Established with VPNv4 capability advertised and received"},
  {"order":3,"title":"Create VRF and CE Peering","description":"On both PEs: create VRF ''BLUE'' with RD 65001:100 and RT 65001:100. Configure eBGP peering with CE routers inside the VRF.","verification_commands":["show route instance BLUE","show bgp summary instance BLUE","show route table BLUE.inet.0"],"expected_output_summary":"VRF BLUE active, eBGP Established with CE, routes in VRF table"},
  {"order":4,"title":"Verify End-to-End VPN Connectivity","description":"Advertise CE1 loopback into BGP. Verify CE2 receives it in its routing table and can ping CE1 loopback via the VPN.","verification_commands":["show route table BLUE.inet.0 1.1.1.1/32","show route advertising-protocol bgp CE2-IP","ping 1.1.1.1 routing-instance BLUE count 5"],"expected_output_summary":"CE1 loopback reachable from CE2 via VPN. Ping succeeds from PE2 VRF context."}
]'::jsonb,
    '[
  {"order":1,"title":"LDP vs RSVP","content":"LDP is simpler (automatic label distribution based on IGP). RSVP-TE provides traffic engineering but requires more config. For basic L3VPN, LDP is sufficient."},
  {"order":2,"title":"MP-BGP Address Families","content":"VPNv4 routes are NLRI with RD prepended (e.g., 65001:100:10.0.1.0/30). Use ''family inet-vpn unicast'' in BGP group config."},
  {"order":3,"title":"VRF Route Targets","content":"RT determines VPN membership. Export RT = routes advertised from VRF. Import RT = routes accepted into VRF. Both PEs must use matching RT values."},
      {"order":4,"title":"CE-PE Routing","content":"eBGP is common for CE-PE. The CE does not know about MPLS or VPNs. It simply exchanges IPv4 routes with the PE."}
]'::jsonb,
    '[
  {"order":1,"task_order":1,"content":"On PE1, P, PE2: set protocols isis level 2, set protocols ldp interface all, set protocols mpls interface all"},
  {"order":2,"task_order":2,"content":"On PE1 and PE2: set protocols bgp group VPNv4 type internal local-address LOOPBACK neighbor OTHER-PE family inet-vpn unicast"},
  {"order":3,"task_order":3,"content":"On PE1: set routing-instances BLUE instance-type vrf, set routing-instances BLUE route-distinguisher 65001:100, set routing-instances BLUE vrf-target target:65001:100, set routing-instances BLUE interface ge-0/0/0.0, set routing-instances BLUE protocols bgp group CE type external peer-as 65002 neighbor CE1-IP"},
  {"order":4,"task_order":4,"content":"On CE1: advertise loopback via BGP. On PE2: verify route in BLUE.inet.0 and reachable from CE2"}
]'::jsonb,
    '[
  {"order":1,"title":"MPLS L3VPN Architecture","content":"L3VPN (RFC 2547bis) allows service providers to create isolated Layer 3 VPNs for customers. Key components: 1) VRF on PEs for customer isolation, 2) MP-BGP for VPNv4 route exchange, 3) MPLS for label switching in core, 4) IGP for core reachability."},
  {"order":2,"title":"Route Distinguisher vs Route Target","content":"RD makes routes unique across VPNs (prevents overlap). RT controls VPN membership (who gets which routes). One VRF can import multiple RTs for extranet/hub-spoke designs."},
  {"order":3,"title":"Label Stack","content":"In MPLS L3VPN, packets carry 2 labels: 1) Transport label (IGP/LDP) to reach egress PE, 2) VPN label (advertised via MP-BGP) to identify the VRF. PHP removes transport label; VPN label is used by egress PE to forward to CE."}
]'::jsonb,
    '[
  {"order":1,"task_order":1,"commands":["configure","set protocols isis interface all","set protocols isis interface lo0.0 passive","set protocols ldp interface all","set protocols mpls interface all","commit and-quit","show ldp session"],"expected_output":"LDP sessions: Operational"},
  {"order":2,"task_order":2,"commands":["configure","set protocols bgp group VPNv4 type internal","set protocols bgp group VPNv4 local-address 2.2.2.2","set protocols bgp group VPNv4 neighbor 4.4.4.4 family inet-vpn unicast","commit and-quit","show bgp summary"],"expected_output":"4.4.4.4 Established"},
  {"order":3,"task_order":3,"commands":["configure","set routing-instances BLUE instance-type vrf","set routing-instances BLUE route-distinguisher 65001:100","set routing-instances BLUE vrf-target target:65001:100","set routing-instances BLUE interface ge-0/0/0.0","set routing-instances BLUE protocols bgp group CE type external peer-as 65002 neighbor 10.0.1.1","commit and-quit","show route instance BLUE"],"expected_output":"BLUE active"},
  {"order":4,"task_order":4,"commands":["show route table BLUE.inet.0 1.1.1.1/32","ping 1.1.1.1 routing-instance BLUE count 5"],"expected_output":"1.1.1.1/32 reachable, ping 0% loss"}
]'::jsonb,
    ARRAY['MPLS', 'LDP', 'MP-BGP', 'VRF', 'IS-IS'],
    'a0000000-0000-0000-0000-000000000001'
)
ON CONFLICT (slug) DO NOTHING;

-- Quick Lab 06: EVPN-VXLAN Data Center (Difficulty 5, JNCIE)
INSERT INTO quick_labs (
    slug, title, description, difficulty, estimated_minutes, level, technology,
    topology_svg, pnetlab_instructions, tasks, hints, answers, explanations, solution_commands,
    prerequisite_topics, track_id
) VALUES (
    'ql-evpn-vxlan-dc',
    'EVPN-VXLAN Data Center Fabric',
    'Design and troubleshoot a modern EVPN-VXLAN data center fabric with spine-leaf topology, asymmetric IRB, and multi-homing.',
    5, 50, 'JNCIE', 'evpn',
    '<svg viewBox="0 0 600 280" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="600" height="280" fill="var(--svg-bg)" rx="8"/><g transform="translate(180,20)"><rect x="0" y="0" width="80" height="40" rx="4" fill="var(--svg-device-router)" opacity="0.9"/><circle cx="15" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="30" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="45" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="60" cy="15" r="3" fill="var(--svg-line-active)"/><text x="40" y="32" text-anchor="middle" fill="var(--svg-bg)" font-size="6" font-family="Geist Mono, monospace">SPINE1</text></g><g transform="translate(340,20)"><rect x="0" y="0" width="80" height="40" rx="4" fill="var(--svg-device-router)" opacity="0.9"/><circle cx="15" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="30" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="45" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="60" cy="15" r="3" fill="var(--svg-line-active)"/><text x="40" y="32" text-anchor="middle" fill="var(--svg-bg)" font-size="6" font-family="Geist Mono, monospace">SPINE2</text></g><g transform="translate(80,120)"><rect x="0" y="0" width="80" height="40" rx="4" fill="var(--svg-device-switch)" opacity="0.9"/><circle cx="15" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="30" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="45" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="60" cy="15" r="3" fill="var(--svg-line-active)"/><text x="40" y="32" text-anchor="middle" fill="var(--svg-bg)" font-size="6" font-family="Geist Mono, monospace">LEAF1</text></g><g transform="translate(260,120)"><rect x="0" y="0" width="80" height="40" rx="4" fill="var(--svg-device-switch)" opacity="0.9"/><circle cx="15" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="30" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="45" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="60" cy="15" r="3" fill="var(--svg-line-active)"/><text x="40" y="32" text-anchor="middle" fill="var(--svg-bg)" font-size="6" font-family="Geist Mono, monospace">LEAF2</text></g><g transform="translate(440,120)"><rect x="0" y="0" width="80" height="40" rx="4" fill="var(--svg-device-switch)" opacity="0.9"/><circle cx="15" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="30" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="45" cy="15" r="3" fill="var(--svg-line-active)"/><circle cx="60" cy="15" r="3" fill="var(--svg-line-active)"/><text x="40" y="32" text-anchor="middle" fill="var(--svg-bg)" font-size="6" font-family="Geist Mono, monospace">LEAF3</text></g><g transform="translate(100,220)"><rect x="0" y="0" width="40" height="28" rx="3" fill="var(--svg-device-host)" opacity="0.8"/><text x="20" y="20" text-anchor="middle" fill="var(--svg-bg)" font-size="5" font-family="Geist Mono, monospace">H1</text></g><g transform="translate(280,220)"><rect x="0" y="0" width="40" height="28" rx="3" fill="var(--svg-device-host)" opacity="0.8"/><text x="20" y="20" text-anchor="middle" fill="var(--svg-bg)" font-size="5" font-family="Geist Mono, monospace">H2</text></g><g transform="translate(460,220)"><rect x="0" y="0" width="40" height="28" rx="3" fill="var(--svg-device-host)" opacity="0.8"/><text x="20" y="20" text-anchor="middle" fill="var(--svg-bg)" font-size="5" font-family="Geist Mono, monospace">H3</text></g><line x1="220" y1="40" x2="120" y2="120" stroke="var(--svg-line-active)" stroke-width="2.5" stroke-linecap="round"/><line x1="220" y1="40" x2="300" y2="120" stroke="var(--svg-line-active)" stroke-width="2.5" stroke-linecap="round"/><line x1="380" y1="40" x2="300" y2="120" stroke="var(--svg-line-active)" stroke-width="2.5" stroke-linecap="round"/><line x1="380" y1="40" x2="480" y2="120" stroke="var(--svg-line-active)" stroke-width="2.5" stroke-linecap="round"/><line x1="120" y1="160" x2="120" y2="220" stroke="var(--svg-line-active)" stroke-width="2" stroke-linecap="round"/><line x1="300" y1="160" x2="300" y2="220" stroke="var(--svg-line-active)" stroke-width="2" stroke-linecap="round"/><line x1="480" y1="160" x2="480" y2="220" stroke="var(--svg-line-active)" stroke-width="2" stroke-linecap="round"/><rect x="85" y="170" width="70" height="16" rx="3" fill="var(--svg-highlight-bg)"/><text x="120" y="181" text-anchor="middle" fill="var(--svg-highlight)" font-size="4" font-family="Geist Mono, monospace">VLAN 100 | VNI 10100</text><rect x="265" y="170" width="70" height="16" rx="3" fill="var(--svg-highlight-bg)"/><text x="300" y="181" text-anchor="middle" fill="var(--svg-highlight)" font-size="4" font-family="Geist Mono, monospace">VLAN 200 | VNI 10200</text><rect x="445" y="170" width="70" height="16" rx="3" fill="var(--svg-highlight-bg)"/><text x="480" y="181" text-anchor="middle" fill="var(--svg-highlight)" font-size="4" font-family="Geist Mono, monospace">VLAN 100 | VNI 10100</text><text x="300" y="260" text-anchor="middle" fill="var(--svg-text)" font-size="7" font-family="Geist, sans-serif" font-weight="600">EVPN-VXLAN Spine-Leaf Fabric</text><text x="300" y="272" text-anchor="middle" fill="var(--svg-text-secondary)" font-size="5" font-family="Geist Mono, monospace">Asymmetric IRB | ESI LAG | Type-2/5 Routes</text></svg>',
    '## PNETlab Setup
1. Create spine-leaf topology: 2 Spines (vQFX), 3 Leafs (vQFX)
2. Connect each Leaf to both Spines (eBGP underlay)
3. Connect hosts: H1 to LEAF1, H2 to LEAF2, H3 to LEAF3
4. Use eBGP for underlay (AS 65000 for spines, AS 65001-65003 for leafs)
5. Use EVPN as overlay with iBGP route-reflection on spines',
    '[
  {"order":1,"title":"Configure eBGP Underlay","description":"Set up eBGP sessions between each Leaf and both Spines using loopbacks. Advertise loopbacks into BGP.","verification_commands":["show bgp summary","show route 1.1.1.1/32"],"expected_output_summary":"Each Leaf has 2 Established eBGP peers (both Spines). All loopbacks reachable."},
  {"order":2,"title":"Configure EVPN BGP Sessions","description":"Enable EVPN address-family between Leafs and Spines. Spines act as route reflectors for EVPN.","verification_commands":["show bgp group EVPN summary","show evpn overview"],"expected_output_summary":"EVPN sessions Established. EVPN instance shows NLRI type evpn."},
  {"order":3,"title":"Configure VXLAN Tunnels and VLANs","description":"On each Leaf: map VLANs to VNIs, configure VTEP source interface (lo0), set up IRB interfaces for L3 gateway.","verification_commands":["show vxlan vtep","show bridge domain","show evpn instance BLUE"],"expected_output_summary":"VTEPs listed, bridge domains active, EVPN instance shows VNI mappings"},
  {"order":4,"title":"Verify End-to-End Connectivity","description":"Verify H1 can ping H3 (same VLAN 100, different leafs) via VXLAN tunnel. Verify H2 (VLAN 200) can reach gateway.","verification_commands":["show evpn database","show bridge mac-table","ping 10.100.1.3"],"expected_output_summary":"MAC addresses learned via EVPN Type-2 routes. Inter-leaf same-VLAN traffic works."}
]'::jsonb,
    '[
      {"order":1,"title":"eBGP Underlay vs iBGP Overlay","content":"eBGP underlay is simple (different AS per device). iBGP overlay runs over the underlay loopbacks. Use ''multihop'' and ''local-address'' for iBGP."},
      {"order":2,"title":"EVPN Route Types","content":"Type 1: Ethernet Auto-Discovery (A-D) for multi-homing. Type 2: MAC/IP Advertisement. Type 3: Inclusive Multicast for BUM traffic. Type 4: Ethernet Segment for DF election. Type 5: IP Prefix for inter-subnet routing."},
      {"order":3,"title":"VXLAN Encapsulation","content":"VXLAN uses UDP 4789. The VTEP IP is typically the loopback. JunOS: set protocols evpn vni-options VNI vrf-target TARGET. Map VLAN to VNI with ''vlan-mapping'' or ''vlans VLAN vxlan vni''."}
]'::jsonb,
    '[
      {"order":1,"task_order":1,"content":"On all devices: configure eBGP underlay with loopback peering, advertise direct/loopback routes"},
      {"order":2,"task_order":2,"content":"On Spines: configure EVPN route-reflector cluster. On Leafs: configure EVPN iBGP peers to both spines with ''family evpn signaling''"},
      {"order":3,"task_order":3,"content":"On Leafs: set vlans VLAN-100 vxlan vni 10100, set protocols evpn vni-options vni 10100 vrf-target target:1:100, configure IRB.100 as L3 gateway"},
      {"order":4,"task_order":4,"content":"Verify: show evpn database should show Type-2 routes for H1 and H3 MACs. Ping between hosts should succeed."}
]'::jsonb,
    '[
      {"order":1,"title":"Spine-Leaf Architecture","content":"Spine-leaf is the modern DC standard. Every Leaf connects to every Spine (full mesh at spine layer). East-west traffic (server-to-server) is optimized. Scale is linear: add more spines for bandwidth, more leafs for endpoints."},
      {"order":2,"title":"Asymmetric IRB","content":"In asymmetric IRB, the ingress Leaf performs both L2 bridging and L3 routing. The egress Leaf only does L2 bridging. This requires all Leafs to have identical IRB configs (same VLANs, same VNIs, same IRB IPs). Simpler than symmetric IRB but consumes more resources."},
      {"order":3,"title":"EVPN Multi-Homing (ESI)","content":"ESI (Ethernet Segment Identifier) allows a CE to dual-home to two Leafs. LAG on CE, ESI-LAG on Leafs. DF (Designated Forwarder) election prevents duplicate BUM traffic. Type-1 A-D per ES routes signal multi-homing capability."}
]'::jsonb,
    '[
      {"order":1,"task_order":1,"commands":["configure","set protocols bgp group UNDERLAY type external","set protocols bgp group UNDERLAY neighbor SPINE1-IP peer-as 65000","set protocols bgp group UNDERLAY neighbor SPINE2-IP peer-as 65000","set protocols bgp group UNDERLAY export EXPORT-LOOPBACK","commit and-quit","show bgp summary"],"expected_output":"2 Established peers"},
      {"order":2,"task_order":2,"commands":["configure","set protocols bgp group EVPN type internal local-address LOOPBACK","set protocols bgp group EVPN family evpn signaling","set protocols bgp group EVPN neighbor SPINE1-LO","set protocols bgp group EVPN neighbor SPINE2-LO","commit and-quit","show bgp group EVPN summary"],"expected_output":"EVPN Established"},
      {"order":3,"task_order":3,"commands":["configure","set vlans VLAN-100 vxlan vni 10100","set protocols evpn vni-options vni 10100 vrf-target target:1:100","set interfaces irb unit 100 family inet address 10.100.1.1/24","commit and-quit","show vxlan vtep"],"expected_output":"VTEP list populated"},
      {"order":4,"task_order":4,"commands":["show evpn database","show bridge mac-table","ping 10.100.1.3 routing-instance BLUE"],"expected_output":"MACs learned, ping succeeds"}
]'::jsonb,
    ARRAY['EVPN', 'VXLAN', 'Data Center', 'Spine-Leaf', 'eBGP Underlay'],
    'a0000000-0000-0000-0000-000000000001'
)
ON CONFLICT (slug) DO NOTHING;

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TABLE IF EXISTS quick_labs CASCADE;
-- +goose StatementEnd