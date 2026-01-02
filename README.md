# RIP Route Injection Attack & Mitigation

**Authors:** Karolina Graf, Yuliia Lesyk, Mylana Herasymenko  
**Project Type:** Network Security / Routing Protocols  
**Tools:** GNS3, Kali Linux, Scapy, Wireshark, Cisco IOS

---

##  Project Overview
This project demonstrates a **RIP Route Injection** attack on a simulated network topology. [span_0](start_span)The Routing Information Protocol (RIP) is vulnerable to such attacks due to its lack of default authentication[span_0](end_span). [span_1](start_span)[span_2](start_span)By injecting false routing information, an attacker can manipulate routing tables, redirect traffic, or cause a Denial of Service (DoS)[span_1](end_span)[span_2](end_span).

The project is divided into three stages:
1.  **Topology Setup:** Configuring the network and understanding RIP basics.
2.  **Attack Execution:** Using Python (Scapy) to inject a false route (`10.1.4.0/24`) and analyzing packets with Wireshark.
3.  **[span_3](start_span)Mitigation:** Securing the network using RIP MD5 authentication[span_3](end_span).

---

##  Network Topology
The simulation was conducted using **GNS3** with the following components:
* **[span_4](start_span)Routers (5):** R1, R2, R3, R4, R5 (Main routing nodes)[span_4](end_span).
* **[span_5](start_span)Switches (3):** IOU1, IOU2, IOU3 (Connecting PCs to Routers)[span_5](end_span).
* **[span_6](start_span)End Devices:** PC1, PC2, PC3[span_6](end_span).
* **[span_7](start_span)Attacker Node:** Kali Linux VM connected to the `10.1.3.0/24` segment[span_7](end_span).

### Addressing Scheme (Selected)
* **PC1:** 10.0.1.10 | [span_8](start_span)GW: 10.0.1.1[span_8](end_span)
* **PC3:** 10.1.2.10 | [span_9](start_span)GW: 10.1.2.1[span_9](end_span)
* **[span_10](start_span)Attacker (Kali):** 10.1.3.11[span_10](end_span)

---

##  The Attack: Route Injection

### Mechanism
The attack involves sending forged RIP response packets to the multicast address `224.0.0.9`. [span_11](start_span)[span_12](start_span)The attacker announces a fake route (e.g., `10.1.4.0/24`) with a low metric (hop count = 1)[span_11](end_span)[span_12](end_span).

### Execution
1.  **[span_13](start_span)Tool:** A Python script using the **Scapy** library generates malicious RIPv2 packets[span_13](end_span).
2.  **[span_14](start_span)Packet Analysis:** Wireshark captures show packets originating from Kali (`10.1.3.11`) sent to `224.0.0.9` on UDP port 520[span_14](end_span).
3.  **Result:** The victim router accepts the fake update.

**Proof of Success:**
The command `show ip route` on the router confirms the injection:
```text
R   10.1.4.0/24 [120/1] via 10.1.3.11, 00:00:06, FastEthernet1/0

