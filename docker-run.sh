#!/bin/bash
export GS_HOME=$(pwd)
docker run --rm -it -v $GS_HOME:/home/gs -v $(readlink src/groundStation/dev.db):/home/gs/src/groundStation/dev.db ground_station:latest
