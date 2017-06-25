#!/usr/bin/env bash

#Initialization of database
printf "Make sure to read README before installing this software!\n\n"

python ./src/init/init.py

printf "\nCopying searcher files to /usr/local/bin/"

#Making xms system-wide (Linux)
USR_BIN='/usr/local/bin/'

if $(sudo cp ./src/lookup/xms $USR_BIN && sudo cp ./src/lookup/xms_utilities.py $USR_BIN)
then
  printf "Files copied successfully to /usr/local/bin directory\n"
  printf "\nProgram usage: xms <keyword>\n"
else
  printf "\nUnable to copy files!\n"
  printf "You may need root privileges to perform this operation\n"
  printf "\nProgram usage: ./xms <keyword> (xms file located in lookup directory)\n"
  printf "If you copy xms and xms_utilities from lookup dir to /usr/local/bin/, you get the following procedure call:\n"
  printf "xms <keyword>"
  return 1
fi
