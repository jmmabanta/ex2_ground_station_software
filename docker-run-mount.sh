#!/bin/bash

# Mounts current directory (repo from host) to container to allow for live changes
# Will NOT automatically run CLI
export GS_HOME=$(pwd)

# To mount a database to log to (OPTIONAL), make a .env file
# with the DATABASE_URL variable set to the database's path
export $(grep -v '^#' .env | xargs)

docker run --rm -it -v $GS_HOME:/home/gs -v $DATABASE_URL:/home/gs/src/groundStation/dev.db ground_station:latest
