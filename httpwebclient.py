#!/usr/bin/python

# based on: https://stackoverflow.com/questions/5755507/creating-a-raw-http-request-with-sockets

import socket
from urllib.parse import urlparse
import re
import os
import sys

# default port number of the web server
PORT = 65432
HOST = ""
HTTP_METHOD = "GET"
RESOURCE_PATH = "/"
CRLF = "\r\n"

# Default url
arg1 = "http://localhost:65432/?event_count=7"
print("Arg length:" + str(len(sys.argv)))
if len(sys.argv) == 2:
    arg1 = sys.argv[1]

server_and_port = arg1.split(":")
if len(server_and_port) < 2:
    print("Invalid URL scheme, URl should be in the format http://hostname:port/resource_path")
    sys.exit()

url = urlparse(arg1)
HOST = url.hostname
if url.port != None:
    PORT = url.port

if url.query != None and url.query != "":
    RESOURCE_PATH = RESOURCE_PATH + "?" + url.query

# If there are two or more arguments passed, then first argumnet is expected to be the host:port number 
# and second argument is expected to be the HTTP Verb name (GET or HEAD)
if len(sys.argv) >= 3:
    arg2 = sys.argv[2]
    if arg2 != None or arg2 != "":
        HTTP_METHOD = arg2

print("Argument successfully validated")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""
***********************************************************************************
* Note that the connect() operation is subject to the timeout setting,
* and in general it is recommended to call settimeout() before calling connect()
* or pass a timeout parameter to create_connection().
* The system network stack may return a connection timeout error of its own
* regardless of any Python socket timeout setting.
***********************************************************************************
"""
s.settimeout(240)
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

msg = HTTP_METHOD + " %s HTTP/1.1%s" % (RESOURCE_PATH, CRLF)
print("msg request: \n", msg)

# send HTTP get request
s.send(msg.encode())

BUFF_SIZE = 4096
data = b''
while True:
    part = s.recv(BUFF_SIZE)
    data += part
    if not part or len(part) < BUFF_SIZE:          
        break
text_file = open("output.txt", "w")
text_file.write(data.decode("utf8"))
text_file.close()
print("received data: " + data.decode("utf8"))

# shutdown and close tcp connection and socket
s.shutdown(2)
s.close()


