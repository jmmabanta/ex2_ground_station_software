/*
 * Copyright (C) 2015  University of Alberta
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
 * @file uTransceiver.c
 * @author Thomas Ganley
 * @date 2020-05-28
 */

#ifndef UTRANSCEIVER_H
#define UTRANSCEIVER_H

#include "mock_i2c.h"
#include <stdint.h>
#include <string.h>

#define MAX_W_CMDLEN 120
#define MAX_W_ANSLEN 30
#define MAX_R_CMDLEN 30
#define MAX_R_ANSLEN 150
#define MIN_U_FREQ 435000000
#define MAX_U_FREQ 438000000

#define LETTER_E 0x45
#define LETTER_M 0x4D
#define LETTER_O 0x4F
#define BLANK_SPACE 0x20
#define CARRIAGE_R 0x0D

typedef enum{
	U_GOOD_CONFIG =  0,
	U_BAD_CONFIG  = -1,
	U_BAD_PARAM   = -2,
	U_BAD_ANS_CRC = -3,

	U_BAD_CMD_CRC = -4,
	U_BAD_CMD_LEN = -5,
	U_CMD_SPEC_2  =  2,
	U_CMD_SPEC_3  =  3,

	U_UNK_ERR     = -10,
}U_ret;

typedef struct {
  uint8_t len;
  uint8_t message[MAX_W_CMDLEN];
} uhf_configStruct;

typedef struct {
  uint32_t add;
  uint8_t data[16];
} uhf_framStruct;

//* Functions for moving data to/from the UHF transceiver in 128 byte chunks
U_ret send_U_data(uint8_t* arr);
U_ret receive_U_data(uint8_t* arr);

// Converts hex values to their ASCII characters
void convHexToASCII(int length, uint8_t * arr);
void convHexFromASCII(int length, uint8_t * arr);
uint32_t crc32_calc(size_t length, char * cmd);
int find_blankSpace(int length, char* string);

int generic_U_write(uint8_t code, void * param);
int generic_U_read(uint8_t code, void * param);
#endif // UTRANSCEIVER_H
