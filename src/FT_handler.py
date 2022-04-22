"""
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
"""
"""
 * @file FT_handler.py
 * @author Daniel Sacro
 * @date 2021-04-21
"""

from groundStation import groundStation
opts = groundStation.options()
gs = groundStation.groundStation(opts.getOptions())

class FT_handler(object):
    def handle_FT(self, mode, filename):
        # Starts all while loops
        bytesToRead = 900

        if mode == "downlink":
            toReceive = open(filename, 'wb')
            while bytesToRead == 900:
                # Tell OBC to send file data to GS
                server, port, toSend = gs.getInput(inVal='obc.FT_2U_PAYLOAD.FT_2U_PAYLOAD_SEND_BYTES')
                resp = gs.transaction(server, port, toSend)
                if resp['err'] != 0:
                    # If a file read fails on the satellite, abort file transfer
                    print("File read failed on the satellite!")
                    break

                bytesToRead = resp['bytesToRead']
                # TODO - Places bytes from CSP packet into a buffer
                # NOTE - Also ensure that the bytes are in binary (i.e. b'')

                try:
                    toReceive.write(buffer)
                except:
                    # If a file write fails on the ground station, abort file transfer
                    print("File write failed on the ground station!")
                    server, port, toSend = gs.getInput(inVal='obc.FT_2U_PAYLOAD.FT_2U_PAYLOAD_STOP_FT')
                    resp = gs.transaction(server, port, toSend)
                    break
            # Close file after FT is finished or aborted
            toReceive.close()
        elif mode == "uplink":
            fileExists = True
            try:
                toSend = open(filename, 'rb')
            except:
                # If file doesn't exist, abort file transfer
                fileExists = False
                server, port, toSend = gs.getInput(inVal='obc.FT_2U_PAYLOAD.FT_2U_PAYLOAD_STOP_FT')
                resp = gs.transaction(server, port, toSend)

            while bytesToRead == 900 and fileExists:
                try:
                    buffer = toSend.read(bytesToRead)
                except:
                    # If a file read fails on ground station, abort file transfer
                    print("File read failed on the ground station!")
                    server, port, toSend = gs.getInput(inVal='obc.FT_2U_PAYLOAD.FT_2U_PAYLOAD_STOP_FT')
                    resp = gs.transaction(server, port, toSend)
                    break

                # TODO - Update bytesToRead somehow
                # TODO - Place data into a CSP packet somehow

                # Tell OBC to process file data from the GS
                server, port, toSend = gs.getInput(inVal='obc.FT_2U_PAYLOAD.FT_2U_PAYLOAD_PROCESS_BYTES')
                resp = gs.transaction(server, port, toSend)
                if resp['err'] != 0:
                    # If a file write on the satellite goes wrong, abort file transfer
                    print("File write failed on the satellite!")
                    server, port, toSend = gs.getInput(inVal='obc.FT_2U_PAYLOAD.FT_2U_PAYLOAD_STOP_FT')
                    resp = gs.transaction(server, port, toSend)
                    break
            # Close file after FT is finished or aborted
            toSend.close()
        return

                
