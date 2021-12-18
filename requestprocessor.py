import sys
import requestvalidator as reqv
import requestbuilder as reqb
import responsebuilder as resb
import moisture_events_data_provider as mep
import os
import const

class RequestProcessor:
    def __init__(self, client_socket, client_address, moisture_events_root_directory):
        self.client_socket = client_socket
        self.client_address = client_address
        self.events_root_directory = moisture_events_root_directory      
        self.events_data_provider = mep.MoistureEventsProvider(os.path.join(moisture_events_root_directory, const.MOISTURE_EVENTS_DATA_FOLDER_NAME))
    
    def process_request(self):        
        if self.client_socket == None:
            print("Client socket is null or address is empty")
            sys.exit()
            
        response = ""
        print("Processing request for the client: %s" % (self.client_address,))  
        try:
            request_message = self.get_request_message()
            httprequest = reqb.RequestBuilder(request_message).build()
            is_valid = reqv.RequestValidator.validate(httprequest)

            # if the request is invalid then send the bad request response
            if is_valid == False:
                response = resb.HttpResponseBuilder().build(501, "Not Implemented")          
                print("Reposne data:" + response)
                self.client_socket.sendall (response.encode('utf8'))
                return
            
            # Get the data from the events data provider, if the events data files doesn't exist and empty string response is returned
            response_string = self.events_data_provider.get_moisture_events(httprequest.requested_events_count)          
            response = resb.HttpResponseBuilder().build(200, "OK", response_string, len(response_string.encode('utf-8')), httprequest.request_method)

            print("Reposne data:" + response)
            self.client_socket.sendall (response.encode('utf8'))
        except:
            response = resb.HttpResponseBuilder().build(500, "Internal server error")          
            print("Reposne data:" + response)
            self.client_socket.sendall (response.encode('utf8'))

    def get_request_message(self):
        BUFF_SIZE = 4096
        data = b''
        while True:
            part = self.client_socket.recv(BUFF_SIZE)
            data += part
            if not part or len(part) < BUFF_SIZE:              
                break
        print("Received data: " + data.decode("utf8"))
        return data.decode("utf8")