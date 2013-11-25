'''
Created on Nov 6, 2013

@author: philwilliammee
'''

import numpy as np
import math

class function_generator():
    def __init__(self, PERIOD=10, AMPLITUDE=510, DELTA_T=.25, function='sine'):
        self.function_dic = {"sine":self.sine, "triangle":self.triangle, 
                             "sawtooth":self.sawtooth, "step":self.step, 
                             "ramp":self.ramp}
        self.T = PERIOD
        self.a = AMPLITUDE
        self.dt = DELTA_T     
        self.y = list()
        self.x = np.arange(0.00,(self.T + self.dt),self.dt)
        self.OFFSET = 512
        self.myfunct = function 
        self.speed_coef = 0.47776
        self.generate() #do it
        self.save_data("test.txt")   
                  
    def generate(self):
        for val in self.x:
            self.y.append(self.function_dic[self.myfunct](val))
                    
    def sine(self,val):
        omega = 2*math.pi*1/self.T
        return self.a*math.sin(omega*val)+self.OFFSET
         
    def triangle(self,val):
        return (2*self.a/math.pi)*math.asin(math.sin((2*math.pi/self.T)*val))+self.OFFSET
        
    def sawtooth(self,val):
        adjustT = self.T*.6667
        try:
            return (-2*self.a/math.pi)*math.atan(1/math.tan((math.pi/adjustT)*val))+self.OFFSET
        except ZeroDivisionError as detail:
            print 'Handling run-time error:', detail
        return self.OFFSET
    
    def step(self,val):
        changeStep = (self.dt, (self.T/2)-(self.dt), (self.T/2), self.T-self.dt )
        sequence = (0, 3, 1, 2)
        mySum = self.OFFSET
        HEAVISIDE = np.where
        for (ii, time) in enumerate(changeStep):
            if (ii == sequence[0]) or (ii == sequence[1]):
                mySum += (HEAVISIDE((val)>time, self.a, 0))
            elif (ii==sequence[2]) or (ii == sequence[3]):
                mySum -= (HEAVISIDE((val)>time, self.a, 0))
        return mySum
    
    def ramp(self,val):
        x = np.arange(0, 10+self.dt, 2*self.dt)
        mySum = self.OFFSET
        DC = 0
        HEAVISIDE = np.where
        for (ii, time) in enumerate(x):
            if (ii < 4) or (ii > 15) and (ii < 20):
                mySum += (HEAVISIDE((val)>time, self.a/4, DC))
            elif (ii > 5) and (ii < 14):
                mySum -= (HEAVISIDE((val)>time, self.a/4, DC))
        return mySum
    
    def getxy(self):
        return (self.x, self.y)
    
    def save_data(self, fname):
        oldy = 432
        slope = list()
        outf = open(fname,'w')#clear the file
        outf.close
        outf = open(fname,'ab')
        for y in self.y:
            myslope = abs(self.speed_coef*((y-oldy)/self.dt))
            if myslope > 1023:
                print ("ERROR: required speed can not be reached try reducing dt or amplitude")
                myslope = 1023
            slope.append(myslope)
            oldy = y
            outf.write(str(int(round(y)))+" ")
        outf.write("\n")
        for s in slope:
            outf.write(str(int(round(s)))+" ")
        outf.write("\n")
        outf.close

def test():
    from matplotlib import pyplot as plt
    period = 10 #seconds
    amplitude = 510
    sampleRate = .25 #seconds  
    func_list = ("sine", "triangle","sawtooth", "step", "ramp")

    for fun in func_list:
        fg = function_generator(period, amplitude, sampleRate, fun) 
        x,y = fg.getxy()
        plt.plot(x,y)

    plt.show()     

#test()
