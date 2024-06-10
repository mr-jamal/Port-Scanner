import socket
import sys
import time
import threading

usage = "python3 port_scan.py TARGET START_PORT END_PORT"
print("-" * 70)
print("Python Simple Port Scanner")
print("-" * 70)

start_time = time.time()

if len(sys.argv) != 4:
    print("Error: Invalid number of arguments.")
    print(usage)
    sys.exit()

try:
    target = socket.gethostbyname(sys.argv[1])
except socket.gaierror:
    print("Error: Name resolution error for target", sys.argv[1])
    sys.exit()

try:
    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])
    if start_port > end_port or start_port < 1 or end_port > 65535:
        print("Error: Ports must be in the range 1-65535 and start_port should be less than or equal to end_port.")
        sys.exit()
except ValueError:
    print("Error: Ports must be integers.")
    print(usage)
    sys.exit()

print("Scanning target", target)

def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    conn = s.connect_ex((target, port))
    if conn == 0:
        print("Port {} is OPEN".format(port))
    s.close()

threads = []

for port in range(start_port, end_port + 1):
    thread = threading.Thread(target=scan_port, args=(port,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

end_time = time.time()
print("Time elapsed:", end_time - start_time, "s")
