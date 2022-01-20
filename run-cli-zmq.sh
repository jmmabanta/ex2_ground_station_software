#!/bin/bash
# Run this script to open CLI in docker container
LD_LIBRARY_PATH=../libcsp/build PYTHONPATH=../libcsp/build python3 src/cli.py -I zmq
