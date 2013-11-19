from IWList import *
import xgpsd
from subprocess import Popen, PIPE, STDOUT
import sys, os, logging, time, subprocess, thread, re
import RPi.GPIO as GPIO
import Tweet
import json
import sqlite3 as lite
from pprint import pprint

logging.basicConfig()
log = logging.getLogger("wifido")
log.setLevel(logging.DEBUG)

interface = "wlan1"  # Use a second wireless device


 # How long to wait for a given signal strength (between 0 and 1)
def wait_time (signal):
    return 5 - 4*signal


if __name__ == "__main__":

    con = lite.connect('db/db.sqlite3')

    json_file = open('auth.json')
    json_data = json.load(json_file)
    json_file.close()

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)

    xgpsd.start_listening()

    while True:
        # Get GPS data
        gpsdata = xgpsd.get_data()

        # Process WiFi data
        strongest_signal = 0
        for cell in IWList(interface).getData().values():

            match = re.match(r"(\d+)/(\d+)", cell["Signal"])
            strength_nu = match.group(1)
            strength_de = match.group(2)
            strength = float(strength_nu) / float(strength_de)
            essid = cell["ESSID"]
            mac = cell["MAC"]

            if essid == "":
                continue

            # Keep track of the strength of our primary network.
            if essid == "Westmont_Encrypted" and strength > strongest_signal:
                strongest_signal = strength

            Tweet.bark(essid, json_data)

            # Write to db
            values = [
                      str(gpsdata["time"]),
                      str(mac),
                      str(essid),
                      str(strength),
                      str(gpsdata["lat"]),
                      str(gpsdata["lon"]),
                      str(gpsdata["alt"])
                     ]

            cur = con.cursor()
            cur.execute("INSERT INTO wifis values('" + "','".join(values) + "')")
            

            
        con.commit()

        print "Current signal strength: " + str(strongest_signal)
        print "Location: " + str(gpsdata["lat"]) + " " + str(gpsdata["lon"]) + " " + str(gpsdata["alt"])

        # Blink LED
        GPIO.output(11, False)
        time.sleep(.1)
        GPIO.output(11, True)

        # Sleep while playing sound
        proc = subprocess.Popen(['mpg321', '-q', 'beep.mp3'], shell=False)
        time.sleep(wait_time(strongest_signal))
        proc.terminate()
        proc.wait()
