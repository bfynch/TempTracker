#!/usr/bin/env python3
import bluetooth
import sqlite3
import string
import requests
import json
from sense_hat import SenseHat

conn=sqlite3.connect('/home/pi/Assignment_1/bt-devices.db')
curs=conn.cursor()
reg_devices = []
sense = SenseHat()
temp = round(sense.get_temperature(), 1)

def sendNotfication(title, body):
    data_send = {"type": "note", "title": title, "body": body}
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + "o.HJSghdccGeKYr301beb7aBZ4FhfSyUo3", 
                         'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Something went wrong')
    else:
        print('Notification sent')

def searchDevices():
    # retrieves all device names from db, converts to string and removes punctuation, and adds to list
    for i in curs.execute("select device_name from bt_devices"):
        device = str(i)
        translator = str.maketrans('', '', string.punctuation)
        reg_devices.append(device.translate(translator))
    
    while True:
        nearby_devices = bluetooth.discover_devices()
        da=None
        for mac_address in nearby_devices:
            for i in reg_devices:
                if i == bluetooth.lookup_name(mac_address, timeout=5):
                    da=i
                    conn.close
                    break
                
            if da is not None:
                print("{} has connected! The current temperature is {}".format(i, temp))    
                sendNotfication("{} has connected!".format(i), "The current temperature is {}".format(temp))
                sense.show_message("{} has connected! The current temperature is {}".format(i, temp), scroll_speed=0.05)
                break
            else:                    
                print("Searching for devices...")

searchDevices()
