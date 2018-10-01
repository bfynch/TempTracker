#!/usr/bin/env python3
import requests
import json
from sense_hat import SenseHat
sense = SenseHat()
temp = round(sense.get_temperature(), 1)

# send a notification to pushbullet
def sendNotfication(title, body):
    data_send = {"type": "note", "title": title, "body": body}
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + "o.HJSghdccGeKYr301beb7aBZ4FhfSyUo3", 
                         'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Something went wrong')
    else:
        print('Notification sent')

# reads the temp set by the config file and compares to the current temperature 
def tempWarning():
    try:
        with open('temp.conf', 'r') as f:
            desired_temp = f.read()
            if int(desired_temp) < temp:
             sendNotfication("The temperature is " + str(temp), "It's warm; wear shorts!")
            else:
                sendNotfication("The temperature is " + str(temp), "It's cold; bring a sweater!")
    except IOError:
        print("Error: can't find file or read data")
    except ValueError: 
        print("Error: invalid value in temp.config")
tempWarning()