#!/bin/bash

# Color setup
Color_Off='\033[0m'
Green='\033[0;32m'
Red='\033[0;31m'
Yellow='\033[0;33m'


# Function to display usage instructions
usage() {
    echo "Usage: $0 [-down]"
    echo "Options:"
    echo "  -down   Stop and remove Docker containers for the application"
    exit 1
}

# Handle script options
DOWN=false
if [[ "$1" == "-down" ]]; then
    DOWN=true
elif [[ "$1" != "" ]]; then
    usage
fi

if [ "$DOWN" = false ]; then

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
            echo -e "[${Red}KO${Color_Off}] Crontab installation failed. Unsupported package manager."
            exit 1
        fi

        # Handle installation state
        if command -v crontab &> /dev/null; then
            echo -e "[${Green}OK${Color_Off}] Crontab installation successful."
        else
            echo -e "[${Red}KO${Color_Off}] Crontab installation failed."
        fi
    else
        echo -e "[${Green}OK${Color_Off}] Crontab already installed."
    fi

    # Install Python3 to run python script
    echo -e "${Yellow}[=================> Python3 Installation <=================]${Color_Off}"

    if ! command -v python3 &> /dev/null; then

        # Arch Linux installation handling
        if command -v pacman &> /dev/null; then
            pacman -Sy python --noconfirm
        # Ubuntu installation handling
        elif command -v apt-get &> /dev/null; then
            apt-get update
            apt-get install python3
        else
            echo -e "[${Red}KO${Color_Off}] Python3 installation failed. Unsupported package manager."
            exit 1
        fi

        # Handle Python3 installation state
        if command -v python3 &> /dev/null; then
            echo -e "[${Green}OK${Color_Off}] Python3 installation successful."
        else
            echo -e "[${Red}KO${Color_Off}] Python3 installation failed."
        fi
    else
        echo -e "[${Green}OK${Color_Off}] Python3 already installed."
    fi

    # Install Docker
    echo -e "${Yellow}[=================> Docker Installation <=================]${Color_Off}"
    if ! command -v docker &> /dev/null; then
        echo -e "[${Red}KO${Color_Off}] Docker not found. Installing Docker..."

        # Install Docker on Ubuntu
        if command -v apt-get &> /dev/null; then
            apt-get update
            apt-get install docker.io
        # Install Docker on Arch Linux
        elif command -v pacman &> /dev/null; then
            pacman -Sy docker --noconfirm
        else
            echo -e "[${Red}KO${Color_Off}] Docker installation failed. Unsupported package manager."
            exit 1
        fi

        # Check Docker installation state
        if command -v docker &> /dev/null; then
            echo -e "[${Green}OK${Color_Off}] Docker installation successful."
        else
            echo -e "[${Red}KO${Color_Off}] Docker installation failed."
            exit 1
        fi
    else
        echo -e "[${Green}OK${Color_Off}] Docker already installed."
    fi

    APP_DIR=/app/cit

    # Setup project on a /app/project directory
    echo -e "${Yellow}[=================> APP_DIR creation <=================]${Color_Off}"

    if [ ! -d "$APP_DIR" ]; then
        mkdir -p "$APP_DIR"
        cp -r "$(dirname "$0")"/* "$APP_DIR"
        echo -e "[${Green}OK${Color_Off}] Created ${APP_DIR} directory and copied files."
    else
        echo -e "[${Green}OK${Color_Off}] ${APP_DIR} directory already exists."
    fi

    if [ -f "$(dirname "$0")/.env" ]; then
            cp "$(dirname "$0")/.env" "$APP_DIR"
            echo -e "[${Green}OK${Color_Off}] Copied .env file to ${APP_DIR}."
    else
            echo -e "[${Red}WARNING${Color_Off}] No .env file found in the source directory."
    fi

    echo -e "${Yellow}[=================> Building and Starting Docker Project <=================]${Color_Off}"

    cd "$APP_DIR"
    docker-compose up -d --build

    # Check Docker Compose execution status
    DOCKER_COMPOSE_EXIT_CODE=$?
    if [ $DOCKER_COMPOSE_EXIT_CODE -eq 0 ]; then
        echo -e "[${Green}OK${Color_Off}] Docker project running"
    else
        echo -e "[${Red}KO${Color_Off}] Docker project failed. See logs"
    fi

    # Cron job setup for script that will run every 5 minutes
    echo -e "${Yellow}[=================> Setting up Cron Job for script <=================]${Color_Off}"
    if command -v crontab &> /dev/null; then
        # Write cron job in temporary file
        CRON_JOB="*/5 * * * * cd ${APP_DIR} && python3 main.py"
        echo "$CRON_JOB" > /tmp/cron_job

        # Add job to crontab
        crontab /tmp/cron_job
        rm /tmp/cron_job

        echo -e "[${Green}OK${Color_Off}] Crontab setup"
    else
        echo -e "[${Red}KO${Color_Off}] Crontab setup"
    fi

    echo -e "${Green}Build completed successfully.${Color_Off}"

else
    #Down the docker
    echo -e "${Yellow}[=================> Down docker <=================]${Color_Off}"
    cd "$APP_DIR"

    docker-compose down
    echo -e "[${Green}OK${Color_Off}] Docker containers stopped and removed."
fi
