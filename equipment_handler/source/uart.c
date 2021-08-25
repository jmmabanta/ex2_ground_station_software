/*
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
 */
/**
 * @file uart.c
 * @author Thomas Ganley
 * @date 2021-08-23
 */

#include "HL_sci.h"
#include "uart.h"

void uart_send(uint32_t length, uint8_t * data){
    sciSetBaudrate(sciREG2, 115200);
    sciSend(sciREG2, length, data);
}

void uart_sendAndReceive(uint32_t command_length, uint8_t * command, uint32_t answer_length, uint8_t * ans){
    sciSetBaudrate(sciREG2, 115200);
    sciSend(sciREG2, command_length, command);
    sciReceive(sciREG2, answer_length, ans);
}
