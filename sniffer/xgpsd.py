import bluetooth
import time
# import threading

def pair:

def start_listening:

def get_fix:


if __name__ == '__main__':

    # what we know about the bluetooth device
    target_name = 'XGPS150-365060'
    target_address = "00:19:01:36:50:60"
    print "Searching for device..."
    # if there is not a address given it will search for one.
    while target_address == None:
        near_devices = bluetooth.discover_devices()
        for near_address in near_devices:
            if target_name == bluetooth.lookup_name( near_address ):
                target_address = near_address
                break

    print "Discovered!", target_address

    sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    port = 1
    sock.connect((target_address,port))
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
                    if line_values[0] = '$GPRMC':
                        gps['lat']: line_values[3] + line_values[4]
                        gps['long']: line_values[5] + line_values[5]
                    print line # put in hash here...
                    old_data = ""
                else:
                    olddata = line
