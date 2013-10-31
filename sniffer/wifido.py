from IWList import *
from subprocess import Popen, PIPE, STDOUT
import sys, os, logging, time, subprocess, thread, re
import RPi.GPIO as GPIO
import Tweet
import json
from pprint import pprint

logging.basicConfig()
log = logging.getLogger("wifido")
log.setLevel(logging.DEBUG)

interface = "wlan1"  # Use a second wireless device

 # How long to wait for a given signal strength (between 0 and 1)
def wait_time (signal):
    return 5 - 4*signal


if __name__ == "__main__":

    json_file = open('auth.json')
    json_data = json.load(json_file)
    json_file.close()

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)

    while True:
        # TODO Get GPS data
        # store in a temp var
        # gpsdata = {time: 12341234, alt: 432, lat: 431423.23, lon: -3232.22}

        # Process WiFi data
        strongest_signal = 0
        for cell in IWList(interface).getData().values():

            match = re.match(r"(\d+)/(\d+)", cell["Signal"])
            strength_nu = match.group(1)
            strength_de = match.group(2)
            strength = float(strength_nu) / float(strength_de)
            essid = cell["ESSID"]

            # Keep track of the strength of our primary network.
            if essid == "Westmont_Encrypted" and strength > strongest_signal:
                strongest_signal = strength

            Tweet.bark(essid, json_data)

            # TODO write to db

        print "Current signal strength: " + str(strength)

        # Blink LED
        GPIO.output(11, False)
        time.sleep(.1)
        GPIO.output(11, True)

        # Sleep while playing sound
        proc = subprocess.Popen(['mpg321', '-q', 'beep.mp3'], shell=False)
        time.sleep(wait_time(strongest_signal))
        proc.terminate()
        proc.wait()
