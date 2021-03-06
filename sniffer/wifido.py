from IWList import *
import xgpsd
from subprocess import Popen, PIPE, STDOUT
import sys, os, logging, time, subprocess, thread, re
#import RPi.GPIO as GPIO
import Tweet
import json
import sqlite3 as lite
from datetime import datetime
from pprint import pprint

logging.basicConfig()
log = logging.getLogger("wifido")
log.setLevel(logging.DEBUG)

interface = "eth1"  # Use a second wireless device

last_upload_day = -1

 # How long to wait for a given signal strength (between 0 and 1)
def wait_time (signal):
    return 5 - 4*signal

if __name__ == "__main__":
  try:
    print '[' + str(datetime.now()) + ']'

    os.system("ifdown " + interface)
    #os.system("amixer cset numid=3 1")

    con = lite.connect('db/db.sqlite3')

    json_file = open('auth.json')
    json_data = json.load(json_file)
    json_file.close()

    #GPIO.setmode(GPIO.BOARD)
    #GPIO.setup(11, GPIO.OUT)

    xgpsd.start_listening()

    last_coords = [0,0]

    while True:
        # Get GPS data
        gpsdata = xgpsd.get_data()

    # this is a rough estimate of distance, Manhattan: not Cartesian 
        distance_moved = (abs(gpsdata["lat"] - last_coords[0]) + abs(gpsdata["lon"] - last_coords[1]))

        strongest_signal = 0
        if distance_moved > .00005:
            # Set last gps coords
            last_coords = [gpsdata["lat"], gpsdata["lon"]]

            # Process WiFi data
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
                          str(time.time()),
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
        elif datetime.now().hour == 22 and last_upload_day != datetime.now().day: # if stationary, upload at 10 pm each day
            last_upload_day = datetime.now().day
            os.system("ifup " + interface)
            loop_count = 0
            while loop_count < 10 and not re.search("inet addr:\d+\.\d+\.\d+\.\d+", os.popen("ifconfig " + interface)):
                time.sleep(5)
                loop_count += 1
            os.system("scp db/db.sqlite3 librarycounter.westmont.edu:wifido/server/db/data.sqlite3")
            Tweet.commit()
            os.system("ifdown " + interface)

        # Blink LED
        #GPIO.output(11, False)
        #time.sleep(.1)
        #GPIO.output(11, True)

        # Sleep while playing sound
        # TODO: figure out if/why this is breaking?
        #proc = subprocess.Popen(['mpg321', '-q', 'beep.mp3'], shell=False)
        time.sleep(wait_time(strongest_signal))
        #proc.terminate()
        #proc.wait()
  except:
    raise
  finally:
    os.system('ifup ' + interface)
