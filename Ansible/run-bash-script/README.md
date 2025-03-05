# Automation with Ansible and Bash Scripting
This repository contains a Bash script and an Ansible playbook to automate the counting of API calls from a log file. This README provides an overview of the script, playbook, and how to use them for automation purposes.

## Bash Script (api-success-counter.sh)
The Bash script api-success-counter.sh reads a log file containing API call records, extracts the API endpoints and response codes, and calculates the counts of successful and total calls for each endpoint. It then prints the results in the format API endpoint | Success Count/Total Count.

## Usage:
Copy the Bash script (api-success-counter.sh) to your desired location.
Ensure you have a log file (file.log) containing API call records.
Update the log_file variable in the script to point to the correct path of your log file.
Execute the script using ./api-success-counter.sh.
Ansible Playbook (playbook.yml)
The Ansible playbook playbook.yml automates the process of copying the log file and the Bash script to remote hosts, executing the Bash script on the remote hosts, and capturing the output.

## Usage:
Update the source and destination paths in the ansible.builtin.copy tasks to match your environment.
Ensure you have Ansible installed on your local machine.
Execute the playbook using ansible-playbook playbook.yml.

# Theory
## Ansible:
Ansible is an open-source automation tool that automates the provisioning, configuration management, and application deployment of IT infrastructure. It uses simple YAML-based playbooks to define automation tasks and relies on SSH for communication with remote hosts. Ansible provides a powerful and agentless approach to automation, making it easy to scale and manage infrastructure.

## Bash Scripting:
Bash (Bourne Again Shell) is a command-line interpreter for Unix-like operating systems. It is a scripting language that allows users to automate tasks, manipulate files and directories, and execute commands. Bash scripts can be used for various automation purposes, such as system administration, file processing, and application deployment.

## Automation with Ansible and Bash Scripting:
Ansible provides a high-level orchestration framework for automating complex tasks and workflows across multiple hosts.
Bash scripting complements Ansible by providing a flexible and powerful way to execute commands and perform tasks on individual hosts or within Ansible playbooks.
Together, Ansible and Bash scripting enable organizations to automate infrastructure provisioning, configuration management, and application deployment efficiently and reliably.

Author
[Sandeep Reddy]

License
This project is licensed under the MIT License.
