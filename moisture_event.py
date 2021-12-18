from datetime import datetime
import json

class MoistureEvent:
    def __init__(self, utc_datetime, is_moisture_present):
        self.IsMoisturePresent = is_moisture_present
        self.UtcDateTime = utc_datetime

    def get_moisture_event(self):
        return self