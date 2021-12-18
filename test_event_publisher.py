import moisture_event_publisher
import threading
import time
from datetime import datetime
import moisture_event as me

class MoistureEventPulisherTest():
    def __init__(self, moisture_event_publisher):
        self.moisture_event_publisher = moisture_event_publisher

    def publish_test_events(self):
        time.sleep(5)
        counter = 1
        while counter <= 10:
            timestamp = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S.%f")
            moist_evt = me.MoistureEvent(timestamp, "yes")
            self.moisture_event_publisher.publish_event(moist_evt)
            time.sleep(5)