import moisture_events_data_provider as mep
import os
import const

current_directory = os.getcwd()
moisture_events_directory_path = os.path.join(current_directory, const.MOISTURE_EVENTS_DATA_FOLDER_NAME)

events_data_provider = mep.MoistureEventsProvider(moisture_events_directory_path)
moisture_events = events_data_provider.get_moisture_events(3)
print(moisture_events)