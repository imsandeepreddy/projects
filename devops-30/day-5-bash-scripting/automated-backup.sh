#!/bin/bash

set -eou pipefail
#Accept source dir and destination dir as arguments
#Validate both exist
#Create a timestamped backup folder: backup_$(date +%Y%m%d_%H%M%S)
#Use rsync -av --progress to copy files
#Write a summary line to a backup.log file with timestamp + size of backup
#Set up a cron job entry (write it as a comment in the script): e.g. run daily at 2am

#Check number of ARGS
if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <SOURCE_DIR> <DESTINATION_DIR>"
    exit 1
fi

SOURCE_DIR="$1"
DESTINATION_DIR="$2"

#Validate the argument exists, print usage and exit with code 1 if not
if [[ -d "$SOURCE_DIR" ]]; then
    echo "Source directory validated"
else
    echo "Error: Directory '$SOURCE_DIR' does not exist."
    exit 1
fi

if [[ -d "$DESTINATION_DIR" ]]; then
    echo "Destination directory validated"
else
    echo "Error: Directory '$DESTINATION_DIR' does not exist."
    exit 1
fi

echo "Creating backup folder '$DESTINATION_DIR/backup_$(date +%Y%m%d)'"
mkdir "$DESTINATION_DIR/backup_$(date +%Y%m%d)"

check_errors(){
    #Loop through all .log files in the directory
    #Count lines containing ERROR and WARN using grep -c
    #If ERROR count exceeds a threshold, print an alert message
    while IFS= read -r -d '' log_file; do
        error_count=$(grep -c "ERROR" "$log_file")
        if [[ $error_count -gt $threshold ]]; then
            echo "[ALERT] ERRORs ($error_count) are more than $threshold in '$log_file'"
        fi
    done < <(find "$directory_path" -type f -name "*.log" -print0)
}

#check_errors

archive_old_logs(){
    #Archive logs older than 7 days using find . -mtime +7 and move them to an archive/ folder
    local dir="$directory_path"

    # Create the archive folder safely
    mkdir -p "$dir/archive"

    # Run the loop
    while IFS= read -r -d '' log_file; do
        
        # Move the file and print confirmation
        mv "$log_file" "$dir/archive/"
        echo "[ARCHIVED] Moved: $(basename "$log_file")"

    done < <(find "$dir" -type f -name "*.log" -mmin +30 -print0)
}

#archive_old_logs







