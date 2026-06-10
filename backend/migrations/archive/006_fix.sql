-- ═══════════════════════════════════════
-- 1. Update JNCIA-Junos to current code JN0-106
-- ═══════════════════════════════════════
UPDATE exams SET code = 'JN0-106', name = 'JNCIA-Junos', total_questions = 65 WHERE code = 'JN0-101';

-- ═══════════════════════════════════════
-- 2. Add missing exams for ENT track
-- ═══════════════════════════════════════
INSERT INTO exams (id, track_id, code, name, level, duration_minutes, total_questions, passing_score) VALUES
    ('b0000000-0000-0000-0000-000000000010', 'a0000000-0000-0000-0000-000000000001', 'JN0-343', 'JNCIS-ENT', 'JNCIS', 90, 65, 70.00),
    ('b0000000-0000-0000-0000-000000000011', 'a0000000-0000-0000-0000-000000000001', 'JN0-664', 'JNCIP-ENT', 'JNCIP', 120, 75, 70.00);

-- ═══════════════════════════════════════
-- 3. Add basic exams for SEC, DC, AUT tracks
-- ═══════════════════════════════════════
INSERT INTO exams (id, track_id, code, name, level, duration_minutes, total_questions, passing_score) VALUES
    ('b0000000-0000-0000-0000-000000000020', 'a0000000-0000-0000-0000-000000000003', 'JN0-230', 'JNCIA-SEC', 'JNCIA', 90, 60, 65.00),
    ('b0000000-0000-0000-0000-000000000021', 'a0000000-0000-0000-0000-000000000004', 'JN0-480', 'JNCIA-DC', 'JNCIA', 90, 60, 65.00),
    ('b0000000-0000-0000-0000-000000000022', 'a0000000-0000-0000-0000-000000000005', 'JN0-223', 'JNCIA-DevOps', 'JNCIA', 90, 60, 65.00);

-- ═══════════════════════════════════════
-- 4. NEW QUESTIONS: JNCIA-Junos (JN0-106)
-- ═══════════════════════════════════════

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, body_translations, options, options_translations, explanation, reference_urls, blueprint_section, blueprint_weight, is_active) VALUES

-- Q36: OSI Model
('c0000000-0000-0000-0000-000000000050', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 1, 'remember',
'At which OSI layer does IP operate?',
'{"ru": "На каком уровне OSI работает IP?"}',
'[{"id":"a","text":"Layer 2 — Data Link","is_correct":false},{"id":"b","text":"Layer 3 — Network","is_correct":true},{"id":"c","text":"Layer 4 — Transport","is_correct":false},{"id":"d","text":"Layer 1 — Physical","is_correct":false}]',
'{"ru": [{"id":"a","text":"Уровень 2 — Канальный"},{"id":"b","text":"Уровень 3 — Сетевой"},{"id":"c","text":"Уровень 4 — Транспортный"},{"id":"d","text":"Уровень 1 — Физический"}]}',
'IP operates at Layer 3 (Network layer). It handles logical addressing and routing.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/junos-overview/'],
'Networking Fundamentals', 8.0, TRUE),

-- Q37: IPv4 subnetting
('c0000000-0000-0000-0000-000000000051', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'apply',
'What is the subnet mask for /27 prefix length?',
'{"ru": "Какая маска подсети соответствует префиксу /27?"}',
'[{"id":"a","text":"255.255.255.0","is_correct":false},{"id":"b","text":"255.255.255.224","is_correct":true},{"id":"c","text":"255.255.255.192","is_correct":false},{"id":"d","text":"255.255.255.248","is_correct":false}]',
'{"ru": [{"id":"a","text":"255.255.255.0"},{"id":"b","text":"255.255.255.224"},{"id":"c","text":"255.255.255.192"},{"id":"d","text":"255.255.255.248"}]}',
'A /27 = 255.255.255.224, providing 30 usable host addresses per subnet.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/junos-overview/'],
'Networking Fundamentals — IPv4', 8.0, TRUE),

-- Q38: Junos RE redundancy
('c0000000-0000-0000-0000-000000000052', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'understand',
'In a Junos dual-RE system, what command performs a graceful switchover?',
'{"ru": "В системе Junos с двумя RE какая команда выполняет graceful переключение?"}',
'[{"id":"a","text":"request chassis routing-engine master switch","is_correct":true},{"id":"b","text":"redundancy switchover","is_correct":false},{"id":"c","text":"reload routing-engine slave","is_correct":false},{"id":"d","text":"request system switchover","is_correct":false}]',
'{"ru": [{"id":"a","text":"request chassis routing-engine master switch"},{"id":"b","text":"redundancy switchover"},{"id":"c","text":"reload routing-engine slave"},{"id":"d","text":"request system switchover"}]}',
'request chassis routing-engine master switch performs GRES, preserving control plane state during transition.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/high-availability/'],
'Junos OS Fundamentals — RE', 8.0, TRUE),

-- Q39: Junos user authentication
('c0000000-0000-0000-0000-000000000053', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'apply',
'Which Junos configuration statement creates a local user account with authentication?',
'{"ru": "Какое выражение конфигурации Junos создает локальную учетную запись?"}',
'[{"id":"a","text":"set system login user admin class super-user authentication plain-text-password","is_correct":true},{"id":"b","text":"set system user admin password test123","is_correct":false},{"id":"c","text":"set system authentication user admin class super-user","is_correct":false},{"id":"d","text":"set system login class super-user user admin","is_correct":false}]',
'{"ru": [{"id":"a","text":"set system login user admin class super-user authentication plain-text-password"},{"id":"b","text":"set system user admin password test123"},{"id":"c","text":"set system authentication user admin class super-user"},{"id":"d","text":"set system login class super-user user admin"}]}',
'The correct hierarchy is set system login user <name> class <class> authentication plain-text-password.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/user-management/'],
'Configuration Basics — User Accounts', 6.0, TRUE),

-- Q40: Forwarding Table
('c0000000-0000-0000-0000-000000000054', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'understand',
'In Junos, what is the difference between the routing table and the forwarding table?',
'{"ru": "В Junos в чем разница между таблицей маршрутизации и таблицей пересылки?"}',
'[{"id":"a","text":"The routing table contains all routes; the forwarding table contains only the active routes used for packet forwarding","is_correct":true},{"id":"b","text":"They are identical; terms are interchangeable","is_correct":false},{"id":"c","text":"The forwarding table contains only BGP routes; the routing table contains all routes","is_correct":false},{"id":"d","text":"The routing table is stored on the PFE; the forwarding table on the RE","is_correct":false}]',
'{"ru": [{"id":"a","text":"Таблица маршрутизации содержит все маршруты; таблица пересылки — только активные"},{"id":"b","text":"Они идентичны; термины взаимозаменяемы"},{"id":"c","text":"Таблица пересылки содержит только BGP-маршруты"},{"id":"d","text":"Таблица маршрутизации хранится на PFE; таблица пересылки на RE"}]}',
'Routing table (inet.0) has all routes. Forwarding table has active routes, downloaded to PFE.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/junos-overview/'],
'Junos OS Architecture', 10.0, TRUE),

-- Q41: Interface configuration
('c0000000-0000-0000-0000-000000000055', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'apply',
'Which Junos command configures an IP address on interface ge-0/0/1?',
'{"ru": "Какая команда Junos настраивает IP-адрес на интерфейсе ge-0/0/1?"}',
'[{"id":"a","text":"set interfaces ge-0/0/1 unit 0 family inet address 192.168.1.1/24","is_correct":true},{"id":"b","text":"set interface ge-0/0/1 ip address 192.168.1.1 255.255.255.0","is_correct":false},{"id":"c","text":"set interfaces ge-0/0/1 ip 192.168.1.1/24","is_correct":false},{"id":"d","text":"ip address 192.168.1.1 255.255.255.0 interface ge-0/0/1","is_correct":false}]',
'{"ru": [{"id":"a","text":"set interfaces ge-0/0/1 unit 0 family inet address 192.168.1.1/24"},{"id":"b","text":"set interface ge-0/0/1 ip address 192.168.1.1 255.255.255.0"},{"id":"c","text":"set interfaces ge-0/0/1 ip 192.168.1.1/24"},{"id":"d","text":"ip address 192.168.1.1 255.255.255.0 interface ge-0/0/1"}]}',
'Junos: set interfaces <name> unit <n> family <family> address <ip/prefix>.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/interfaces/'],
'Configuration Basics — Interfaces', 8.0, TRUE),

-- Q42: Monitoring
('c0000000-0000-0000-0000-000000000056', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'remember',
'Which Junos operational command shows interface errors and statistics?',
'{"ru": "Какая операционная команда Junos показывает ошибки и статистику интерфейса?"}',
'[{"id":"a","text":"show interfaces ge-0/0/1 extensive","is_correct":true},{"id":"b","text":"show configuration interfaces ge-0/0/1","is_correct":false},{"id":"c","text":"monitor interface ge-0/0/1","is_correct":false},{"id":"d","text":"show ge-0/0/1 statistics","is_correct":false}]',
'{"ru": [{"id":"a","text":"show interfaces ge-0/0/1 extensive"},{"id":"b","text":"show configuration interfaces ge-0/0/1"},{"id":"c","text":"monitor interface ge-0/0/1"},{"id":"d","text":"show ge-0/0/1 statistics"}]}',
'show interfaces <name> extensive provides detailed error counts and statistics.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/interfaces/'],
'Operational Monitoring', 6.0, TRUE),

-- Q43: Rescue configuration
('c0000000-0000-0000-0000-000000000057', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'understand',
'What is the purpose of the rescue configuration in Junos?',
'{"ru": "Какова цель rescue configuration в Junos?"}',
'[{"id":"a","text":"A known-good configuration saved separately that can be loaded if the active config fails","is_correct":true},{"id":"b","text":"A minimal config that allows SSH access only","is_correct":false},{"id":"c","text":"An automatic backup created every commit","is_correct":false},{"id":"d","text":"Used to recover from a failed software upgrade","is_correct":false}]',
'{"ru": [{"id":"a","text":"Заведомо рабочая конфигурация для загрузки при сбое активной"},{"id":"b","text":"Минимальная конфигурация только для SSH"},{"id":"c","text":"Автоматический backup при каждом commit"},{"id":"d","text":"Восстановление после неудачного обновления ПО"}]}',
'request system configuration rescue save and rollback rescue for recovery.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli/'],
'Junos Configuration Management', 6.0, TRUE),

-- Q44: IS-IS
('c0000000-0000-0000-0000-000000000058', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'understand',
'In IS-IS, which statement is correct about Level 1 and Level 2 routers?',
'{"ru": "В IS-IS какое утверждение верно о маршрутизаторах Level 1 и Level 2?"}',
'[{"id":"a","text":"Level 1 routers route within an area, Level 2 routers route between areas","is_correct":true},{"id":"b","text":"Level 1 handles IPv6 only, Level 2 handles IPv4 only","is_correct":false},{"id":"c","text":"Level 2 routers only participate in BGP","is_correct":false},{"id":"d","text":"Level 1 cannot form adjacencies with Level 2 routers","is_correct":false}]',
'{"ru": [{"id":"a","text":"Level 1 маршрутизируют внутри области, Level 2 — между областями"},{"id":"b","text":"Level 1 только IPv6, Level 2 только IPv4"},{"id":"c","text":"Level 2 участвуют только в BGP"},{"id":"d","text":"Level 1 не могут устанавливать смежности с Level 2"}]}',
'IS-IS: Level 1 = intra-area, Level 2 = inter-area. Level 1-2 routers act as borders.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/is-is/'],
'Routing Fundamentals — IS-IS', 8.0, TRUE),

-- Q45: Static route with next-table
('c0000000-0000-0000-0000-000000000059', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 4, 'apply',
'In Junos, what is the purpose of the next-table option in a static route?',
'{"ru": "В Junos какова цель опции next-table в статическом маршруте?"}',
'[{"id":"a","text":"To point to another routing table instead of a next-hop IP, enabling policy-based routing between instances","is_correct":true},{"id":"b","text":"To install the route in multiple routing tables simultaneously","is_correct":false},{"id":"c","text":"To load balance traffic across multiple tables","is_correct":false},{"id":"d","text":"To create a recursive route lookup within the same table","is_correct":false}]',
'{"ru": [{"id":"a","text":"Указывать на другую таблицу маршрутизации для policy-based routing"},{"id":"b","text":"Устанавливать маршрут в несколько таблиц"},{"id":"c","text":"Балансировать трафик между таблицами"},{"id":"d","text":"Создавать рекурсивный поиск в той же таблице"}]}',
'next-table resolves next-hop by looking up destination in another routing table. Used for multi-instance forwarding.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/routing-policy/'],
'Routing Fundamentals — Static Routes', 6.0, TRUE),

-- Q46: Auto-configuration recovery
('c0000000-0000-0000-0000-000000000060', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'troubleshoot',
'You lost management access after committing a firewall filter change on Junos. What is the BEST recovery method?',
'{"ru": "Вы потеряли управление после commit изменений firewall filter. Какой метод восстановления ЛУЧШИЙ?"}',
'[{"id":"a","text":"Reboot, interrupt boot to single-user mode, rollback configuration","is_correct":true},{"id":"b","text":"Use console to login with default credentials","is_correct":false},{"id":"c","text":"Power cycle — it will auto-load rescue configuration","is_correct":false},{"id":"d","text":"Contact JTAC to remotely restore access","is_correct":false}]',
'{"ru": [{"id":"a","text":"Перезагрузить, прервать загрузку, откатить конфигурацию"},{"id":"b","text":"Войти через консоль с данными по умолчанию"},{"id":"c","text":"Перезагрузить — загрузится rescue config"},{"id":"d","text":"Связаться с JTAC для удаленного восстановления"}]}',
'Physical access + reboot + interrupt boot + rollback. Prevention: use commit confirmed.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli/'],
'Troubleshooting — Recovery', 8.0, TRUE),

-- Q47: PFE
('c0000000-0000-0000-0000-000000000061', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand',
'Which Junos component forwards packets at high speed?',
'{"ru": "Какой компонент Junos отвечает за высокоскоростную пересылку?"}',
'[{"id":"a","text":"PFE (Packet Forwarding Engine)","is_correct":true},{"id":"b","text":"RE (Routing Engine)","is_correct":false},{"id":"c","text":"Control Board","is_correct":false},{"id":"d","text":"IOC (Input Output Card)","is_correct":false}]',
'{"ru": [{"id":"a","text":"PFE (Packet Forwarding Engine)"},{"id":"b","text":"RE (Routing Engine)"},{"id":"c","text":"Control Board"},{"id":"d","text":"IOC (Input Output Card)"}]}',
'PFE handles hardware-based forwarding. RE handles control plane (routing, management).',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/junos-overview/'],
'Junos OS Architecture — PFE', 8.0, TRUE),

-- Q48: Multiple-choice CLI filters
('c0000000-0000-0000-0000-000000000062', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'multiple-choice', 2, 'understand',
'Which are valid Junos CLI pipe filters? (Select TWO)',
'{"ru": "Какие фильтры CLI Junos допустимы? (Выберите ДВА)"}',
'[{"id":"a","text":"| match — show lines containing pattern","is_correct":true},{"id":"b","text":"| except — show lines NOT containing pattern","is_correct":true},{"id":"c","text":"| find and count together as one filter","is_correct":false},{"id":"d","text":"| save to filter by MAC address","is_correct":false}]',
'{"ru": [{"id":"a","text":"| match — показать строки с шаблоном"},{"id":"b","text":"| except — показать строки без шаблона"},{"id":"c","text":"| find и count вместе"},{"id":"d","text":"| save для фильтрации по MAC"}]}',
'Junos pipe: match, except, find, count, display set, display xml, last, hold.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli/'],
'Junos CLI', 8.0, TRUE),

-- Q49: Routing instances
('c0000000-0000-0000-0000-000000000063', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 4, 'understand',
'In Junos, what is a routing instance type virtual-router?',
'{"ru": "В Junos что такое routing instance типа virtual-router?"}',
'[{"id":"a","text":"Creates separate routing/forwarding tables with own interfaces, independent of inet.0","is_correct":true},{"id":"b","text":"Used exclusively for MPLS L3VPN configurations","is_correct":false},{"id":"c","text":"Provides Layer 2 bridging between VLANs","is_correct":false},{"id":"d","text":"Enables multicast routing for video traffic","is_correct":false}]',
'{"ru": [{"id":"a","text":"Создает отдельные таблицы маршрутизации/пересылки со своими интерфейсами"},{"id":"b","text":"Используется только для MPLS L3VPN"},{"id":"c","text":"Обеспечивает L2 мост между VLAN"},{"id":"d","text":"Включает мультикаст-маршрутизацию"}]}',
'virtual-router creates independent routing/forwarding tables for network virtualization.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/routing-instances/'],
'Routing Fundamentals — Routing Instances', 8.0, TRUE),

-- Q50: J-Web
('c0000000-0000-0000-0000-000000000064', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 1, 'remember',
'What is J-Web in the context of Junos?',
'{"ru": "Что такое J-Web в контексте Junos?"}',
'[{"id":"a","text":"A web-based interface for managing and monitoring Junos devices","is_correct":true},{"id":"b","text":"A protocol for web-based routing decisions","is_correct":false},{"id":"c","text":"A Juniper web server for hosting configs","is_correct":false},{"id":"d","text":"An automation tool for web-based config generation","is_correct":false}]',
'{"ru": [{"id":"a","text":"Веб-интерфейс для управления и мониторинга устройств Junos"},{"id":"b","text":"Протокол для веб-маршрутизации"},{"id":"c","text":"Веб-сервер для хранения конфигураций"},{"id":"d","text":"Инструмент для веб-генерации конфигураций"}]}',
'J-Web is the built-in web GUI for Junos. Enable with set system services web-management http.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/j-web/'],
'Junos CLI — J-Web', 4.0, TRUE);

-- Tags for JNCIA-Junos
INSERT INTO question_tags (question_id, technology, protocol) VALUES
    ('c0000000-0000-0000-0000-000000000050', 'OSI Model', 'General'),
    ('c0000000-0000-0000-0000-000000000051', 'IPv4 Subnetting', 'IPv4'),
    ('c0000000-0000-0000-0000-000000000052', 'Junos HA', 'GRES'),
    ('c0000000-0000-0000-0000-000000000053', 'User Management', 'SSH'),
    ('c0000000-0000-0000-0000-000000000054', 'Junos Architecture', 'General'),
    ('c0000000-0000-0000-0000-000000000055', 'Interface Configuration', 'Ethernet'),
    ('c0000000-0000-0000-0000-000000000056', 'Operational Monitoring', 'General'),
    ('c0000000-0000-0000-0000-000000000057', 'Rescue Configuration', 'General'),
    ('c0000000-0000-0000-0000-000000000058', 'IS-IS', 'IS-IS'),
    ('c0000000-0000-0000-0000-000000000059', 'Static Routing', 'IPv4'),
    ('c0000000-0000-0000-0000-000000000060', 'Recovery', 'General'),
    ('c0000000-0000-0000-0000-000000000061', 'PFE', 'General'),
    ('c0000000-0000-0000-0000-000000000062', 'CLI', 'General'),
    ('c0000000-0000-0000-0000-000000000063', 'Routing Instances', 'General'),
    ('c0000000-0000-0000-0000-000000000064', 'J-Web', 'HTTP');

-- ═══════════════════════════════════════
-- 5. NEW QUESTIONS: CCNA (200-301)
-- ═══════════════════════════════════════

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, body_translations, options, options_translations, explanation, reference_urls, blueprint_section, blueprint_weight, is_active) VALUES

-- Q36: DHCP
('c0000000-0000-0000-0000-000000000070', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'understand',
'What does DHCP DORA stand for?',
'{"ru": "Что означает DORA в DHCP?"}',
'[{"id":"a","text":"Discovery, Offer, Request, Acknowledgment","is_correct":true},{"id":"b","text":"Dynamic Open Routing Algorithm","is_correct":false},{"id":"c","text":"Data Overload Recovery Application","is_correct":false},{"id":"d","text":"Domain Offer Request Assignment","is_correct":false}]',
'{"ru": [{"id":"a","text":"Discovery, Offer, Request, Acknowledgment"},{"id":"b","text":"Dynamic Open Routing Algorithm"},{"id":"c","text":"Data Overload Recovery Application"},{"id":"d","text":"Domain Offer Request Assignment"}]}',
'DORA: Discover (client broadcast), Offer (server offers IP), Request (client requests), Acknowledgment (server confirms).',
ARRAY['https://www.cisco.com/c/en/us/support/docs/ip/dynamic-address-allocation-resolution/'],
'IP Services — DHCP', 8.0, TRUE),

-- Q37: NAT
('c0000000-0000-0000-0000-000000000071', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 3, 'apply',
'Configure static NAT on a Cisco router: map public IP 203.0.113.10 to private 192.168.1.100.',
'{"ru": "Настройте статический NAT на Cisco: public 203.0.113.10 на private 192.168.1.100."}',
'[{"id":"a","text":"ip nat inside source static 192.168.1.100 203.0.113.10","is_correct":true},{"id":"b","text":"ip nat static 192.168.1.100 203.0.113.10","is_correct":false},{"id":"c","text":"nat inside source static 192.168.1.100 203.0.113.10","is_correct":false},{"id":"d","text":"ip static nat 203.0.113.10 192.168.1.100","is_correct":false}]',
'{"ru": [{"id":"a","text":"ip nat inside source static 192.168.1.100 203.0.113.10"},{"id":"b","text":"ip nat static 192.168.1.100 203.0.113.10"},{"id":"c","text":"nat inside source static 192.168.1.100 203.0.113.10"},{"id":"d","text":"ip static nat 203.0.113.10 192.168.1.100"}]}',
'Also configure ip nat inside/outside on interfaces. Creates permanent one-to-one mapping.',
ARRAY['https://www.cisco.com/c/en/us/support/docs/ip/network-address-translation-nat/'],
'IP Services — NAT', 8.0, TRUE),

-- Q38: VLAN Trunking
('c0000000-0000-0000-0000-000000000072', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'understand',
'Which Cisco IOS command configures an interface as 802.1Q trunk?',
'{"ru": "Какая команда Cisco IOS настраивает trunk 802.1Q?"}',
'[{"id":"a","text":"switchport mode trunk","is_correct":true},{"id":"b","text":"trunk mode on","is_correct":false},{"id":"c","text":"set interface trunk","is_correct":false},{"id":"d","text":"port trunk mode enable","is_correct":false}]',
'{"ru": [{"id":"a","text":"switchport mode trunk"},{"id":"b","text":"trunk mode on"},{"id":"c","text":"set interface trunk"},{"id":"d","text":"port trunk mode enable"}]}',
'switchport mode trunk + switchport trunk allowed vlan <vlan-list>. Use switchport nonegotiate to disable DTP.',
ARRAY['https://www.cisco.com/c/en/us/support/docs/lan-switching/vlan/'],
'Network Access — VLAN Trunking', 8.0, TRUE),

-- Q39: EtherChannel
('c0000000-0000-0000-0000-000000000073', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 3, 'remember',
'Which Cisco IOS command shows the EtherChannel load-balancing method?',
'{"ru": "Какая команда Cisco IOS показывает метод балансировки EtherChannel?"}',
'[{"id":"a","text":"show etherchannel load-balance","is_correct":true},{"id":"b","text":"show port-channel load-balance","is_correct":false},{"id":"c","text":"show lacp load-balance","is_correct":false},{"id":"d","text":"show interfaces load-balance","is_correct":false}]',
'{"ru": [{"id":"a","text":"show etherchannel load-balance"},{"id":"b","text":"show port-channel load-balance"},{"id":"c","text":"show lacp load-balance"},{"id":"d","text":"show interfaces load-balance"}]}',
'Methods: src-ip, dst-ip, src-dst-ip, src-mac, dst-mac, src-dst-mac. Default is src-dst-ip.',
ARRAY['https://www.cisco.com/c/en/us/support/docs/lan-switching/etherchannel/'],
'Network Access — EtherChannel', 6.0, TRUE),

-- Q40: OSPF DR/BDR
('c0000000-0000-0000-0000-000000000074', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 3, 'apply',
'Which OSPF network type requires a DR/BDR election?',
'{"ru": "Какой тип сети OSPF требует выбора DR/BDR?"}',
'[{"id":"a","text":"Broadcast (Ethernet)","is_correct":true},{"id":"b","text":"Point-to-Point","is_correct":false},{"id":"c","text":"Point-to-Multipoint","is_correct":false},{"id":"d","text":"Loopback","is_correct":false}]',
'{"ru": [{"id":"a","text":"Broadcast (Ethernet)"},{"id":"b","text":"Point-to-Point"},{"id":"c","text":"Point-to-Multipoint"},{"id":"d","text":"Loopback"}]}',
'DR/BDR election on broadcast networks only. Highest priority (default 1), then highest Router ID.',
ARRAY['https://www.cisco.com/c/en/us/support/docs/ip/open-shortest-path-first-ospf/'],
'IP Connectivity — OSPF', 8.0, TRUE),

-- Q41: FHRP
('c0000000-0000-0000-0000-000000000075', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 3, 'understand',
'What is the primary difference between HSRP and VRRP?',
'{"ru": "В чем основное различие между HSRP и VRRP?"}',
'[{"id":"a","text":"HSRP is Cisco proprietary; VRRP is IEEE open standard (RFC 5798)","is_correct":true},{"id":"b","text":"HSRP supports only IPv6; VRRP only IPv4","is_correct":false},{"id":"c","text":"VRRP requires a license; HSRP is free","is_correct":false},{"id":"d","text":"HSRP uses multicast 224.0.0.18; VRRP uses broadcast","is_correct":false}]',
'{"ru": [{"id":"a","text":"HSRP — проприетарный Cisco; VRRP — открытый стандарт IEEE (RFC 5798)"},{"id":"b","text":"HSRP только IPv6; VRRP только IPv4"},{"id":"c","text":"VRRP требует лицензию; HSRP бесплатный"},{"id":"d","text":"HSRP использует 224.0.0.18; VRRP broadcast"}]}',
'HSRP: active/standby, virtual MAC 0000.0c07.acXX. VRRP: master/backup, uses physical MAC of master.',
ARRAY['https://www.cisco.com/c/en/us/support/docs/ip/hot-standby-router-protocol-hsrp/'],
'IP Services — FHRP', 8.0, TRUE),

-- Q42: Port Security
('c0000000-0000-0000-0000-000000000076', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'apply',
'Which command enables port security on a Cisco switch and limits MAC addresses to 2?',
'{"ru": "Какая команда включает port security и ограничивает MAC до 2?"}',
'[{"id":"a","text":"switchport port-security maximum 2","is_correct":true},{"id":"b","text":"port-security max-mac 2","is_correct":false},{"id":"c","text":"switchport security limit 2","is_correct":false},{"id":"d","text":"mac-address-table limit 2 interface","is_correct":false}]',
'{"ru": [{"id":"a","text":"switchport port-security maximum 2"},{"id":"b","text":"port-security max-mac 2"},{"id":"c","text":"switchport security limit 2"},{"id":"d","text":"mac-address-table limit 2 interface"}]}',
'Also need switchport port-security. Violation modes: protect/restrict/shutdown. Default: shutdown (err-disable).',
ARRAY['https://www.cisco.com/c/en/us/support/docs/security/port-security/'],
'Security Fundamentals — Port Security', 6.0, TRUE),

-- Q43: RESTCONF
('c0000000-0000-0000-0000-000000000077', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'remember',
'Which protocol is commonly used with RESTCONF for network device configuration?',
'{"ru": "Какой протокол используется с RESTCONF для конфигурации устройств?"}',
'[{"id":"a","text":"HTTP/HTTPS (RESTful API calls)","is_correct":true},{"id":"b","text":"SNMP GET/SET requests","is_correct":false},{"id":"c","text":"SSH directly for CLI commands","is_correct":false},{"id":"d","text":"Telnet for automated scripting","is_correct":false}]',
'{"ru": [{"id":"a","text":"HTTP/HTTPS (RESTful API вызовы)"},{"id":"b","text":"SNMP GET/SET запросы"},{"id":"c","text":"SSH для CLI-команд"},{"id":"d","text":"Telnet для скриптов"}]}',
'RESTCONF uses HTTP (GET/POST/PUT/PATCH/DELETE) with YANG data models, returns XML/JSON. NETCONF uses SSH port 830.',
ARRAY['https://www.cisco.com/c/en/us/support/docs/software-programmability/'],
'Automation — RESTCONF', 6.0, TRUE);

-- Tags for CCNA questions
INSERT INTO question_tags (question_id, technology, protocol) VALUES
    ('c0000000-0000-0000-0000-000000000070', 'DHCP', 'DHCP'),
    ('c0000000-0000-0000-0000-000000000071', 'NAT', 'NAT'),
    ('c0000000-0000-0000-0000-000000000072', 'VLAN', '802.1Q'),
    ('c0000000-0000-0000-0000-000000000073', 'EtherChannel', 'LACP'),
    ('c0000000-0000-0000-0000-000000000074', 'OSPF', 'OSPF'),
    ('c0000000-0000-0000-0000-000000000075', 'FHRP', 'HSRP and VRRP'),
    ('c0000000-0000-0000-0000-000000000076', 'Port Security', 'Security'),
    ('c0000000-0000-0000-0000-000000000077', 'RESTCONF', 'HTTP');

-- ═══════════════════════════════════════
-- 6. NEW QUESTIONS: JNCIA-SP (JN0-201)
-- ═══════════════════════════════════════

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, body_translations, options, options_translations, explanation, reference_urls, blueprint_section, blueprint_weight, is_active) VALUES

('c0000000-0000-0000-0000-000000000080', 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'single-choice', 3, 'understand',
'What address family is used for IPv6 BGP peering in Junos?',
'{"ru": "Какое address family используется для IPv6 BGP-пиринга в Junos?"}',
'[{"id":"a","text":"inet6","is_correct":true},{"id":"b","text":"inet","is_correct":false},{"id":"c","text":"iso","is_correct":false},{"id":"d","text":"mpls","is_correct":false}]',
'{"ru": [{"id":"a","text":"inet6"},{"id":"b","text":"inet"},{"id":"c","text":"iso"},{"id":"d","text":"mpls"}]}',
'MP-BGP uses inet6 for IPv6 unicast. Configure: set protocols bgp group <name> family inet6 unicast.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/bgp/'],
'BGP — IPv6', 10.0, TRUE),

('c0000000-0000-0000-0000-000000000081', 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'single-choice', 4, 'understand',
'What is the purpose of a BGP Route Reflector?',
'{"ru": "Какова цель BGP Route Reflector?"}',
'[{"id":"a","text":"To reduce IBGP sessions by reflecting routes from one IBGP peer to other IBGP peers","is_correct":true},{"id":"b","text":"To reflect EBGP routes back to the originating AS","is_correct":false},{"id":"c","text":"To provide encryption for BGP sessions","is_correct":false},{"id":"d","text":"To summarize BGP routes before advertisement","is_correct":false}]',
'{"ru": [{"id":"a","text":"Уменьшить IBGP-сессии, отражая маршруты между IBGP-пирами"},{"id":"b","text":"Отражать EBGP-маршруты обратно в исходную AS"},{"id":"c","text":"Шифрование BGP-сессий"},{"id":"d","text":"Суммировать BGP-маршруты"}]}',
'Route Reflector breaks full-mesh IBGP requirement. Rule: reflect client->all, non-client->clients, always reflect EBGP.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/bgp/'],
'BGP — Route Reflector', 12.0, TRUE),

('c0000000-0000-0000-0000-000000000082', 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'single-choice', 4, 'understand',
'In MPLS L3VPN, what is the purpose of the Route Distinguisher (RD)?',
'{"ru": "В MPLS L3VPN какова цель Route Distinguisher (RD)?"}',
'[{"id":"a","text":"To make globally unique IPv4 prefixes that may overlap between customers","is_correct":true},{"id":"b","text":"To distinguish between EBGP and IBGP routes","is_correct":false},{"id":"c","text":"To set the MPLS label value for a VPN route","is_correct":false},{"id":"d","text":"To determine VPN membership using RT import/export","is_correct":false}]',
'{"ru": [{"id":"a","text":"Сделать уникальными IPv4-префиксы, перекрывающиеся между клиентами"},{"id":"b","text":"Различать EBGP и IBGP маршруты"},{"id":"c","text":"Устанавливать MPLS-метку для VPN-маршрута"},{"id":"d","text":"Определять членство в VPN через RT"}]}',
'RD (8 bytes) + IPv4 prefix = unique VPNv4 prefix. RT controls VPN membership via import/export policies.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/mpls/'],
'MPLS L3VPN', 12.0, TRUE);

INSERT INTO question_tags (question_id, technology, protocol) VALUES
    ('c0000000-0000-0000-0000-000000000080', 'BGP IPv6', 'BGP'),
    ('c0000000-0000-0000-0000-000000000081', 'Route Reflector', 'BGP'),
    ('c0000000-0000-0000-0000-000000000082', 'MPLS L3VPN', 'MPLS');

-- ═══════════════════════════════════════
-- 7. SEED QUESTIONS: JNCIA-SEC (JN0-230)
-- ═══════════════════════════════════════

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, body_translations, options, options_translations, explanation, reference_urls, blueprint_section, blueprint_weight, is_active) VALUES

('c0000000-0000-0000-0000-000000000090', 'b0000000-0000-0000-0000-000000000020', 'a0000000-0000-0000-0000-000000000003', 'single-choice', 2, 'remember',
'On Junos SRX, what is the difference between a security policy and a firewall filter?',
'{"ru": "На SRX в чем разница между security policy и firewall filter?"}',
'[{"id":"a","text":"Security policies are stateful (track session state); filters are stateless (process each packet)","is_correct":true},{"id":"b","text":"Security policies apply to routing; filters apply to forwarding","is_correct":false},{"id":"c","text":"Firewall filters are stateful; security policies are stateless","is_correct":false},{"id":"d","text":"There is no difference; terms are interchangeable","is_correct":false}]',
'{"ru": [{"id":"a","text":"Security policies — stateful; firewall filters — stateless"},{"id":"b","text":"Security policies для маршрутизации; filters для пересылки"},{"id":"c","text":"Firewall filters — stateful; policies — stateless"},{"id":"d","text":"Нет разницы"}]}',
'Security policies are stateful (first-packet inspection, session tracking). Filters are stateless (every packet evaluated). Both can coexist on SRX.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/security-policies/'],
'Security Policies', 10.0, TRUE),

('c0000000-0000-0000-0000-000000000091', 'b0000000-0000-0000-0000-000000000020', 'a0000000-0000-0000-0000-000000000003', 'single-choice', 3, 'understand',
'Which phase of IPsec IKE establishes the ISAKMP Security Association?',
'{"ru": "Какая фаза IKE устанавливает ISAKMP SA?"}',
'[{"id":"a","text":"Phase 1 — establishes secure IKE control channel","is_correct":true},{"id":"b","text":"Phase 2 — establishes IPsec data tunnel","is_correct":false},{"id":"c","text":"Phase 3 — key regeneration","is_correct":false},{"id":"d","text":"Main mode — establishes only data plane","is_correct":false}]',
'{"ru": [{"id":"a","text":"Фаза 1 — защищенный канал управления IKE"},{"id":"b","text":"Фаза 2 — туннель данных IPsec"},{"id":"c","text":"Фаза 3 — регенерация ключей"},{"id":"d","text":"Main mode — только плоскость данных"}]}',
'IKE Phase 1 establishes ISAKMP SA with DH key exchange. Uses Main Mode (6 messages) or Aggressive Mode (3 messages). Phase 2 establishes IPsec SA.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/vpn/'],
'IPsec VPN', 12.0, TRUE),

('c0000000-0000-0000-0000-000000000092', 'b0000000-0000-0000-0000-000000000020', 'a0000000-0000-0000-0000-000000000003', 'single-choice', 2, 'apply',
'Which configuration defines a security zone and assigns an interface on SRX?',
'{"ru": "Какая конфигурация определяет security zone на SRX?"}',
'[{"id":"a","text":"set security zones security-zone trust interfaces ge-0/0/1.0","is_correct":true},{"id":"b","text":"set interfaces ge-0/0/1 security-zone trust","is_correct":false},{"id":"c","text":"set zone trust member ge-0/0/1","is_correct":false},{"id":"d","text":"set security zone trust interface ge-0/0/1","is_correct":false}]',
'{"ru": [{"id":"a","text":"set security zones security-zone trust interfaces ge-0/0/1.0"},{"id":"b","text":"set interfaces ge-0/0/1 security-zone trust"},{"id":"c","text":"set zone trust member ge-0/0/1"},{"id":"d","text":"set security zone trust interface ge-0/0/1"}]}',
'Correct hierarchy: security zones security-zone <name> interfaces <interface>. Intra-zone allowed by default, inter-zone requires policy.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/security-policies/'],
'Security Zones', 8.0, TRUE);

INSERT INTO question_tags (question_id, technology, protocol) VALUES
    ('c0000000-0000-0000-0000-000000000090', 'SRX Security', 'Security'),
    ('c0000000-0000-0000-0000-000000000091', 'IPsec', 'IKE'),
    ('c0000000-0000-0000-0000-000000000092', 'SRX Zones', 'Security');

-- ═══════════════════════════════════════
-- 8. SEED QUESTIONS: JNCIA-DC (JN0-480)
-- ═══════════════════════════════════════

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, body_translations, options, options_translations, explanation, reference_urls, blueprint_section, blueprint_weight, is_active) VALUES

('c0000000-0000-0000-0000-000000000100', 'b0000000-0000-0000-0000-000000000021', 'a0000000-0000-0000-0000-000000000004', 'single-choice', 3, 'understand',
'What is the purpose of VXLAN in a data center network?',
'{"ru": "Какова цель VXLAN в ЦОД?"}',
'[{"id":"a","text":"To create L2 overlay networks over L3 underlay using MAC-in-UDP encapsulation","is_correct":true},{"id":"b","text":"To replace Spanning Tree with faster convergence","is_correct":false},{"id":"c","text":"To encrypt data center traffic","is_correct":false},{"id":"d","text":"To enable IPv6 routing in the DC","is_correct":false}]',
'{"ru": [{"id":"a","text":"L2 оверлей поверх L3 underlay с MAC-in-UDP инкапсуляцией"},{"id":"b","text":"Заменить STP"},{"id":"c","text":"Шифровать трафик"},{"id":"d","text":"Включить IPv6"}]}',
'VXLAN: MAC-in-UDP (port 4789), extends VLAN ID from 12-bit to 24-bit (16M VNIs). EVPN is control plane for VXLAN.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/evpn-vxlan/'],
'EVPN-VXLAN', 15.0, TRUE),

('c0000000-0000-0000-0000-000000000101', 'b0000000-0000-0000-0000-000000000021', 'a0000000-0000-0000-0000-000000000004', 'single-choice', 2, 'remember',
'What is a Juniper QFX series switch designed for?',
'{"ru": "Для чего предназначен коммутатор Juniper QFX?"}',
'[{"id":"a","text":"High-performance data center switching with low latency","is_correct":true},{"id":"b","text":"Service provider edge routing","is_correct":false},{"id":"c","text":"Branch office security appliance","is_correct":false},{"id":"d","text":"Wireless LAN controller","is_correct":false}]',
'{"ru": [{"id":"a","text":"Высокопроизводительные коммутаторы ЦОД"},{"id":"b","text":"Провайдерская маршрутизация"},{"id":"c","text":"Устройство безопасности для филиалов"},{"id":"d","text":"Контроллер WLAN"}]}',
'QFX series: high-density 10/25/40/100GbE, low latency, EVPN-VXLAN, MC-LAG. Purpose-built for data center.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/interfaces/'],
'Data Center Switching', 10.0, TRUE);

INSERT INTO question_tags (question_id, technology, protocol) VALUES
    ('c0000000-0000-0000-0000-000000000100', 'VXLAN', 'VXLAN'),
    ('c0000000-0000-0000-0000-000000000101', 'QFX', 'Ethernet');

-- ═══════════════════════════════════════
-- 9. SEED QUESTIONS: JNCIA-DevOps (JN0-223)
-- ═══════════════════════════════════════

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, body_translations, options, options_translations, explanation, reference_urls, blueprint_section, blueprint_weight, is_active) VALUES

('c0000000-0000-0000-0000-000000000110', 'b0000000-0000-0000-0000-000000000022', 'a0000000-0000-0000-0000-000000000005', 'single-choice', 2, 'remember',
'What is Juniper PyEZ?',
'{"ru": "Что такое Juniper PyEZ?"}',
'[{"id":"a","text":"A Python library for automating Junos device management and configuration","is_correct":true},{"id":"b","text":"A GUI tool for Junos configuration","is_correct":false},{"id":"c","text":"A protocol for real-time monitoring","is_correct":false},{"id":"d","text":"A replacement for Junos CLI","is_correct":false}]',
'{"ru": [{"id":"a","text":"Библиотека Python для автоматизации Junos"},{"id":"b","text":"GUI для конфигурации Junos"},{"id":"c","text":"Протокол мониторинга"},{"id":"d","text":"Замена CLI Junos"}]}',
'PyEZ (junos-eznc): Python abstraction over NETCONF for Junos automation. from jnpr.junos import Device.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/pyez/'],
'Junos Automation — PyEZ', 12.0, TRUE),

('c0000000-0000-0000-0000-000000000111', 'b0000000-0000-0000-0000-000000000022', 'a0000000-0000-0000-0000-000000000005', 'single-choice', 2, 'understand',
'Which port does NETCONF use by default?',
'{"ru": "Какой порт использует NETCONF?"}',
'[{"id":"a","text":"Port 830 (SSH)","is_correct":true},{"id":"b","text":"Port 22","is_correct":false},{"id":"c","text":"Port 443","is_correct":false},{"id":"d","text":"Port 161","is_correct":false}]',
'{"ru": [{"id":"a","text":"Порт 830 (SSH)"},{"id":"b","text":"Порт 22"},{"id":"c","text":"Порт 443"},{"id":"d","text":"Порт 161"}]}',
'NETCONF (RFC 6241) uses SSH on TCP 830. Enable: set system services netconf ssh. Operations: get, get-config, edit-config, commit.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/netconf/'],
'Automation — NETCONF', 10.0, TRUE),

('c0000000-0000-0000-0000-000000000112', 'b0000000-0000-0000-0000-000000000022', 'a0000000-0000-0000-0000-000000000005', 'single-choice', 3, 'understand',
'What is SLAX in the context of Junos automation?',
'{"ru": "Что такое SLAX в контексте автоматизации Junos?"}',
'[{"id":"a","text":"A scripting language for Junos commit scripts, op scripts, and event scripts","is_correct":true},{"id":"b","text":"A network monitoring protocol","is_correct":false},{"id":"c","text":"A replacement for Ansible in Junos environments","is_correct":false},{"id":"d","text":"A YANG data model compiler","is_correct":false}]',
'{"ru": [{"id":"a","text":"Язык сценариев Junos (commit, op, event scripts)"},{"id":"b","text":"Протокол мониторинга"},{"id":"c","text":"Замена Ansible"},{"id":"d","text":"Компилятор YANG"}]}',
'SLAX: C-like syntax that compiles to XSLT. Used for op scripts, commit scripts, event scripts on Junos.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/automation/'],
'Junos Automation — SLAX', 10.0, TRUE);

INSERT INTO question_tags (question_id, technology, protocol) VALUES
    ('c0000000-0000-0000-0000-000000000110', 'PyEZ', 'NETCONF'),
    ('c0000000-0000-0000-0000-000000000111', 'NETCONF', 'NETCONF'),
    ('c0000000-0000-0000-0000-000000000112', 'SLAX', 'XSLT');
