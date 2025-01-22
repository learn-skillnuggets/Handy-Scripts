import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

# Filenames
devices_file = "devices.txt"
pingable_file = "pingable.txt"
failed_file = "failed-ping.txt"

# Ensure devices.txt exists
if not os.path.exists(devices_file):
    print(f"Error: {devices_file} not found in the current directory.")
    exit(1)

# Read hostnames from devices.txt
with open(devices_file, "r") as file:
    hostnames = [line.strip() for line in file if line.strip()]

# Lists to hold results
pingable = []
failed = []

# Ping function
def ping_host(hostname):
    try:
        # Ping command
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", hostname],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # Return result based on return code
        return hostname, result.returncode == 0
    except Exception as e:
        print(f"Error pinging {hostname}: {e}")
        return hostname, False

# Multithreading with progress display
print("Pinging hosts...")
with ThreadPoolExecutor(max_workers=10) as executor:
    future_to_host = {executor.submit(ping_host, host): host for host in hostnames}
    for future in as_completed(future_to_host):
        host, success = future.result()
        if success:
            pingable.append(host)
            print(f"[SUCCESS] {host}")
        else:
            failed.append(host)
            print(f"[FAILED] {host}")

# Write results to files
with open(pingable_file, "w") as file:
    file.write("\n".join(pingable))
with open(failed_file, "w") as file:
    file.write("\n".join(failed))

print("\nPing results saved:")
print(f"  Pingable hosts: {pingable_file}")
print(f"  Failed hosts: {failed_file}")
