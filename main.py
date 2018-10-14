from lights import Light
from sheets import Sheet
from time import sleep
from datetime import datetime, timedelta
import os

datasource = f'{os.environ["GOOGLE_SHEET_KEY"]}'

    # dictionary to store current status 
person_status = {
    'Louise\'s iPhone':'Connected',
    'Zaks-iPhone':'Connected',
}

while True:
    last_record = Sheet(datasource).get_last_record()
    now = datetime.now()
    previous_timestamp = datetime.now() - timedelta(minutes = 2)
    date_last_record = last_record['Timestamp'][0]
    if previous_timestamp < date_last_record < now:
        print('update lights')
        # for device, status in person_status.items():
        #     if last_record['Device'][0] == device and person_status[device] != last_record['Status'][0]:
        #         person_status[device] = last_record['Status'][0]
        #         if last_record['Status'] == 'Connected':
        #             # lights on
        #         elif last_record['Status'] =='Disconnected':
        #             # lights off if both disconnected
        #     else:
        #         print('fail')
    else:
        print("no update")
        




lamp = Light(1)

# lamp.set_colour(Light.RANDOM)
# sleep(0.5)
# lamp.turn_off()
# sleep(1.5)
lamp.turn_on()

# print(lamp.get_state())