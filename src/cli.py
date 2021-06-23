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
 * @author Andrew Rooney
 * @date 2020-11-20
'''

'''  to run > sudo LD_LIBRARY_PATH=../libcsp/build PYTHONPATH=../libcsp/build python3 src/cli.py -I uart -d /dev/ttyUSB1  '''
import time
from groundStation import groundStation

opts = groundStation.options()
gs = groundStation.groundStation(opts.getOptions())
flag = groundStation.GracefulExiter()

def cli():
    while True:
        if flag.exit():
            print('Exiting receiving loop')
            flag.reset()
            return
        try:
            server, port, toSend = gs.getInput(prompt='to send: ')
            resp = gs.transaction(server, port, toSend)

            [print(key,':',value) for key, value in resp.items()]
        except Exception as e:
            print(e)

if __name__ == '__main__':
    flag = groundStation.GracefulExiter()
    cli()
