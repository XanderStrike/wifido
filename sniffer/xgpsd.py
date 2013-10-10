import bluetooth
import time
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
        sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        port = 1
        sock.connect((target_address,port))
        return true
    except:
        return false
    



def start_listening():
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
        start_listening
    get_fix
