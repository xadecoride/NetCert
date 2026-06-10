"use client";

import { useState, useEffect, useMemo, useCallback, Suspense } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { useAuth } from "@/lib/auth-context";
import { useTranslation } from "@/lib/i18n/context";
import { tracksApi, studyProgressApi } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";
import AnimatedTerminal from "@/components/AnimatedTerminal";
import { LabTerminal } from "@/components/lab/LabTerminal";
import {
  BookOpen,
  MagnifyingGlass,
  CaretDown,
  Code,
  Network,
  ShieldCheck,
  ComputerTower,
  Cloud,
  Trophy,
  FileText,
  BookmarkSimple,
  Copy,
  Check,
  ArrowsDownUp,
  Command,
  Terminal,
  ArrowLeft,
  Circle,
  CheckCircle,
  Gauge,
} from "@phosphor-icons/react";

// ─── Study Content ───────────────────────────────────────────

interface TechnologyGuide {
  id: string;
  technology: string;
  title: string;
  level: string;
  track: string;
  summary: string;
  sections: GuideSection[];
}

interface GuideSection {
  title: string;
  content: string;
  type: "text" | "code" | "command" | "note" | "tip" | "warning";
}

const technologyGuides: TechnologyGuide[] = [    {
    id: "junos-cli",
    technology: "junos-cli",
    title: "JunOS CLI Basics",
    level: "JNCIA",
    track: "junos-ent",
    summary: "Навигация по JunOS CLI: operational vs configuration mode, команды show, управление конфигурацией.",
    sections: [
      {
        title: "Operational Mode",
        type: "text",
        content:
          "При входе на устройство JunOS вы попадаете в operational mode (приглашение >). Здесь выполняются команды show, ping, traceroute, мониторинг.",
      },
      {
        title: "Переход в Configuration Mode",
        type: "command",
        content: "user@router> configure\nuser@router#",
      },
      {
        title: "Базовые show-команды",
        type: "code",
        content: "show interfaces terse             # Краткая информация об интерфейсах\nshow configuration                # Текущая конфигурация\nshow route                        # Таблица маршрутизации\nshow arp                          # ARP-таблица\nshow log messages                 # Системные логи",
      },
      {
        title: "Управление конфигурацией",
        type: "code",
        content: "show | compare                   # Показать изменения\ncommit                            # Применить изменения\ncommit check                      # Проверить без применения\nrollback 0                        # Откатить до предыдущей\nrun show configuration            # Из конфигурационного режима",
      },
      {
        title: "Совет",
        type: "tip",
        content: "Используйте `show configuration | display set` для отображения конфигурации в формате set-команд — это удобно для copy-paste в автоматизации.",
      },
    ],
  },
  {
    id: "ospf",
    technology: "ospf",
    title: "OSPF Configuration Guide",
    level: "JNCIA",
    track: "junos-ent",
    summary: "Настройка OSPFv2 на JunOS: area, интерфейсы, пассивные интерфейсы, проверка соседства.",
    sections: [
      {
        title: "Базовая настройка OSPF",
        type: "command",
        content: "set protocols ospf area 0 interface ge-0/0/0.0\nset protocols ospf area 0 interface ge-0/0/1.0\nset protocols ospf area 0 interface lo0.0 passive",
      },
      {
        title: "Проверка OSPF",
        type: "code",
        content: "show ospf neighbor                # Соседи (State: Full/DOWN)\nshow ospf interface               # OSPF-интерфейсы\nshow route protocol ospf          # Маршруты, полученные по OSPF\nshow ospf database                # LSDB\nshow ospf neighbor detail         # DR/BDR, Priority, Dead timer",
      },
      {
        title: "OSPF States",
        type: "text",
        content:
          "Down → Attempt → Init → 2-Way → ExStart → Exchange → Loading → Full.\n- Down: сосед недоступен\n- Init: получен Hello, но сосед не видит нас\n- 2-Way: двухсторонняя связь (на broadcast — выбор DR/BDR)\n- ExStart: мастер/слейв, DD-пакеты\n- Exchange: обмен LSA\n- Loading: запрос недостающих LSA\n- Full: полная смежность",
      },
      {
        title: "DR/BDR Election",
        type: "note",
        content: "На broadcast-сетях (Ethernet) выбирается DR и BDR. DR = highest priority (по умолчанию 128), затем highest Router ID. BDR = второй по приоритету. Все остальные — DROther (2-Way).",
      },
      {
        title: "Траблшутинг",
        type: "warning",
        content: "Если сосед не поднимается:\n1. Проверьте IP-адреса (должны быть в одной подсети)\n2. Проверьте MTU — должен совпадать на обоих сторонах\n3. Проверьте firewall (ACL) — не блокирует ли OSPF (IP 89)\n4. Проверьте area ID — должен совпадать\n5. `clear ospf neighbor` — перезапустить соседство",
      },
    ],
  },
  {
    id: "bgp",
    technology: "bgp",
    title: "BGP Configuration Guide",
    level: "JNCIP",
    track: "junos-ent",
    summary: "Настройка EBGP и IBGP на JunOS: peer groups, policy, атрибуты, проверка.",
    sections: [
      {
        title: "EBGP Peering (External BGP)",
        type: "command",
        content: "set protocols bgp group EBGP type external\nset protocols bgp group EBGP peer-as 65002\nset protocols bgp group EBGP neighbor 10.0.12.2\nset protocols bgp group EBGP export EXPORT-DIRECT",
      },
      {
        title: "IBGP Peering (Internal BGP)",
        type: "command",
        content: "set protocols bgp group IBGP type internal\nset protocols bgp group IBGP local-address 1.1.1.1\nset protocols bgp group IBGP neighbor 2.2.2.2\nset protocols bgp group IBGP neighbor 3.3.3.3",
      },
      {
        title: "BGP Policy Example",
        type: "code",
        content: "policy-statement EXPORT-LOOPBACK {\n    term LOOPBACK {\n        from {\n            protocol direct;\n            route-filter 1.1.1.1/32 exact;\n        }\n        then accept;\n    }\n    then reject;\n}",
      },
      {
        title: "Проверка BGP",
        type: "code",
        content: "show bgp summary                   # Соседи (Established/Active/Idle)\nshow bgp neighbor 10.0.12.2      # Детали соседства\nshow route protocol bgp          # BGP-маршруты\nshow route advertising-protocol bgp 10.0.12.2  # Что анонсируем\nshow route receive-protocol bgp 10.0.12.2       # Что получаем",
      },
      {
        title: "BGP States",
        type: "text",
        content:
          "Idle → Connect → Active → OpenSent → OpenConfirm → Established.\n- Idle: начальное состояние\n- Connect: ожидание TCP-соединения (порт 179)\n- Active: повтор TCP-соединения\n- OpenSent: отправлен OPEN\n- OpenConfirm: получен OPEN, ожидание Keepalive\n- Established: BGP-соседство установлено",
      },
      {
        title: "Важно",
        type: "warning",
        content: "BGP не анонсирует маршруты без export policy! Даже connected маршруты. Всегда создавайте policy-statement и указывайте его в export.",
      },
    ],
  },
  {
    id: "isis",
    technology: "isis",
    title: "IS-IS Configuration Guide",
    level: "JNCIP",
    track: "junos-ent",
    summary: "Настройка IS-IS на JunOS: NET, level-1/level-2, adjacency, проверка.",
    sections: [
      {
        title: "Network Entity Title (NET)",
        type: "text",
        content:
          "NET = Area ID + System ID + N-Selector (00).\nФормат: XX.XXXX.XXXX.XXXX.XX\nПример: 49.0001.0010.0100.1001.00\n- 49.0001 — Area ID\n- 0010.0100.1001 — System ID (обычно из MAC или loopback)\n- 00 — N-Selector (всегда 00 для routers)",
      },
      {
        title: "Настройка IS-IS",
        type: "command",
        content: "set interfaces lo0 unit 0 family iso address 49.0001.0010.0100.1001.00\nset interfaces ge-0/0/0 unit 0 family iso\nset protocols isis level 2\nset protocols isis interface ge-0/0/0.0\nset protocols isis interface lo0.0 passive",
      },
      {
        title: "Проверка IS-IS",
        type: "code",
        content: "show isis adjacency                 # Соседи (Up/Down)\nshow isis adjacency detail         # DIS, Priority, Level\nshow isis database                 # LSPDB\nshow route protocol isis          # Маршруты IS-IS\nshow isis hostname                 # Карта hostname → System ID",
      },
      {
        title: "DIS Election",
        type: "note",
        content: "DIS (Designated IS) — аналог DR в OSPF. Выбирается на broadcast-сегментах по highest priority (по умолч. 64) и MAC. DIS отправляет CSNP каждые 10 секунд.",
      },
    ],
  },
  {
    id: "mpls",
    technology: "mpls",
    title: "MPLS & LDP Guide",
    level: "JNCIP",
    track: "junos-ent",
    summary: "Настройка MPLS и LDP: family mpls, MPLS-интерфейсы, проверка LSP и меток.",
    sections: [
      {
        title: "Базовая настройка MPLS/LDP",
        type: "command",
        content: "# Включить MPLS на интерфейсах\nset interfaces ge-0/0/0 unit 0 family mpls\nset interfaces ge-0/0/1 unit 0 family mpls\n\n# Включить MPLS протокол\nset protocols mpls interface ge-0/0/0.0\nset protocols mpls interface ge-0/0/1.0\n\n# Включить LDP\nset protocols ldp interface ge-0/0/0.0\nset protocols ldp interface ge-0/0/1.0",
      },
      {
        title: "Проверка MPLS/LDP",
        type: "code",
        content: "show mpls lsp                       # LSP (Ingress/Transit/Egress)\nshow mpls interface                # MPLS-интерфейсы\nshow ldp session                   # LDP-сессии\nshow ldp neighbor                  # LDP-соседи\nshow route table inet.3            # MPLS-метки (inet.3)\nshow route 3.3.3.3                # Путь с меткой",
      },
      {
        title: "Label Operations",
        type: "text",
        content:
          "Ingress LSR: Push — добавляет метку\nTransit LSR: Swap — заменяет метку\nEgress LSR: Pop — удаляет метку (PHP — Penultimate Hop Popping)\n\nLDP использует UDP 646 (discovery, multicast 224.0.0.2) и TCP 646 (session).",
      },
      {
        title: "Важно",
        type: "tip",
        content: "Перед MPLS/LDP должен работать IGP (OSPF или IS-IS). MPLS строится поверх IGP-маршрутов. Проверьте, что все loopback достижимы через IGP, прежде чем настраивать MPLS.",
      },
    ],
  },
  {
    id: "vlan",
    technology: "junos-cli",
    title: "VLAN Configuration on JunOS",
    level: "JNCIA",
    track: "junos-ent",
    summary: "Настройка VLAN на JunOS (EX-серия): tagged/untagged, IRB, L3-интерфейсы.",
    sections: [
      {
        title: "Настройка VLAN (Access Port)",
        type: "command",
        content: "set vlans VLAN10 vlan-id 10\nset interfaces ge-0/0/0 unit 0 family ethernet-switching interface-mode access\nset interfaces ge-0/0/0 unit 0 family ethernet-switching vlan members VLAN10",
      },
      {
        title: "Настройка VLAN (Trunk Port)",
        type: "command",
        content: "set interfaces ge-0/0/1 unit 0 family ethernet-switching interface-mode trunk\nset interfaces ge-0/0/1 unit 0 family ethernet-switching vlan members [ VLAN10 VLAN20 ]",
      },
      {
        title: "IRB (L3 Interface)",
        type: "command",
        content: "set interfaces irb unit 10 family inet address 10.0.10.1/24\nset vlans VLAN10 l3-interface irb.10",
      },
      {
        title: "Проверка VLAN",
        type: "code",
        content: "show vlans                         # VLANs и порты\nshow ethernet-switching table      # MAC-таблица\nshow interfaces irb                # IRB-интерфейсы\nshow ethernet-switching interface  # Статус портов",
      },
    ],
  },
  {
    id: "firewall-filters",
    technology: "srx-policies",
    title: "Firewall Filters & Security Policies",
    level: "JNCIA",
    track: "junos-sec",
    summary: "Настройка firewall filter и security policies на SRX: zones, policies, screens.",
    sections: [
      {
        title: "Firewall Filter (на транзитный трафик)",
        type: "command",
        content: "set firewall family inet filter PROTECT term ALLOW-ICMP from protocol icmp\nset firewall family inet filter PROTECT term ALLOW-ICMP then accept\nset firewall family inet filter PROTECT term REJECT then discard\nset interfaces lo0 unit 0 family inet filter input PROTECT",
      },
      {
        title: "Security Zones & Policies (SRX)",
        type: "command",
        content: "set security zones security-zone TRUST interfaces ge-0/0/0.0\nset security zones security-zone UNTRUST interfaces ge-0/0/1.0\n\nset security policies from-zone TRUST to-zone UNTRUST policy OUTBOUND\nset security policies from-zone TRUST to-zone UNTRUST policy OUTBOUND match source-address any\nset security policies from-zone TRUST to-zone UNTRUST policy OUTBOUND match destination-address any\nset security policies from-zone TRUST to-zone UNTRUST policy OUTBOUND match application any\nset security policies from-zone TRUST to-zone UNTRUST policy OUTBOUND then permit",
      },
      {
        title: "Screen (IDS/IPS)",
        type: "command",
        content: "set security screen ids-option UNTRUST-SCREEN icmp flood threshold 500\nset security screen ids-option UNTRUST-SCREEN tcp syn-flood alarm-threshold 1024\nset security screen ids-option UNTRUST-SCREEN tcp syn-flood attack-threshold 200\nset security zones security-zone UNTRUST screen UNTRUST-SCREEN",
      },
      {
        title: "Проверка",
        type: "code",
        content: "show security policies              # Политики безопасности\nshow security zones                 # Зоны\nshow security flow session          # Активные сессии\nshow security screen statistics     # Screen-статистика\nshow log security                   # Security-логи",
      },
    ],
  },
  {
    id: "evpn-vxlan",
    technology: "evpn-vxlan",
    title: "EVPN-VXLAN Guide",
    level: "JNCIP",
    track: "junos-dc",
    summary: "Настройка EVPN-VXLAN на JunOS: route-distinguisher, route-target, VLAN-aware bundle, VXLAN encapsulation, проверка.",
    sections: [
      {
        title: "Концепция EVPN-VXLAN",
        type: "text",
        content:
          "EVPN (Ethernet VPN) — это технология для передачи L2-трафика через L3-сеть с помощью BGP. VXLAN — инкапсуляция, использующая UDP (порт 4789) для туннелирования Ethernet-кадров. Вместе они заменяют традиционные STP и VLAN Trunking, позволяя строить гигантские Data Center fabrics с мульти-арендой и anycast-шлюзами.",
      },
      {
        title: "Базовая настройка EVPN на JunOS",
        type: "command",
        content: "# Включить IGP (OSPF/IS-IS) и BGP для Underlay\nset protocols bgp group UNDERLAY type internal\nset protocols bgp group UNDERLAY local-address 1.1.1.1\nset protocols bgp group UNDERLAY family inet unicast\nset protocols bgp group UNDERLAY neighbor 2.2.2.2\nset protocols bgp group UNDERLAY neighbor 3.3.3.3\n\n# Включить BGP EVPN\nset protocols bgp group EVPN type internal\nset protocols bgp group EVPN local-address 1.1.1.1\nset protocols bgp group EVPN family evpn signaling\nset protocols bgp group EVPN neighbor 2.2.2.2\nset protocols bgp group EVPN neighbor 3.3.3.3",
      },
      {
        title: "Настройка VXLAN и VLAN-aware Bundle",
        type: "command",
        content: "# Создать switch-options для EVPN\nset switch-options route-distinguisher 1.1.1.1:100\nset switch-options vrf-target target:100:100\nset switch-options vrf-target auto\n\n# VLAN-aware bundle (VLAN-Bundle)\nset vlans VLAN100 vlan-id 100\nset vlans VLAN100 vxlan vni 10100\nset vlans VLAN100 vxlan ingress-node-replication\n\nset vlans VLAN200 vlan-id 200\nset vlans VLAN200 vxlan vni 10200\nset vlans VLAN200 vxlan ingress-node-replication\n\n# IRB (Anycast Gateway)\nset interfaces irb unit 100 family inet address 10.0.100.1/24\nset interfaces irb unit 100 virtual-gateway-accept-data\nset vlans VLAN100 l3-interface irb.100\n\nset interfaces irb unit 200 family inet address 10.0.200.1/24\nset interfaces irb unit 200 virtual-gateway-accept-data\nset vlans VLAN200 l3-interface irb.200",
      },
      {
        title: "Проверка EVPN-VXLAN",
        type: "code",
        content: "show evpn instance                       # EVPN-инстансы (Type)\nshow evpn database                       # EVPN-база (MAC/VNI)\nshow evpn l3-context                     # L3-контекст\nshow ethernet-switching table            # MAC-таблица\nshow interfaces vxlan                    # VXLAN-интерфейсы\nshow route table evpn.0                  # EVPN-маршруты (Type-2, Type-3)\nshow route table inet.0 protocol evpn    # EVPN-симметричный IRB\nshow bgp summary                         # BGP-соседи (EVPN family)",
      },
      {
        title: "EVPN Route Types",
        type: "text",
        content:
          "Type 1 — Ethernet Auto-Discovery (AD): обнаружение PE, защита от дублей MAC\nType 2 — MAC/IP Advertisement: анонс MAC-адреса (опционально с IP)\nType 3 — Inclusive Multicast Ethernet Tag: IMET, для BUM-трафика\nType 4 — Ethernet Segment: для multi-homing (ESI)\nType 5 — IP Prefix: для передачи L3-маршрутов поверх EVPN (aka EVPN-Prefix)",
      },
      {
        title: "Совет",
        type: "tip",
        content: "Используйте `vrf-target auto` для автоматического формирования RT по VNI — это упрощает конфигурацию. Для симметричного IRB (Type-5) нужно указывать L3-контекст EVPN.",
      },
    ],
  },
  {
    id: "ipsec-vpn",
    technology: "srx-policies",
    title: "IPsec VPN Configuration Guide",
    level: "JNCIP",
    track: "junos-sec",
    summary: "Настройка Site-to-Site IPsec VPN на SRX: IKE, IPsec proposal, security associations, tunnel interface.",
    sections: [
      {
        title: "Концепция IPsec на SRX",
        type: "text",
        content:
          "IPsec VPN на Juniper SRX состоит из двух фаз:\n- Phase 1 (IKE): аутентификация и установка ISAKMP SA\n- Phase 2 (Quick mode): согласование IPsec SA и шифрование трафика\n\nОсновные компоненты:\n- IKE Proposal — шифрование, аутентификация, DH-группа\n- IKE Policy — привязка proposal, режим (main/aggressive), pre-shared key\n- IPsec Policy — transforms (ESP/AH, шифрование, аутентификация)\n- IPsec VPN — связка IKE + IPsec + gateway\n- Secure Tunnel (st0.x) — виртуальный туннельный интерфейс",
      },
      {
        title: "Настройка IKE Phase 1",
        type: "command",
        content: "# IKE Proposal\nset security ike proposal IKE-PROP authentication-method pre-shared-keys\nset security ike proposal IKE-PROP dh-group group14\nset security ike proposal IKE-PROP authentication-algorithm sha-256\nset security ike proposal IKE-PROP encryption-algorithm aes-256-cbc\nset security ike proposal IKE-PROP lifetime-seconds 28800\n\n# IKE Policy\nset security ike policy IKE-POL mode main\nset security ike policy IKE-POL proposals IKE-PROP\nset security ike policy IKE-POL pre-shared-key ascii-text \"$trongK3y!\"\n\n# IKE Gateway\nset security ike gateway GW-REMOTE ike-policy IKE-POL\nset security ike gateway GW-REMOTE address 203.0.113.1\nset security ike gateway GW-REMOTE external-interface ge-0/0/1.0\nset security ike gateway GW-REMOTE version v2-only\nset security ike gateway GW-REMOTE local-address 198.51.100.1",
      },
      {
        title: "Настройка IPsec Phase 2",
        type: "command",
        content: "# IPsec Proposal\nset security ipsec proposal IPSEC-PROP protocol esp\nset security ipsec proposal IPSEC-PROP authentication-algorithm hmac-sha-256-128\nset security ipsec proposal IPSEC-PROP encryption-algorithm aes-256-cbc\nset security ipsec proposal IPSEC-PROP lifetime-seconds 3600\n\n# IPsec Policy\nset security ipsec policy IPSEC-POL proposals IPSEC-PROP\n\n# IPsec VPN\nset security ipsec vpn VPN-TO-REMOTE bind-interface st0.100\nset security ipsec vpn VPN-TO-REMOTE ike gateway GW-REMOTE\nset security ipsec vpn VPN-TO-REMOTE ike ipsec-policy IPSEC-POL\nset security ipsec vpn VPN-TO-REMOTE establish-tunnels immediately",
      },
      {
        title: "Tunnel Interface и Security Policy",
        type: "command",
        content: "# Tunnel Interface\nset interfaces st0 unit 100 description \"VPN to Remote-Office\"\nset interfaces st0 unit 100 family inet address 10.0.1.1/30\n\n# Security Zone для VPN\nset security zones security-zone VPN-V4\nset security zones security-zone VPN-V4 interfaces st0.100\n\n# Security Policies (разрешаем трафик через VPN)\nset security policies from-zone TRUST to-zone VPN-V4 policy VPN-OUT\nset security policies from-zone TRUST to-zone VPN-V4 policy VPN-OUT match source-address any\nset security policies from-zone TRUST to-zone VPN-V4 policy VPN-OUT match destination-address any\nset security policies from-zone TRUST to-zone VPN-V4 policy VPN-OUT match application any\nset security policies from-zone TRUST to-zone VPN-V4 policy VPN-OUT then permit\n\n# Route to remote subnet через st0\nset routing-options static route 10.0.2.0/24 next-hop 10.0.1.2",
      },
      {
        title: "Проверка IPsec VPN",
        type: "code",
        content: "show security ike security-associations    # IKE SA (UP/DOWN)\nshow security ipsec security-associations   # IPsec SA (UP/DOWN)\nshow security ike statistics                # IKE-статистика\nshow security ipsec statistics              # IPsec-статистика\nshow security flow session interface st0.100  # Сессии через туннель\nshow security ipsec vpn                     # VPN-статус\nshow interfaces st0.100                     # Статус tunnel-интерфейса\nshow security ipsec sa detail               # Детали SA (bytes, packets)",
      },
      {
        title: "Траблшутинг IPsec",
        type: "warning",
        content: "Если VPN не встаёт:\n1. Проверьте, что внешние IP доступны (ping, traceroute)\n2. Проверьте firewall — не блокирует ли UDP 500 (IKE), UDP 4500 (NAT-T), ESP (IP 50)\n3. Проверьте, что pre-shared key совпадают на обоих сторонах\n4. Проверьте IKE proposal на совместимость (шифрование, DH-группа, auth-алгоритм)\n5. Включите `traceoptions security ike` для детального лога\n6. Проверьте, что NAT не сбивает IPsec (NAT-T должен включиться автоматически)",
      },
    ],
  },
  {
    id: "vrf",
    technology: "bgp",
    title: "VRF & MPLS L3VPN Guide",
    level: "JNCIP",
    track: "junos-sp",
    summary: "Настройка VRF и MPLS L3VPN на JunOS: route-distinguisher, route-target, VRF-таблицы, BGP VPNv4.",
    sections: [
      {
        title: "Концепция VRF",
        type: "text",
        content:
          "VRF (Virtual Routing and Forwarding) — виртуальная таблица маршрутизации. Каждый VRF имеет:\n- Свой RIB (Routing Information Base) — Customer VPN-таблица\n- Route Distinguisher (RD) — делает маршруты уникальными в глобальной таблице\n- Route Target (RT) — BGP extended community для импорта/экспорта\n- Свои интерфейсы (Customer Edge attachment)\n\nMPLS L3VPN использует BGP для передачи VPNv4-маршрутов между PE-роутерами.",
      },
      {
        title: "Настройка VRF на JunOS",
        type: "command",
        content: "# Создание VRF (CUSTOMER-A)\nset routing-instances CUSTOMER-A instance-type vrf\nset routing-instances CUSTOMER-A interface ge-0/0/0.100\nset routing-instances CUSTOMER-A interface ge-0/0/1.100\nset routing-instances CUSTOMER-A route-distinguisher 1.1.1.1:100\nset routing-instances CUSTOMER-A vrf-target target:65000:100\n\n# VRF с разными RT для импорта/экспорта\nset routing-instances CUSTOMER-B instance-type vrf\nset routing-instances CUSTOMER-B interface ge-0/0/2.200\nset routing-instances CUSTOMER-B route-distinguisher 1.1.1.1:200\nset routing-instances CUSTOMER-B vrf-import IMPORT-CUST-B\nset routing-instances CUSTOMER-B vrf-export EXPORT-CUST-B\n\n# BGP в VRF для CE-PE\nset routing-instances CUSTOMER-A protocols bgp group CE type external\nset routing-instances CUSTOMER-A protocols bgp group CE peer-as 65100\nset routing-instances CUSTOMER-A protocols bgp group CE local-as 65000\nset routing-instances CUSTOMER-A protocols bgp group CE neighbor 10.100.1.2\n\n# Или статический маршрут в VRF\nset routing-instances CUSTOMER-A routing-options static route 10.100.0.0/16 next-hop 10.100.1.2",
      },
      {
        title: "BGP VPNv4 (для передачи между PE)",
        type: "command",
        content: "# VPNv4 BGP (на каждом PE)\nset protocols bgp group VPN type internal\nset protocols bgp group VPN local-address 1.1.1.1\nset protocols bgp group VPN family inet-vpn unicast\nset protocols bgp group VPN family inet6-vpn unicast\nset protocols bgp group VPN neighbor 2.2.2.2\nset protocols bgp group VPN neighbor 3.3.3.3\n\n# Route Target Policy (опционально)\nset policy-options community CUST-A-IMPORT members target:65000:100\nset policy-options community CUST-A-EXPORT members target:65000:100\n\npolicy-statement VPN-IMPORT {\n    term A {\n        from community CUST-A-IMPORT;\n        then accept;\n    }\n    then reject;\n}",
      },
      {
        title: "Проверка VRF и L3VPN",
        type: "code",
        content: "show route instance                   # Все VRF-инстансы\nshow route instance CUSTOMER-A        # Детали VRF\nshow route table CUSTOMER-A.inet.0     # VRF-таблица\nshow route table bgp.l3vpn.0          # Глобальная VPNv4-таблица\nshow route table CUSTOMER-A.inet.0 protocol bgp  # BGP-маршруты в VRF\nshow bgp summary                      # BGP-соседи (обычные + VPNv4)\nping routing-instance CUSTOMER-A 10.100.1.2   # Ping из VRF",
      },
      {
        title: "Важно",
        type: "note",
        content: "Для работы MPLS L3VPN обязательна IGP reachability между loopback PE-роутеров, настроенный MPLS/LDP и семейство `inet-vpn unicast` в BGP. JunOS автоматически создаёт таблицу `bgp.l3vpn.0` при включении семейства к BGP.",
      },
    ],
  },
  {
    id: "bgp-lu",
    technology: "bgp",
    title: "BGP Labeled Unicast Guide",
    level: "JNCIP",
    track: "junos-sp",
    summary: "Настройка BGP Labeled Unicast (BGP-LU): BGP-метки, inter-AS MPLS, сегментная маршрутизация SR-MPLS.",
    sections: [
      {
        title: "Концепция BGP-LU",
        type: "text",
        content:
          "BGP Labeled Unicast (BGP-LU, RFC 8277) — технология, при которой BGP распространяет не только маршруты, но и MPLS-метки. В отличие от LDP, метки передаются вместе с NLRI в BGP UPDATE. BGP-LU используется:\n- Для MPLS в Inter-AS Option C (BGP-free core)\n- Как альтернатива LDP/RSVP\n- В Segment Routing (SR-MPLS) с BGP Prefix-SID\n- Для label-unicast на ASBR/PE",
      },
      {
        title: "Настройка BGP-LU на JunOS",
        type: "command",
        content: "# Включить семейство inet-labeled-unicast\nset protocols bgp group BGP-LU type internal\nset protocols bgp group BGP-LU local-address 1.1.1.1\nset protocols bgp group BGP-LU family inet-labeled-unicast rib inet.3\nset protocols bgp group BGP-LU neighbor 2.2.2.2\nset protocols bgp group BGP-LU neighbor 3.3.3.3\n\n# BGP-LU для EBGP (inter-AS Option C)\nset protocols bgp group EBGP-LU type external\nset protocols bgp group EBGP-LU family inet-labeled-unicast\nset protocols bgp group EBGP-LU peer-as 65002\nset protocols bgp group EBGP-LU export EXPORT-BGP-LU\nset protocols bgp group EBGP-LU neighbor 10.0.12.2",
      },
      {
        title: "Export Policy для BGP-LU",
        type: "code",
        content: "policy-statement EXPORT-BGP-LU {\n    term LOOPBACK {\n        from {\n            protocol direct;\n            route-filter 1.1.1.1/32 exact;\n        }\n        then {\n            community add NO-EXPORT;\n            accept;\n        }\n    }\n    then reject;\n}",
      },
      {
        title: "Проверка BGP-LU",
        type: "code",
        content: "show bgp summary                        # Соседи (inet-labeled-unicast)\nshow route protocol bgp table inet.3   # BGP-LU метки в inet.3\nshow route table inet.3                # MPLS Label table\nshow bgp neighbor 2.2.2.2              # Детали BGP-LU (received prefixes)\nshow route 3.3.3.3 detail             # Путь с меткой\nshow mpls lsp                          # MPLS LSP",
      },
      {
        title: "Совет",
        type: "tip",
        content: "Указывайте `rib inet.3` при настройке BGP-LU, чтобы метки записывались в inet.3 (MPLS-таблица), а не в inet.0. Это позволяет MPLS-коммутации работать корректно. Если метки не появляются — проверьте, что next-hop достижим через IGP.",
      },
    ],
  },
  {
    id: "multicast",
    technology: "multicast",
    title: "Multicast Guide (PIM-SM & IGMP)",
    level: "JNCIP",
    track: "junos-ent",
    summary: "Настройка мультикаста на JunOS: PIM-SM, IGMP/MLD, RP, rendezvous point, group membership.",
    sections: [
      {
        title: "Концепция Multicast на JunOS",
        type: "text",
        content:
          "Multicast — передача трафика от одного источника (Source) группе получателей (Receivers) через групповой адрес.\n\nОсновные компоненты JunOS:\n- IGMP (Internet Group Management Protocol) — на стороне получателя, подписка на группу\n- PIM (Protocol Independent Multicast) — построение (S,G) и (*,G) деревьев\n- PIM-SM (Sparse Mode) — RP-based, дерево строится от RP\n- PIM-SSM (Source-Specific Multicast) — (S,G) без RP, с IGMPv3\n- RP (Rendezvous Point) — центральная точка для PIM-SM\n- MSDP — обмен информацией об active sources между RP разных доменов",
      },
      {
        title: "Настройка IGMP",
        type: "command",
        content: "# Включить IGMP на интерфейсе к получателям\nset protocols igmp interface ge-0/0/1.0\nset protocols igmp interface ge-0/0/1.0 version 3\nset protocols igmp interface ge-0/0/2.0\n\n# IGMP Static Join (для тестирования)\nset protocols igmp interface ge-0/0/2.0 static group 239.0.1.1\n\n# IGMP Snooping (в свитчевой части)\nset vlans VLAN100 igmp-snooping",
      },
      {
        title: "Настройка PIM-SM",
        type: "command",
        content: "# Включить PIM на интерфейсах\nset protocols pim interface lo0.0\nset protocols pim interface ge-0/0/0.0\nset protocols pim interface ge-0/0/1.0 mode sparse\nset protocols pim interface ge-0/0/2.0 mode sparse\n\n# Static RP\nset protocols pim rp static address 1.1.1.1\nset protocols pim rp static address 1.1.1.1 group-rp ff00::/8\nset protocols pim rp static address 2.2.2.2 group-rp 239.0.0.0/8\n\n# Bootstrap RP (BSR — динамический RP)\nset protocols pim rp local address 1.1.1.1\nset protocols pim rp local group-ranges 224.0.0.0/4\nset protocols pim bsr-candidate interface lo0.0 priority 200\nset protocols pim rp-candidate interface lo0.0",
      },
      {
        title: "Проверка Multicast",
        type: "code",
        content: "show pim neighbors                     # PIM-соседи (Up/Down)\nshow pim interfaces                    # PIM-интерфейсы\nshow pim rp                             # RP-информация\nshow pim join                           # (S,G) и (*,G) join-состояния\nshow multicast route                    # Multicast routing table\nshow igmp groups                       # IGMP-группы\nshow igmp interface                    # IGMP-интерфейсы\nping multicast 239.0.1.1               # Мультикаст ping",
      },
      {
        title: "(S,G) vs (*,G)",
        type: "text",
        content:
          "(S,G) — Source-Specific Tree (SPT). Путь от источника к получателям, оптимальный маршрут.\n(*,G) — Shared Tree (RPT). Дерево через RP: \"от любого источника к группе G, через RP\".\n\nPIM-SM: получатель отправляет (*,G) Join к RP. RP получает трафик от источника по (S,G) регистрации. После первого пакета последний хоп может переключиться на (S,G) SPT (switchover).\n\nPIM-SSM: только (S,G), без RP, с IGMPv3 — получатель явно указывает источник.",
      },
      {
        title: "Траблшутинг",
        type: "warning",
        content: "Если мультикаст не работает:\n1. Проверьте, что PIM соседства Up: `show pim neighbors`\n2. Проверьте RP: `show pim rp` — RP должен быть active\n3. Проверьте RP reachability: ping до RP\n4. Проверьте, что IGP маршрутирует (не BGP) — PIM не работает поверх EBGP без настройки\n5. Проверьте firewall — не блокирует ли IGMP (IP 2) и PIM (IP 103)\n6. Проверьте TTL multicast-пакетов (должен быть >= количество хопов)\n7. Включите `traceoptions pim` для детального логирования",
      },
    ],
  },
];

// ─── Quick Reference Commands ─────────────────────────────────

interface CommandRef {
  category: string;
  commands: { cmd: string; description: string }[];
}

const quickReference: Record<string, CommandRef[]> = {
  "junos-ent": [
    {
      category: "System",
      commands: [
        { cmd: "show version", description: "Версия JunOS" },
        { cmd: "show system uptime", description: "Аптайм системы" },
        { cmd: "show system storage", description: "Использование диска" },
        { cmd: "show system processes extensive", description: "Процессы" },
        { cmd: "request system reboot", description: "Перезагрузка" },
      ],
    },
    {
      category: "Interfaces",
      commands: [
        { cmd: "show interfaces terse", description: "Кратко по всем интерфейсам" },
        { cmd: "show interfaces ge-0/0/0 extensive", description: "Детально по интерфейсу" },
        { cmd: "show interfaces diagnostics optics ge-0/0/0", description: "Оптика (SFP)" },
        { cmd: "monitor interface traffic", description: "Трафик в реальном времени" },
        { cmd: "show configuration interfaces", description: "Конфиг интерфейсов" },
      ],
    },
    {
      category: "Routing",
      commands: [
        { cmd: "show route", description: "Таблица маршрутизации" },
        { cmd: "show route protocol ospf", description: "OSPF-маршруты" },
        { cmd: "show route protocol bgp", description: "BGP-маршруты" },
        { cmd: "show route 10.0.0.0/8", description: "Поиск маршрута" },
        { cmd: "show route table inet.3", description: "MPLS-метки (inet.3)" },
        { cmd: "show route forwarding-table", description: "FIB" },
      ],
    },
    {
      category: "OSPF",
      commands: [
        { cmd: "show ospf neighbor", description: "OSPF-соседи" },
        { cmd: "show ospf interface", description: "OSPF-интерфейсы" },
        { cmd: "show ospf database", description: "LSDB" },
        { cmd: "show ospf statistics", description: "Статистика OSPF" },
        { cmd: "clear ospf neighbor", description: "Сброс соседства" },
      ],
    },
    {
      category: "BGP",
      commands: [
        { cmd: "show bgp summary", description: "BGP-соседи" },
        { cmd: "show bgp neighbor 10.0.12.2", description: "Детали соседства" },
        { cmd: "show route advertising-protocol bgp 10.0.12.2", description: "Анонсы" },
        { cmd: "show route receive-protocol bgp 10.0.12.2", description: "Полученные" },
        { cmd: "clear bgp neighbor 10.0.12.2", description: "Сброс соседства" },
      ],
    },
    {
      category: "IS-IS",
      commands: [
        { cmd: "show isis adjacency", description: "IS-IS соседи" },
        { cmd: "show isis database", description: "LSDB" },
        { cmd: "show isis hostname", description: "Карта hostname" },
        { cmd: "show isis spf log", description: "SPF-логи" },
      ],
    },
    {
      category: "MPLS/LDP",
      commands: [
        { cmd: "show mpls lsp", description: "MPLS LSP" },
        { cmd: "show mpls interface", description: "MPLS-интерфейсы" },
        { cmd: "show ldp session", description: "LDP-сессии" },
        { cmd: "show ldp database", description: "LDP-база меток" },
      ],
    },
    {
      category: "Multicast",
      commands: [
        { cmd: "show pim neighbors", description: "PIM-соседи" },
        { cmd: "show pim rp", description: "RP-информация" },
        { cmd: "show pim join", description: "(S,G) и (*,G) join" },
        { cmd: "show multicast route", description: "Multicast routing table" },
        { cmd: "show igmp groups", description: "IGMP-группы" },
        { cmd: "ping multicast 239.0.1.1", description: "Мультикаст ping" },
      ],
    },
  ],
  "junos-sp": [
    {
      category: "MPLS",
      commands: [
        { cmd: "show mpls lsp", description: "LSP" },
        { cmd: "show mpls lsp name LSP-PE1-PE2", description: "LSP по имени" },
        { cmd: "show mpls lsp statistics", description: "Статистика LSP" },
        { cmd: "show mpls path", description: "MPLS-пути (для RSVP)" },
        { cmd: "show rsvp session", description: "RSVP-сессии" },
      ],
    },
    {
      category: "MPLS L3VPN",
      commands: [
        { cmd: "show route table VPN-A.inet.0", description: "VRF-таблица" },
        { cmd: "show route instance CUSTOMER-A", description: "Детали VRF" },
        { cmd: "show route protocol bgp table bgp.l3vpn.0", description: "VPNv4-маршруты" },
        { cmd: "ping routing-instance CUSTOMER-A 10.0.0.1", description: "Ping из VRF" },
      ],
    },
    {
      category: "BGP-LU (Labeled Unicast)",
      commands: [
        { cmd: "show route protocol bgp table inet.3", description: "BGP-LU метки" },
        { cmd: "show route table inet.3", description: "MPLS Label table" },
        { cmd: "show bgp neighbor 2.2.2.2", description: "Детали BGP-LU" },
        { cmd: "show mpls lsp", description: "MPLS LSP" },
      ],
    },
  ],
  "junos-sec": [
    {
      category: "Security Policies",
      commands: [
        { cmd: "show security policies", description: "Все политики" },
        { cmd: "show security policies from-zone TRUST to-zone UNTRUST", description: "Политики между зонами" },
        { cmd: "show security zones", description: "Зоны безопасности" },
        { cmd: "show security zones terse", description: "Зоны кратко" },
      ],
    },
    {
      category: "Sessions & NAT",
      commands: [
        { cmd: "show security flow session", description: "Активные сессии" },
        { cmd: "show security flow session summary", description: "Кратко по сессиям" },
        { cmd: "show security nat source", description: "Source NAT" },
        { cmd: "show security nat destination", description: "Destination NAT" },
        { cmd: "clear security flow session", description: "Сброс всех сессий" },
      ],
    },
    {
      category: "IPsec VPN",
      commands: [
        { cmd: "show security ike security-associations", description: "IKE SA (UP/DOWN)" },
        { cmd: "show security ipsec security-associations", description: "IPsec SA (UP/DOWN)" },
        { cmd: "show security ipsec vpn", description: "VPN-статус" },
        { cmd: "show security flow session interface st0.100", description: "Сессии через туннель" },
        { cmd: "clear security ike security-associations", description: "Сброс IKE SA" },
      ],
    },
  ],
  "junos-dc": [
    {
      category: "EVPN/VXLAN",
      commands: [
        { cmd: "show evpn instance", description: "EVPN-инстансы" },
        { cmd: "show evpn database", description: "EVPN-база (MAC/VNI)" },
        { cmd: "show evpn l3-context", description: "L3-контекст" },
        { cmd: "show ethernet-switching table", description: "MAC-таблица" },
        { cmd: "show interfaces vxlan", description: "VXLAN-интерфейсы" },
        { cmd: "show route table evpn.0", description: "EVPN-маршруты (Type-2/3/5)" },
        { cmd: "show route table inet.0 protocol evpn", description: "EVPN-симметричный IRB" },
      ],
    },
    {
      category: "LAG/MC-LAG",
      commands: [
        { cmd: "show lacp interfaces", description: "LACP" },
        { cmd: "show lacp statistics interfaces ae0", description: "LACP-статистика" },
        { cmd: "show interfaces ae0", description: "AE-интерфейс" },
        { cmd: "show configuration interfaces ae0", description: "Конфиг агрегации" },
      ],
    },
  ],
  "junos-aut": [
    {
      category: "PyEZ",
      commands: [
        { cmd: "from jnpr.junos import Device", description: "Импорт Device" },
        { cmd: "dev = Device(host='10.0.0.1', user='admin')", description: "Подключение" },
        { cmd: "dev.open()", description: "Открыть соединение" },
        { cmd: "dev.facts['hostname']", description: "Факты об устройстве" },
        { cmd: "dev.rpc.get_interface_information()", description: "RPC-вызов" },
        { cmd: "dev.close()", description: "Закрыть соединение" },
      ],
    },
    {
      category: "Ansible",
      commands: [
        { cmd: "ansible-playbook -i inventory deploy.yml", description: "Запуск playbook" },
        { cmd: "ansible all -m juniper_junos_command -a \"commands='show version'\"", description: "Выполнить команду" },
        { cmd: "ansible all -m juniper_junos_config -a \"src=config.conf\"", description: "Применить конфиг" },
        { cmd: "ansible-inventory -i inventory --list", description: "Проверить inventory" },
      ],
    },
  ],
};

// ─── Components ───────────────────────────────────────────────

const trackIcons: Record<string, any> = {
  "junos-ent": Network,
  "junos-sp": Network,
  "junos-sec": ShieldCheck,
  "junos-dc": ComputerTower,
  "junos-aut": Cloud,
  "cisco": Trophy,
};

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <button
      onClick={() => {
        navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => setCopied(false), 1500);
      }}
      className="absolute top-2 right-2 p-1.5 rounded-lg bg-zinc-800/50 hover:bg-zinc-700 text-zinc-400 hover:text-zinc-200 transition-all opacity-0 group-hover:opacity-100"
      title="Copy"
    >
      {copied ? <Check className="h-3.5 w-3.5 text-emerald-400" weight="bold" /> : <Copy className="h-3.5 w-3.5" weight="regular" />}
    </button>
  );
}

function SectionBlock({ section }: { section: GuideSection }) {
  const bgMap = {
    text: "",
    code: "bg-zinc-900 dark:bg-zinc-950",
    command: "bg-black",
    note: "bg-sky-900/20 border border-sky-800/30",
    tip: "bg-emerald-900/20 border border-emerald-800/30",
    warning: "bg-amber-900/20 border border-amber-800/30",
  };

  const iconMap = {
    note: <BookOpen className="h-4 w-4 text-sky-400 shrink-0 mt-0.5" weight="fill" />,
    tip: <Copy className="h-4 w-4 text-emerald-400 shrink-0 mt-0.5" weight="fill" />,
    warning: <ArrowsDownUp className="h-4 w-4 text-amber-400 shrink-0 mt-0.5" weight="fill" />,
  };

  const labelMap = {
    note: "Примечание",
    tip: "Совет",
    warning: "Внимание",
  };

  if (section.type === "code" || section.type === "command") {
    return (
      <div className="relative group">
        <pre className={`${bgMap[section.type]} text-zinc-200 font-mono text-sm p-4 rounded-xl overflow-x-auto leading-relaxed border border-zinc-800`}>
          <code>{section.content}</code>
        </pre>
        <CopyButton text={section.content} />
      </div>
    );
  }

  if (section.type === "note" || section.type === "tip" || section.type === "warning") {
    return (
      <div className={`${bgMap[section.type]} rounded-xl p-4 flex gap-3`}>
        {iconMap[section.type]}
        <div>
          <span className="text-xs font-semibold uppercase tracking-wider text-zinc-400 mb-1 block">
            {labelMap[section.type]}
          </span>
          <p className="text-sm text-zinc-300 whitespace-pre-wrap leading-relaxed">{section.content}</p>
        </div>
      </div>
    );
  }

  return <p className="text-zinc-300 leading-relaxed text-sm">{section.content}</p>;
}

// ─── Animated Terminal ────────────────────────────────────────
// Extracted to frontend/components/AnimatedTerminal.tsx

export default function StudyPageWrapper() {
  return (
    <Suspense fallback={
      <div className="flex items-center justify-center min-h-[60dvh]">
        <Spinner />
      </div>
    }>
      <StudyPage />
    </Suspense>
  );
}

function StudyPage() {
  const { isAuthenticated, loading: authLoading } = useAuth();
  const { t } = useTranslation();
  const router = useRouter();

  const [tracks, setTracks] = useState<any[]>([]);
  const [activeGuide, setActiveGuide] = useState<string>("junos-cli");
  const [activeTrack, setActiveTrack] = useState<string>("all");
  const [activeLevel, setActiveLevel] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [showCommands, setShowCommands] = useState(false);
  const [showIncompleteOnly, setShowIncompleteOnly] = useState(false);
  const [completedGuides, setCompletedGuides] = useState<Set<string>>(new Set());
  const [savingGuides, setSavingGuides] = useState<Set<string>>(new Set());
  // Copy animation state per command index
  const [copiedIdx, setCopiedIdx] = useState<number | null>(null);
  // Terminal animation state
  const [activeTerminal, setActiveTerminal] = useState<{ trackSlug: string; category: string } | null>(null);
  // Live terminal state (real WebSocket/SSH connection)
  const [liveTerminal, setLiveTerminal] = useState<{ trackSlug: string; category: string } | null>(null);

  // Compute sandbox WebSocket URLs
  const baseWsUrl = typeof window !== "undefined"
    ? `${window.location.protocol === "https:" ? "wss" : "ws"}://${window.location.hostname}:8080`
    : "";
  const sandboxWsUrl = baseWsUrl ? `${baseWsUrl}/ws/sandbox/playground` : "";
  const vtyshWsUrl = baseWsUrl ? `${baseWsUrl}/ws/sandbox/vtysh` : "";
  const junosWsUrl = baseWsUrl ? `${baseWsUrl}/ws/sandbox/junos` : "";
  const [liveBackend, setLiveBackend] = useState<"vtysh" | "junos">("vtysh");
  // Sandbox backend status (FRR / cRPD)
  const [sandboxStatus, setSandboxStatus] = useState<{ vtysh: string; junos: string } | null>(null);

  // Poll sandbox status every 10 seconds
  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const res = await fetch("/api/v1/sandbox/status");
        if (res.ok) {
          setSandboxStatus(await res.json());
        }
      } catch {
        // Silently ignore — backend might not expose this endpoint yet
      }
    };
    fetchStatus();
    const interval = setInterval(fetchStatus, 10000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/auth/login");
      return;
    }
    tracksApi.list().then(setTracks).catch(() => {});
    studyProgressApi.getProgress().then((progress) => {
      setCompletedGuides(new Set(progress.map((p: any) => p.guide_id)));
    }).catch(() => {});
  }, [isAuthenticated, authLoading, router]);

  // Toggle guide completion status
  const toggleProgress = async (guideId: string) => {
    const isCompleted = completedGuides.has(guideId);
    // Optimistic update
    const newCompleted = new Set(completedGuides);
    if (isCompleted) {
      newCompleted.delete(guideId);
    } else {
      newCompleted.add(guideId);
    }
    setSavingGuides((prev) => new Set(prev).add(guideId));
    setCompletedGuides(newCompleted);
    try {
      await studyProgressApi.toggleGuide({ guide_id: guideId, completed: !isCompleted });
    } catch {
      // Revert on error — restore original state
      setCompletedGuides(completedGuides);
    } finally {
      setSavingGuides((prev) => {
        const next = new Set(prev);
        next.delete(guideId);
        return next;
      });
    }
  };

  // Guide progress stats
  const totalGuides = technologyGuides.length;
  const completedCount = technologyGuides.filter((g) => completedGuides.has(g.id)).length;
  const progressPercent = totalGuides > 0 ? Math.round((completedCount / totalGuides) * 100) : 0;

  // Filtered guides
  const filteredGuides = useMemo(() => {
    return technologyGuides.filter((g) => {
      if (activeTrack !== "all" && g.track !== activeTrack) return false;
      if (activeLevel !== "all" && g.level !== activeLevel) return false;
      if (showIncompleteOnly && completedGuides.has(g.id)) return false;
      if (searchQuery) {
        const q = searchQuery.toLowerCase();
        return (
          g.title.toLowerCase().includes(q) ||
          g.summary.toLowerCase().includes(q) ||
          g.sections.some((s) => s.content.toLowerCase().includes(q))
        );
      }
      return true;
    });
  }, [activeTrack, activeLevel, showIncompleteOnly, completedGuides, searchQuery]);

  const currentGuide = technologyGuides.find((g) => g.id === activeGuide);

  if (authLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60dvh]">
        <Spinner />
      </div>
    );
  }

  // Levels for filter
  const levels = ["all", "JNCIA", "JNCIP", "CCNA"];

  return (
    <div className="min-h-[100dvh] bg-zinc-50 dark:bg-zinc-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 mb-8">
          <div>
            <Badge variant="secondary" className="mb-3">
              <BookOpen className="h-3 w-3 mr-1" weight="fill" />
              Study Materials
            </Badge>
            <h1 className="text-4xl font-bold tracking-tighter text-zinc-900 dark:text-white">
              Учебные материалы
            </h1>
            <p className="mt-1 text-zinc-500 dark:text-zinc-400">
              CLI-шпаргалки, конфигурационные гайды и справочники по технологиям
            </p>
          </div>
        </div>

        {/* Progress Bar */}
        {totalGuides > 0 && (
          <div className="mb-6">
            <div className="flex items-center gap-3 mb-2">
              <div className="p-1.5 rounded-lg bg-emerald-100 dark:bg-emerald-900/20">
                <Gauge className="h-4 w-4 text-emerald-600 dark:text-emerald-400" weight="fill" />
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
                    Study Progress
                  </span>
                  <span className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">
                    {completedCount} / {totalGuides} ({progressPercent}%)
                  </span>
                </div>
                <div className="w-full h-2 bg-zinc-200 dark:bg-zinc-800 rounded-full overflow-hidden">
                  <motion.div
                    className="h-full bg-gradient-to-r from-emerald-500 to-emerald-400 rounded-full"
                    initial={false}
                    animate={{ width: `${progressPercent}%` }}
                    transition={{ duration: 0.8, ease: "easeOut" }}
                  />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Search & Filters */}
        <div className="flex flex-wrap items-center gap-3 mb-8">
          {/* Search */}
          <div className="relative flex-1 min-w-[200px] max-w-sm">
            <MagnifyingGlass className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-zinc-400" weight="regular" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search guides, commands..."
              className="w-full pl-9 pr-4 py-2 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-300 dark:border-zinc-700 text-sm text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 transition-all"
            />
          </div>

          {/* Track filter */}  
          <div className="flex items-center gap-2">
            <button
              onClick={() => setActiveTrack("all")}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${
                activeTrack === "all"
                  ? "bg-zinc-900 text-white dark:bg-white dark:text-zinc-900"
                  : "bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700"
              }`}
            >
              All
            </button>
            {tracks.map((track) => (
              <button
                key={track.slug}
                onClick={() => setActiveTrack(track.slug)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${
                  activeTrack === track.slug
                    ? "bg-zinc-900 text-white dark:bg-white dark:text-zinc-900"
                    : "bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700"
                }`}
              >
                {track.name}
              </button>
            ))}
          </div>

          <div className="w-px h-5 bg-zinc-300 dark:bg-zinc-600" />

          {/* Level filter */}
          {levels.map((l) => (
            <button
              key={l}
              onClick={() => setActiveLevel(l === "all" ? "all" : l)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${
                activeLevel === l
                  ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-300"
                  : "bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700"
              }`}
            >
              {l === "all" ? "All Levels" : l}
            </button>
          ))}

          {/* Show incomplete only toggle */}
          <button
            onClick={() => setShowIncompleteOnly(!showIncompleteOnly)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 flex items-center gap-1.5 ${
              showIncompleteOnly
                ? "bg-amber-100 text-amber-700 dark:bg-amber-900/20 dark:text-amber-300"
                : "bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700"
            }`}
          >
            <Circle className="h-3.5 w-3.5" weight="regular" />
            {showIncompleteOnly ? "Incomplete only" : "All guides"}
          </button>

          {/* Toggle commands reference */}
          <button
            onClick={() => setShowCommands(!showCommands)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 flex items-center gap-1.5 ${
              showCommands
                ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-300"
                : "bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700"
            }`}
          >
            <Terminal className="h-3.5 w-3.5" weight="regular" />
            CLI Reference
          </button>
        </div>

        {showCommands ? (
          /* ─── COMMANDS REFERENCE ─── */
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-8">
            <div className="flex items-center gap-2 mb-2">
              <Button variant="ghost" size="sm" onClick={() => setShowCommands(false)}>
                <ArrowLeft className="h-4 w-4 mr-1" weight="regular" />
                Back to guides
              </Button>
            </div>

            {Object.entries(quickReference).map(([trackSlug, categories]) => {
              const track = tracks.find((t) => t.slug === trackSlug);
              if (!track) return null;
              if (activeTrack !== "all" && trackSlug !== activeTrack) return null;
              const Icon = trackIcons[trackSlug] || BookOpen;

              return (
                <div key={trackSlug}>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="p-2 rounded-xl bg-emerald-100 dark:bg-emerald-900/20">
                      <Icon className="h-4 w-4 text-emerald-600 dark:text-emerald-400" weight="fill" />
                    </div>
                    <h2 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">{track.name}</h2>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {categories.map((cat) => (
                      <div key={cat.category} className="bento-card">
                        <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 mb-3 flex items-center gap-2">
                          <Terminal className="h-3.5 w-3.5 text-emerald-500" weight="fill" />
                          {cat.category}
                        </h3>
                        <div className="flex items-center gap-2 mb-2">
                          <div className="flex items-center gap-1.5">
                            {/* Animated terminal button */}
                            <button
                              onClick={() => {
                                setActiveTerminal(
                                  activeTerminal?.trackSlug === trackSlug && activeTerminal?.category === cat.category
                                    ? null
                                    : { trackSlug, category: cat.category }
                                );
                                setLiveTerminal(null);
                              }}
                              className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[10px] font-mono font-medium transition-all duration-200 ${
                                activeTerminal?.trackSlug === trackSlug && activeTerminal?.category === cat.category
                                  ? "bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400"
                                  : "bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 hover:bg-emerald-100 dark:hover:bg-emerald-900/20 hover:text-emerald-600 dark:hover:text-emerald-400"
                              }`}
                            >
                              <Terminal className="h-3 w-3" weight="bold" />
                              {activeTerminal?.trackSlug === trackSlug && activeTerminal?.category === cat.category
                                ? "Close"
                                : "Animated"}
                            </button>
                            {/* Live terminal button — FRRouting VTYSH */}
                            <button
                              onClick={() => {
                                setLiveBackend("vtysh");
                                setLiveTerminal(
                                  liveTerminal?.trackSlug === trackSlug && liveTerminal?.category === cat.category
                                    ? null
                                    : { trackSlug, category: cat.category }
                                );
                                setActiveTerminal(null);
                              }}
                              className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[10px] font-mono font-medium transition-all duration-200 ${
                                liveTerminal?.trackSlug === trackSlug && liveTerminal?.category === cat.category && liveBackend === "vtysh"
                                  ? "bg-sky-100 dark:bg-sky-900/30 text-sky-600 dark:text-sky-400"
                                  : "bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 hover:bg-sky-100 dark:hover:bg-sky-900/20 hover:text-sky-600 dark:hover:text-sky-400"
                              }`}
                            >
                              <Command className="h-3 w-3" weight="bold" />
                              {liveTerminal?.trackSlug === trackSlug && liveTerminal?.category === cat.category && liveBackend === "vtysh"
                                ? "Close"
                                : "VTYSH"}
                              {/* Status indicator */}
                              {sandboxStatus && (
                                <span className={`inline-flex items-center gap-1 ml-1 px-1.5 py-0.5 rounded-full text-[8px] font-semibold uppercase tracking-wider ${
                                  sandboxStatus.vtysh === "running"
                                    ? "bg-emerald-500/20 text-emerald-600 dark:text-emerald-400"
                                    : "bg-red-500/20 text-red-500"
                                }`}>
                                  <span className={`w-1.5 h-1.5 rounded-full ${
                                    sandboxStatus.vtysh === "running"
                                      ? "bg-emerald-500"
                                      : "bg-red-500"
                                  }`} />
                                  {sandboxStatus.vtysh === "running" ? "Online" : "Offline"}
                                </span>
                              )}
                            </button>
                            {/* cRPD JunOS CLI button (requires crpd image) */}
                            <button
                              onClick={() => {
                                setLiveBackend("junos");
                                setLiveTerminal(
                                  liveTerminal?.trackSlug === trackSlug && liveTerminal?.category === cat.category
                                    ? null
                                    : { trackSlug, category: cat.category }
                                );
                                setActiveTerminal(null);
                              }}
                              className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[10px] font-mono font-medium transition-all duration-200 ${
                                liveTerminal?.trackSlug === trackSlug && liveTerminal?.category === cat.category && liveBackend === "junos"
                                  ? "bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400"
                                  : "bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 hover:bg-amber-100 dark:hover:bg-amber-900/20 hover:text-amber-600 dark:hover:text-amber-400"
                              }`}
                            >
                              <Terminal className="h-3 w-3" weight="bold" />
                              {liveTerminal?.trackSlug === trackSlug && liveTerminal?.category === cat.category && liveBackend === "junos"
                                ? "Close"
                                : "cRPD"}
                              {/* Status indicator */}
                              {sandboxStatus && (
                                <span className={`inline-flex items-center gap-1 ml-1 px-1.5 py-0.5 rounded-full text-[8px] font-semibold uppercase tracking-wider ${
                                  sandboxStatus.junos === "running"
                                    ? "bg-emerald-500/20 text-emerald-600 dark:text-emerald-400"
                                    : "bg-red-500/20 text-red-500"
                                }`}>
                                  <span className={`w-1.5 h-1.5 rounded-full ${
                                    sandboxStatus.junos === "running"
                                      ? "bg-emerald-500"
                                      : "bg-red-500"
                                  }`} />
                                  {sandboxStatus.junos === "running" ? "Online" : "Offline"}
                                </span>
                              )}
                            </button>
                          </div>
                        </div>
                        <div className="space-y-1.5">
                          {cat.commands.map((cmd, idx) => (
                            <div
                              key={idx}
                              className="flex items-center justify-between gap-2 py-1.5 px-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 group text-xs"
                            >
                              <div className="flex items-center gap-2 min-w-0">
                                <code className="font-mono text-emerald-600 dark:text-emerald-400 whitespace-nowrap shrink-0">
                                  {cmd.cmd}
                                </code>
                                <span className="text-zinc-500 dark:text-zinc-400 truncate">{cmd.description}</span>
                              </div>
                              <button
                                onClick={() => {
                                  navigator.clipboard.writeText(cmd.cmd);
                                  setCopiedIdx(idx);
                                  setTimeout(() => setCopiedIdx(null), 1500);
                                }}
                                className="shrink-0 p-1 rounded opacity-0 group-hover:opacity-100 hover:bg-zinc-200 dark:hover:bg-zinc-700 transition-all"
                              >
                                {copiedIdx === idx ? (
                                  <Check className="h-3 w-3 text-emerald-400" weight="bold" />
                                ) : (
                                  <Copy className="h-3 w-3 text-zinc-400" weight="regular" />
                                )}
                              </button>
                            </div>
                          ))}
                        </div>
                        {/* Animated terminal for this category */}
                        {activeTerminal?.trackSlug === trackSlug && activeTerminal?.category === cat.category && (
                          <AnimatedTerminal
                            commands={cat.commands}
                            onClose={() => setActiveTerminal(null)}
                          />
                        )}
                        {/* Live terminal for this category (real FRR VTYSH / cRPD CLI) */}
                        {liveTerminal?.trackSlug === trackSlug && liveTerminal?.category === cat.category && (
                          <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 320 }}
                            exit={{ opacity: 0, height: 0 }}
                            className={`overflow-hidden rounded-xl border mb-4 ${
                              liveBackend === "junos"
                                ? "border-amber-700/50"
                                : "border-sky-700/50"
                            }`}
                          >
                            {/* Terminal chrome */}
                            <div className={`flex items-center justify-between px-4 py-2 bg-zinc-900 border-b ${
                              liveBackend === "junos"
                                ? "border-amber-700/50"
                                : "border-sky-700/50"
                            }`}>
                              <div className="flex items-center gap-2">
                                <div className="w-3 h-3 rounded-full bg-red-500/80" />
                                <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
                                <div className="w-3 h-3 rounded-full bg-emerald-500/80" />
                                <span className="ml-2 text-xs text-zinc-500 font-mono">
                                  {liveBackend === "junos" ? "cRPD — JunOS CLI" : "FRR — VTYSH CLI"}
                                </span>
                              </div>
                              <div className="flex items-center gap-2">
                                {/* Dynamic status indicator */}
                                {sandboxStatus ? (
                                  <span className={`inline-flex items-center gap-1.5 text-[10px] font-mono font-medium ${
                                    (liveBackend === "vtysh" && sandboxStatus.vtysh === "running") ||
                                    (liveBackend === "junos" && sandboxStatus.junos === "running")
                                      ? "text-emerald-500"
                                      : "text-red-400"
                                  }`}>
                                    <span className={`w-2 h-2 rounded-full ${
                                      (liveBackend === "vtysh" && sandboxStatus.vtysh === "running") ||
                                      (liveBackend === "junos" && sandboxStatus.junos === "running")
                                        ? "bg-emerald-500"
                                        : "bg-red-400"
                                    }`} />
                                    {(liveBackend === "vtysh" && sandboxStatus.vtysh === "running") ||
                                     (liveBackend === "junos" && sandboxStatus.junos === "running")
                                      ? "Connected"
                                      : "Disconnected"}
                                  </span>
                                ) : (
                                  <span className="text-[10px] text-zinc-500 font-mono">
                                    Checking...
                                  </span>
                                )}
                                <button
                                  onClick={() => setLiveTerminal(null)}
                                  className="p-1 rounded hover:bg-zinc-700 text-zinc-400 hover:text-zinc-200 transition-all"
                                >
                                  <CaretDown className="h-4 w-4" weight="bold" />
                                </button>
                              </div>
                            </div>
                            {/* Interactive terminal */}
                            <div className="h-[280px]">
                              <LabTerminal
                                key={`${liveBackend}-${trackSlug}-${cat.category}`}
                                deviceName={liveBackend === "junos" ? "crpd" : "frr"}
                                wsUrl={liveBackend === "junos" ? junosWsUrl : vtyshWsUrl}
                                className="h-full rounded-none border-0"
                              />
                            </div>
                          </motion.div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </motion.div>
        ) : (
          <div className="flex gap-8">
            {/* ─── Sidebar ─── */}
            <div className="w-64 shrink-0 hidden lg:block">
              <div className="sticky top-24 space-y-1">
                {filteredGuides.map((guide) => (
                  <button
                    key={guide.id}
                    onClick={() => setActiveGuide(guide.id)}
                    className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-all duration-200 ${
                      activeGuide === guide.id
                        ? "bg-emerald-100 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-300 font-medium"
                        : "text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800"
                    }`}
                  >
                    <div className="flex items-center gap-2">
                      {completedGuides.has(guide.id) ? (
                        <CheckCircle className="h-3.5 w-3.5 shrink-0 text-emerald-500" weight="fill" />
                      ) : (
                        <Circle className="h-3.5 w-3.5 shrink-0 text-zinc-400" weight="regular" />
                      )}
                      <span className={`truncate ${completedGuides.has(guide.id) ? 'text-emerald-600 dark:text-emerald-400' : ''}`}>
                        {guide.title}
                      </span>
                    </div>
                    <div className="flex gap-1.5 mt-1 ml-5.5">
                      <Badge variant="outline" className="text-[10px] px-1 py-0">{guide.level}</Badge>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* ─── Guide Content ─── */}
            <div className="flex-1 min-w-0">
              {currentGuide ? (
                <motion.div
                  key={currentGuide.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="space-y-6"
                >
                  {/* Guide header */}
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <Badge variant="secondary">{currentGuide.level}</Badge>
                      <Badge variant="outline">{currentGuide.technology}</Badge>
                    </div>
                    <div className="flex items-center justify-between gap-4">
                      <h2 className="text-2xl font-bold text-zinc-900 dark:text-zinc-100 mb-1">
                        {currentGuide.title}
                      </h2>
                      <button
                        onClick={() => toggleProgress(currentGuide.id)}
                        disabled={savingGuides.has(currentGuide.id)}
                        className={`shrink-0 flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-200 ${
                          completedGuides.has(currentGuide.id)
                            ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-300"
                            : "bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700"
                        }`}
                      >
                        {completedGuides.has(currentGuide.id) ? (
                          <>
                            <CheckCircle className="h-4 w-4" weight="fill" />
                            {savingGuides.has(currentGuide.id) ? "Saving..." : "Completed"}
                          </>
                        ) : (
                          <>
                            <Circle className="h-4 w-4" weight="regular" />
                            {savingGuides.has(currentGuide.id) ? "Saving..." : "Mark as completed"}
                          </>
                        )}
                      </button>
                    </div>
                    <p className="text-sm text-zinc-500 dark:text-zinc-400">{currentGuide.summary}</p>
                  </div>

                  {/* Sections */}
                  {currentGuide.sections.map((section, idx) => (
                    <div key={idx} className="space-y-2">
                      {section.type === "code" || section.type === "command" ? (
                        <>
                          {section.title && (
                            <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-200 flex items-center gap-2">
                              <Code className="h-3.5 w-3.5 text-emerald-500" weight="fill" />
                              {section.title}
                            </h3>
                          )}
                          <SectionBlock section={section} />
                        </>
                      ) : (
                        <div className={`${section.type === "text" ? "" : "space-y-1"}`}>
                          {section.title && (
                            <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-200 mb-1.5">
                              {section.title}
                            </h3>
                          )}
                          <SectionBlock section={section} />
                        </div>
                      )}
                    </div>
                  ))}

                  {/* Mobile guide navigation */}
                  <div className="flex items-center justify-between pt-6 border-t border-zinc-200 dark:border-zinc-800 mt-8">
                    <div className="flex gap-1">
                      {filteredGuides.map((g) => (
                        <button
                          key={g.id}
                          onClick={() => setActiveGuide(g.id)}
                          className={`w-2 h-2 rounded-full transition-all ${
                            activeGuide === g.id
                              ? "bg-emerald-500 w-4"
                              : "bg-zinc-300 dark:bg-zinc-600"
                          }`}
                        />
                      ))}
                    </div>
                  </div>
                </motion.div>
              ) : (
                <div className="text-center py-16">
                  <BookOpen className="h-16 w-16 mx-auto mb-4 text-zinc-300 dark:text-zinc-600" weight="light" />
                  <h2 className="text-xl font-semibold text-zinc-900 dark:text-zinc-100 mb-2">No guides found</h2>
                  <p className="text-zinc-500 dark:text-zinc-400">Try changing filters or search query.</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}


