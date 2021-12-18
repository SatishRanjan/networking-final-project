import os
from typing import Counter
import json

class MoistureEventsProvider():
    def __init__(self, events_folder_root_path):
        self.events_folder_root_path = events_folder_root_path        
    
    def get_moisture_events(self, requested_events_count):
        if not os.path.exists(self.events_folder_root_path):
            return ""
        
        events_files = next(os.walk(self.events_folder_root_path))[2]
        if len(events_files) == 0:
            return ""

        events_files.sort(reverse=True)
        files_to_read = []

        # If there's only one event file, only the latest file needs to be read
        if len(events_files) == 1:
            files_to_read.append(events_files[0])
        else:
            files_to_read.append(events_files[0])
            files_to_read.append(events_files[1])        
       
        response_data = []       
        counter = 0       
        for file_name in files_to_read:
            file_ref = open(os.path.join(self.events_folder_root_path, file_name), 'r')
            while counter < requested_events_count and counter < 100:
                line = file_ref.readline()                
                if line.strip() != '':                    
                    response_data.append(line.strip())
                    counter += 1
                else:
                    break
            file_ref.close()
        events_json = json.dumps(response_data)        
        return events_json