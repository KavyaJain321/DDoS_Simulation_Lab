# 🛡️ DDoS Simulation Lab
> **Academic Project | Network Security**  
> **Author:** Kavya Jain

## 📖 Overview
This repository contains a controlled, educational environment for simulating and analyzing Denial of Service (DoS) attacks on a local machine. The project demonstrates how resource starvation and bandwidth exhaustion vulnerabilities can be exploited using fundamental networking concepts.

**⚠️ Disclaimer:** This project and its contents are strictly for educational and academic purposes. All simulations are designed to launch attacks against the local loopback interface (`127.0.0.1`) which is harmless. Do **not** use these scripts against external networks or servers without explicit, legal authorization. 

---

## 🛠️ Technologies Used
*   **Python 3.x:** Scripting language used to create raw sockets for custom packet crafting.
*   **Wireshark:** Network protocol analyzer used to capture and inspect the simulated attack traffic.
*   **Built-in Python Libraries:** `socket`, `argparse`, `time`, `random`. (No external pip dependencies required).

---

## 🚀 Attacks Simulated

### 1. TCP SYN Flood (`tcp_syn_attack_simulator.py`)
This attack targets the stateful nature of the TCP protocol. By rapidly initiating the "SYN" portion of the 3-way handshake and subsequently dropping the connection before the final "ACK", the target's connection tracking tables are filled with half-open connections.

*   **Mechanism:** Resource Starvation (Connection Tracking)
*   **Target:** `127.0.0.1:80`

### 2. UDP Flood (`udp_flood_attack_simulator.py`)
This attack targets network bandwidth. Because UDP is connectionless, it does not require a handshake. Large volumes of junk UDP packets (e.g., 1024-byte payloads) are continuously blasted at the target, causing severe network congestion and forcing the operating system to expend resources generating `ICMP Destination Unreachable` errors.

*   **Mechanism:** Bandwidth Exhaustion
*   **Target:** `127.0.0.1:80`

---

## 💻 How to Run the Simulations

1. **Clone the repository:**
   ```bash
   git clone https://github.com/KavyaJain321/DDoS_Simulation_Lab.git
   cd DDoS_Simulation_Lab
   ```

2. **Run the TCP SYN Flood:**
   ```bash
   python tcp_syn_attack_simulator.py --target 127.0.0.1 --port 80 --count 10000
   ```

3. **Run the UDP Flood:**
   ```bash
   python udp_flood_attack_simulator.py --target 127.0.0.1 --port 80 --count 100000 --size 1024
   ```

*(Press `Ctrl+C` to stop any simulation early.)*

---

## 🔬 Analyzing the Traffic in Wireshark

To observe these attacks at the protocol level:
1. Open **Wireshark**.
2. Start capturing on the **Loopback** interface (since we are attacking `127.0.0.1`).
3. Run one of the Python scripts above.
4. Stop the capture and use the following display filters to analyze the traffic:
   *   **For SYN Floods:** `tcp.flags.syn == 1 && ip.dst == 127.0.0.1`
   *   **For UDP Floods:** `udp && ip.dst == 127.0.0.1`

*For detailed visual breakdowns of the expected Wireshark output and statistics graphing, please refer to the `DDoS_Wireshark_Analysis_Guide.md` included in this repository.*
