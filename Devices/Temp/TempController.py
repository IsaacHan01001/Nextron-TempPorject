from TempUtility.Utils import *
import time
import serial
import minimalmodbus
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union
import asyncio

class GenericTempDevice(ABC):
    
    __author__ = "Isaac Han"
    __email__ = "cogitoergosum01001@gmail.com"
    __citation__ ="Numat's Alicat Driver created by Alex Ruddick and Jonas Berg's minimal modbus"

    def __init__(self, timeout: float): #One Example showing data type to the maintainer.
        '''
        Taken from Numant's ALicat Driver by Alex Ruddick and modified its usage
        '''

        self.open = False
        self.timeout = timeout
        self.timeouts = 0
        self.max_timeouts = 10
        # self.lock = asyncio.Lock() #lock is not implemented. Need to study its documentation
        self.logger = None

        self.instrument = None
        self.temperature = self.setTempfields()

    def setTempfields(self):
        rootFields = ["Temperature", "PID"]
        temperatureFields = ["CurrentTemp", "SetTemp", "RampingTemp", "HotPower", "CoolPower"]
        PIDFields = ["P_hot", "I_hot", "D_hot", "P_Cool", "I_Cool", "D_Cool"]
        subFields = [temperatureFields, PIDFields]

        ans = dict().fromkeys(rootFields, None)
        for subInd, field in enumerate(rootFields):
            ans[field] = dict().fromkeys(subFields[subInd], 0)
        return ans

    @abstractmethod
    def _setLogger(self):
        pass

    @abstractmethod
    def _connect(self):
        '''
        Connect to Device through MinimalModbus
        :return:
        '''
        pass

    @abstractmethod
    def _isInstrument(self):
        '''
        Check whether the connected device is a correct device
        :return:
        '''
        pass

    @abstractmethod
    def setInstrument(self):
        pass

    @abstractmethod
    def setRampingRateUpper(self, aFloat: float):
        pass

    @abstractmethod
    def setRampingRateLower(self, aFloat: float):
        pass

    @abstractmethod
    def getTemperature(self):
        pass

    @abstractmethod
    def setRunOrStop(self, aInt: int):
        pass

    @abstractmethod
    def setTemperature(self, aFloat: float):
        pass

    #Composite Utility ##########
    def setSingleRampingRate(self, aFloat):
        assert isinstance(aFloat, float), f"Invalid input num {aFloat} at setSingleRamping Rate"
        self.setRampingRateUpper(aFloat)
        self.setRampingRateLower(aFloat)

    def stopDevice(self):
        '''
        Gives about 10 seconds to use its internal cooling engine to cool down below 100 degree celsius
        Regardless of Fahrenheit or Celsius, it checks whether the magnitude is lower than 100 or not.
        Using
        '''

        counter = 0
        while counter < 10:
            counter += 1
            time.sleep(0.5)
            if self.getTemperature() < 100:
                self.setRunOrStop(1)
                return
            else:
                self.setSingleRampingRate(50)
                self.setSetValue(90)
                self.setRunOrStop(0) #keep running until cooled off
                time.sleep(0.5)
        self.setRunOrStop(1) #turned off after about 10 seconds no matter what

        #looping over 5 times to ensure the device is stopped. If the device is not stopped,
        # the program will porint Unsuccessful message in the console
        for i in range(5):
            time.sleep(0.1)
            if self.getRunOrStop() == 1:
                return

            self.setRunOrStop(1)

        logging.error(f"{1111}")
        return

    def updateFieldsInfo(self):
        '''
        Generic Method for updating Temperature fields
        :return:
        '''
        self.temperature["Temperature"]["CurrentTemp"] = self.getTemperature()
        self.temperature["Temperature"]["SetTemp"] = self.getSetValue()
        self.temperature["Temperature"]["RampingTemp"] = self.getRampingRateLower() # assumes lower ramping == upper
        # self.temperature["Temperature"]["HotPower"] = self.getHeatingManipulatedOutputValue()
        # self.temperature["Temperature"]["HotPower"] = self.getCoolingManipulatedOutputValue()

        PID_hot = self.getHeatingPID()
        self.temperature["PID"]["P_hot"] = PID_hot[0]
        self.temperature["PID"]["I_hot"] = PID_hot[1]
        self.temperature["PID"]["D_hot"] = PID_hot[2]

        PID_cool = self.getCoolingPID()
        self.temperature["PID"]["P_cool"] = PID_cool[0]
        self.temperature["PID"]["I_cool"] = PID_cool[1]
        self.temperature["PID"]["D_cool"] = PID_cool[2]
