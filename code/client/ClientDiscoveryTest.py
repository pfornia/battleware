from socket import *
import struct

PORT = 50000
MAGIC = "fna349fn" #to make sure we don't confuse or get confused by other programs
multicast_group = '224.2.2.4'
interface_ip = '192.168.122.30'
myMcast = (multicast_group, PORT)

try:
    s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP) #create UDP socket
except socket.error:
    print("Failed to create socket")
    sys.exit()

print("Socket Created")

s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#server_address = ('localhost', PORT)
#s.bind(server_address)
s.bind((multicast_group, PORT))
#mreq = inet_aton(multicast_group) + inet_aton(interface_ip)
mreq = struct.pack("4sl", inet_aton(multicast_group), INADDR_ANY)
s.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)

print("Listening for Server's announcement on ", myMcast)

while 1:
    data, addr = s.recvfrom(10240) #wait for a packet
    if data.startswith(bytes(MAGIC.encode('utf-8'))):
        print("Got ", data, " from ", myMcast, " to join server at ", addr)
    else:
        print("Not the MAGIC packet.")
