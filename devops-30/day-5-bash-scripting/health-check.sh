#!/bin/bash
#Accept a URL as $1 and max retries as $2
#Use a while loop with a counter
#Hit the URL with curl -sf — check the exit code
#If successful print green status, if all retries fail print red and exit 1
#Add a sleep 5 between retries
#Use a trap to catch CTRL+C and print a clean exit message

# Define color codes for output
GREEN='\e[0;32m'
RED='\e[0;31m'
NC='\e[0m' # No Color

# Trap CTRL+C (SIGINT) and execute a clean exit function
clean_exit() {
    echo -e "\n${RED}[!] Script interrupted by user. Exiting cleanly.${NC}"
    exit 130
}

trap clean_exit SIGINT

if [[ $# -le 2 ]]; then
    echo "Usage: $0 <URL> <RETRIES>"
fi

URL=$1
MAX_RETRIES=$2

count=1

while [[ count -le $MAX_RETRIES ]]; do
    echo "Attempt $count of $MAX_RETRIES: Fetching $URL..."
    
    # Temporarily allow non-zero exit codes for the curl check
    set +e
    curl -sf "$1" >> /dev/null
    exit_code=$?
    set -e

    if [[ $exit_code -eq 0 ]]; then
        echo -e "${GREEN}[SUCCESS] Status code 200 OK${NC}"
        exit 0
    fi

    # Only sleep and increment if we haven't hit the max limit yet
    if [[ $count -lt $MAX_RETRIES ]]; then
        sleep 5
    fi

    ((count++))
done

# If the loop finishes, it means all retries were exhausted
echo -e "${RED}[ERROR] All $MAX_RETRIES retries failed.${NC}"
exit 1
