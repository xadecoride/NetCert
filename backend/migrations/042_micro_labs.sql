-- +goose Up
-- +goose StatementBegin

-- ============================================================
-- Migration 042: Concept Micro-Labs
-- ============================================================
-- Создаёт таблицу микро-лаб и связь с учебными главами (V2).
-- Seed: 5 первых Concept Micro-Labs (L1) для JNCIA уровня.

-- Micro-labs table
CREATE TABLE IF NOT EXISTS micro_labs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    difficulty SMALLINT NOT NULL CHECK (difficulty >= 1 AND difficulty <= 5),
    duration_minutes INT NOT NULL DEFAULT 15,
    level VARCHAR(20) NOT NULL DEFAULT 'JNCIA' CHECK (level IN ('JNCIA', 'JNCIP', 'JNCIE', 'CCNA', 'CCNP', 'CCIE')),
    technology VARCHAR(50) NOT NULL,
    -- Containerlab YAML stored as text
    topology_yaml TEXT NOT NULL,
    -- Initial configs as JSON object: { "r1": "...", "r2": "..." }
    initial_configs JSONB NOT NULL DEFAULT '{}',
    -- Task description in Markdown
    task_description TEXT NOT NULL,
    -- Progressive hints (array of strings, revealed one by one)
    hints TEXT[] DEFAULT '{}',
    -- Solution configs (JSON object with device config keys)
    solution_configs JSONB,
    -- Grading script path (relative to labs directory)
    grading_script_path VARCHAR(200),
    -- Fault injection config for troubleshooting mode
    fault_config JSONB,
    -- Troubleshooting mode flag
    is_troubleshooting BOOLEAN DEFAULT FALSE,
    -- Track reference
    track_id UUID REFERENCES tracks(id) ON DELETE SET NULL,
    -- Path to lab directory on disk
    lab_directory VARCHAR(200) NOT NULL,
    -- Active flag
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Junction table: micro-lab ↔ study chapter (V2 Learning Paths)
-- chapter_id is a plain UUID (no FK constraint) because the chapters table
-- is created in a separate V2 migration. The FK will be added later via:
--   ALTER TABLE chapter_micro_labs ADD CONSTRAINT ... REFERENCES chapters(id);
CREATE TABLE IF NOT EXISTS chapter_micro_labs (
    chapter_id UUID NOT NULL,
    micro_lab_id UUID NOT NULL REFERENCES micro_labs(id) ON DELETE CASCADE,
    sort_order SMALLINT DEFAULT 0,
    is_required BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (chapter_id, micro_lab_id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_micro_labs_technology ON micro_labs(technology);
CREATE INDEX IF NOT EXISTS idx_micro_labs_level ON micro_labs(level);
CREATE INDEX IF NOT EXISTS idx_micro_labs_track_id ON micro_labs(track_id);
CREATE INDEX IF NOT EXISTS idx_chapter_micro_labs_lab_id ON chapter_micro_labs(micro_lab_id);

-- ============================================================
-- SEED DATA: 5 Concept Micro-Labs (L1)
-- ============================================================

-- Track references (using canonical UUIDs from migration 001)
-- a0000000-0000-0000-0000-000000000001 = junos-ent (JNCIA-Junos ENT)

-- Lab 1: JunOS CLI Basics
INSERT INTO micro_labs (
    slug, title, description, difficulty, duration_minutes,
    level, technology, topology_yaml, initial_configs,
    task_description, hints, grading_script_path,
    lab_directory, track_id
) VALUES (
    'junos-cli-basics',
    'JunOS CLI Basics',
    'Освойте базовые команды JunOS CLI: навигация между operational и configuration mode, настройка интерфейсов, проверка connectivity.',
    1, 15,
    'JNCIA', 'junos-cli',
    -- topology_yaml: minified single-line version of clab.yml
    'name: netcert-ml01-cli-basics\ntopology:\n  kinds:\n    juniper_crpd:\n      image: crpd:24.2R1\n      cpu: 1\n      memory: 512M\n  nodes:\n    r1:\n      kind: juniper_crpd\n      mgmt-ipv4: 172.100.1.2\n      env:\n        JUNOS_ROOT_PASSWORD: NetCert123\n    r2:\n      kind: juniper_crpd\n      mgmt-ipv4: 172.100.1.3\n      env:\n        JUNOS_ROOT_PASSWORD: NetCert123\n  links:\n    - endpoints: [\"r1:eth1\", \"r2:eth1\"]',
    -- initial_configs: JSONB
    '{
        "r1": "system { host-name R1; root-authentication { encrypted-password \"$6$...\"; } } interfaces { lo0 { unit 0 { family inet { address 1.1.1.1/32; } } } ge-0/0/0 { unit 0 { family inet { address 10.0.12.1/30; } } } }",
        "r2": "system { host-name R2; root-authentication { encrypted-password \"$6$...\"; } } interfaces { lo0 { unit 0 { family inet { address 2.2.2.2/32; } } } ge-0/0/0 { unit 0 { family inet { address 10.0.12.2/30; } } } }"
    }'::jsonb,
    '## Micro-Lab 01: JunOS CLI Basics\n\n### Tasks\n1. **Explore Operational Mode** — выполните show interfaces terse, show configuration, show version\n2. **Configure Interface Description** — добавьте description к ge-0/0/0 на R1\n3. **Change Hostname** — измените hostname R2 на R2-Core-1\n4. **Verify Connectivity** — ping 10.0.12.2 с R1 (5 пакетов)\n5. **Save Configuration** — сохраните конфиг в /tmp/my-config.txt',
    ARRAY[
        'Используйте `configure` для перехода в configuration mode. Приглашение сменится с > на #.',
        'Для проверки конфигурации без применения: `commit check`.',
        '`commit and-quit` — commit и выход в operational mode.'
    ],
    '01-junos-cli-basics/grade.py',
    'backend/labs/micro-labs/01-junos-cli-basics',
    'a0000000-0000-0000-0000-000000000001'
);

-- Lab 2: OSPF Adjacency
INSERT INTO micro_labs (
    slug, title, description, difficulty, duration_minutes,
    level, technology, topology_yaml, initial_configs,
    task_description, hints, grading_script_path,
    lab_directory, track_id
) VALUES (
    'ospf-adjacency',
    'OSPF Adjacency',
    'Настройте OSPFv2 в Area 0 на трёх роутерах, сформируйте adjacency, проверьте обмен маршрутами и определите DR/BDR.',
    2, 20,
    'JNCIP', 'ospf',
    'name: netcert-ml02-ospf-adjacency\ntopology:\n  kinds:\n    juniper_crpd:\n      image: crpd:24.2R1\n      cpu: 1\n      memory: 512M\n  nodes:\n    r1:\n      kind: juniper_crpd\n      mgmt-ipv4: 172.100.1.2\n      env:\n        JUNOS_ROOT_PASSWORD: NetCert123\n    r2:\n      kind: juniper_crpd\n      mgmt-ipv4: 172.100.1.3\n      env:\n        JUNOS_ROOT_PASSWORD: NetCert123\n    r3:\n      kind: juniper_crpd\n      mgmt-ipv4: 172.100.1.4\n      env:\n        JUNOS_ROOT_PASSWORD: NetCert123\n  links:\n    - endpoints: [\"r1:eth1\", \"r2:eth1\"]\n    - endpoints: [\"r2:eth1\", \"r3:eth1\"]\n    - endpoints: [\"r3:eth1\", \"r1:eth1\"]',
    '{
        "r1": "system { host-name R1; } interfaces { lo0 { unit 0 { family inet { address 1.1.1.1/32; } } } ge-0/0/0 { unit 0 { family inet { address 10.0.12.1/30; } } } ge-0/0/1 { unit 0 { family inet { address 10.0.13.1/30; } } } }",
        "r2": "system { host-name R2; } interfaces { lo0 { unit 0 { family inet { address 2.2.2.2/32; } } } ge-0/0/0 { unit 0 { family inet { address 10.0.12.2/30; } } } ge-0/0/1 { unit 0 { family inet { address 10.0.23.2/30; } } } }",
        "r3": "system { host-name R3; } interfaces { lo0 { unit 0 { family inet { address 3.3.3.3/32; } } } ge-0/0/0 { unit 0 { family inet { address 10.0.23.3/30; } } } ge-0/0/1 { unit 0 { family inet { address 10.0.13.2/30; } } } }"
    }'::jsonb,
    '## Micro-Lab 02: OSPF Adjacency\n\n### Tasks\n1. **OSPF on R1** — set protocols ospf area 0 interface ge-0/0/0.0, ge-0/0/1.0, lo0.0 passive\n2. **OSPF on R2** — то же самое на двух интерфейсах\n3. **OSPF on R3** — то же самое\n4. **Verify Routes** — show route protocol ospf (должны быть 2.2.2.2 и 3.3.3.3)\n5. **DR/BDR** — show ospf neighbor detail\n6. **Ping** — проверьте связность',
    ARRAY[
        'show ospf neighbor — проверьте состояние. Должно быть Full.',
        'Если сосед в Init/ExStart — проверьте IP и MTU.',
        'DR/BDR выбираются на broadcast-сегментах. DR = highest priority, затем highest RID.'
    ],
    '02-ospf-adjacency/grade.py',
    'backend/labs/micro-labs/02-ospf-adjacency',
    'a0000000-0000-0000-0000-000000000001'
);

-- Lab 3: EBGP Peering
INSERT INTO micro_labs (
    slug, title, description, difficulty, duration_minutes,
    level, technology, topology_yaml, initial_configs,
    task_description, hints, grading_script_path,
    lab_directory, track_id
) VALUES (
    'ebgp-peering',
    'EBGP Peering',
    'Настройте EBGP peering между тремя AS (65001, 65002, 65003), настройте экспорт маршрутов через policy и проверьте BGP-таблицу.',
    3, 20,
    'JNCIP', 'bgp',
    'name: netcert-ml03-ebgp-peering\ntopology:\n  kinds:\n    juniper_crpd:\n      image: crpd:24.2R1\n      cpu: 1\n      memory: 512M\n  nodes:\n    r1:\n      kind: juniper_crpd\n      mgmt-ipv4: 172.100.1.2\n      env:\n        JUNOS_ROOT_PASSWORD: NetCert123\n    r2:\n      kind: juniper_crpd\n      mgmt-ipv4: 172.100.1.3\n      env:\n        JUNOS_ROOT_PASSWORD: NetCert123\n    r3:\n      kind: juniper_crpd\n      mgmt-ipv4: 172.100.1.4\n      env:\n        JUNOS_ROOT_PASSWORD: NetCert123\n  links:\n    - endpoints: [\"r1:eth1\", \"r2:eth1\"]\n    - endpoints: [\"r2:eth1\", \"r3:eth1\"]',
    '{
        "r1": "system { host-name R1; } interfaces { lo0 { unit 0 { family inet { address 1.1.1.1/32; } } } ge-0/0/0 { unit 0 { family inet { address 10.0.12.1/30; } } } }",
        "r2": "system { host-name R2; } interfaces { lo0 { unit 0 { family inet { address 2.2.2.2/32; } } } ge-0/0/0 { unit 0 { family inet { address 10.0.12.2/30; } } } ge-0/0/1 { unit 0 { family inet { address 10.0.23.2/30; } } } }",
        "r3": "system { host-name R3; } interfaces { lo0 { unit 0 { family inet { address 3.3.3.3/32; } } } ge-0/0/0 { unit 0 { family inet { address 10.0.23.3/30; } } } }"
    }'::jsonb,
    '## Micro-Lab 03: EBGP Peering\n\n### Tasks\n1. **EBGP R1→R2** — AS65001 to AS65002, peer 10.0.12.2\n2. **EBGP R2→R1 & R2→R3** — два peer-группы на R2\n3. **EBGP R3→R2** — AS65003 to AS65002\n4. **Export Loopbacks** — policy-statement EXPORT-BGP с term LOOPBACK\n5. **Verify** — show bgp summary, show route protocol bgp, ping across AS',
    ARRAY[
        'show bgp summary — проверьте Established vs Active.',
        'BGP не анонсирует маршруты без export policy. Добавьте policy-statement.',
        'AS-path на R1 для 3.3.3.3 должен быть [65002 65003].'
    ],
    '03-ebgp-peering/grade.py',
    'backend/labs/micro-labs/03-ebgp-peering',
    'a0000000-0000-0000-0000-000000000001'
);

-- Lab 4: IS-IS Single-Level
INSERT INTO micro_labs (
    slug, title, description, difficulty, duration_minutes,
    level, technology, topology_yaml, initial_configs,
    task_description, hints, grading_script_path,
    lab_directory, track_id
) VALUES (
    'isis-single-level',
    'IS-IS Single-Level',
    'Настройте IS-IS Level 2 на трёх роутерах, настройте NET (Network Entity Title), сформируйте adjacency и проверьте маршруты.',
    3, 20,
    'JNCIP', 'isis',
    'name: netcert-ml04-isis-single-level\ntopology:\n  kinds:\n    juniper_crpd:\n      image: crpd:24.2R1\n      cpu: 1\n      memory: 512M\n  nodes:\n    r1:\n      kind: juniper_crpd\n      mgmt-ipv4: 172.100.1.2\n      env:\n        JUNOS_ROOT_PASSWORD: NetCert123\n    r2:\n      kind: juniper_crpd\n      mgmt-ipv4: 172.100.1.3\n      env:\n        JUNOS_ROOT_PASSWORD: NetCert123\n    r3:\n      kind: juniper_crpd\n      mgmt-ipv4: 172.100.1.4\n      env:\n        JUNOS_ROOT_PASSWORD: NetCert123\n  links:\n    - endpoints: [\"r1:eth1\", \"r2:eth1\"]\n    - endpoints: [\"r2:eth1\", \"r3:eth1\"]\n    - endpoints: [\"r3:eth1\", \"r1:eth1\"]',
    '{
        "r1": "system { host-name R1; } interfaces { lo0 { unit 0 { family inet { address 1.1.1.1/32; } family iso { address 49.0001.0010.0100.1001.00; } } } ge-0/0/0 { unit 0 { family inet { address 10.0.12.1/30; } family iso; } } ge-0/0/1 { unit 0 { family inet { address 10.0.13.1/30; } family iso; } } }",
        "r2": "system { host-name R2; } interfaces { lo0 { unit 0 { family inet { address 2.2.2.2/32; } family iso { address 49.0001.0020.0200.2002.00; } } } ge-0/0/0 { unit 0 { family inet { address 10.0.12.2/30; } family iso; } } ge-0/0/1 { unit 0 { family inet { address 10.0.23.2/30; } family iso; } } }",
        "r3": "system { host-name R3; } interfaces { lo0 { unit 0 { family inet { address 3.3.3.3/32; } family iso { address 49.0001.0030.0300.3003.00; } } } ge-0/0/0 { unit 0 { family inet { address 10.0.23.3/30; } family iso; } } ge-0/0/1 { unit 0 { family inet { address 10.0.13.2/30; } family iso; } } }"
    }'::jsonb,
    '## Micro-Lab 04: IS-IS Single-Level\n\n### Tasks\n1. **IS-IS on R1** — set protocols isis level 2 + interface ге-0/0/0.0, ге-0/0/1.0, lo0.0 passive\n2. **IS-IS on R2** — то же самое\n3. **IS-IS on R3** — то же самое\n4. **Verify Adjacencies** — show isis adjacency detail (Up)\n5. **Verify Routes** — show route protocol isis, ping',
    ARRAY[
        'IS-IS требует family iso на интерфейсах (уже настроено в initial config).',
        'Все соседи должны быть в одном Level (Level 2).',
        'DIS (Designated IS) — аналог DR в OSPF, выбирается на broadcast-сегментах.'
    ],
    '04-isis-single-level/grade.py',
    'backend/labs/micro-labs/04-isis-single-level',
    'a0000000-0000-0000-0000-000000000001'
);

-- Lab 5: MPLS LSP
INSERT INTO micro_labs (
    slug, title, description, difficulty, duration_minutes,
    level, technology, topology_yaml, initial_configs,
    task_description, hints, grading_script_path,
    lab_directory, track_id
) VALUES (
    'mpls-lsp',
    'MPLS LSP with LDP',
    'Настройте MPLS на трёх роутерах, запустите LDP для автоматического распределения меток и проверьте LSP через MPLS-домен.',
    4, 25,
    'JNCIP', 'mpls',
    'name: netcert-ml05-mpls-lsp\ntopology:\n  kinds:\n    juniper_crpd:\n      image: crpd:24.2R1\n      cpu: 1\n      memory: 512M\n  nodes:\n    pe1:\n      kind: juniper_crpd\n      mgmt-ipv4: 172.100.1.2\n      env:\n        JUNOS_ROOT_PASSWORD: NetCert123\n    p:\n      kind: juniper_crpd\n      mgmt-ipv4: 172.100.1.3\n      env:\n        JUNOS_ROOT_PASSWORD: NetCert123\n    pe2:\n      kind: juniper_crpd\n      mgmt-ipv4: 172.100.1.4\n      env:\n        JUNOS_ROOT_PASSWORD: NetCert123\n  links:\n    - endpoints: [\"pe1:eth1\", \"p:eth1\"]\n    - endpoints: [\"p:eth1\", \"pe2:eth1\"]',
    '{
        "pe1": "system { host-name PE1; } interfaces { lo0 { unit 0 { family inet { address 1.1.1.1/32; } } } ge-0/0/0 { unit 0 { family inet { address 10.0.12.1/30; } family mpls; } } }",
        "p": "system { host-name P; } interfaces { lo0 { unit 0 { family inet { address 2.2.2.2/32; } } } ge-0/0/0 { unit 0 { family inet { address 10.0.12.2/30; } family mpls; } } ge-0/0/1 { unit 0 { family inet { address 10.0.23.2/30; } family mpls; } } }",
        "pe2": "system { host-name PE2; } interfaces { lo0 { unit 0 { family inet { address 3.3.3.3/32; } } } ge-0/0/0 { unit 0 { family inet { address 10.0.23.3/30; } family mpls; } } }"
    }'::jsonb,
    '## Micro-Lab 05: MPLS LSP\n\n### Tasks\n1. **IGP (OSPF)** — настройте OSPF Area 0 на всех\n2. **MPLS** — set protocols mpls interface\n3. **LDP** — set protocols ldp interface на всех\n4. **Verify MPLS** — show mpls lsp, show ldp session\n5. **Verify Labels** — show route 3.3.3.3 (должна быть метка)\n6. **Ping** — проверьте MPLS connectivity',
    ARRAY[
        'Перед MPLS/LDP должен работать IGP (OSPF или IS-IS) для IP-связности.',
        'LDP использует UDP 646 (discovery) и TCP 646 (session).',
        'Ingress LSR = Push, Transit LSR = Swap, Egress LSR = Pop (PHP).'
    ],
    '05-mpls-lsp/grade.py',
    'backend/labs/micro-labs/05-mpls-lsp',
    'a0000000-0000-0000-0000-000000000001'
);

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TABLE IF EXISTS chapter_micro_labs CASCADE;
DROP TABLE IF EXISTS micro_labs CASCADE;
-- +goose StatementEnd
