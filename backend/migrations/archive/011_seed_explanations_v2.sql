-- Seed 10 explanations for existing _v2 questions
-- Uses DO block with jsonb_build_object to avoid JSON escaping issues

DO $$
DECLARE
    q_id uuid;
    q_hash text;
    section_data jsonb;
BEGIN

    -- Explanation 1: Static route preference (jncia_static_pref_v2)
    q_hash := 'jncia_static_pref_v2';
    SELECT id INTO q_id FROM questions WHERE content_hash = q_hash LIMIT 1;
    IF q_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM explanations WHERE question_id = q_id) THEN
        section_data := jsonb_build_array(
            jsonb_build_object('type', 'tldr', 'title', 'TL;DR', 'content', 'Static routes in Junos OS have a default preference of 18. This is higher than OSPF (pref 10) but lower than BGP (pref 170).'),
            jsonb_build_object('type', 'distractor_breakdown', 'title', 'Distractor Analysis', 'content', E'**A: 18** — Correct. Default preference for static routes in Junos OS.\n\n**B: 10** — Incorrect. This is the preference for OSPF (internal routes).\n\n**C: 170** — Incorrect. This is the preference for EBGP.\n\n**D: 5** — Incorrect. This is the preference for direct (connected) routes.'),
            jsonb_build_object('type', 'cli_example', 'title', 'CLI Verification', 'content', E'user@router> show route protocol static\n\ninet.0: 5 destinations, 5 routes (5 active, 0 holddown, 0 hidden)\n+ = Active Route, - = Last Active, * = Both\n\n0.0.0.0/0          *[Static/18] 00:02:34 > to 10.0.0.1 via ge-0/0/0.0')
        );
        INSERT INTO explanations (id, question_id, version, sections, summary, created_at)
        VALUES (gen_random_uuid(), q_id, 1, section_data, 'Static routes use preference 18 in Junos OS.', NOW());
    END IF;

    -- Explanation 2: show route command (jncia_show_route_v2)
    q_hash := 'jncia_show_route_v2';
    SELECT id INTO q_id FROM questions WHERE content_hash = q_hash LIMIT 1;
    IF q_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM explanations WHERE question_id = q_id) THEN
        section_data := jsonb_build_array(
            jsonb_build_object('type', 'tldr', 'title', 'TL;DR', 'content', 'The show route command displays the routing table in Junos OS.'),
            jsonb_build_object('type', 'distractor_breakdown', 'title', 'Distractor Analysis', 'content', E'**A: show route** — Correct. Main command for viewing the routing table.\n\n**B: show routing-table** — This command does not exist in Junos.\n\n**C: display ip route** — Cisco IOS command.\n\n**D: show ip route** — Cisco IOS command.')
        );
        INSERT INTO explanations (id, question_id, version, sections, summary, created_at)
        VALUES (gen_random_uuid(), q_id, 1, section_data, 'show route displays the routing table in Junos OS.', NOW());
    END IF;

    -- Explanation 3: commit command (jncia_commit_v2)
    q_hash := 'jncia_commit_v2';
    SELECT id INTO q_id FROM questions WHERE content_hash = q_hash LIMIT 1;
    IF q_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM explanations WHERE question_id = q_id) THEN
        section_data := jsonb_build_array(
            jsonb_build_object('type', 'tldr', 'title', 'TL;DR', 'content', 'The commit command activates the candidate configuration in Junos OS.'),
            jsonb_build_object('type', 'distractor_breakdown', 'title', 'Distractor Analysis', 'content', E'**A: Activates candidate config** — Correct.\n\n**B: Saves to file** — Use the save command.\n\n**C: Displays candidate** — Use show | compare.\n\n**D: Rollback** — Use rollback N.')
        );
        INSERT INTO explanations (id, question_id, version, sections, summary, created_at)
        VALUES (gen_random_uuid(), q_id, 1, section_data, 'Commit activates the candidate configuration.', NOW());
    END IF;

    -- Explanation 4: commit check (jncia_commit_check_v2)
    q_hash := 'jncia_commit_check_v2';
    SELECT id INTO q_id FROM questions WHERE content_hash = q_hash LIMIT 1;
    IF q_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM explanations WHERE question_id = q_id) THEN
        section_data := jsonb_build_array(
            jsonb_build_object('type', 'tldr', 'title', 'TL;DR', 'content', 'commit check validates syntax of the candidate configuration without activating it.'),
            jsonb_build_object('type', 'cli_example', 'title', 'Example', 'content', E'user@router# commit check\n\nerror: syntax in configuration\n[edit interfaces ge-0/0/0 unit 0 family inet]\n  address requires 10.0.0.1/24\n  ^')
        );
        INSERT INTO explanations (id, question_id, version, sections, summary, created_at)
        VALUES (gen_random_uuid(), q_id, 1, section_data, 'commit check validates config syntax.', NOW());
    END IF;

    -- Explanation 5: VLAN tagging (jncia_vlan_tag_v2)
    q_hash := 'jncia_vlan_tag_v2';
    SELECT id INTO q_id FROM questions WHERE content_hash = q_hash LIMIT 1;
    IF q_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM explanations WHERE question_id = q_id) THEN
        section_data := jsonb_build_array(
            jsonb_build_object('type', 'tldr', 'title', 'TL;DR', 'content', 'VLAN tagging in Junos uses logical units: set interfaces ge-0/0/1 unit 100 vlan-id 100.'),
            jsonb_build_object('type', 'distractor_breakdown', 'title', 'Distractor Analysis', 'content', E'**A: set interfaces ge-0/0/1 unit 100 vlan-id 100** — Correct. VLANs configured on logical units.\n\n**B: set interfaces ge-0/0/1 vlan-id 100** — Incorrect. vlan-id must be on unit level.\n\n**C: set vlans 100 interface ge-0/0/1** — VLAN-aware mode syntax.\n\n**D: switchport access vlan** — Cisco IOS command.')
        );
        INSERT INTO explanations (id, question_id, version, sections, summary, created_at)
        VALUES (gen_random_uuid(), q_id, 1, section_data, 'VLAN tagging uses logical units with vlan-id.', NOW());
    END IF;

    -- Explanation 6: OSPF interface (jncia_ospf_if_v2)
    q_hash := 'jncia_ospf_if_v2';
    SELECT id INTO q_id FROM questions WHERE content_hash = q_hash LIMIT 1;
    IF q_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM explanations WHERE question_id = q_id) THEN
        section_data := jsonb_build_array(
            jsonb_build_object('type', 'tldr', 'title', 'TL;DR', 'content', 'Junos OSPF: set protocols ospf area 0 interface ge-0/0/1.'),
            jsonb_build_object('type', 'distractor_breakdown', 'title', 'Distractor Analysis', 'content', E'**A: set protocols ospf area 0 interface ge-0/0/1** — Correct.\n\n**B: set protocols ospf interface ge-0/0/1 area 0** — Incorrect syntax.\n\n**C: router ospf 1; network area 0** — Cisco IOS syntax.\n\n**D: set routing-options ospf** — OSPF is under protocols, not routing-options.')
        );
        INSERT INTO explanations (id, question_id, version, sections, summary, created_at)
        VALUES (gen_random_uuid(), q_id, 1, section_data, 'OSPF uses set protocols ospf area syntax.', NOW());
    END IF;

    -- Explanation 7: BGP Local Preference (jncia_bgp_lp_v2)
    q_hash := 'jncia_bgp_lp_v2';
    SELECT id INTO q_id FROM questions WHERE content_hash = q_hash LIMIT 1;
    IF q_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM explanations WHERE question_id = q_id) THEN
        section_data := jsonb_build_array(
            jsonb_build_object('type', 'tldr', 'title', 'TL;DR', 'content', 'Default BGP Local Preference in Junos is 100, same as most vendors.'),
            jsonb_build_object('type', 'distractor_breakdown', 'title', 'Distractor Analysis', 'content', E'**A: 100** — Correct. Default LP in Junos and Cisco.\n\n**B: 0** — Incorrect. Minimum priority value.\n\n**C: 170** — This is EBGP route preference, not LP.\n\n**D: 65535** — Maximum value, not default.')
        );
        INSERT INTO explanations (id, question_id, version, sections, summary, created_at)
        VALUES (gen_random_uuid(), q_id, 1, section_data, 'Default BGP Local Preference is 100.', NOW());
    END IF;

    -- Explanation 8: Default static route (jncia_default_static_v2)
    q_hash := 'jncia_default_static_v2';
    SELECT id INTO q_id FROM questions WHERE content_hash = q_hash LIMIT 1;
    IF q_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM explanations WHERE question_id = q_id) THEN
        section_data := jsonb_build_array(
            jsonb_build_object('type', 'tldr', 'title', 'TL;DR', 'content', 'Default static route: set routing-options static route 0.0.0.0/0 next-hop 10.0.0.1.'),
            jsonb_build_object('type', 'cli_example', 'title', 'Configuration Example', 'content', E'set routing-options static route 0.0.0.0/0 next-hop 10.0.0.1\nset routing-options static route 0.0.0.0/0 qualified-next-hop 10.0.0.2 preference 25\n\n# Verification:\nuser@router> show configuration routing-options static'),
            jsonb_build_object('type', 'vendor_nuance', 'title', 'Vendor Note', 'content', 'Unlike Cisco (ip route 0.0.0.0 0.0.0.0), Junos uses hierarchical routing-options with preference 18 vs Cisco AD 1.')
        );
        INSERT INTO explanations (id, question_id, version, sections, summary, created_at)
        VALUES (gen_random_uuid(), q_id, 1, section_data, 'Default static route syntax in Junos.', NOW());
    END IF;

    -- Explanation 9: CCNA OSPF AD (ccna_ospf_ad_v2)
    q_hash := 'ccna_ospf_ad_v2';
    SELECT id INTO q_id FROM questions WHERE content_hash = q_hash LIMIT 1;
    IF q_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM explanations WHERE question_id = q_id) THEN
        section_data := jsonb_build_array(
            jsonb_build_object('type', 'tldr', 'title', 'TL;DR', 'content', 'OSPF has administrative distance 110 in Cisco IOS.'),
            jsonb_build_object('type', 'distractor_breakdown', 'title', 'Distractor Analysis', 'content', E'**A: 110** — Correct. AD for OSPF.\n\n**B: 120** — AD for RIP.\n\n**C: 90** — AD for EIGRP (internal).\n\n**D: 100** — No default AD of 100.'),
            jsonb_build_object('type', 'comparison', 'title', 'AD vs Preference', 'content', E'| Protocol | Cisco AD | Junos Pref |\n|----------|----------|------------|\n| Connected | 0 | 0 |\n| Static | 1 | 18 |\n| OSPF | 110 | 10 |\n| IS-IS | 115 | 18 |\n| EBGP | 20 | 170 |\n| IBGP | 200 | 170 |')
        );
        INSERT INTO explanations (id, question_id, version, sections, summary, created_at)
        VALUES (gen_random_uuid(), q_id, 1, section_data, 'OSPF AD is 110 in Cisco IOS.', NOW());
    END IF;

    -- Explanation 10: VXLAN purpose (dc_vxlan_v2)
    q_hash := 'dc_vxlan_v2';
    SELECT id INTO q_id FROM questions WHERE content_hash = q_hash LIMIT 1;
    IF q_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM explanations WHERE question_id = q_id) THEN
        section_data := jsonb_build_array(
            jsonb_build_object('type', 'tldr', 'title', 'TL;DR', 'content', 'VXLAN encapsulates L2 frames in UDP to extend Layer 2 segments across Layer 3 boundaries.'),
            jsonb_build_object('type', 'distractor_breakdown', 'title', 'Distractor Analysis', 'content', E'**A: Extend L2 over L3** — Correct. Primary purpose of VXLAN.\n\n**B: Encrypt traffic** — VXLAN does not provide encryption.\n\n**C: Replace STP** — Not VXLAN purpose.\n\n**D: Load balance** — Not primary purpose.'),
            jsonb_build_object('type', 'vendor_nuance', 'title', 'VXLAN vs EVPN', 'content', 'VXLAN is the encapsulation (MAC-in-UDP). EVPN is the control plane using MP-BGP. Juniper uses EVPN+VXLAN together for data center fabrics.')
        );
        INSERT INTO explanations (id, question_id, version, sections, summary, created_at)
        VALUES (gen_random_uuid(), q_id, 1, section_data, 'VXLAN extends L2 over L3 via MAC-in-UDP.', NOW());
    END IF;

    RAISE NOTICE 'Seeded 10 explanations successfully';
END $$;
