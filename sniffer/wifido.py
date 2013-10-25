from IWList import *
from subprocess import Popen, PIPE, STDOUT
from datetime import date, datetime, timedelta
import sys, os, logging, time, subprocess, thread, re
import RPi.GPIO as GPIO
import Tweet
import json
from pprint import pprint

logging.basicConfig()
log = logging.getLogger("wifido")
log.setLevel(logging.DEBUG)

interface = "eth1"
current_signal = -0.1
multiplier = 4
wait_time = 5


if __name__ == "__main__":

    json_file = open('auth.json')
    json_data = json.load(json_file)
    json_file.close()

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)

    while True:
        # Get GPS data
        # store in a temp var
        # gpsdata = {time: 12341234, alt: 432, lat: 431423.23, lon: -3232.22}

        # Process WiFi data
        for cell in IWList(interface).getData().values():

            match = re.match(r"(\d+)/(\d+)", cell["Signal"])
            strength_nu = match.group(1)
            strength_de = match.group(2)
            strength = float(strength_nu) / float(strength_de)
            essid = cell["ESSID"]

            print strength_nu + " / " + strength_de + " = " + str(strength) + " for " + current_essid
            # Keep track of the strength of our primary network.
            if essid == "Westmont_Encrypted"
                current_signal = strength

            Tweet.bark(essid, json_data)

            # write to db

        # Blink LED
        GPIO.output(11, False)
        time.sleep(.1)
        GPIO.output(11, True)

        # Sleep while playing sound
        proc = subprocess.Popen(['mpg321', 'beep.mp3'], shell=False)
        time.sleep( wait_time - (current_signal * multiplier) )

        proc.terminate()
        proc.wait()
