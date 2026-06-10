# Micro-Lab 03: EBGP Peering

## 🎯 Objective
Настроить EBGP peering между тремя автономными системами (AS65001, AS65002, AS65003), настроить экспорт маршрутов и проверить BGP-таблицу.

## ⏱ Duration: 15-20 минут

## 📋 Topology
```
AS65001        AS65002        AS65003
┌─────┐  10.0.12.0/30  ┌─────┐  10.0.23.0/30  ┌─────┐
│ R1  │────────────────│ R2  │────────────────│ R3  │
│1.1.1.1│  EBGP       │2.2.2.2│  EBGP       │3.3.3.3│
└─────┘               └─────┘               └─────┘
```

## 📝 Tasks

### Task 1: Configure EBGP on R1 → R2 (4 minutes)
```junos
configure
set protocols bgp group EBGP-TO-R2 type external
set protocols bgp group EBGP-TO-R2 peer-as 65002
set protocols bgp group EBGP-TO-R2 neighbor 10.0.12.2
set protocols bgp group EBGP-TO-R2 local-address 10.0.12.1
commit
```

**Checkpoint:** `show bgp summary` — R1 должен видеть R2 в состоянии `Established`.

### Task 2: Configure EBGP on R2 → R1 and R2 → R3 (4 minutes)
На R2 настройте EBGP с R1 (AS65001) и R3 (AS65003):

```junos
configure
set protocols bgp group EBGP-TO-R1 type external
set protocols bgp group EBGP-TO-R1 peer-as 65001
set protocols bgp group EBGP-TO-R1 neighbor 10.0.12.1
set protocols bgp group EBGP-TO-R1 local-address 10.0.12.2

set protocols bgp group EBGP-TO-R3 type external
set protocols bgp group EBGP-TO-R3 peer-as 65003
set protocols bgp group EBGP-TO-R3 neighbor 10.0.23.3
set protocols bgp group EBGP-TO-R3 local-address 10.0.23.2
commit
```

### Task 3: Configure EBGP on R3 → R2 (3 minutes)
```junos
configure
set protocols bgp group EBGP-TO-R2 type external
set protocols bgp group EBGP-TO-R2 peer-as 65002
set protocols bgp group EBGP-TO-R2 neighbor 10.0.23.2
set protocols bgp group EBGP-TO-R2 local-address 10.0.23.3
commit
```

### Task 4: Advertise Loopback Routes (3 minutes)
Добавьте экспорт loopback-маршрутов в BGP на каждом роутере:

**R1:**
```junos
configure
set policy-options policy-statement EXPORT-BGP term LOOPBACK from protocol direct
set policy-options policy-statement EXPORT-BGP term LOOPBACK from route-filter 1.1.1.1/32 exact
set policy-options policy-statement EXPORT-BGP term LOOPBACK then accept
set protocols bgp group EBGP-TO-R2 export EXPORT-BGP
commit
```

**R2:**
```junos
configure
set policy-options policy-statement EXPORT-BGP term LOOPBACK from protocol direct
set policy-options policy-statement EXPORT-BGP term LOOPBACK from route-filter 2.2.2.2/32 exact
set policy-options policy-statement EXPORT-BGP term LOOPBACK then accept
set protocols bgp group EBGP-TO-R1 export EXPORT-BGP
set protocols bgp group EBGP-TO-R3 export EXPORT-BGP
commit
```

**R3:**
```junos
configure
set policy-options policy-statement EXPORT-BGP term LOOPBACK from protocol direct
set policy-options policy-statement EXPORT-BGP term LOOPBACK from route-filter 3.3.3.3/32 exact
set policy-options policy-statement EXPORT-BGP term LOOPBACK then accept
set protocols bgp group EBGP-TO-R2 export EXPORT-BGP
commit
```

### Task 5: Verify BGP Routes (3 minutes)
Проверьте BGP-таблицы и достижимость:

```junos
show bgp summary
show route protocol bgp
show route 3.3.3.3          # на R1
show route 1.1.1.1          # на R3
ping 3.3.3.3 count 3        # с R1
ping 1.1.1.1 count 3        # с R3
```

**Checkpoint:** R1 должен видеть 3.3.3.3/32 с AS-path `[65002 65003]`.

## 💡 Hints

<details>
<summary>Hint 1: BGP не в Established? Проверьте первое</summary>

1. Ping до IP соседа — проверьте L3 connectivity
2. `show bgp summary` — смотрите столбец State
3. Проверьте AS-номер: peer-as должен совпадать с remote AS
</details>

<details>
<summary>Hint 2: AS-path verification</summary>

`show route protocol bgp` покажет AS-path в формате `[AS-path]`.
R1 → 3.3.3.3 должен показывать `[65002 65003]` — два AS hop'a.
</details>

<details>
<summary>Hint 3: Почему маршрут не анонсируется?</summary>

EBGP по умолчанию не анонсирует маршруты — нужен explicit `export` policy.
Проверьте `show configuration protocols bgp` — есть ли export policy.
</details>

## ✅ Success Criteria

| Критерий | Проверка |
|----------|----------|
| 1. Все три BGP сессии Established | `show bgp summary` — 2 peers на R2, 1 peer на R1/R3 |
| 2. Loopback маршруты в BGP | `show route protocol bgp` показывает все 3 loopback'а |
| 3. AS-path корректен | R1 видит 3.3.3.3 с AS-path [65002 65003] |
| 4. Ping across AS | С R1 до 3.3.3.3 и с R3 до 1.1.1.1 — success |

## 🔗 Связанные темы

- [Juniper — BGP Configuration Guide](https://www.juniper.net/documentation/us/en/software/junos/bgp/topics/)
- [RFC 4271 — BGP-4](https://datatracker.ietf.org/doc/html/rfc4271)
- [BGP AS-path Basics](https://www.juniper.net/documentation/us/en/software/junos/bgp/topics/concept/bgp-as-path-overview.html)
