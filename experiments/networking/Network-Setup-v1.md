```md
# Linux Networking Lab – Final Notes

---

## 1️⃣ Problem Statement

The goal was to **learn real-world Linux networking** by building a lab that simulates how enterprise networks actually work.

Specifically, the objectives were:

- Simulate **multiple subnets** (client network and server network)
- Use a **Linux VM as a router**
- Implement **internal DNS resolution**
- Ensure **end-to-end connectivity** (Client → DNS → Web Server)
- Understand and fix common real-world issues:
  - Missing return routes
  - DHCP overriding routes and DNS
  - `.local` DNS conflicts
  - systemd-resolved behavior
  - NAT and packet forwarding
  - Why `ping` may fail while `curl` works

The challenge was not just to “make it work”, but to **understand why it breaks and how to fix it correctly**.

---

## 2️⃣ Entire Setup Architecture

### Network Design

```

```
                Internet
                    |
              (VirtualBox NAT)
                    |
                 Router
      --------------------------------
      |                              |
```

Server Network                  Client Network
10.0.1.0/24                      10.0.3.0/24

```

### VM Roles and IPs

| VM Name | Role | IP Address | Network |
|------|------|-----------|--------|
| router | Linux router + NAT | 10.0.1.1 / 10.0.3.1 | Server + Client |
| dns | Internal DNS server | 10.0.1.10 | Server |
| web1 | Web application server | 10.0.1.11 | Server |
| web2 | (Optional) Web server | 10.0.1.12 | Server |
| client | User machine | 10.0.3.10 | Client |

### DNS Domain

```

lab.internal

````

---

## 3️⃣ How the Architecture Was Set Up

### Step 1: Vagrant Setup

After running:

```bash
vagrant up
````

Vagrant created:

* Multiple Ubuntu VMs
* Multiple network interfaces per VM
* A **VirtualBox NAT interface** on all VMs (for internet access)
* One or more **private_network** interfaces for lab networking

At this point, **networking is NOT correct yet**. Further configuration is required.

---

## 4️⃣ Configuration Done on Each Server (and Why)

---

### 🟢 Router VM

**Role:** Acts as the central router between client and server networks.

#### Commands / Configurations

1. **Enable IP forwarding**

```bash
net.ipv4.ip_forward=1
```

**Why**

* Linux does not forward packets by default.
* Required to allow traffic to pass between interfaces.

---

2. **Allow forwarding in firewall**

```bash
iptables -P FORWARD ACCEPT
```

**Why**

* Firewall can block packets even when forwarding is enabled.

---

3. **Configure NAT**

```bash
iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE
```

**Why**

* Allows private IPs (10.x.x.x) to access the internet.
* Required for `apt update`, package installs, etc.

---

### 🟢 DNS Server (dns)

**Role:** Internal DNS server resolving service names.

#### Configurations

1. **Static IP**

```
10.0.1.10
```

**Why**

* DNS server IP must be stable.
* Clients depend on this address.

---

2. **Default Gateway**

```bash
default via 10.0.1.1
```

**Why**

* DNS replies must return to the client network via router.

---

3. **Ignore DHCP routes and DNS**

```yaml
dhcp4-overrides:
  use-routes: false
  use-dns: false
```

**Why**

* VirtualBox NAT injects incorrect gateway and DNS.
* Causes replies to go to the wrong place.

---

4. **Install and configure BIND9**

```bash
sudo apt install bind9
```

Configured zone:

```
lab.internal
```

**Why**

* `.local` conflicts with mDNS.
* `lab.internal` is enterprise-safe.

---

### 🟢 Web Server (web1)

**Role:** Serves the application (HTTP).

#### Configurations

1. **Static IP**

```
10.0.1.11
```

---

2. **Default Gateway**

```bash
default via 10.0.1.1
```

**Why**

* Enables return traffic to client network.
* Without this, HTTP hangs even though requests arrive.

---

3. **Ignore DHCP routes and DNS**

```yaml
use-routes: false
use-dns: false
```

**Why**

* Prevents NAT from hijacking routing.

---

4. **Install Nginx**

```bash
sudo apt install nginx
```

Used as a simple service to validate networking.

---

### 🟢 Client VM

**Role:** Simulates a user machine.

#### Configurations

1. **Static IP**

```
10.0.3.10
```

---

2. **Default Gateway**

```bash
default via 10.0.3.1
```

**Why**

* All non-local traffic must go to router.

---

3. **Explicit DNS server**

```yaml
nameservers:
  addresses:
    - 10.0.1.10
```

**Why**

* systemd-resolved ignores `/etc/resolv.conf`.
* Ensures client queries internal DNS.

---

4. **Ignore DHCP DNS and routes**

```yaml
use-routes: false
use-dns: false
```

**Why**

* Prevents NAT DNS (127.0.0.53 → external DNS).
* Avoids wrong DNS resolution.

---

## 5️⃣ Packet Flow in Final Setup

### HTTP Request Flow

```
Client (10.0.3.10)
 → Router (10.0.3.1)
 → Web1 (10.0.1.11)
 → Router (10.0.1.1)
 → Client (10.0.3.10)
```

### DNS Resolution Flow

```
Client
 → DNS (10.0.1.10)
 ← IP address returned
```

---

## 6️⃣ Important Points to Note

### 🔹 Routing is Bidirectional

* Forward path working is not enough.
* Every server must know **how to send replies back**.

---

### 🔹 DHCP is Dangerous in Multi-NIC Systems

* DHCP can override:

  * Default gateway
  * DNS servers
* Must be explicitly controlled.

---

### 🔹 `.local` Should Be Avoided

* Reserved for mDNS.
* Causes SERVFAIL with systemd-resolved.

---

### 🔹 Ping Is Not Proof

* ICMP can fail while TCP works.
* `curl` is the real test.

---

### 🔹 Convergence Delays Are Normal

* ARP learning
* DNS cache refresh
* Connection tracking cleanup

Waiting a few seconds is normal in real systems.

---

## 7️⃣ Key Takeaway

> **Most networking problems are return-path problems, not forward-path problems.**

Understanding this lab means you now understand:

* Enterprise routing
* Cloud VPC networking
* Kubernetes node networking
* Real-world DNS and NAT behavior

---

✅ This setup is now a **solid, production-grade learning baseline**.

```
```
