#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import boto3

def provision_ec2(instance_type, image_id, key_name):
    ec2 = boto3.client('ec2')
    response = ec2.run_instances(
        InstanceType=instance_type,
        ImageId=image_id,
        KeyName=key_name,
        MinCount=1,
        MaxCount=1
    )
    instance_id = response['Instances'][0]['InstanceId']
    return instance_id

def terminate_ec2(instance_id):
    ec2 = boto3.client('ec2')
    ec2.terminate_instances(InstanceIds=[instance_id])

def main():
    module_args = dict(
        instance_type=dict(type='str', required=True),
        image_id=dict(type='str', required=True),
        key_name=dict(type='str', required=True),
        state=dict(type='str', required=True, choices=['present', 'absent'])
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    instance_type = module.params['instance_type']
    image_id = module.params['image_id']
    key_name = module.params['key_name']
    state = module.params['state']

    changed = False

    if state == 'present':
        instance_id = provision_ec2(instance_type, image_id, key_name)
        changed = True
        module.exit_json(changed=changed, instance_id=instance_id)
    elif state == 'absent':
        # Code to terminate EC2 instance
        instance_id = 'i-1234567890'  # Dummy instance ID for demonstration
        terminate_ec2(instance_id)
        changed = True
        module.exit_json(changed=changed, instance_id=instance_id)

if __name__ == '__main__':
    main()
