Below is a **single README.md-style document** that summarizes **everything discussed so far (Day 1–Day 7)**.
It is **concise**, **interview-oriented**, and **beginner-safe**, with **theory (2–3 lines)**, **commands + examples**, **memory tips**, and a **debugging mind map**.

---

# Linux & DevOps Foundations – README

## Scope

This document covers:

* Linux processes, CPU, memory
* Disk & filesystem
* Networking basics
* Bash scripting
* Python for DevOps
* Automation & troubleshooting mindset

---

## Day 1 – Processes, CPU, Memory

### Theory (2–3 lines)

A **process** is a running program. CPU cores execute processes using time-sharing, while memory provides working space. Linux uses scheduling and context switching to fairly distribute CPU among processes.

### Key Concepts

* Process states: Running, Sleeping, Zombie
* CPU core = one execution unit
* Context switch = CPU switching between tasks

### Commands

```bash
top
ps -ef
vmstat 1
free -h
```

### Examples

```bash
ps -eo pid,cmd,%cpu --sort=-%cpu | head
vmstat 1
```

### Tips to Remember

* **High CPU ≠ app bug always** → check I/O wait
* **Low free memory is normal** → check `available`
* Zombies don’t use CPU, only PIDs

---

## Day 2 – Disk, Filesystem, systemd

### Theory

Files are stored using **inodes**, not filenames. Disk can appear full due to inode exhaustion, open-but-deleted files, or reserved blocks. systemd manages services and logs.

### Key Concepts

* Inode = file metadata
* Disk space and inodes are independent
* Open file still consumes space

### Commands

```bash
df -h
df -i
lsof
journalctl
```

### Examples

```bash
df -i
lsof | grep deleted
journalctl -u nginx
```

### Tips to Remember

* **df -h shows space, df -i shows files**
* If space not freeing → check `lsof`
* systemd logs can fill disk

---

## Day 3 – Networking Basics

### Theory

Applications communicate using IP + port. TCP ensures reliable communication using a 3-way handshake. DNS resolves names to IPs, and NAT translates private to public IPs.

### Key Concepts

* TCP handshake: SYN → SYN-ACK → ACK
* DNS failure can break apps even if server is up
* NAT is common in cloud & containers

### Commands

```bash
ss -tuln
netstat -tulnp
tcpdump
```

### Examples

```bash
ss -tuln | grep 8080
tcpdump port 80
```

### Tips to Remember

* Process running ≠ port listening
* Port listening ≠ reachable
* Reachable ≠ DNS correct

---

## Day 4 – Bash Scripting

### Theory

Bash is used for system automation. Loops repeat actions, functions organize logic, and exit codes indicate success or failure.

### Key Concepts

* `0` = success, non-zero = failure
* Cron runs with minimal environment
* Absolute paths matter

### Commands / Constructs

```bash
for, while
function_name() {}
$?
set -x
```

### Examples

```bash
if df -h | grep -q 90%; then
  echo "Disk alert"
fi
```

### Tips to Remember

* Always check exit codes in scripts
* Cron failures are usually path/env issues
* Debug with `set -x`

---

## Day 5 – Python for DevOps

### Theory

Python is preferred for APIs, JSON, and complex logic. It offers better error handling and readability compared to Bash.

### Key Concepts

* `requests` for APIs
* JSON for structured data
* `subprocess` to run system commands

### Examples

```python
import requests
r = requests.get("https://api.example.com")
data = r.json()
print(data["status"])
```

```python
import subprocess
subprocess.run(["df", "-h"])
```

### Tips to Remember

* Bash → quick system tasks
* Python → APIs, parsing, retries, logic
* Python scales better for automation

---

## Day 6 – Combined Automation

### Theory

Automation combines system data, logic, and alerting. Design should focus on reliability, idempotency, and clarity.

### Example Use Case

* Parse logs
* Count errors
* Alert if threshold exceeded

### Design Principles

* Clear input/output
* Error handling
* Avoid duplicate alerts
* Logging for debugging

### Tips to Remember

* Think in **input → process → output**
* Design before coding
* Prefer maintainability over shortcuts

---

## Day 7 – Revision & Cheatsheet

### Must-Know Commands

```bash
top
df -h
df -i
ss -tuln
lsof
journalctl
```

### Bash

```bash
$?        # exit code
set -x    # debug
```

### Python

```python
requests.get()
response.json()
subprocess.run()
```

---

## Debugging Mind Map (Mental Model)

```
Problem
 |
 +-- Is app slow/unreachable?
     |
     +-- CPU?
     |    |
     |    +-- High user CPU → app bug
     |    +-- High iowait → disk issue
     |
     +-- Memory?
     |    |
     |    +-- Swap used → memory pressure
     |
     +-- Disk?
     |    |
     |    +-- df -h (space)
     |    +-- df -i (inodes)
     |    +-- lsof deleted
     |
     +-- Network?
     |    |
     |    +-- ss (port listening)
     |    +-- firewall
     |    +-- DNS
     |
     +-- Automation?
          |
          +-- cron logs
          +-- exit codes
          +-- paths/env
```

---

## Interview Golden Rule

> Always explain **what you check first**, **why**, and **what the result tells you**. Commands matter less than reasoning.

---

If you want, next I can:

* Create a **printable one-page cheat sheet**
* Provide **mock interview Q&A**
* Move to **advanced concepts (containers, Kubernetes, cloud internals)**
