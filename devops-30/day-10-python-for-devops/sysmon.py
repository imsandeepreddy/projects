import subprocess
import os
from pathlib import Path
from datetime import datetime

def get_disk_usage(path="/"):
    # use subprocess to call df -h
    disk_usage_result = subprocess.run(["df", "-h"], capture_output=True, text=True)
    return disk_usage_result

def get_top_processes(n=5):
    # use subprocess to call ps aux --sort=-%cpu
    top_process_result = subprocess.run(["ps", "aux", "--sort=-%cpu"], capture_output=True, text=True)
    lines = top_process_result.stdout.strip().split("\n")
    header = lines[0]
    top_n_processes = lines[1:n+1]
    
    return [header] + top_n_processes

def find_large_files(directory, min_size_mb=50):
    # use pathlib.Path.rglob to walk directory
    # filter by stat().st_size
    ...

def write_report(output_dir="/tmp/sysmon"):
    # use pathlib to create dir if not exists
    # write timestamped report file
    ...

if __name__ == "__main__":
    write_report()