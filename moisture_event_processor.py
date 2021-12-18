from threading import Thread, Lock
import moisture_event
import os
import glob
import const
import json

class MoistureEventProcessor:
    def __init__(self, moisture_event_store_file_path):       
        self.event_counter_file_path = moisture_event_store_file_path
        self.moisture_event_store_file_path = os.path.join(moisture_event_store_file_path, const.MOISTURE_EVENTS_DATA_FOLDER_NAME)
        self.file_name_prefix = const.MOISTURE_EVENTS_STORE_FILE_NAME_PREFIX        
        self.file_sequence_number = 0
        self.latest_file_name = self.file_name_prefix + str(self.file_sequence_number) + ".txt"
        self.event_count_file_name = const.EVENTS_COUNTER_FILE_NAME
        self.event_counter = 0
        self.txtfiles = []
        self.mutex = Lock()
        self.bootstrap_events_storage()

    def bootstrap_events_storage(self):
        if self.moisture_event_store_file_path == "":
            return

        # If the moisture event store path doesn't exist, create the folder
        if not os.path.exists(self.moisture_event_store_file_path):
            os.makedirs(self.moisture_event_store_file_path)
        
        # If the event_count.txt file doesn't exist, create one
        if not os.path.exists(os.path.join(self.event_counter_file_path, self.event_count_file_name)):
            open(os.path.join(self.event_counter_file_path, self.event_count_file_name), "w")
        
        # If there're already moisture event data file, read file_sequence_number, latest_file_name and event_counter
        self.txtfiles = next(os.walk(self.moisture_event_store_file_path))[2]

        if len(self.txtfiles) > 0:
            # Sort the file in the reverse order, so that the highest sequence number file (i.e. the latest file come on top)
            self.txtfiles.sort(reverse=True)
            self.latest_file_name = self.txtfiles[0]

            # Get the latest file sequence number and set it as the file_sequence_number for the MoistureEventProcessor
            latest_file_part_with_seq_number = self.txtfiles[0].split("_")[1]
            if latest_file_part_with_seq_number != "":
                seq_number_text = latest_file_part_with_seq_number.split(".")[0]
                if  seq_number_text != "":
                    self.file_sequence_number = int(seq_number_text)

            # Read the event_count.txt file and if there're existing events, update the event_counter for the MoistureEventProcessor to start with
            event_count_file = open(os.path.join(self.event_counter_file_path, self.event_count_file_name), "r")
            event_count = event_count_file.readline()
            event_count_file.close()

            if event_count != "":
                self.event_counter = int(event_count)

    def process_moisture_event(self, moist_event):
        if moist_event is None:
            return
        
        self.write_moisture_event_to_file(moist_event)

    def update_latest_file_name(self):
        self.mutex.acquire()
        try:
            self.file_sequence_number = self.file_sequence_number + 1           
            self.latest_file_name = self.file_name_prefix + str(self.file_sequence_number) + ".txt"
        finally:
            self.mutex.release()
    
    def write_moisture_event_to_file(self, moist_event):
        # Each file contains only 100 events for the query performance reason
        file_event_quotient = self.event_counter // 100

        # If the file_sequence_number doesn't match the file_event_quotient, that means a new file needs to be created for the new events for a 
        # file to not contain more than 100 events for the query performance reasons
        if self.file_sequence_number != file_event_quotient:
            self.update_latest_file_name()

        self.mutex.acquire()
        try:
            self.event_counter = self.event_counter + 1
            event_count_file = open(os.path.join(self.event_counter_file_path, self.event_count_file_name), "w")
            event_count_file.write(str(self.event_counter))
            event_count_file.close()
        finally:
            self.mutex.release()

        # Write moisture events to the file
        #convert to JSON string
        jsonStr = json.dumps(moist_event.__dict__)
        line_to_write = jsonStr + "\n"
        f = open(os.path.join(self.moisture_event_store_file_path, self.latest_file_name), "a")
        f.write(line_to_write)
        f.close()
