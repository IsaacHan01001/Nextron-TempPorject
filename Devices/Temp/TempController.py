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

        self.temperature = dict().fromkeys(rootFields, None)
        for subInd, field in enumerate(rootFields):
            self.temperature[field] = dict().fromkeys(subFields[subInd], 0)

    @abstractmethod
    def setLogger(self):
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

    def setInstrument(self):
        ports, deviceInfo = all_ports()







    def makeInstrument(self):
        '''
        creating minimalmodbus.instrument instance when received a valid port and channel
        :return:
        '''
        try:
            if self.port and self.channel:
                self.instrument = minimalmodbus.Instrument(self.port["Device"], self.channel)
                self.instrument.serial.baudrate = 9600 #we set baudrate as we used 9600 It might cause error you change
            else:
                print(f"Insufficient args: port: {self.port} channel: {self.channel}")
            return
        except:
            import traceback
            traceback.print_exc()
            raise Exception(f"Connection failure from class FB100 with port {self.port} channel {self.channel}")

    def makeTempfields(self):
        rootFields = ["Temperature", "PID"]
        temperatureFields = ["CurrentTemp", "SetTemp", "RampingTemp", "HotPower", "CoolPower"]
        PIDFields = ["P_hot", "I_hot", "D_hot", "P_Cool", "I_Cool", "D_Cool"]
        subFields = [temperatureFields, PIDFields]

        self.temperature = dict().fromkeys(rootFields, None)
        for subInd, field in enumerate(rootFields):
            self.temperature[field] = dict().fromkeys(subFields[subInd], 0)

    #getting initial configuration##############################################
    def getTempDecimalSetting(self):
        '''
        0: Interger
        1: One decimal place
        2: Two decimal place
        '''
        return self.instrument.read_register(84, 0)

    def getTemperatureUnit(self):
        '''
        0 is for Celsius \u00B0CC
        1 is for Farenheit \u00B0CF
        '''
        return self.instrument.read_register(83, 0)
    # setting configuration#################################################

    def setTempUnit(self, aInt):
        assert isinstance(aInt, int), "Invalid data type for setTempUnit. It expects an integer"
        if 0 <= aInt <= 2:
            self.instrument.write_register(83, aInt) # for degree C
        else:
            raise Exception(f"Error with setting TempUnit Unknown command {aInt}")

    def setTemperatureDecimal(self, aInt):
        assert isinstance(aInt, int), "Invalid data type for setTemperatureUnit. It expects an integer"
        if 0 <= aInt <= 2:
            self.instrument.write_register(84, aInt)
        else:
            raise Exception(f"setTemperatureUnit Expects 0 or 1, not {aInt}")

    # get Process values ##################################
    def getTemperature(self):
        return self.instrument.read_register(0, self.getTempDecimalSetting())

    def getSetValueMonitor(self):
        return self.instrument.read_register(3, self.getTempDecimalSetting())

    def getHeatSideMVI(self):
        return self.instrument.read_register(13, 1)

    def getCoolSideMV1(self):
        return self.instrument.read_register(14, 1)

    def getHeatingPID(self):
        '''
        Unit is important: Call self.getTempUnit
        There is also 1/10th setting in derivative time unit
        '''
        P_heat = self.instrument.read_register(45, self.getTempDecimalSetting())
        I_heat = self.instrument.read_register(46, self.getTempDecimalSetting())
        D_heat = self.instrument.read_register(47, self.getTempDecimalSetting())
        return (P_heat, I_heat, D_heat)

    def getCoolingPID(self):
        '''
        Unit is important:
        :return:
        '''
        P_cool = self.instrument.read_register(49, self.getTempDecimalSetting())
        I_cool = self.instrument.read_register(50, self.getTempDecimalSetting())
        D_cool = self.instrument.read_register(51, self.getTempDecimalSetting())
        return (P_cool, I_cool, D_cool)

    def getRampingRateLower(self):
        '''
        There are two ramping rate limiter one is down and the other is up
        :return: (lower limit, upper limit)
        '''
        return self.instrument.read_register(55, self.getTempDecimalSetting())

    def getRampingRateUpper(self):
        '''
        There are two ramping rate limiter one is down and the other is up
        :return: (lower limit, upper limit)
        '''
        return self.instrument.read_register(54, self.getTempDecimalSetting())

    def getSetValue(self):
        '''
        This gets the set temperature value
        :return:
        '''
        return self.instrument.read_register(44)

    def getHeatingManipulatedOutputValue(self):
        '''
        AKA heat power
        RKC: O1
        Modbus: 13
        :return:
        '''
        return self.instrument.read_register(13)

    def getCoolingManipulatedOutputValue(self):
        '''
        AKA cool power
        RKC O2
        Modbus: 14
        :return:
        '''
        return self.instrument.read_register(14)

    # set process values#########################################

    def setHeatingPID(self, P = None, I = None, D = None): #d
        if P is not None:
            assert isinstance(P, int), f"Invalid P value with {P}"
            self.write_register(45, P)
        if I is not None:
            assert isinstance(I, int), f"Invalid I value with {I}"
            self.write_register(46, I)
        if D is not None:
            assert isinstance(D, int), f"Invalid D value with {D}"
            self.write_register(47, D)

    def setCoolingPID(self, P=None, I=None, D=None):
        if P is not None:
            assert isinstance(P, int), f"Invalid P value with {P}"
            self.instrument.write_register(45, P)
        if I is not None:
            assert isinstance(I, int), f"Invalid P value with {I}"
            self.instrument.write_register(46, I)
        if D is not None:
            assert isinstance(D, int), f"Invalid D value with {D}"
            self.instrument.write_register(47, D)

    def setRampingRateLower(self, aFloat):
        assert isinstance(aFloat, float) or isinstance(aFloat, int), f"Problem with float: {aFloat} in setRampingRateLower"
        '''
        There are two ramping rate limiter one is down and the other is up
        :return: (lower limit, upper limit)
        '''
        return self.instrument.write_register(55, aFloat, self.getTempDecimalSetting())

    def setRampingRateUpper(self, aFloat):
        assert isinstance(aFloat, float) or isinstance(aFloat, int), f"Problem with float: {aFloat} in setRampingRateHigher"
        '''
        There are two ramping rate limiter one is down and the other is up
        :return: (lower limit, upper limit)
        '''
        return self.instrument.write_register(54, aFloat, self.getTempDecimalSetting())

    def setSetValue(self, aFloat):
        '''
        This sets the set temperature
        :param aFloat:
        :return:
        '''
        assert isinstance(aFloat, float) or isinstance(aFloat, int), f"Problem with float: {aFloat} in setSV"
        '''
        Named as set temp. What is it????
        :return: 
        '''
        self.instrument.write_register(44, aFloat)

    # get operations#######################################################
    def getRunOrStop(self):
        return self.instrument.read_register(35, 0)

    def getInputScaleLow(self):
        return self.instrument.read_register(86, self.getTempDecimalSetting())

    def getInputErrorDetermination(self):
        return self.instrument.read_register(88, self.getTempDecimalSetting())

    def getSettingLimiterLow(self):
        return self.instrument.read_register(216, self.getTempDecimalSetting())

    # set operations ######################################################
    def getInputScaleHigh(self):
        return self.instrument.read_register(86, self.getTempDecimalSetting())

    def  OrStop(self, aInt):
        assert isinstance(aInt, int) and 0<=aInt<=1, f"{aInt} is not a valid integer"
        self.instrument.write_register(35, aInt)

    def setInputScaleLow(self, aFloat):
        assert isinstance(aFloat, float), f"Invalid float with {aFloat} in SetInputScaleLow"
        self.instrument.write_register(86, aFloat)

    def setInputErrorDeterminaiton(self, aFloat):
        assert isinstance(aFloat, float), f"Invalid float with {aFloat} in SetInputErrorDetermination"
        self.instrument.write_register(88, aFloat)

    def setSettingLimiterLow(self, aFloat):
        assert isinstance(aFloat, float), f"Invalid float with {aFloat} in setSettingLimiterLow"
        self.instrument.write_register(216, aFloat)


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

        logging.error(f"{}")
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
