import os
import sys
from datetime import datetime
import uuid
from itertools import chain
import threading
from scapy.all import *
import time
import subprocess
s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345
while true :                # Reserve a port for your servic
    s.connect((host, port))
    os.system("nmap 192.168.153.0/24")
    subprocess.call("arp -a",shell=True)
    output = subprocess.check_output("arp -a",shell=True)
    print output


    sys_mac= ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])
    print sys_mac
    st=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    st.connect(("192.168.153.1",80))
    sys_ip=st.getsockname()[0]
    print "\n Scanning"
    s.send(output)
    print s.recv(10240)
    s.close
    time.sleep(10)                     # Close the socket when done






# start_time = datetime.now()
# conf.verb = 0
# ans, uans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst = ips),timeout = 2,
# iface = interface,inter=0.1)
#
# print "MAC - IP\n"
# for snd,rcv in ans:
#     mac = rcv.sprintf(r"%Ether.src% - %ARP.psrc%").split(" ")[0]
#     print mac
#     ip = rcv.sprintf(r"%Ether.src% - %ARP.psrc%").split(" ")[2]
#     print ip
#
#
# stop_time = datetime.now()
# total_time = stop_time - start_time
# print "\nScan complete!"
