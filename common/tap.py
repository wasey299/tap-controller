##########################################################
# PSU ECE510 Post-silicon Validation Project 1
# --------------------------------------------------------
# Filename: tap.py
# --------------------------------------------------------
# Purpose: TAP Controler Class
##########################################################

from tap.common.tap_gpio import *
from tap.log.logging_setup import *
import time

class Tap(Tap_GPIO): # Tap inherits Tap_GPIO
    """ Class for JTAG TAP Controller"""

    def __init__(self,log_level=logging.INFO): 
        """ initialize TAP """
        self.logger = get_logger(__file__,log_level)
        self.max_length = 1000

        #set up the RPi TAP pins
        Tap_GPIO.__init__(self) # Calling the _init_ method from parent. So basically adding properties in the parent method.

    def toggle_tck(self, tms, tdi): # For state transition
        """ toggle TCK for state transition 

        :param tms: data for TMS pin
        :type tms: int (0/1)
        :param tdi: data for TDI pin
        :type tdi: int (0/1)

        """
        self.set_io_data(tms, tdi, 1)
        self.set_io_data(tms, tdi, 0)
       #   self.set_io_data(tms, tdi, 0)
       # pass
       
    def reset(self):
        """ set TAP state to Test_Logic_Reset """
        # assert TMS for 5 TCKs in a row
        # we decided to do it for 6 ticks just to make sure that every state transitions to Test-Logic-Reset
        for i in range(6):
            self.toggle_tck(1,0)
       # pass

    def reset2ShiftIR(self):
        """ shift TAP state from reset to shiftIR """

        # reset -> idle, de-assert TMS for one TCK cycle
        self.toggle_tck(0,0)
        
        # idle -> select DR-Scan, assert TMS for one TCK cycle
        self.toggle_tck(1,0)

        # select DR-Scan -> Select IR-Scan, assert TMS for one TCK cycle
        self.toggle_tck(1,0)

        # select IR-Scan -> Capture-IR, de-assert TMS for one TCK cycle
        self.toggle_tck(0,0)

        # Capture-IR -> Shift-IR, de-assert TMS for one TCK cycle
        self.toggle_tck(0,0)

        #pass 

    def exit1IR2ShiftDR(self): 
        """ shift TAP state from exit1IR to shiftDR """
        # Exit1-IR -> Update-IR, assert TMS for one TCK cycle
        self.toggle_tck(1,0)

        # Update-IR -> Select DR-Scan, assert TMS for one TCK cycle
        self.toggle_tck(1,0)

        # Select DR-Scan -> Capture-DR, de-assert TMS for one TCK cycle
        self.toggle_tck(0,0)

        # Capture-DR -> Shift-DR, de-assert TMS for one TCK cycle
        self.toggle_tck(0,0)
        
        #pass

    def exit1DR2ShiftIR(self):
        """ shift TAP state from exit1DR to shiftIR """
        
        # Exit1-DR -> Update-DR, assert TMS for one TCK cycle
        self.toggle_tck(1,0)

        # Update-DR -> Select DR-Scan, assert TMS for one TCK cycle
        self.toggle_tck(1,0)

        # select DR-Scan -> Select IR-Scan, assert TMS for one TCK cycle
        self.toggle_tck(1,0)

        # select IR-Scan -> Capture-IR, de-assert TMS for one TCK cycle
        self.toggle_tck(0,0)

        # Capture-IR -> Shift-IR, de-assert TMS for one TCK cycle
        self.toggle_tck(0,0)        
        
        #pass

    def shiftInData(self, tdi_str):    
        """ shift in IR/DR data

        :param tdi_str: TDI data to shift in
        :type tdo_str: str

        """      
        
        # De-asserting TMS with TDI (converted from string to int) bits excluding the LSB
        for i in range(len(tdi_str) - 1):
            self.toggle_tck(0, int(tdi_str[i]))

        # Asserting TMS with LSB of TDI (converted from string to int) 
        self.toggle_tck(1, int(tdi_str[len(tdi_str) - 1]))

        #pass

    def shiftOutData(self, length): #
        """ get IR/DR data

        :param length: chain length        
        :type length: int
        :returns: int - TDO data
        After looping, go to idle
        """
        
        # Instantiate an empty list, data_out, and appended it with the value returning from the method read_tdo_data() with TMS de-asserted
        data_out =[]
        for i in range(length):
                data_out.append(self.read_tdo_data())
                if i < length -1:
                        self.toggle_tck(0,0)

        # TMS is then asserted
        self.toggle_tck(1,0)

        #The data is changed into list to perform reverse operation
        data_str =''.join(map(str, reversed(data_out)))

        # Chang back to int and return in binary
        return int(data_str, 2)    


    def getChainLength(self): #This is not required
        """ get chain length

        :returns: int -- chain length	

        """

        return 0
