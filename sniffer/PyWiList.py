from IWList import *
from subprocess import Popen, PIPE, STDOUT
from datetime import date, datetime, timedelta
import sys, os, logging, time, subprocess, thread
import RPi.GPIO as GPIO
import Tweet
import json
from pprint import pprint

logging.basicConfig()
log = logging.getLogger("PyWiList")
log.setLevel(logging.DEBUG)

current_signal = -0.1
multiplier = 4
wait_time = 5
last_tweeted = datetime.now()
tweet_frequency = 30 # seconds

whitelist = ["Westmont_Encrypted", "Westmont_Open", ""]

if __name__ == "__main__":

    json_file = open('auth.json')
    json_data = json.load(json_file)
    json_file.close()

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)

    while True:

        iwl = IWList("wlan0")
        data = iwl.getData()
        
        for i in range(0, len(data.keys())):

            strength_1 = float(data[data.keys()[i]]["Signal"][0:data[data.keys()[i]]["Signal"].index("/")])
            strength_2 = float(data[data.keys()[i]]["Signal"][3:6])
            current_essid = data[data.keys()[i]]["ESSID"]
            
            print str(strength_1) + " / " + str(strength_2) + " = " + str(strength_1 / strength_2) + " for " + current_essid
            if ((strength_1 / strength_2) > current_signal) and current_essid == "Westmont_Encrypted":
                current_signal = strength_1 / strength_2

            # tweet here
            tdelta = datetime.now() - last_tweeted
            if (tdelta.total_seconds() >= tweet_frequency and current_essid not in whitelist):
                tweet = "Bark! " + current_essid
                Tweet.update_status(tweet, json_data["app_key"], json_data["app_secret"], json_data["oauth_token"], json_data["oauth_token_secret"])
                last_tweeted = datetime.now()
                whitelist.append(current_essid)


        # GPIO here

        GPIO.output(11, False)
        time.sleep(.1)
        GPIO.output(11, True)

        print "Best Signal: " + str(current_signal)
        print "UP"
        proc = subprocess.Popen(['mpg321', 'beep.mp3'], shell=False)
        time.sleep( wait_time - (current_signal * multiplier) )

        proc.terminate()
        print "DOWN"
        proc.wait() 
