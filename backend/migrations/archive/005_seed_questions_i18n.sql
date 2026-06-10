-- +goose Up
-- +goose StatementBegin

-- ═══════════════════════════════════════
-- Russian translations for existing questions
-- JNCIA-Junos (JN0-101)
-- ═══════════════════════════════════════

-- Fix: replace literal \n with actual newlines in exhibit question bodies
UPDATE questions SET body = REPLACE(body, E'\\n', E'\n') WHERE body LIKE E'%\\n%';

UPDATE questions SET
    body_translations = '{"ru": "Какое утверждение верно описывает архитектуру Junos OS?"}'::jsonb,
    options_translations = '{"ru": [{"id":"a","text":"Junos OS использует монолитное ядро со всеми процессами в пространстве ядра"},{"id":"b","text":"Junos OS имеет модульную архитектуру с отдельными пользовательскими процессами для каждого протокола"},{"id":"c","text":"Junos OS базируется на ядре Linux и запускает протоколы маршрутизации как модули ядра"},{"id":"d","text":"Junos OS использует операционную систему реального времени без пользовательских процессов"}]}'::jsonb
WHERE id = 'c0000000-0000-0000-0000-000000000001';

UPDATE questions SET
    body_translations = '{"ru": "В Junos OS какой режим CLI позволяет просматривать текущую конфигурацию?"}'::jsonb,
    options_translations = '{"ru": [{"id":"a","text":"Режим конфигурации (configure exclusive)"},{"id":"b","text":"Операционный режим"},{"id":"c","text":"Режим мониторинга"},{"id":"d","text":"Режим Enable"}]}'::jsonb
WHERE id = 'c0000000-0000-0000-0000-000000000002';

UPDATE questions SET
    body_translations = '{"ru": "Какая команда отображает OSPF-соседей на устройстве Junos?"}'::jsonb,
    options_translations = '{"ru": [{"id":"a","text":"show ospf neighbor"},{"id":"b","text":"show ospf database"},{"id":"c","text":"show ospf interface"},{"id":"d","text":"show ospf adjacency"}]}'::jsonb
WHERE id = 'c0000000-0000-0000-0000-000000000003';

UPDATE questions SET
    body_translations = '{"ru": "Какой атрибут BGP используется для предотвращения петель?"}'::jsonb,
    options_translations = '{"ru": [{"id":"a","text":"MED (Multi-Exit Discriminator)"},{"id":"b","text":"Local Preference"},{"id":"c","text":"AS_PATH"},{"id":"d","text":"Community"}]}'::jsonb
WHERE id = 'c0000000-0000-0000-0000-000000000004';

UPDATE questions SET
    body_translations = '{"ru": "В Junos какая политика импорта по умолчанию для EBGP-сессий?"}'::jsonb,
    options_translations = '{"ru": [{"id":"a","text":"Принимать все BGP-маршруты"},{"id":"b","text":"Отклонять все BGP-маршруты"},{"id":"c","text":"Принимать все активные BGP-маршруты"},{"id":"d","text":"Принимать только маршруты по умолчанию"}]}'::jsonb
WHERE id = 'c0000000-0000-0000-0000-000000000005';

UPDATE questions SET
    body_translations = '{"ru": "Какие из перечисленных являются допустимыми действиями firewall filter в Junos? (Выберите ДВА)"}'::jsonb,
    options_translations = '{"ru": [{"id":"a","text":"accept"},{"id":"b","text":"discard"},{"id":"c","text":"permit"},{"id":"d","text":"forward"}]}'::jsonb
WHERE id = 'c0000000-0000-0000-0000-000000000006';

UPDATE questions SET
    body_translations = '{"ru": "Какое утверждение о commit model в Junos верно?"}'::jsonb,
    options_translations = '{"ru": [{"id":"a","text":"Изменения вступают в силу сразу при наборе команды"},{"id":"b","text":"Изменения накапливаются и применяются атомарно командой commit"},{"id":"c","text":"Изменения автоматически сохраняются каждые 5 минут"},{"id":"d","text":"Изменения требуют перезагрузки системы"}]}'::jsonb
WHERE id = 'c0000000-0000-0000-0000-000000000007';

UPDATE questions SET
    body_translations = '{"ru": "На устройстве Junos настроен статический маршрут:\nset routing-options static route 192.168.100.0/24 next-hop 10.0.0.1\nКакая команда проверит наличие этого маршрута в таблице маршрутизации? (Введите полную команду)"}'::jsonb,
    options_translations = '{"ru": [{"id":"a","text":"show route 192.168.100.0/24"}]}'::jsonb
WHERE id = 'c0000000-0000-0000-0000-000000000008';

UPDATE questions SET
    body_translations = '{"ru": "Какие из перечисленных являются допустимыми типами интерфейсов Junos? (Выберите ДВА)"}'::jsonb,
    options_translations = '{"ru": [{"id":"a","text":"ge (Gigabit Ethernet)"},{"id":"b","text":"xe (10 Gigabit Ethernet)"},{"id":"c","text":"gi (Cisco-стиль GigabitEthernet)"},{"id":"d","text":"fa (Cisco-стиль FastEthernet)"}]}'::jsonb
WHERE id = 'c0000000-0000-0000-0000-000000000009';

UPDATE questions SET
    body_translations = '{"ru": "Вам нужно применить firewall filter, который считает пакеты на интерфейсе ge-0/0/1 без отбрасывания трафика. Какое действие следует использовать?"}'::jsonb,
    options_translations = '{"ru": [{"id":"a","text":"then accept;"},{"id":"b","text":"then count;"},{"id":"c","text":"then count accept;"},{"id":"d","text":"then log;"}]}'::jsonb
WHERE id = 'c0000000-0000-0000-0000-000000000010';

-- Russian translations for JNCIA-SP questions
UPDATE questions SET
    body_translations = '{"ru": "Какова основная функция MPLS?"}'::jsonb,
    options_translations = '{"ru": [{"id":"a","text":"Заменить IP-маршрутизацию коммутацией по меткам для более быстрой пересылки"},{"id":"b","text":"Обеспечить шифрование VPN-трафика"},{"id":"c","text":"Заменить BGP как протокол интернет-маршрутизации"},{"id":"d","text":"Обеспечить трансляцию сетевых адресов"}]}'::jsonb
WHERE id = 'c0000000-0000-0000-0000-000000000011';

UPDATE questions SET
    body_translations = '{"ru": "В MPLS какое устройство добавляет метку к пакету на границе MPLS-домена?"}'::jsonb,
    options_translations = '{"ru": [{"id":"a","text":"P-маршрутизатор (Provider)"},{"id":"b","text":"PE-маршрутизатор (Provider Edge)"},{"id":"c","text":"CE-маршрутизатор (Customer Edge)"},{"id":"d","text":"RR (Route Reflector)"}]}'::jsonb
WHERE id = 'c0000000-0000-0000-0000-000000000012';

UPDATE questions SET
    body_translations = '{"ru": "Какой протокол используется для распределения меток в MPLS?"}'::jsonb,
    options_translations = '{"ru": [{"id":"a","text":"OSPF"},{"id":"b","text":"LDP (Label Distribution Protocol)"},{"id":"c","text":"RIP"},{"id":"d","text":"SNMP"}]}'::jsonb
WHERE id = 'c0000000-0000-0000-0000-000000000013';

-- Russian translations for CCNA questions
UPDATE questions SET
    body_translations = '{"ru": "Каково значение административной дистанции OSPF по умолчанию в Cisco IOS?"}'::jsonb,
    options_translations = '{"ru": [{"id":"a","text":"90"},{"id":"b","text":"100"},{"id":"c","text":"110"},{"id":"d","text":"120"}]}'::jsonb
WHERE id = 'c0000000-0000-0000-0000-000000000014';

UPDATE questions SET
    body_translations = '{"ru": "Какой диапазон VLAN зарезервирован для normal-range VLAN на коммутаторе Cisco?"}'::jsonb,
    options_translations = '{"ru": [{"id":"a","text":"1-1001"},{"id":"b","text":"1-4094"},{"id":"c","text":"1002-4096"},{"id":"d","text":"1-1005"}]}'::jsonb
WHERE id = 'c0000000-0000-0000-0000-000000000015';

UPDATE questions SET
    body_translations = '{"ru": "Какая команда включает маршрутизацию RIP на маршрутизаторе Cisco?"}'::jsonb,
    options_translations = '{"ru": [{"id":"a","text":"router rip"},{"id":"b","text":"enable rip"},{"id":"c","text":"rip enable"},{"id":"d","text":"ip routing rip"}]}'::jsonb
WHERE id = 'c0000000-0000-0000-0000-000000000016';

-- ═══════════════════════════════════════
-- NEW QUESTIONS: JNCIA-Junos (JN0-101)
-- ═══════════════════════════════════════

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, body_translations, options, options_translations, explanation, reference_urls, blueprint_section, blueprint_weight, is_active) VALUES

-- Q17 (id: 021): BGP Route Selection
('c0000000-0000-0000-0000-000000000021', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'understand',
'In BGP route selection, which attribute is considered FIRST in the selection algorithm?',
'{"ru": "В алгоритме выбора маршрута BGP какой атрибут рассматривается ПЕРВЫМ?"}',
'[{"id":"a","text":"Local Preference","is_correct":false},{"id":"b","text":"Weight (Cisco-specific)","is_correct":false},{"id":"c","text":"Highest IP next-hop","is_correct":false},{"id":"d","text":"Prefer routes with highest local preference, then shortest AS_PATH","is_correct":true}]',
'{"ru": [{"id":"a","text":"Local Preference"},{"id":"b","text":"Weight (Cisco-specific)"},{"id":"c","text":"Наивысший IP next-hop"},{"id":"d","text":"Предпочитать маршруты с наибольшим local preference, затем с кратчайшим AS_PATH"}]}',
'The BGP route selection process in Junos first compares local preference (higher is better), then AS_PATH length (shorter is better), then origin code, MED, and finally IGP metric to the next-hop. Junos does not use Cisco-specific Weight attribute.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/bgp/topics/topic-map/bgp-route-selection.html'],
'BGP Route Selection', 12.0, TRUE),

-- Q18 (id: 022): MSTP
('c0000000-0000-0000-0000-000000000022', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand',
'What is the purpose of MSTP (Multiple Spanning Tree Protocol) in a Junos switch network?',
'{"ru": "Какова цель MSTP (Multiple Spanning Tree Protocol) в сети коммутаторов Junos?"}',
'[{"id":"a","text":"To combine multiple VLANs into a single spanning tree instance","is_correct":false},{"id":"b","text":"To allow multiple spanning tree instances, each mapping to one or more VLANs","is_correct":true},{"id":"c","text":"To replace RSTP with faster convergence","is_correct":false},{"id":"d","text":"To enable routing between VLANs","is_correct":false}]',
'{"ru": [{"id":"a","text":"Объединить несколько VLAN в один экземпляр spanning tree"},{"id":"b","text":"Создать несколько экземпляров spanning tree, каждый для одного или нескольких VLAN"},{"id":"c","text":"Заменить RSTP на более быструю сходимость"},{"id":"d","text":"Включить маршрутизацию между VLAN"}]}',
'MSTP (IEEE 802.1s) allows multiple spanning tree instances, each capable of mapping to one or more VLANs. This provides better link utilization than STP or RSTP, as different VLANs can use different active paths.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/spanning-tree/'],
'Spanning Tree Protocol', 8.0, TRUE),

-- Q19 (id: 023): Load Balancing
('c0000000-0000-0000-0000-000000000023', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'apply',
'You have two equal-cost paths to the same destination in Junos. Which statement about load balancing is correct?',
'{"ru": "У вас есть два равнозатратных пути к одному получателю в Junos. Какое утверждение о балансировке нагрузки верно?"}',
'[{"id":"a","text":"Junos automatically load-balances per-packet across equal-cost paths","is_correct":false},{"id":"b","text":"Junos installs only one of the equal-cost paths in the forwarding table by default","is_correct":false},{"id":"c","text":"Junos performs per-flow load balancing for equal-cost paths by default","is_correct":true},{"id":"d","text":"Load balancing must be manually configured using the load-balance knob","is_correct":false}]',
'{"ru": [{"id":"a","text":"Junos автоматически балансирует нагрузку по пакетам между равнозатратными путями"},{"id":"b","text":"Junos устанавливает только один из равнозатратных путей в таблицу пересылки по умолчанию"},{"id":"c","text":"Junos выполняет балансировку нагрузки по потокам для равнозатратных путей по умолчанию"},{"id":"d","text":"Балансировка нагрузки должна быть настроена вручную"}]}',
'Junos performs per-flow load balancing by default when multiple equal-cost paths exist. Per-packet load balancing is not recommended and would require explicit configuration. The per-flow approach ensures packets from the same flow take the same path, preventing out-of-order delivery.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/routing-policy/'],
'Routing Policy — Load Balancing', 10.0, TRUE),

-- Q20 (id: 024): Troubleshooting — BGP session down (exhibit)
('c0000000-0000-0000-0000-000000000024', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 4, 'troubleshoot',
'Exhibit: ---\nshow bgp summary\nGroups: 1 Peers: 1 Down peers: 1\nPeer          AS      InPkt   OutPkt   OutQ   Flaps   Last Up   State\n10.0.1.2      65002   0       0        0      5       Never     Active\n---\nThe EBGP session between two Junos routers remains in the Active state. Both routers have correct peer IPs and AS numbers. What is the MOST likely cause?',
'{"ru": "Exhibit: ---\nshow bgp summary\nGroups: 1 Peers: 1 Down peers: 1\nPeer          AS      InPkt   OutPkt   OutQ   Flaps   Last Up   State\n10.0.1.2      65002   0       0        0      5       Never     Active\n---\nEBGP-сессия между двумя маршрутизаторами Junos остается в состоянии Active. Оба маршрутизатора имеют правильные IP-адреса пиров и номера AS. Какова НАИБОЛЕЕ вероятная причина?"}',
'[{"id":"a","text":"The BGP peer is not reachable (no route to 10.0.1.2)","is_correct":true},{"id":"b","text":"The BGP group name is misspelled","is_correct":false},{"id":"c","text":"The hold timer is too short","is_correct":false},{"id":"d","text":"The AS number exceeds 65535","is_correct":false}]',
'{"ru": [{"id":"a","text":"BGP-пир недоступен (нет маршрута до 10.0.1.2)"},{"id":"b","text":"Имя BGP-группы написано с ошибкой"},{"id":"c","text":"Слишком короткий hold timer"},{"id":"d","text":"Номер AS превышает 65535"}]}',
'The BGP Active state indicates the router is actively trying to initiate a TCP connection to the peer. 0 packets received (InPkt=0) confirms the TCP connection is not being established. The most likely cause is that the peer is not reachable (no route in the routing table). A missing route to the peer''s IP would prevent TCP port 179 from opening.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/bgp/topics/topic-map/bgp-troubleshooting.html'],
'BGP Troubleshooting', 10.0, TRUE),

-- Q21 (id: 025): commit check
('c0000000-0000-0000-0000-000000000025', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand',
'Which command validates the candidate configuration without activating it?',
'{"ru": "Какая команда проверяет кандидатскую конфигурацию без её активации?"}',
'[{"id":"a","text":"commit check","is_correct":true},{"id":"b","text":"commit confirmed","is_correct":false},{"id":"c","text":"commit verify","is_correct":false},{"id":"d","text":"validate configuration","is_correct":false}]',
'{"ru": [{"id":"a","text":"commit check"},{"id":"b","text":"commit confirmed"},{"id":"c","text":"commit verify"},{"id":"d","text":"validate configuration"}]}',
'The "commit check" command validates syntax and semantics of the candidate configuration without applying it. "commit confirmed" activates the configuration with automatic rollback if not confirmed within the timeout period.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli/'],
'Junos Configuration Management', 8.0, TRUE),

-- Q22 (id: 026): GRE Tunnel
('c0000000-0000-0000-0000-000000000026', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'apply',
'You need to configure a GRE tunnel between two Junos routers. Which interface type is used?',
'{"ru": "Вам нужно настроить GRE-туннель между двумя маршрутизаторами Junos. Какой тип интерфейса используется?"}',
'[{"id":"a","text":"gr- (Generic Routing Encapsulation interface)","is_correct":true},{"id":"b","text":"ip- (IP tunnel interface)","is_correct":false},{"id":"c","text":"vt- (VPN tunnel interface)","is_correct":false},{"id":"d","text":"tunnel- (Generic tunnel interface)","is_correct":false}]',
'{"ru": [{"id":"a","text":"gr- (Generic Routing Encapsulation)"},{"id":"b","text":"ip- (IP tunnel)"},{"id":"c","text":"vt- (VPN tunnel)"},{"id":"d","text":"tunnel- (Generic tunnel)"}]}',
'Junos uses the gr- (GRE) interface type for GRE tunnels. Configuration requires "tunnel source", "tunnel destination", and a family (inet/inet6). GRE is defined in RFC 2784 and does not provide encryption — use IPsec for secure tunnels.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/vpn/'],
'GRE Tunnels', 8.0, TRUE),

-- Q23 (id: 027): VRRP (multiple-choice)
('c0000000-0000-0000-0000-000000000027', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'multiple-choice', 3, 'apply',
'Which of the following are valid VRRP configuration elements in Junos? (Select TWO)',
'{"ru": "Какие из перечисленных являются допустимыми элементами конфигурации VRRP в Junos? (Выберите ДВА)"}',
'[{"id":"a","text":"virtual-inet-address","is_correct":true},{"id":"b","text":"virtual-router-id","is_correct":true},{"id":"c","text":"vrrp-group priority","is_correct":false},{"id":"d","text":"standby ip","is_correct":false}]',
'{"ru": [{"id":"a","text":"virtual-inet-address"},{"id":"b","text":"virtual-router-id"},{"id":"c","text":"vrrp-group priority"},{"id":"d","text":"standby ip"}]}',
'In Junos, VRRP is configured under the interface with "virtual-inet-address" and "virtual-router-id" statements. "vrrp-group priority" is used in Cisco IOS. Junos uses "priority" under the VRRP configuration, not "standby ip" (which is Cisco''s HSRP syntax).',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/high-availability/'],
'High Availability — VRRP', 8.0, TRUE),

-- Q24 (id: 028): SNMP
('c0000000-0000-0000-0000-000000000028', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'remember',
'Which protocol does Junos use for system logging to an external server?',
'{"ru": "Какой протокол использует Junos для системного журналирования на внешний сервер?"}',
'[{"id":"a","text":"syslog","is_correct":true},{"id":"b","text":"SNMP traps","is_correct":false},{"id":"c","text":"NetFlow","is_correct":false},{"id":"d","text":"RMON","is_correct":false}]',
'{"ru": [{"id":"a","text":"syslog"},{"id":"b","text":"SNMP traps"},{"id":"c","text":"NetFlow"},{"id":"d","text":"RMON"}]}',
'Junos uses syslog (UDP port 514) to send log messages to external logging servers. Configuration is under "set system syslog host <server>". SNMP traps are for network management alerts, not detailed logging.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/system-logging/'],
'System Logging', 5.0, TRUE);

-- Tags for new JNCIA-Junos questions
INSERT INTO question_tags (question_id, technology, protocol) VALUES
    ('c0000000-0000-0000-0000-000000000021', 'BGP', 'BGP'),
    ('c0000000-0000-0000-0000-000000000022', 'Spanning Tree', 'MSTP'),
    ('c0000000-0000-0000-0000-000000000023', 'Load Balancing', 'ECMP'),
    ('c0000000-0000-0000-0000-000000000024', 'BGP Troubleshooting', 'BGP'),
    ('c0000000-0000-0000-0000-000000000025', 'Junos Configuration', 'General'),
    ('c0000000-0000-0000-0000-000000000026', 'Tunnels', 'GRE'),
    ('c0000000-0000-0000-0000-000000000027', 'VRRP', 'VRRP'),
    ('c0000000-0000-0000-0000-000000000028', 'System Logging', 'syslog');

-- ═══════════════════════════════════════
-- NEW QUESTIONS: JNCIA-SP (JN0-201)
-- ═══════════════════════════════════════

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, body_translations, options, options_translations, explanation, reference_urls, blueprint_section, blueprint_weight, is_active) VALUES

-- Q25 (id: 031): LSP path
('c0000000-0000-0000-0000-000000000031', 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'single-choice', 3, 'understand',
'In MPLS, what command displays the label-switched path (LSP) information on a Junos router?',
'{"ru": "В MPLS какая команда отображает информацию о LSP (label-switched path) на маршрутизаторе Junos?"}',
'[{"id":"a","text":"show mpls lsp","is_correct":true},{"id":"b","text":"show mpls label","is_correct":false},{"id":"c","text":"show route label-switched","is_correct":false},{"id":"d","text":"show mpls path","is_correct":false}]',
'{"ru": [{"id":"a","text":"show mpls lsp"},{"id":"b","text":"show mpls label"},{"id":"c","text":"show route label-switched"},{"id":"d","text":"show mpls path"}]}',
'The "show mpls lsp" command displays all LSPs, their state (Up/Down), path, bandwidth, and statistics. "show route table mpls.0" displays the MPLS label forwarding table.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/mpls/'],
'MPLS Operations', 15.0, TRUE),

-- Q26 (id: 032): RSVP-TE
('c0000000-0000-0000-0000-000000000032', 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'single-choice', 4, 'apply',
'Which protocol provides traffic engineering capabilities in MPLS networks?',
'{"ru": "Какой протокол обеспечивает возможности Traffic Engineering в MPLS-сетях?"}',
'[{"id":"a","text":"RSVP-TE","is_correct":true},{"id":"b","text":"LDP","is_correct":false},{"id":"c","text":"IS-IS","is_correct":false},{"id":"d","text":"MP-BGP","is_correct":false}]',
'{"ru": [{"id":"a","text":"RSVP-TE"},{"id":"b","text":"LDP"},{"id":"c","text":"IS-IS"},{"id":"d","text":"MP-BGP"}]}',
'RSVP-TE (Resource Reservation Protocol with Traffic Engineering extensions) provides MPLS traffic engineering capabilities including explicit path configuration, bandwidth reservation, and fast reroute. LDP is simpler but does not support TE.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/mpls/'],
'MPLS Traffic Engineering', 15.0, TRUE),

-- Q27 (id: 033): BGP-LU
('c0000000-0000-0000-0000-000000000033', 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'single-choice', 4, 'analyze',
'What is the primary advantage of BGP-LU (BGP with Labeled Unicast) in a service provider network?',
'{"ru": "В чем основное преимущество BGP-LU (BGP с Labeled Unicast) в провайдерской сети?"}',
'[{"id":"a","text":"It replaces LDP entirely by carrying MPLS labels in BGP updates","is_correct":true},{"id":"b","text":"It provides encryption for BGP sessions","is_correct":false},{"id":"c","text":"It increases the BGP table size limit","is_correct":false},{"id":"d","text":"It enables IPv6 routing over IPv4 MPLS","is_correct":false}]',
'{"ru": [{"id":"a","text":"Полностью заменяет LDP, передавая MPLS-метки в BGP-обновлениях"},{"id":"b","text":"Обеспечивает шифрование BGP-сессий"},{"id":"c","text":"Увеличивает лимит размера BGP-таблицы"},{"id":"d","text":"Включает IPv6-маршрутизацию поверх MPLS IPv4"}]}',
'BGP-LU (RFC 3107) allows BGP to carry MPLS labels alongside IPv4/IPv6 prefixes. This eliminates the need for a full mesh of LDP sessions and enables inter-AS MPLS VPNs. It is commonly used in SP networks for seamless MPLS.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/mpls/'],
'BGP-LU', 12.0, TRUE),

-- Q28 (id: 034): Troubleshooting MTU (exhibit)
('c0000000-0000-0000-0000-000000000034', 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'single-choice', 5, 'troubleshoot',
'Exhibit: ---\nMPLS LSP to 10.0.0.2 is down. MPLS ping shows "Label switched path signalled but MPLS TTL expired in transit."\n---\nTwo PE routers are connected via P routers over a network where the physical MTU is 1500 bytes. MPLS labels have been added but packets are being fragmented. What is the MOST likely issue?',
'{"ru": "Exhibit: ---\nMPLS LSP до 10.0.0.2 не работает. MPLS ping показывает \"Label switched path signalled but MPLS TTL expired in transit.\"\n---\nДва PE-маршрутизатора соединены через P-маршрутизаторы по сети с MTU 1500 байт. MPLS-метки добавлены, но пакеты фрагментируются. Какова НАИБОЛЕЕ вероятная причина?"}',
'[{"id":"a","text":"The interface MTU is too small to accommodate the MPLS label overhead (4 bytes per label)","is_correct":true},{"id":"b","text":"BGP session between PEs is down","is_correct":false},{"id":"c","text":"OSPF is not redistributing connected routes","is_correct":false},{"id":"d","text":"LDP is not enabled on the loopback interface","is_correct":false}]',
'{"ru": [{"id":"a","text":"MTU интерфейса слишком мал для размещения служебных данных MPLS-меток (4 байта на метку)"},{"id":"b","text":"BGP-сессия между PE не работает"},{"id":"c","text":"OSPF не редистрибьютирует connected-маршруты"},{"id":"d","text":"LDP не включен на loopback-интерфейсе"}]}',
'When MPLS labels are added to packets, the total packet size increases (typically 4 bytes per label). If the physical MTU (1500) is not adjusted to account for label overhead (e.g., set to 1512 or higher), packets may exceed MTU and be fragmented or dropped. The "MPLS TTL expired" error can occur when MPLS packets are fragmented and the fragments take different paths.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/mpls/topics/topic-map/mpls-troubleshooting.html'],
'MPLS Troubleshooting', 10.0, TRUE);

-- Tags for new JNCIA-SP questions
INSERT INTO question_tags (question_id, technology, protocol) VALUES
    ('c0000000-0000-0000-0000-000000000031', 'MPLS', 'LDP'),
    ('c0000000-0000-0000-0000-000000000032', 'MPLS Traffic Engineering', 'RSVP-TE'),
    ('c0000000-0000-0000-0000-000000000033', 'BGP-LU', 'BGP'),
    ('c0000000-0000-0000-0000-000000000034', 'MPLS Troubleshooting', 'MPLS');

-- ═══════════════════════════════════════
-- NEW QUESTIONS: CCNA (200-301)
-- ═══════════════════════════════════════

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, body_translations, options, options_translations, explanation, reference_urls, blueprint_section, blueprint_weight, is_active) VALUES

-- Q29 (id: 041): STP
('c0000000-0000-0000-0000-000000000041', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'understand',
'Which spanning tree variant provides the fastest convergence in a Cisco switched network?',
'{"ru": "Какая разновидность spanning tree обеспечивает самую быструю сходимость в коммутируемой сети Cisco?"}',
'[{"id":"a","text":"RSTP (802.1w)","is_correct":true},{"id":"b","text":"STP (802.1D)","is_correct":false},{"id":"c","text":"PVST+","is_correct":false},{"id":"d","text":"Rapid PVST+","is_correct":false}]',
'{"ru": [{"id":"a","text":"RSTP (802.1w)"},{"id":"b","text":"STP (802.1D)"},{"id":"c","text":"PVST+"},{"id":"d","text":"Rapid PVST+"}]}',
'RSTP (802.1w) provides the fastest convergence (typically 1-3 seconds vs 30-50 seconds for traditional STP). Rapid PVST+ is Cisco''s per-VLAN implementation of RSTP. Both use rapid transition mechanisms like edge ports and link types.',
ARRAY['https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/'],
'Network Access — STP', 10.0, TRUE),

-- Q30 (id: 042): IPv6 SLAAC
('c0000000-0000-0000-0000-000000000042', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 3, 'apply',
'In SLAAC (Stateless Address Autoconfiguration), which IPv6 prefix does a host use to generate its interface ID?',
'{"ru": "В SLAAC (Stateless Address Autoconfiguration), какой IPv6-префикс использует хост для генерации своего interface ID?"}',
'[{"id":"a","text":"The prefix received in Router Advertisement (RA) messages","is_correct":true},{"id":"b","text":"The link-local prefix (fe80::/10)","is_correct":false},{"id":"c","text":"The prefix configured via DHCPv6","is_correct":false},{"id":"d","text":"The multicast prefix (ff00::/8)","is_correct":false}]',
'{"ru": [{"id":"a","text":"Префикс, полученный в сообщениях Router Advertisement (RA)"},{"id":"b","text":"Link-local префикс (fe80::/10)"},{"id":"c","text":"Префикс, настроенный через DHCPv6"},{"id":"d","text":"Мультикаст префикс (ff00::/8)"}]}',
'In SLAAC, hosts learn the IPv6 prefix from Router Advertisement messages sent by routers. The host then generates its interface ID using EUI-64 or privacy extensions, combining it with the learned prefix to form a global unicast address.',
ARRAY['https://www.cisco.com/c/en/us/support/docs/ip/ipv6/'],
'IP Connectivity — IPv6', 8.0, TRUE),

-- Q31 (id: 043): EtherChannel
('c0000000-0000-0000-0000-000000000043', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'understand',
'Which protocol is used for dynamic EtherChannel negotiation on Cisco switches?',
'{"ru": "Какой протокол используется для динамического согласования EtherChannel на коммутаторах Cisco?"}',
'[{"id":"a","text":"LACP (802.3ad)","is_correct":true},{"id":"b","text":"PAgP (Port Aggregation Protocol)","is_correct":false},{"id":"c","text":"DTP (Dynamic Trunking Protocol)","is_correct":false},{"id":"d","text":"CDP (Cisco Discovery Protocol)","is_correct":false}]',
'{"ru": [{"id":"a","text":"LACP (802.3ad)"},{"id":"b","text":"PAgP (Port Aggregation Protocol)"},{"id":"c","text":"DTP (Dynamic Trunking Protocol)"},{"id":"d","text":"CDP (Cisco Discovery Protocol)"}]}',
'LACP (IEEE 802.3ad) is the open standard protocol for EtherChannel negotiation. PAgP is Cisco proprietary. Both can be used, but LACP is recommended for multi-vendor interoperability. DTP negotiates trunking, not aggregation.',
ARRAY['https://www.cisco.com/c/en/us/support/docs/lan-switching/etherchannel/'],
'Network Access — EtherChannel', 8.0, TRUE),

-- Q32 (id: 044): ACL troubleshooting (exhibit)
('c0000000-0000-0000-0000-000000000044', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 4, 'troubleshoot',
'Exhibit: ---\ninterface GigabitEthernet0/1\n ip access-group BLOCK_TELNET in\n!\nip access-list extended BLOCK_TELNET\n deny tcp any any eq 23\n permit ip any any\n---\nUsers on VLAN 10 (connected to Gi0/1) cannot SSH to the server at 10.0.0.100 on VLAN 20. What is the issue?',
'{"ru": "Exhibit: ---\ninterface GigabitEthernet0/1\n ip access-group BLOCK_TELNET in\n!\nip access-list extended BLOCK_TELNET\n deny tcp any any eq 23\n permit ip any any\n---\nПользователи из VLAN 10 (подключенного к Gi0/1) не могут подключиться по SSH к серверу 10.0.0.100 в VLAN 20. В чем проблема?"}',
'[{"id":"a","text":"The ACL blocks Telnet (TCP/23), which is correct; SSH (TCP/22) should be allowed. The issue is elsewhere.","is_correct":true},{"id":"b","text":"The ACL is applied inbound, so return traffic from the server is blocked","is_correct":false},{"id":"c","text":"The ACL does not block Telnet unless applied outbound","is_correct":false},{"id":"d","text":"The permit ip any any allows all traffic, so SSH is not blocked by this ACL","is_correct":false}]',
'{"ru": [{"id":"a","text":"ACL блокирует Telnet (TCP/23), это верно; SSH (TCP/22) должен быть разрешен. Проблема в другом."},{"id":"b","text":"ACL применен входящим, поэтому обратный трафик от сервера блокируется"},{"id":"c","text":"ACL не блокирует Telnet, если не применен исходящим"},{"id":"d","text":"permit ip any any разрешает весь трафик, поэтому SSH не блокируется этим ACL"}]}',
'The ACL shown is correct for blocking Telnet while allowing SSH. The ACL blocks TCP/23 (Telnet) but permits all other IP traffic including SSH (TCP/22). If users cannot SSH, the issue is elsewhere (e.g., routing, server configuration, VRF, or a missing permit statement on another interface).',
ARRAY['https://www.cisco.com/c/en/us/support/docs/security/access-lists/'],
'Network Access — ACLs', 10.0, TRUE),

-- Q33 (id: 045): NTP
('c0000000-0000-0000-0000-000000000045', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'remember',
'Which Cisco IOS command configures the device as an NTP client with a single NTP server at 192.168.1.10?',
'{"ru": "Какая команда Cisco IOS настраивает устройство как NTP-клиент с единственным NTP-сервером 192.168.1.10?"}',
'[{"id":"a","text":"ntp server 192.168.1.10","is_correct":true},{"id":"b","text":"ntp peer 192.168.1.10","is_correct":false},{"id":"c","text":"clock ntp 192.168.1.10","is_correct":false},{"id":"d","text":"ntp client 192.168.1.10","is_correct":false}]',
'{"ru": [{"id":"a","text":"ntp server 192.168.1.10"},{"id":"b","text":"ntp peer 192.168.1.10"},{"id":"c","text":"clock ntp 192.168.1.10"},{"id":"d","text":"ntp client 192.168.1.10"}]}',
'The "ntp server" command configures the device as an NTP client that synchronizes to the specified server. "ntp peer" is used for symmetric peering (both devices can sync to each other). Use "show ntp associations" and "show ntp status" to verify synchronization.',
ARRAY['https://www.cisco.com/c/en/us/support/docs/management-utility/network-time-protocol-ntp/'],
'Network Management — NTP', 5.0, TRUE),

-- Q34 (id: 046): QoS — both options are correct
('c0000000-0000-0000-0000-000000000046', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'multiple-choice', 3, 'understand',
'Which QoS mechanisms provide bandwidth guarantee to specific traffic classes? (Select TWO)',
'{"ru": "Какие механизмы QoS гарантируют пропускную способность для определенных классов трафика? (Выберите ДВА)"}',
'[{"id":"a","text":"CBWFQ (Class-Based Weighted Fair Queuing)","is_correct":true},{"id":"b","text":"LLQ (Low Latency Queuing)","is_correct":true},{"id":"c","text":"FIFO (First In First Out)","is_correct":false},{"id":"d","text":"WRED (Weighted Random Early Detection)","is_correct":false}]',
'{"ru": [{"id":"a","text":"CBWFQ (Class-Based Weighted Fair Queuing)"},{"id":"b","text":"LLQ (Low Latency Queuing)"},{"id":"c","text":"FIFO (First In First Out)"},{"id":"d","text":"WRED (Weighted Random Early Detection)"}]}',
'Both CBWFQ and LLQ guarantee bandwidth to specific traffic classes. CBWFQ assigns a minimum bandwidth allocation per class. LLQ adds a strict priority queue on top of CBWFQ for delay-sensitive traffic while still providing bandwidth guarantees. FIFO has no guarantees; WRED is a congestion avoidance mechanism, not a queuing method.',
ARRAY['https://www.cisco.com/c/en/us/support/docs/quality-of-service-qos/'],
'Network Management — QoS', 8.0, TRUE),

-- Q35 (id: 047): MAC table
('c0000000-0000-0000-0000-000000000047', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 3, 'remember',
'Which Cisco IOS command displays the MAC address table on a switch?',
'{"ru": "Какая команда Cisco IOS отображает таблицу MAC-адресов на коммутаторе?"}',
'[{"id":"a","text":"show mac address-table","is_correct":true},{"id":"b","text":"show mac-table","is_correct":false},{"id":"c","text":"show switch mac","is_correct":false},{"id":"d","text":"display mac-address-table","is_correct":false}]',
'{"ru": [{"id":"a","text":"show mac address-table"},{"id":"b","text":"show mac-table"},{"id":"c","text":"show switch mac"},{"id":"d","text":"display mac-address-table"}]}',
'The "show mac address-table" command (or "show mac address-table dynamic" for dynamic entries only) displays the switch MAC address table. This includes VLAN, MAC address, type (dynamic/static), and port mappings.',
ARRAY['https://www.cisco.com/c/en/us/support/docs/lan-switching/'],
'Network Access — Switching', 5.0, TRUE);

-- Tags for new CCNA questions
INSERT INTO question_tags (question_id, technology, protocol) VALUES
    ('c0000000-0000-0000-0000-000000000041', 'Spanning Tree', 'STP'),
    ('c0000000-0000-0000-0000-000000000042', 'IPv6', 'SLAAC'),
    ('c0000000-0000-0000-0000-000000000043', 'EtherChannel', 'LACP'),
    ('c0000000-0000-0000-0000-000000000044', 'ACL', 'TCP'),
    ('c0000000-0000-0000-0000-000000000045', 'NTP', 'NTP'),
    ('c0000000-0000-0000-0000-000000000046', 'QoS', 'CBWFQ'),
    ('c0000000-0000-0000-0000-000000000047', 'Switching', 'MAC');

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
-- Remove new question tags
DELETE FROM question_tags WHERE question_id IN (
    'c0000000-0000-0000-0000-000000000021','c0000000-0000-0000-0000-000000000022',
    'c0000000-0000-0000-0000-000000000023','c0000000-0000-0000-0000-000000000024',
    'c0000000-0000-0000-0000-000000000025','c0000000-0000-0000-0000-000000000026',
    'c0000000-0000-0000-0000-000000000027','c0000000-0000-0000-0000-000000000028',
    'c0000000-0000-0000-0000-000000000031','c0000000-0000-0000-0000-000000000032',
    'c0000000-0000-0000-0000-000000000033','c0000000-0000-0000-0000-000000000034',
    'c0000000-0000-0000-0000-000000000041','c0000000-0000-0000-0000-000000000042',
    'c0000000-0000-0000-0000-000000000043','c0000000-0000-0000-0000-000000000044',
    'c0000000-0000-0000-0000-000000000045','c0000000-0000-0000-0000-000000000046',
    'c0000000-0000-0000-0000-000000000047'
);
-- Remove new questions
DELETE FROM questions WHERE id IN (
    'c0000000-0000-0000-0000-000000000021','c0000000-0000-0000-0000-000000000022',
    'c0000000-0000-0000-0000-000000000023','c0000000-0000-0000-0000-000000000024',
    'c0000000-0000-0000-0000-000000000025','c0000000-0000-0000-0000-000000000026',
    'c0000000-0000-0000-0000-000000000027','c0000000-0000-0000-0000-000000000028',
    'c0000000-0000-0000-0000-000000000031','c0000000-0000-0000-0000-000000000032',
    'c0000000-0000-0000-0000-000000000033','c0000000-0000-0000-0000-000000000034',
    'c0000000-0000-0000-0000-000000000041','c0000000-0000-0000-0000-000000000042',
    'c0000000-0000-0000-0000-000000000043','c0000000-0000-0000-0000-000000000044',
    'c0000000-0000-0000-0000-000000000045','c0000000-0000-0000-0000-000000000046',
    'c0000000-0000-0000-0000-000000000047'
);
-- Reset translations on original questions to empty JSONB
UPDATE questions SET body_translations = '{}'::jsonb, options_translations = '{}'::jsonb;
-- +goose StatementEnd
