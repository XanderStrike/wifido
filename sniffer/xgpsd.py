# Adam Hess 2013
# gpsdx: listens to a gps unit and reports the result.

import os
from gps import *
from time import *
import time
import threading

gpsd = None

class Listener(threading.Thread):
  def __init__(self):
    # make a thread
    threading.Thread.__init__(self)
    # start the gps listening
    global gpsd
    gpsd = gps(mode=WATCH_ENABLE)
    self.current_value = None
    self.running = True

  def run(self):
    # keep getting the newest data
    global gpsd
    while self.running: # thread prevents it from hanging.
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

def start_listening():
    # start listening
    gpsd = Listener()
    try:
        gpsd.start()
        print "Now Listening..."
    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
        print "\nKilling Thread..."
        gpsd.running = False
        gpsd.join()
    print "Done.\nExiting."


def get_data():
    # hash of common gps data
    print "hey hey hey"
    print gpsd.fix.latitude
    return {
        'lat': gpsd.fix.latitude,
        'lon': gpsd.fix.longitude,
        'alt': gpsd.fix.altitude,
        'speed': gpsd.fix.speed, # m/s
        'sats': gpsd.satellites,
        'utc': gpsd.utc,
        'time': gpsd.fix.time
    }


def stop_listening():
    gpsd.running = False
    gpsd.join()
    print "Done"

if __name__ == '__main__':
    start_listening()
    while True:
        time.sleep(5) #set to whatever
        print get_data()
