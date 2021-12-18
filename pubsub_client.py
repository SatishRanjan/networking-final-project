import socket
from urllib.parse import urlparse
import sys

# default port number and hostname of the web server
PORT = 8965
HOST = "localhost"

print("Arg length:" + str(len(sys.argv)))
if len(sys.argv) == 3:
    HOST = str(sys.argv[1])
    PORT = int(sys.argv[2])
    

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""
**************************************************************************************
* Avoid socket.error: [Errno 98] Address already in use exception
* The SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state,
* without waiting for its natural timeout to expire.
**************************************************************************************
"""
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print("Host name: " + HOST)
print("Port: " + str(PORT))
# set up TCP connection
s.connect((HOST, PORT))

print("Connected to the moisture sever as subscriber to receive the moisture events")


# Keep running the client with the connected socket to receive the published events from the server
BUFF_SIZE = 4096
data = b''
while True:
    try:
        part = s.recv(BUFF_SIZE)
        data += part
        if not part or len(part) < BUFF_SIZE:
            if data != b'':
                print("Moisture event received, event data: " + data.decode("utf8"))          
            data = b''
    except:
        print("Sever socket connection is broken, closing the client socket") 
        s.close()
        break


