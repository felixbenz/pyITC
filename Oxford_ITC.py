# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 13:13:27 2015

@author: Felix Benz (fb400)
"""

import visa

class OxfordITC():
    def __init__(self):
        self.comport = str('COM3')
        self.address = str('0000006')
        self.visa_address = str('ASRL3::INSTR')
    
    def open_connection(self):
        rm = visa.ResourceManager()
        self.device = rm.open_resource(self.visa_address, baud_rate=9600, read_termination='\r', timeout=1000)
        self.device.write_termination = '\r'
        self.write("+a:" + str(self.address))
        self.setControlMode(3)
    
    def clear(self):
        self.device.read()

    def write(self,msg):
        self.device.write(msg)
        self.clear()
        
    def getTemperature(self):
        temp = self.device.query('R1')
        temp = float(temp[1:len(temp)]) # Remove the first character ('R')
        
        return temp
    
    def setControlMode(self,mode):
        """
        Sets the operation mode (local or remote)
        0 LOCAL & LOCKED (Default State)
        1 REMOTE & LOCKED (Front Panel Disabled)
        2 LOCAL & UNLOCKED
        3 REMOTE & UNLOCKED (Front Panel Active)
        """
        if (mode not in [0,1,2,3]):
            raise Exception('valid modes are 0-3, see documentation')
        self.write('C'+str(mode))
   
    def readSetTemperature(self):
        temp = self.device.query('R0')
        temp = float(temp[1:len(temp)]) # Remove the first character ('R')
        return temp
    
    def setHeaterMode(self,mode):
        """
        Sets the heater mode (auto, manual)
        0 HEATER MANUAL, GAS MANUAL
        1 HEATER AUTO, GAS MANUAL
        2 HEATER MANUAL, GAS AUTO
        3 HEATER AUTO, GAS AUTO
        """
        if (mode not in [0,1,2,3]):
            raise Exception('valid modes are 0-3, see documentation')
        self.write('A'+str(mode))
        
    def setSetTemperature(self,temp):
        """
        Sets the set temperature (requires and integer in Kelvin)
        """
        self.write('T'+str(int(temp)))
    
    def setHeaterPower(self,power):
        self.write('O'+str(int(power)))
    
    def heaterOff(self):
        self.setHeaterMode(0)
        self.setHeaterPower(0)
        
    def setAutoPID(self,mode):
        """
        Sets the PID mode (auto or manual)
        0 DISABLES USE OF AUTO-PID
        1 USES AUTO-PID
        """
        if (mode not in [0,1]):
            raise Exception('valid modes are 0 (off) or 1 (on)')
        self.write('L'+str(mode))
        
    def setPID(self,P,I,D):
        """
        Sets the PID parameters for manual PID control
        P: PROPORTIONAL BAND in Kelvin (resolution 0.001K, ideally 5 to 50K)
        I: INTEGRAL ACTION TIME in minutes (0 to 140, ideally 1 to 10)
        D: DERIVATIVE ACTION TIME in minutes (0 to 273, can be left at 0)
        """
        self.write('P'+str(P))
        self.write('I'+str(I))
        self.write('D'+str(D))
    
    def close_connection(self):
        self.heaterOff()
        self.setControlMode(0)
        self.device.close()
        
if __name__=='__main__':
    ITC = OxfordITC()
    print ITC.getTemperature()