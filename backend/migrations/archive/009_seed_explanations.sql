-- Seed 10 deep-dive explanations for existing questions
-- Uses materialized DO block approach with jsonb_build_array

DO $$
DECLARE
    q_id uuid;
    q_hash text;
BEGIN
    -- Explanation 1: Static route preference
    SELECT id INTO q_id FROM questions WHERE content_hash = 'jncia_static_pref_final' LIMIT 1;
    IF q_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM explanations WHERE question_id = q_id) THEN
        INSERT INTO explanations (id, question_id, version, sections, summary, created_at)
        VALUES (gen_random_uuid(), q_id, 1,
            '[{"type":"tldr","title":"TL;DR","content":"Static routes in Junos OS have a default preference of 18. This is higher than OSPF (pref 10) but lower than BGP (pref 170)."},{"type":"distractor_breakdown","title":"Разбор вариантов ответа","content":"**A: 18** — Верно. Это значение по умолчанию для статических маршрутов в Junos OS.\n\n**B: 10** — Неверно. Это значение preference для OSPF (внутренние маршруты).\n\n**C: 170** — Неверно. Это значение preference для BGP (EBGP).\n\n**D: 5** — Неверно. Это значение preference для direct (подключенных) маршрутов."},{"type":"cli_example","title":"Проверка в CLI","content":"user@router> show route protocol static\n\ninet.0: 5 destinations, 5 routes (5 active, 0 holddown, 0 hidden)\n+ = Active Route, - = Last Active, * = Both\n\n0.0.0.0/0          *[Static/18] 00:02:34 > to 10.0.0.1 via ge-0/0/0.0"},{"type":"vendor_nuance","title":"Нюансы вендора","content":"В отличие от Cisco (где статический маршрут имеет AD 1), в Junos preference статического маршрута равен 18. Это значит, что OSPF-маршрут (pref 10) будет предпочтительнее статического по умолчанию."}]'::jsonb,
            'Static routes use preference 18 in Junos OS.',
            NOW());
    END IF;

    -- Explanation 2: show route command
    SELECT id INTO q_id FROM questions WHERE content_hash = 'jncia_show_route_final' LIMIT 1;
    IF q_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM explanations WHERE question_id = q_id) THEN
        INSERT INTO explanations (id, question_id, version, sections, summary, created_at)
        VALUES (gen_random_uuid(), q_id, 1,
            '[{"type":"tldr","title":"TL;DR","content":"The \"show route\" command displays the routing table in Junos OS."},{"type":"distractor_breakdown","title":"Разбор вариантов","content":"**A: show route** — Верно. Основная команда для просмотра таблицы маршрутизации.\n\n**B: show routing-table** — Такой команды не существует в Junos.\n\n**C: display ip route** — Команда Cisco IOS.\n\n**D: show ip route** — Команда Cisco IOS."}]'::jsonb,
            'show route displays the routing table in Junos OS.',
            NOW());
    END IF;

    -- Explanation 3: commit command
    SELECT id INTO q_id FROM questions WHERE content_hash = 'jncia_commit_final' LIMIT 1;
    IF q_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM explanations WHERE question_id = q_id) THEN
        INSERT INTO explanations (id, question_id, version, sections, summary, created_at)
        VALUES (gen_random_uuid(), q_id, 1,
            '[{"type":"tldr","title":"TL;DR","content":"The \"commit\" command activates the candidate configuration in Junos OS."},{"type":"distractor_breakdown","title":"Разбор вариантов","content":"**A: Activates the candidate configuration** — Верно. Commit делает активной текущую кандидатскую конфигурацию.\n\n**B: Saves to file** — Для сохранения в файл используется \"save\" или \"commit and-quit\".\n\n**C: Displays candidate** — Для просмотра используется \"show | compare\".\n\n**D: Rollback** — Для отката используется \"rollback 0\" или \"rollback N\"."}]'::jsonb,
            'Commit command activates the candidate configuration in Junos OS.',
            NOW());
    END IF;

    -- Explanation 4: commit check
    SELECT id INTO q_id FROM questions WHERE content_hash = 'jncia_commit_check_final' LIMIT 1;
    IF q_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM explanations WHERE question_id = q_id) THEN
        INSERT INTO explanations (id, question_id, version, sections, summary, created_at)
        VALUES (gen_random_uuid(), q_id, 1,
            '[{"type":"tldr","title":"TL;DR","content":"\"commit check\" validates the syntax of the candidate configuration without activating it."},{"type":"cli_example","title":"Пример","content":"user@router# commit check\n\nerror: syntax in configuration\n[edit interfaces ge-0/0/0 unit 0 family inet]\n  address requires 10.0.0.1/24\n  ^"}]'::jsonb,
            'commit check validates config syntax without activating.',
            NOW());
    END IF;

    -- Explanation 5: VLAN tagging
    SELECT id INTO q_id FROM questions WHERE content_hash = 'jncia_vlan_tag_final' LIMIT 1;
    IF q_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM explanations WHERE question_id = q_id) THEN
        INSERT INTO explanations (id, question_id, version, sections, summary, created_at)
        VALUES (gen_random_uuid(), q_id, 1,
            '[{"type":"tldr","title":"TL;DR","content":"VLAN tagging in Junos is configured by creating a logical unit with the desired VLAN ID."},{"type":"distractor_breakdown","title":"Разбор вариантов","content":"**A: set interfaces ge-0/0/1 unit 100 vlan-id 100** — Верно. В Junos вланы настраиваются на логическом юните.\n\n**B: set interfaces ge-0/0/1 vlan-id 100** — Неверно. vlan-id указывается на уровне unit, а не interface.\n\n**C: set vlans 100 interface ge-0/0/1** — Это для VLAN-aware режима, не для тегирования интерфейса.\n\n**D: switchport access vlan** — Это команда Cisco IOS."}]'::jsonb,
            'VLAN tagging in Junos uses logical units with vlan-id.',
            NOW());
    END IF;

    -- Explanation 6: OSPF interface config
    SELECT id INTO q_id FROM questions WHERE content_hash = 'jncia_ospf_if_final' LIMIT 1;
    IF q_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM explanations WHERE question_id = q_id) THEN
        INSERT INTO explanations (id, question_id, version, sections, summary, created_at)
        VALUES (gen_random_uuid(), q_id, 1,
            '[{"type":"tldr","title":"TL;DR","content":"Junos OSPF config uses hierarchy: set protocols ospf area 0 interface ge-0/0/1."},{"type":"distractor_breakdown","title":"Разбор вариантов","content":"**A: set protocols ospf area 0 interface ge-0/0/1** — Верно. Правильный синтаксис Junos.\n\n**B: set protocols ospf interface ge-0/0/1 area 0** — Неверно. В Junos сначала указывается area, потом interface.\n\n**C: router ospf 1; network area 0** — Синтаксис Cisco IOS.\n\n**D: set routing-options ospf** — OSPF настраивается в иерархии protocols, не routing-options."}]'::jsonb,
            'Junos OSPF uses set protocols ospf area <id> interface <if> syntax.',
            NOW());
    END IF;

    -- Explanation 7: BGP Local Preference
    SELECT id INTO q_id FROM questions WHERE content_hash = 'jncia_bgp_lp_final' LIMIT 1;
    IF q_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM explanations WHERE question_id = q_id) THEN
        INSERT INTO explanations (id, question_id, version, sections, summary, created_at)
        VALUES (gen_random_uuid(), q_id, 1,
            '[{"type":"tldr","title":"TL;DR","content":"Default BGP Local Preference in Junos is 100, same as most other vendors."},{"type":"distractor_breakdown","title":"Разбор вариантов","content":"**A: 100** — Верно. Default Local Preference в Junos и Cisco одинаков — 100.\n\n**B: 0** — Неверно. LP=0 будет означать минимальный приоритет.\n\n**C: 170** — Это preference EBGP маршрутов в таблице маршрутизации, не LP.\n\n**D: 65535** — Максимальное значение, но не дефолтное."}]'::jsonb,
            'Default BGP Local Preference is 100 in Junos OS.',
            NOW());
    END IF;

    -- Explanation 8: Default static route
    SELECT id INTO q_id FROM questions WHERE content_hash = 'jncia_default_static_final' LIMIT 1;
    IF q_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM explanations WHERE question_id = q_id) THEN
        INSERT INTO explanations (id, question_id, version, sections, summary, created_at)
        VALUES (gen_random_uuid(), q_id, 1,
            '[{"type":"tldr","title":"TL;DR","content":"The correct Junos command for a default static route is: set routing-options static route 0.0.0.0/0 next-hop 10.0.0.1."},{"type":"cli_example","title":"Пример конфигурации","content":"set routing-options static route 0.0.0.0/0 next-hop 10.0.0.1\nset routing-options static route 0.0.0.0/0 qualified-next-hop 10.0.0.2 preference 25\n\n# Просмотр настроенных статических маршрутов:\nuser@router> show configuration routing-options static"}]'::jsonb,
            'Default static route uses routing-options static route 0.0.0.0/0 next-hop syntax.',
            NOW());
    END IF;

    -- Explanation 9: CCNA OSPF AD
    SELECT id INTO q_id FROM questions WHERE content_hash = 'ccna_ospf_ad_final' LIMIT 1;
    IF q_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM explanations WHERE question_id = q_id) THEN
        INSERT INTO explanations (id, question_id, version, sections, summary, created_at)
        VALUES (gen_random_uuid(), q_id, 1,
            '[{"type":"tldr","title":"TL;DR","content":"OSPF has administrative distance 110 in Cisco IOS."},{"type":"distractor_breakdown","title":"Разбор вариантов","content":"**A: 110** — Верно. Administrative distance для OSPF.\n\n**B: 120** — AD для RIP.\n\n**C: 90** — AD для EIGRP (internal).\n\n**D: 100** — Нет протокола с AD 100 по умолчанию."},{"type":"comparison","title":"Таблица AD (Cisco vs Junos preference)","content":"| Протокол | Cisco AD | Junos Preference |\n|----------|----------|-----------------|\n| Connected | 0 | 0 |\n| Static | 1 | 18 |\n| OSPF | 110 | 10 |\n| IS-IS | 115 | 18 |\n| EIGRP | 90 | — |\n| BGP (EBGP) | 20 | 170 |\n| BGP (IBGP) | 200 | 170 |"}]'::jsonb,
            'OSPF administrative distance is 110 in Cisco IOS.',
            NOW());
    END IF;

    -- Explanation 10: VXLAN purpose
    SELECT id INTO q_id FROM questions WHERE content_hash = 'dc_vxlan_final' LIMIT 1;
    IF q_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM explanations WHERE question_id = q_id) THEN
        INSERT INTO explanations (id, question_id, version, sections, summary, created_at)
        VALUES (gen_random_uuid(), q_id, 1,
            '[{"type":"tldr","title":"TL;DR","content":"VXLAN encapsulates Layer 2 frames in UDP packets to extend Layer 2 segments across Layer 3 network boundaries."},{"type":"diagram_svg","title":"Архитектура VXLAN","content":"<svg viewBox=\"0 0 600 300\" xmlns=\"http://www.w3.org/2000/svg\"><rect x=\"10\" y=\"10\" width=\"130\" height=\"80\" rx=\"8\" fill=\"#1e293b\" stroke=\"#38bdf8\" stroke-width=\"2\"/><text x=\"75\" y=\"50\" text-anchor=\"middle\" fill=\"#38bdf8\" font-size=\"12\">VM/Host A</text><text x=\"75\" y=\"70\" text-anchor=\"middle\" fill=\"#94a3b8\" font-size=\"10\">VTEP: 10.1.1.1</text><rect x=\"460\" y=\"10\" width=\"130\" height=\"80\" rx=\"8\" fill=\"#1e293b\" stroke=\"#38bdf8\" stroke-width=\"2\"/><text x=\"525\" y=\"50\" text-anchor=\"middle\" fill=\"#38bdf8\" font-size=\"12\">VM/Host B</text><text x=\"525\" y=\"70\" text-anchor=\"middle\" fill=\"#94a3b8\" font-size=\"10\">VTEP: 10.2.2.2</text><rect x=\"100\" y=\"130\" width=\"400\" height=\"60\" rx=\"8\" fill=\"#0f172a\" stroke=\"#475569\" stroke-width=\"1\" stroke-dasharray=\"4\"/><text x=\"300\" y=\"165\" text-anchor=\"middle\" fill=\"#475569\" font-size=\"12\">Underlay IP Network (L3)</text><line x1=\"140\" y1=\"90\" x2=\"200\" y2=\"130\" stroke=\"#38bdf8\" stroke-width=\"2\" stroke-dasharray=\"4\"/><text x=\"170\" y=\"108\" text-anchor=\"middle\" fill=\"#38bdf8\" font-size=\"10\">VXLAN Tunnel</text><line x1=\"460\" y1=\"90\" x2=\"400\" y2=\"130\" stroke=\"#38bdf8\" stroke-width=\"2\" stroke-dasharray=\"4\"/><text x=\"430\" y=\"108\" text-anchor=\"middle\" fill=\"#38bdf8\" font-size=\"10\">VXLAN Tunnel</text></svg>"},{"type":"vendor_nuance","title":"VXLAN vs EVPN","content":"VXLAN — это технология инкапсуляции (MAC-in-UDP). EVPN — это control plane для VXLAN, использующий MP-BGP для распределения MAC/VNI информации. Juniper использует EVPN+VXLAN вместе для фабрик ЦОД."}]'::jsonb,
            'VXLAN extends L2 segments over L3 networks using MAC-in-UDP encapsulation.',
            NOW());
    END IF;

    RAISE NOTICE 'Seeded 10 explanations successfully';
END $$;
