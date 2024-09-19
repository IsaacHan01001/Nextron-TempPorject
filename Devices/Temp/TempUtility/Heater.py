"""Driver for the heater in the CVD system. Talks to the heater controller and the heater policeman.

Implemented with the modules :mod:`eurotherm3500` and :mod:`eurotherm3216i`.

"""

import eurotherm3500
import eurotherm3216i

class heater():
    """Class for the heater in the CVD system. Talks to the heater controller and the heater policeman.

    """

    ADDRESS_HEATERCONTROLLER = 1
    """Modbus address for the heater controller."""

    ADDRESS_POLICEMAN = 2
    """Modbus address for the heater over-temperature protection unit."""

    SUPPLY_VOLTAGE = 230
    """Supply voltage (V)."""

    def __init__(self, port):
        self.heatercontroller = eurotherm3500.Eurotherm3500(   port, self.ADDRESS_HEATERCONTROLLER)
        self.policeman        = eurotherm3216i.Eurotherm3216i( port, self.ADDRESS_POLICEMAN)

    def getTemperatureCenter(self):
        """Return the temperature (in deg C)."""
        return self.heatercontroller.get_pv_loop1()

    def getTemperatureEdge(self):
        """Return the temperature (in deg C) for the edge heater zone."""
        return self.heatercontroller.get_pv_loop2()

    def getTemperaturePolice(self):
        """Return the temperature (in deg C) for the overtemperature protection sensor."""
        return self.policeman.get_pv()

    def getOutputCenter(self):
        """Return the output (in %) for the heater center zone."""
        return self.heatercontroller.get_op_loop1()