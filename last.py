import sys
import socket
import binascii
import struct
from itertools import chain
from struct import *

d_mac="18:cf:5e:27:75:df"
s_mac="b8:ee:65:02:de:bd"
d_ip="192.168.1.102"
s_ip="192.168.1.103" 
etherPack=""

def arpmod():

	try: 
		 iFace = "wlan0"
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
		 dMac =  d_mac
		 dMacTup = checkMac(dMac)
		 sMac =  s_mac
		 sMacTup = checkMac(sMac)
		 type = 0x0806
		 etherPack = struct.pack ("!6B6BH",*tuple(chain(dMacTup,sMacTup,[type])))
		 #print etherPack
		 hardwareType = 0x0001
		 protocolType = 0x0800
		 hln = 0x06
		 pln = 0x04
		 op = 0x0001
		 srcIp = s_ip   
		 intSrcIp = checkIp(srcIp)
		 destIp = d_ip
		 intDestIp = checkIp(destIp)
		 arpPack = struct.pack("!HHBBH6BI6BI", *tuple(chain( [hardwareType,protocolType,hln,pln,op], sMacTup,[intSrcIp], dMacTup,[intDestIp] )))
		 finalPack = etherPack + arpPack
		 for i in range(2):
			rawSocket.send(finalPack + "Hello peeps!...")
			print "Sending Packet %d"%i
	finally:
		print "Closing the created Raw Socket ..."
		rawSocket.close()


def tcpsend() :
	def checksum(msg):
		s = 0
		for i in range(0, len(msg), 2):
			w = ord(msg[i]) + (ord(msg[i+1]) << 8 )
			s = s + w
		s = (s>>16) + (s & 0xffff);
		s = s + (s >> 16);
		s = ~s & 0xffff
		return s
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
	except socket.error , msg:
		print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()
	packet = '';
	source_ip = s_ip
	dest_ip = d_ip # or socket.gethostbyname('www.google.com')
 	ip_ihl = 5
	ip_ver = 4
	ip_tos = 0
	ip_tot_len = 0  # kernel will fill the correct total length
	ip_id = 54321   #Id of this packet
	ip_frag_off = 0
	ip_ttl = 255
	ip_proto = socket.IPPROTO_TCP
	ip_check = 0    # kernel will fill the correct checksum
	ip_saddr = socket.inet_aton ( source_ip )   #Spoof the source ip address if you want to
	ip_daddr = socket.inet_aton ( dest_ip )
	ip_ihl_ver = (ip_ver << 4) + ip_ihl
	ip_header = pack('!BBHHHBBH4s4s' , ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)

	tcp_source = 1234   # source port
	tcp_dest = 80   # destination port
	tcp_seq = 454
	tcp_ack_seq = 0
	tcp_doff = 5    #4 bit field, size of tcp header, 5 * 4 = 20 bytes
	tcp_fin = 0
	tcp_syn = 1
	tcp_rst = 0
	tcp_psh = 0
	tcp_ack = 0
	tcp_urg = 0
	tcp_window = socket.htons (5840)    #   maximum allowed window size
	tcp_check = 0
	tcp_urg_ptr = 0
 	tcp_offset_res = (tcp_doff << 4) + 0
	tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh <<3) + (tcp_ack << 4) + (tcp_urg << 5)
 
	tcp_header = pack('!HHLLBBHHH' , tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window, tcp_check, tcp_urg_ptr)
 
	user_data = 'Hello, how are you'

	source_address = socket.inet_aton( source_ip )
	dest_address = socket.inet_aton(dest_ip)
	placeholder = 0
	protocol = socket.IPPROTO_TCP
	tcp_length = len(tcp_header) + len(user_data)
 
	psh = pack('!4s4sBBH' , source_address , dest_address , placeholder , protocol , tcp_length);
	psh = psh + tcp_header + user_data;
 
	tcp_check = checksum(psh)
	tcp_header = pack('!HHLLBBH' , tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window) + pack('H' , tcp_check) + pack('!H' , tcp_urg_ptr)
	packet = etherPack + ip_header + tcp_header + user_data
	#print etherPack
	#ip_hdr=[0x45,0x00,0x00,0x54,0x80,0xc6,0x40,0x00,0x40,0x01,0x36,0x8a,0xc0,0xa8,0x01,0x67,0xc0,0xa8,0x01,0x66]
 	#finpacket=etherPack + packet
 	s.sendto(packet, (dest_ip , 0 ))    # put this in a loop if you want to flood the target
 	print "packet sent"

 	try:
 		s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
 	except socket.error , msg:
 		print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
 		sys.exit()
 	print "socket created"
	if True:
		print "first if"
		pac = s.recvfrom(80)
		if(pac) :
			print "2nd if"
			temp=1
   			pac = pac[0]
   			ip_header = pac[0:20]
   			iph = unpack('!BBHHHBBH4s4s' , ip_header)
   			version_ihl = iph[0]
   			version = version_ihl >> 4
   			ihl = version_ihl & 0xF
   			iph_length = ihl * 4
   			ttl = iph[5]
   			protocol = iph[6]
   			s_addr = socket.inet_ntoa(iph[8]);
   			d_addr = socket.inet_ntoa(iph[9])
   			print s_addr
   			if s_addr== d_ip:
   				print "3rd if"
   				tcp_header = pac[iph_length:iph_length+20]
   				tcph = unpack('!HHLLBBHHH' , tcp_header)
   				flag=tcph[5]
   				print flag
   				ack=(temp<<2) & flag
   				temp=1
   				rst=(temp<<4) & flag 
   				print ack
   				print rst
   				if ack or rst:
   					print "Authentic "
			else :
				print "Spoofed"	
		else :
			print "Spoofed" 
def main() :
	arpmod()
	tcpsend()

if __name__ == '__main__':
    main()


