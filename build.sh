#!/bin/bash

# Color setup
Color_Off='\033[0m'
Green='\033[0;32m'
Red='\033[0;31m'
Yellow='\033[0;33m'

# Handle sudo permission
if [ "$(id -u)" != "0" ]; then
    echo "Run 'sudo ./build.sh' to build this programm"
    exit 1
fi

# Install Crontab
echo -e "${Yellow}[=================> Crontab Installation <=================]${Color_Off}"
if ! command -v crontab &> /dev/null; then
    
    # Arch-linux installation handling
    if command -v pacman &> /dev/null; then
        pacman -Sy cronie --noconfirm
    # Ubuntu installation handling
    elif command -v apt-get &> /dev/null; then
        apt-get update
        apt-get install cron
    else
        echo -e "[${Red}KO${Color_Off}] Crontab installation failed due to package manager."
        exit 1
    fi

    # Handle installation state
    if command -v crontab &> /dev/null; then
        echo -e "[${Green}OK${Color_Off}] Crontab installation."
    else
        echo -e "[${Red}KO${Color_Off}] Crontab installation failed."
    fi
else
    echo -e "[${Green}OK${Color_Off}] Crontab already installed."
fi
