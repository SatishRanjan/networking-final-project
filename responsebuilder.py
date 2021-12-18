import datetime
class HttpResponseBuilder:
     def build(self, status_code, status_name, content = None, content_length = 0, request_http_verb = None):
        current_datetime = datetime.datetime.utcnow()
        status_header = "HTTP/1.1" + " " + str(status_code) + " " + status_name + "\r\n"
        date_header = "Date: " + current_datetime.strftime('%b %d %Y %I:%M%p') + "\r\n"
        server_header = "Server: Satish Ranjan" + "\r\n"

        response = status_header + date_header + server_header

        # if content length is not zero add, the Content-Type and Content-Length header
        if content_length != 0:
            content_type_header = "Content-Type: text/html\r\n"
            content_length_header = "Content-Length: " + str(content_length) + "\r\n\r\n"
            response = response + content_type_header + content_length_header
        else:
            response = response + "\r\n"

        # if the Http request verb is get then add the content to the request body
        if content != None and request_http_verb == "GET":
            response = response + content

        return response