import subprocess
import socket, struct
import os

def get_default_gateway_linux():
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue

            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

def device_discovery(gateway):
    iprange = gateway[:-1] + "0/24"
    cmd = "nmap -sn {:}".format(iprange)
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    discovery_output_raw, discovery_error = process.communicate()
    lines = discovery_output_raw.split('\n')[2:]
    for i in range(0,len(lines)):
        if gateway[:-3] in lines[i] and host_name not in lines[i]:
            print(lines[i][20:] + ": " + lines[i+2][30:])

def gateway_scan(gateway):
    cmd = "nmap -T4 -A -v -Pn {:}".format(gateway) 
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    gateway_scan_output_raw, gateway_scan_error = process.communicate()
    print(gateway_scan_output_raw)

if os.getuid() != 0:
    exit("Run netinfo with sudo. Exiting.")

host_name = socket.gethostname()
gateway = get_default_gateway_linux()

print("Gateway: " + gateway)

###device discovery
print("Device Discovery: \n")
device_discovery(gateway)

###nmap on router
print("Scan on Gateway: \n")
gateway_scan(gateway)
