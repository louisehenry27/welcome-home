from lights import Light, LightSet
from sheets import Sheet
from time import sleep
from datetime import datetime, timedelta
from people import Person
import os

datasource = f'{os.environ["GOOGLE_SHEET_KEY"]}'

# people_devices = {
#     'ZAK': 'Zaks-iPhone',
#     'LOUISE': 'Louise\'s iPhone'
# }
    # dictionary to store current status 
person_status = {
    'Zaks-iPhone': None,
    'Louise’s iPhone': None
}

sheet = Sheet(datasource)

lights = LightSet()

for i in range(0, 13):
    lights.add_light(Light(i))

# louise = Person('Louise')
# zak = Person('Zak')

previous_index = None # -1??

async def poll_event(loop, prev_datetime):

    global previous_index

    # print('prev_datetime', prev_datetime)
    # last_record = sheet.get_last_record()
    # now = datetime.now()
    # previous_timestamp = datetime.now() - timedelta(seconds = seconds)
    records_since = sheet.get_records_since_index(previous_index)
    print(records_since)

    if (len(records_since) == 0):
        return

    for index, event in records_since.iterrows():
        if person_status[event['Device']] != event['Status']:    
            person_status[event['Device']] = event['Status']

            if previous_index is not None:
                if event['Status'] == 'Connected':
                    lights.announce_arrival(event['Device'])
                elif event['Status'] == 'Disconnected':
                    print('turn off (if all disconnected)')

    previous_index = records_since.index[-1]
    print(previous_index)
        
    #         # if (event['Device'] == people_device['LOUISE']):
    #         #     lights.annouce_arrival(louise)
    #         # elif (event['Device'] == people_devices['ZAK']):
    #         #     lights.annouce_arrival(zak)


    # date_last_record = last_record['Timestamp'][0]
    # if previous_timestamp < date_last_record < now:
    #     print('update lights')
    #     # for device, status in person_status.items():
    #     #     if last_record['Device'][0] == device and person_status[device] != last_record['Status'][0]:
    #     #         person_status[device] = last_record['Status'][0]
    #     #         if last_record['Status'] == 'Connected':
    #     #             # lights on
    #     #         elif last_record['Status'] =='Disconnected':
    #     #             # lights off if both disconnected
    #     #     else:
    #     #         print('fail')
    # else:
    #     print("no update")
        


# lamp = Light(1)

# lamp.set_colour(Light.RANDOM)
# sleep(0.5)
# lamp.turn_off()
# sleep(1.5)
# lamp.turn_on()

# print(lamp.get_state())