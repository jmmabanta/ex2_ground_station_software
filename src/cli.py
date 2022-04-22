'''
 * Copyright (C) 2020  University of Alberta
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
 * @file test.py
 * @author Andrew Rooney, Daniel Sacro
 * @date 2020-11-20
'''

'''  to run > sudo LD_LIBRARY_PATH=../libcsp/build PYTHONPATH=../libcsp/build python3 src/cli.py -I uart -d /dev/ttyUSB1  '''
import time
from groundStation import groundStation
from FT_handler import FT_handler

opts = groundStation.options()
gs = groundStation.groundStation(opts.getOptions())
flag = groundStation.GracefulExiter()
ft_handler = FT_handler()

def cli():
    while True:
        if flag.exit():
            print('Exiting receiving loop')
            flag.reset()
            return
        try:
            server, port, toSend = gs.getInput(prompt='to send: ')
            if server == 24:
                # This is a direct UART command to a ground station EnduroSat transceiver to enter PIPE
                # Can be deleted for flight
                gs.__setPIPE__()
            elif port == 20:
                # A command was issued specifically to the 2U Payload File Transferring Service (port 20)
                resp = gs.transaction(server, port, toSend)

                # TODO - Somehow check what subport it's going to (in order to know whether it's a downlink, uplink, or stop FT)
                # TODO - Also check what arguments are being taken (in order to know what file to open)

                # TODO - Implement a check that ensures that subservices 4 and 5 are NOT accessible by SC operators

                if resp['err'] == 0:
                    # Only begin file transfer process if OBC is ready to begin as well
                    ft_handler.handle_FT() # NOTE - This method takes 2 arguments: a mode (either "downlink" or "uplink") and a filename
            else:
                resp = gs.transaction(server, port, toSend)

                #checks if housekeeping multiple packets. if so, a list of dictionaries is returned
                if type(resp) == list:
                    for rxData in resp:
                        print("--------------------------------------------------------------------------")
                        [print(key,':',value) for key, value in rxData.items()]
                #else, only a single dictionary is returned
                else:
                    [print(key,':',value) for key, value in resp.items()]
            
        except Exception as e:
            print(e)

if __name__ == '__main__':
    flag = groundStation.GracefulExiter()
    cli()
