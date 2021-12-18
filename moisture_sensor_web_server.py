import RPi.GPIO as GPIO
import time
import socket
import threading
import os
import moisture_event_processor as mep
import moisture_event as me
from datetime import datetime
import requestprocessor
import sys
import moisture_event_publisher as eventpublisher
import test_event_publisher as tep


# By default the server runs in the client server mode
server_mode = "clientserver"

HOST = ''      # Standard loopback interface address, empty means server is listening for all of the network interfaces
PORT = 8965   # Port to listen on (non-privileged ports are > 1023)
print("Arg length:" + str(len(sys.argv)))
if len(sys.argv) == 3:
    PORT = int(sys.argv[1])
    server_mode = str(sys.argv[2])

if server_mode != "clientserver" and server_mode != "pubsub":
    print("Invalid server mode {0}, the server mode can either be 'clientserver' or 'pubsub'".format(server_mode))
    sys.exit()

moisture_event_publisher_test = None
moisture_event_publisher = None
if server_mode == "pubsub":
    moisture_event_publisher = eventpublisher.MoistureEventPublisher()
    # This is only used to test in the pubsub mode
    moisture_event_publisher_test = tep.MoistureEventPulisherTest(moisture_event_publisher)

# The current directory will be the default directory for the moisture events storage
current_directory = os.getcwd()
event_processor = mep.MoistureEventProcessor(current_directory)

#GPIO setup
#The signal input port is GPIO21 (PIN# 40 on Raspberry Pi4)
channel = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

is_moisture_detected = "no"
def callback(channel):
    global is_moisture_detected
    timestamp = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S.%f")   
    if GPIO.input(channel):
        print("No moisture detected")
        is_moisture_present = "no"        
    else:
        print("Moisture detected")
        is_moisture_present = "yes"
    
    moist_evt = me.MoistureEvent(timestamp, is_moisture_present)
    event_processor.process_moisture_event(moist_evt)

    # If the web server is running in the pubsub mode, send the event to MoistureEventPublisher for publishing to connected clents sockets
    if server_mode == "pubsub":
        moisture_event_publisher.publish_event(moist_evt)

# Setup the callbach channel and function for the GPIO pin voltage change
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(channel, callback)

svr_socket = None

print("The web server is runnig in the {0} mode on port {1}".format(server_mode, PORT))

svr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
svr_socket.bind((HOST, PORT))
svr_socket.listen(1000)
while True:
    print('Server is listening for the client connection')
    client_socket, client_addr = svr_socket.accept()
    print('Connected client is: ', client_addr)
    if server_mode == "pubsub":
        print('Server added client socket to the moisture event publisher')
        moisture_event_publisher.add_socket(client_socket)
        '''
        # This code is to test the connected client sockets
        moisture_event_publisher_test_thread = threading.Thread(target=moisture_event_publisher_test.publish_test_events())
        moisture_event_publisher_test_thread.start()
        '''
    else:
        # In the clientserver mode proces the http request through request processor
        response_thread = threading.Thread(target=requestprocessor.RequestProcessor(client_socket, client_addr, current_directory).process_request())   
        response_thread.start()
  
            
    