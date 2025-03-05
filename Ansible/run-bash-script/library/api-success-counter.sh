#!/bin/bash

# Define the log file path
log_file="/root/file.log"

# Initialize associative arrays to store counts
declare -A success_count total_count

# Read the log file line by line
while IFS= read -r line; do
    # Extract API endpoint and response code from each line
    api_endpoint=$(echo "$line" | awk '{print $2}')
    response_code=$(echo "$line" | awk '{print $3}')

    # Increment total count for the API endpoint
    ((total_count[$api_endpoint]++))

    # Check if response code is successful (status code 200)
    if [[ $response_code -eq 200 ]]; then
        # Increment success count for the API endpoint
        ((success_count[$api_endpoint]++))
    fi
done < "$log_file"

# Print the results
echo "API call | Count"
for api_endpoint in "${!total_count[@]}"; do
    total=${total_count[$api_endpoint]}
    success=${success_count[$api_endpoint]}
    echo "$api_endpoint | $success/$total"
done
