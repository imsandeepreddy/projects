## Ansible Custom Module: AWS EC2 Provisioner
This repository contains an Ansible custom module (aws_ec2.py) for provisioning and terminating AWS EC2 instances. The module leverages the boto3 library to interact with the AWS EC2 API.

### Custom Module (aws_ec2.py)
The aws_ec2.py script provides two main functions:

provision_ec2(instance_type, image_id, key_name): Provisions a new EC2 instance with the specified instance type, AMI ID, and key pair name. Returns the instance ID of the newly provisioned instance.
terminate_ec2(instance_id): Terminates an existing EC2 instance with the specified instance ID.
Usage:
To use the aws_ec2.py module, follow these steps:

Copy the aws_ec2.py script to your Ansible playbook directory.
Use the aws_ec2 module in your playbook YAML file (playbook.yml) to provision or terminate EC2 instances. Here's an example:
```yaml
---
- name: Provision EC2 Instance
  hosts: localhost
  tasks:
    - name: Provision EC2 instance
      aws_ec2:
        instance_type: t2.micro
        image_id: ami-1234567890abcdef0
        key_name: my-key
        state: present
      register: ec2_result

    - debug:
        var: ec2_result
```
This playbook provisions a new EC2 instance with the specified parameters and registers the result in the ec2_result variable.
Run the playbook using the ansible-playbook command.

License
This project is licensed under the MIT License.
