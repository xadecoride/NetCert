# Micro-Lab 05: MPLS LSP

## 🎯 Objective
Настроить MPLS на сети из трёх роутеров, запустить LDP (Label Distribution Protocol) для автоматического распределения меток, проверить LSP (Label Switched Path) и убедиться, что MPLS-коммутация работает.

## ⏱ Duration: 20-25 минут

## 📋 Topology
```
    ┌─────┐  10.0.12.0/30  ┌───┐  10.0.23.0/30  ┌─────┐
    │ PE1 │────────────────│ P │────────────────│ PE2 │
    │1.1.1.1│    MPLS     │2.2.2.2│    MPLS     │3.3.3.3│
    └─────┘               └───┘               └─────┘
         ^                    ^                    ^
      Ingress LSR          Transit LSR          Egress LSR
      (LER)
```

## 📝 Prerequisites
Перед настройкой MPLS необходимо базовое IGP (внутренний протокол маршрутизации) — используем OSPF или IS-IS для обеспечения IP-связности внутри MPLS-домена.

## 📝 Tasks

### Task 1: Configure IGP (OSPF) (5 minutes)
Настройте OSPF на всех трёх роутерах для обеспечения IP-связности:

**PE1:**
```junos
configure
set protocols ospf area 0 interface ge-0/0/0.0
set protocols ospf area 0 interface lo0.0 passive
commit
```

**P:**
```junos
configure
set protocols ospf area 0 interface ge-0/0/0.0
set protocols ospf area 0 interface ge-0/0/1.0
set protocols ospf area 0 interface lo0.0 passive
commit
```

**PE2:**
```junos
configure
set protocols ospf area 0 interface ge-0/0/0.0
set protocols ospf area 0 interface lo0.0 passive
commit
```

**Checkpoint:** `show route protocol ospf` — каждый роутер должен видеть все loopback'ы.

### Task 2: Enable MPLS on Interfaces (3 minutes)
Включите MPLS на всех интерфейсах (семейство mpls уже добавлено в initial config, но MPLS-протокол нужно активировать):

**На всех роутерах:**
```junos
configure
set protocols mpls interface ge-0/0/0.0
commit
```

**На P (транзитном роутере) дополнительно:**
```junos
set protocols mpls interface ge-0/0/1.0
commit
```

### Task 3: Enable LDP (4 minutes)
LDP будет автоматически распределять метки между MPLS-соседями:

**PE1:**
```junos
configure
set protocols ldp interface ge-0/0/0.0
set protocols ldp interface lo0.0
commit
```

**P:**
```junos
configure
set protocols ldp interface ge-0/0/0.0
set protocols ldp interface ge-0/0/1.0
set protocols ldp interface lo0.0
commit
```

**PE2:**
```junos
configure
set protocols ldp interface ge-0/0/0.0
set protocols ldp interface lo0.0
commit
```

**Checkpoint:** `show ldp session` — должны быть LDP-сессии между соседями в состоянии `Operational`.

### Task 4: Verify MPLS (4 minutes)
Проверьте MPLS LSP и метки:

```junos
show mpls lsp                  # LSP status
show mpls lsp ingress          # На PE1 — ingress LSP
show mpls lsp egress           # На PE2 — egress LSP
show route label-switched-path # MPLS-маршруты
show ldp database              # LDP label database
```

**Checkpoint:** На PE1 должен быть LSP до 3.3.3.3 в состоянии `Up`.

### Task 5: Verify Label Switching (3 minutes)
Проверьте, как проходят метки через транзитный роутер:

```junos
# На P (транзит):
show mpls lsp transit

# На PE1 проверьте маршрут с меткой:
show route 3.3.3.3

# Проверьте MPLS connectivity:
ping 3.3.3.3 count 3
```

**Checkpoint:** P должен иметь transport LSP. Маршрут до 3.3.3.3 на PE1 должен показывать метку.

### Bonus Task: MPLS Traceroute (2 minutes)
Проверьте MPLS path:

```junos
traceroute 3.3.3.3
```

**Checkpoint:** Traceroute должен показывать MPLS-метки на каждом hop'е.

## 💡 Hints

<details>
<summary>Hint 1: Почему LDP session не поднимается?</summary>

1. Должен быть IGP (OSPF/IS-IS) между LDP-пирами для IP-связности
2. На интерфейсах должна быть включена `family mpls`
3. LDP использует UDP port 646 (discovery) + TCP 646 (session)
4. LDP Router ID должен быть reachable (обычно loopback)
</details>

<details>
<summary>Hint 2: LDP vs RSVP-TE</summary>

В этой лабе мы используем LDP — простой протокол распределения меток без TE.
- LDP: автоматически, без трафика сигнализации, по кратчайшему пути IGP
- RSVP-TE: ручное (или CSPF) управление путём LSP, резервирование bandwidth
</details>

<details>
<summary>Hint 3: Label Operations (PHP)</summary>

- **Ingress (PE1):** Push метку → отправляет пакет с меткой
- **Transit (P):** Swap метку → меняет входящую на исходящую
- **Egress (PE2):** Pop метку (PHP) → отдаёт IP-пакет без метки
</details>

## ✅ Success Criteria

| Критерий | Проверка |
|----------|----------|
| 1. OSPF маршруты в таблице | Все 3 loopback видны через OSPF |
| 2. LDP sessions Operational | `show ldp session` — все сессии Operational |
| 3. MPLS LSP Up | `show mpls lsp` — LSP до PE2 в состоянии Up |
| 4. LDP label database | `show ldp database` — метки распределены |
| 5. Ping через MPLS | ping 3.3.3.3 success rate 100% |

## 🔗 Связанные темы

- [Juniper — MPLS Configuration Guide](https://www.juniper.net/documentation/us/en/software/junos/mpls/topics/)
- [RFC 5036 — LDP Specification](https://datatracker.ietf.org/doc/html/rfc5036)
- [RFC 3031 — MPLS Architecture](https://datatracker.ietf.org/doc/html/rfc3031)
- [MPLS Label Operations](https://www.juniper.net/documentation/us/en/software/junos/mpls/topics/concept/mpls-label-operations-overview.html)
- [Juniper — Configuring LDP](https://www.juniper.net/documentation/us/en/software/junos/mpls/topics/task/mpls-ldp-configuring.html)
