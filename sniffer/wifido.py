from IWList import *
from subprocess import Popen, PIPE, STDOUT
from datetime import date, datetime, timedelta
import sys, os, logging, time, subprocess, thread, re
import RPi.GPIO as GPIO
import Tweet
import json
from pprint import pprint

logging.basicConfig()
log = logging.getLogger("PyWiList")
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

        iwl = IWList(interface)
        data = iwl.getData()

        for cell in data.values():

            match = re.match(r"(\r+)/(\r+)", cell["Signal"])
            strength_1 = float(match.group(1))
            strength_2 = float(match.group(2))
            current_essid = cell["ESSID"]

            print str(strength_1) + " / " + str(strength_2) + " = " + str(strength_1 / strength_2) + " for " + current_essid
            if ((strength_1 / strength_2) > current_signal) and current_essid == "Westmont_Encrypted":
                current_signal = strength_1 / strength_2

            Tweet.bark(current_essid, json_data)

        # Blink LED
        GPIO.output(11, False)
        time.sleep(.1)
        GPIO.output(11, True)

        # Sleep while playing sound
        proc = subprocess.Popen(['mpg321', 'beep.mp3'], shell=False)
        time.sleep( wait_time - (current_signal * multiplier) )

        proc.terminate()
        proc.wait()
