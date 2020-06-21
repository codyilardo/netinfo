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
        if gateway[:-3] in lines[i] and host_name not in lines[i]: #host_name is for the last line of nmap output that throws off formatting
            devices.append((lines[i][21:]).strip())
            print(lines[i][21:] + ": " + lines[i+2][31:])




#check if running as root
if os.getuid() != 0:
    exit("Run netinfo with sudo. Exiting.")

#get hostnmae
host_name = socket.gethostname()
#get gateway
gateway = get_default_gateway_linux()
devices = []


###display gateway
print("Gateway: " + gateway)

###nmap on router
print("Scan on Gateway: \n")
gateway_scan(gateway)

###device discovery
print("***Device Discovery***")
device_discovery(gateway)
print(devices)
