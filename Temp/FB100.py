from TempUtility.Utils import *
import serial
import minimalmodbus

class FB100:
    __author__ = "Isaaac Han"
    __email__ = "cogitoergosum01001@gmail.com"

    def __init__(self, port = None, channel = None):
        '''
        Communication for FB100. Communicate via RKC communication protocol

        The program assumes: RS485. To make it more versatile, simply change regex in grep funciton at Utils.py
        :param port: listportinfo channel: slaveaddress
        :param channel: channel number, default 0 is used for broadcasting command to all
        '''

        self.port = port
        self.channel = channel
        self.isConnected = False
        self.makeInstrument()
        self.makeTempfields()

    def makeInstrument(self):
        '''
        creating minimalmodbus.instrument instance when received a valid port and channel
        :return:
        '''
        try:
            if self.port and self.channel:
                self.instruments = minimalmodbus.Instrument(self.port["Device"], self.channel)
                self.port["Channel"] = self.channel
                self.isConnected = True
            else:
                print(f"Insufficient args: port: {self.port} channel: {self.channel}")
            return
        except:
            import traceback
            traceback.print_exc()
            return

    def makeTempfields(self):
        rootFields = ["Temperature", "PID"]
        temperatureFields = ["CurrentTemp", "SetTemp"]
        PIDFields = ["P", "I", "D"]
        subFields = [temperatureFields, PIDFields]

        self.Temperature = dict().fromkeys(rootFields, None)
        for subInd, field in enumerate(rootFields):
            self.Temperature[field] = dict().fromkeys(subFields[subInd], 0)


    def

    def _Is_LN(self):
        return True if self.mode is None else False

    def _write(self):
        '''
        W
        :return:
        '''
        self.write()
        self.read()

    def formatSendData(self, data, mode=0):
        '''
        data format STX(1) Identifier(2) Data(7) ETX(1) BCC(1) or
        data format STX(1) Memory Area Number(2), Identifier(2) Data(7) ETX(1) BCC(1)
        EOT = (04H), ENQ = (05H), ACK = (06H), NAK = (15H), STX = (02H), and ETX = (03H)
        polling is in manual p# 20
        EOT [Address] [Memory area Number] [ID] [ENQ] [EOT]
        mode: 0 no memory area number selected, 1 for area number specified
        :return: string
        '''

        if mode == 0:
            bcc_data = data[-1]
            paddedString = f'\x04{}'

    def set_Mode(self, mode):
        self.mode = mode

    def get_pv_loop1(self):
        """Return the process value (PV) for loop1."""
        return self.read_register(289, 1)

    def is_manual_loop1(self):
        """Return True if loop1 is in manual mode."""
        return self.read_register(273, 1) > 0

    def get_sptarget_loop1(self):
        """Return the setpoint (SP) target for loop1."""
        return self.read_register(2, 1)

    def get_sp_loop1(self):
        """Return the (working) setpoint (SP) for loop1."""
        return self.read_register(5, 1)

    def set_sp_loop1(self, value):
        """Set the SP1 for loop1.

        Note that this is not necessarily the working setpoint.

        Args:
            value (float): Setpoint (most often in degrees)
        """
        self.write_register(24, value, 1)

    def disable_sprate_loop1(self):
        """Disable the setpoint (SP) change rate for loop1. """
        VALUE = 1
        self.write_register(78, VALUE, 0)
