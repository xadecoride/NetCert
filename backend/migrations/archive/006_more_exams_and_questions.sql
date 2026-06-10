-- +goose Up
-- +goose StatementBegin

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
'IP (Internet Protocol) operates at Layer 3 (Network layer) of the OSI model. It is responsible for logical addressing, routing, and packet forwarding between networks.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/junos-overview/'],
'Networking Fundamentals', 8.0, TRUE),

-- Q37: IPv4 subnetting
('c0000000-0000-0000-0000-000000000051', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'apply',
'What is the subnet mask for /27 prefix length?',
'{"ru": "Какая маска подсети соответствует префиксу /27?"}',
'[{"id":"a","text":"255.255.255.0","is_correct":false},{"id":"b","text":"255.255.255.224","is_correct":true},{"id":"c","text":"255.255.255.192","is_correct":false},{"id":"d","text":"255.255.255.248","is_correct":false}]',
'{"ru": [{"id":"a","text":"255.255.255.0"},{"id":"b","text":"255.255.255.224"},{"id":"c","text":"255.255.255.192"},{"id":"d","text":"255.255.255.248"}]}',
'A /27 prefix means the first 27 bits are network bits. In binary: 11111111.11111111.11111111.11100000 = 255.255.255.224. This provides 30 usable host addresses per subnet (2^(32-27) = 32 total, minus 2 for network and broadcast).',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/junos-overview/'],
'Networking Fundamentals — IPv4', 8.0, TRUE),

-- Q38: Junos RE redundancy
('c0000000-0000-0000-0000-000000000052', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'understand',
'In a Junos dual-RE (Routing Engine) system, what command do you use to perform a graceful switchover?',
'{"ru": "В системе Junos с двумя RE (Routing Engine) какая команда выполняет graceful переключение?"}',
'[{"id":"a","text":"request chassis routing-engine master switch","is_correct":true},{"id":"b","text":"redundancy switchover","is_correct":false},{"id":"c","text":"reload routing-engine slave","is_correct":false},{"id":"d","text":"request system switchover","is_correct":false}]',
'{"ru": [{"id":"a","text":"request chassis routing-engine master switch"},{"id":"b","text":"redundancy switchover"},{"id":"c","text":"reload routing-engine slave"},{"id":"d","text":"request system switchover"}]}',
'The command "request chassis routing-engine master switch" performs a graceful Routing Engine switchover in Junos. Graceful Routing Engine Switchover (GRES) preserves the control plane state and forwarding information during the transition. Both REs must have synchronized configurations and be running the same software version.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/high-availability/'],
'Junos OS Fundamentals — RE', 8.0, TRUE),

-- Q39: Junos user authentication
('c0000000-0000-0000-0000-000000000053', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'apply',
'Which Junos configuration statement creates a local user account with authentication?',
'{"ru": "Какое выражение конфигурации Junos создает локальную учетную запись пользователя с аутентификацией?"}',
'[{"id":"a","text":"set system login user admin class super-user authentication plain-text-password","is_correct":true},{"id":"b","text":"set system user admin password test123","is_correct":false},{"id":"c","text":"set system authentication user admin class super-user","is_correct":false},{"id":"d","text":"set system login class super-user user admin","is_correct":false}]',
'{"ru": [{"id":"a","text":"set system login user admin class super-user authentication plain-text-password"},{"id":"b","text":"set system user admin password test123"},{"id":"c","text":"set system authentication user admin class super-user"},{"id":"d","text":"set system login class super-user user admin"}]}',
'The correct hierarchy is "set system login user <name> class <class> authentication plain-text-password". Junos then prompts for the password. The authentication can also use SSH RSA/DSA keys via "set system login user <name> authentication ssh-rsa \'<key>\'".',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/user-management/'],
'Configuration Basics — User Accounts', 6.0, TRUE),

-- Q40: Forwarding Table
('c0000000-0000-0000-0000-000000000054', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'understand',
'In Junos, what is the difference between the routing table and the forwarding table?',
'{"ru": "В Junos в чем разница между таблицей маршрутизации и таблицей пересылки?"}',
'[{"id":"a","text":"The routing table (route table) contains all routes; the forwarding table (forwarding-table) contains only the active routes used for packet forwarding","is_correct":true},{"id":"b","text":"They are identical; the terms are used interchangeably","is_correct":false},{"id":"c","text":"The forwarding table contains only BGP routes; the routing table contains all routes","is_correct":false},{"id":"d","text":"The routing table is stored on the PFE; the forwarding table on the RE","is_correct":false}]',
'{"ru": [{"id":"a","text":"Таблица маршрутизации содержит все маршруты; таблица пересылки — только активные маршруты для пересылки пакетов"},{"id":"b","text":"Они идентичны; термины взаимозаменяемы"},{"id":"c","text":"Таблица пересылки содержит только BGP-маршруты; таблица маршрутизации — все маршруты"},{"id":"d","text":"Таблица маршрутизации хранится на PFE; таблица пересылки на RE"}]}',
'In Junos, the Routing Engine (RE) maintains the routing table (inet.0, inet6.0, etc.) containing all learned routes. The active (best) routes are installed in the forwarding table, which is then downloaded to the Packet Forwarding Engine (PFE) for hardware-based forwarding. "show route" displays the routing table; "show route forwarding-table" displays the forwarding table.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/junos-overview/'],
'Junos OS Architecture', 10.0, TRUE),

-- Q41: Interface configuration
('c0000000-0000-0000-0000-000000000055', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'apply',
'Which Junos command configures an IP address on interface ge-0/0/1?',
'{"ru": "Какая команда Junos настраивает IP-адрес на интерфейсе ge-0/0/1?"}',
'[{"id":"a","text":"set interfaces ge-0/0/1 unit 0 family inet address 192.168.1.1/24","is_correct":true},{"id":"b","text":"set interface ge-0/0/1 ip address 192.168.1.1 255.255.255.0","is_correct":false},{"id":"c","text":"set interfaces ge-0/0/1 ip 192.168.1.1/24","is_correct":false},{"id":"d","text":"ip address 192.168.1.1 255.255.255.0 interface ge-0/0/1","is_correct":false}]',
'{"ru": [{"id":"a","text":"set interfaces ge-0/0/1 unit 0 family inet address 192.168.1.1/24"},{"id":"b","text":"set interface ge-0/0/1 ip address 192.168.1.1 255.255.255.0"},{"id":"c","text":"set interfaces ge-0/0/1 ip 192.168.1.1/24"},{"id":"d","text":"ip address 192.168.1.1 255.255.255.0 interface ge-0/0/1"}]}',
'Junos uses a hierarchical configuration structure: interfaces → interface-name → unit → family → address. The correct syntax is "set interfaces ge-0/0/1 unit 0 family inet address 192.168.1.1/24". Each interface can have multiple units (logical interfaces), and each unit can have multiple address families (inet, inet6, iso, mpls, etc.).',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/interfaces/'],
'Configuration Basics — Interfaces', 8.0, TRUE),

-- Q42: Monitoring — show interfaces
('c0000000-0000-0000-0000-000000000056', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'remember',
'Which Junos operational command shows interface errors and statistics?',
'{"ru": "Какая операционная команда Junos показывает ошибки и статистику интерфейса?"}',
'[{"id":"a","text":"show interfaces ge-0/0/1 extensive","is_correct":true},{"id":"b","text":"show configuration interfaces ge-0/0/1","is_correct":false},{"id":"c","text":"monitor interface ge-0/0/1","is_correct":false},{"id":"d","text":"show ge-0/0/1 statistics","is_correct":false}]',
'{"ru": [{"id":"a","text":"show interfaces ge-0/0/1 extensive"},{"id":"b","text":"show configuration interfaces ge-0/0/1"},{"id":"c","text":"monitor interface ge-0/0/1"},{"id":"d","text":"show ge-0/0/1 statistics"}]}',
'The "show interfaces ge-0/0/1 extensive" command provides detailed statistics including input/output errors, CRC errors, collisions, giants, runts, and packet counts. "monitor interface" provides real-time traffic display. "show interfaces terse" gives a concise summary.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/interfaces/'],
'Operational Monitoring', 6.0, TRUE),

-- Q43: Junos — rescue configuration
('c0000000-0000-0000-0000-000000000057', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'understand',
'What is the purpose of the rescue configuration in Junos?',
'{"ru": "Какова цель rescue configuration в Junos?"}',
'[{"id":"a","text":"It is a known-good configuration saved to a separate partition that can be loaded if the active configuration fails","is_correct":true},{"id":"b","text":"It is a minimal configuration that allows SSH access only","is_correct":false},{"id":"c","text":"It is an automatic backup created every time a commit is performed","is_correct":false},{"id":"d","text":"It is used to recover from a failed software upgrade","is_correct":false}]',
'{"ru": [{"id":"a","text":"Это заведомо рабочая конфигурация, сохраненная в отдельный раздел, которая может быть загружена при сбое активной конфигурации"},{"id":"b","text":"Это минимальная конфигурация, разрешающая только SSH-доступ"},{"id":"c","text":"Это автоматический backup, создаваемый при каждом commit"},{"id":"d","text":"Это используется для восстановления после неудачного обновления ПО"}]}',
'The rescue configuration is a known-good configuration saved with the "request system configuration rescue save" command. It can be loaded with "rollback rescue" if the active configuration causes problems (e.g., management access is lost). It survives reboots and is stored separately from the regular configuration rollback files.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli/'],
'Junos Configuration Management', 6.0, TRUE),

-- Q44: Dynamic Routing — IS-IS
('c0000000-0000-0000-0000-000000000058', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'understand',
'In IS-IS, which statement is correct about Level 1 and Level 2 routers?',
'{"ru": "В IS-IS какое утверждение верно о маршрутизаторах Level 1 и Level 2?"}',
'[{"id":"a","text":"Level 1 routers route within an area, Level 2 routers route between areas","is_correct":true},{"id":"b","text":"Level 1 routers handle IPv6 only, Level 2 routers handle IPv4 only","is_correct":false},{"id":"c","text":"Level 2 routers only participate in BGP","is_correct":false},{"id":"d","text":"Level 1 routers cannot form adjacencies with Level 2 routers","is_correct":false}]',
'{"ru": [{"id":"a","text":"Маршрутизаторы Level 1 маршрутизируют внутри области, Level 2 — между областями"},{"id":"b","text":"Маршрутизаторы Level 1 работают только с IPv6, Level 2 — только с IPv4"},{"id":"c","text":"Маршрутизаторы Level 2 участвуют только в BGP"},{"id":"d","text":"Маршрутизаторы Level 1 не могут устанавливать смежности с Level 2"}]}',
'IS-IS has a two-level hierarchy. Level 1 routers route within an area (intra-area). Level 2 routers route between areas (inter-area). Level 1-2 routers act as border routers between areas, similar to ABRs in OSPF. A Level 1 router typically has a default route pointing to the nearest Level 1-2 router for inter-area traffic.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/is-is/'],
'Routing Fundamentals — IS-IS', 8.0, TRUE),

-- Q45: Static route with next-table
('c0000000-0000-0000-0000-000000000059', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 4, 'apply',
'In Junos, what is the purpose of the "next-table" option in a static route?',
'{"ru": "В Junos какова цель опции next-table в статическом маршруте?"}',
'[{"id":"a","text":"To point to another routing table instead of a next-hop IP, enabling policy-based routing between routing instances","is_correct":true},{"id":"b","text":"To install the route in multiple routing tables simultaneously","is_correct":false},{"id":"c","text":"To load balance traffic across multiple routing tables","is_correct":false},{"id":"d","text":"To create a recursive route lookup within the same table","is_correct":false}]',
'{"ru": [{"id":"a","text":"Указывать на другую таблицу маршрутизации вместо next-hop IP, реализуя policy-based routing между routing instances"},{"id":"b","text":"Устанавливать маршрут в несколько таблиц маршрутизации одновременно"},{"id":"c","text":"Балансировать трафик между несколькими таблицами маршрутизации"},{"id":"d","text":"Создавать рекурсивный поиск маршрута в той же таблице"}]}',
'The "next-table" option in a static route allows the route to resolve its next-hop by looking up the destination in another routing table. This is commonly used in multi-instance (virtual-router) setups for inter-instance forwarding. Example: "set routing-options static route 0.0.0.0/0 next-table my-instance.inet.0".',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/routing-policy/'],
'Routing Fundamentals — Static Routes', 6.0, TRUE),

-- Q46: Junos — auto-configuration recovery
('c0000000-0000-0000-0000-000000000060', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 3, 'troubleshoot',
'You have lost management access to a Junos device after committing a firewall filter change. What is the BEST recovery method?',
'{"ru": "Вы потеряли управление устройством Junos после commit изменений firewall filter. Какой метод восстановления ЛУЧШИЙ?"}',
'[{"id":"a","text":"Reboot the device and interrupt the boot process to enter single-user mode and rollback the configuration","is_correct":true},{"id":"b","text":"Use the console to login with default credentials","is_correct":false},{"id":"c","text":"Power cycle the device and it will automatically load the rescue configuration","is_correct":false},{"id":"d","text":"Contact JTAC to remotely restore access","is_correct":false}]',
'{"ru": [{"id":"a","text":"Перезагрузить устройство и прервать процесс загрузки для входа в однопользовательский режим и отката конфигурации"},{"id":"b","text":"Использовать консоль для входа с учетными данными по умолчанию"},{"id":"c","text":"Перезагрузить устройство — оно автоматически загрузит rescue configuration"},{"id":"d","text":"Связаться с JTAC для удаленного восстановления доступа"}]}',
'If a filter change blocks management access (SSH, SNMP), the best recovery is: 1) Physical access to console, 2) Reboot the device, 3) Press space during boot to stop auto-boot, 4) Enter recovery mode, 5) Use "rollback 1" or load rescue config, 6) Reboot. Prevention: always use "commit confirmed 5" when making filter changes.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli/'],
'Troubleshooting — Recovery', 8.0, TRUE),

-- Q47: Junos — packet forwarding
('c0000000-0000-0000-0000-000000000061', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 2, 'understand',
'Which Junos component is responsible for forwarding packets at high speed?',
'{"ru": "Какой компонент Junos отвечает за высокоскоростную пересылку пакетов?"}',
'[{"id":"a","text":"PFE (Packet Forwarding Engine)","is_correct":true},{"id":"b","text":"RE (Routing Engine)","is_correct":false},{"id":"c","text":"Control Board","is_correct":false},{"id":"d","text":"IOC (Input Output Card)","is_correct":false}]',
'{"ru": [{"id":"a","text":"PFE (Packet Forwarding Engine)"},{"id":"b","text":"RE (Routing Engine)"},{"id":"c","text":"Control Board"},{"id":"d","text":"IOC (Input Output Card)"}]}',
'The PFE (Packet Forwarding Engine) handles high-speed packet forwarding using ASICs. The RE (Routing Engine) handles control plane functions (routing protocols, management). This separation of control and forwarding planes is a fundamental Junos architecture principle. The RE runs Junos OS; the PFE runs Junos OS Kernel.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/junos-overview/'],
'Junos OS Architecture — PFE', 8.0, TRUE),

-- Q48: Multiple-choice — Junos CLI
('c0000000-0000-0000-0000-000000000062', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'multiple-choice', 2, 'understand',
'Which of the following are valid methods to filter the output of "show" commands in Junos CLI? (Select TWO)',
'{"ru": "Какие из перечисленных являются допустимыми методами фильтрации вывода команд show в CLI Junos? (Выберите ДВА)"}',
'[{"id":"a","text":"Using the pipe with match: show interfaces terse | match ge-","is_correct":true},{"id":"b","text":"Using the pipe with except: show interfaces terse | except fxp","is_correct":true},{"id":"c","text":"Using the pipe with find and count together","is_correct":false},{"id":"d","text":"Using the pipe with save to filter by MAC address","is_correct":false}]',
'{"ru": [{"id":"a","text":"Использование | match: show interfaces terse | match ge-"},{"id":"b","text":"Использование | except: show interfaces terse | except fxp"},{"id":"c","text":"Использование | find и count вместе"},{"id":"d","text":"Использование | save для фильтрации по MAC-адресу"}]}',
'Junos CLI supports pipe filters including: "match" (show lines containing pattern), "except" (show lines NOT containing pattern), "find" (start display at first match), "count" (count lines), "display set" (show as set commands), "display xml" (show as XML), "last x", "hold", and more.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/cli/'],
'Junos CLI', 8.0, TRUE),

-- Q49: Routing instances
('c0000000-0000-0000-0000-000000000063', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 4, 'understand',
'In Junos, what is a routing instance with type "virtual-router"?',
'{"ru": "В Junos что такое routing instance типа virtual-router?"}',
'[{"id":"a","text":"It creates a separate routing table and forwarding table with its own interfaces, independent of the default inet.0","is_correct":true},{"id":"b","text":"It is used exclusively for MPLS L3VPN configurations","is_correct":false},{"id":"c","text":"It provides Layer 2 bridging between VLANs","is_correct":false},{"id":"d","text":"It enables multicast routing for video traffic","is_correct":false}]',
'{"ru": [{"id":"a","text":"Создает отдельную таблицу маршрутизации и пересылки со своими интерфейсами, независимо от inet.0"},{"id":"b","text":"Используется исключительно для MPLS L3VPN"},{"id":"c","text":"Обеспечивает мост Layer 2 между VLAN"},{"id":"d","text":"Включает мультикаст-маршрутизацию для видео"}]}',
'A "virtual-router" routing instance creates a completely independent routing table (e.g., my-instance.inet.0) and forwarding table. It has its own interfaces, routing protocols, and routing policies. This enables network virtualization where different customers or services can have isolated routing domains on the same physical hardware. Other instance types include: "forwarding", "l3vpn", "vrf", "evpn", "vpls".',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/routing-instances/'],
'Routing Fundamentals — Routing Instances', 8.0, TRUE),

-- Q50: J-Web
('c0000000-0000-0000-0000-000000000064', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'single-choice', 1, 'remember',
'What is J-Web in the context of Junos?',
'{"ru": "Что такое J-Web в контексте Junos?"}',
'[{"id":"a","text":"A web-based interface for managing and monitoring Junos devices","is_correct":true},{"id":"b","text":"A protocol for web-based routing decisions","is_correct":false},{"id":"c","text":"A Juniper-specific web server for hosting configuration files","is_correct":false},{"id":"d","text":"An automation tool for web-based configuration generation","is_correct":false}]',
'{"ru": [{"id":"a","text":"Веб-интерфейс для управления и мониторинга устройств Junos"},{"id":"b","text":"Протокол для веб-маршрутизации"},{"id":"c","text":"Веб-сервер Juniper для хранения конфигураций"},{"id":"d","text":"Инструмент автоматизации для веб-генерации конфигураций"}]}',
'J-Web is the built-in web-based management interface for Junos devices. It provides configuration, monitoring, and troubleshooting capabilities through a graphical interface. It can be enabled with "set system services web-management http". J-Web is included with Junos OS and does not require additional licensing.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/j-web/'],
'Junos CLI — J-Web', 4.0, TRUE);

-- Tags for new JNCIA-Junos questions
INSERT INTO question_tags (question_id, technology, protocol) VALUES
    ('c0000000-0000-0000-0000-000000000050', 'OSI Model', 'General'),
    ('c0000000-0000-0000-0000-000000000051', 'IPv4 Subnetting', 'IPv4'),
    ('c0000000-0000-0000-0000-000000000052', 'Junos HA', 'GRES'),
    ('c0000000-0000-0000-0000-000000000053', 'Junos User Management', 'SSH'),
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
'What is the purpose of the DHCP DORA process?',
'{"ru": "Какова цель процесса DORA в DHCP?"}',
'[{"id":"a","text":"Discovery, Offer, Request, Acknowledgment — the four steps for a client to obtain an IP address","is_correct":true},{"id":"b","text":"Dynamic Open Routing Algorithm — used for OSPF path selection","is_correct":false},{"id":"c","text":"Data Overload Recovery Application — used for network recovery","is_correct":false},{"id":"d","text":"Domain Offer Request Assignment — DNS zone transfer process","is_correct":false}]',
'{"ru": [{"id":"a","text":"Discovery, Offer, Request, Acknowledgment — четыре шага для получения клиентом IP-адреса"},{"id":"b","text":"Dynamic Open Routing Algorithm — используется для выбора пути OSPF"},{"id":"c","text":"Data Overload Recovery Application — используется для восстановления сети"},{"id":"d","text":"Domain Offer Request Assignment — процесс передачи зон DNS"}]}',
'DORA stands for: Discover (client broadcasts to find DHCP server), Offer (server offers an IP), Request (client requests the offered IP), Acknowledgment (server confirms). DHCP uses UDP ports 67 (server) and 68 (client). On Cisco routers, "service dhcp" must be enabled.',
ARRAY['https://www.cisco.com/c/en/us/support/docs/ip/dynamic-address-allocation-resolution/'],
'IP Services — DHCP', 8.0, TRUE),

-- Q37: NAT
('c0000000-0000-0000-0000-000000000071', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 3, 'apply',
'You need to configure static NAT on a Cisco router to map a public IP 203.0.113.10 to a private server at 192.168.1.100. Which configuration achieves this?',
'{"ru": "Вам нужно настроить статический NAT на маршрутизаторе Cisco для отображения публичного IP 203.0.113.10 на сервер 192.168.1.100. Какая конфигурация это реализует?"}',
'[{"id":"a","text":"ip nat inside source static 192.168.1.100 203.0.113.10","is_correct":true},{"id":"b","text":"ip nat static 192.168.1.100 203.0.113.10","is_correct":false},{"id":"c","text":"nat inside source static 192.168.1.100 203.0.113.10","is_correct":false},{"id":"d","text":"ip static nat 203.0.113.10 192.168.1.100","is_correct":false}]',
'{"ru": [{"id":"a","text":"ip nat inside source static 192.168.1.100 203.0.113.10"},{"id":"b","text":"ip nat static 192.168.1.100 203.0.113.10"},{"id":"c","text":"nat inside source static 192.168.1.100 203.0.113.10"},{"id":"d","text":"ip static nat 203.0.113.10 192.168.1.100"}]}',
'The correct command is "ip nat inside source static 192.168.1.100 203.0.113.10". Additionally, the inside interface must be configured with "ip nat inside" and the outside interface with "ip nat outside". Static NAT creates a permanent one-to-one mapping between the private and public address.',
ARRAY['https://www.cisco.com/c/en/us/support/docs/ip/network-address-translation-nat/'],
'IP Services — NAT', 8.0, TRUE),

-- Q38: VLAN Trunking
('c0000000-0000-0000-0000-000000000072', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'understand',
'Which Cisco IOS command configures an interface as an 802.1Q trunk?',
'{"ru": "Какая команда Cisco IOS настраивает интерфейс как trunk 802.1Q?"}',
'[{"id":"a","text":"switchport mode trunk","is_correct":true},{"id":"b","text":"trunk mode on","is_correct":false},{"id":"c","text":"set interface trunk","is_correct":false},{"id":"d","text":"port trunk mode enable","is_correct":false}]',
'{"ru": [{"id":"a","text":"switchport mode trunk"},{"id":"b","text":"trunk mode on"},{"id":"c","text":"set interface trunk"},{"id":"d","text":"port trunk mode enable"}]}',
'The "switchport mode trunk" command sets the interface into permanent trunking mode. DTP (Dynamic Trunking Protocol) negotiation occurs to agree on trunking. For security, "switchport nonegotiate" can be added to disable DTP. To specify allowed VLANs: "switchport trunk allowed vlan 10,20,30".',
ARRAY['https://www.cisco.com/c/en/us/support/docs/lan-switching/vlan/'],
'Network Access — VLAN Trunking', 8.0, TRUE),

-- Q39: EtherChannel load-balancing
('c0000000-0000-0000-0000-000000000073', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 3, 'remember',
'Which Cisco IOS command displays the EtherChannel load-balancing method?',
'{"ru": "Какая команда Cisco IOS отображает метод балансировки нагрузки EtherChannel?"}',
'[{"id":"a","text":"show etherchannel load-balance","is_correct":true},{"id":"b","text":"show port-channel load-balance","is_correct":false},{"id":"c","text":"show lacp load-balance","is_correct":false},{"id":"d","text":"show interfaces load-balance","is_correct":false}]',
'{"ru": [{"id":"a","text":"show etherchannel load-balance"},{"id":"b","text":"show port-channel load-balance"},{"id":"c","text":"show lacp load-balance"},{"id":"d","text":"show interfaces load-balance"}]}',
'The "show etherchannel load-balance" command displays the current load-balancing algorithm for EtherChannel. Common methods include src-ip, dst-ip, src-dst-ip, src-mac, dst-mac, src-dst-mac. The default is typically src-dst-ip on most Cisco switches.',
ARRAY['https://www.cisco.com/c/en/us/support/docs/lan-switching/etherchannel/'],
'Network Access — EtherChannel', 6.0, TRUE),

-- Q40: OSPF network types
('c0000000-0000-0000-0000-000000000074', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 3, 'apply',
'Which OSPF network type requires a DR/BDR election?',
'{"ru": "Какой тип сети OSPF требует выбора DR/BDR?"}',
'[{"id":"a","text":"Broadcast (Ethernet)","is_correct":true},{"id":"b","text":"Point-to-Point","is_correct":false},{"id":"c","text":"Point-to-Multipoint","is_correct":false},{"id":"d","text":"Loopback","is_correct":false}]',
'{"ru": [{"id":"a","text":"Broadcast (Ethernet)"},{"id":"b","text":"Point-to-Point"},{"id":"c","text":"Point-to-Multipoint"},{"id":"d","text":"Loopback"}]}',
'OSPF broadcast networks (Ethernet) require a Designated Router (DR) and Backup Designated Router (BDR) election to reduce adjacencies and LSA flooding. Point-to-point and point-to-multipoint networks do not use DR/BDR. The DR is elected based on highest OSPF priority (default 1), then highest Router ID.',
ARRAY['https://www.cisco.com/c/en/us/support/docs/ip/open-shortest-path-first-ospf/'],
'IP Connectivity — OSPF', 8.0, TRUE),

-- Q41: First Hop Redundancy
('c0000000-0000-0000-0000-000000000075', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 3, 'understand',
'What is the primary difference between HSRP and VRRP?',
'{"ru": "В чем основное различие между HSRP и VRRP?"}',
'[{"id":"a","text":"HSRP is Cisco proprietary; VRRP is an IEEE open standard (RFC 5798)","is_correct":true},{"id":"b","text":"HSRP supports only IPv6; VRRP supports only IPv4","is_correct":false},{"id":"c","text":"VRRP requires a license; HSRP is free","is_correct":false},{"id":"d","text":"HSRP uses multicast 224.0.0.18; VRRP uses broadcast","is_correct":false}]',
'{"ru": [{"id":"a","text":"HSRP — проприетарный протокол Cisco; VRRP — открытый стандарт IEEE (RFC 5798)"},{"id":"b","text":"HSRP поддерживает только IPv6; VRRP — только IPv4"},{"id":"c","text":"VRRP требует лицензию; HSRP бесплатный"},{"id":"d","text":"HSRP использует мультикаст 224.0.0.18; VRRP использует broadcast"}]}',
'HSRP (Hot Standby Router Protocol) is Cisco proprietary, while VRRP (Virtual Router Redundancy Protocol) is an IEEE open standard (RFC 5798). Both provide default gateway redundancy. Key difference: HSRP has an active/standby model with a virtual MAC (0000.0c07.acXX), while VRRP uses the master/backup model and the physical MAC of the master router (unless configured otherwise).',
ARRAY['https://www.cisco.com/c/en/us/support/docs/ip/hot-standby-router-protocol-hsrp/'],
'IP Services — FHRP', 8.0, TRUE),

-- Q42: Security — Port Security
('c0000000-0000-0000-0000-000000000076', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'apply',
'Which command enables port security on a Cisco switch interface and limits the number of learned MAC addresses to 2?',
'{"ru": "Какая команда включает port security на интерфейсе коммутатора Cisco и ограничивает количество изучаемых MAC-адресов до 2?"}',
'[{"id":"a","text":"switchport port-security maximum 2","is_correct":true},{"id":"b","text":"port-security max-mac 2","is_correct":false},{"id":"c","text":"switchport security limit 2","is_correct":false},{"id":"d","text":"mac-address-table limit 2 interface","is_correct":false}]',
'{"ru": [{"id":"a","text":"switchport port-security maximum 2"},{"id":"b","text":"port-security max-mac 2"},{"id":"c","text":"switchport security limit 2"},{"id":"d","text":"mac-address-table limit 2 interface"}]}',
'Port security is configured with "switchport port-security" followed by "switchport port-security maximum <n>". Features include MAC address sticky learning, violation modes (protect/restrict/shutdown), and aging. Default maximum is 1 MAC per port. Violation mode defaults to "shutdown", which err-disables the port.',
ARRAY['https://www.cisco.com/c/en/us/support/docs/security/port-security/'],
'Security Fundamentals — Port Security', 6.0, TRUE),

-- Q43: Automation — REST API
('c0000000-0000-0000-0000-000000000077', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006', 'single-choice', 2, 'remember',
'Which protocol is commonly used with RESTCONF for network device configuration?',
'{"ru": "Какой протокол обычно используется с RESTCONF для конфигурации сетевых устройств?"}',
'[{"id":"a","text":"HTTP/HTTPS (RESTful API calls)","is_correct":true},{"id":"b","text":"SNMP GET/SET requests","is_correct":false},{"id":"c","text":"SSH directly for CLI commands","is_correct":false},{"id":"d","text":"Telnet for automated scripting","is_correct":false}]',
'{"ru": [{"id":"a","text":"HTTP/HTTPS (RESTful API вызовы)"},{"id":"b","text":"SNMP GET/SET запросы"},{"id":"c","text":"SSH напрямую для CLI-команд"},{"id":"d","text":"Telnet для автоматизации скриптов"}]}',
'RESTCONF uses HTTP/HTTPS methods (GET, POST, PUT, PATCH, DELETE) to interact with YANG data models on network devices. It returns data in XML or JSON format. Cisco devices support RESTCONF with the "restconf" feature. NETCONF uses SSH (port 830) as its transport protocol, while RESTCONF uses HTTP/HTTPS.',
ARRAY['https://www.cisco.com/c/en/us/support/docs/software-programmability/'],
'Automation — RESTCONF', 6.0, TRUE);

-- Tags for new CCNA questions
INSERT INTO question_tags (question_id, technology, protocol) VALUES
    ('c0000000-0000-0000-0000-000000000070', 'DHCP', 'DHCP'),
    ('c0000000-0000-0000-0000-000000000071', 'NAT', 'NAT'),
    ('c0000000-0000-0000-0000-000000000072', 'VLAN', '802.1Q'),
    ('c0000000-0000-0000-0000-000000000073', 'EtherChannel', 'LACP'),
    ('c0000000-0000-0000-0000-000000000074', 'OSPF', 'OSPF'),
    ('c0000000-0000-0000-0000-000000000075', 'FHRP', 'HSRP/VRRP'),
    ('c0000000-0000-0000-0000-000000000076', 'Port Security', 'Security'),
    ('c0000000-0000-0000-0000-000000000077', 'RESTCONF', 'HTTP');

-- ═══════════════════════════════════════
-- 6. NEW QUESTIONS: JNCIA-SP (JN0-201)
-- ═══════════════════════════════════════

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, body_translations, options, options_translations, explanation, reference_urls, blueprint_section, blueprint_weight, is_active) VALUES

-- Q38: BGP IPv6
('c0000000-0000-0000-0000-000000000080', 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'single-choice', 3, 'understand',
'What address family is used for IPv6 BGP peering in Junos?',
'{"ru": "Какое address family используется для IPv6 BGP-пиринга в Junos?"}',
'[{"id":"a","text":"inet6","is_correct":true},{"id":"b","text":"inet","is_correct":false},{"id":"c","text":"iso","is_correct":false},{"id":"d","text":"mpls","is_correct":false}]',
'{"ru": [{"id":"a","text":"inet6"},{"id":"b","text":"inet"},{"id":"c","text":"iso"},{"id":"d","text":"mpls"}]}',
'In Junos BGP configuration, the address family "inet6" is used for IPv6 unicast routes. Configuration: "set protocols bgp group <name> family inet6 unicast". For dual-stack, both "family inet" and "family inet6" can be configured. MP-BGP (RFC 4760) uses address family identifiers to distinguish between different network layer protocols.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/bgp/'],
'BGP — IPv6', 10.0, TRUE),

-- Q39: Route Reflector
('c0000000-0000-0000-0000-000000000081', 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'single-choice', 4, 'understand',
'What is the purpose of a BGP Route Reflector?',
'{"ru": "Какова цель BGP Route Reflector?"}',
'[{"id":"a","text":"To reduce the number of IBGP sessions by allowing routes learned from one IBGP peer to be reflected to other IBGP peers","is_correct":true},{"id":"b","text":"To reflect EBGP routes back to the originating AS","is_correct":false},{"id":"c","text":"To provide encryption for BGP sessions","is_correct":false},{"id":"d","text":"To summarize BGP routes before advertisement","is_correct":false}]',
'{"ru": [{"id":"a","text":"Уменьшить количество IBGP-сессий, позволяя отражать маршруты, полученные от одного IBGP-пира, другим IBGP-пирам"},{"id":"b","text":"Отражать EBGP-маршруты обратно в исходную AS"},{"id":"c","text":"Обеспечить шифрование BGP-сессий"},{"id":"d","text":"Суммировать BGP-маршруты перед анонсом"}]}',
'A Route Reflector (RR) breaks the IBGP full-mesh requirement. An RR reflects routes from its clients to other clients and non-clients. In Junos, configure with "set protocols bgp group <name> cluster <cluster-id>" and the "local-address" statement. The RR rule: reflect from client to all peers, reflect from non-client to clients only, and always reflect from EBGP peers.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/bgp/'],
'BGP — Route Reflector', 12.0, TRUE),

-- Q40: L3VPN
('c0000000-0000-0000-0000-000000000082', 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002', 'single-choice', 4, 'understand',
'In MPLS L3VPN, what is the purpose of the Route Distinguisher (RD)?',
'{"ru": "В MPLS L3VPN какова цель Route Distinguisher (RD)?"}',
'[{"id":"a","text":"To make globally unique IPv4 prefixes that may overlap between different customers","is_correct":true},{"id":"b","text":"To distinguish between EBGP and IBGP routes","is_correct":false},{"id":"c","text":"To set the MPLS label value for a VPN route","is_correct":false},{"id":"d","text":"To determine the VPN membership using RT import/export","is_correct":false}]',
'{"ru": [{"id":"a","text":"Сделать глобально уникальными IPv4-префиксы, которые могут перекрываться между разными клиентами"},{"id":"b","text":"Различать EBGP и IBGP маршруты"},{"id":"c","text":"Устанавливать значение MPLS-метки для VPN-маршрута"},{"id":"d","text":"Определять членство в VPN через RT import/export"}]}',
'The Route Distinguisher (RD) is an 8-byte value prepended to IPv4 prefixes to create unique VPNv4 prefixes (96-bit total: RD + prefix). This allows overlapping customer addresses to be unique in the MPLS core. RD format: <ASN>:<nn> or <IP>:<nn>. The Route Target (RT) controls VPN membership via import/export policies, not the RD.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/mpls/'],
'MPLS L3VPN', 12.0, TRUE);

-- Tags for new JNCIA-SP questions
INSERT INTO question_tags (question_id, technology, protocol) VALUES
    ('c0000000-0000-0000-0000-000000000080', 'BGP IPv6', 'BGP'),
    ('c0000000-0000-0000-0000-000000000081', 'Route Reflector', 'BGP'),
    ('c0000000-0000-0000-0000-000000000082', 'MPLS L3VPN', 'MPLS');

-- ═══════════════════════════════════════
-- 7. SEED QUESTIONS: JNCIA-SEC (JN0-230)
-- ═══════════════════════════════════════

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, body_translations, options, options_translations, explanation, reference_urls, blueprint_section, blueprint_weight, is_active) VALUES

-- Q1: SRX Security Policy
('c0000000-0000-0000-0000-000000000090', 'b0000000-0000-0000-0000-000000000020', 'a0000000-0000-0000-0000-000000000003', 'single-choice', 2, 'remember',
'In Junos SRX, what is the difference between a security policy and a firewall filter?',
'{"ru": "В Junos SRX в чем разница между security policy и firewall filter?"}',
'[{"id":"a","text":"Security policies are stateful and track session state; firewall filters are stateless and process individual packets","is_correct":true},{"id":"b","text":"Security policies apply to routing decisions; firewall filters apply to packet forwarding","is_correct":false},{"id":"c","text":"Firewall filters are stateful; security policies are stateless","is_correct":false},{"id":"d","text":"There is no difference; they are interchangeable terms","is_correct":false}]',
'{"ru": [{"id":"a","text":"Security policies — stateful, отслеживают состояние сессий; firewall filters — stateless, обрабатывают отдельные пакеты"},{"id":"b","text":"Security policies применяются к решениям маршрутизации; firewall filters — к пересылке пакетов"},{"id":"c","text":"Firewall filters — stateful; security policies — stateless"},{"id":"d","text":"Нет разницы; термины взаимозаменяемы"}]}',
'SRX security policies are stateful — they track session states (SYN, SYN-ACK, ACK, etc.) and only apply to the first packet of a session. Subsequent packets are forwarded based on the session table. Firewall filters are stateless and evaluate every packet individually. Both can coexist: security policies for stateful inspection and firewall filters for stateless packet filtering.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/security-policies/'],
'Security Policies', 10.0, TRUE),

-- Q2: IPsec
('c0000000-0000-0000-0000-000000000091', 'b0000000-0000-0000-0000-000000000020', 'a0000000-0000-0000-0000-000000000003', 'single-choice', 3, 'understand',
'Which phase of IPsec IKE establishes the ISAKMP Security Association (SA)?',
'{"ru": "Какая фаза IPsec IKE устанавливает ISAKMP Security Association (SA)?"}',
'[{"id":"a","text":"Phase 1 — establishes the secure IKE control channel","is_correct":true},{"id":"b","text":"Phase 2 — establishes the IPsec data tunnel","is_correct":false},{"id":"c","text":"Phase 3 — performs key regeneration","is_correct":false},{"id":"d","text":"Main mode — establishes only the data plane","is_correct":false}]',
'{"ru": [{"id":"a","text":"Фаза 1 — устанавливает защищенный канал управления IKE"},{"id":"b","text":"Фаза 2 — устанавливает туннель данных IPsec"},{"id":"c","text":"Фаза 3 — выполняет регенерацию ключей"},{"id":"d","text":"Main mode — устанавливает только плоскость данных"}]}',
'IKE Phase 1 establishes the ISAKMP SA, an encrypted control channel using Diffie-Hellman key exchange. It uses either Main Mode (6 messages, more secure) or Aggressive Mode (3 messages, faster). Phase 2 (Quick Mode) establishes the IPsec SA for actual data encryption using the keys negotiated in Phase 1.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/vpn/'],
'IPsec VPN', 12.0, TRUE),

-- Q3: SRX Zones
('c0000000-0000-0000-0000-000000000092', 'b0000000-0000-0000-0000-000000000020', 'a0000000-0000-0000-0000-000000000003', 'single-choice', 2, 'apply',
'Which configuration defines a security zone and assigns an interface on an SRX device?',
'{"ru": "Какая конфигурация определяет security zone и назначает интерфейс на устройстве SRX?"}',
'[{"id":"a","text":"set security zones security-zone trust interfaces ge-0/0/1.0","is_correct":true},{"id":"b","text":"set interfaces ge-0/0/1 security-zone trust","is_correct":false},{"id":"c","text":"set zone trust member ge-0/0/1","is_correct":false},{"id":"d","text":"set security zone trust interface ge-0/0/1","is_correct":false}]',
'{"ru": [{"id":"a","text":"set security zones security-zone trust interfaces ge-0/0/1.0"},{"id":"b","text":"set interfaces ge-0/0/1 security-zone trust"},{"id":"c","text":"set zone trust member ge-0/0/1"},{"id":"d","text":"set security zone trust interface ge-0/0/1"}]}',
'The correct hierarchy is "security zones security-zone <name> interfaces <interface>". Zones separate network segments with different trust levels. By default, intra-zone traffic is allowed, inter-zone traffic requires a security policy. Screens (attack detection) can also be applied per zone.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/security-policies/'],
'Security Zones', 8.0, TRUE);

-- Tags for SEC questions
INSERT INTO question_tags (question_id, technology, protocol) VALUES
    ('c0000000-0000-0000-0000-000000000090', 'SRX Security', 'Security'),
    ('c0000000-0000-0000-0000-000000000091', 'IPsec', 'IKE'),
    ('c0000000-0000-0000-0000-000000000092', 'SRX Zones', 'Security');

-- ═══════════════════════════════════════
-- 8. SEED QUESTIONS: JNCIA-DC (JN0-480)
-- ═══════════════════════════════════════

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, body_translations, options, options_translations, explanation, reference_urls, blueprint_section, blueprint_weight, is_active) VALUES

-- Q1: EVPN-VXLAN
('c0000000-0000-0000-0000-000000000100', 'b0000000-0000-0000-0000-000000000021', 'a0000000-0000-0000-0000-000000000004', 'single-choice', 3, 'understand',
'What is the purpose of VXLAN in a data center network?',
'{"ru": "Какова цель VXLAN в сети центра обработки данных?"}',
'[{"id":"a","text":"To create Layer 2 overlay networks over a Layer 3 underlay using MAC-in-UDP encapsulation","is_correct":true},{"id":"b","text":"To replace Spanning Tree Protocol with faster convergence","is_correct":false},{"id":"c","text":"To provide encryption for data center traffic","is_correct":false},{"id":"d","text":"To enable IPv6 routing in the data center","is_correct":false}]',
'{"ru": [{"id":"a","text":"Создавать оверлейные сети Layer 2 поверх underlay Layer 3 с использованием MAC-in-UDP инкапсуляции"},{"id":"b","text":"Заменить STP на более быструю сходимость"},{"id":"c","text":"Обеспечить шифрование трафика ЦОД"},{"id":"d","text":"Включить IPv6-маршрутизацию в ЦОД"}]}',
'VXLAN (Virtual Extensible LAN) creates Layer 2 overlay networks over an IP underlay using MAC-in-UDP encapsulation (UDP port 4789). It extends VLAN IDs from 12-bit (4094 VLANs) to 24-bit (16 million VNIs), enabling massive multi-tenant networks. EVPN is the control plane for VXLAN.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/evpn-vxlan/'],
'EVPN-VXLAN', 15.0, TRUE),

-- Q2: QFX
('c0000000-0000-0000-0000-000000000101', 'b0000000-0000-0000-0000-000000000021', 'a0000000-0000-0000-0000-000000000004', 'single-choice', 2, 'remember',
'What type of device is a Juniper QFX series switch primarily designed for?',
'{"ru": "Для какого применения в первую очередь предназначен коммутатор Juniper QFX?"}',
'[{"id":"a","text":"High-performance data center switching with low latency","is_correct":true},{"id":"b","text":"Service provider edge routing","is_correct":false},{"id":"c","text":"Branch office security appliance","is_correct":false},{"id":"d","text":"Wireless LAN controller","is_correct":false}]',
'{"ru": [{"id":"a","text":"Высокопроизводительные коммутаторы ЦОД с низкой задержкой"},{"id":"b","text":"Провайдерская граничная маршрутизация"},{"id":"c","text":"Устройство безопасности для филиалов"},{"id":"d","text":"Контроллер беспроводной сети"}]}',
'Juniper QFX series switches (QFX5100, QFX5110, QFX5120, QFX5200, QFX10000) are purpose-built for high-performance data center environments. They support high-density 10/25/40/100GbE, low latency cut-through switching, EVPN-VXLAN, MC-LAG, and Junos OS.',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/interfaces/'],
'Data Center Switching', 10.0, TRUE);

-- Tags for DC questions
INSERT INTO question_tags (question_id, technology, protocol) VALUES
    ('c0000000-0000-0000-0000-000000000100', 'VXLAN', 'VXLAN'),
    ('c0000000-0000-0000-0000-000000000101', 'QFX', 'Ethernet');

-- ═══════════════════════════════════════
-- 9. SEED QUESTIONS: JNCIA-DevOps (JN0-223)
-- ═══════════════════════════════════════

INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, body_translations, options, options_translations, explanation, reference_urls, blueprint_section, blueprint_weight, is_active) VALUES

-- Q1: PyEZ
('c0000000-0000-0000-0000-000000000110', 'b0000000-0000-0000-0000-000000000022', 'a0000000-0000-0000-0000-000000000005', 'single-choice', 2, 'remember',
'What is Juniper PyEZ?',
'{"ru": "Что такое Juniper PyEZ?"}',
'[{"id":"a","text":"A Python library for automating Junos device management and configuration","is_correct":true},{"id":"b","text":"A GUI tool for Junos configuration","is_correct":false},{"id":"c","text":"A protocol for real-time device monitoring","is_correct":false},{"id":"d","text":"A replacement for Junos CLI","is_correct":false}]',
'{"ru": [{"id":"a","text":"Библиотека Python для автоматизации управления и конфигурации устройств Junos"},{"id":"b","text":"GUI-инструмент для конфигурации Junos"},{"id":"c","text":"Протокол для мониторинга устройств в реальном времени"},{"id":"d","text":"Замена CLI Junos"}]}',
'PyEZ (junos-eznc) is a Python library that provides an abstraction layer for automating Junos devices. It uses NETCONF (SSH) for communication and provides Pythonic methods for configuration, operational commands, facts retrieval, and software upgrades. Example: "from jnpr.junos import Device; dev = Device(host=\'192.168.1.1\', user=\'admin\')".',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/pyez/'],
'Junos Automation — PyEZ', 12.0, TRUE),

-- Q2: NETCONF
('c0000000-0000-0000-0000-000000000111', 'b0000000-0000-0000-0000-000000000022', 'a0000000-0000-0000-0000-000000000005', 'single-choice', 2, 'understand',
'Which port does NETCONF use by default for SSH-based communication?',
'{"ru": "Какой порт использует NETCONF по умолчанию для SSH-коммуникации?"}',
'[{"id":"a","text":"Port 830","is_correct":true},{"id":"b","text":"Port 22","is_correct":false},{"id":"c","text":"Port 443","is_correct":false},{"id":"d","text":"Port 161","is_correct":false}]',
'{"ru": [{"id":"a","text":"Порт 830"},{"id":"b","text":"Порт 22"},{"id":"c","text":"Порт 443"},{"id":"d","text":"Порт 161"}]}',
'NETCONF (RFC 6241) uses SSH as its transport protocol on TCP port 830. It provides operations like get, get-config, edit-config, copy-config, commit, etc. Schema is defined in YANG models. Enable on Junos with "set system services netconf ssh".',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/netconf/'],
'Automation — NETCONF', 10.0, TRUE),

-- Q3: SLAX
('c0000000-0000-0000-0000-000000000112', 'b0000000-0000-0000-0000-000000000022', 'a0000000-0000-0000-0000-000000000005', 'single-choice', 3, 'understand',
'What is SLAX in the context of Junos automation?',
'{"ru": "Что такое SLAX в контексте автоматизации Junos?"}',
'[{"id":"a","text":"A scripting language for Junos commit scripts, op scripts, and event scripts","is_correct":true},{"id":"b","text":"A network monitoring protocol","is_correct":false},{"id":"c","text":"A replacement for Ansible in Junos environments","is_correct":false},{"id":"d","text":"A YANG data model compiler","is_correct":false}]',
'{"ru": [{"id":"a","text":"Язык сценариев для commit scripts, op scripts и event scripts Junos"},{"id":"b","text":"Протокол мониторинга сети"},{"id":"c","text":"Замена Ansible в средах Junos"},{"id":"d","text":"Компилятор моделей данных YANG"}]}',
'SLAX is an alternative syntax for Junos automation scripts (op scripts, commit scripts, event scripts). It provides a C-like syntax that compiles to XSLT. SLAX scripts can automate operational commands, enforce configuration policies, and react to system events. Example SLAX op script: "match / { <op-script-results> { <output> { call show-command(\'show interfaces\'); } } }".',
ARRAY['https://www.juniper.net/documentation/us/en/software/junos/automation/'],
'Junos Automation — SLAX', 10.0, TRUE);

-- Tags for AUT questions
INSERT INTO question_tags (question_id, technology, protocol) VALUES
    ('c0000000-0000-0000-0000-000000000110', 'PyEZ', 'NETCONF'),
    ('c0000000-0000-0000-0000-000000000111', 'NETCONF', 'NETCONF'),
    ('c0000000-0000-0000-0000-000000000112', 'SLAX', 'XSLT');

-- +goose StatementEnd


-- +goose Down
-- +goose StatementBegin

-- Remove new questions for AUT
DELETE FROM question_tags WHERE question_id IN (
    'c0000000-0000-0000-0000-000000000110','c0000000-0000-0000-0000-000000000111','c0000000-0000-0000-0000-000000000112'
);
DELETE FROM questions WHERE id IN (
    'c0000000-0000-0000-0000-000000000110','c0000000-0000-0000-0000-000000000111','c0000000-0000-0000-0000-000000000112'
);

-- Remove new questions for DC
DELETE FROM question_tags WHERE question_id IN (
    'c0000000-0000-0000-0000-000000000100','c0000000-0000-0000-0000-000000000101'
);
DELETE FROM questions WHERE id IN (
    'c0000000-0000-0000-0000-000000000100','c0000000-0000-0000-0000-000000000101'
);

-- Remove new questions for SEC
DELETE FROM question_tags WHERE question_id IN (
    'c0000000-0000-0000-0000-000000000090','c0000000-0000-0000-0000-000000000091','c0000000-0000-0000-0000-000000000092'
);
DELETE FROM questions WHERE id IN (
    'c0000000-0000-0000-0000-000000000090','c0000000-0000-0000-0000-000000000091','c0000000-0000-0000-0000-000000000092'
);

-- Remove new questions for JNCIA-SP
DELETE FROM question_tags WHERE question_id IN (
    'c0000000-0000-0000-0000-000000000080','c0000000-0000-0000-0000-000000000081','c0000000-0000-0000-0000-000000000082'
);
DELETE FROM questions WHERE id IN (
    'c0000000-0000-0000-0000-000000000080','c0000000-0000-0000-0000-000000000081','c0000000-0000-0000-0000-000000000082'
);

-- Remove new questions for CCNA
DELETE FROM question_tags WHERE question_id IN (
    'c0000000-0000-0000-0000-000000000070','c0000000-0000-0000-0000-000000000071',
    'c0000000-0000-0000-0000-000000000072','c0000000-0000-0000-0000-000000000073',
    'c0000000-0000-0000-0000-000000000074','c0000000-0000-0000-0000-000000000075',
    'c0000000-0000-0000-0000-000000000076','c0000000-0000-0000-0000-000000000077'
);
DELETE FROM questions WHERE id IN (
    'c0000000-0000-0000-0000-000000000070','c0000000-0000-0000-0000-000000000071',
    'c0000000-0000-0000-0000-000000000072','c0000000-0000-0000-0000-000000000073',
    'c0000000-0000-0000-0000-000000000074','c0000000-0000-0000-0000-000000000075',
    'c0000000-0000-0000-0000-000000000076','c0000000-0000-0000-0000-000000000077'
);

-- Remove new questions for JNCIA-Junos
DELETE FROM question_tags WHERE question_id IN (
    'c0000000-0000-0000-0000-000000000050','c0000000-0000-0000-0000-000000000051',
    'c0000000-0000-0000-0000-000000000052','c0000000-0000-0000-0000-000000000053',
    'c0000000-0000-0000-0000-000000000054','c0000000-0000-0000-0000-000000000055',
    'c0000000-0000-0000-0000-000000000056','c0000000-0000-0000-0000-000000000057',
    'c0000000-0000-0000-0000-000000000058','c0000000-0000-0000-0000-000000000059',
    'c0000000-0000-0000-0000-000000000060','c0000000-0000-0000-0000-000000000061',
    'c0000000-0000-0000-0000-000000000062','c0000000-0000-0000-0000-000000000063',
    'c0000000-0000-0000-0000-000000000064'
);
DELETE FROM questions WHERE id IN (
    'c0000000-0000-0000-0000-000000000050','c0000000-0000-0000-0000-000000000051',
    'c0000000-0000-0000-0000-000000000052','c0000000-0000-0000-0000-000000000053',
    'c0000000-0000-0000-0000-000000000054','c0000000-0000-0000-0000-000000000055',
    'c0000000-0000-0000-0000-000000000056','c0000000-0000-0000-0000-000000000057',
    'c0000000-0000-0000-0000-000000000058','c0000000-0000-0000-0000-000000000059',
    'c0000000-0000-0000-0000-000000000060','c0000000-0000-0000-0000-000000000061',
    'c0000000-0000-0000-0000-000000000062','c0000000-0000-0000-0000-000000000063',
    'c0000000-0000-0000-0000-000000000064'
);

-- Remove new exams (AUT, DC, SEC)
DELETE FROM exams WHERE id IN (
    'b0000000-0000-0000-0000-000000000022',
    'b0000000-0000-0000-0000-000000000021',
    'b0000000-0000-0000-0000-000000000020'
);

-- Remove new exams (ENT higher levels)
DELETE FROM exams WHERE id IN (
    'b0000000-0000-0000-0000-000000000011',
    'b0000000-0000-0000-0000-000000000010'
);

-- Revert JNCIA-Junos code to JN0-101
UPDATE exams SET code = 'JN0-101', total_questions = 60 WHERE code = 'JN0-106';

-- +goose StatementEnd
