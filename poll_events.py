from lights import Light, LightSet
from sheets import Sheet
from time import sleep
from datetime import datetime, timedelta
from people import Person
import os

datasource = f'{os.environ["GOOGLE_SHEET_KEY"]}'

    # dictionary to store current status 
person_status = {
    'Zaks-iPhone': None,
    'Louise’s iPhone': None
}

sheet = Sheet(datasource)

lights = LightSet()

for i in range(1, 13):
    lights.add_light(i, Light(i))

# louise = Person('Louise')
# zak = Person('Zak')

previous_index = None

async def poll_event(loop, prev_datetime):

    global previous_index

    records_since = sheet.get_records_since_index(previous_index)

    if (len(records_since) == 0):
        return

    for index, event in records_since.iterrows():
            # match the device per the new sheet addition to the device in the person_status dictionary
            # if the current status of the device doesn't match the new sheet addition, then update the dictionary.
        if person_status[event['Device']] != event['Status']:
            person_status[event['Device']] = event['Status']
            if previous_index is not None:
                    # if the status is connected, do connection event
                if event['Status'] == 'Connected':
                    lights.announce_arrival(event['Device'])
                    # else if the status is disconnected and all other devices are disconnected, then turn all lights off.
                elif event['Status'] == 'Disconnected':
                    if all(status == 'Disconnected' for status in person_status.values()):
                        print('Everyone is Disconnected, turning all lights off')
                        lights.all_off()
    previous_index = records_since.index[-1]
        



# lamp = Light(1)

# lamp.set_colour(Light.RANDOM)
# sleep(0.5)
# lamp.turn_off()
# sleep(1.5)
# lights.turn_on()

# print(lamp.get_state())