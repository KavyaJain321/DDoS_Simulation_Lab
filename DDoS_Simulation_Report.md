# DDoS Simulation Lab Report

**Project:** Simulation of TCP SYN Flood and UDP Flood Attacks  
**Objective:** To understand, simulate, and analyze Denial of Service (DoS) attacks on a local loopback network using Python and Wireshark.

---

## 1. Introduction
Denial of Service (DoS) attacks aim to make a machine or network resource unavailable to its intended users by temporarily or indefinitely disrupting services of a host connected to a network.

This lab report documents the step-by-step execution and analysis of two common types of DoS attacks:
1. **TCP SYN Flood**: Targets server connection tracking capabilities.
2. **UDP Flood**: Targets network bandwidth by causing congestion.

The attacks were simulated locally on `127.0.0.1` (loopback interface) using Python sockets to ensure a safe, isolated environment.

---

## 2. Experimental Setup

### Tools Used
*   **Python 3**: For scripting the attack simulations (`tcp_syn_attack_simulator.py` and `udp_flood_attack_simulator.py`).
*   **Wireshark**: For real-time packet capture and traffic analysis.

### Step 1: Configuring Wireshark for Capture
Before launching the attacks, Wireshark was configured to listen to the local machine's internal traffic. This prevents external internet traffic from polluting the capture.

As shown below, the **Adapter for loopback traffic capture** was selected as the listening interface in Wireshark:

![Adapter Selection - Loopback](c:\Users\Jain\Desktop\Network assignment\Adapter for loopback traffic capture.png)

*Caption: Selecting the Loopback adapter in Wireshark from the Capture Interfaces menu.*

---

## 3. TCP SYN Flood Simulation

### The Attack Mechanism
A TCP SYN flood exploits part of the normal TCP three-way handshake. The attacker sends a succession of `SYN` requests to a target's system. The target responds to each with a `SYN-ACK` packet and leaves the port open waiting for the final `ACK` packet, which the attacker never sends. The target's connection-listening queue eventually fills up, leading to a denial of service for legitimate traffic.

### Execution
The following command was executed in the terminal to launch the SYN Flood script against localhost (`127.0.0.1`) on port `80`:
```bash
python tcp_syn_attack_simulator.py --target 127.0.0.1 --port 80 --count 10000
```
This script rapidly opened thousands of raw sockets to initiate the `SYN` handshake without completing it.

### Wireshark Analysis
During the simulation, Wireshark captured the massive influx of `SYN` packets. A display filter (`tcp.flags.syn == 1 && ip.dst == 127.0.0.1`) was applied to isolate the attack traffic.

![SYN Flood Attack Logs](c:\Users\Jain\Desktop\Network assignment\WhatsApp Image 2026-03-17 at 1.02.40 PM.jpeg)

*Note: The exact visual output of the SYN flood in Wireshark shows continuous, repeating attempts to establish a connection (SYN) from randomized high-numbered source ports to the target application port 80.*

Additionally, the captured traffic (saved locally as **`SYN flood attack logs.pcapng`**) confirms the overwhelming volume of incomplete TCP handshakes, validating the effectiveness of the SYN Flood simulation.

---

## 4. UDP Flood Simulation

### The Attack Mechanism
Unlike TCP, the User Datagram Protocol (UDP) is connectionless. A UDP flood occurs when an attacker sends a massive number of UDP packets to random ports on a target host. 

For each packet, the victim's system checks for an application listening at that port. Seeing no application, the victim replies with an ICMP `Destination Unreachable` packet. This process consumes target host resources, ultimately leading to bandwidth exhaustion.

### Execution
The following command was executed to launch the UDP Flood attack, sending large 1024-byte payloads at a rapid rate:
```bash
python udp_flood_attack_simulator.py --target 127.0.0.1 --port 80 --count 100000 --size 1024
```

### Wireshark Analysis
During the attack, Wireshark captured a massive wall of UDP protocol packets. The display filter (`udp && ip.dst == 127.0.0.1`) successfully isolated the flood.

![UDP Flood Traffic Captured](c:\Users\Jain\Desktop\Network assignment\UDP Flood logs.png)

![Additional UDP Logs](c:\Users\Jain\Desktop\Network assignment\WhatsApp Image 2026-03-17 at 1.06.38 PM.jpeg)

*Captions: Wireshark captures displaying a high volume of uniform UDP packets flooding the interface. Notice how the traffic almost entirely consists of the simulated payload data.*

Because the target machine's port 80 was likely not hosting a UDP service, the flood caused the operating system to respond continually, consuming processing power and bandwidth simply to process the junk data. This data is preserved in the local packet capture: **`UDP Flood logs.pcapng`**.

---

## 5. Conclusion
This lab successfully demonstrated the vulnerability of network protocols to resource starvation attacks:
*   The **TCP SYN Flood** exposed the weakness in the stateful connection tracking of the TCP 3-way handshake.
*   The **UDP Flood** proved that large volumes of connectionless traffic can easily saturate bandwidth and force the processing hardware into an overwhelmed state.

By running these simulations on a local loopback adapter securely using Python and analyzing the raw bits via Wireshark, the mechanics of Denial of Service attacks were clearly observed and documented.
