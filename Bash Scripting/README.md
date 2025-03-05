Bash scripting some essential commands and concepts.

### Conditionals:

- **If-else statement:**

   ```bash
   if [ condition ]; then
       # code to be executed if the condition is true
   else
       # code to be executed if the condition is false
   fi
   ```

- **Comparison Operators:**
   - `-eq`: Equal
   - `-ne`: Not equal
   - `-lt`: Less than
   - `-le`: Less than or equal
   - `-gt`: Greater than
   - `-ge`: Greater than or equal

### Loops:

- **For Loop:**

   ```bash
   for i in {1..5}; do
       # code to be executed
   done
   ```

- **While Loop:**

   ```bash
   while [ condition ]; do
       # code to be executed
   done
   ```

### Functions:

- **Defining a Function:**

   ```bash
   function my_function() {
       # code to be executed
   }
   ```

- **Calling a Function:**

   ```bash
   my_function
   ```

### File Operations:

- **Checking if a File Exists:**

   ```bash
   if [ -e "filename" ]; then
       # code to be executed
   fi
   ```

- **Checking if a Directory Exists:**

   ```bash
   if [ -d "directory" ]; then
       # code to be executed
   fi
   ```

- **File Permissions:**

   ```bash
   chmod +x script.sh  # Make script executable
   ```

### Special Variables:

- **Positional Parameters:**

   - `$0`: Script name
   - `$1`, `$2`, ...: First argument, second argument, etc.

- **Special Variables:**

   - `$$`: Process ID of the current script
   - `$?`: Exit status of the last command

### Example Script:

```bash
#!/bin/bash

# This is a simple bash script

name="John"

echo "Hello, $name!"

read -p "Enter a number: " num

if [ $num -gt 10 ]; then
    echo "The number is greater than 10."
else
    echo "The number is 10 or less."
fi

for i in {1..5}; do
    echo "Iteration $i"
done
```

### Log Rotation

Log rotation is a common task in system administration to manage log files efficiently. Log rotation helps prevent log files from becoming too large and consuming excessive disk space. Below is a simple Bash script for log rotation automation. This script rotates logs by compressing and archiving old log files.

```bash
#!/bin/bash

# Log rotation script

LOG_DIR="/var/log/myapp"
ROTATE_DAYS=7
DATE_FORMAT="%Y%m%d"

# Check if the log directory exists
if [ ! -d "$LOG_DIR" ]; then
    echo "Error: Log directory does not exist."
    exit 1
fi

# Change to the log directory
cd "$LOG_DIR" || exit 1

# Find and rotate old log files
find . -name "*.log" -type f -mtime +$ROTATE_DAYS -exec sh -c '
    for file do
        # Compress and archive the log file
        gzip -9 "$file"

        # Append the current date to the archived file
        mv "$file.gz" "${file%.log}.$(date +'$DATE_FORMAT').log.gz"

        # Create a new empty log file
        touch "$file"
    done
' sh {} +

echo "Log rotation completed successfully."
```

Save this script, for example, as `log_rotation.sh`. Make it executable with:

```bash
chmod +x log_rotation.sh
```

You may want to schedule this script to run periodically using a tool like cron. For example, to run the script every day, you can add the following line to your crontab:

```bash
0 0 * * * /path/to/log_rotation.sh
```

This script performs the following actions:

1. It checks if the log directory exists.
2. It changes to the log directory.
3. It finds log files older than the specified rotation period and compresses, archives, and renames them.
4. It creates new empty log files to continue logging.

Make sure to customize the `LOG_DIR`, `ROTATE_DAYS`, and `DATE_FORMAT` variables according to your needs. Adjust the cron schedule based on your desired rotation frequency.
