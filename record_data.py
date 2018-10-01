#!/usr/bin/env python3
import time
import sqlite3
import requests
import json
import os
from sense_hat import SenseHat
dbname='/home/pi/Assignment_1/assignment.db'
sense = SenseHat()
temp = round(sense.get_temperature(), 1)
humidity = round(sense.get_humidity(), 1)

# get data from SenseHat sensor
def getSenseHatData(temp, humidity):	
    if temp and humidity is not None:
        logData (temp, humidity)

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


# log sensor data on database
def logData (temp, humidity):	
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("INSERT INTO sensehat_data values(datetime('now', 'localtime'), (?), (?))", (temp, humidity))
    conn.commit()
    conn.close()

# prints all info from database and displays message on pi LEDs
def displayData():
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    print ("\nEntire database contents:\n")
    for row in curs.execute("SELECT * FROM sensehat_data"):
        print (row)
    conn.close()
    sense.show_message(str(temp))

# main function
def main():
    getSenseHatData(temp, humidity)
    sendNotfication("New data has been recorded", "")

main()
