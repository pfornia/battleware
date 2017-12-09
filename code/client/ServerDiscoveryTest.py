import sys, time
from socket import *
import struct

PORT = 50000
MAGIC = "fna349fn" #to make sure we don't confuse or get confused by other programs
multicast_group = '224.2.2.4'

try:
    s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP) #create UDP socket
except socket.error:
    print("Failed to create socket")
    sys.exit()

print("Socket Created")

myMcast = (multicast_group, PORT)
#s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) #this is a broadcast socket
s.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, 2)
#mreq = struct.pack("4sl", inet_aton(multicast_group), INADDR_ANY)
#s.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)
my_ip= gethostbyname(gethostname()) #get our IP. Be careful if you have multiple network interfaces or IPs

try:    
    #To use local active IP address
    #s = socket(AF_INET, SOCK_DGRAM) 
    s.connect(('8.8.8.8', 0))
    localIP = s.getsockname()
    #print(localIP)   
    #s.close()
    splitIP = str(localIP).split('.')
    onlyIP = str(localIP).split('\'')
    splitIP[3:] = (['0/24'])
    IPRange = ".".join(splitIP)
    #Not needed but saving it
    splitFields = str(localIP).split(',')
    splitIP[1:] = (['1338)'])
    newAddress = ",".join(splitFields)
    myLink = (str(onlyIP[1]),1338)
except:
    print("No network connection found, trying localhost.")
    myLink = ('localhost',1339)

print("STARTING SERVER ON " + str(myLink))

while 1:
    #data = MAGIC+my_ip
    data = MAGIC+str(myLink)
    #s.sendto(data.encode('utf-8'), ('localhost', PORT))
    s.sendto(data.encode('utf-8'), myMcast)
    print("Sending service announcement on ", myMcast)
    time.sleep(5)
    s.send
