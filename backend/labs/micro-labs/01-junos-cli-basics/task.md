# Micro-Lab 01: JunOS CLI Basics

## 🎯 Objective
Освоить базовые команды JunOS CLI: навигация между operational и configuration mode, настройка интерфейсов, проверка connectivity.

## ⏱ Duration: 10-15 minutes

## 📋 Topology
```
    ┌─────┐   10.0.12.0/30    ┌─────┐
    │ R1  │───────────────────│ R2  │
    │1.1.1.1│   ge-0/0/0     │2.2.2.2│
    └─────┘                   └─────┘
```

## 📝 Tasks

### Task 1: Explore Operational Mode (2 minutes)
Подключитесь к R1 через Web-терминал и выполните следующие команды:

```junos
show interfaces terse
show configuration
show version
show system uptime
```

**Checkpoint:** Вы должны увидеть интерфейсы `ge-0/0/0` и `lo0` в статусе `up`.

### Task 2: Configure Interface Description (3 minutes)
Перейдите в configuration mode на R1 и добавьте description к интерфейсу:

```junos
configure
set interfaces ge-0/0/0 unit 0 description "Link to R2"
commit
```

**Checkpoint:** Выполните `show interfaces description` — должна появиться строка с описанием.

### Task 3: Change Hostname (3 minutes)
На R2 измените hostname с `R2` на `R2-Core-1`:

```junos
configure
set system host-name R2-Core-1
commit
commit and-quit    # commit and exit to operational mode
```

**Checkpoint:** Приглашение CLI должно измениться на `R2-Core-1>`.

### Task 4: Verify Connectivity (3 minutes)
С R1 выполните ping до R2 (адрес 10.0.12.2):

```junos
ping 10.0.12.2 count 5
```

**Checkpoint:** Должен быть success rate 100% (5/5 packets received).

### Task 5: Save Configuration (2 minutes)
На любом устройстве сохраните конфигурацию в файл и проверьте содержимое:

```junos
save /tmp/my-config.txt
file show /tmp/my-config.txt
```

## 💡 Hints

<details>
<summary>Hint 1: Как перейти в configuration mode?</summary>

Введите `configure` в operational mode. Приглашение сменится с `>` на `#`.
</details>

<details>
<summary>Hint 2: Как проверить commit?</summary>

Используйте `commit check` перед `commit`, чтобы проверить конфигурацию без применения.
</details>

<details>
<summary>Hint 3: Как выйти из configuration mode?</summary>

Используйте `exit` configuration mode или `commit and-quit` для commit + exit.
</details>

## ✅ Success Criteria

| Критерий | Проверка |
|----------|----------|
| 1. Интерфейсы up | `show interfaces terse` показывает ge-0/0/0 и lo0 в status up |
| 2. Description добавлен | `show interfaces description` показывает описание для ge-0/0/0 |
| 3. Hostname изменён | Приглашение показывает `R2-Core-1>` |
| 4. Ping успешен | 5/5 echo-replies получено |
| 5. Конфиг сохранён | Файл /tmp/my-config.txt существует и не пуст |

## 🔗 Связанные темы

- JunOS CLI Guide: [Juniper TechLibrary — CLI User Guide](https://www.juniper.net/documentation/us/en/software/junos/cli/topics/)
- Configuration basics: [Juniper — Configuring Junos OS](https://www.juniper.net/documentation/us/en/software/junos/junos-basics/topics/)
