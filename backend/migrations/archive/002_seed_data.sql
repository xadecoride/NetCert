-- +goose Up
-- +goose StatementBegin

-- Seed tracks
INSERT INTO tracks (id, slug, vendor, name, description, sort_order) VALUES
    ('a0000000-0000-0000-0000-000000000001', 'junos-ent', 'juniper', 'JNCIA-Junos (ENT)', 'Enterprise Routing & Switching — базовый трек Juniper для корпоративных сетей', 1),
    ('a0000000-0000-0000-0000-000000000002', 'junos-sp', 'juniper', 'JNCIA-SP (SP)', 'Service Provider — провайдерские сети и MPLS', 2),
    ('a0000000-0000-0000-0000-000000000003', 'junos-sec', 'juniper', 'JNCIA-SEC (SEC)', 'Security — межсетевые экраны Juniper SRX и IPsec VPN', 3),
    ('a0000000-0000-0000-0000-000000000004', 'junos-dc', 'juniper', 'JNCIA-DC (DC)', 'Data Center — EVPN-VXLAN, QFX, коммутация ЦОД', 4),
    ('a0000000-0000-0000-0000-000000000005', 'junos-aut', 'juniper', 'JNCIA-DevOps (AUT)', 'Automation & DevOps — PyEZ, Ansible, NETCONF, Junos OS Automation', 5),
    ('a0000000-0000-0000-0000-000000000006', 'cisco-ccna', 'cisco', 'CCNA', 'Cisco Certified Network Associate — базовый трек Cisco', 6);

-- Seed exams
INSERT INTO exams (id, track_id, code, name, level, duration_minutes, total_questions, passing_score) VALUES
    ('b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'JN0-101', 'JNCIA-Junos', 'JNCIA', 90, 60, 65.00),
    ('b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'JN0-201', 'JNCIA-SP', 'JNCIA', 90, 60, 65.00),
    ('b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', '200-301', 'CCNA', 'CCNA', 120, 102, 70.00);

-- Seed questions for JNCIA-Junos (JN0-101)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active) VALUES
-- Question 1
('c0000000-0000-0000-0000-000000000001', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 1, 'remember',
'Which statement correctly describes the Junos OS architecture?',
'[
  {"id":"a","text":"Junos OS uses a monolithic kernel with all processes running in kernel space","is_correct":false},
  {"id":"b","text":"Junos OS has a modular architecture with separate user-space processes for each protocol","is_correct":true},
  {"id":"c","text":"Junos OS is based on the Linux kernel and runs all routing protocols as kernel modules","is_correct":false},
  {"id":"d","text":"Junos OS uses a real-time operating system with no user-space processes","is_correct":false}
]'::jsonb,
'Junos OS is built on the FreeBSD kernel and uses a modular architecture. Each routing protocol (OSPF, BGP, IS-IS, etc.) runs as a separate user-space daemon. This provides process isolation: if one protocol daemon crashes, it does not affect other processes.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/junos-overview/'],
'Junos OS Fundamentals', 15.0, TRUE),

-- Question 2
('c0000000-0000-0000-0000-000000000002', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 1, 'remember',
'In Junos OS, which CLI mode allows you to view the current configuration?',
'[
  {"id":"a","text":"Configuration mode (configure exclusive)","is_correct":false},
  {"id":"b","text":"Operational mode","is_correct":true},
  {"id":"c","text":"Monitor mode","is_correct":false},
  {"id":"d","text":"Enable mode","is_correct":false}
]'::jsonb,
'Junos CLI has two main modes: operational mode (>) for monitoring and troubleshooting, and configuration mode (#) for making changes. In operational mode you can use "show configuration" to view the active config, or "show | display set" for set-based output.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli/'],
'Junos CLI Fundamentals', 10.0, TRUE),

-- Question 3
('c0000000-0000-0000-0000-000000000003', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand',
'Which command displays the OSPF neighbors on a Junos device?',
'[
  {"id":"a","text":"show ospf neighbor","is_correct":true},
  {"id":"b","text":"show ospf database","is_correct":false},
  {"id":"c","text":"show ospf interface","is_correct":false},
  {"id":"d","text":"show ospf adjacency","is_correct":false}
]'::jsonb,
'The correct command is "show ospf neighbor". It displays all OSPF neighbors, their state (Full, 2-Way, etc.), interface, and neighbor ID. Other useful OSPF commands include "show ospf interface" and "show ospf database".',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/ospf/'],
'OSPF', 12.0, TRUE),

-- Question 4
('c0000000-0000-0000-0000-000000000004', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand',
'Which BGP attribute is used for loop prevention in BGP?',
'[
  {"id":"a","text":"MED (Multi-Exit Discriminator)","is_correct":false},
  {"id":"b","text":"Local Preference","is_correct":false},
  {"id":"c","text":"AS_PATH","is_correct":true},
  {"id":"d","text":"Community","is_correct":false}
]'::jsonb,
'AS_PATH is used for loop prevention in BGP. When a BGP router receives an update, it checks if its own AS number is in the AS_PATH attribute. If so, it discards the update to prevent routing loops.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/bgp/'],
'BGP', 15.0, TRUE),

-- Question 5
('c0000000-0000-0000-0000-000000000005', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'apply',
'In Junos, what is the default import policy for EBGP sessions?',
'[
  {"id":"a","text":"Accept all BGP routes","is_correct":false},
  {"id":"b","text":"Reject all BGP routes","is_correct":false},
  {"id":"c","text":"Accept all active BGP routes","is_correct":true},
  {"id":"d","text":"Only accept default routes","is_correct":false}
]'::jsonb,
'By default, Junos accepts all BGP routes from EBGP peers. However, best practice is to apply import and export policies to control which routes are accepted and advertised. Without policies, all routes in the routing table are considered for advertisement to EBGP peers.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/bgp/topics/topic-map/bgp-configuration.html'],
'BGP Policy', 12.0, TRUE),

-- Question 6 (Multiple Choice)
('c0000000-0000-0000-0000-000000000006', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'multiple-choice', 3, 'understand',
'Which of the following are valid Junos firewall filter actions? (Select TWO)',
'[
  {"id":"a","text":"accept","is_correct":true},
  {"id":"b","text":"discard","is_correct":true},
  {"id":"c","text":"permit","is_correct":false},
  {"id":"d","text":"forward","is_correct":false}
]'::jsonb,
'Junos firewall filter actions include: accept (allow the packet), discard (silently drop), reject (drop with ICMP unreachable), and count (count packets without dropping). "permit" and "forward" are not valid Junos filter actions.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/security-policies/'],
'Firewall Filters', 10.0, TRUE),

-- Question 7
('c0000000-0000-0000-0000-000000000007', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 1, 'remember',
'Which statement about the Junos commit model is correct?',
'[
  {"id":"a","text":"Changes take effect immediately as you type them","is_correct":false},
  {"id":"b","text":"Changes are staged and applied atomically with the commit command","is_correct":true},
  {"id":"c","text":"Changes are automatically saved every 5 minutes","is_correct":false},
  {"id":"d","text":"Changes require a system reboot to take effect","is_correct":false}
]'::jsonb,
'Junos uses a two-phase configuration model: first you stage changes in candidate configuration, then you apply them atomically with the "commit" command. This ensures configuration consistency and allows validation before activation.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli/'],
'Junos Configuration Management', 10.0, TRUE),

-- Question 8 (Fill-blank)
('c0000000-0000-0000-0000-000000000008', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'fill-blank', 4, 'analyze',
'A Junos device has the following static route configured:
"set routing-options static route 192.168.100.0/24 next-hop 10.0.0.1"
What command would you use to verify this route is in the routing table? (Type the full command)',
'[
  {"id":"a","text":"show route 192.168.100.0/24","is_correct":true}
]'::jsonb,
'The command "show route 192.168.100.0/24" displays all routes matching the prefix. You can also use "show route protocol static" to see all static routes, or "show route table inet.0" for the full IPv4 routing table.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/routing-policy/'],
'Routing Fundamentals', 8.0, TRUE),

-- Question 9 (Multiple Choice)
('c0000000-0000-0000-0000-000000000009', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'multiple-choice', 2, 'understand',
'Which of these are valid Junos interface types? (Select TWO)',
'[
  {"id":"a","text":"ge (Gigabit Ethernet)","is_correct":true},
  {"id":"b","text":"xe (10 Gigabit Ethernet)","is_correct":true},
  {"id":"c","text":"gi (GigabitEthernet Cisco-style)","is_correct":false},
  {"id":"d","text":"fa (FastEthernet Cisco-style)","is_correct":false}
]'::jsonb,
'Junos uses its own interface naming convention: ge- (Gigabit Ethernet), xe- (10 Gigabit Ethernet), et- (40/100 Gigabit Ethernet), lo (loopback), fxp (management). Cisco-style names like gi and fa are not used in Junos.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/interfaces/'],
'Junos Interface Types', 8.0, TRUE),

-- Question 10
('c0000000-0000-0000-0000-000000000010', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 4, 'analyze',
'You need to apply a firewall filter that counts packets on interface ge-0/0/1 without dropping any traffic. Which action should you use?',
'[
  {"id":"a","text":"then accept;","is_correct":false},
  {"id":"b","text":"then count;","is_correct":false},
  {"id":"c","text":"then count accept;","is_correct":true},
  {"id":"d","text":"then log;","is_correct":false}
]'::jsonb,
'To count packets without dropping, you need both count AND accept actions: "then count accept;". Using just "count" would count the packet but then continue to the next term (and if no term matches, it would be discarded by the implicit deny).',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/security-policies/firewall-filter.html'],
'Firewall Filters', 8.0, TRUE);

-- Seed tags for questions
INSERT INTO question_tags (question_id, technology, protocol) VALUES
    ('c0000000-0000-0000-0000-000000000001', 'Junos OS Architecture', 'General'),
    ('c0000000-0000-0000-0000-000000000002', 'Junos CLI', 'General'),
    ('c0000000-0000-0000-0000-000000000003', 'OSPF', 'OSPF'),
    ('c0000000-0000-0000-0000-000000000004', 'BGP', 'BGP'),
    ('c0000000-0000-0000-0000-000000000005', 'BGP', 'BGP'),
    ('c0000000-0000-0000-0000-000000000006', 'Firewall Filters', 'General'),
    ('c0000000-0000-0000-0000-000000000007', 'Junos Configuration', 'General'),
    ('c0000000-0000-0000-0000-000000000008', 'Static Routing', 'IPv4'),
    ('c0000000-0000-0000-0000-000000000009', 'Junos Interfaces', 'Ethernet'),
    ('c0000000-0000-0000-0000-000000000010', 'Firewall Filters', 'General');

-- Seed JNCIA-SP questions
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active) VALUES
('c0000000-0000-0000-0000-000000000011', 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'single-choice', 1, 'remember',
'What is the primary function of MPLS?',
'[
  {"id":"a","text":"To replace IP routing with label switching for faster forwarding","is_correct":true},
  {"id":"b","text":"To provide encryption for VPN traffic","is_correct":false},
  {"id":"c","text":"To replace BGP as the internet routing protocol","is_correct":false},
  {"id":"d","text":"To provide network address translation","is_correct":false}
]'::jsonb,
'MPLS (Multiprotocol Label Switching) inserts a label between Layer 2 and Layer 3 headers. Routers forward packets based on labels rather than IP addresses, enabling faster lookups, traffic engineering, and Layer 3 VPN services.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/mpls/'],
'MPLS Fundamentals', 20.0, TRUE),

('c0000000-0000-0000-0000-000000000012', 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'single-choice', 2, 'understand',
'In MPLS, what device adds a label to a packet at the edge of the MPLS domain?',
'[
  {"id":"a","text":"P router (Provider router)","is_correct":false},
  {"id":"b","text":"PE router (Provider Edge router)","is_correct":true},
  {"id":"c","text":"CE router (Customer Edge router)","is_correct":false},
  {"id":"d","text":"RR (Route Reflector)","is_correct":false}
]'::jsonb,
'The PE (Provider Edge) router sits at the edge of the service provider network. It performs label imposition (push) on incoming packets and label disposition (pop) on outgoing packets. P routers perform label switching based on the top label.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/mpls/'],
'MPLS Architecture', 20.0, TRUE),

('c0000000-0000-0000-0000-000000000013', 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'single-choice', 2, 'understand',
'Which protocol is used for label distribution in MPLS?',
'[
  {"id":"a","text":"OSPF","is_correct":false},
  {"id":"b","text":"LDP (Label Distribution Protocol)","is_correct":true},
  {"id":"c","text":"RIP","is_correct":false},
  {"id":"d","text":"SNMP","is_correct":false}
]'::jsonb,
'LDP (Label Distribution Protocol) is used to distribute MPLS label bindings between routers. RSVP-TE can also distribute labels while providing traffic engineering capabilities. BGP can carry MPLS labels for VPN services.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/mpls/'],
'MPLS Label Distribution', 15.0, TRUE);

-- Seed CCNA questions
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active) VALUES
('c0000000-0000-0000-0000-000000000014', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 1, 'remember',
'What is the default administrative distance of OSPF in Cisco IOS?',
'[
  {"id":"a","text":"90","is_correct":false},
  {"id":"b","text":"100","is_correct":false},
  {"id":"c","text":"110","is_correct":true},
  {"id":"d","text":"120","is_correct":false}
]'::jsonb,
'OSPF has a default administrative distance of 110 in Cisco IOS. Administrative distance is used to select the best route when multiple routing protocols provide routes to the same destination. Lower AD is preferred.',
ARRAY['https://www.cisco.com/c/en/us/support/docs/ip/open-shortest-path-first-ospf/7039-1.html'],
'IP Connectivity - OSPF', 12.0, TRUE),

('c0000000-0000-0000-0000-000000000015', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 1, 'remember',
'Which VLAN range is reserved for normal-range VLANs on a Cisco switch?',
'[
  {"id":"a","text":"1-1001","is_correct":true},
  {"id":"b","text":"1-4094","is_correct":false},
  {"id":"c","text":"1002-4096","is_correct":false},
  {"id":"d","text":"1-1005","is_correct":false}
]'::jsonb,
'Normal-range VLANs on Cisco switches are VLAN 1-1001. VLANs 1002-1005 are reserved for legacy Token Ring and FDDI. Extended-range VLANs (1006-4094) are supported on some platforms but require VTP transparent mode.',
ARRAY['https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst2960/software/12-2/55-se/configuration/guide/scg/swvlan.html'],
'Network Access - VLANs', 10.0, TRUE),

('c0000000-0000-0000-0000-000000000016', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'understand',
'Which command is used to enable RIP routing on a Cisco router?',
'[
  {"id":"a","text":"router rip","is_correct":true},
  {"id":"b","text":"enable rip","is_correct":false},
  {"id":"c","text":"rip enable","is_correct":false},
  {"id":"d","text":"ip routing rip","is_correct":false}
]'::jsonb,
'The "router rip" command enters RIP configuration mode. From there, you use "network" statements to advertise interfaces and "version 2" to enable RIPv2. RIP is a distance-vector protocol that uses hop count as its metric (max 15 hops).',
ARRAY['https://www.cisco.com/c/en/us/support/docs/ip/routing-information-protocol-rip/13708-routing.html'],
'IP Connectivity - RIP', 8.0, TRUE);

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
TRUNCATE question_tags CASCADE;
TRUNCATE questions CASCADE;
TRUNCATE exams CASCADE;
TRUNCATE tracks CASCADE;
-- +goose StatementEnd
