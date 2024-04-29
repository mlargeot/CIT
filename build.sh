#!/bin/bash

# Handle sudo permission
if [ "$(id -u)" != "0" ]; then
    echo "Run 'sudo ./build.sh' to build this programm"
    exit 1
fi
