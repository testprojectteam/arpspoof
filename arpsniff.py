import socket
import struct
import textwrap
from itertools import chain
def arp_frame(data):
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
def get_mac_addr(bytes_addr):
 bytes_str =  ":".join("{:02x}".format(ord(c)) for c in bytes_addr)
 return bytes_str


# unpack ethernet frame
def ethernet_frame(data):
 dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
 return get_mac_addr(dest_mac), get_mac_addr(src_mac), socket.htons(proto),data[14:]


def main():
 conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
 while True:
  raw_data, addr = conn.recvfrom(65535)
  ethdest_mac, ethsrc_mac, eth_proto, data = ethernet_frame(raw_data)[0], ethernet_frame(raw_data)[1], ethernet_frame(raw_data)[2], ethernet_frame(raw_data)[3]
  arpdest_mac, arpsrc_mac, src_ip, arpop = arp_frame(raw_data)[0], arp_frame(raw_data)[1], arp_frame(raw_data)[2],  arp_frame(raw_data)[3]
  if(ethdest_mac==arpdest_mac):
   print ('\nARP Source IP:')
   print src_ip
   print ('\nARP Operation:')
   print arpop
   print ('Destination: {}, Source: {}, Protocol: {}'.format(ethdest_mac, ethsrc_mac, eth_proto))

   if(arpop==2):
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
   				print "The MAC is in correct. It should be in Hexadecimal Format with each byte separated with colon...\n" 
   				sys.exit(0)
   			else:
   				macList = mac.split(":")
   				macLen = len(macList)
   				return tuple ([int(macList[index],16) for index in range(macLen)])
		def checkIp(ip):
			ipList = ip.split(".")
			ipLen = len(ipList)
			return int( "".join( [ "{:02X}".format(int(ele)) for ele in ipList ] ), 16 )

    #dMac = raw_input("Enter the Destination MAC .. hexadecimal charaters separated with ':' \n")
		dMac =  arpsrc_mac
		dMacTup = checkMac(dMac)

 #  sMac = raw_input("Enter the Source MAC .. hexadecimal charaters separated with ':' \n")
		sMac =  "18:cf:5e:27:75:c1"
		sMacTup = checkMac(sMac)
		type = 0x0806


 # Creating an Ethernet Packet .... using dMac, sMac, type

		etherPack = struct.pack ("!6B6BH",*tuple(chain(dMacTup,sMacTup,[type])))



  # Creating an ARP Packet .... now

		hardwareType = 0x0001

		protocolType = 0x0800
		hln = 0x06
		pln = 0x04
		op = 0x0001

#       srcIp = raw_input("Enter the Source IP ':' \n")
		srcIp = "192.168.153.103"    
		intSrcIp = checkIp(srcIp)
    #destIp = raw_input("Enter the Destination IP .. \n")
		destIp = src_ip
		intDestIp = checkIp(destIp)


		arpPack = struct.pack("!HHBBH6BI6BI", *tuple(chain( [hardwareType,protocolType,hln,pln,op], sMacTup,[intSrcIp], dMacTup,[intDestIp] )))

 # Framing the final Packet

		finalPack = etherPack + arpPack

		for i in range(2):
			rawSocket.send(finalPack + "Meeta rocks!...")
			print "Sending Packet %d"%i
	finally:
		arpop=0
		print "Closing the created Raw Socket ..."
		rawSocket.close()


if __name__ == '__main__':
    main()
