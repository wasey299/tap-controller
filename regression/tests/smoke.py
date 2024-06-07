##########################################################
# PSU ECE510 Post-silicon Validation Projects
# --------------------------------------------------------
# Filename: smoke.py
# --------------------------------------------------------
# Purpose: TAP Controller Smoke Tests
##########################################################

import os, sys
from tap.common.loopback import *
from tap.common.tap import *
import unittest

class smoke(unittest.TestCase): 
    """ smoke/power on tests, hopefully won't produce actual smoke """
    
    def setUp(self):
        """ fires before each test
        Setting up for the test
    
        """
        log_level = LOG_LEVEL 
        self.logger = get_logger(self.id(), log_level)
        log(self.logger, 'info', '{}Running {}'.format(color_map['highlight'],self.id()))

        self.tap = Tap(log_level=log_level)
        self.loopback_monitor = LoopBack(log_level=log_level)
        self.loopback_monitor.set_monitor()
    
    def tearDown(self):
        """ fires after each test
        Cleaning up after the test
    
        """
        self.loopback_monitor.remove_monitor()
        self.tap.clean_up()
        log(self.logger, 'info', '{}Done with {}\n'.format(color_map['highlight'],self.id()))    
    
    def testReset(self):

        # Transtion to reset
        self.tap.reset()

        # Check for reset state
        self.assertEqual("Test_Logic_Reset",self.loopback_monitor.cur_state)

   # @unittest.skip
    def testReset2ShiftIR(self):
        # print(self.loopback_monitor.cur_state)
        
        # Transition to reset state
        self.tap.reset()

        #print(self.loopback_monitor.cur_state)
        
        # reset -> Shift-IR
        self.tap.reset2ShiftIR()
        # print(self.loopback_monitor.cur_state)
        
        # Check for SHift-IR
        self.assertEqual("Shift_IR", self.loopback_monitor.cur_state)
       # pass

   # @unittest.skip
    def testReadDeviceCode(self): #

        # Transition to reset state
        self.tap.reset()

        # reset -> Shift-IR
        self.tap.reset2ShiftIR()

        # Shifting in data: "100100" to activate IDCODE Register
        self.tap.shiftInData("100100")
        
        # Exit1-IR -> ShiftDR
        self.tap.exit1IR2ShiftDR()

        # Capturing the ShiftOutData for Device ID
        deviceID = self.tap.shiftOutData(32)

        # Printing Device ID
        print("IDcode value is: %#x" %deviceID)
        #self.assertEqual("whatever the hex number",rslt) 
#Go to idle
#Go to idle
   
      #  pass


    def testExit1IR2ShiftDR(self):

        # Transition to reset state    
        self.tap.reset()

        # reset -> Shift-IR
        self.tap.reset2ShiftIR()

        # Shifting in data: "100100" to activate IDCODE Register
        self.tap.shiftInData("100100")

        # Exit1-IR -> ShiftDR
        self.tap.exit1IR2ShiftDR()

        # Check for Shift-DR 
        self.assertEqual("Shift_DR", self.loopback_monitor.cur_state)
        
        
       # pass


