-- Migration 008: Seed additional questions (final fixed version)
-- Uses ARRAY[...] for text[] reference_urls column

-- ============================================================
-- Part 1: JNCIA-Junos (+25 questions)
-- ============================================================

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand', 'What is the default preference value for static routes in Junos OS?', '[{"id":"A","text":"18"},{"id":"B","text":"10"},{"id":"C","text":"170"},{"id":"D","text":"5"}]', 'Static routes have a default preference of 18 in Junos OS.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/routing-policy/topics/topic-map/route-configuration.html'], 'Routing Fundamentals', 12.0, true, 'jncia_static_pref_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_static_pref_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand', 'In Junos OS, which command is used to view the routing table?', '[{"id":"A","text":"show route"},{"id":"B","text":"show routing-table"},{"id":"C","text":"display ip route"},{"id":"D","text":"show ip route"}]', 'The "show route" operational mode command displays the routing table in Junos OS.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli-reference/'], 'Routing Fundamentals', 10.0, true, 'jncia_show_route_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_show_route_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'apply', 'What is the correct Junos command to configure a default static route via 10.0.0.1?', '[{"id":"A","text":"set routing-options static route 0.0.0.0/0 next-hop 10.0.0.1"},{"id":"B","text":"set protocols static route 0.0.0.0/0 next-hop 10.0.0.1"},{"id":"C","text":"set routing-options static default-route next-hop 10.0.0.1"},{"id":"D","text":"ip route 0.0.0.0 0.0.0.0 10.0.0.1"}]', 'The correct Junos syntax for a default static route is "set routing-options static route 0.0.0.0/0 next-hop 10.0.0.1".', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/routing-policy/'], 'Routing Fundamentals', 12.0, true, 'jncia_default_static_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_default_static_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 1, 'remember', 'What is the Junos CLI prompt symbol for operational mode?', '[{"id":"A","text":">"},{"id":"B","text":"#"},{"id":"C","text":"$"},{"id":"D","text":"%"}]', 'The ">" symbol indicates operational mode in Junos CLI.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli-reference/'], 'Junos OS Fundamentals', 8.0, true, 'jncia_op_prompt_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_op_prompt_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 1, 'remember', 'Which command enters configuration mode in Junos OS?', '[{"id":"A","text":"configure"},{"id":"B","text":"config"},{"id":"C","text":"configure terminal"},{"id":"D","text":"config mode"}]', 'The "configure" command enters configuration mode in Junos OS.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli-reference/'], 'Junos OS Fundamentals', 8.0, true, 'jncia_config_mode_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_config_mode_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand', 'What is the function of the "commit" command in Junos OS?', '[{"id":"A","text":"Activates the candidate configuration"},{"id":"B","text":"Saves the configuration to a file"},{"id":"C","text":"Displays the candidate configuration"},{"id":"D","text":"Rolls back to the previous configuration"}]', 'The "commit" command activates the candidate configuration.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli-reference/'], 'Junos OS Fundamentals', 12.0, true, 'jncia_commit_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_commit_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'analyze', 'After running "commit check" you get "error: syntax in configuration". What does this mean?', '[{"id":"A","text":"A syntax error was found in the candidate configuration"},{"id":"B","text":"The configuration was committed successfully"},{"id":"C","text":"Syntactic changes are valid but semantic checks are needed"},{"id":"D","text":"Only the checked portion was committed"}]', '"commit check" validates syntax of the candidate configuration without activating it.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli-reference/'], 'Junos OS Fundamentals', 8.0, true, 'jncia_commit_check_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_commit_check_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'apply', 'Which command creates a tagged VLAN 100 on interface ge-0/0/1 in Junos?', '[{"id":"A","text":"set interfaces ge-0/0/1 unit 100 vlan-id 100"},{"id":"B","text":"set interfaces ge-0/0/1 vlan-id 100"},{"id":"C","text":"set vlans 100 interface ge-0/0/1"},{"id":"D","text":"set interface ge-0/0/1 switchport access vlan 100"}]', 'In Junos, VLAN tagging is configured by creating a logical unit with the desired VLAN ID.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/ethernet-switching/'], 'Layer 2 Technologies', 12.0, true, 'jncia_vlan_tag_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_vlan_tag_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand', 'What happens in Junos when you deactivate an interface?', '[{"id":"A","text":"Config remains but is not applied; can be reactivated"},{"id":"B","text":"The interface is disabled at the physical level"},{"id":"C","text":"The config is removed from the candidate config"},{"id":"D","text":"The interface is permanently deleted"}]', 'The "deactivate" command temporarily disables a config statement until "activate" is used.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli-reference/'], 'Junos OS Fundamentals', 8.0, true, 'jncia_deactivate_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_deactivate_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'apply', 'How do you configure OSPF on interface ge-0/0/1 with area 0 in Junos?', '[{"id":"A","text":"set protocols ospf area 0 interface ge-0/0/1"},{"id":"B","text":"set protocols ospf interface ge-0/0/1 area 0"},{"id":"C","text":"router ospf 1; network 0.0.0.0 area 0"},{"id":"D","text":"set routing-options ospf area 0 interface ge-0/0/1"}]', 'Junos OSPF syntax is "set protocols ospf area 0 interface ge-0/0/1".', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/ospf/'], 'OSPF', 15.0, true, 'jncia_ospf_if_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_ospf_if_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand', 'What does the "passive" option do on an OSPF interface in Junos?', '[{"id":"A","text":"No hellos sent but subnet is advertised"},{"id":"B","text":"Sends hellos but does not accept adjacencies"},{"id":"C","text":"OSPF is completely disabled on the interface"},{"id":"D","text":"Only accepts passive adjacencies"}]', 'A passive OSPF interface does not send/receive hellos, but the subnet is advertised in LSAs.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/ospf/'], 'OSPF', 10.0, true, 'jncia_ospf_passive_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_ospf_passive_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'apply', 'Which firewall filter action counts packets in Junos without permitting or denying?', '[{"id":"A","text":"then count"},{"id":"B","text":"then accept"},{"id":"C","text":"then log"},{"id":"D","text":"then sample"}]', 'The "then count" action increments a packet counter without permitting or denying.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/security-policy/'], 'Security Fundamentals', 10.0, true, 'jncia_fw_count_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_fw_count_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand', 'What is the default zone for interfaces in Junos SRX?', '[{"id":"A","text":"No zone — must be assigned explicitly"},{"id":"B","text":"trust"},{"id":"C","text":"untrust"},{"id":"D","text":"management"}]', 'SRX interfaces must be explicitly assigned to a security zone.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/srx-series/'], 'Security Fundamentals', 8.0, true, 'jncia_zone_default_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_zone_default_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'apply', 'Which BGP attribute is used for outbound traffic engineering in Junos?', '[{"id":"A","text":"Local Preference"},{"id":"B","text":"MED"},{"id":"C","text":"AS Path"},{"id":"D","text":"Next Hop"}]', 'Local Preference influences outbound traffic. Higher value is preferred.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/bgp/'], 'BGP', 12.0, true, 'jncia_bgp_med_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_bgp_med_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand', 'What is the default BGP Local Preference in Junos?', '[{"id":"A","text":"100"},{"id":"B","text":"0"},{"id":"C","text":"170"},{"id":"D","text":"65535"}]', 'Default BGP Local Preference in Junos is 100.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/bgp/'], 'BGP', 10.0, true, 'jncia_bgp_lp_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_bgp_lp_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand', 'Which Junos command shows real-time interface traffic statistics?', '[{"id":"A","text":"monitor interface traffic"},{"id":"B","text":"show interface statistics"},{"id":"C","text":"show interfaces detail"},{"id":"D","text":"show interfaces extensive"}]', '"monitor interface traffic" provides a real-time view of interface traffic.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/interfaces-ipsec/'], 'Junos OS Fundamentals', 8.0, true, 'jncia_monitor_if_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_monitor_if_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 1, 'remember', 'Which command displays Juniper device model and serial number?', '[{"id":"A","text":"show chassis hardware"},{"id":"B","text":"show version"},{"id":"C","text":"show system info"},{"id":"D","text":"show hardware detail"}]', '"show chassis hardware" displays model and serial number.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli-reference/'], 'Junos OS Fundamentals', 6.0, true, 'jncia_chassis_hw_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_chassis_hw_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand', 'What is "rescue configuration" in Junos?', '[{"id":"A","text":"A known-good config loaded in emergencies"},{"id":"B","text":"The factory default configuration"},{"id":"C","text":"An automatic backup saved every hour"},{"id":"D","text":"A config pushed from a management server"}]', 'Rescue configuration can be loaded with "rollback rescue".', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli-reference/'], 'Junos OS Fundamentals', 8.0, true, 'jncia_rescue_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_rescue_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'apply', 'What is the correct Junos syntax to configure EBGP to neighbor 10.0.0.2 AS 65001?', '[{"id":"A","text":"set protocols bgp group EBGP peer-as 65001 neighbor 10.0.0.2"},{"id":"B","text":"set protocols bgp neighbor 10.0.0.2 remote-as 65001"},{"id":"C","text":"router bgp 65001; neighbor 10.0.0.2 remote-as 65002"},{"id":"D","text":"set routing-options bgp peer 10.0.0.2 as 65001"}]', 'Junos BGP uses protocol groups.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/bgp/'], 'BGP', 12.0, true, 'jncia_bgp_config_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_bgp_config_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'troubleshoot', 'A Junos device cannot ping a directly connected neighbor. Interface is up/up. Most likely cause?', '[{"id":"A","text":"Missing or incorrect IP address on the interface unit"},{"id":"B","text":"BGP not configured"},{"id":"C","text":"Firewall filter blocking OSPF"},{"id":"D","text":"The routing table is full"}]', 'Missing or incorrect IP address is the most likely cause.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/interfaces-ipsec/'], 'Troubleshooting', 10.0, true, 'jncia_ping_fail_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_ping_fail_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'apply', 'What is "apply-groups" in Junos used for?', '[{"id":"A","text":"Apply reusable config groups to hierarchy levels"},{"id":"B","text":"Apply an access list to an interface"},{"id":"C","text":"Apply a routing policy to BGP"},{"id":"D","text":"Apply class of service configuration"}]', '"apply-groups" allows reusable configuration groups.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli-reference/'], 'Junos OS Fundamentals', 8.0, true, 'jncia_apply_groups_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_apply_groups_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'troubleshoot', 'After configuring BGP, the session shows "Active". What does this mean?', '[{"id":"A","text":"Trying to establish the TCP connection to the peer"},{"id":"B","text":"The BGP session is up and passing routes"},{"id":"C","text":"The BGP configuration has been deactivated"},{"id":"D","text":"BGP routes are being processed"}]', 'The "Active" state means the router is attempting a TCP connection to the BGP peer.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/bgp/'], 'BGP', 10.0, true, 'jncia_bgp_active_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_bgp_active_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 4, 'troubleshoot', 'A router has OSPF route (pref 10) and IS-IS route (pref 18) to 10.0.0.0/24. Which wins?', '[{"id":"A","text":"The OSPF route (lower preference)"},{"id":"B","text":"The IS-IS route (higher metric)"},{"id":"C","text":"Both routes (ECMP)"},{"id":"D","text":"Neither (conflicting routes cancel)"}]', 'The route with the lowest preference value wins. OSPF (10) beats IS-IS (18).', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/routing-policy/'], 'Routing Fundamentals', 12.0, true, 'jncia_pref_compare_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_pref_compare_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'multiple-choice', 3, 'understand', 'Which are valid Junos configuration modes? (Select TWO)', '[{"id":"A","text":"configure exclusive"},{"id":"B","text":"configure private"},{"id":"C","text":"configure dynamic"},{"id":"D","text":"configure shared"}]', '"configure exclusive" locks the config database; "configure private" provides isolated candidate config.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli-reference/'], 'Junos OS Fundamentals', 8.0, true, 'jncia_config_modes_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'jncia_config_modes_final');

-- ============================================================
-- Part 2: CCNA (+15 questions)
-- ============================================================

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 1, 'remember', 'What is the default administrative distance for OSPF in Cisco IOS?', '[{"id":"A","text":"110"},{"id":"B","text":"120"},{"id":"C","text":"90"},{"id":"D","text":"100"}]', 'OSPF has AD 110 in Cisco IOS.', ARRAY['https://learningnetwork.cisco.com/'], 'Routing Fundamentals', 8.0, true, 'ccna_ospf_ad_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_ospf_ad_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 1, 'remember', 'Which Cisco IOS command displays the running configuration?', '[{"id":"A","text":"show running-config"},{"id":"B","text":"display running-config"},{"id":"C","text":"show configuration"},{"id":"D","text":"display configuration"}]', '"show running-config" displays the active config.', ARRAY['https://learningnetwork.cisco.com/'], 'Network Fundamentals', 6.0, true, 'ccna_show_run_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_show_run_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 1, 'understand', 'What is the default VLAN on all Cisco switch ports?', '[{"id":"A","text":"VLAN 1"},{"id":"B","text":"VLAN 0"},{"id":"C","text":"VLAN 100"},{"id":"D","text":"VLAN 1002"}]', 'VLAN 1 is the default VLAN on all Cisco switch ports.', ARRAY['https://learningnetwork.cisco.com/'], 'Network Access', 8.0, true, 'ccna_default_vlan_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_default_vlan_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'apply', 'What command configures an interface as a trunk in Cisco IOS?', '[{"id":"A","text":"switchport mode trunk"},{"id":"B","text":"port mode trunk"},{"id":"C","text":"trunk mode on"},{"id":"D","text":"set interface trunk"}]', '"switchport mode trunk" is the Cisco trunk command.', ARRAY['https://learningnetwork.cisco.com/'], 'Network Access', 10.0, true, 'ccna_trunk_cmd_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_trunk_cmd_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'understand', 'What is the purpose of Spanning Tree Protocol?', '[{"id":"A","text":"Prevent Layer 2 loops in redundant switched networks"},{"id":"B","text":"Provide load balancing across multiple links"},{"id":"C","text":"Enable VLAN trunking"},{"id":"D","text":"Provide Layer 3 redundancy"}]', 'STP prevents Layer 2 loops by blocking redundant links.', ARRAY['https://learningnetwork.cisco.com/'], 'Network Access', 8.0, true, 'ccna_stp_purpose_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_stp_purpose_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'apply', 'Which routing protocol is considered link-state?', '[{"id":"A","text":"OSPF"},{"id":"B","text":"RIP"},{"id":"C","text":"EIGRP"},{"id":"D","text":"BGP"}]', 'OSPF is a link-state routing protocol using the SPF algorithm.', ARRAY['https://learningnetwork.cisco.com/'], 'IP Connectivity', 8.0, true, 'ccna_linkstate_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_linkstate_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'understand', 'What are the private IP ranges per RFC 1918?', '[{"id":"A","text":"10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16"},{"id":"B","text":"10.0.0.0/8, 172.0.0.0/8, 192.168.0.0/16"},{"id":"C","text":"10.0.0.0/16, 172.16.0.0/16, 192.168.0.0/24"},{"id":"D","text":"100.64.0.0/10, 172.16.0.0/12, 192.168.0.0/16"}]', 'RFC 1918: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16.', ARRAY['https://learningnetwork.cisco.com/'], 'Network Fundamentals', 8.0, true, 'ccna_rfc1918_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_rfc1918_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'apply', 'What is the purpose of NAT overload (PAT)?', '[{"id":"A","text":"Map multiple private IPs to a single public IP using ports"},{"id":"B","text":"Translate IPv6 to IPv4"},{"id":"C","text":"Static one-to-one mapping"},{"id":"D","text":"Translate MAC addresses to IPs"}]', 'PAT maps multiple private IPs to a single public IP differentiated by port numbers.', ARRAY['https://learningnetwork.cisco.com/'], 'IP Services', 10.0, true, 'ccna_pat_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_pat_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'apply', 'How many host addresses are available in a /26 subnet?', '[{"id":"A","text":"62"},{"id":"B","text":"64"},{"id":"C","text":"126"},{"id":"D","text":"30"}]', 'A /26 has 6 host bits: 2^6 - 2 = 62 usable addresses.', ARRAY['https://learningnetwork.cisco.com/'], 'Network Fundamentals', 10.0, true, 'ccna_subnet_26_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_subnet_26_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 1, 'remember', 'Default DHCP lease time on a Cisco router?', '[{"id":"A","text":"24 hours (86400 seconds)"},{"id":"B","text":"7 days"},{"id":"C","text":"1 hour"},{"id":"D","text":"30 minutes"}]', 'Default DHCP lease on Cisco IOS is 24 hours.', ARRAY['https://learningnetwork.cisco.com/'], 'IP Services', 6.0, true, 'ccna_dhcp_lease_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_dhcp_lease_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 3, 'troubleshoot', 'PC (192.168.1.10/24, gw 192.168.1.1) cannot reach internet. Gateway can ping 8.8.8.8, PC cannot. Most likely?', '[{"id":"A","text":"NAT not configured on the gateway"},{"id":"B","text":"DNS not configured on the PC"},{"id":"C","text":"Wrong subnet mask on PC"},{"id":"D","text":"No route from gateway to PC subnet"}]', 'Since the gateway reaches 8.8.8.8, NAT/PAT is likely not configured.', ARRAY['https://learningnetwork.cisco.com/'], 'IP Services', 12.0, true, 'ccna_nat_issue_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_nat_issue_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'apply', 'What is the IOS interface subcommand to enable OSPF?', '[{"id":"A","text":"ip ospf 1 area 0"},{"id":"B","text":"router ospf 1"},{"id":"C","text":"ip routing ospf area 0"},{"id":"D","text":"enable ospf interface"}]', '"ip ospf 1 area 0" enables OSPF on an interface.', ARRAY['https://learningnetwork.cisco.com/'], 'IP Connectivity', 10.0, true, 'ccna_ospf_if_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_ospf_if_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 1, 'remember', 'What does SVI stand for?', '[{"id":"A","text":"Switch Virtual Interface"},{"id":"B","text":"System VLAN Interface"},{"id":"C","text":"Standard Virtual Interface"},{"id":"D","text":"Serial VLAN Interface"}]', 'SVI = Switch Virtual Interface for Layer 3 VLAN connectivity.', ARRAY['https://learningnetwork.cisco.com/'], 'Network Access', 6.0, true, 'ccna_svi_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_svi_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'understand', 'What does an inbound ACL do?', '[{"id":"A","text":"Filters traffic before it enters the router interface"},{"id":"B","text":"Filters traffic after routing out the exit interface"},{"id":"C","text":"Affects only locally-originated traffic"},{"id":"D","text":"Filters routing updates only"}]', 'An inbound ACL filters traffic arriving on the interface before the routing decision.', ARRAY['https://learningnetwork.cisco.com/'], 'Security Fundamentals', 10.0, true, 'ccna_acl_inbound_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'ccna_acl_inbound_final');

-- ============================================================
-- Part 3: SP (+3), SEC (+3), DC (+3), AUT (+3)
-- ============================================================

-- JNCIA-SP
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'single-choice', 2, 'understand', 'What is the purpose of BGP route reflectors?', '[{"id":"A","text":"Reduce the number of IBGP peerings required"},{"id":"B","text":"Reflect BGP updates between different ASes"},{"id":"C","text":"Filter BGP routes based on community"},{"id":"D","text":"Load balance BGP traffic"}]', 'Route reflectors reduce the IBGP full mesh requirement.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/bgp/'], 'BGP', 12.0, true, 'sp_rr_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'sp_rr_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'single-choice', 3, 'apply', 'In MPLS, what label operation does a P router perform?', '[{"id":"A","text":"Swaps the incoming label for an outgoing label"},{"id":"B","text":"Adds (pushes) a label"},{"id":"C","text":"Removes (pops) the top label"},{"id":"D","text":"Removes all labels"}]', 'A P router performs label swapping.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/mpls/'], 'MPLS', 12.0, true, 'sp_mpls_swap_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'sp_mpls_swap_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'single-choice', 2, 'understand', 'What does LDP do in an MPLS network?', '[{"id":"A","text":"Distributes label bindings to LDP peers"},{"id":"B","text":"Forwards MPLS packets"},{"id":"C","text":"Signals RSVP-TE tunnels"},{"id":"D","text":"Distributes routing information"}]', 'LDP distributes label bindings to MPLS LDP peers.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/mpls/'], 'MPLS', 10.0, true, 'sp_ldp_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'sp_ldp_final');

-- JNCIA-SEC
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000022', 'a0000000-0000-0000-0000-000000000003', 'single-choice', 2, 'understand', 'In Junos SRX, what is the default action for traffic not matching any policy?', '[{"id":"A","text":"Denied (implicit deny)"},{"id":"B","text":"Permitted"},{"id":"C","text":"Logged and permitted"},{"id":"D","text":"Redirected to management interface"}]', 'Junos SRX has an implicit deny at the end of every security policy.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/srx-series/'], 'Security Policies', 10.0, true, 'sec_implicit_deny_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'sec_implicit_deny_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000022', 'a0000000-0000-0000-0000-000000000003', 'single-choice', 3, 'apply', 'How does SRX handle return traffic for established sessions?', '[{"id":"A","text":"Stateful firewall with session-based forwarding"},{"id":"B","text":"ALG"},{"id":"C","text":"Reverse path forwarding"},{"id":"D","text":"Zone-based forwarding"}]', 'SRX uses stateful firewall with session entries for return traffic.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/srx-series/'], 'Security Policies', 12.0, true, 'sec_stateful_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'sec_stateful_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000022', 'a0000000-0000-0000-0000-000000000003', 'single-choice', 2, 'understand', 'Which policy type allows traffic from trust to untrust in SRX?', '[{"id":"A","text":"From-zone trust to-zone untrust"},{"id":"B","text":"From-zone untrust to-zone trust"},{"id":"C","text":"Global security policy"},{"id":"D","text":"Interface security policy"}]', 'Junos SRX uses from-zone/to-zone security policies.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/srx-series/'], 'Security Policies', 10.0, true, 'sec_from_to_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'sec_from_to_final');

-- JNCIA-DC
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000021', 'a0000000-0000-0000-0000-000000000004', 'single-choice', 2, 'understand', 'What is the purpose of VXLAN in data center networks?', '[{"id":"A","text":"Extend Layer 2 segments across Layer 3 boundaries"},{"id":"B","text":"Encrypt data center traffic"},{"id":"C","text":"Replace Spanning Tree Protocol"},{"id":"D","text":"Load balance traffic across DCs"}]', 'VXLAN encapsulates L2 frames in UDP to extend L2 across L3 boundaries.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/evpn-vxlan/'], 'EVPN-VXLAN', 12.0, true, 'dc_vxlan_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'dc_vxlan_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000021', 'a0000000-0000-0000-0000-000000000004', 'single-choice', 3, 'apply', 'What is the VXLAN UDP destination port?', '[{"id":"A","text":"4789"},{"id":"B","text":"8472"},{"id":"C","text":"6633"},{"id":"D","text":"179"}]', 'The IANA-assigned VXLAN UDP destination port is 4789.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/evpn-vxlan/'], 'EVPN-VXLAN', 8.0, true, 'dc_vxlan_port_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'dc_vxlan_port_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000021', 'a0000000-0000-0000-0000-000000000004', 'single-choice', 2, 'understand', 'What is the role of a leaf switch in spine-leaf?', '[{"id":"A","text":"Connects to all spines and provides server access"},{"id":"B","text":"Connects only to other leaf switches"},{"id":"C","text":"Aggregates traffic from all spines"},{"id":"D","text":"Provides inter-DC connectivity"}]', 'Leaf switches connect to all spine switches and provide server connectivity.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/data-center/'], 'Data Center Architecture', 12.0, true, 'dc_leaf_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'dc_leaf_final');

-- JNCIA-DevOps
INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000020', 'a0000000-0000-0000-0000-000000000005', 'single-choice', 2, 'understand', 'What is Junos PyEZ?', '[{"id":"A","text":"Python library for Junos automation via NETCONF"},{"id":"B","text":"Python OS for Junos"},{"id":"C","text":"Visual topology builder"},{"id":"D","text":"CLI replacement for Junos"}]', 'Junos PyEZ is a Python library for Junos automation via NETCONF.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/pyez/'], 'Automation Fundamentals', 10.0, true, 'aut_pyez_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'aut_pyez_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000020', 'a0000000-0000-0000-0000-000000000005', 'single-choice', 2, 'understand', 'What protocol does Ansible use by default for Junos?', '[{"id":"A","text":"NETCONF (SSH)"},{"id":"B","text":"SNMP"},{"id":"C","text":"REST API"},{"id":"D","text":"Telnet"}]', 'Ansible uses NETCONF over SSH for Junos management.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/automation/'], 'Automation Fundamentals', 10.0, true, 'aut_ansible_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'aut_ansible_final');

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, content_hash)
SELECT gen_random_uuid(), 'b0000000-0000-0000-0000-000000000020', 'a0000000-0000-0000-0000-000000000005', 'single-choice', 2, 'understand', 'What is the primary benefit of Infrastructure as Code?', '[{"id":"A","text":"Consistent, repeatable, version-controlled deployments"},{"id":"B","text":"Automatic bandwidth optimization"},{"id":"C","text":"Real-time traffic monitoring"},{"id":"D","text":"Hardware replacement detection"}]', 'IaC treats config as version-controlled code for consistent deployments.', ARRAY['https://www.juniper.net/documentation/us/en/software/junos/automation/'], 'Automation Fundamentals', 10.0, true, 'aut_iac_final'
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE content_hash = 'aut_iac_final');

-- ============================================================
-- Part 4: Update exam total_question counts
-- ============================================================

UPDATE exams SET total_questions = (SELECT COUNT(*)::int FROM questions WHERE exam_id = 'b0000000-0000-0000-0000-000000000001') WHERE id = 'b0000000-0000-0000-0000-000000000001';
UPDATE exams SET total_questions = (SELECT COUNT(*)::int FROM questions WHERE exam_id = 'b0000000-0000-0000-0000-000000000003') WHERE id = 'b0000000-0000-0000-0000-000000000003';
UPDATE exams SET total_questions = (SELECT COUNT(*)::int FROM questions WHERE exam_id = 'b0000000-0000-0000-0000-000000000002') WHERE id = 'b0000000-0000-0000-0000-000000000002';
UPDATE exams SET total_questions = (SELECT COUNT(*)::int FROM questions WHERE exam_id = 'b0000000-0000-0000-0000-000000000022') WHERE id = 'b0000000-0000-0000-0000-000000000022';
UPDATE exams SET total_questions = (SELECT COUNT(*)::int FROM questions WHERE exam_id = 'b0000000-0000-0000-0000-000000000021') WHERE id = 'b0000000-0000-0000-0000-000000000021';
UPDATE exams SET total_questions = (SELECT COUNT(*)::int FROM questions WHERE exam_id = 'b0000000-0000-0000-0000-000000000020') WHERE id = 'b0000000-0000-0000-0000-000000000020';
