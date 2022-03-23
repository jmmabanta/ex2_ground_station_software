'''
 * Copyright (C) 2021  University of Alberta
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
'''
'''
 * @file test_charon_and_gps.py
 * @author Daniel Sacro
 * @date 2022-3-10
'''

'''Please note that many of the ground station commands and housekeeping variables needed in this file do not yet exist at the time of last edit'''
import time
import numpy as np

import sys
import os
sys.path.append("./test")
from testLib import testLib as test

sys.path.append("../src")
from groundStation import groundStation
opts = groundStation.options()
gs = groundStation.groundStation(opts.getOptions())

test = test() #call to initialize local test class

# TODO - Automate the remaining steps in the EPS Ping Watchdog test - 2-4
def test_EPS_pingWatchdog():
    testPassed = "Pass"
    # 1) Ensure OBC, UHF, and EPS are turned on, and that the OBC has the most up-to-date firmware installed (Doesn't have to be automated)

    # 2) Ensure that the OBC is operating in such a way that it will respond to ping requests of CSP ID 1

    # 3) Configure an EPS and OBC ping watchdogs to check CSP ID 1 every 5 mins and toggle EPS output 6 for 10 seconds if it times out

    # 4) Enable OBC to check Charon's operating status every 5 min by verifying the GPS CRC. OBC will command EPS to reset power channel 7 for 10 seconds if verification fails

    # TODO "pchannelX" (where X = a num from 1-9) doesn't exist yet. The name is just a placeholder, so replace them with the right HK names
    pchannels = ['pchannel1', 'pchannel2', 'pchannel3', 'pchannel4', 'pchannel5', 'pchannel6', 'pchannel7', 'pchannel8','pchannel9']

    # 5) Repeat the following every 10 seconds for 6 minutes:
    for i in range(36): 
        # Gather all EPS HK info
        server, port, toSend = gs.getInput('eps.cli.general_telemetry')
        response = gs.transaction(server, port, toSend)
        
        # Display data on ground station CLI
        for val in test.expected_EPS_HK:
            # To pass test, all active power channels have output state = 1
            colour = '\033[0m' #white
            if val in pchannels:
                if (response[val] == 0):
                    testPassed = "Fail"
                    colour = '\033[91m' #red
                else:
                    colour = '\033[92m' #green
            print(colour + str(val) + ": " + str(response[val]))

        time.sleep(10)

    # 6) Disconnect UART connection between CHaron and OBC
    input("\nPlease disconnect the UART connection between Charon and the OBC. Press enter to resume tests.\n") 

    # 7) Repeat step 5:
    for j in range(36): 
        server, port, toSend = gs.getInput('eps.cli.general_telemetry')
        response = gs.transaction(server, port, toSend)

        for val in test.expected_EPS_HK:
            # To pass test, all active power channels have output state = 1 except channel 7, which should be 0
            colour = '\033[0m' #white
            if val in pchannels:
                if (response[val] == 0) and (val != 'pchannel7'):
                    testPassed = "Fail"
                    colour = '\033[91m' #red
                elif (response[val] == 1) and (val == 'pchannel7'):
                    testPassed = "Fail"
                    colour = '\033[91m' #red
                else:
                    colour = '\033[92m' #green
            print(colour + str(val) + ": " + str(response[val]))
            
        time.sleep(10)

    # 8) Reconnect UART connection between Charon and OBC
    input("\nPlease Reconnect the UART connection between Charon and the OBC. Press enter to resume tests.\n")  

    # Take note of the test results
    if (testPassed == "Pass"):
        colour = '\033[92m' #green
        test.passed += 1
    else:
        colour = '\033[91m' #red
        test.failed += 1

    print(colour + ' - EPS PING WATCHDOG TEST ' + testPassed + '\n\n' + '\033[0m')

    # PASS CONDITION: During step 5, Output State = 1 for all active power channels at all times
    #                 During step 7, Output State = 1 for all active power channels except channel 7, which should be 0
    return True

def testAllCommandsToOBC():
    print("\n---------- OBC SYSTEM-WIDE HOUSEKEEPING TEST ----------\n")
    test.testHousekeeping(1, 1, 1, 1, 1, 0, 0, 0, 0, 0)

    # TODO - Finish function implementation
    print("\n---------- EPS PING WATCHDOG TEST ----------\n")
    test_EPS_pingWatchdog()

    test.summary() #call when done to print summary of tests

if __name__ == '__main__':
    testAllCommandsToOBC()
