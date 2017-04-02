import socket
import struct
import textwrap
from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5 import QtGui,QtWidgets
from dbclass import db
import sys
import uuid
from itertools import chain
import threading
from scapy.all import *

#################################################
def concat_ip_mac(ip,mac):
    ip_mac = ip + mac
    # print ip_mac
    return ip_mac
############### Database Params##################
dbi = db("localhost","root","Impulses@211","test")
#################################################
class hDialogdb(QThread):
    signal = pyqtSignal('PyQt_PyObject')
    def __init__(self,hbit):
        QThread.__init__(self)
        self.hostbit=hbit
        ###change these before deploy!######
        # dbi.add_info('192.168.1.1','ff.f.ff.ff.ff.ff.ff.ff',concat_ip_mac('192.168.1.1','ff.f.ff.ff.ff.ff.ff.ff'))
        # dbi.add_info_inv('192.168.1.3','ff.ff.ff.f.ff.ff.ff.ff')
        # dbi.add_info_inv('192.168.1.4','ff.ff.ff.ff.f.ff.ff.ff')
    def __del__(self):
        self.self.terminate()
        return True
    def stop(self):
        self.terminate()
    def run(self):
        if self.hostbit==0:
            data = dbi.return_table()
        elif self.hostbit==1:
            data = dbi.return_table_inv()

        model = QtGui.QStandardItemModel()
        model.setColumnCount(3)
        headerNames = []
        headerNames.append("IP Address ")
        headerNames.append("Mac Address")
        headerNames.append('Binded Address')
        model.setHorizontalHeaderLabels(headerNames)
        for d in data:
			row = []
			for name in d:
				item = QtGui.QStandardItem(name)
				item.setEditable(False)
				row.append(item)
			model.appendRow(row)
        # dbi.add_info('192.168.1.2','ff.ff.f.ff.ff.ff.ff.ff')
        self.signal.emit(model)

class arpsniff(QThread):
    dbi = db("localhost","root","Impulses@211","test")
    modelUpdateSignal = pyqtSignal('PyQt_PyObject')
    spoofDetectedSignal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QThread.__init__(self)
        self.sys_mac= ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])
        # print self.sys_mac
        self.st=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.st.connect(("192.168.153.1",80))
        self.s = socket.socket()         # Create a socket object
        self.host = socket.gethostname() # Get local machine name
        self.port = 12345                # Reserve a port for your service.
        self.s.bind((self.host, self.port))	    # Bind to the port
        self.s.listen(5)                 # Now wait for client connection.
        self.sys_ip=self.st.getsockname()[0]
        self.model = QtGui.QStandardItemModel()
        self.model.setColumnCount(2)
        headerNames = []
        headerNames.append("Source IP")
        headerNames.append("Source Mac")
        self.model.setHorizontalHeaderLabels(headerNames)

    def __del__(self):
        self.s.close()
        self.terminate()

    def detect(self,c, addr):
        print 'Got connection from', addr
        output = c.recv(10240)
        for e in output.split("\n"):
            row= []
            if len(e.strip()) > 0:
                arr=e.split(" ")
                print arr
                mac = arr[3]
                ip = arr[1].split("(")[1].split(")")[0]
                print mac
                print ip
                if(mac != self.sys_mac and mac!="<incomplete>"):

                    srcip = QtGui.QStandardItem(ip)
                    srcip.setEditable(False)
                    row.append(srcip)

                    srcmac= QtGui.QStandardItem(mac)
                    srcmac.setEditable(False)
                    row.append(srcmac)

                    self.model.appendRow(row)
                    self.modelUpdateSignal.emit(self.model)
                    pac = srp1(Ether(src=self.sys_mac,dst=mac)/IP(src=self.sys_ip,dst=ip)/TCP(dport=80)/b"die",timeout=4)
                    if dbi.present_mac(concat_ip_mac(ip,mac)):
                        if ip != dbi.get_ip(mac):
                            try:
                                print pac[1].src
                                print pac[0].src
                                if(pac[0].src==mac and pac[1].src==ip):
                                    print "Authentic"
                                    dbi.update_ip(ip,mac)
                                else:
                                    print "spoof"
                                    self.spoofDetectedSignal.emit(ip)
                                    dbi.add_info_inv(ip,mac,concat_ip_mac(ip,mac))
                            except:
                                print "spoooooof  :D"
                                self.spoofDetectedSignal.emit(ip)
                                dbi.add_info_inv(ip,mac,concat_ip_mac(ip,mac))
                    else:
                        try:
                            print pac[1].src
                            print pac[0].src
                            if(pac[0].src==mac and pac[1].src==ip):
                                print "Authentic"
                                dbi.add_info(ip,mac,concat_ip_mac(ip,mac))
                            else:
                                print "spoof"
                                self.spoofDetectedSignal.emit(ip)
                                dbi.add_info_inv(ip,mac,concat_ip_mac(ip,mac))
                        except:
                            print "spoooooof  :D"
                            self.spoofDetectedSignal.emit(ip)
                            dbi.add_info_inv(ip,mac,concat_ip_mac(ip,mac))
                elif mac=="<incomplete>":
                    print "invalid mac sent"
                else:
                    print "its me and i trust myself :p"
        c.close()
        # thread_count = thread_count-1


    def run(self):
        while True:
           c, addr = self.s.accept()     # Establish connection with client.
           detect_spoof = threading.Thread(target=self.detect,name="check_valid_arp",args=(c, addr))
           detect_spoof.start()
