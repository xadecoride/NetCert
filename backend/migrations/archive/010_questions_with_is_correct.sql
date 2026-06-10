-- Migration 010: Questions with is_correct in options JSONB
-- Fixes the missing is_correct field from migration 008

-- ============================================================
-- Part 1: JNCIA-Junos (+25 questions)
-- ============================================================

-- Q1: static route preference (correct: A=18)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand', 'What is the default preference value for static routes in Junos OS?',
'[{"id":"A","text":"18","is_correct":true},{"id":"B","text":"10","is_correct":false},{"id":"C","text":"170","is_correct":false},{"id":"D","text":"5","is_correct":false}]',
'Static routes have a default preference of 18 in Junos OS.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/routing-policy/topics/topic-map/route-configuration.html'],
'Routing Fundamentals', 12.0, true, 'jncia_static_pref_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_static_pref_v2');

-- Q2: show route command (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand', 'In Junos OS, which command is used to view the routing table?',
'[{"id":"A","text":"show route","is_correct":true},{"id":"B","text":"show routing-table","is_correct":false},{"id":"C","text":"display ip route","is_correct":false},{"id":"D","text":"show ip route","is_correct":false}]',
'The "show route" operational mode command displays the routing table in Junos OS.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli-reference/'],
'Routing Fundamentals', 10.0, true, 'jncia_show_route_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_show_route_v2');

-- Q3: default static route (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'apply', 'What is the correct Junos command to configure a default static route via 10.0.0.1?',
'[{"id":"A","text":"set routing-options static route 0.0.0.0/0 next-hop 10.0.0.1","is_correct":true},{"id":"B","text":"set protocols static route 0.0.0.0/0 next-hop 10.0.0.1","is_correct":false},{"id":"C","text":"set routing-options static default-route next-hop 10.0.0.1","is_correct":false},{"id":"D","text":"ip route 0.0.0.0 0.0.0.0 10.0.0.1","is_correct":false}]',
'The correct Junos syntax for a default static route is "set routing-options static route 0.0.0.0/0 next-hop 10.0.0.1".',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/routing-policy/'],
'Routing Fundamentals', 12.0, true, 'jncia_default_static_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_default_static_v2');

-- Q4: operational prompt symbol (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 1, 'remember', 'What is the Junos CLI prompt symbol for operational mode?',
'[{"id":"A","text":">","is_correct":true},{"id":"B","text":"#","is_correct":false},{"id":"C","text":"$","is_correct":false},{"id":"D","text":"%","is_correct":false}]',
'The ">" symbol indicates operational mode in Junos CLI.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli-reference/'],
'Junos OS Fundamentals', 8.0, true, 'jncia_op_prompt_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_op_prompt_v2');

-- Q5: configuration mode command (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 1, 'remember', 'Which command enters configuration mode in Junos OS?',
'[{"id":"A","text":"configure","is_correct":true},{"id":"B","text":"config","is_correct":false},{"id":"C","text":"configure terminal","is_correct":false},{"id":"D","text":"config mode","is_correct":false}]',
'The "configure" command enters configuration mode in Junos OS.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli-reference/'],
'Junos OS Fundamentals', 8.0, true, 'jncia_config_mode_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_config_mode_v2');

-- Q6: commit function (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand', 'What is the function of the "commit" command in Junos OS?',
'[{"id":"A","text":"Activates the candidate configuration","is_correct":true},{"id":"B","text":"Saves the configuration to a file","is_correct":false},{"id":"C","text":"Displays the candidate configuration","is_correct":false},{"id":"D","text":"Rolls back to the previous configuration","is_correct":false}]',
'The "commit" command activates the candidate configuration.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli-reference/'],
'Junos OS Fundamentals', 12.0, true, 'jncia_commit_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_commit_v2');

-- Q7: commit check error (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'analyze', 'After running "commit check" you get "error: syntax in configuration". What does this mean?',
'[{"id":"A","text":"A syntax error was found in the candidate configuration","is_correct":true},{"id":"B","text":"The configuration was committed successfully","is_correct":false},{"id":"C","text":"Syntactic changes are valid but semantic checks are needed","is_correct":false},{"id":"D","text":"Only the checked portion was committed","is_correct":false}]',
'"commit check" validates syntax of the candidate configuration without activating it.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli-reference/'],
'Junos OS Fundamentals', 8.0, true, 'jncia_commit_check_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_commit_check_v2');

-- Q8: VLAN tagging (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'apply', 'Which command creates a tagged VLAN 100 on interface ge-0/0/1 in Junos?',
'[{"id":"A","text":"set interfaces ge-0/0/1 unit 100 vlan-id 100","is_correct":true},{"id":"B","text":"set interfaces ge-0/0/1 vlan-id 100","is_correct":false},{"id":"C","text":"set vlans 100 interface ge-0/0/1","is_correct":false},{"id":"D","text":"set interface ge-0/0/1 switchport access vlan 100","is_correct":false}]',
'In Junos, VLAN tagging is configured by creating a logical unit with the desired VLAN ID.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/ethernet-switching/'],
'Layer 2 Technologies', 12.0, true, 'jncia_vlan_tag_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_vlan_tag_v2');

-- Q9: deactivate interface (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand', 'What happens in Junos when you deactivate an interface?',
'[{"id":"A","text":"Config remains but is not applied; can be reactivated","is_correct":true},{"id":"B","text":"The interface is disabled at the physical level","is_correct":false},{"id":"C","text":"The config is removed from the candidate config","is_correct":false},{"id":"D","text":"The interface is permanently deleted","is_correct":false}]',
'The "deactivate" command temporarily disables a config statement until "activate" is used.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli-reference/'],
'Junos OS Fundamentals', 8.0, true, 'jncia_deactivate_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_deactivate_v2');

-- Q10: OSPF interface (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'apply', 'How do you configure OSPF on interface ge-0/0/1 with area 0 in Junos?',
'[{"id":"A","text":"set protocols ospf area 0 interface ge-0/0/1","is_correct":true},{"id":"B","text":"set protocols ospf interface ge-0/0/1 area 0","is_correct":false},{"id":"C","text":"router ospf 1; network 0.0.0.0 area 0","is_correct":false},{"id":"D","text":"set routing-options ospf area 0 interface ge-0/0/1","is_correct":false}]',
'Junos OSPF syntax is "set protocols ospf area 0 interface ge-0/0/1".',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/ospf/'],
'OSPF', 15.0, true, 'jncia_ospf_if_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_ospf_if_v2');

-- Q11: OSPF passive (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand', 'What does the "passive" option do on an OSPF interface in Junos?',
'[{"id":"A","text":"No hellos sent but subnet is advertised","is_correct":true},{"id":"B","text":"Sends hellos but does not accept adjacencies","is_correct":false},{"id":"C","text":"OSPF is completely disabled on the interface","is_correct":false},{"id":"D","text":"Only accepts passive adjacencies","is_correct":false}]',
'A passive OSPF interface does not send/receive hellos, but the subnet is advertised in LSAs.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/ospf/'],
'OSPF', 10.0, true, 'jncia_ospf_passive_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_ospf_passive_v2');

-- Q12: firewall filter count (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'apply', 'Which firewall filter action counts packets in Junos without permitting or denying?',
'[{"id":"A","text":"then count","is_correct":true},{"id":"B","text":"then accept","is_correct":false},{"id":"C","text":"then log","is_correct":false},{"id":"D","text":"then sample","is_correct":false}]',
'The "then count" action increments a packet counter without permitting or denying.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/security-policy/'],
'Security Fundamentals', 10.0, true, 'jncia_fw_count_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_fw_count_v2');

-- Q13: SRX default zone (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand', 'What is the default zone for interfaces in Junos SRX?',
'[{"id":"A","text":"No zone; must be assigned explicitly","is_correct":true},{"id":"B","text":"trust","is_correct":false},{"id":"C","text":"untrust","is_correct":false},{"id":"D","text":"management","is_correct":false}]',
'SRX interfaces must be explicitly assigned to a security zone.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/srx-series/'],
'Security Fundamentals', 8.0, true, 'jncia_zone_default_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_zone_default_v2');

-- Q14: BGP attribute for outbound traffic engineering (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'apply', 'Which BGP attribute is used for outbound traffic engineering in Junos?',
'[{"id":"A","text":"Local Preference","is_correct":true},{"id":"B","text":"MED","is_correct":false},{"id":"C","text":"AS Path","is_correct":false},{"id":"D","text":"Next Hop","is_correct":false}]',
'Local Preference influences outbound traffic. Higher value is preferred.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/bgp/'],
'BGP', 12.0, true, 'jncia_bgp_med_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_bgp_med_v2');

-- Q15: default BGP LP (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand', 'What is the default BGP Local Preference in Junos?',
'[{"id":"A","text":"100","is_correct":true},{"id":"B","text":"0","is_correct":false},{"id":"C","text":"170","is_correct":false},{"id":"D","text":"65535","is_correct":false}]',
'Default BGP Local Preference in Junos is 100.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/bgp/'],
'BGP', 10.0, true, 'jncia_bgp_lp_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_bgp_lp_v2');

-- Q16: monitor interface traffic (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand', 'Which Junos command shows real-time interface traffic statistics?',
'[{"id":"A","text":"monitor interface traffic","is_correct":true},{"id":"B","text":"show interface statistics","is_correct":false},{"id":"C","text":"show interfaces detail","is_correct":false},{"id":"D","text":"show interfaces extensive","is_correct":false}]',
'"monitor interface traffic" provides a real-time view of interface traffic.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/interfaces-ipsec/'],
'Junos OS Fundamentals', 8.0, true, 'jncia_monitor_if_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_monitor_if_v2');

-- Q17: chassis hardware (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 1, 'remember', 'Which command displays Juniper device model and serial number?',
'[{"id":"A","text":"show chassis hardware","is_correct":true},{"id":"B","text":"show version","is_correct":false},{"id":"C","text":"show system info","is_correct":false},{"id":"D","text":"show hardware detail","is_correct":false}]',
'"show chassis hardware" displays model and serial number.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli-reference/'],
'Junos OS Fundamentals', 6.0, true, 'jncia_chassis_hw_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_chassis_hw_v2');

-- Q18: rescue configuration (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand', 'What is "rescue configuration" in Junos?',
'[{"id":"A","text":"A known-good config loaded in emergencies","is_correct":true},{"id":"B","text":"The factory default configuration","is_correct":false},{"id":"C","text":"An automatic backup saved every hour","is_correct":false},{"id":"D","text":"A config pushed from a management server","is_correct":false}]',
'Rescue configuration can be loaded with "rollback rescue".',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli-reference/'],
'Junos OS Fundamentals', 8.0, true, 'jncia_rescue_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_rescue_v2');

-- Q19: BGP configuration (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'apply', 'What is the correct Junos syntax to configure EBGP to neighbor 10.0.0.2 AS 65001?',
'[{"id":"A","text":"set protocols bgp group EBGP peer-as 65001 neighbor 10.0.0.2","is_correct":true},{"id":"B","text":"set protocols bgp neighbor 10.0.0.2 remote-as 65001","is_correct":false},{"id":"C","text":"router bgp 65001; neighbor 10.0.0.2 remote-as 65002","is_correct":false},{"id":"D","text":"set routing-options bgp peer 10.0.0.2 as 65001","is_correct":false}]',
'Junos BGP uses protocol groups.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/bgp/'],
'BGP', 12.0, true, 'jncia_bgp_config_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_bgp_config_v2');

-- Q20: ping troubleshooting (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'troubleshoot', 'A Junos device cannot ping a directly connected neighbor. Interface is up/up. Most likely cause?',
'[{"id":"A","text":"Missing or incorrect IP address on the interface unit","is_correct":true},{"id":"B","text":"BGP not configured","is_correct":false},{"id":"C","text":"Firewall filter blocking OSPF","is_correct":false},{"id":"D","text":"The routing table is full","is_correct":false}]',
'Missing or incorrect IP address is the most likely cause.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/interfaces-ipsec/'],
'Troubleshooting', 10.0, true, 'jncia_ping_fail_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_ping_fail_v2');

-- Q21: apply-groups (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'apply', 'What is "apply-groups" in Junos used for?',
'[{"id":"A","text":"Apply reusable config groups to hierarchy levels","is_correct":true},{"id":"B","text":"Apply an access list to an interface","is_correct":false},{"id":"C","text":"Apply a routing policy to BGP","is_correct":false},{"id":"D","text":"Apply class of service configuration","is_correct":false}]',
'"apply-groups" allows reusable configuration groups.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli-reference/'],
'Junos OS Fundamentals', 8.0, true, 'jncia_apply_groups_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_apply_groups_v2');

-- Q22: BGP Active state (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'troubleshoot', 'After configuring BGP, the session shows "Active". What does this mean?',
'[{"id":"A","text":"Trying to establish the TCP connection to the peer","is_correct":true},{"id":"B","text":"The BGP session is up and passing routes","is_correct":false},{"id":"C","text":"The BGP configuration has been deactivated","is_correct":false},{"id":"D","text":"BGP routes are being processed","is_correct":false}]',
'The "Active" state means the router is attempting a TCP connection to the BGP peer.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/bgp/'],
'BGP', 10.0, true, 'jncia_bgp_active_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_bgp_active_v2');

-- Q23: route preference comparison (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 4, 'troubleshoot', 'A router has OSPF route (pref 10) and IS-IS route (pref 18) to 10.0.0.0/24. Which wins?',
'[{"id":"A","text":"The OSPF route (lower preference)","is_correct":true},{"id":"B","text":"The IS-IS route (higher metric)","is_correct":false},{"id":"C","text":"Both routes (ECMP)","is_correct":false},{"id":"D","text":"Neither (conflicting routes cancel)","is_correct":false}]',
'The route with the lowest preference value wins. OSPF (10) beats IS-IS (18).',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/routing-policy/'],
'Routing Fundamentals', 12.0, true, 'jncia_pref_compare_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_pref_compare_v2');

-- Q24: configuration modes (correct: A,B - multiple-choice)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'multiple-choice', 3, 'understand', 'Which are valid Junos configuration modes? (Select TWO)',
'[{"id":"A","text":"configure exclusive","is_correct":true},{"id":"B","text":"configure private","is_correct":true},{"id":"C","text":"configure dynamic","is_correct":false},{"id":"D","text":"configure shared","is_correct":false}]',
'"configure exclusive" locks the config database; "configure private" provides isolated candidate config.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli-reference/'],
'Junos OS Fundamentals', 8.0, true, 'jncia_config_modes_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_config_modes_v2');

-- Q25: Zero Touch Provisioning (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand', 'What is the purpose of "request system zeroize" in Junos?',
'[{"id":"A","text":"Delete all config files and log files; reboot with factory defaults","is_correct":true},{"id":"B","text":"Reset only the management interface config","is_correct":false},{"id":"C","text":"Clear all firewall filters","is_correct":false},{"id":"D","text":"Remove all users from the system","is_correct":false}]',
'"request system zeroize" deletes all configuration and log files, returning the device to factory defaults.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/system/'],
'Security Fundamentals', 8.0, true, 'jncia_zeroize_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_zeroize_v2');

-- ============================================================
-- Part 2: CCNA (+15 questions)
-- ============================================================

-- CCNA Q1: OSPF AD (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 1, 'remember', 'What is the default administrative distance for OSPF in Cisco IOS?',
'[{"id":"A","text":"110","is_correct":true},{"id":"B","text":"120","is_correct":false},{"id":"C","text":"90","is_correct":false},{"id":"D","text":"100","is_correct":false}]',
'OSPF has AD 110 in Cisco IOS.',
ARRAY['https://learningnetwork.cisco.com/'],
'Routing Fundamentals', 8.0, true, 'ccna_ospf_ad_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_ospf_ad_v2');

-- CCNA Q2: show running-config (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 1, 'remember', 'Which Cisco IOS command displays the running configuration?',
'[{"id":"A","text":"show running-config","is_correct":true},{"id":"B","text":"display running-config","is_correct":false},{"id":"C","text":"show configuration","is_correct":false},{"id":"D","text":"display configuration","is_correct":false}]',
'"show running-config" displays the active config.',
ARRAY['https://learningnetwork.cisco.com/'],
'Network Fundamentals', 6.0, true, 'ccna_show_run_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_show_run_v2');

-- CCNA Q3: default VLAN (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 1, 'understand', 'What is the default VLAN on all Cisco switch ports?',
'[{"id":"A","text":"VLAN 1","is_correct":true},{"id":"B","text":"VLAN 0","is_correct":false},{"id":"C","text":"VLAN 100","is_correct":false},{"id":"D","text":"VLAN 1002","is_correct":false}]',
'VLAN 1 is the default VLAN on all Cisco switch ports.',
ARRAY['https://learningnetwork.cisco.com/'],
'Network Access', 8.0, true, 'ccna_default_vlan_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_default_vlan_v2');

-- CCNA Q4: trunk command (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'apply', 'What command configures an interface as a trunk in Cisco IOS?',
'[{"id":"A","text":"switchport mode trunk","is_correct":true},{"id":"B","text":"port mode trunk","is_correct":false},{"id":"C","text":"trunk mode on","is_correct":false},{"id":"D","text":"set interface trunk","is_correct":false}]',
'"switchport mode trunk" is the Cisco trunk command.',
ARRAY['https://learningnetwork.cisco.com/'],
'Network Access', 10.0, true, 'ccna_trunk_cmd_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_trunk_cmd_v2');

-- CCNA Q5: STP purpose (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'understand', 'What is the purpose of Spanning Tree Protocol?',
'[{"id":"A","text":"Prevent Layer 2 loops in redundant switched networks","is_correct":true},{"id":"B","text":"Provide load balancing across multiple links","is_correct":false},{"id":"C","text":"Enable VLAN trunking","is_correct":false},{"id":"D","text":"Provide Layer 3 redundancy","is_correct":false}]',
'STP prevents Layer 2 loops by blocking redundant links.',
ARRAY['https://learningnetwork.cisco.com/'],
'Network Access', 8.0, true, 'ccna_stp_purpose_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_stp_purpose_v2');

-- CCNA Q6: link-state protocol (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'apply', 'Which routing protocol is considered link-state?',
'[{"id":"A","text":"OSPF","is_correct":true},{"id":"B","text":"RIP","is_correct":false},{"id":"C","text":"EIGRP","is_correct":false},{"id":"D","text":"BGP","is_correct":false}]',
'OSPF is a link-state routing protocol using the SPF algorithm.',
ARRAY['https://learningnetwork.cisco.com/'],
'IP Connectivity', 8.0, true, 'ccna_linkstate_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_linkstate_v2');

-- CCNA Q7: private IP ranges (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'understand', 'What are the private IP ranges per RFC 1918?',
'[{"id":"A","text":"10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16","is_correct":true},{"id":"B","text":"10.0.0.0/8, 172.0.0.0/8, 192.168.0.0/16","is_correct":false},{"id":"C","text":"10.0.0.0/16, 172.16.0.0/16, 192.168.0.0/24","is_correct":false},{"id":"D","text":"100.64.0.0/10, 172.16.0.0/12, 192.168.0.0/16","is_correct":false}]',
'RFC 1918: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16.',
ARRAY['https://learningnetwork.cisco.com/'],
'Network Fundamentals', 8.0, true, 'ccna_rfc1918_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_rfc1918_v2');

-- CCNA Q8: NAT overload (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'apply', 'What is the purpose of NAT overload (PAT)?',
'[{"id":"A","text":"Map multiple private IPs to a single public IP using ports","is_correct":true},{"id":"B","text":"Translate IPv6 to IPv4","is_correct":false},{"id":"C","text":"Static one-to-one mapping","is_correct":false},{"id":"D","text":"Translate MAC addresses to IPs","is_correct":false}]',
'PAT maps multiple private IPs to a single public IP differentiated by port numbers.',
ARRAY['https://learningnetwork.cisco.com/'],
'IP Services', 10.0, true, 'ccna_pat_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_pat_v2');

-- CCNA Q9: /26 subnet hosts (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'apply', 'How many host addresses are available in a /26 subnet?',
'[{"id":"A","text":"62","is_correct":true},{"id":"B","text":"64","is_correct":false},{"id":"C","text":"126","is_correct":false},{"id":"D","text":"30","is_correct":false}]',
'A /26 has 6 host bits: 2^6 - 2 = 62 usable addresses.',
ARRAY['https://learningnetwork.cisco.com/'],
'Network Fundamentals', 10.0, true, 'ccna_subnet_26_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_subnet_26_v2');

-- CCNA Q10: DHCP lease (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 1, 'remember', 'Default DHCP lease time on a Cisco router?',
'[{"id":"A","text":"24 hours (86400 seconds)","is_correct":true},{"id":"B","text":"7 days","is_correct":false},{"id":"C","text":"1 hour","is_correct":false},{"id":"D","text":"30 minutes","is_correct":false}]',
'Default DHCP lease on Cisco IOS is 24 hours.',
ARRAY['https://learningnetwork.cisco.com/'],
'IP Services', 6.0, true, 'ccna_dhcp_lease_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_dhcp_lease_v2');

-- CCNA Q11: NAT troubleshooting (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 3, 'troubleshoot', 'PC (192.168.1.10/24, gw 192.168.1.1) cannot reach internet. Gateway can ping 8.8.8.8, PC cannot. Most likely?',
'[{"id":"A","text":"NAT not configured on the gateway","is_correct":true},{"id":"B","text":"DNS not configured on the PC","is_correct":false},{"id":"C","text":"Wrong subnet mask on PC","is_correct":false},{"id":"D","text":"No route from gateway to PC subnet","is_correct":false}]',
'Since the gateway reaches 8.8.8.8, NAT/PAT is likely not configured.',
ARRAY['https://learningnetwork.cisco.com/'],
'IP Services', 12.0, true, 'ccna_nat_issue_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_nat_issue_v2');

-- CCNA Q12: OSPF interface subcommand (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'apply', 'What is the IOS interface subcommand to enable OSPF?',
'[{"id":"A","text":"ip ospf 1 area 0","is_correct":true},{"id":"B","text":"router ospf 1","is_correct":false},{"id":"C","text":"ip routing ospf area 0","is_correct":false},{"id":"D","text":"enable ospf interface","is_correct":false}]',
'"ip ospf 1 area 0" enables OSPF on an interface.',
ARRAY['https://learningnetwork.cisco.com/'],
'IP Connectivity', 10.0, true, 'ccna_ospf_if_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_ospf_if_v2');

-- CCNA Q13: SVI meaning (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 1, 'remember', 'What does SVI stand for?',
'[{"id":"A","text":"Switch Virtual Interface","is_correct":true},{"id":"B","text":"System VLAN Interface","is_correct":false},{"id":"C","text":"Standard Virtual Interface","is_correct":false},{"id":"D","text":"Serial VLAN Interface","is_correct":false}]',
'SVI = Switch Virtual Interface for Layer 3 VLAN connectivity.',
ARRAY['https://learningnetwork.cisco.com/'],
'Network Access', 6.0, true, 'ccna_svi_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_svi_v2');

-- CCNA Q14: inbound ACL (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'understand', 'What does an inbound ACL do?',
'[{"id":"A","text":"Filters traffic before it enters the router interface","is_correct":true},{"id":"B","text":"Filters traffic after routing out the exit interface","is_correct":false},{"id":"C","text":"Affects only locally-originated traffic","is_correct":false},{"id":"D","text":"Filters routing updates only","is_correct":false}]',
'An inbound ACL filters traffic arriving on the interface before the routing decision.',
ARRAY['https://learningnetwork.cisco.com/'],
'Security Fundamentals', 10.0, true, 'ccna_acl_inbound_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_acl_inbound_v2');

-- CCNA Q15: EtherChannel purpose (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'understand', 'What is the purpose of EtherChannel?',
'[{"id":"A","text":"Combine multiple physical links into a single logical link for bandwidth and redundancy","is_correct":true},{"id":"B","text":"Encrypt traffic between switches","is_correct":false},{"id":"C","text":"Provide VLAN tagging between devices","is_correct":false},{"id":"D","text":"Create a loop-free Layer 2 topology","is_correct":false}]',
'EtherChannel bundles multiple physical links into a single logical link.',
ARRAY['https://learningnetwork.cisco.com/'],
'Network Access', 8.0, true, 'ccna_etherchannel_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_etherchannel_v2');

-- ============================================================
-- Part 3: SP (+3), SEC (+3), DC (+3), AUT (+3), JNCIS-ENT (+10), JNCIP-ENT (+10)
-- ============================================================

-- SP Q1: BGP route reflectors (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'single-choice', 2, 'understand', 'What is the purpose of BGP route reflectors?',
'[{"id":"A","text":"Reduce the number of IBGP peerings required","is_correct":true},{"id":"B","text":"Reflect BGP updates between different ASes","is_correct":false},{"id":"C","text":"Filter BGP routes based on community","is_correct":false},{"id":"D","text":"Load balance BGP traffic","is_correct":false}]',
'Route reflectors reduce the IBGP full mesh requirement.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/bgp/'],
'BGP', 12.0, true, 'sp_rr_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'sp_rr_v2');

-- SP Q2: MPLS P router (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'single-choice', 3, 'apply', 'In MPLS, what label operation does a P router perform?',
'[{"id":"A","text":"Swaps the incoming label for an outgoing label","is_correct":true},{"id":"B","text":"Adds (pushes) a label","is_correct":false},{"id":"C","text":"Removes (pops) the top label","is_correct":false},{"id":"D","text":"Removes all labels","is_correct":false}]',
'A P router performs label swapping.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/mpls/'],
'MPLS', 12.0, true, 'sp_mpls_swap_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'sp_mpls_swap_v2');

-- SP Q3: LDP purpose (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'single-choice', 2, 'understand', 'What does LDP do in an MPLS network?',
'[{"id":"A","text":"Distributes label bindings to LDP peers","is_correct":true},{"id":"B","text":"Forwards MPLS packets","is_correct":false},{"id":"C","text":"Signals RSVP-TE tunnels","is_correct":false},{"id":"D","text":"Distributes routing information","is_correct":false}]',
'LDP distributes label bindings to MPLS LDP peers.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/mpls/'],
'MPLS', 10.0, true, 'sp_ldp_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'sp_ldp_v2');

-- SP Q4: IS-IS level (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'single-choice', 2, 'understand', 'Which IS-IS level is equivalent to OSPF area 0 (backbone)?',
'[{"id":"A","text":"Level 2","is_correct":true},{"id":"B","text":"Level 1","is_correct":false},{"id":"C","text":"Level 3","is_correct":false},{"id":"D","text":"Level 1-2","is_correct":false}]',
'IS-IS Level 2 routers form the backbone, similar to OSPF area 0.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/is-is/'],
'IS-IS', 10.0, true, 'sp_isis_level_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'sp_isis_level_v2');

-- SP Q5: BGP next-hop-self (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'single-choice', 3, 'apply', 'In Junos, what does "next-hop self" do in a BGP group configuration?',
'[{"id":"A","text":"Advertise routes with the local router as next-hop","is_correct":true},{"id":"B","text":"Set the next-hop to the original sender","is_correct":false},{"id":"C","text":"Disable next-hop processing for the group","is_correct":false},{"id":"D","text":"Enable BGP multipath","is_correct":false}]',
'"next-hop self" forces BGP to advertise itself as the next-hop for routes.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/bgp/'],
'BGP', 10.0, true, 'sp_nhs_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'sp_nhs_v2');

-- SEC Q1: implicit deny (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000022', 'a0000000-0000-0000-0000-000000000003', 'single-choice', 2, 'understand', 'In Junos SRX, what is the default action for traffic not matching any policy?',
'[{"id":"A","text":"Denied (implicit deny)","is_correct":true},{"id":"B","text":"Permitted","is_correct":false},{"id":"C","text":"Logged and permitted","is_correct":false},{"id":"D","text":"Redirected to management interface","is_correct":false}]',
'Junos SRX has an implicit deny at the end of every security policy.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/srx-series/'],
'Security Policies', 10.0, true, 'sec_implicit_deny_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'sec_implicit_deny_v2');

-- SEC Q2: stateful firewall (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000022', 'a0000000-0000-0000-0000-000000000003', 'single-choice', 3, 'apply', 'How does SRX handle return traffic for established sessions?',
'[{"id":"A","text":"Stateful firewall with session-based forwarding","is_correct":true},{"id":"B","text":"ALG","is_correct":false},{"id":"C","text":"Reverse path forwarding","is_correct":false},{"id":"D","text":"Zone-based forwarding","is_correct":false}]',
'SRX uses stateful firewall with session entries for return traffic.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/srx-series/'],
'Security Policies', 12.0, true, 'sec_stateful_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'sec_stateful_v2');

-- SEC Q3: from-zone to-zone (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000022', 'a0000000-0000-0000-0000-000000000003', 'single-choice', 2, 'understand', 'Which policy type allows traffic from trust to untrust in SRX?',
'[{"id":"A","text":"From-zone trust to-zone untrust","is_correct":true},{"id":"B","text":"From-zone untrust to-zone trust","is_correct":false},{"id":"C","text":"Global security policy","is_correct":false},{"id":"D","text":"Interface security policy","is_correct":false}]',
'Junos SRX uses from-zone/to-zone security policies.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/srx-series/'],
'Security Policies', 10.0, true, 'sec_from_to_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'sec_from_to_v2');

-- SEC Q4: Screenzones (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000022', 'a0000000-0000-0000-0000-000000000003', 'single-choice', 2, 'understand', 'What is a screen (screenzones) in Junos SRX?',
'[{"id":"A","text":"Zone-based security features that protect against DoS and flood attacks","is_correct":true},{"id":"B","text":"A virtual display for monitoring traffic","is_correct":false},{"id":"C","text":"An interface filtering feature for web traffic","is_correct":false},{"id":"D","text":"A logging mechanism for security events","is_correct":false}]',
'Screens are zone-based security features to protect against various attacks.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/srx-series/'],
'Security Policies', 8.0, true, 'sec_screens_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'sec_screens_v2');

-- SEC Q5: IPsec (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000022', 'a0000000-0000-0000-0000-000000000003', 'single-choice', 3, 'apply', 'In Junos SRX, which phase of IPsec establishes the IKE security association?',
'[{"id":"A","text":"IKE Phase 1","is_correct":true},{"id":"B","text":"IKE Phase 2","is_correct":false},{"id":"C","text":"IPsec Phase 1","is_correct":false},{"id":"D","text":"AH Phase","is_correct":false}]',
'IKE Phase 1 establishes the initial security association for key exchange.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/vpn/'],
'IPsec VPN', 10.0, true, 'sec_ipsec_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'sec_ipsec_v2');

-- DC Q1: VXLAN purpose (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000021', 'a0000000-0000-0000-0000-000000000004', 'single-choice', 2, 'understand', 'What is the purpose of VXLAN in data center networks?',
'[{"id":"A","text":"Extend Layer 2 segments across Layer 3 boundaries","is_correct":true},{"id":"B","text":"Encrypt data center traffic","is_correct":false},{"id":"C","text":"Replace Spanning Tree Protocol","is_correct":false},{"id":"D","text":"Load balance traffic across DCs","is_correct":false}]',
'VXLAN encapsulates L2 frames in UDP to extend L2 across L3 boundaries.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/evpn-vxlan/'],
'EVPN-VXLAN', 12.0, true, 'dc_vxlan_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'dc_vxlan_v2');

-- DC Q2: VXLAN port (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000021', 'a0000000-0000-0000-0000-000000000004', 'single-choice', 3, 'apply', 'What is the VXLAN UDP destination port?',
'[{"id":"A","text":"4789","is_correct":true},{"id":"B","text":"8472","is_correct":false},{"id":"C","text":"6633","is_correct":false},{"id":"D","text":"179","is_correct":false}]',
'The IANA-assigned VXLAN UDP destination port is 4789.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/evpn-vxlan/'],
'EVPN-VXLAN', 8.0, true, 'dc_vxlan_port_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'dc_vxlan_port_v2');

-- DC Q3: leaf switch role (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000021', 'a0000000-0000-0000-0000-000000000004', 'single-choice', 2, 'understand', 'What is the role of a leaf switch in spine-leaf?',
'[{"id":"A","text":"Connects to all spines and provides server access","is_correct":true},{"id":"B","text":"Connects only to other leaf switches","is_correct":false},{"id":"C","text":"Aggregates traffic from all spines","is_correct":false},{"id":"D","text":"Provides inter-DC connectivity","is_correct":false}]',
'Leaf switches connect to all spine switches and provide server connectivity.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/data-center/'],
'Data Center Architecture', 12.0, true, 'dc_leaf_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'dc_leaf_v2');

-- DC Q4: EVPN route type 2 (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000021', 'a0000000-0000-0000-0000-000000000004', 'single-choice', 3, 'understand', 'In EVPN, what does Route Type 2 (MAC/IP Advertisement) carry?',
'[{"id":"A","text":"MAC address and IP address of an attached host","is_correct":true},{"id":"B","text":"The Ethernet segment identifier","is_correct":false},{"id":"C","text":"Inclusive multicast Ethernet tag routes","is_correct":false},{"id":"D","text":"IP prefix reachability information","is_correct":false}]',
'EVPN Route Type 2 carries MAC and IP address information of attached hosts.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/evpn-vxlan/'],
'EVPN-VXLAN', 10.0, true, 'dc_evpn_rt2_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'dc_evpn_rt2_v2');

-- DC Q5: MC-LAG (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000021', 'a0000000-0000-0000-0000-000000000004', 'single-choice', 3, 'apply', 'What is the purpose of MC-LAG in Junos?',
'[{"id":"A","text":"Multi-chassis LAG for active-active redundancy across two switches","is_correct":true},{"id":"B","text":"Multi-core LAG for distributing traffic across CPU cores","is_correct":false},{"id":"C","text":"Management control LAG for out-of-band management","is_correct":false},{"id":"D","text":"Multi-cast LAG for video traffic","is_correct":false}]',
'MC-LAG enables multi-chassis link aggregation across two switches.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/ethernet-switching/'],
'Data Center Architecture', 10.0, true, 'dc_mclag_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'dc_mclag_v2');

-- AUT Q1: PyEZ (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000020', 'a0000000-0000-0000-0000-000000000005', 'single-choice', 2, 'understand', 'What is Junos PyEZ?',
'[{"id":"A","text":"Python library for Junos automation via NETCONF","is_correct":true},{"id":"B","text":"Python OS for Junos","is_correct":false},{"id":"C","text":"Visual topology builder","is_correct":false},{"id":"D","text":"CLI replacement for Junos","is_correct":false}]',
'Junos PyEZ is a Python library for Junos automation via NETCONF.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/pyez/'],
'Automation Fundamentals', 10.0, true, 'aut_pyez_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'aut_pyez_v2');

-- AUT Q2: Ansible (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000020', 'a0000000-0000-0000-0000-000000000005', 'single-choice', 2, 'understand', 'What protocol does Ansible use by default for Junos?',
'[{"id":"A","text":"NETCONF (SSH)","is_correct":true},{"id":"B","text":"SNMP","is_correct":false},{"id":"C","text":"REST API","is_correct":false},{"id":"D","text":"Telnet","is_correct":false}]',
'Ansible uses NETCONF over SSH for Junos management.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/automation/'],
'Automation Fundamentals', 10.0, true, 'aut_ansible_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'aut_ansible_v2');

-- AUT Q3: IaC benefit (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000020', 'a0000000-0000-0000-0000-000000000005', 'single-choice', 2, 'understand', 'What is the primary benefit of Infrastructure as Code?',
'[{"id":"A","text":"Consistent, repeatable, version-controlled deployments","is_correct":true},{"id":"B","text":"Automatic bandwidth optimization","is_correct":false},{"id":"C","text":"Real-time traffic monitoring","is_correct":false},{"id":"D","text":"Hardware replacement detection","is_correct":false}]',
'IaC treats config as version-controlled code for consistent deployments.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/automation/'],
'Automation Fundamentals', 10.0, true, 'aut_iac_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'aut_iac_v2');

-- AUT Q4: Salt (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000020', 'a0000000-0000-0000-0000-000000000005', 'single-choice', 2, 'understand', 'What is the role of Salt (SaltStack) in network automation?',
'[{"id":"A","text":"Configuration management and remote execution engine","is_correct":true},{"id":"B","text":"SNMP trap collector","is_correct":false},{"id":"C","text":"Network topology discovery tool","is_correct":false},{"id":"D","text":"Packet capture and analysis tool","is_correct":false}]',
'Salt is a configuration management and remote execution engine.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/automation/'],
'Automation Fundamentals', 8.0, true, 'aut_salt_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'aut_salt_v2');

-- AUT Q5: JSNAPy (correct: A)
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000020', 'a0000000-0000-0000-0000-000000000005', 'single-choice', 2, 'understand', 'What is JSNAPy used for in Junos automation?',
'[{"id":"A","text":"Testing and validating operational state of Junos devices","is_correct":true},{"id":"B","text":"Compiling SLAX scripts","is_correct":false},{"id":"C","text":"Monitoring interface statistics","is_correct":false},{"id":"D","text":"Generating configuration templates","is_correct":false}]',
'JSNAPy validates operational state against expected values.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/automation/'],
'Automation Fundamentals', 8.0, true, 'aut_jsnapy_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'aut_jsnapy_v2');

-- ============================================================
-- Part 4: JNCIS-ENT (+10 questions)
-- ============================================================

-- JNCIS-ENT Q1
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000010', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'apply', 'In Junos, which command displays OSPF neighbor states?',
'[{"id":"A","text":"show ospf neighbor","is_correct":true},{"id":"B","text":"show protocols ospf neighbor","is_correct":false},{"id":"C","text":"show ospf adjacency","is_correct":false},{"id":"D","text":"show routing protocols ospf neighbor","is_correct":false}]',
'"show ospf neighbor" displays OSPF neighbor states and adjacencies.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/ospf/'],
'OSPF', 10.0, true, 'jnce1_ospf_nbr_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jnce1_ospf_nbr_v2');

-- JNCIS-ENT Q2
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000010', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'apply', 'What is the default IS-IS metric style in Junos?',
'[{"id":"A","text":"narrow (6-bit)","is_correct":true},{"id":"B","text":"wide (24-bit)","is_correct":false},{"id":"C","text":"extended (32-bit)","is_correct":false},{"id":"D","text":"No default metric","is_correct":false}]',
'Junos defaults to narrow metrics (1-63) for IS-IS.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/is-is/'],
'IS-IS', 10.0, true, 'jnce1_isis_metric_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jnce1_isis_metric_v2');

-- JNCIS-ENT Q3
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000010', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 4, 'troubleshoot', 'An OSPF neighbor is stuck in ExStart state. Most likely cause?',
'[{"id":"A","text":"MTU mismatch between the two routers","is_correct":true},{"id":"B","text":"Area ID mismatch","is_correct":false},{"id":"C","text":"Hello timer mismatch","is_correct":false},{"id":"D","text":"OSPF process not enabled","is_correct":false}]',
'ExStart state indicates MTU mismatch on the link.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/ospf/'],
'OSPF Troubleshooting', 12.0, true, 'jnce1_ospf_exstart_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jnce1_ospf_exstart_v2');

-- JNCIS-ENT Q4
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000010', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'apply', 'In Junos, how do you configure a BGP export policy that only advertises loopback routes?',
'[{"id":"A","text":"policy-statement EXPORT-LO term 1 from interface lo0; then accept","is_correct":true},{"id":"B","text":"policy-statement EXPORT-LO term 1 from route-filter 127.0.0.0/8; then accept","is_correct":false},{"id":"C","text":"set protocols bgp export lo0-only","is_correct":false},{"id":"D","text":"set routing-options bgp advertise-loopback","is_correct":false}]',
'BGP export policies can filter by interface source.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/bgp/'],
'BGP Policy', 12.0, true, 'jnce1_bgp_export_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jnce1_bgp_export_v2');

-- JNCIS-ENT Q5
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000010', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'understand', 'What is the purpose of "shared bandwidth" in Junos class of service?',
'[{"id":"A","text":"Distributes excess bandwidth among competing queues","is_correct":true},{"id":"B","text":"Shares bandwidth between interfaces on the same PIC","is_correct":false},{"id":"C","text":"Enables multi-chassis link aggregation","is_correct":false},{"id":"D","text":"Allows unused bandwidth to be used by other forwarding classes","is_correct":false}]',
'Shared bandwidth distributes remaining bandwidth among competing queues based on their configured share.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cos/'],
'Class of Service', 10.0, true, 'jnce1_cos_share_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jnce1_cos_share_v2');

-- JNCIS-ENT Q6
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000010', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 4, 'troubleshoot', 'BGP routes are received but not installed in routing table. "show route protocol bgp" shows them as hidden. Most likely?',
'[{"id":"A","text":"No valid route to the BGP next-hop","is_correct":true},{"id":"B","text":"BGP session is in Idle state","is_correct":false},{"id":"C","text":"Export policy is blocking the routes","is_correct":false},{"id":"D","text":"Maximum prefix limit exceeded","is_correct":false}]',
'Hidden BGP routes typically indicate no route to the BGP next-hop.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/bgp/'],
'BGP Troubleshooting', 12.0, true, 'jnce1_bgp_hidden_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jnce1_bgp_hidden_v2');

-- JNCIS-ENT Q7
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000010', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'apply', 'What is the correct Junos configuration for VRRP on interface ge-0/0/1?',
'[{"id":"A","text":"set interfaces ge-0/0/1 unit 0 family inet address 10.0.0.1/24 vrrp-group 1 virtual-address 10.0.0.254","is_correct":true},{"id":"B","text":"set protocols vrrp interface ge-0/0/1 virtual-ip 10.0.0.254","is_correct":false},{"id":"C","text":"set routing-options vrrp group 1 virtual-address 10.0.0.254","is_correct":false},{"id":"D","text":"set interfaces ge-0/0/1 vrrp-group 1 virtual-address 10.0.0.254","is_correct":false}]',
'VRRP is configured under the interface address hierarchy in Junos.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/vrrp/'],
'High Availability', 10.0, true, 'jnce1_vrrp_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jnce1_vrrp_v2');

-- JNCIS-ENT Q8
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000010', 'a0000000-0000-0000-0000-000000000001', 'multiple-choice', 4, 'understand', 'Which statements about Junos routing instances are correct? (Select TWO)',
'[{"id":"A","text":"Each routing instance has its own routing table","is_correct":true},{"id":"B","text":"Routing instances can share interfaces between instances","is_correct":false},{"id":"C","text":"The default instance is called inet.0","is_correct":false},{"id":"D","text":"Instance-import can leak routes between routing instances","is_correct":true}]',
'Routing instances have independent tables and instance-import can import routes from other instances.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/routing-instances/'],
'Routing Instances', 12.0, true, 'jnce1_routing_inst_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jnce1_routing_inst_v2');

-- JNCIS-ENT Q9
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000010', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 4, 'analyze', 'In Junos, what is the purpose of "forwarding-options helpers bootp"?',
'[{"id":"A","text":"Configure DHCP relay agent functionality","is_correct":true},{"id":"B","text":"Enable BOOTP server on the router","is_correct":false},{"id":"C","text":"Forward DNS queries to external servers","is_correct":false},{"id":"D","text":"Configure NTP broadcast forwarding","is_correct":false}]',
'DHCP relay is configured under forwarding-options helpers bootp in Junos.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/forwarding-options/'],
'DHCP Services', 8.0, true, 'jnce1_dhcp_relay_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jnce1_dhcp_relay_v2');

-- JNCIS-ENT Q10
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000010', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'apply', 'What is the correct Junos command to configure MSTP?',
'[{"id":"A","text":"set protocols mstp configuration-name DC-MSTP","is_correct":true},{"id":"B","text":"set spanning-tree mode mst","is_correct":false},{"id":"C","text":"set protocols rstp mode mst","is_correct":false},{"id":"D","text":"set ethernet-switching-options mstp enable","is_correct":false}]',
'Junos uses "set protocols mstp" for MSTP configuration.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/ethernet-switching/'],
'Layer 2 Technologies', 10.0, true, 'jnce1_mstp_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jnce1_mstp_v2');

-- ============================================================
-- Part 5: JNCIP-ENT (+10 questions)
-- ============================================================

-- JNCIP-ENT Q1
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000011', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 4, 'troubleshoot', 'In a Junos VPLS environment, MAC addresses are not learning across the MPLS network. Most likely cause?',
'[{"id":"A","text":"MTU mismatch in the MPLS LSP or incorrect VPLS encapsulation","is_correct":true},{"id":"B","text":"BGP session not established","is_correct":false},{"id":"C","text":"VLAN ID mismatch","is_correct":false},{"id":"D","text":"Interface not in trunk mode","is_correct":false}]',
'MAC learning failures in VPLS often relate to MTU or encapsulation issues.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/vpls/'],
'VPLS', 12.0, true, 'jnce2_vpls_mac_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jnce2_vpls_mac_v2');

-- JNCIP-ENT Q2
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000011', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 5, 'troubleshoot', 'You have configured BGP add-path on a Juniper router, but only one path is being advertised. What could be missing?',
'[{"id":"A","text":"The BGP group needs bgp-options add-path and the routing policy must use add-path action in both config and policy","is_correct":true},{"id":"B","text":"The BGP session must be restarted","is_correct":false},{"id":"C","text":"The peer does not need add-path support","is_correct":false},{"id":"D","text":"Multipath must be enabled","is_correct":false}]',
'BGP add-path requires both the configuration and policy action.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/bgp/'],
'BGP Advanced', 15.0, true, 'jnce2_bgp_addpath_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jnce2_bgp_addpath_v2');

-- JNCIP-ENT Q3
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000011', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 4, 'apply', 'In Junos, how do you configure LDP-over-RSVP tunneling?',
'[{"id":"A","text":"Enable LDP on the RSVP-signaled MPLS interface; LDP will automatically use the RSVP LSP","is_correct":true},{"id":"B","text":"Set protocols ldp tunneled-rsvp","is_correct":false},{"id":"C","text":"Configure ldp-over-rsvp under routing-options","is_correct":false},{"id":"D","text":"RSVP and LDP cannot coexist","is_correct":false}]',
'LDP automatically uses RSVP-signaled LSPs when both are enabled on an interface.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/mpls/'],
'MPLS', 12.0, true, 'jnce2_ldp_rsvp_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jnce2_ldp_rsvp_v2');

-- JNCIP-ENT Q4
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000011', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 4, 'troubleshoot', 'OSPF virtual-link is stuck in Init state. What is the most likely cause?',
'[{"id":"A","text":"Reachability issue between the two endpoints of the virtual link","is_correct":true},{"id":"B","text":"Hello timer mismatch","is_correct":false},{"id":"C","text":"Area 0 not configured","is_correct":false},{"id":"D","text":"MTU mismatch","is_correct":false}]',
'Virtual-links require IP reachability between endpoints to establish adjacency.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/ospf/'],
'OSPF Advanced', 12.0, true, 'jnce2_ospf_vlink_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jnce2_ospf_vlink_v2');

-- JNCIP-ENT Q5
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000011', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 5, 'design', 'You need to design a network with BGP-LU (BGP labelled unicast) and MPLS. What is the minimal BGP configuration required on the route reflector?',
'[{"id":"A","text":"family inet labeled-unicast under the BGP group with route-reflector-client","is_correct":true},{"id":"B","text":"family inet unicast with send-community","is_correct":false},{"id":"C","text":"family inet-vpn unicast","is_correct":false},{"id":"D","text":"family route-target","is_correct":false}]',
'BGP-LU uses the inet labeled-unicast address family.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/bgp/'],
'BGP Advanced', 15.0, true, 'jnce2_bgp_lu_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jnce2_bgp_lu_v2');

-- JNCIP-ENT Q6
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000011', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 4, 'apply', 'In Junos, what is the purpose of "protocols ldp transport-address" configuration?',
'[{"id":"A","text":"Specify which interface IP to use for LDP TCP sessions","is_correct":true},{"id":"B","text":"Define the MTU for LDP packets","is_correct":false},{"id":"C","text":"Set the transport class for LDP packets","is_correct":false},{"id":"D","text":"Configure LDP over MPLS TE tunnels","is_correct":false}]',
'The LDP transport-address specifies the source IP for LDP TCP connections.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/mpls/'],
'MPLS', 10.0, true, 'jnce2_ldp_transport_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jnce2_ldp_transport_v2');

-- JNCIP-ENT Q7
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000011', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 4, 'troubleshoot', 'RSVP-signaled LSPs are going down and up repeatedly (flapping). What is the most likely cause?',
'[{"id":"A","text":"Interface flapping or RSVP hello failure along the path","is_correct":true},{"id":"B","text":"BGP session reset","is_correct":false},{"id":"C","text":"LDP session flapping","is_correct":false},{"id":"D","text":"OSPF route flapping","is_correct":false}]',
'RSVP LSP flapping is usually caused by physical or RSVP hello failures.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/mpls/'],
'MPLS TE', 12.0, true, 'jnce2_rsvp_flap_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jnce2_rsvp_flap_v2');

-- JNCIP-ENT Q8
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000011', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 5, 'design', 'Which IPsec VPN type is most appropriate for hub-and-spoke interconnecting multiple branch offices through an MPLS core?',
'[{"id":"A","text":"Route-based VPN with tunnel interfaces","is_correct":true},{"id":"B","text":"Policy-based VPN with proxy-IDs","is_correct":false},{"id":"C","text":"Dynamic multipoint VPN (DMVPN)","is_correct":false},{"id":"D","text":"SSL VPN","is_correct":false}]',
'Route-based VPNs allow routing protocols to run over tunnel interfaces.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/vpn/'],
'IPsec VPN', 15.0, true, 'jnce2_vpn_design_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jnce2_vpn_design_v2');

-- JNCIP-ENT Q9
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000011', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 4, 'troubleshoot', 'A Juniper router is not load balancing across two equal-cost BGP paths. What is a potential issue?',
'[{"id":"A","text":"BGP multipath not enabled or the paths differ in IGP metric to next-hop","is_correct":true},{"id":"B","text":"BGP is not a supported protocol for load balancing","is_correct":false},{"id":"C","text":"The router only has one forwarding engine","is_correct":false},{"id":"D","text":"The routes must be tagged with a community","is_correct":false}]',
'BGP multipath requires equal IGP distance to next-hops and explicit configuration.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/bgp/'],
'BGP Advanced', 12.0, true, 'jnce2_bgp_ecmp_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jnce2_bgp_ecmp_v2');

-- JNCIP-ENT Q10
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000011', 'a0000000-0000-0000-0000-000000000001', 'multiple-choice', 5, 'understand', 'Which statements about IS-IS overload-bit in Junos are correct? (Select TWO)',
'[{"id":"A","text":"Setting the overload-bit tells other routers not to use this router for transit traffic","is_correct":true},{"id":"B","text":"The overload-bit prevents the router from forming IS-IS adjacencies","is_correct":false},{"id":"C","text":"The overload-bit is automatically set when CPU utilization exceeds 90%","is_correct":false},{"id":"D","text":"The overload-bit can be configured to clear after a specified timeout","is_correct":true}]',
'Overload-bit prevents transit traffic and can auto-clear after timeout.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/is-is/'],
'IS-IS Advanced', 12.0, true, 'jnce2_isis_olbit_v2'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jnce2_isis_olbit_v2');

-- ============================================================
-- Part 6: Update all exam total_question counts
-- ============================================================

UPDATE exams SET total_questions = (SELECT COUNT(*)::int FROM questions WHERE exam_id = exams.id);
