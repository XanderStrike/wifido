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

current_signal = -0.1
multiplier = 4
wait_time = 5
tweet_frequency = 87 # seconds

whitelist = ["Westmont_Encrypted", "Westmont_Open", ""]
#rogue_networks = {}
last_tweeted = datetime.now()
last_rogue_essid = ""

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
            match = re.match(r"(\d+)/(\d+)", data[data.keys()[i]]["Signal"])
            strength_1 = float(match.group(1))
            strength_2 = float(match.group(2))
            current_essid = data[data.keys()[i]]["ESSID"]

            print str(strength_1) + " / " + str(strength_2) + " = " + str(strength_1 / strength_2) + " for " + current_essid
            if ((strength_1 / strength_2) > current_signal) and current_essid == "Westmont_Encrypted":
                current_signal = strength_1 / strength_2

            # tweet here
            tweet = "Bark! at " + current_essid + " on  " + datetime.now().strftime("%Y-%m-%d %H:%M and %S seconds")

            if (current_essid not in whitelist):

                # if current_essid not in rogue_networks.keys():
                #     rogue_networks[current_essid] = datetime.now()

                # rogue_ready = (datetime.now() - rogue_networks[current_essid]).total_seconds() >= tweet_frequency

                global_ready = (datetime.now() - last_tweeted).total_seconds() >= tweet_frequency

                # print "GLOBAL: " + str(global_ready) + " ROGUE: " + str(rogue_ready)

                if (global_ready and last_rogue_essid != current_essid):
                    Tweet.update_status(tweet, json_data["app_key"], json_data["app_secret"], json_data["oauth_token"], json_data["oauth_token_secret"])

                    last_tweeted = datetime.now()

                    #rogue_networks[current_essid] = datetime.now()

                    last_rogue_essid = current_essid


        # GPIO here

        GPIO.output(11, False)
        time.sleep(.1)
        GPIO.output(11, True)

        # print "Best Signal: " + str(current_signal)
        # print "UP"
        proc = subprocess.Popen(['mpg321', 'beep.mp3'], shell=False)
        time.sleep( wait_time - (current_signal * multiplier) )

        proc.terminate()
        # print "DOWN"
        proc.wait()
