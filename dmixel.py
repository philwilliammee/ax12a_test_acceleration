#!/usr/bin/python2.7
'''
Created on Nov 4, 2013

@author: philwilliammee

to test seria port
dmesg | grep tty

sudo chmod a+rw /dev/"ttyUSB1"

'''
from Ports import *
import serial                  # we need to import the pySerial stuff to use
import threading
#from matplotlib import pyplot as plt
import time
import math

PING = 1 #used to obtain a status packet
READ_DATA = 2
WRITE_DATA = 3
REG_WRITE = 4
ACTION = 5
RESET = 6
SYNC_WRITE = 0x83

threadLock = threading.Lock()
ys = list()
xs = list()
        
class Transmit_Thread(threading.Thread):
    def __init__(self, threadID, axID, Pdata, Sdata, sample):
        threading.Thread.__init__(self)
        print "starting transmit thread"
        self.event = threading.Event()
        self.P = Pdata
        self.S = Sdata
        self.sample = sample
        self.axID = axID

    def run(self):
        global threadLock
        sample = self.sample
        
        Ptail = self.P[-1]
        Stail = self.S[-1]
        mrange = int(sample*20)
        for _ in xrange(0,mrange,1):
            self.P.append(Ptail)
            self.S.append(Stail)
        for (p,s) in zip(self.P, self.S):
            self.event.wait(sample)  #this actually takes about .250
            threadLock.acquire
            try:
                self.error = setReg(self.axID ,30,((p%256),(p>>8),(s%256),(s>>8)))
            finally:
                threadLock.release 
                
        print "ending transmit thread"
        
            
class Recieve_Thread(threading.Thread):
    def __init__(self, threadID, axID, obj):
        threading.Thread.__init__(self)
        print "starting recieve thread"
        self.threadID = threadID
        self.event = threading.Event()
        self.count = 0
        self.error = 0
        self.tran_error = 0
        self.run_time = 0
        self.thread1 = obj
        self.axID = axID

    def run(self):
        global xs
        global ys
        global threadLock

        while self.thread1.isAlive():

            self.event.wait(self.run_time)
            start_time = time.time()  
                    
            threadLock.acquire()
            data = getReg(self.axID ,36,5)    
            threadLock.release() 
                      
            if len(data) > 1:
                myData = data[0] + (data[1]<<8)
                if myData < 1024 and myData > 0:
                    self.count += 1
                    ys.append(myData) 
                    xs.append(self.count) 
            else:
                self.tran_error += 1  
            #self.myFrame.real_time_plot()#this takes .03s
            self.run_time = 0.1- math.ceil((time.time() - start_time)*1000.0) / 1000.0 #3 decimals usually .003s
            #print self.run_time
        if self.tran_error:
            print "data received ", self.tran_error, " errors" 
        print "receive thread is closing" 

class dmixel():
    def __init__(self, sample=0.25, AX12_ID=1 ):
        P, S = read_text_data()         
        threads = []
        sample = (sample - .0003)
        # Create new threads
        self.thread1 = Transmit_Thread(1, AX12_ID, P, S, sample)
        self.thread2 = Recieve_Thread(2, AX12_ID, self.thread1)

        # Start new Threads
        self.thread1.start()
        self.thread2.start()

        # Add threads to thread list
        threads.append(self.thread1)
        threads.append(self.thread2)
        
        # Wait for all threads to complete
        #for t in threads:
            #t.join()
        #print "Exiting Main Thread"
        
    def __del__(self):
        class_name = self.__class__.__name__
        print class_name, "destroyed"
      
def read_text_data():
    P = S = []
    fname = 'test.txt'
    with open(fname) as f:#with closes file
        for (j,line) in enumerate(f):
            line = line.split() # to deal with blank 
            if line:            # lines (ie skip them)
                line = [int(i) for i in line]
            if j ==0:
                P = line
            elif j ==1:
                S = line
    return P, S
  
# set register values
def setReg(ID, reg, values):
    global s
    global WRITE_DATA
    length = 3 + len(values)
    checksum = 255-((ID+length+WRITE_DATA+reg+sum(values))%256)          
    s.write(chr(0xFF)+chr(0xFF)+chr(ID)+chr(length)+chr(WRITE_DATA)+chr(reg))
    for val in values:
        s.write(chr(val))
    s.write(chr(checksum))

def getReg(ID, regstart, rlength):
    global s
    global READ_DATA
    vals = list() 
    s.flushInput() 
    checksum = 255 - (( 6 + ID + regstart + rlength)%256)
    s.write(chr(0xFF)+chr(0xFF)+chr(ID)+chr(0x04)+chr(READ_DATA)+
            chr(regstart)+chr(rlength)+chr(checksum))
    s.read()   # 0xff
    s.read()   # 0xff
    s.read()   # ID
    length = ord(s.read()) - 1
    s.read()   #error length will be 1 catch in data thread
    while length > 0:
        vals.append(ord(s.read()))
        length = length - 1
    
    return vals

def read_control_table():
    control_table = {}
    with open('Control_table.txt', 'r') as f:
        for line in f:
            splitLine = line.split()
            control_table[int(splitLine[0])] = ",".join(splitLine[1:])
    return control_table

def print_control_table(axID = 1):
    control_table = {}
    with open('Control_table.txt', 'r') as f:
        for line in f:
            splitLine = line.split()
            control_table[int(splitLine[0])] = ",".join(splitLine[1:])
            
    for key, value in control_table.iteritems():
        print key , " " , value, " : ", getReg(axID ,key,1)

#mymixel = dmixel()
