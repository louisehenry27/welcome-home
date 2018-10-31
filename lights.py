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

    def restore_state(self,previous_state):
        return self._set_state(previous_state)

    def turn_off(self):
        return self._set_state({'on': False})

    def turn_on(self):
        return self._set_state({'on': True})

    async def party(self, count, seconds,prev_state):

        self.turn_on()
        for i in range(0, count):
            self.set_colour(_random_colour())
            await asyncio.sleep(seconds/count)
        print(prev_state)
        self._set_state(prev_state)
        return "party is over :("


    def _set_state(self, data):
        return self._call_hue_api('/lights/{}/state'.format(self.light_id), 'put', data)

    def _call_hue_api(self, path, method, data=None):
        # print('calling', method, Light._HUE_BASE_URL + path, data)
        return getattr(requests, method)(Light._HUE_BASE_URL + path, data=json.dumps(data) if (data is not None) else None) 

class LightSet:

    def __init__(self):
        self.lights = {}

    def add_light(self, light_id, light):
        self.lights[light_id] = light

    def all_off(self):
        for light_id, light in self.lights.items():
            light.turn_off()

    def all_on(self):
        for light_id, light in self.lights.items():
            light.turn_on()       

    def current_state_on(self):
        state_dict = {}
        for light_id, light in self.lights.items():
            state_dict[light_id] = light.get_state()['state']
        return state_dict

    def restore_current_state_on(self,state_dict):
        for light_id, state in state_dict.items():
            light = self.lights[light_id]
            light.restore_state(state)

    def announce_arrival(self, device):
            # get the current state of all lights and store in dictionary
        state_dict = self.current_state_on()

        print("lights: announce user arrival", device)
        if device == 'Zaks-iPhone':
            loop = asyncio.get_running_loop()
            for light_id, light in self.lights.items():
                for dict_light_id, state in state_dict.items():
                    if light_id == dict_light_id:
                        loop.create_task(light.party(seconds = 2, count = 2, prev_state = state))
                
        elif device == 'Louise’s iPhone':
            loop = asyncio.get_running_loop()
            for light_id, light in self.lights.items():
                for dict_light_id, state in state_dict.items():
                    if light_id == dict_light_id:
                        loop.create_task(light.party(seconds = 5, count = 4, prev_state = state))
        

        

        pass
