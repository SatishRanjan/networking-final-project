import json

class MoistureEventPublisher:
    def __init__(self):
        self.client_sockets = []

    def add_socket(self, client_socket):
        self.client_sockets.append(client_socket)
    
    def publish_event(self, moisture_event):
        # Send the data to all connected clients
        for client_socket in self.client_sockets:
            try:
                moisture_event_json_str = json.dumps(moisture_event.__dict__)
                client_socket.sendall (moisture_event_json_str.encode('utf8'))
            except:
                # If there's an error sending the data to the socket, remove it from the client_sockets list,
                # As the clients might have been disconnected
                self.client_sockets.remove(client_socket)