# Linux & Bash — DevSecOps Interview Quick Reference

> **How to use:** Skim section headers before the interview. Deep-dive only flagged `[INTERVIEW]` blocks. All `[GOTCHA]` items are common trick questions.

---

## TABLE OF CONTENTS

1. [Linux Commands — Must-Know Arsenal](#1-linux-commands)
2. [Bash Scripting — Non-Negotiables](#2-bash-scripting)
3. [Interview Q&A — Bash Deep Dives](#3-interview-qa-bash)
4. [Interview Q&A — Linux System](#4-interview-qa-linux-system)
5. [Quick-Fire Answers](#5-quick-fire-answers)
6. [Debugging Roadmap](#6-debugging-roadmap)

---

## 1. LINUX COMMANDS

### File System

```bash
find /var/log -mtime -1 -type f -name "*.log"          # files modified last 24h
find / -type f -size +100M 2>/dev/null                  # files >100MB
df -hT                                                  # disk usage + fs type
du -sh /var/log/* | sort -rh | head -20                 # top space consumers
df -i                                                   # inode usage (GOTCHA: disk full with space free = inode exhaustion)
```

### Process Investigation

```bash
ps aux --sort=-%mem | head -10      # top memory consumers
ps aux --sort=-%cpu | head -10      # top CPU consumers
ps auxf                             # process tree (forest view)
lsof -i :8080                       # who owns port 8080
lsof -p <PID>                       # all files a process has open
ps aux | awk '$8 == "Z"'            # zombie processes
```

### Networking

```bash
ss -tulnp                           # all listening ports + process (ss > netstat, netstat deprecated)
ss -tnp state established           # active TCP connections
ip route get 8.8.8.8                # which interface/gateway for a dest
tcpdump -i eth0 -n port 5432 -w /tmp/pg.pcap   # capture traffic
nc -zv <host> <port>                # raw TCP port test
curl -fsSL https://<host>           # fail-silent, follow redirects (CI-safe)
```

> **[INTERVIEW]** `netstat` is deprecated — always say `ss`. Interviewers notice.

### Log Analysis

```bash
tail -f /var/log/app.log | grep --line-buffered "ERROR"
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head -20   # top IPs
grep "ERROR" app.log | awk -F'ERROR' '{print $2}' | sort | uniq -c | sort -rn       # top errors
journalctl -u nginx --since "1 hour ago" --no-pager
journalctl -b -1 -p err             # errors from previous (crashed) boot
```

### Security Audit Commands

```bash
find / -perm -4000 -type f 2>/dev/null      # SUID binaries
find / -type f -perm -o+w 2>/dev/null       # world-writable files
sudo -l -U <username>                        # what a user can sudo
cat /proc/<PID>/environ                      # process env vars — may contain secrets
ls /proc/<PID>/fd | wc -l                   # open FD count for process
```

---

## 2. BASH SCRIPTING

### The Non-Negotiable Header

```bash
#!/usr/bin/env bash
set -euo pipefail
# -e  = exit on any error
# -u  = treat unset variables as errors
# -o pipefail = pipeline fails if ANY stage fails (not just last)

IFS=$'\n\t'   # safer word splitting

trap cleanup EXIT                          # always runs on any exit
trap 'echo "Error on line $LINENO"' ERR   # error line reporting

cleanup() { rm -f /tmp/script_$$.tmp; }
```

> **[GOTCHA]** `set -e` does NOT fire for commands in `if` conditions, `||`, `&&` chains, or subshells. Use explicit `|| exit 1` in those contexts.

### Variable Patterns

```bash
APP_ENV="${APP_ENV:-staging}"          # default if unset
VAR="${VAR:?'VAR is required'}"        # exit with error if unset — use for required vars
echo "${VAR:=default}"                 # assign AND use default if unset

# Indirect reference (check variable by name)
for var in AWS_REGION ECR_REPO IMAGE_TAG; do
    [[ -z "${!var:-}" ]] && echo "MISSING: $var" && exit 1
done
```

### String Manipulation

```bash
str="deployment/my-app-v1.2.3"
echo "${str##*/}"      # my-app-v1.2.3    — strip longest prefix
echo "${str%/*}"       # deployment       — strip shortest suffix
echo "${str/v1/v2}"    # replace first match
echo "${str//v/V}"     # replace ALL matches
echo "${str^^}"        # UPPERCASE
echo "${str,,}"        # lowercase

# Extract tag from ECR URI
ecr_uri="123456.dkr.ecr.us-east-1.amazonaws.com/myapp:abc1234"
tag="${ecr_uri##*:}"   # abc1234
```

### Arrays — Critical Quoting Rules

```bash
services=("auth" "api" "worker")

for svc in "${services[@]}"; do   # ALWAYS quote with [@]
    kubectl rollout restart deployment/"$svc"
done

# [GOTCHA] quoting rules:
# "${arr[@]}"  — correct: each element quoted separately
# "${arr[*]}"  — joins all into one string (word-splits on spaces in elements)
# $arr         — only expands FIRST element
```

### Production Functions

```bash
# Logging with timestamps
log_info()  { echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO]  $*"; }
log_error() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $*" >&2; }

# Retry — essential for flaky cloud APIs
retry() {
    local max=$1; local delay=$2; shift 2
    local attempt=1
    while [[ $attempt -le $max ]]; do
        "$@" && return 0
        echo "Attempt $attempt/$max failed. Retrying in ${delay}s..."
        sleep "$delay"; ((attempt++))
    done
    return 1
}
# Usage: retry 3 5 aws s3 cp file.txt s3://bucket/

# Require command exists
require_command() {
    command -v "$1" &>/dev/null || { echo "Missing: $1"; exit 1; }
}
```

### Secret Handling

```bash
# NEVER: visible in ps aux, leaked to logs
export DB_PASSWORD="plaintext"

# CORRECT: fetch at runtime, don't export
DB_PASSWORD=$(aws secretsmanager get-secret-value \
    --secret-id "prod/myapp/db" \
    --query SecretString \
    --output text | jq -r '.password')

# Prevent leaking in set -x traces
set +x
TOKEN=$(fetch_secret)
set -x

# GitHub Actions masking
echo "::add-mask::${DB_PASSWORD}"
```

### Redirections — The Tricky Ones

```bash
command > file 2>&1       # CORRECT: stdout→file, stderr→same as stdout
command 2>&1 > file       # WRONG: stderr→terminal, stdout→file (order matters!)
command &>/dev/null       # suppress ALL output (bash shorthand)
command >/dev/null 2>&1   # same, POSIX compatible

# Capture stderr separately
output=$(command 2>/tmp/stderr_$$)
stderr=$(cat /tmp/stderr_$$); rm -f /tmp/stderr_$$

# Redirect ALL script output to log
exec > >(tee -a /var/log/deploy.log) 2>&1
```

### Here-Docs & Process Substitution

```bash
# Apply K8s manifest inline — no temp file needed
kubectl apply -f - <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: ${NAMESPACE}
data:
  LOG_LEVEL: "${LOG_LEVEL}"
EOF

# diff two live commands — no temp files
diff <(kubectl get pods -n prod -o name | sort) \
     <(kubectl get pods -n staging -o name | sort)

# [PROD] Loop that preserves variable changes (pipe subshell trap fix)
count=0
while IFS= read -r line; do
    ((count++))
done < <(cat file.txt)    # process substitution keeps while in current shell
echo $count               # correct — not lost in subshell
```

### Cron — Production Gotchas

```bash
# Syntax: MIN  HOUR  DOM  MON  DOW  command
*/5 * * * * /usr/local/bin/healthcheck.sh   # every 5 minutes
30 2 * * * /usr/local/bin/backup.sh         # 2:30 AM daily
0 9 * * 1  /usr/local/bin/report.sh         # Monday 9 AM

# [PROD] Production cron template
0 2 * * * /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1
```

> **[GOTCHA] Top 3 cron failures:**
> 1. PATH is minimal — use full paths (`/usr/local/bin/aws` not `aws`)
> 2. No environment variables — set them explicitly in the crontab line
> 3. Output goes to local mail — always redirect `>> /var/log/x.log 2>&1`

---

## 3. INTERVIEW Q&A — BASH

### `[ ]` vs `[[ ]]` vs `(( ))`

| Construct | Type | Use For |
|-----------|------|---------|
| `[ ]` | POSIX external cmd | Portable scripts, fragile with empty vars |
| `[[ ]]` | Bash built-in | All Bash scripts — safer, supports regex `=~` |
| `(( ))` | Arithmetic | Integer math, `((count++))` |
| `$( )` | Command sub | Capture command output |
| `< ( )` | Process sub | Create named pipe from command output |

```bash
# [GOTCHA] empty variable breaks [ ] but not [[ ]]
var=""
[ $var = "" ]    # ERROR: unary operator expected
[[ $var = "" ]]  # SAFE

# regex — ONLY works in [[ ]]
[[ "$port" =~ ^[0-9]+$ ]] || { echo "Invalid port"; exit 1; }
```

### `$*` vs `$@`

- `"$@"` — each argument quoted separately — **always use this** when forwarding args
- `"$*"` — joins all args into one string (breaks args with spaces)
- `$@` (unquoted) — same as `$*` unquoted — both word-split

### `exec` — Why It Matters in Docker

```bash
# BAD: shell is PID 1, app is child → doesn't receive SIGTERM
#!/bin/bash
python3 app.py

# GOOD: exec replaces shell with app — app IS PID 1, receives signals
#!/bin/bash
exec python3 app.py
```

> **[INTERVIEW]** `exec` replaces the current shell process using the same PID. In containers, if your entrypoint is a shell script without `exec`, `docker stop` sends SIGTERM to bash (PID 1) not your app — graceful shutdown breaks.

### `source` vs Executing a Script

| | Executing (`./script.sh`) | Sourcing (`source script.sh`) |
|--|--|--|
| Process | Child process (fork) | Current shell |
| Variables | Lost after exit | Persist in current shell |
| `cd` | Doesn't affect parent | Changes current dir |
| Use for | Running tasks | Loading env vars, functions |

### Process Substitution vs Pipe

```bash
# Pipe — while runs in SUBSHELL — variable changes lost
count=0
cat file | while read line; do ((count++)); done
echo $count   # 0 — WRONG

# Process substitution — while in CURRENT shell — state preserved
count=0
while read line; do ((count++)); done < <(cat file)
echo $count   # correct
```

### Robust Error Handling

```bash
# Error handler with full context
error_handler() {
    echo "Command '$BASH_COMMAND' failed with exit $? on line $1"
    # Stack trace:
    local i=0; while caller $i; do ((i++)); done
}
trap 'error_handler $LINENO' ERR

# Timeout wrapper
run_with_timeout() {
    local timeout=$1; shift
    timeout "$timeout" "$@" || {
        [[ $? -eq 124 ]] && echo "Timed out after ${timeout}s"
        return 1
    }
}
```

---

## 4. INTERVIEW Q&A — LINUX SYSTEM

### Boot Process (Memorize This Order)

```
Power → BIOS/UEFI → GRUB2 → Kernel + initramfs → systemd (PID 1) → Targets → Login

Key debug commands:
journalctl -b -1 -p err          # errors from previous (crashed) boot
systemd-analyze blame            # what slowed boot down
systemd-analyze critical-chain   # bottleneck in boot chain
```

### What Happens When You Run `ls -l`

```
1. Shell fork()s child process
2. Child execve("/usr/bin/ls", ["ls","-l"], env)
3. Kernel loads ELF binary
4. ls: openat(AT_FDCWD, ".", O_RDONLY) — open directory
5. ls: getdents64(fd, buf, size) — read entries
6. ls: lstat() for each entry — get metadata
7. ls: write(1, output, len) — write stdout
8. ls: exit_group(0)
9. Parent receives SIGCHLD, wait() collects exit code

# Verify:
strace -e trace=openat,getdents64,lstat ls -l 2>&1 | head -20
```

> **[INTERVIEW]** Tests OS fundamentals. Key concepts: `fork()` + `execve()` = Unix process creation model. Everything is a file descriptor. Syscalls = boundary between user space and kernel space.

### Zombie Processes

```bash
# Zombie = finished but parent hasn't called wait() — holds PID in process table
ps aux | awk '$8 == "Z"'          # find zombies

# [INTERVIEW] You CANNOT kill a zombie — it's already dead
# Fix: kill the PARENT → init/systemd inherits and reaps orphans
kill -9 <parent_pid>

# Prevention in Docker — use tini as PID 1
ENTRYPOINT ["/sbin/tini", "--"]   # handles SIGCHLD + zombie reaping
CMD ["node", "server.js"]

# Or in docker-compose:
init: true
```

### Open File Limit Errors

```bash
# Diagnose "Too many open files"
ulimit -n                        # soft limit (current shell)
ulimit -Hn                       # hard limit
cat /proc/sys/fs/file-max        # system-wide max

lsof -n | awk '{print $1}' | sort | uniq -c | sort -rn | head -10  # top consumers
ls /proc/<PID>/fd | wc -l        # FDs for specific process

# Fix for systemd service:
# /etc/systemd/system/myapp.service
[Service]
LimitNOFILE=65536

# Monitor for FD leaks:
watch -n 2 'ls /proc/<PID>/fd | wc -l'   # growing = leak
```

### Signals — Kill Chain

| Signal | Number | Behaviour | Catchable? |
|--------|--------|-----------|-----------|
| SIGTERM | 15 | Graceful shutdown request | Yes |
| SIGKILL | 9 | Kernel force-kill | **NO** |
| SIGHUP | 1 | Reload config (nginx, sshd) | Yes |
| SIGCHLD | 17 | Child process status changed | Yes |
| SIGSTOP | 19 | Pause process | **NO** |

```bash
# [PROD] Graceful shutdown pattern
kill -SIGTERM "$pid"
waited=0
while kill -0 "$pid" 2>/dev/null && [[ $waited -lt 30 ]]; do
    sleep 1; ((waited++))
done
kill -0 "$pid" 2>/dev/null && kill -9 "$pid"   # force if still alive
```

> **[INTERVIEW]** SIGKILL and SIGSTOP cannot be caught or ignored — kernel handles them directly. SIGKILL bypasses: DB connection cleanup, in-flight requests, file buffer flushing, lock file removal. Always try SIGTERM first.

### `/proc` — Why DevOps Engineers Care

```bash
/proc/<PID>/cmdline    # exact launch command
/proc/<PID>/environ    # env vars — may contain secrets (security concern)
/proc/<PID>/fd/        # open file descriptors
/proc/sys/net/ipv4/ip_forward   # IP forwarding (K8s nodes need this = 1)
/proc/meminfo          # detailed memory breakdown
/proc/loadavg          # load average

# sysctl is just a friendly interface to /proc/sys/
sysctl net.ipv4.ip_forward=1
# === same as:
echo 1 > /proc/sys/net/ipv4/ip_forward
```

### `awk` — 3 Production Patterns

```bash
# 1. Alert on high-CPU pods
kubectl top pods -n production --no-headers | awk '{
    cpu=$2; sub(/m/,"",cpu)
    if(cpu>800) print "HIGH CPU:",$1,cpu"m"
}'

# 2. Extract field from structured log
grep "duration=" app.log | awk -F'duration=' '{print $2}' | \
    awk '{print $1}' | sort -n | awk 'END{print "max:", $0"ms"}'

# 3. Detect config drift across servers
for h in web1 web2 web3; do ssh $h 'nginx -v 2>&1'; done | \
    awk -F'/' '{v[$2]++} END{
        for(ver in v) print ver, "("v[ver]" servers)"
    }'
```

---

## 5. QUICK-FIRE ANSWERS

**`chmod 755` means?**
> Owner: rwx(7), Group: r-x(5), Others: r-x(5). Binary: 111 101 101. Standard for scripts/dirs — owner can modify, everyone can read/execute.

**Hard link vs soft link?**
> Hard link = another dir entry pointing to same inode (survives deletion, same filesystem only). Soft/symlink = pointer to a path (breaks if target deleted, works across filesystems). `[PROD]` Use symlinks for versioning: `current -> app-v2.1.3/`

**`umask` — what's a secure default?**
```bash
umask 027    # files=640, dirs=750 — blocks world read/write
umask 022    # files=644, dirs=755 — common default
# Formula: file perms = 666 - umask | dir perms = 777 - umask
```

**`sudo` vs `su`?**
> `su` switches user entirely (needs target's password, no audit trail). `sudo` runs one command elevated (YOUR password, logged to `/var/log/auth.log`, fine-grained via sudoers). Always prefer `sudo` in production — audit trail is non-negotiable.

**`LD_PRELOAD` security implication?**
> Injects a shared library before standard libs, intercepting syscalls like `open()`, `read()`, `exec()`. Legitimate use: `jemalloc`, `tcmalloc`. Security risk: rootkit technique — can completely override libc behaviour. Audit `/etc/ld.so.preload`, use `nosuid` mount options in hardened environments.

**What's the difference between a process and a thread?**
> Process = isolated memory space + at least one thread. Thread = lightweight execution unit sharing process memory. Processes communicate via IPC (pipes, sockets, shared memory). Threads share heap, can race on shared data → need mutexes. In containers, each container is a process group with its own namespaces.

**How does `sudo` know what you're allowed to do?**
> Reads `/etc/sudoers` (edit with `visudo` only — validates syntax before saving). Rules: `user  host=(run_as) command`. The `%group` syntax grants to a group. `NOPASSWD:` skips password prompt. `[PROD]` Use `/etc/sudoers.d/` directory for per-service drop-in files instead of editing main file.

---

## 6. DEBUGGING ROADMAP

### Bash Script Failures

```
Script fails silently
→ Add 'set -euo pipefail' at top
→ Run: bash -x script.sh 2>&1 | less   (xtrace)

"unbound variable" error
→ bash -u script.sh to find which var
→ Add defaults: ${VAR:-default}

Pipeline succeeds but wrong result
→ Missing -o pipefail — each pipe stage's exit ignored
→ Test each command individually

Script works locally, fails in CI
→ PATH differences: use /usr/bin/aws not aws
→ Missing env vars: add validation block at top
→ Locale: export LANG=C LC_ALL=C
→ Line endings: file was saved as CRLF (Windows)
   dos2unix script.sh
```

### Linux System Issues

```
"Too many open files"
→ lsof -n | awk '{print $1}' | sort | uniq -c | sort -rn
→ Check ulimit -n vs process actual usage
→ Fix: LimitNOFILE in systemd unit

Disk full but df shows space
→ df -i (inode exhaustion)
→ find / -xdev -type f | wc -l (count all files)
→ find / -name "*.log" | xargs ls -lh | sort -k5 -rh | head

Process hangs, high CPU
→ strace -p <PID> -e trace=all (what syscall is it stuck on?)
→ lsof -p <PID> (waiting on file/socket?)
→ ss -tnp (stuck on network?)

Boot failure
→ journalctl -b -1 -p err
→ Boot to emergency target, check /etc/fstab (wrong UUID?)
→ systemd-analyze blame (slow unit blocking boot)

Can't connect to port
→ ss -tulnp | grep <port> (is it listening?)
→ iptables -L -n -v (firewall blocking?)
→ systemctl status <service> (is it running?)
→ SELinux: ausearch -m avc (SELinux denial?)
```

---

## KEY NUMBERS TO REMEMBER

| Item | Value |
|------|-------|
| Default SSH port | 22 |
| Default ulimit nofile | 1024 (too low for prod) |
| Prod recommended nofile | 65536 |
| K8s terminationGracePeriodSeconds default | 30s |
| SIGTERM | 15 |
| SIGKILL | 9 |
| SIGHUP (reload) | 1 |
| Inode size (typical) | 256 bytes |
| TCP TIME_WAIT default | 60s |

---

## PRODUCTION BEST PRACTICES SUMMARY

- **Always** `set -euo pipefail` + trap in scripts
- **Always** use full paths in cron jobs
- **Always** `exec` before your app in Docker entrypoints (signal handling)
- **Never** store secrets in env vars visible via `ps aux`
- **Never** run `kill -9` as first resort — SIGTERM + wait + SIGKILL
- **Never** `netstat` — use `ss`
- **Never** `chmod 777` — find the actual permission needed
- **Always** redirect cron output: `>> /var/log/x.log 2>&1`
- **Always** validate required vars at script start
- **Always** use `"${arr[@]}"` not `$arr` for arrays

---

*Generated from DevSecOps Interview Prep Session — Linux & Bash Module*
