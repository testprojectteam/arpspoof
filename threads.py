import socket
import struct
import textwrap
from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5 import QtGui
from dbclass import db

class hDialogdb(QThread):
    signal = pyqtSignal('PyQt_PyObject')
    def __init__(self,hbit):
        QThread.__init__(self)
        self.hostbit=hbit
        ###change these before deploy!######
        self.dbi = db("localhost","root","Impulses@211","test")
        # self.dbi.add_info('192.168.1.1','ff.f.ff.ff.ff.ff.ff.ff')
        # self.dbi.add_info('192.168.1.2','ff.ff.f.ff.ff.ff.ff.ff')
        # self.dbi.add_info_inv('192.168.1.3','ff.ff.ff.f.ff.ff.ff.ff')
        # self.dbi.add_info_inv('192.168.1.4','ff.ff.ff.ff.f.ff.ff.ff')
    def __del__(self):
        self.wait()

    def run(self):
        if self.hostbit==0:
            data = self.dbi.return_table()
        elif self.hostbit==1:
            data = self.dbi.return_table_inv()

        model = QtGui.QStandardItemModel()
        model.setColumnCount(2)
        headerNames = []
        headerNames.append("IP Address")
        headerNames.append("Mac Address")
        model.setHorizontalHeaderLabels(headerNames)
        for d in data:
			row = []
			for name in d:
				item = QtGui.QStandardItem(name)
				item.setEditable(False)
				row.append(item)
			model.appendRow(row)
        self.signal.emit(model)



class arpsniff(QThread):
    dbi = db("localhost","root","Impulses@211","test")
    signal = pyqtSignal('PyQt_PyObject')
    def __init__(self):
        QThread.__init__(self)
    def __del__(self):
        self.wait()
    # Return properly formatted MAC address (ie AA:BB:CC:DD:EE:FF)
    def get_mac_addr(self,bytes_addr):
        bytes_str =  ":".join("{:02x}".format(ord(c)) for c in bytes_addr)
        return bytes_str

    def ethernet_frame(self,data):
        dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
        return self.get_mac_addr(dest_mac), self.get_mac_addr(src_mac), socket.htons(proto),data[14:]

    def arp_frame(self,data):
        arpHeader = data[14:42]
        arpHeaderUnpacked = struct.unpack('!HHBBH6s4s6s4s', arpHeader)
        arpSenderHardAddress = arpHeaderUnpacked[5]
        arpTargetHardAddress = arpHeaderUnpacked[7]
        arpSourceProtAddress = socket.inet_ntoa(arpHeaderUnpacked[6])
        arpSenderHardAddress = '%.2x:%.2x:%.2x:%.2x:%.2x:%.2x' % (ord(arpSenderHardAddress[0]), ord(arpSenderHardAddress[1]), ord(arpSenderHardAddress[2]), ord(arpSenderHardAddress[3]), ord(arpSenderHardAddress[4]), ord(arpSenderHardAddress[5]))
        arpTargetHardAddress = '%.2x:%.2x:%.2x:%.2x:%.2x:%.2x' % (ord(arpTargetHardAddress[0]), ord(arpTargetHardAddress[1]), ord(arpTargetHardAddress[2]), ord(arpTargetHardAddress[3]), ord(arpTargetHardAddress[4]), ord(arpTargetHardAddress[5]))
        return arpTargetHardAddress,arpSenderHardAddress,arpSourceProtAddress

    def run(self):
        model = QtGui.QStandardItemModel()
        model.setColumnCount(4)
        headerNames = []
        headerNames.append("IP Address")
        headerNames.append("Dest Mac")
        headerNames.append("Source Mac")
        headerNames.append("Protocol")
        model.setHorizontalHeaderLabels(headerNames)
        conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        while True:
            row = []
            raw_data, addr = conn.recvfrom(65535)
            ethdest_mac, ethsrc_mac, eth_proto, data = self.ethernet_frame(raw_data)[0], self.ethernet_frame(raw_data)[1], self.ethernet_frame(raw_data)[2], self.ethernet_frame(raw_data)[3]
            arpdest_mac, arpsrc_mac, src_ip = self.arp_frame(raw_data)[0], self.arp_frame(raw_data)[1], self.arp_frame(raw_data)[2]
            if(ethdest_mac==arpdest_mac):
                print ('\nEthernet Frame:')
                print src_ip
                print ('Destination: {}, Source: {}, Protocol: {}'.format(ethdest_mac, ethsrc_mac, eth_proto))

                if not self.dbi.present(src_ip,arpsrc_mac):
                    self.dbi.add_info(src_ip,arpsrc_mac)

                srcip = QtGui.QStandardItem(src_ip)
                srcip.setEditable(False)
                row.append(srcip)

                destmac = QtGui.QStandardItem(ethdest_mac)
                destmac.setEditable(False)
                row.append(destmac)

                sourcemac = QtGui.QStandardItem(ethsrc_mac)
                sourcemac.setEditable(False)
                row.append(sourcemac)

                proto = QtGui.QStandardItem(str(eth_proto))
                proto.setEditable(False)
                row.append(proto)

                model.appendRow(row)

                self.signal.emit(model)
        # for d in data:
		# 	row = []
		# 	for name in d:
		# 		item = QtGui.QStandardItem(name)
		# 		item.setEditable(False)
		# 		row.append(item)
		# 	model.appendRow(row)
