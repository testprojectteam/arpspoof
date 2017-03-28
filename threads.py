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
############### Database Params##################
dbi = db("localhost","root","Impulses@211","test")
#################################################
class hDialogdb(QThread):
    signal = pyqtSignal('PyQt_PyObject')
    def __init__(self,hbit):
        QThread.__init__(self)
        self.hostbit=hbit
        ###change these before deploy!######
        # dbi.add_info('192.168.1.1','ff.f.ff.ff.ff.ff.ff.ff')
        # dbi.add_info('192.168.1.2','ff.ff.f.ff.ff.ff.ff.ff')
        # dbi.add_info_inv('192.168.1.3','ff.ff.ff.f.ff.ff.ff.ff')
        # dbi.add_info_inv('192.168.1.4','ff.ff.ff.ff.f.ff.ff.ff')
    def __del__(self):
        self.wait()

    def run(self):
        if self.hostbit==0:
            data = dbi.return_table()
        elif self.hostbit==1:
            data = dbi.return_table_inv()

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
    modelUpdateSignal = pyqtSignal('PyQt_PyObject')
    tcpSpoofedSignal = pyqtSignal('PyQt_PyObject')
    spoofDetectedSignal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QThread.__init__(self)
        self.sys_mac= ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])
        print self.sys_mac
        self.st=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.st.connect(("192.168.153.1",80))
        self.sys_ip=self.st.getsockname()[0]
        self.source_mac_list = []
        self.model = QtGui.QStandardItemModel()
        self.model.setColumnCount(3)
        headerNames = []
        headerNames.append("IP Address")
        headerNames.append("Dest Mac")
        headerNames.append("Source Mac")
        # headerNames.append("Protocol")
        self.model.setHorizontalHeaderLabels(headerNames)

    def __del__(self):
        self.wait()

    def arp_frame(self,data):
        arpHeader = data[14:42]
        arpHeaderUnpacked = struct.unpack('!HHBBH6s4s6s4s', arpHeader)
        arpSenderHardAddress = arpHeaderUnpacked[5]
        arpTargetHardAddress = arpHeaderUnpacked[7]
        arpTargetProtAddress = socket.inet_ntoa(arpHeaderUnpacked[6])
        arpSenderHardAddress = '%.2x:%.2x:%.2x:%.2x:%.2x:%.2x' % (ord(arpSenderHardAddress[0]), ord(arpSenderHardAddress[1]), ord(arpSenderHardAddress[2]), ord(arpSenderHardAddress[3]), ord(arpSenderHardAddress[4]), ord(arpSenderHardAddress[5]))
        arpTargetHardAddress = '%.2x:%.2x:%.2x:%.2x:%.2x:%.2x' % (ord(arpTargetHardAddress[0]), ord(arpTargetHardAddress[1]), ord(arpTargetHardAddress[2]), ord(arpTargetHardAddress[3]), ord(arpTargetHardAddress[4]), ord(arpTargetHardAddress[5]))
        arpoperation= arpHeaderUnpacked[4]
        #arpoperation= '%.2x %.2x' % (ord(arpoperation[0]),ord(arpoperation[1]))
        return arpTargetHardAddress,arpSenderHardAddress,arpTargetProtAddress, arpoperation


    # Return properly formatted MAC address (ie AA:BB:CC:DD:EE:FF)
    def get_mac_addr(self,bytes_addr):
        bytes_str =  ":".join("{:02x}".format(ord(c)) for c in bytes_addr)
        return bytes_str

    def tcp_req(self,arpsrc_mac, src_ip):
        d_mac=arpsrc_mac
        s_mac=self.sys_mac
        d_ip=src_ip
        s_ip=self.sys_ip

        def sniftcp():
            #global p
            try:
                p=sniff(filter='tcp',timeout=3)
                f= p[1][2].flags
                if (f and (0x10)) or (f and (0x04)) :
                    print  src_ip + " is Authentic"##################### add to db
                    dbi.add_info(src_ip,d_ip)
                else :
                    print src_ip + " is spoofed"############################################################################################ popup
                    dbi.add_info_inv(src_ip,d_ip)
                    self.spoofDetectedSignal.emit(src_ip)
            except:
                print 'tcp spoofed ' + src_ip########################################################################################popup
                self.tcpSpoofedSignal.emit(src_ip)
                #dbi.add_info(src_ip,d_ip)

        def send_packets():
            global flag
            sendp(Ether(src=s_mac, dst=d_mac)/IP(src=s_ip, dst=d_ip)/TCP(dport=80)/b"Hello ")
        #try:
        snif_tcp_thread = threading.Thread(target=sniftcp, name = "snif_tcp_thread")
        snif_tcp_thread.start()
        send_packet_thread = threading.Thread(target=send_packets, name = "send_tcp_thread")
        send_packet_thread.start()

        #except:
            #print "Spoofed except wala"

    def arp_req(self,arpsrc_mac, src_ip):
        try:
            iFace = "wlo1"
            rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW,socket.htons(0x0800))
            rawSocket.bind((iFace, socket.htons(0x0800)))
            print "Raw Socket got created .... with the Ethernet Protocol Id : 0x0806 at interface %s"%str(iFace)
        except:
            print "Something unexpected happened during the Program execution."
        else:
            def checkMac(mac):
                if len(mac.split(":")) != 6:
                    print "The MAC is incorrect. It should be in Hexadecimal Format with each byte separated with colon...\n"
                    sys.exit(0)
                else:
                    macList = mac.split(":")
                    macLen = len(macList)
                    return tuple ([int(macList[index],16) for index in range(macLen)])
            def checkIp(ip):
                ipList = ip.split(".")
                ipLen = len(ipList)
                return int( "".join( [ "{:02X}".format(int(ele)) for ele in ipList ] ), 16 )
            dMac =  arpsrc_mac
            dMacTup = checkMac(dMac)

     #      sMac = raw_input("Enter the Source MAC .. hexadecimal charaters separated with ':' \n")
            sMac =  self.sys_mac
            sMacTup = checkMac(sMac)
            type = 0x0806
            #Creating an Ethernet Packet .... using dMac, sMac, type
            etherPack = struct.pack ("!6B6BH",*tuple(chain(dMacTup,sMacTup,[type])))
            #Creating an ARP Packet .... now
            hardwareType = 0x0001
            protocolType = 0x0800
            hln = 0x06
            pln = 0x04
            op = 0x0001
        #       srcIp = raw_input("Enter the Source IP ':' \n")
            srcIp = self.sys_ip
            intSrcIp = checkIp(srcIp)
            #destIp = raw_input("Enter the Destination IP .. \n")
            destIp = src_ip
            intDestIp = checkIp(destIp)
            arpPack = struct.pack("!HHBBH6BI6BI", *tuple(chain( [hardwareType,protocolType,hln,pln,op], sMacTup,[intSrcIp], dMacTup,[intDestIp] )))

         # Framing the final Pa
            finalPack = etherPack + arpPack
            for i in range(1):
                rawSocket.send(finalPack + "packet going yo!...")
                print "Sending Packet %d"%i
            arpop=0
            print "Closing the created Raw Socket ..."
            rawSocket.close()

    # unpack ethernet frame
    def ethernet_frame(self,data):
        dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
        return self.get_mac_addr(dest_mac), self.get_mac_addr(src_mac), socket.htons(proto),data[14:]

    def check_arp_response(self,raw_data):
        row = []
        #global raw_data
        #print 'Inside func'
        ethdest_mac, ethsrc_mac, eth_proto, data = self.ethernet_frame(raw_data)[0], self.ethernet_frame(raw_data)[1], self.ethernet_frame(raw_data)[2], self.ethernet_frame(raw_data)[3]
        arpdest_mac, arpsrc_mac, src_ip, arpop = self.arp_frame(raw_data)[0], self.arp_frame(raw_data)[1], self.arp_frame(raw_data)[2],  self.arp_frame(raw_data)[3]
        #print 'Checking the first if'
        if(ethdest_mac==arpdest_mac and arpsrc_mac != self.sys_mac):# and ethdest_mac!=arr[i] and c==0):
            #print 'First if is correct'
            print ('\nARP Source IP:')
            print src_ip
            print ('\nARP Operation:')
            print arpop
            print ('Destination: {}, Source: {}, Protocol: {}'.format(ethdest_mac, ethsrc_mac, eth_proto))

            srcip = QtGui.QStandardItem(src_ip)
            srcip.setEditable(False)
            row.append(srcip)

            destmac = QtGui.QStandardItem(ethdest_mac)
            destmac.setEditable(False)
            row.append(destmac)

            sourcemac = QtGui.QStandardItem(ethsrc_mac)
            sourcemac.setEditable(False)
            row.append(sourcemac)

            # proto = QtGui.QStandardItem(str(eth_proto))
            # proto.setEditable(False)
            # row.append(proto)

            ##### check in db #####
            if not dbi.present(src_ip,arpsrc_mac):
                if( arpop == 2 ):
                    if arpsrc_mac in self.source_mac_list:
                        print arpsrc_mac + ' is in list'
                        self.tcp_req(arpsrc_mac, src_ip)
                        self.source_mac_list.remove(arpsrc_mac)
                    else:
                        print arpsrc_mac + ' is not in list'
                        self.source_mac_list.append(arpsrc_mac)
                        self.arp_req(arpsrc_mac, src_ip)

            self.model.appendRow(row)
            self.modelUpdateSignal.emit(self.model)

        return
                    #return True
            #return False #2 means response


                        #c=c+1

    def snif(self):
        #global raw_data
        conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        print 'Starting main'
        while True:
            raw_data, addr = conn.recvfrom(65535)
            check_arp_thread = threading.Thread(target=self.check_arp_response, name='check_arp_response_thread', args = (raw_data, ))
            check_arp_thread.start()

    def run(self):
        self.snif()
        # conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        # while True:
        #     row = []
        #     raw_data, addr = conn.recvfrom(65535)
        #     ethdest_mac, ethsrc_mac, eth_proto, data = self.ethernet_frame(raw_data)[0], self.ethernet_frame(raw_data)[1], self.ethernet_frame(raw_data)[2], self.ethernet_frame(raw_data)[3]
        #     arpdest_mac, arpsrc_mac, src_ip = self.arp_frame(raw_data)[0], self.arp_frame(raw_data)[1], self.arp_frame(raw_data)[2]
        #     if(ethdest_mac==arpdest_mac):
        #         print ('\nEthernet Frame:')
        #         print src_ip
        #         print ('Destination: {}, Source: {}, Protocol: {}'.format(ethdest_mac, ethsrc_mac, eth_proto))
        #
        #         if not dbi.present(src_ip,arpsrc_mac):
        #             dbi.add_info(src_ip,arpsrc_mac)
        #
