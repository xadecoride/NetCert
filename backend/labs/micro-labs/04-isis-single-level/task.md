# Micro-Lab 04: IS-IS Single-Level

## 🎯 Objective
Настроить IS-IS (ISO 10589) Level 2 на трёх роутерах, сформировать adjacency, настроить NET (Network Entity Title), проверить IS-IS маршруты и определить DIS.

## ⏱ Duration: 15-20 минут

## 📋 Topology
```
                      Area 49.0001
    ┌─────┐  10.0.12.0/30  ┌─────┐
    │ R1  │────────────────│ R2  │
    │NET  │  ge-0/0/0     │NET  │
    │..001│                │..002│
    └──┬──┘                └──┬──┘
       │                      │
       │    10.0.13.0/30     │ 10.0.23.0/30
       │                      │
    ┌──┴──────────────────────┴──┐
    │           R3               │
    │         NET ..003         │
    └────────────────────────────┘
```

### NET Structure
Каждый роутер имеет NSAP-адрес (Network Service Access Point):
- `49.0001` — Area ID (private Area 49, Area 0x0001)
- `0010.0100.1001` — System ID (R1: 0010.0100.1001 = 1.1.1.1)
- `00` — SEL (Selector = 00 для NET)

## 📝 Tasks

### Task 1: Configure IS-IS on R1 (4 minutes)

IS-IS требует `family iso` на интерфейсах. В initial config уже настроены ISO-адреса. Вам нужно включить протокол IS-IS:

```junos
configure
set protocols isis level 2
set protocols isis interface ge-0/0/0.0 level 2
set protocols isis interface ge-0/0/1.0 level 2
set protocols isis interface lo0.0 passive
commit
```

Проверьте:
```junos
show isis interface
show isis adjacency
```

**Checkpoint:** R1 должен видеть IS-IS соседей.

### Task 2: Configure IS-IS on R2 (3 minutes)
```junos
configure
set protocols isis level 2
set protocols isis interface ge-0/0/0.0 level 2
set protocols isis interface ge-0/0/1.0 level 2
set protocols isis interface lo0.0 passive
commit
```

### Task 3: Configure IS-IS on R3 (3 minutes)
```junos
configure
set protocols isis level 2
set protocols isis interface ge-0/0/0.0 level 2
set protocols isis interface ge-0/0/1.0 level 2
set protocols isis interface lo0.0 passive
commit
```

### Task 4: Verify IS-IS Adjacencies (3 minutes)
На каждом роутере проверьте соседей:
```junos
show isis adjacency detail
show isis hostname
```

**Checkpoint:** Все adjacency должны быть в состоянии `Up`. Обратите внимание на поле `DIS`.

### Task 5: Verify IS-IS Routes (3 minutes)
Проверьте IS-IS маршруты и end-to-end connectivity:
```junos
show route protocol isis
show isis route
ping 2.2.2.2 count 3
ping 3.3.3.3 count 3
```

**Checkpoint:** IS-IS маршруты до всех loopback'ов должны быть в таблице маршрутизации.

## 💡 Hints

<details>
<summary>Hint 1: Что такое NET и NSAP?</summary>

NET = Network Entity Title — идентификатор роутера в IS-IS.
Формат: `Area.SystemID.SEL`
- Area: 49.0001 (private area)
- SystemID: 6 байт, уникальный для каждого роутера
- SEL: всегда 00 для NET
</details>

<details>
<summary>Hint 2: Почему adjacency не Up?</summary>

1. На всех интерфейсах должна быть включена `family iso`
2. Level должен совпадать (все Level 2)
3. MTU не менее 1500 (IS-IS требует min 1492)
4. Hello-таймеры: по умолчанию Level 2 = 10s, Level 1 = 3.3s
</details>

<details>
<summary>Hint 3: Что такое DIS?</summary>

Designated IS — аналог DR в OSPF.
- Выбирается на broadcast-сегментах (не point-to-point)
- DIS отправляет CSNP каждые 10 секунд
- DIS может быть принудительно выбран через priority
</details>

## ✅ Success Criteria

| Критерий | Проверка |
|----------|----------|
| 1. IS-IS adjacencies Up | `show isis adjacency` — все соседи в Up |
| 2. IS-IS hostnames видны | `show isis hostname` — все имена отображаются |
| 3. Маршруты IS-IS в таблице | `show route protocol isis` — маршруты до всех loopback |
| 4. Ping всех loopback | 100% success rate |

## 🔗 Связанные темы

- [Juniper — IS-IS Configuration Guide](https://www.juniper.net/documentation/us/en/software/junos/isis/topics/)
- [RFC 1195 — Integrated IS-IS for TCP/IP](https://datatracker.ietf.org/doc/html/rfc1195)
- [ISO 10589 — IS-IS Protocol Specification](https://www.iso.org/standard/65445.html)
- [IS-IS NET Addressing](https://www.juniper.net/documentation/us/en/software/junos/isis/topics/concept/isis-net-address-overview.html)
