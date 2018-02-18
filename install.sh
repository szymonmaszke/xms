#!/usr/bin/env bash

#Initialization of database
printf "Make sure to read README before installing this software!\\n\\n"

python ./src/init/create_database.py

printf "\\nCopying searcher files to /usr/local/bin/"

#Making xms system-wide (Linux)
USR_BIN='/usr/local/bin/'

if $(sudo cp ./src/lookup/xms $USR_BIN && sudo cp ./src/lookup/xms_utilities.py $USR_BIN); then
	printf "Files copied successfully to /usr/local/bin directory\\n \
		    \\nProgram usage: xms <keyword>\\n"
else
	printf "\\nUnable to copy files!\\n
	        You may need root privileges to perform this operation\\n
	        \\nProgram usage: ./xms <keyword> (xms file located in lookup directory)\\n
	        If you copy xms and xms_utilities from lookup dir to /usr/local/bin/,
	        you can use this software as follows:\\n
	        xms <keyword>"
	return 1
fi
