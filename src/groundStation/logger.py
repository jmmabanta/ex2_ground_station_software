"""
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
"""
"""
 * @file logger.py
 * @author John Mabanta
 * @date 2022-01-23
"""
import datetime
import sqlite3
import os

class Logger:
    """Logs commands + responses to communication table in
    ex2_ground_station_website/groundStation.

    Will automatically disable itself if DATABASE_URL is not set in .env
    prior to starting the docker container.
    """
    def __init__(self, db='src/groundStation/dev.db') -> None:
        self.disabled = False
        if os.path.isfile(db):
            self.__connection = sqlite3.connect(db)
            self.__cursor = self.__connection.cursor()
        else:
            self.disabled = True

    def log(self, command: str, recv='logs', sender='cli'): # FIXME: User
        """Logs the command to the communications table in the db."""
        if not self.disabled:
            data = [command.upper(), datetime.datetime.now(), sender, recv]
            self.__cursor.execute("""INSERT INTO communications
                                    (message, timestamp, sender, receiver, is_queued)
                                    VALUES (?, ?, ?, ?, 0)""", data)
            self.__connection.commit()

    def printLog(self, output: str, recv='logs', sender='cli'):
        """Prints to standard output and logs that same output to db."""
        print(output)
        self.log(output, recv, sender)

    def __del__(self) -> None:
        """Saves any lingering changes to the db before closing."""
        if not self.disabled:
            self.__connection.commit()
            self.__connection.close()
