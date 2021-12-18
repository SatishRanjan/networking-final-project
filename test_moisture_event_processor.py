import os
import moisture_event_processor as mep
import utils
from datetime import datetime
import moisture_event as me
import json

is_moisture_present = "no"
current_directory = os.getcwd()
event_processor = mep.MoistureEventProcessor(utils.ServerMode.CLIENT_SERVER, current_directory)

counter  = 1
while counter <= 101:
    timestamp = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S.%f")
    moist_evt = me.MoistureEvent(timestamp, is_moisture_present)
    if counter == 101:
        print("stop")
    event_processor.process_moisture_event(moist_evt)
    counter = counter + 1