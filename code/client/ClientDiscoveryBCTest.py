from socket import *
import struct

PORT = 50000
MAGIC = "fna349fn" #to make sure we don't confuse or get confused by other programs
multicast_group = '10.10.4.255'
interface_ip = '10.10.4.175'
myMcast = (multicast_group, PORT)
myUcast = (interface_ip, PORT)
try:
    s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP) #create UDP socket
except socket.error:
    print("Failed to create socket")
    sys.exit()

print("Socket Created")

#s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) #this is a broadcast socket
s.bind((interface_ip, PORT))
#mreq = struct.pack("4sl", inet_aton(multicast_group), INADDR_ANY)
#s.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)
#s.setblocking(False)
print("Listening for Server's announcement on ", myUcast)

while 1:
    data, addr = s.recvfrom(1024) #wait for a packet
    if data.startswith(bytes(MAGIC.encode('utf-8'))):
        print("Got invite from " , myUcast , " to join server at ", addr)
    else:
        print("Not the MAGIC packet.")
