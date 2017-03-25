import socket
import struct
import textwrap

def arp_frame(data):
 arpHeader = data[14:42]
 arpHeaderUnpacked = struct.unpack('!HHBBH6s4s6s4s', arpHeader)
 arpSenderHardAddress = arpHeaderUnpacked[5]
 arpTargetHardAddress = arpHeaderUnpacked[7]
 arpSenderHardAddress = '%.2x:%.2x:%.2x:%.2x:%.2x:%.2x' % (ord(arpSenderHardAddress[0]), ord(arpSenderHardAddress[1]), ord(arpSenderHardAddress[2]), ord(arpSenderHardAddress[3]), ord(arpSenderHardAddress[4]), ord(arpSenderHardAddress[5]))
 arpTargetHardAddress = '%.2x:%.2x:%.2x:%.2x:%.2x:%.2x' % (ord(arpTargetHardAddress[0]), ord(arpTargetHardAddress[1]), ord(arpTargetHardAddress[2]), ord(arpTargetHardAddress[3]), ord(arpTargetHardAddress[4]), ord(arpTargetHardAddress[5]))
 return arpTargetHardAddress,arpSenderHardAddress


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
  arpdest_mac, arpsrc_mac = arp_frame(raw_data)[0], arp_frame(raw_data)[1]
  if(ethdest_mac==arpdest_mac):
   print ('\nEthernet Frame:')
   print ('Destination: {}, Source: {}, Protocol: {}'.format(ethdest_mac, ethsrc_mac, eth_proto))

   

if __name__ == '__main__':
    main()
