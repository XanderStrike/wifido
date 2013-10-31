# Adam Hess 2013
# gpsdx: listens to a gps unit and reports the result.

import os
from gps import *
from time import *
import time
import threading
<<<<<<< HEAD

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
=======
# import threading

sock = None
gps = {'lat': None, 'long':None}

def pair(target_address=None, target_name=None):
    # if there is not a address given it will search for one.
    while target_address == None:
        near_devices = bluetooth.discover_devices()
        for near_address in near_devices:
            if target_name == bluetooth.lookup_name( near_address ):
                target_address = near_address
                # print "Discovered!", target_address
                break
    try:
        global sock
        sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        port = 1
        sock.connect((target_address,port))
        return True
    except:
        return False



class ThreadListen(threading.Thread):
    def run(self):
     data = ""
     old_data = ""
     while True: # make thread...
         time.sleep(1)
         data = sock.recv(1024)
         if len(data) > 0:
             data = old_data + data
             lines = data.splitlines(1)
             for line in lines:
                 if line.find("\r\n") != -1:
                     line = line.strip()
                     line_values = line.split(',')
                     if line_values[0] == '$GPRMC':
                         global gps
                         gps['lat'] = line_values[3] + line_values[4]
                         gps['long'] = line_values[5] + line_values[5]
                     print line # put in hash here...
                     old_data = ""
                 else:
                     olddata = line

def get_fix():
    return gps

if __name__ == '__main__':
    if pair('00:19:01:36:50:60'):
        listener = ThreadListen()
        listener.start()
    while True:
        time.sleep(2)
        print get_fix()
>>>>>>> 02554f2f4fea2c129de8144696617e88fd830a8b
