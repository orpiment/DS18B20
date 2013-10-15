#!/usr/bin/python

import time, httplib, urllib, os, glob, socket, gmaileralert
from datetime import datetime


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

""" 
This script streams data to ThingSpeak:
https://www.thingspeak.com
"""

def readsensor(input):
    raw = open(input, "r").read()
    temperature = float(raw.split("t=")[-1])/1000
    return round(temperature, 1)

def doit(input):
    params = urllib.urlencode(input)
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    conn.request("POST", "/update", params, headers)
    response = conn.getresponse()
    # Uncomment the print statement to check connection to TS
    #  print response.status, response.reason
    data = response.read()
    conn.close()

def log_temperature(input):
    with open("log_temperature.txt", "a") as f: 
        f.write(str(datetime.now()))
        for sensor, temperature in sorted(input.items()):
            f.write("\t")
            f.write(str(temperature))
        f.write("\n")

if __name__ == "__main__":
    # dictionary for each sensor and device location
    w1= { 'field1': '/sys/bus/w1/devices/28-00000521ca90/w1_slave' }
    
    toemail = "From: My <email@gmail.com>\n"
    fromemail = "To: You <email@mac.com>\n"
    subject = "Subject: RPI Sensor Error \n"
    msg1 = "There is a problem with the temperture sensor."
    msg2 = "The program quit, SystemExit error."
    mymsg = toemail + fromemail + subject

    print "starting temperature readings on: " + str(datetime.now())
    while True:
        try:
            dict = { }
            for key, value in w1.iteritems():
                dict[key] = readsensor(value)
           
            # Log the data to a file
            # log_temperature(dict)

            # add Things Speak special API key pair
            dict['key'] = 'ThingSpeak Key'
            
            doit(dict) # send the data to Things Speak
            
            #sleep for 16 seconds (api limit of 15 secs)
            time.sleep(16)

        except socket.gaierror, e:
            print "%s There was a socket.gaierror: %s" % (e, str(datetime.now()))
            gmaileralert.blue_alert(mymsg+msg1)
            time.sleep(15)
        except socket.error, e:
            print "%s There was a socket.error: %s" % (e, str(datetime.now()))
            gmaileralert.blue_alert(mymsg+msg1)
            time.sleep(15)
        except (SystemExit):
            gmaileralert.blue_alert(mymsg+msg2)
            raise
