#!/usr/bin/env bash

set -eou pipefail
#Accept a directory path as an argument: $1
directory_path="$1"
threshold=1

#Validate the argument exists, print usage and exit with code 1 if not
if [[ -d "$directory_path" ]]; then
    cd "$directory_path" || exit 1
else
    echo "Error: Directory '$directory_path' does not exist."
    exit 1
fi

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

archive_old_logs







