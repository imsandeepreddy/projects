
### Mount and Unmount

### Example Scenario

Let's say you have another partition called `/dev/sdb1` that you want to mount to `/mnt` instead of `/dev/sda1`.

1. **Check the Current Mounts**

   ```bash
   lsblk
   ```

   Output:
   ```
   NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
   sda      8:0    0  100G  0 disk 
   └─sda1   8:1    0  100G  0 part /mnt
   sdb      8:16   0  200G  0 disk 
   └─sdb1   8:17   0  200G  0 part 
   ```

2. **Unmount `/dev/sda1` from `/mnt`**

   ```bash
   umount /mnt
   ```

3. **Mount `/dev/sdb1` to `/mnt`**

   ```bash
   mount /dev/sdb1 /mnt
   ```

4. **Verify the New Mount**

   ```bash
   lsblk
   ```

   Updated output:
   ```
   NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
   sda      8:0    0  100G  0 disk 
   └─sda1   8:1    0  100G  0 part 
   sdb      8:16   0  200G  0 disk 
   └─sdb1   8:17   0  200G  0 part /mnt
   ```

### Networking

Let's explore some basic networking concepts in Linux with corresponding commands and scenarios:

### 1. Checking Network Configuration: `ifconfig` or `ip addr`

**Scenario**: You want to see all the network interfaces on your computer.

**Command**:
```bash
ifconfig
# or
ip addr
```

**Explanation**: These commands display information about all network interfaces on your system, including their IP addresses, MAC addresses, and other relevant details.

### 2. Testing Network Connectivity: `ping`

**Scenario**: You want to check if you can reach a specific website on the internet.

**Command**:
```bash
ping www.example.com
```

**Explanation**: The `ping` command sends a small packet to a specified destination (in this case, `www.example.com`) and waits for a response. If the destination is reachable, you'll see responses indicating successful communication.

### 3. Checking Connectivity to a Specific Port: `telnet` or `nc`

**Scenario**: You want to verify if a specific port on a remote server is open and reachable.

**Command**:
```bash
telnet example.com 80
# or
nc -vz example.com 80
```

**Explanation**: These commands attempt to establish a connection to the specified port (e.g., port 80 for HTTP) on the remote server (`example.com`). If the port is open and accessible, you'll receive a success message.

### 4. Checking Routing Information: `ip route`

**Scenario**: You want to view the routing table to see how network packets are forwarded.

**Command**:
```bash
ip route
```

**Explanation**: The `ip route` command displays the routing table, which shows how network packets are routed based on their destination IP addresses. It lists the available routes along with their associated network interfaces and gateways.

### 5. Configuring Network Interfaces: `ifconfig` or `ip`

**Scenario**: You want to assign an IP address to a network interface.

**Command**:
```bash
ifconfig eth0 192.168.1.100 netmask 255.255.255.0
# or
ip addr add 192.168.1.100/24 dev eth0
```

**Explanation**: These commands configure the IP address (`192.168.1.100`) and netmask (`255.255.255.0`) for the network interface `eth0`. This assigns the specified IP address to the interface, allowing it to communicate on the network.

### 6. Checking DNS Configuration: `cat /etc/resolv.conf`

**Scenario**: You want to view the DNS servers configured on your system.

**Command**:
```bash
cat /etc/resolv.conf
```

**Explanation**: This command displays the contents of the `/etc/resolv.conf` file, which typically contains the IP addresses of DNS servers that your system uses to resolve domain names to IP addresses.

### 7. Checking Listening Ports: `netstat` or `ss`

**Scenario**: You want to see which network services are listening for incoming connections.

**Command**:
```bash
netstat -tuln
# or
ss -tuln
```

**Explanation**: These commands display a list of all listening ports on your system, along with the associated network services. This helps you identify which services are running and accessible from the network.

These scenarios cover some fundamental networking concepts and corresponding Linux commands, providing a practical understanding of networking in a Linux environment.

Now, `/dev/sdb1` is mounted at `/mnt`, and you can access its contents from that location.
