# Micro-Lab 02: OSPF Adjacency

## 🎯 Objective
Настроить OSPFv2 (RFC 2328) в Area 0 на трёх роутерах, сформировать adjacency, проверить обмен маршрутами и понять механизм DR/BDR election.

## ⏱ Duration: 15-20 минут

## 📋 Topology
```
                     Area 0
    ┌─────┐  10.0.12.0/30  ┌─────┐
    │ R1  │────────────────│ R2  │
    │1.1.1.1│  ge-0/0/0   │2.2.2.2│
    └──┬──┘                └──┬──┘
       │                      │
       │    10.0.13.0/30     │ 10.0.23.0/30
       │                      │
    ┌──┴──────────────────────┴──┐
    │           R3               │
    │         3.3.3.3            │
    └────────────────────────────┘
```

## 📝 Tasks

### Task 1: Configure OSPF on R1 (4 minutes)
Настройте OSPF Area 0 на всех интерфейсах R1:

```junos
configure
set protocols ospf area 0 interface ge-0/0/0.0
set protocols ospf area 0 interface ge-0/0/1.0
set protocols ospf area 0 interface lo0.0 passive
commit
```

Проверьте:
```junos
show ospf interface
show ospf neighbor
```

**Checkpoint:** R1 должен видеть соседей R2 и R3 в состоянии `Full`.

### Task 2: Configure OSPF on R2 (3 minutes)
Настройте OSPF Area 0 на R2:

```junos
configure
set protocols ospf area 0 interface ge-0/0/0.0
set protocols ospf area 0 interface ge-0/0/1.0
set protocols ospf area 0 interface lo0.0 passive
commit
```

**Checkpoint:** Выполните `show ospf neighbor` — должны быть соседи с R1 и R3.

### Task 3: Configure OSPF on R3 (3 minutes)
Настройте OSPF Area 0 на R3:

```junos
configure
set protocols ospf area 0 interface ge-0/0/0.0
set protocols ospf area 0 interface ge-0/0/1.0
set protocols ospf area 0 interface lo0.0 passive
commit
```

### Task 4: Verify OSPF Routes (3 minutes)
Проверьте, что все маршруты обмениваются:

```junos
show route protocol ospf
show ospf route
show route 2.2.2.2
```

**Checkpoint:** R1 должен видеть маршруты до loopback R2 (2.2.2.2/32) и R3 (3.3.3.3/32).

### Task 5: Identify DR/BDR (2 minutes)
Определите, кто является Designated Router (DR) и Backup DR:

```junos
show ospf neighbor detail
```

**Checkpoint:** Oбратите внимание на поля `DR` и `BDR` в выводе.

### Task 6: Ping Test (2 minutes)
Проверьте end-to-end connectivity:

```junos
ping 2.2.2.2 count 3
ping 3.3.3.3 count 3
```

## 💡 Hints

<details>
<summary>Hint 1: Как проверить OSPF adjacency?</summary>

`show ospf neighbor` — покажет всех соседей. Состояние должно быть `Full`.

Если сосед в состоянии `Init` или `ExStart` — проблема с конфигурацией.
</details>

<details>
<summary>Hint 2: Почему не формируется adjacency?</summary>

Проверьте:
1. Интерфейсы в status up: `show interfaces terse`
2. Правильные IP-адреса в одной подсети
3. OSPF Area совпадает (все должны быть в Area 0)
4. Нет ACL/firewall, блокирующих OSPF (protocol 89)
</details>

<details>
<summary>Hint 3: Что такое passive interface?</summary>

`passive` означает, что OSPF анонсирует сеть, но не отправляет hello-пакеты. Используется на loopback и интерфейсах, где нет OSPF-соседей.
</details>

## ✅ Success Criteria

| Критерий | Проверка |
|----------|----------|
| 1. Все три adjacency Full | `show ospf neighbor` — 2 соседа на каждом в Full |
| 2. Маршруты OSPF есть | `show route protocol ospf` показывает 2.2.2.2/32 и 3.3.3.3/32 |
| 3. DR/BDR определены | `show ospf neighbor detail` показывает DR ≠ BDR |
| 4. Ping до всех | ping до 2.2.2.2 и 3.3.3.3 success rate 100% |

## 🔗 Связанные темы

- [Juniper — OSPF Configuration Guide](https://www.juniper.net/documentation/us/en/software/junos/ospf/topics/)
- [RFC 2328 — OSPFv2](https://datatracker.ietf.org/doc/html/rfc2328)
- [OSPF LSA Types Overview](https://www.juniper.net/documentation/us/en/software/junos/ospf/topics/concept/ospf-lsa-types-overview.html)
