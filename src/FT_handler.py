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
        # TODO - maxBytesToRead can and should be changed to a higher value to speed up file transfers
        # NOTE - If you increase maxBytesToRead, you should add in more '>u4" variables to the subservice
        # commands 4 and 5 in system.py
        maxBytesToRead = 100 
        bytesToRead = maxBytesToRead
        
        # NOTE - if mode = 0 (success) nothing should happen since 0 is only returned for subservices 3-5, 
        # which are STOP_FT, SEND_BYTES, and PROCESS_BYTES. The first of the three can only stop file
        # transfers and can't return a mode 2 or 3. Similarly, the last two of the three also can't return
        # modes 2 or 3 and additionally should NOT be accessible by SC operators. Only the FT_handler
        # should have access to subservices 4 and 5 so that it can automatically handle the file transfer
        # process

        if mode == 1:
            # Mode 1 = fail -> Some subservice command fails for some reason, close any opened files on the OBC
            print("Something failed on the OBC!")
            server, port, toSend = gs.getInput(inVal='obc.FT_2U_PAYLOAD.FT_2U_PAYLOAD_STOP_FT')
            resp = gs.transaction(server, port, toSend)
        elif mode == 2:
            # Mode 2 = downlink
            fileIsOpen = True
            writeFailed = False
            try:
                toReceive = open(filename, 'wb')
            except:
                # If file can't be opened, abort file transfer
                print("File can't be opened on the GS for " + str(filename) + "!")
                fileIsOpen = False
                server, port, toSend = gs.getInput(inVal='obc.FT_2U_PAYLOAD.FT_2U_PAYLOAD_STOP_FT')
                resp = gs.transaction(server, port, toSend)

            while bytesToRead == maxBytesToRead and fileIsOpen:
                # Tell OBC to send file data to GS
                server, port, toSend = gs.getInput(inVal='obc.FT_2U_PAYLOAD.FT_2U_PAYLOAD_SEND_BYTES')
                resp = gs.transaction(server, port, toSend)
                if resp['err'] != 0:
                    # If a file read fails on the satellite, abort file transfer
                    print("File read failed on the satellite!")
                    break

                # Save bytes from CSP packet
                bytesToRead = resp['bytesToRead']
                for i in range(1, bytesToRead + 1):
                    index = "block" + str(i)
                    # Format value into binary
                    buffer = format(resp[index], "b")
                    try:
                        toReceive.write(buffer)
                    except:
                        # If a file write fails on the ground station, abort file transfer
                        print("File write failed on the ground station!")
                        writeFailed = True
                        server, port, toSend = gs.getInput(inVal='obc.FT_2U_PAYLOAD.FT_2U_PAYLOAD_STOP_FT')
                        resp = gs.transaction(server, port, toSend)
                        break

                if writeFailed:
                    break
                
            # Close file after FT is finished or aborted
            toReceive.close()
        elif mode == 3:
            # Mode 3 = uplink
            fileExists = True
            try:
                toSend = open(filename, 'rb')
            except:
                # If file doesn't exist, abort file transfer
                print(str(filename) + " doesn't exist on the GS!")
                fileExists = False
                server, port, toSend = gs.getInput(inVal='obc.FT_2U_PAYLOAD.FT_2U_PAYLOAD_STOP_FT')
                resp = gs.transaction(server, port, toSend)

            while bytesToRead == maxBytesToRead and fileExists:
                try:
                    byteBuffer = toSend.read(maxBytesToRead)
                except:
                    # If a file read fails on ground station, abort file transfer
                    print("File read failed on the ground station!")
                    server, port, toSend = gs.getInput(inVal='obc.FT_2U_PAYLOAD.FT_2U_PAYLOAD_STOP_FT')
                    resp = gs.transaction(server, port, toSend)
                    break

                # Update bytesToRead
                bytesToRead = len(byteBuffer)
                bytesArrayBuffer = bytearray(byteBuffer)

                # Pad buffer with 0-bytes
                if bytesToRead < maxBytesToRead:
                    for i in range(0, maxBytesToRead - bytesToRead):
                        bytesArrayBuffer.append(0)

                # Place data into a CSP packet 
                command = 'obc.FT_2U_PAYLOAD.FT_2U_PAYLOAD_PROCESS_BYTES(' + str(bytesToRead)
                block = bytearray(b'')
                byteCount = 0
                for byte in bytesArrayBuffer:
                    if byteCount < 4:
                        # Place 4 bytes into a "block"
                        block.append(byte) 
                        byteCount += 1
                    else:
                        # Convert this "block" of 4 bytes into an unsigned integer and place into command as an argument
                        command += ',' + str(int.from_bytes(block, "big"))
                        # Reset block and counters
                        block = bytearray('b')
                        byteCount = 0
                # Close command with bracket at the end
                command += ')'

                # Tell OBC to process file data from the GS
                server, port, toSend = gs.getInput(inVal=command)
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

                
