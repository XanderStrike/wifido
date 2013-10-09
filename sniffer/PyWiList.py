from IWList import *
from subprocess import Popen, PIPE, STDOUT
import sys, os, logging, time, subprocess

logging.basicConfig()
log = logging.getLogger("PyWiList")
log.setLevel(logging.DEBUG)

if __name__  ==  '__main__':

    multiplier = 4
    wait_time = 3
    while True:
        iwl = IWList("wlan0")
        data = iwl.getData()
        current_signal = -0.1
        

        for i in range(0, len(data.keys())):

            strength_1 = float(data[data.keys()[i]]["Signal"][0:data[data.keys()[i]]["Signal"].index("/")])
            strength_2 = float(data[data.keys()[i]]["Signal"][3:6])

            print "Signal strengths"
            print strength_1
            print strength_2
            print str(strength_1) + " / " + str(strength_2) + " = " + str(strength_1 / strength_2) + " for " + data[data.keys()[i]]["ESSID"]
            if ((strength_1 / strength_2) > current_signal) and data[data.keys()[i]]["ESSID"] == "Westmont_Encrypted":
                current_signal = strength_1 / strength_2
        
        # make GPIO calls here
        print "Best Signal: " + str(current_signal)
        proc = subprocess.Popen(['mpg321', 'beep.mp3'], shell=False)
        time.sleep( wait_time -  multiplier * current_signal)
        proc.terminate()
        #proc.wait()
