# Wireshark Analysis Guide: DDoS Simulations

This guide will walk you through how to simulate TCP SYN Floods and UDP Floods using your Python scripts and how to analyze the resulting traffic using Wireshark.

**Important Note:** All simulations use the loopback address (`127.0.0.1`), meaning your computer is attacking itself. This is perfectly safe and will not harm your system or network.

---

## Prerequisites

1.  **Python Installed:** Ensure you have Python installed on your system.
2.  **Wireshark Installed:** Download and install [Wireshark](https://www.wireshark.org/).

---

## Step 1: Setting up Wireshark Capture

Before launching any attacks, you need to start listening to the network traffic.

1.  **Open Wireshark.**
2.  On the welcome screen, you will see a list of network interfaces. Since we are attacking `127.0.0.1` (localhost), look for an interface named **Loopback Pseudo-Interface 1** (or simply **Loopback**).
3.  **Double-click** the Loopback interface to start capturing packets.
4.  You will likely see some background traffic. That is normal. Leave this window open and running.

---

## Step 2: Simulating and Analyzing a TCP SYN Flood

A TCP SYN Flood exploits the initial "handshake" process of a TCP connection. 

### The Attack

1.  Open a Terminal or Command Prompt.
2.  Navigate to the folder containing your scripts (e.g., `cd "C:\Users\Jain\Desktop\Network assignment\DDoS_Simulation_Lab"`).
3.  Run the TCP script:
    ```bash
    python tcp_syn_attack_simulator.py --target 127.0.0.1 --port 80 --count 5000
    ```
4.  You will see progress in your terminal as it rapidly attempts thousands of connections.

### Wireshark Analysis

Switch back to your running Wireshark window. You should see a massive flood of new packets.

1.  **Apply the Filter:** In the "Apply a display filter" bar at the top, type the following exactly and press Enter:
    ```
    tcp.flags.syn == 1 && ip.dst == 127.0.0.1
    ```
2.  **What you are seeing:**
    *   This filter isolates packets that have the *SYN flag set* (meaning they are asking to start a connection) and are destined for *127.0.0.1*.
    *   You will see thousands of rows rapidly appearing. This is the flood.
    *   Because our script uses raw sockets to initiate connections rapidly without waiting, the server receiving these (your own machine) is getting bombarded with connection requests on port 80.
3.  **Visualizing the Flood:**
    *   Go to **Statistics -> I/O Graphs** in the top menu bar.
    *   This graph shows the volume of packets over time. You will see a massive spike corresponding exactly to when you ran your Python script. This visual proves the flood occurred.

---

## Step 3: Simulating and Analyzing a UDP Flood

A UDP Flood blasts random junk data at a target to overwhelm its bandwidth.

### The Attack

1.  Return to your Terminal or Command Prompt.
2.  Run the UDP script:
    ```bash
    python udp_flood_attack_simulator.py --target 127.0.0.1 --port 80 --count 100000 --size 1024
    ```
    *Note: This script sends large packets (1024 bytes) extremely fast, which generates a serious bandwidth spike.*

### Wireshark Analysis

Switch back to Wireshark.

1.  **Apply the Filter:** Change the filter bar to the following and press Enter:
    ```
    udp && ip.dst == 127.0.0.1
    ```
2.  **What you are seeing:**
    *   You will see a massive wall of UDP protocol packets.
    *   If you look at the "Length" column, you will see they are uniformly large (around 1052 bytes: 1024 bytes of our random payload + UDP/IP headers).
    *   If you look at the "Info" column, you might see corresponding `ICMP Destination Unreachable (Port unreachable)` packets sent *back* from 127.0.0.1. This happens because the port we are attacking might not actually have anything listening on it, so the operating system is desperately trying to respond "nobody is home" to every single flood packet.
3.  **Visualizing the Flood (Protocol Hierarchy):**
    *   Go to **Statistics -> Protocol Hierarchy**.
    *   Expand the trees (Internet Protocol Version 4 -> User Datagram Protocol -> Data).
    *   You will see that UDP traffic makes up nearly 100% of the packets and bytes captured during that specific timeframe, perfectly illustrating a bandwidth exhaustion attack.

---

## Conclusion

By running these scripts locally and observing them in Wireshark, you've successfully simulated DoS attacks and learned how to identify their signatures (SYN packets without completion, or massive volumes of UDP data) on a network level.

**Remember:** To stop Wireshark from capturing forever, click the red square **Stop** button in the top left corner when you are done.
