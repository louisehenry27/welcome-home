import requests
import time
import random
import asyncio
import json
import pandas as pd
from dateutil.parser import parse
import os

# colours = {
#     'cool_white': '{"bri": 254, "hue": 5618,  "sat": 141}',
#     'warm_white': '{"bri": 254, "hue": 34112, "sat": 254}',
#     'tungsten_white': '{"bri": 254,	"hue": 14988, "sat": 141}',
#     'red': '{"bri": 254,"hue": 34112, "sat": 141}',
#     # 'red': '{"xy": [ 0.6736, 0.3218 ]',
#     # 'white': '{"xy": [0.305,0.3259]}',
# }
# # 		"xy": [	0.6736, 0.3218 ],

def _random_colour():
    return {"hue": random.randint(1,65000)}

class Light:
    RED = {"bri": 254,"hue": 34112, "sat": 141}
    RANDOM = _random_colour()

    _HUE_BASE_URL = f'http://{os.environ["HUE_IP_ADDRESS"]}/api/{os.environ["HUE_USER_ID"]}'

    def __init__(self, light_id):
        self.light_id = light_id

    def set_colour(self, colour):
        return self._set_state(colour)

    def get_state(self):
        response = self._call_hue_api('/lights/{}'.format(self.light_id), 'get')
        return response.json()

    def turn_off(self):
        return self._set_state({'on': False})

    def turn_on(self):
        return self._set_state({'on': True})

    async def party(self, count, seconds):

        self.turn_on()
        for i in range(0, count):
            self.set_colour(_random_colour())
            await asyncio.sleep(seconds/count)

        self.turn_off()

        return "party is over :("

    def _set_state(self, data):
        return self._call_hue_api('/lights/{}/state'.format(self.light_id), 'put', data)

    def _call_hue_api(self, path, method, data=None):
        print('calling', method, Light._HUE_BASE_URL + path, data)
        return getattr(requests, method)(Light._HUE_BASE_URL + path, data=json.dumps(data) if (data is not None) else None) 

class LightSet:

    def __init__(self):
        self.lights = []

    def add_light(self, light):
        self.lights.append(light)

    def all_off(self):
        for light in self.lights:
            light.turn_off()

    def all_on(self):
        for light in self.lights:
            light.turn_on()

    def announce_arrival(self, device):
        print("lights: announce user arrival", device)
        if device == 'Zaks-iPhone':
            print('zak')
            loop = asyncio.get_running_loop()
            for light in self.lights:
                loop.create_task(light.party(seconds = 2, count = 2))
        elif device == 'Louise’s iPhone':
            self.all_on()

        pass