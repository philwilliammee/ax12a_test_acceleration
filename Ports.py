'''
Created on Nov 18, 2013

@author: philwilliammee
make sure user is a member of dialout
sudo usermod -a -G tty yourUserName
sudo usermod -a -G dialout username
Log off and log on again for the changes to take effect! 
'''
import serial
import os
import stat
import getpass

s = serial.Serial()               # create a serial port object
BAUDRATE = 1000000

class Port():
    def __init__(self):
        global s
        open_port()
  
def findPorts():
    """ return a list of serial ports """
    ports = list()
    # windows first
    for i in range(20):
        try:
            sp = serial.Serial("COM"+str(i))
            sp.close()
            ports.append("COM"+str(i))
        except:
            pass
    if len(ports) > 0:
        return ports
    # mac specific next:        
    try:
        for port in os.listdir("/dev/"):
            if port.startswith("tty.usbserial"):
                ports.append("/dev/"+port)
    except:
        pass
    # linux/some-macs
    for k in ["/dev/ttyUSB","/dev/ttyACM","/dev/ttyS"]:
            for i in range(6):
                try:
                    sp = serial.Serial(k+str(i))
                    sp.close()
                    ports.append(k+str(i))
                except:
                    pass
    return ports
    
def open_port():
    global s
    global BAUDRATE
    s.baudrate = BAUDRATE             # baud rate, in bits/second
    p = findPorts()
    s.port = p[0]
    s.open()
    if (s.isOpen() == False):
        print "error could not open", s
    else:
        print "port open at ", s.port
    
def is_writable(filepath):
    st = os.stat(filepath)
    return bool(st.st_mode & stat.S_IWUSR)

def test_ports():
    global s
    p = findPorts()
    print p
    open_port()
    if (s.isOpen() == False):
        print "error could not open", s
    else:
        print"port ", s, " opened success"
        
myport = Port()   
