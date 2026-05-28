#!/usr/bin/env python3

#-------------Disk usage--------------#
#import shutil
#import smtplib
#
#def check_disk_usage():
#    print("Started checking disk usage")
#    total, used, free = shutil.disk_usage("./")
#    if (used/total) * 100 > 10:
#        print("Disk is 90 used")
#    else:
#        print("Disk usage is under limits")
#
#check_disk_usage()

#-------------Run shell inside python--------------#
#import subprocess
#
#print(subprocess.run(["df", "-h"], capture_output=True, text=True).stdout)

#-------------Parse json file--------------#
#import json
#
#with open("dataset.json", "r") as f:
#    json_data = json.load(f)
#
#for data in json_data:
#    print(data["task"])

#-------------Argparse--------------#
#import argparse
#
#parser = argparse.ArgumentParser()
#parser.add_argument("--service", default="ngnix", help="Provide service name")
#args = parser.parse_args()
#
#print("Service name:", args.service)
#
##-------------Restart a service--------------#
#import subprocess
#
#service = args.service
#status = subprocess.run(["systemctl", "is-active", service], capture_output=True, text=True)
#print(status)
#if "inactive" in status.stdout:
#    print("Restarting service")
#else:
#    print(f"{service} is up and running")

#-------------Production-Ready template--------------#
# Shebang already defined in line 1 so working on rest
import subprocess, os, logging, sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)


def main():
    log.info("Starting...")
    #------------------Actual code logic is here-------------#
    service = "systemd-logind.service"
    status = subprocess.run(["systemctl", "is-active", service], capture_output=True, text=True)
    print(status)
    if "inactive" in status.stdout:
        print("Restarting service")
    else:
        print(f"{service} is up and running")
    #------------------Actual code logic is here-------------#

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        log.error(f"Fatal: {e}")
        sys.exit(1)