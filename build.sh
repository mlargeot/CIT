#!/bin/bash

# Color setup
Color_Off='\033[0m'
Green='\033[0;32m'
Red='\033[0;31m'
Yellow='\033[0;33m'

# Function to display usage instructions
usage() {
    echo "Usage: $0 [--option]"
    echo "
Global options:"
    echo "  --help     Display build usage and options list"
    echo "  --down     Stop project execution and remove from crontab"
    echo "  --remove   Remove project directory '/app/cit'"
    echo "
Commands:"
    echo "  --add <symbol>  Add cryptocurrency into filter"
    echo "  --del <symbol>  Remove cryptocurrency from filter"
    echo "  --run           Manually run the script project"
    exit 1
}

# Handle script options
DOWN=false
REMOVE=false
ADD=""
DEL=""
RUN=false

if [[ "$1" == "--help" ]]; then
    usage
elif [[ "$1" == "--down" ]]; then
    DOWN=true
elif [[ "$1" == "--remove" ]]; then
    REMOVE=true
elif [[ "$1" == "--add" && "$2" != "" ]]; then
    ADD="$2"
    RUN=true
elif [[ "$1" == "--del" && "$2" != "" ]]; then
    DEL="$2"
    RUN=true
elif [[ "$1" == "--run" ]]; then
    RUN=true
elif [[ "$1" != "" ]]; then
    usage
fi

# Handle --down option
if [ "$DOWN" = true ]; then
    echo -e "${Yellow}[=================> Down Docker Project <=================]${Color_Off}"
    APP_DIR="/app/cit"
    if [ -d "$APP_DIR" ]; then
        cd "$APP_DIR"
        docker-compose down --rmi all --remove-orphans
        echo -e "[${Green}OK${Color_Off}] Docker containers stopped and removed."

        # Remove crontab entry for the script
        if crontab -l >/dev/null 2>&1; then
            crontab -l | grep -v "/app/cit/src" | { cat; echo ""; } | crontab -
            echo -e "[${Green}OK${Color_Off}] Removed crontab entry."
        else
            echo -e "[${Yellow}INFO${Color_Off}] No crontab for current user."
        fi
    else
        echo -e "[${Red}KO${Color_Off}] Project directory '/app/cit' not found."
        exit 1
    fi
fi

# Handle --remove option
if [ "$REMOVE" = true ]; then
    echo -e "${Yellow}[=================> Remove Project Directory <=================]${Color_Off}"
    APP_DIR="/app/cit"
    if [ -d "$APP_DIR" ]; then
        cd "$APP_DIR"
        docker-compose down --rmi all --remove-orphans
        echo -e "[${Green}OK${Color_Off}] Docker containers stopped and removed."
        rm -rf "$APP_DIR"
        echo -e "[${Green}OK${Color_Off}] Removed project directory '/app/cit'."
    else
        echo -e "[${Red}KO${Color_Off}] Project directory '/app/cit' not found."
        exit 1
    fi
fi

# Handle --add and --del options
if [ "$RUN" = true ]; then
    echo -e "${Yellow}[=================> Running Python Script <=================]${Color_Off}"
    APP_DIR="/app/cit"
    if [ -d "$APP_DIR" ]; then
        cd "$APP_DIR/src"
        source venv/bin/activate
        if [ "$ADD" != "" ]; then
            python3 main.py add "$ADD"
            echo -e "[${Green}OK${Color_Off}] Python script 'main.py' executed with 'add $ADD'."
        elif [ "$DEL" != "" ]; then
            python3 main.py del "$DEL"
            echo -e "[${Green}OK${Color_Off}] Python script 'main.py' executed with 'del $DEL'."
        else
            python3 main.py
            echo -e "[${Green}OK${Color_Off}] Python script 'main.py' executed."
        fi
        deactivate
    else
        echo -e "[${Red}KO${Color_Off}] Project directory '/app/cit' not found."
        exit 1
    fi
fi

# Handle default execution
if [ "$DOWN" = false ] && [ "$REMOVE" = false ] && [ "$RUN" = false ]; then

    # Handle sudo permission
    if [ "$(id -u)" != "0" ]; then
        echo "Run 'sudo $0' to execute this script."
        exit 1
    fi

    # Install Crontab
    echo -e "${Yellow}[=================> Crontab Installation <=================]${Color_Off}"
    if ! command -v crontab &> /dev/null; then
        # Arch Linux installation handling
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

    APP_DIR="/app/cit"

    # Setup project in /app/cit directory
    echo -e "${Yellow}[=================> Setup Project Directory <=================]${Color_Off}"
    if [ ! -d "$APP_DIR" ]; then
        mkdir -p "$APP_DIR"
        cp -r "$(dirname "$0")"/* "$APP_DIR"
        echo -e "[${Green}OK${Color_Off}] Created '$APP_DIR' directory and copied files."
    else
        echo -e "[${Green}OK${Color_Off}] '$APP_DIR' directory already exists."
    fi

    # Copy .env file to project directory
    if [ -f "$(dirname "$0")/.env" ]; then
        cp "$(dirname "$0")/.env" "$APP_DIR/src"
        cp "$(dirname "$0")/.env" "$APP_DIR"
        echo -e "[${Green}OK${Color_Off}] Copied .env file to '$APP_DIR/src' and '$APP_DIR'."
    else
        echo -e "[${Red}WARNING${Color_Off}] No .env file found in the source directory."
    fi

    # Create virtual environment and install dependencies
    echo -e "${Yellow}[=================> Creating Virtual Environment <=================]${Color_Off}"
    cd "$APP_DIR/src" || exit 1
    python3 -m venv venv
    source venv/bin/activate
    pip install -r ../build/requirements.txt
    deactivate
    echo -e "[${Green}OK${Color_Off}] Venv setup."

    echo -e "${Yellow}[=================> Building and Starting Docker Project <=================]${Color_Off}"
    cd "$APP_DIR"
    docker-compose up -d --build

    # Check Docker Compose execution status
    DOCKER_COMPOSE_EXIT_CODE=$?
    if [ $DOCKER_COMPOSE_EXIT_CODE -eq 0 ]; then
        echo -e "[${Green}OK${Color_Off}] Docker project running."
    else
        echo -e "[${Red}KO${Color_Off}] Docker project failed. See logs."
    fi

    # Cron job setup for script to run every 5 minutes
    echo -e "${Yellow}[=================> Setting up Cron Job for script <=================]${Color_Off}"
    if command -v crontab &> /dev/null; then
        # Write cron job in temporary file
        CRON_JOB="*/5 * * * * cd ${APP_DIR}/src && source venv/bin/activate && python3 main.py"
        echo "$CRON_JOB" > /tmp/cron_job

        # Add job to crontab
        crontab /tmp/cron_job
        rm /tmp/cron_job

        echo -e "[${Green}OK${Color_Off}] Crontab setup."
    else
        echo -e "[${Red}KO${Color_Off}] Crontab setup failed."
    fi

    echo -e "${Green}Build completed successfully.${Color_Off}"
fi

# Exit script after executing commands
exit 0
