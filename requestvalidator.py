class RequestValidator:
    def validate(httprequest):               
        if httprequest == None \
            or (httprequest.request_method != "GET"):
            return False
        return True