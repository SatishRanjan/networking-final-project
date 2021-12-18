import httprequest
import os

class RequestBuilder:
    def __init__(self, request_message):
        self.request_message = request_message        
    def build(self):
        if self.request_message == None or str.isspace(self.request_message):
            return None

        # if the request message doesn't conform to the HTTP 1.1 RFC, return None
        message_lines = self.request_message.split("\r\n")
        request_line_parts = message_lines[0].split()
        if len(request_line_parts) != 3:
            return None

        # per HTTP 1.1 RFC
        http_method = message_lines[0].split()[0]
        requested_resource = request_line_parts[1]
        http_version = request_line_parts[2]

        request = httprequest.HttpRequest()        
        if requested_resource == "/" or requested_resource == "" or str.isspace(requested_resource):
            # By default the server returns the last 100 events
            request.requested_events_count = 100
        else:
            # Get the requested events count from the query string
            events_count_request_string = requested_resource.split("=")
            # This is the invalid events count, set the default to 100 as a result
            if len(events_count_request_string) < 2:
                request.requested_events_count = 100
            else:
                try:
                    requested_events_count = int(events_count_request_string[1])
                    if requested_events_count > 100:
                        request.requested_events_count = 100
                    else:
                        request.requested_events_count = requested_events_count
                except:
                    # If there's ivalid event count value in the request, set the value to default as a result
                    request.requested_events_count = 100

        request.request_method = http_method       
        request.http_version = http_version
        return request
