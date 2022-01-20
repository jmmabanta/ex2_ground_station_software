#!/bin/bash
export GS_HOME=$(pwd)
docker run --rm -it -v $GS_HOME:/home/gs ground_station:latest
