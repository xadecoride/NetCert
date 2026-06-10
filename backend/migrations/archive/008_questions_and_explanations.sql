-- Migration 008: Additional Questions + Explanation Seed Data
-- Adds ~200 questions across all exams + seed explanations for existing questions

-- ============================================================
-- Part 1: Seed Explanations for existing questions
-- ============================================================

-- Explanation for JNCIA question 1: "show configuration"
INSERT INTO explanations (question_id, version, sections, summary, is_active)
SELECT q.id, 1,
  jsonb_build_array(
    jsonb_build_object('section_type', 'tl_dr', 'title', 'TL;DR', 'content', 'The "show configuration" command displays the active router configuration in Junos OS. It shows the complete configuration hierarchy, or you can display specific sections using the pipe modifier.', 'is_collapsible', false, 'sort_order', 1),
    jsonb_build_object('section_type', 'scenario', 'title', 'Scenario Breakdown', 'content', 'When troubleshooting a Juniper device, you need to view the active configuration. The "show configuration" operational mode command displays the entire active configuration in the CLI.\n\n`show configuration | display set` shows configuration in set format (one command per line).\n`show configuration | display xml` shows configuration in XML format.', 'is_collapsible', true, 'sort_order', 2),
    jsonb_build_object('section_type', 'why_correct', 'title', 'Why this is correct', 'content', 'Option A is correct because "show configuration" is the standard Junos operational mode command for displaying the active configuration. Configuration mode uses "show" within "edit configuration" context, and operational mode uses "show configuration" at the `>` prompt.', 'is_collapsible', true, 'sort_order', 3),
    jsonb_build_object('section_type', 'distractor_analysis', 'title', 'Trap Analysis', 'content', jsonb_build_array(
      jsonb_build_object('option_id', 'A', 'why_wrong', 'Correct answer.', 'common_mistake', false),
      jsonb_build_object('option_id', 'B', 'why_wrong', '"display configuration" is not a valid Junos CLI command. The correct command is "show configuration". This distractor tests whether you know the correct verb (show vs display).', 'common_mistake', true),
      jsonb_build_object('option_id', 'C', 'why_wrong', '"show active-config" is not a valid Junos command. Some other networking platforms (e.g., some Cisco devices) use "show running-config", but Junos uses "show configuration".', 'common_mistake', false),
      jsonb_build_object('option_id', 'D', 'why_wrong', '"get configuration" is not a valid Junos CLI command. This distractor tests familiarity with the Junos operational mode command syntax.', 'common_mistake', false)
    )::text, 'is_collapsible', true, 'sort_order', 4),
    jsonb_build_object('section_type', 'cli_examples', 'title', 'CLI Examples', 'content', '```junos\nuser@router> show configuration | display set\nset version 22.4R3\nset system host-name router\nset interfaces ge-0/0/0 unit 0 family inet address 10.0.0.1/24\n```\n\n```junos\nuser@router> show configuration interfaces\nge-0/0/0 {\n    unit 0 {\n        family inet {\n            address 10.0.0.1/24;\n        }\n    }\n}\n```', 'is_collapsible', true, 'sort_order', 5),
    jsonb_build_object('section_type', 'vendor_nuances', 'title', 'Vendor-Specific Nuances', 'content', 'In Junos, the configuration is always stored as a hierarchical text file. Unlike Cisco IOS where "show running-config" shows the active configuration, Junos uses "show configuration". Additionally, Junos supports powerful pipe modifiers: `| display set`, `| display xml`, `| match`, `| except`, and more.', 'is_collapsible', true, 'sort_order', 6)
  ),
  'The "show configuration" command displays the active Junos router configuration in operational mode.',
  true
FROM questions q
WHERE q.body LIKE '%Which command displays the active configuration%'
LIMIT 1;

-- Explanation for OSPF AD question
INSERT INTO explanations (question_id, version, sections, summary, is_active)
SELECT q.id, 1,
  jsonb_build_array(
    jsonb_build_object('section_type', 'tl_dr', 'title', 'TL;DR', 'content', 'OSPF routes have an administrative distance (AD) of 10 in Junos. This is lower than the Junos default for static routes (18) and BGP (170), meaning OSPF routes are preferred when multiple routing protocols advertise the same prefix.', 'is_collapsible', false, 'sort_order', 1),
    jsonb_build_object('section_type', 'why_correct', 'title', 'Why this is correct', 'content', 'Junos uses a preference (AD) value of 10 for OSPF internal routes. This differs from Cisco where OSPF AD is 110. Understanding Junos preference values is critical for route selection troubleshooting.\n\nKey Junos preference values:\n- Direct: 0\n- Static: 18\n- OSPF: 10\n- IS-IS: 18\n- BGP: 170', 'is_collapsible', true, 'sort_order', 2),
    jsonb_build_object('section_type', 'distractor_analysis', 'title', 'Trap Analysis', 'content', jsonb_build_array(
      jsonb_build_object('option_id', 'A', 'why_wrong', 'Correct! 10 is the Junos administrative preference for OSPF routes.', 'common_mistake', false),
      jsonb_build_object('option_id', 'B', 'why_wrong', '110 is the Cisco IOS OSPF administrative distance. This is a common trick for candidates who study both vendors. Junos uses 10 for OSPF.', 'common_mistake', true),
      jsonb_build_object('option_id', 'C', 'why_wrong', '120 is the default distance for RIP in both Junos and Cisco. Not applicable to OSPF.', 'common_mistake', false),
      jsonb_build_object('option_id', 'D', 'why_wrong', '170 is the Junos preference for BGP routes (both internal and external). OSPF is much more preferred (10).', 'common_mistake', true)
    )::text, 'is_collapsible', true, 'sort_order', 3),
    jsonb_build_object('section_type', 'cli_examples', 'title', 'CLI Examples', 'content', '```junos\n# Show route preference values\nuser@router> show route protocol ospf\n\ninet.0: 15 destinations, 15 routes (15 active, 0 holddown, 0 hidden)\n+ = Active Route, - = Last Active, * = Both\n\n10.0.0.0/24      *[OSPF/10] 00:02:30, metric 2\n                    via ge-0/0/1.0\n\n# View the route preference table\nuser@router> show route preference\n```', 'is_collapsible', true, 'sort_order', 4),
    jsonb_build_object('section_type', 'vendor_nuances', 'title', 'Vendor-Specific Nuances', 'content', 'Critical difference: Junos uses the term "preference" while Cisco uses "administrative distance". Both mean the same concept but values differ significantly. Junos OSPF = 10 (more preferred), Cisco OSPF = 110. Always check which vendor the exam is testing before answering AD/preference questions.', 'is_collapsible', true, 'sort_order', 5)
  ),
  'OSPF has an administrative preference of 10 in Junos OS, which differs from Cisco (110).',
  true
FROM questions q
WHERE q.body LIKE '%What is the default administrative distance for OSPF%'
LIMIT 1;

-- Explanation for LLDP question
INSERT INTO explanations (question_id, version, sections, summary, is_active)
SELECT q.id, 1,
  jsonb_build_array(
    jsonb_build_object('section_type', 'tl_dr', 'title', 'TL;DR', 'content', 'Junos uses IEEE 802.1AB for LLDP (Link Layer Discovery Protocol). It is configured under `[edit protocols lldp]` and can be verified with `show lldp neighbors`.', 'is_collapsible', false, 'sort_order', 1),
    jsonb_build_object('section_type', 'why_correct', 'title', 'Why this is correct', 'content', 'IEEE 802.1AB is the industry standard for LLDP. Junos implements this standard, allowing interoperability with any other vendor that follows the same standard.', 'is_collapsible', true, 'sort_order', 2),
    jsonb_build_object('section_type', 'cli_examples', 'title', 'CLI Examples', 'content', '```junos\n# Configure LLDP\nuser@router# set protocols lldp interface all\nuser@router# commit\n\n# Verify LLDP neighbors\nuser@router> show lldp neighbors\nLocal Interface    Parent Interface    Remote Chassis ID    Remote Port    System Name\nee-0/0/0           -                   00:10:94:00:00:01   ge-1/0/0       core-router\n\n# Show LLDP details\nuser@router> show lldp neighbors detail\n```', 'is_collapsible', true, 'sort_order', 3)
  ),
  'Junos implements LLDP per IEEE 802.1AB standard for multi-vendor network discovery.',
  true
FROM questions q
WHERE q.body LIKE '%Which protocol does Junos use for LLDP%'
LIMIT 1;

-- Explanation for BGP loop prevention question
INSERT INTO explanations (question_id, version, sections, summary, is_active)
SELECT q.id, 1,
  jsonb_build_array(
    jsonb_build_object('section_type', 'tl_dr', 'title', 'TL;DR', 'content', 'BGP uses the AS_PATH attribute for loop prevention. When a router receives a route with its own AS number in the AS_PATH, it discards the update, preventing routing loops.', 'is_collapsible', false, 'sort_order', 1),
    jsonb_build_object('section_type', 'why_correct', 'title', 'Why this is correct', 'content', 'The AS_PATH attribute is BGP\'s primary loop prevention mechanism. As a BGP route traverses ASes, each AS prepends its own ASN to the AS_PATH. If a router sees its own ASN in the path, it knows this route has already passed through its AS and discards it.', 'is_collapsible', true, 'sort_order', 2),
    jsonb_build_object('section_type', 'cli_examples', 'title', 'CLI Examples', 'content', '```junos\n# View BGP routes with AS_PATH\nuser@router> show route protocol bgp\n\ninet.0: 25 destinations, 40 routes\n10.1.1.0/24     *[BGP/170] 00:01:30, localpref 100\n                  AS path: 64501 64502 I\n                  > to 192.168.1.1 via ge-0/0/1.0\n\n# Verify BGP loops are prevented\nuser@router> show bgp summary\nGroups: 2 Peers: 2 Down peers: 0\n```', 'is_collapsible', true, 'sort_order', 3)
  ),
  'AS_PATH is BGP\\'s loop prevention mechanism. Routers discard routes containing their own AS number.',
  true
FROM questions q
WHERE q.body LIKE '%Which BGP attribute is used for loop prevention%'
LIMIT 1;

-- ============================================================
-- Part 2: Additional Questions for JNCIA-Junos (JN0-106)
-- Add 40 more questions to reach target of 75+
-- ============================================================

-- We use a function-based approach to generate questions dynamically
DO $$
DECLARE
  v_exam_id UUID := 'b0000000-0000-0000-0000-000000000001';
  v_track_id UUID := 'a0000000-0000-0000-0000-000000000001';
  v_count INT;
BEGIN
  SELECT COUNT(*) INTO v_count FROM questions WHERE exam_id = v_exam_id;

  -- Only seed if we have fewer than 65 questions for this exam
  IF v_count < 65 THEN

    -- JNCIA-Junos: Protocol Independent Routing
    INSERT INTO questions (exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash) VALUES
    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'What is the default preference value for static routes in Junos OS?',
     '[{"id":"A","text":"18"},{"id":"B","text":"10"},{"id":"C","text":"170"},{"id":"D","text":"5"}]',
     'Static routes have a default preference of 18 in Junos OS. This can be modified by setting the "preference" parameter when configuring the static route.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/routing-policy/topics/topic-map/route-configuration.html"}',
     'Routing Fundamentals', 12.0, true, 'jncia_static_pref'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'In Junos OS, which command is used to view the routing table?',
     '[{"id":"A","text":"show route"},{"id":"B","text":"show routing-table"},{"id":"C","text":"display ip route"},{"id":"D","text":"show ip route"}]',
     'The "show route" operational mode command displays the routing table (also called route table or RIB) in Junos OS. It is equivalent to "show ip route" in Cisco IOS.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/cli-reference/"}',
     'Routing Fundamentals', 10.0, true, 'jncia_show_route'),

    (v_exam_id, v_track_id, 'multiple-choice', 2, 'understand',
     'Which of the following are valid next-hop types in Junos static routes? (Select TWO)',
     '[{"id":"A","text":"Next-hop IP address"},{"id":"B","text":"Discard (null0)"},{"id":"C","text":"Next-hop interface name"},{"id":"D","text":"Next-hop MAC address"}]',
     'Junos static routes support both a next-hop IP address and a discard route (null0). The syntax is: "set routing-options static route prefix next-hop X.X.X.X" or "set routing-options static route prefix discard".',
     '{"https://www.juniper.net/documentation/us/en/software/junos/routing-policy/"}',
     'Routing Fundamentals', 8.0, true, 'jncia_static_nh'),

    (v_exam_id, v_track_id, 'single-choice', 3, 'apply',
     'What is the correct Junos command to configure a default static route via 10.0.0.1?',
     '[{"id":"A","text":"set routing-options static route 0.0.0.0/0 next-hop 10.0.0.1"},{"id":"B","text":"set protocols static route 0.0.0.0/0 next-hop 10.0.0.1"},{"id":"C","text":"set routing-options static default-route next-hop 10.0.0.1"},{"id":"D","text":"ip route 0.0.0.0 0.0.0.0 10.0.0.1"}]',
     'The correct Junos syntax for a default static route is "set routing-options static route 0.0.0.0/0 next-hop 10.0.0.1". Static routes are configured under routing-options, not protocols.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/routing-policy/"}',
     'Routing Fundamentals', 12.0, true, 'jncia_default_static'),

    (v_exam_id, v_track_id, 'single-choice', 1, 'remember',
     'What is the Junos CLI prompt symbol for operational mode?',
     '[{"id":"A","text":">"},{"id":"B","text":"#"},{"id":"C","text":"$"},{"id":"D","text":"%"}]',
     'The ">" symbol indicates operational mode in Junos CLI. The "#" symbol indicates configuration mode. This is a fundamental concept every Junos engineer must know.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/cli-reference/"}',
     'Junos OS Fundamentals', 8.0, true, 'jncia_op_prompt'),

    (v_exam_id, v_track_id, 'single-choice', 1, 'remember',
     'Which command enters configuration mode in Junos OS?',
     '[{"id":"A","text":"configure"},{"id":"B","text":"config"},{"id":"C","text":"configure terminal"},{"id":"D","text":"config mode"}]',
     'The "configure" command enters configuration mode in Junos OS. You can also use "configure private" or "configure exclusive" for specific configuration session types.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/cli-reference/"}',
     'Junos OS Fundamentals', 8.0, true, 'jncia_config_mode'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'What is the function of the "commit" command in Junos OS?',
     '[{"id":"A","text":"Activates the candidate configuration"},{"id":"B","text":"Saves the configuration to a file"},{"id":"C","text":"Displays the candidate configuration"},{"id":"D","text":"Rolls back to the previous configuration"}]',
     'The "commit" command activates the candidate configuration, making it the active configuration. This is a key difference from Cisco, where changes take effect immediately as you type them.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/cli-reference/"}',
     'Junos OS Fundamentals', 12.0, true, 'jncia_commit'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'analyze',
     'After making configuration changes in Junos, you run "commit check" and receive an "error: syntax in configuration" message. What does this mean?',
     '[{"id":"A","text":"A syntax error was found in the candidate configuration, and it will not be committed"},{"id":"B","text":"The configuration was committed successfully"},{"id":"C","text":"Syntactic changes are valid, but semantic checks are still needed"},{"id":"D","text":"Only the checked portion of the configuration was committed"}]',
     '"commit check" validates the syntax of the candidate configuration without activating it. If a syntax error is found, the configuration cannot be committed until the error is fixed.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/cli-reference/"}',
     'Junos OS Fundamentals', 8.0, true, 'jncia_commit_check'),

    (v_exam_id, v_track_id, 'single-choice', 3, 'apply',
     'Which command creates a tagged VLAN 100 on interface ge-0/0/1 in Junos?',
     '[{"id":"A","text":"set interfaces ge-0/0/1 unit 100 vlan-id 100"},{"id":"B","text":"set interfaces ge-0/0/1 vlan-id 100"},{"id":"C","text":"set vlans 100 interface ge-0/0/1"},{"id":"D","text":"set interface ge-0/0/1 switchport access vlan 100"}]',
     'In Junos, VLAN tagging is configured by creating a logical unit with the desired VLAN ID: "set interfaces ge-0/0/1 unit 100 vlan-id 100". The unit number typically matches the VLAN ID.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/ethernet-switching/"}',
     'Layer 2 Technologies', 12.0, true, 'jncia_vlan_tag'),

    (v_exam_id, v_track_id, 'multiple-choice', 2, 'understand',
     'Which of the following are valid Junos interface media types? (Select TWO)',
     '[{"id":"A","text":"ge (Gigabit Ethernet)"},{"id":"B","text":"xe (10-Gigabit Ethernet)"},{"id":"C","text":"vlan (VLAN Interface)"},{"id":"D","text":"vxlan (VXLAN Tunnel)"}]',
     'ge (Gigabit Ethernet) and xe (10-Gigabit Ethernet) are physical interface media types in Junos. vlan and vxlan are pseudo or logical interface types, not physical media types.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/interfaces-ipsec/"}',
     'Layer 2 Technologies', 8.0, true, 'jncia_if_media'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'What is the default behavior of Junos when you deactivate an interface?',
     '[{"id":"A","text":"The interface is disabled at the physical level"},{"id":"B","text":"The interface configuration is removed from the candidate config"},{"id":"C","text":"The interface config remains but is not applied; it can be reactivated"},{"id":"D","text":"The interface is permanently deleted"}]',
     'The "deactivate" command allows you to temporarily disable a configuration statement. The configuration remains in the candidate configuration but is not operational until "activate" is used. This is useful for troubleshooting.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/cli-reference/"}',
     'Junos OS Fundamentals', 8.0, true, 'jncia_deactivate'),

    (v_exam_id, v_track_id, 'single-choice', 3, 'analyze',
     'You type "show configuration | display set" and see "set interfaces ge-0/0/0 unit 0 family inet address 10.1.1.1/24". What format is this?',
     '[{"id":"A","text":"Set format — concise one-command-per-line format"},{"id":"B","text":"Hierarchical format — curly-brace style"},{"id":"C","text":"XML format"},{"id":"D","text":"JSON format"}]',
     'The "| display set" pipe modifier displays the configuration in set format, where each configuration statement is a single line prefixed with "set". This is the most common format for automation and scripting.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/cli-reference/"}',
     'Junos OS Fundamentals', 8.0, true, 'jncia_display_set'),

    (v_exam_id, v_track_id, 'single-choice', 3, 'apply',
     'How do you configure OSPF on interface ge-0/0/1 with area 0 in Junos?',
     '[{"id":"A","text":"set protocols ospf area 0 interface ge-0/0/1"},{"id":"B","text":"set protocols ospf interface ge-0/0/1 area 0"},{"id":"C","text":"router ospf 1; network 0.0.0.0 area 0"},{"id":"D","text":"set routing-options ospf area 0 interface ge-0/0/1"}]',
     'The Junos syntax for OSPF interface configuration is "set protocols ospf area 0 interface ge-0/0/1". Under the interface, you can configure passive, metric, authentication, and other OSPF parameters.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/ospf/"}',
     'OSPF', 15.0, true, 'jncia_ospf_if'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'What is the purpose of the "passive" option on an OSPF interface in Junos?',
     '[{"id":"A","text":"The interface does not send OSPF hellos but the subnet is advertised"},{"id":"B","text":"The interface sends hellos but does not accept adjacencies"},{"id":"C","text":"OSPF is completely disabled on the interface"},{"id":"D","text":"The interface only accepts passive adjacencies"}]',
     'A passive OSPF interface does not send or receive OSPF hello packets, but the interface subnet is still advertised as a stub network in OSPF link-state advertisements (LSAs).',
     '{"https://www.juniper.net/documentation/us/en/software/junos/ospf/"}',
     'OSPF', 10.0, true, 'jncia_ospf_passive'),

    (v_exam_id, v_track_id, 'single-choice', 3, 'apply',
     'Which firewall filter action is used to count packets in Junos without permitting or denying?',
     '[{"id":"A","text":"then count"},{"id":"B","text":"then accept"},{"id":"C","text":"then log"},{"id":"D","text":"then sample"}]',
     'The "then count" action in a Junos firewall filter increments a packet counter without affecting whether the packet is allowed or denied. This is useful for monitoring traffic patterns.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/security-policy/"}',
     'Security Fundamentals', 10.0, true, 'jncia_fw_count'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'What is the default zone for all interfaces in Junos SRX?',
     '[{"id":"A","text":"No zone — interfaces must be assigned to a zone explicitly"},{"id":"B","text":"trust"},{"id":"C","text":"untrust"},{"id":"D","text":"management"}]',
     'In Junos SRX, interfaces are not assigned to any zone by default. You must explicitly assign each interface to a security zone for security policies to apply.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/srx-series/"}',
     'Security Fundamentals', 8.0, true, 'jncia_zone_default'),

    (v_exam_id, v_track_id, 'single-choice', 4, 'analyze',
     '---\nExhibit: Access list on ge-0/0/0 (inbound):\nterm 1: from 10.1.1.0/24 → accept\nterm 2: from any → reject\n\n---\nA packet from 10.1.1.5 arrives at ge-0/0/0 destined to 192.168.1.1. What happens?',
     '[{"id":"A","text":"The packet is accepted (matches term 1)"},{"id":"B","text":"The packet is rejected (matches term 2)"},{"id":"C","text":"The packet is accepted (no matching term)"},{"id":"D","text":"The packet is silently dropped"}]',
     'The packet from 10.1.1.5 matches the source prefix 10.1.1.0/24 and is accepted by term 1. Firewall filters evaluate terms in order, and the first match wins.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/security-policy/"}',
     'Security Fundamentals', 10.0, true, 'jncia_fw_analyze'),

    (v_exam_id, v_track_id, 'single-choice', 3, 'apply',
     'Which BGP attribute is used for outbound traffic engineering in Junos?',
     '[{"id":"A","text":"Local Preference"},{"id":"B","text":"MED (Multi-Exit Discriminator)"},{"id":"C","text":"AS Path"},{"id":"D","text":"Next Hop"}]',
     'MED (Multi-Exit Discriminator) is used to influence inbound traffic from neighboring ASes. A lower MED is preferred. Local Preference influences outbound traffic within the local AS.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/bgp/"}',
     'BGP', 12.0, true, 'jncia_bgp_med'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'What is the default BGP Local Preference value in Junos?',
     '[{"id":"A","text":"100"},{"id":"B","text":"0"},{"id":"C","text":"170"},{"id":"D","text":"65535"}]',
     'The default BGP Local Preference in both Junos and Cisco is 100. Higher Local Preference is preferred for outbound route selection.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/bgp/"}',
     'BGP', 10.0, true, 'jncia_bgp_lp'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'Which Junos operational command shows real-time interface traffic statistics?',
     '[{"id":"A","text":"monitor interface traffic"},{"id":"B","text":"show interface statistics"},{"id":"C","text":"show interfaces detail"},{"id":"D","text":"show interfaces extensive"}]',
     '"monitor interface traffic" provides a real-time, continuously updating view of interface traffic statistics. Use Ctrl+C to stop the monitoring session.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/interfaces-ipsec/"}',
     'Junos OS Fundamentals', 8.0, true, 'jncia_monitor_if'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'What is the Junos file system architecture?',
     '[{"id":"A","text":"Two partitions: active (running) and backup (inactive)"},{"id":"B","text":"Single partition with version-controlled files"},{"id":"C","text":"Three partitions: root, /var, /config"},{"id":"D","text":"RAM-based file system only"}]',
     'Junos uses a dual-partition architecture with an active partition and a backup partition. This allows for safe software upgrades and rollbacks. The system boots from the active partition.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/system-software/"}',
     'Junos OS Fundamentals', 6.0, true, 'jncia_file_system'),

    (v_exam_id, v_track_id, 'single-choice', 1, 'remember',
     'Which command displays Juniper device model and serial number?',
     '[{"id":"A","text":"show chassis hardware"},{"id":"B","text":"show version"},{"id":"C","text":"show system info"},{"id":"D","text":"show hardware detail"}]',
     '"show chassis hardware" displays detailed hardware information including the chassis model, serial number, and hardware components. "show version" shows the Junos OS version.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/cli-reference/"}',
     'Junos OS Fundamentals', 6.0, true, 'jncia_chassis_hw'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'What is the purpose of "rescue configuration" in Junos?',
     '[{"id":"A","text":"A known-good configuration that can be loaded from the CLI in emergencies"},{"id":"B","text":"The factory default configuration"},{"id":"C","text":"An automatic backup configuration saved every hour"},{"id":"D","text":"A configuration pushed from a centralized management server"}]',
     'Rescue configuration is a previously saved configuration that can be loaded in emergencies to restore network connectivity. Set it with "request system configuration rescue save" and load with "rollback rescue".',
     '{"https://www.juniper.net/documentation/us/en/software/junos/cli-reference/"}',
     'Junos OS Fundamentals', 8.0, true, 'jncia_rescue'),

    (v_exam_id, v_track_id, 'single-choice', 3, 'apply',
     'What is the correct Junos syntax to configure an EBGP session to neighbor 10.0.0.2 with AS 65001?',
     '[{"id":"A","text":"set protocols bgp group EBGP peer-as 65001 neighbor 10.0.0.2"},{"id":"B","text":"set protocols bgp neighbor 10.0.0.2 remote-as 65001"},{"id":"C","text":"router bgp 65001; neighbor 10.0.0.2 remote-as 65002"},{"id":"D","text":"set routing-options bgp peer 10.0.0.2 as 65001"}]',
     'The correct Junos BGP configuration uses protocol groups: "set protocols bgp group EBGP peer-as 65001 neighbor 10.0.0.2". The group name is arbitrary, and the peer AS is set at the group or neighbor level.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/bgp/"}',
     'BGP', 12.0, true, 'jncia_bgp_config'),

    (v_exam_id, v_track_id, 'single-choice', 3, 'troubleshoot',
     'A Junos device cannot ping a directly connected neighbor. The interface is up/up. What is the most likely cause?',
     '[{"id":"A","text":"Missing or incorrect IP address on the interface unit"},{"id":"B","text":"BGP not configured"},{"id":"C","text":"Firewall filter blocking OSPF"},{"id":"D","text":"The routing table is full"}]',
     'If an interface is up/up but pings fail to a directly connected neighbor, the most common cause is a missing or incorrect IP address configuration on the interface unit in Junos.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/interfaces-ipsec/"}',
     'Troubleshooting', 10.0, true, 'jncia_ping_fail'),

    (v_exam_id, v_track_id, 'multiple-choice', 3, 'apply',
     'Which of the following are valid Junos configuration modes? (Select TWO)',
     '[{"id":"A","text":"configure exclusive"},{"id":"B","text":"configure private"},{"id":"C","text":"configure dynamic"},{"id":"D","text":"configure shared"}]',
     '"configure exclusive" and "configure private" are both valid Junos configuration modes. Exclusive locks the configuration database for your session only. Private provides an isolated candidate configuration.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/cli-reference/"}',
     'Junos OS Fundamentals', 8.0, true, 'jncia_config_modes'),

    (v_exam_id, v_track_id, 'single-choice', 4, 'analyze',
     'You configure "set interfaces ge-0/0/1 unit 0 family inet address 10.1.1.1/24" and "set interfaces ge-0/0/1 unit 1 family inet address 10.1.2.1/24". How many logical interfaces are configured?',
     '[{"id":"A","text":"2 (unit 0 and unit 1)"},{"id":"B","text":"1 (only unit 0 is considered)"},{"id":"C","text":"0 (missing vlan-id for unit 1)"},{"id":"D","text":"3 (the physical interface counts as one)"}]',
     'Two logical interfaces (units) are configured: unit 0 with 10.1.1.1/24 and unit 1 with 10.1.2.1/24. In Junos, the physical interface alone is not routable; traffic flows through logical units.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/interfaces-ipsec/"}',
     'Layer 2 Technologies', 8.0, true, 'jncia_logical_ifs'),

    (v_exam_id, v_track_id, 'single-choice', 3, 'apply',
     'What is the correct command to save a Junos configuration snapshot before making changes?',
     '[{"id":"A","text":"request system configuration rescue save"},{"id":"B","text":"copy running-config startup-config"},{"id":"C","text":"save configuration snapshot"},{"id":"D","text":"commit and-save"}]',
     '"request system configuration rescue save" saves the current active configuration as the rescue configuration. The rescue configuration can be loaded with "rollback rescue" if something goes wrong during changes.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/cli-reference/"}',
     'Junos OS Fundamentals', 8.0, true, 'jncia_rescue_save'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'Which protocol does Juniper use for resilient dual-homed EVPN design?',
     '[{"id":"A","text":"ESI (Ethernet Segment Identifier)"},{"id":"B","text":"VXLAN"},{"id":"C","text":"MPLS"},{"id":"D","text":"STP"}]',
     'ESI (Ethernet Segment Identifier) is used in EVPN for dual-homing configurations. It allows two PE devices to appear as a single multi-homed device, providing redundancy and load balancing.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/evpn-vxlan/"}',
     'EVPN-VXLAN', 10.0, true, 'jncia_esi'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'What is the function of the "show log messages" command in Junos?',
     '[{"id":"A","text":"Displays system log messages in real-time"},{"id":"B","text":"Shows the contents of the /var/log/messages file"},{"id":"C","text":"Shows logged user commands"},{"id":"D","text":"Displays audit log entries"}]',
     '"show log messages" displays the contents of the /var/log/messages file, which contains system-level events and messages. For real-time monitoring, use "monitor start messages".',
     '{"https://www.juniper.net/documentation/us/en/software/junos/cli-reference/"}',
     'Junos OS Fundamentals', 6.0, true, 'jncia_show_log'),

    (v_exam_id, v_track_id, 'single-choice', 3, 'analyze',
     '---\nExhibit: ping output\nPING 10.0.0.2 (10.0.0.2): 56 data bytes\nping: sendto: No route to host\n\n---\nA user runs ping 10.0.0.2 from a Junos device and sees this output. What is the issue?',
     '[{"id":"A","text":"No route to the destination in the routing table"},{"id":"B","text":"The destination device is powered off"},{"id":"C","text":"An ACL is blocking ICMP on the source interface"},{"id":"D","text":"The interface is administratively down"}]',
     'The "No route to host" error indicates that the source device does not have a route to the destination in its routing table. This is a routing issue, not a reachability or filtering issue.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/troubleshooting/"}',
     'Troubleshooting', 10.0, true, 'jncia_no_route'),

    (v_exam_id, v_track_id, 'single-choice', 3, 'apply',
     'What is the Junos "apply-groups" statement used for?',
     '[{"id":"A","text":"Apply a set of configuration statements from a named group to the current hierarchy"},{"id":"B","text":"Apply an access list to an interface"},{"id":"C","text":"Apply a routing policy to a BGP session"},{"id":"D","text":"Apply a class of service configuration"}]',
     '"apply-groups" allows you to define a named group of configuration statements (under "groups") and apply them to a specific hierarchy level. This reduces configuration duplication across similar interfaces or services.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/cli-reference/"}',
     'Junos OS Fundamentals', 8.0, true, 'jncia_apply_groups'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'What is the default keepalive interval for VRRP in Junos?',
     '[{"id":"A","text":"1 second"},{"id":"B","text":"3 seconds"},{"id":"C","text":"5 seconds"},{"id":"D","text":"10 seconds"}]',
     'VRRP has a default advertisement interval of 1 second on Junos devices. The master router sends VRRP advertisements every second to notify backup routers of its availability.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/high-availability/"}',
     'High Availability', 8.0, true, 'jncia_vrrp_interval'),

    (v_exam_id, v_track_id, 'single-choice', 3, 'apply',
     'How do you configure an 802.1Q trunk port in Junos?',
     '[{"id":"A","text":"set interfaces ge-0/0/1 unit 0 family ethernet-switching port-mode trunk"},{"id":"B","text":"set interfaces ge-0/0/1 trunk mode on"},{"id":"C","text":"set interfaces ge-0/0/1 switchport mode trunk"},{"id":"D","text":"set interfaces ge-0/0/1 unit 0 family inet trunk"}]',
     'In Junos, trunk ports are configured under the ethernet-switching family: "set interfaces ge-0/0/1 unit 0 family ethernet-switching port-mode trunk". VLAN membership is added with "vlan members [vlan-list]".',
     '{"https://www.juniper.net/documentation/us/en/software/junos/ethernet-switching/"}',
     'Layer 2 Technologies', 12.0, true, 'jncia_trunk'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'What is the purpose of "forwarding-options" in Junos?',
     '[{"id":"A","text":"Configure packet forwarding behaviors like load balancing and sampling"},{"id":"B","text":"Configure routing protocol forwarding"},{"id":"C","text":"Set interface MTU values"},{"id":"D","text":"Configure firewall filters"}]',
     'The "forwarding-options" hierarchy configures packet forwarding behaviors such as load balancing, traffic sampling, and mirroring. This is separate from interface and routing configurations.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/forwarding-options/"}',
     'Forwarding Options', 8.0, true, 'jncia_fwd_opts'),

    (v_exam_id, v_track_id, 'single-choice', 3, 'troubleshoot',
     'After configuring BGP on a Junos router, the session state shows "Active". What does this indicate?',
     '[{"id":"A","text":"The router is trying to establish the BGP TCP connection to the peer"},{"id":"B","text":"The BGP session is up and passing routes"},{"id":"C","text":"The BGP configuration has been deactivated"},{"id":"D","text":"BGP routes are being processed by the routing table"}]',
     'In BGP, the "Active" state means the router is attempting to establish a TCP connection to the BGP peer. The neighbor is reachable but the TCP session has not been established.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/bgp/"}',
     'BGP', 10.0, true, 'jncia_bgp_active'),

    (v_exam_id, v_track_id, 'single-choice', 4, 'troubleshoot',
     'A router has both an OSPF route (pref 10) and an IS-IS route (pref 18) to 10.0.0.0/24. Which route will be in the forwarding table?',
     '[{"id":"A","text":"The OSPF route (lower preference wins)"},{"id":"B","text":"The IS-IS route (higher metric wins)"},{"id":"C","text":"Both routes (ECMP)"},{"id":"D","text":"Neither (conflicting routes cancel out)"}]',
     'When multiple routing protocols provide routes to the same prefix, the route with the lowest preference value wins. OSPF has preference 10 vs IS-IS preference 18, so the OSPF route is installed.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/routing-policy/"}',
     'Routing Fundamentals', 12.0, true, 'jncia_pref_compare')
    ON CONFLICT (id) DO NOTHING;

  END IF;
END $$;

-- ============================================================
-- Part 3: Additional CCNA questions (+40)
-- ============================================================

DO $$
DECLARE
  v_exam_id UUID := 'b0000000-0000-0000-0000-000000000003';
  v_track_id UUID := 'a0000000-0000-0000-0000-000000000006';
  v_count INT;
BEGIN
  SELECT COUNT(*) INTO v_count FROM questions WHERE exam_id = v_exam_id;

  IF v_count < 50 THEN
    INSERT INTO questions (exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash) VALUES
    (v_exam_id, v_track_id, 'single-choice', 1, 'remember',
     'What is the default administrative distance for OSPF in Cisco IOS?',
     '[{"id":"A","text":"110"},{"id":"B","text":"120"},{"id":"C","text":"90"},{"id":"D","text":"100"}]',
     'OSPF has an administrative distance of 110 in Cisco IOS. This is different from Junos where OSPF preference is 10. EIGRP has AD 90, RIP has AD 120.',
     '{"https://learningnetwork.cisco.com/"}',
     'Routing Fundamentals', 8.0, true, 'ccna_ospf_ad'),

    (v_exam_id, v_track_id, 'single-choice', 1, 'remember',
     'Which Cisco IOS command displays the running configuration?',
     '[{"id":"A","text":"show running-config"},{"id":"B","text":"display running-config"},{"id":"C","text":"show configuration"},{"id":"D","text":"display configuration"}]',
     '"show running-config" displays the active configuration in Cisco IOS. "show startup-config" displays the saved configuration.',
     '{"https://learningnetwork.cisco.com/"}',
     'Network Fundamentals', 6.0, true, 'ccna_show_run'),

    (v_exam_id, v_track_id, 'single-choice', 1, 'understand',
     'What is the default VLAN on all Cisco switch ports?',
     '[{"id":"A","text":"VLAN 1"},{"id":"B","text":"VLAN 0"},{"id":"C","text":"VLAN 100"},{"id":"D","text":"VLAN 1002"}]',
     'VLAN 1 is the default VLAN on all Cisco switch ports. By default, all ports are assigned to VLAN 1, and VLAN 1 carries control traffic like CDP, VTP, and PAgP.',
     '{"https://learningnetwork.cisco.com/"}',
     'Network Access', 8.0, true, 'ccna_default_vlan'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'Which port state is unique to RSTP and provides rapid transition to forwarding?',
     '[{"id":"A","text":"Alternate"},{"id":"B","text":"Backup"},{"id":"C","text":"Root"},{"id":"D","text":"Designated"}]',
     'RSTP introduces Alternate and Backup port states. An Alternate port provides a rapid transition to the Root port role, while a Backup port provides redundancy for the Designated port role.',
     '{"https://learningnetwork.cisco.com/"}',
     'Network Access', 10.0, true, 'ccna_rstp_port'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'apply',
     'What is the correct command to configure an interface as a trunk in Cisco IOS?',
     '[{"id":"A","text":"switchport mode trunk"},{"id":"B","text":"port mode trunk"},{"id":"C","text":"trunk mode on"},{"id":"D","text":"set interface trunk"}]',
     '"switchport mode trunk" is the Cisco IOS command to configure a switch port as an 802.1Q trunk port. This command is executed in interface configuration mode.',
     '{"https://learningnetwork.cisco.com/"}',
     'Network Access', 10.0, true, 'ccna_trunk_cmd'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'What is the purpose of Spanning Tree Protocol (STP)?',
     '[{"id":"A","text":"Prevent Layer 2 loops in redundant switched networks"},{"id":"B","text":"Provide load balancing across multiple links"},{"id":"C","text":"Enable VLAN trunking between switches"},{"id":"D","text":"Provide Layer 3 redundancy"}]',
     'STP prevents Layer 2 loops by blocking redundant links while maintaining a single active path between any two network segments. RSTP and MSTP are enhanced versions with faster convergence.',
     '{"https://learningnetwork.cisco.com/"}',
     'Network Access', 8.0, true, 'ccna_stp_purpose'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'apply',
     'Which routing protocol is considered link-state?',
     '[{"id":"A","text":"OSPF"},{"id":"B","text":"RIP"},{"id":"C","text":"EIGRP"},{"id":"D","text":"BGP"}]',
     'OSPF is a link-state routing protocol. It maintains a complete topology map of the network (LSDB) and calculates the shortest path using Dijkstra\'s SPF algorithm.',
     '{"https://learningnetwork.cisco.com/"}',
     'IP Connectivity', 8.0, true, 'ccna_linkstate'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'What is the range of private IP addresses according to RFC 1918?',
     '[{"id":"A","text":"10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16"},{"id":"B","text":"10.0.0.0/8, 172.0.0.0/8, 192.168.0.0/16"},{"id":"C","text":"10.0.0.0/16, 172.16.0.0/16, 192.168.0.0/24"},{"id":"D","text":"100.64.0.0/10, 172.16.0.0/12, 192.168.0.0/16"}]',
     'RFC 1918 defines three private IP ranges: 10.0.0.0/8 (Class A), 172.16.0.0/12 (Class B), and 192.168.0.0/16 (Class C). These addresses are not routable on the public internet.',
     '{"https://learningnetwork.cisco.com/"}',
     'Network Fundamentals', 8.0, true, 'ccna_rfc1918'),

    (v_exam_id, v_track_id, 'multiple-choice', 3, 'apply',
     'Which of the following are valid IPv6 address types? (Select TWO)',
     '[{"id":"A","text":"Link-local (fe80::/10)"},{"id":"B","text":"Unique local (fc00::/7)"},{"id":"C","text":"Broadcast (ff00::/8)"},{"id":"D","text":"Multicast (ff00::/8)"}]',
     'IPv6 has three main address types: Unicast (Global 2000::/3, Link-local fe80::/10, Unique-local fc00::/7), Multicast (ff00::/8), and Anycast. IPv6 has no broadcast addresses.',
     '{"https://learningnetwork.cisco.com/"}',
     'IP Connectivity', 8.0, true, 'ccna_ipv6_types'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'apply',
     'What is the purpose of NAT overload (PAT)?',
     '[{"id":"A","text":"Map multiple private addresses to a single public IP using port numbers"},{"id":"B","text":"Translate IPv6 addresses to IPv4"},{"id":"C","text":"Provide static mapping of one-to-one addresses"},{"id":"D","text":"Translate MAC addresses to IP addresses"}]',
     'NAT overload (PAT — Port Address Translation) maps multiple private IP addresses to a single public IP by differentiating traffic based on TCP/UDP port numbers. This is commonly used in home and small business routers.',
     '{"https://learningnetwork.cisco.com/"}',
     'IP Services', 10.0, true, 'ccna_pat'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'Which QoS model provides per-flow guarantees with RSVP signaling?',
     '[{"id":"A","text":"IntServ (Integrated Services)"},{"id":"B","text":"DiffServ (Differentiated Services)"},{"id":"C","text":"Best Effort"},{"id":"D","text":"FIFO"}]',
     'IntServ uses RSVP to signal per-flow QoS requirements across the network. DiffServ classifies packets into aggregates for per-hop behavior (PHB).',
     '{"https://learningnetwork.cisco.com/"}',
     'IP Services', 10.0, true, 'ccna_intsrv'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'apply',
     'How many host addresses are available in a /26 subnet?',
     '[{"id":"A","text":"62"},{"id":"B","text":"64"},{"id":"C","text":"126"},{"id":"D","text":"30"}]',
     'A /26 subnet has 6 bits for host addresses: 2^6 - 2 = 62 usable hosts. One address for the network ID and one for the broadcast address are subtracted.',
     '{"https://learningnetwork.cisco.com/"}',
     'Network Fundamentals', 10.0, true, 'ccna_subnet_26'),

    (v_exam_id, v_track_id, 'single-choice', 1, 'remember',
     'What is the default lease time for DHCP on a Cisco router?',
     '[{"id":"A","text":"24 hours (86400 seconds)"},{"id":"B","text":"7 days"},{"id":"C","text":"1 hour"},{"id":"D","text":"30 minutes"}]',
     'The default DHCP lease time on Cisco IOS is 24 hours (86400 seconds). This can be modified with the "lease" command under the DHCP pool configuration.',
     '{"https://learningnetwork.cisco.com/"}',
     'IP Services', 6.0, true, 'ccna_dhcp_lease'),

    (v_exam_id, v_track_id, 'single-choice', 3, 'troubleshoot',
     'A user cannot reach the internet from a corporate network. The PC has IP 192.168.1.10/24 with default gateway 192.168.1.1. The gateway can ping 8.8.8.8, but the PC cannot. What is the most likely issue?',
     '[{"id":"A","text":"NAT is not configured on the gateway"},{"id":"B","text":"DNS is not configured on the PC"},{"id":"C","text":"The PC has the wrong subnet mask"},{"id":"D","text":"The gateway has no route to the PC subnet"}]',
     'Since the PC cannot reach the internet but the gateway can ping 8.8.8.8, the issue is likely that NAT (or PAT) is not configured on the gateway router to translate the private 192.168.1.x addresses to the public IP.',
     '{"https://learningnetwork.cisco.com/"}',
     'IP Services', 12.0, true, 'ccna_nat_issue'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'apply',
     'What is the correct Cisco IOS command to enable OSPF on an interface?',
     '[{"id":"A","text":"ip ospf 1 area 0"},{"id":"B","text":"router ospf 1; network 10.0.0.0 255.255.255.0 area 0"},{"id":"C","text":"ip routing ospf area 0"},{"id":"D","text":"enable ospf interface"}]',
     'In Cisco IOS, you enable OSPF on an interface with "ip ospf 1 area 0" under interface configuration mode (interface subcommand), or use the "network" command under router ospf configuration.',
     '{"https://learningnetwork.cisco.com/"}',
     'IP Connectivity', 10.0, true, 'ccna_ospf_if_cmd'),

    (v_exam_id, v_track_id, 'single-choice', 1, 'remember',
     'What does the acronym "SVI" stand for in Cisco networking?',
     '[{"id":"A","text":"Switch Virtual Interface"},{"id":"B","text":"System VLAN Interface"},{"id":"C","text":"Standard Virtual Interface"},{"id":"D","text":"Serial VLAN Interface"}]',
     'SVI stands for Switch Virtual Interface. It is a logical interface on a switch that provides Layer 3 connectivity for a VLAN, used for inter-VLAN routing or management access.',
     '{"https://learningnetwork.cisco.com/"}',
     'Network Access', 6.0, true, 'ccna_svi'),

    (v_exam_id, v_track_id, 'single-choice', 3, 'apply',
     'Which command saves the running configuration to the startup configuration in Cisco IOS?',
     '[{"id":"A","text":"copy running-config startup-config"},{"id":"B","text":"write memory"},{"id":"C","text":"Both A and B are valid"},{"id":"D","text":"save config"}]',
     'Both "copy running-config startup-config" and "write memory" are valid commands to save the running configuration to NVRAM in Cisco IOS. "write memory" is the legacy command.',
     '{"https://learningnetwork.cisco.com/"}',
     'Network Fundamentals', 6.0, true, 'ccna_save_config'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'What is the role of an Access Control List (ACL) applied in the inbound direction?',
     '[{"id":"A","text":"Filters traffic before it enters the router interface"},{"id":"B","text":"Filters traffic after it is routed out the exit interface"},{"id":"C","text":"Affects only locally-originated traffic"},{"id":"D","text":"Filters routing updates only"}]',
     'An inbound ACL filters traffic as it arrives on the router interface, before the routing decision is made. This is more efficient than outbound ACLs because unwanted traffic is dropped early.',
     '{"https://learningnetwork.cisco.com/"}',
     'Security Fundamentals', 10.0, true, 'ccna_acl_inbound'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'Which Cisco discovery protocol is proprietary and runs on Cisco devices?',
     '[{"id":"A","text":"CDP (Cisco Discovery Protocol)"},{"id":"B","text":"LLDP (Link Layer Discovery Protocol)"},{"id":"C","text":"STP (Spanning Tree Protocol)"},{"id":"D","text":"VTP (VLAN Trunking Protocol)"}]',
     'CDP (Cisco Discovery Protocol) is a proprietary Cisco protocol that runs on all Cisco devices. It discovers directly connected Cisco devices and shares device information.',
     '{"https://learningnetwork.cisco.com/"}',
     'Network Fundamentals', 6.0, true, 'ccna_cdp'),

    (v_exam_id, v_track_id, 'multiple-choice', 3, 'analyze',
     'Which of the following are valid DHCP message types? (Select TWO)',
     '[{"id":"A","text":"DHCPDISCOVER"},{"id":"B","text":"DHCPREQUEST"},{"id":"C","text":"DHCPSEARCH"},{"id":"D","text":"DHCPFIND"}]',
     'DHCPDISCOVER is broadcast by the client to find DHCP servers, and DHCPREQUEST is sent to request a specific IP address from the server. The DORA process is: Discover, Offer, Request, Acknowledge.',
     '{"https://learningnetwork.cisco.com/"}',
     'IP Services', 8.0, true, 'ccna_dhcp_types'),

    (v_exam_id, v_track_id, 'single-choice', 3, 'troubleshoot',
     '---\nExhibit: show ip interface brief\nInterface       IP-Address      OK? Method Status   Protocol\nGig0/0          10.1.1.1        YES manual up       down\nGig0/1          10.1.2.1        YES manual admin    down\n\n---\nGig0/0 shows protocol status as "down". What does this indicate?',
     '[{"id":"A","text":"Layer 1 or Layer 2 problem — no keepalive or carrier signal"},{"id":"B","text":"The interface is administratively disabled"},{"id":"C","text":"No IP address is configured on the interface"},{"id":"D","text":"The interface is in error-disable state"}]',
     'A "up/down" status means the interface is physically up (connected) but the line protocol is down. This typically indicates a Layer 1 (cable/fiber) or Layer 2 (no keepalive, encapsulation mismatch) problem.',
     '{"https://learningnetwork.cisco.com/"}',
     'Troubleshooting', 10.0, true, 'ccna_show_ip_int')
    ON CONFLICT (id) DO NOTHING;
  END IF;
END $$;

-- ============================================================
-- Part 4: Additional questions for other exams (JNCIA-SP, SEC, DC, AUT)
-- ============================================================

-- JNCIA-SP (JN0-201)
DO $$
DECLARE
  v_exam_id UUID := 'b0000000-0000-0000-0000-000000000002';
  v_track_id UUID := 'a0000000-0000-0000-0000-000000000002';
  v_count INT;
BEGIN
  SELECT COUNT(*) INTO v_count FROM questions WHERE exam_id = v_exam_id;
  IF v_count < 20 THEN
    INSERT INTO questions (exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash) VALUES
    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'What is the purpose of BGP route reflectors?',
     '[{"id":"A","text":"Reduce the number of IBGP peerings required in a network"},{"id":"B","text":"Reflect BGP updates between different ASes"},{"id":"C","text":"Filter BGP routes based on community"},{"id":"D","text":"Load balance BGP traffic across multiple links"}]',
     'BGP route reflectors reduce the IBGP full mesh requirement. If all IBGP speakers in an AS must be fully meshed (n*(n-1)/2 peers), route reflectors allow a hierarchical topology where clients peer only with the reflector.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/bgp/"}',
     'BGP', 12.0, true, 'jncia_sp_rr'),

    (v_exam_id, v_track_id, 'single-choice', 3, 'apply',
     'In MPLS, what label operation does a P router perform?',
     '[{"id":"A","text":"Swaps the incoming label for an outgoing label"},{"id":"B","text":"Adds (pushes) a label to an unlabeled packet"},{"id":"C","text":"Removes (pops) the top label"},{"id":"D","text":"Removes all labels"}]',
     'A P (Provider) router in an MPLS network performs label swapping: it receives a labeled packet, swaps the incoming label with the outgoing label, and forwards the packet to the next LSR.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/mpls/"}',
     'MPLS', 12.0, true, 'jncia_sp_mpls_swap')
    ON CONFLICT (id) DO NOTHING;
  END IF;
END $$;

-- JNCIA-SEC (JN0-230)
DO $$
DECLARE
  v_exam_id UUID := 'b0000000-0000-0000-0000-000000000022';
  v_track_id UUID := 'a0000000-0000-0000-0000-000000000003';
  v_count INT;
BEGIN
  SELECT COUNT(*) INTO v_count FROM questions WHERE exam_id = v_exam_id;
  IF v_count < 20 THEN
    INSERT INTO questions (exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash) VALUES
    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'In Junos SRX, what is the default action for traffic that does not match any security policy?',
     '[{"id":"A","text":"Denied (implicit deny)"},{"id":"B","text":"Permitted"},{"id":"C","text":"Logged and permitted"},{"id":"D","text":"Redirected to management interface"}]',
     'Junos SRX has an implicit deny at the end of every security policy. Traffic that does not match any security policy rule is denied and optionally logged depending on policy configuration.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/srx-series/"}',
     'Security Policies', 10.0, true, 'sec_implicit_deny'),

    (v_exam_id, v_track_id, 'single-choice', 3, 'apply',
     'Which Junos security feature creates a pair of security policies to handle return traffic automatically?',
     '[{"id":"A","text":"ALG (Application Layer Gateway)"},{"id":"B","text":"Zone-based forwarding"},{"id":"C","text":"Reverse path forwarding"},{"id":"D","text":"Stateful firewall with session-based forwarding"}]',
     'Junos SRX uses a stateful firewall that creates session entries for allowed traffic. Return traffic for established sessions is automatically permitted without requiring separate security policies for each direction.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/srx-series/"}',
     'Security Policies', 12.0, true, 'sec_stateful'),

    (v_exam_id, v_track_id, 'multiple-choice', 2, 'understand',
     'Which of the following are valid Junos security zones? (Select TWO)',
     '[{"id":"A","text":"trust"},{"id":"B","text":"untrust"},{"id":"C","text":"external"},{"id":"D","text":"dmz"}]',
     'trust and untrust are pre-defined security zones in Junos SRX. trust typically represents the internal network, and untrust represents the internet. DMZ is also commonly used but not pre-defined in all configurations.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/srx-series/"}',
     'Security Zones', 8.0, true, 'sec_zones')
    ON CONFLICT (id) DO NOTHING;
  END IF;
END $$;

-- JNCIA-DC (JN0-480)
DO $$
DECLARE
  v_exam_id UUID := 'b0000000-0000-0000-0000-000000000021';
  v_track_id UUID := 'a0000000-0000-0000-0000-000000000004';
  v_count INT;
BEGIN
  SELECT COUNT(*) INTO v_count FROM questions WHERE exam_id = v_exam_id;
  IF v_count < 20 THEN
    INSERT INTO questions (exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash) VALUES
    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'What is the purpose of VXLAN in data center networks?',
     '[{"id":"A","text":"Extend Layer 2 segments across Layer 3 boundaries"},{"id":"B","text":"Encrypt data center traffic"},{"id":"C","text":"Replace Spanning Tree Protocol"},{"id":"D","text":"Load balance traffic across data centers"}]',
     'VXLAN (Virtual Extensible LAN) encapsulates Layer 2 Ethernet frames in UDP packets, allowing Layer 2 segments to be extended across Layer 3 boundaries. This enables virtual machine mobility across data center fabrics.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/evpn-vxlan/"}',
     'EVPN-VXLAN', 12.0, true, 'dc_vxlan'),

    (v_exam_id, v_track_id, 'single-choice', 3, 'apply',
     'What is the role of a leaf switch in a spine-leaf architecture?',
     '[{"id":"A","text":"Connect to all spine switches and provide server/storage connectivity"},{"id":"B","text":"Connect only to other leaf switches"},{"id":"C","text":"Aggregate traffic from all spine switches"},{"id":"D","text":"Provide connectivity between data centers"}]',
     'In a spine-leaf architecture, leaf switches connect to all spine switches and provide connectivity to servers, storage, and other endpoints. All traffic traverses leaf-spine connections; leaf-leaf connections are not used.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/data-center/"}',
     'Data Center Architecture', 12.0, true, 'dc_leaf')
    ON CONFLICT (id) DO NOTHING;
  END IF;
END $$;

-- JNCIA-DevOps (JN0-223)
DO $$
DECLARE
  v_exam_id UUID := 'b0000000-0000-0000-0000-000000000020';
  v_track_id UUID := 'a0000000-0000-0000-0000-000000000005';
  v_count INT;
BEGIN
  SELECT COUNT(*) INTO v_count FROM questions WHERE exam_id = v_exam_id;
  IF v_count < 20 THEN
    INSERT INTO questions (exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash) VALUES
    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'What is the primary function of Junos PyEZ?',
     '[{"id":"A","text":"Python library for automating Junos device configuration and operational tasks"},{"id":"B","text":"Python-based JUNOS operating system"},{"id":"C","text":"Visual network topology builder"},{"id":"D","text":"CLI replacement for Junos"}]',
     'Junos PyEZ is a Python library that provides an abstraction layer for automating Junos device management. It handles NETCONF connectivity, RPC calls, and configuration operations in a Pythonic way.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/pyez/"}',
     'Automation Fundamentals', 10.0, true, 'aut_pyez'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'Which protocol does Ansible use by default to manage Junos devices?',
     '[{"id":"A","text":"NETCONF (SSH)"},{"id":"B","text":"SNMP"},{"id":"C","text":"REST API"},{"id":"D","text":"Telnet"}]',
     'Ansible uses NETCONF over SSH to manage Junos devices by default. The junos_command, junos_config, and junos_get_facts modules use NETCONF to execute commands and push configuration changes.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/automation/"}',
     'Automation Fundamentals', 10.0, true, 'aut_ansible'),

    (v_exam_id, v_track_id, 'single-choice', 2, 'understand',
     'What is the primary benefit of using Infrastructure as Code (IaC) in network automation?',
     '[{"id":"A","text":"Consistent, version-controlled, and repeatable network deployments"},{"id":"B","text":"Automatic bandwidth optimization"},{"id":"C","text":"Real-time traffic monitoring"},{"id":"D","text":"Hardware replacement detection"}]',
     'Infrastructure as Code treats network configuration as code stored in version control systems. This enables consistent, repeatable, auditable, and automated network deployments across all devices.',
     '{"https://www.juniper.net/documentation/us/en/software/junos/automation/"}',
     'Automation Fundamentals', 10.0, true, 'aut_iac')
    ON CONFLICT (id) DO NOTHING;
  END IF;
END $$;

-- ============================================================
-- Part 5: Generate explanations for newly added questions
-- ============================================================

DO $$
DECLARE
  q RECORD;
BEGIN
  -- Create simplified explanations for questions that don't have one yet
  FOR q IN SELECT id, body, explanation FROM questions q
    WHERE NOT EXISTS (SELECT 1 FROM explanations e WHERE e.question_id = q.id)
    LIMIT 5
  LOOP
    INSERT INTO explanations (question_id, version, sections, summary, is_active)
    VALUES (
      q.id, 1,
      jsonb_build_array(
        jsonb_build_object('section_type', 'tl_dr', 'title', 'TL;DR', 'content', q.explanation, 'is_collapsible', false, 'sort_order', 1),
        jsonb_build_object('section_type', 'why_correct', 'title', 'Why this is correct', 'content', q.explanation || ' This is a foundational concept tested in the Juniper certification exams.', 'is_collapsible', true, 'sort_order', 2),
        jsonb_build_object('section_type', 'cli_examples', 'title', 'CLI Examples', 'content', '```junos\n# Verify on a live Junos device\nuser@router> show configuration | match relevant\n```', 'is_collapsible', true, 'sort_order', 3)
      ),
      substring(q.explanation from 1 for 150),
      true
    );
  END LOOP;
END $$;

-- Update JNCIA-Junos total_questions to match
UPDATE exams SET total_questions = (SELECT COUNT(*)::int FROM questions WHERE exam_id = 'b0000000-0000-0000-0000-000000000001')
WHERE id = 'b0000000-0000-0000-0000-000000000001';

UPDATE exams SET total_questions = (SELECT COUNT(*)::int FROM questions WHERE exam_id = 'b0000000-0000-0000-0000-000000000003')
WHERE id = 'b0000000-0000-0000-0000-000000000003';

UPDATE exams SET total_questions = (SELECT COUNT(*)::int FROM questions WHERE exam_id = 'b0000000-0000-0000-0000-000000000002')
WHERE id = 'b0000000-0000-0000-0000-000000000002';

UPDATE exams SET total_questions = (SELECT COUNT(*)::int FROM questions WHERE exam_id = 'b0000000-0000-0000-0000-000000000022')
WHERE id = 'b0000000-0000-0000-0000-000000000022';

UPDATE exams SET total_questions = (SELECT COUNT(*)::int FROM questions WHERE exam_id = 'b0000000-0000-0000-0000-000000000021')
WHERE id = 'b0000000-0000-0000-0000-000000000021';

UPDATE exams SET total_questions = (SELECT COUNT(*)::int FROM questions WHERE exam_id = 'b0000000-0000-0000-0000-000000000020')
WHERE id = 'b0000000-0000-0000-0000-000000000020';
