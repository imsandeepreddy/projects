# (DO NOT COMMIT to Git if it has secrets)
aws_region          = "ap-south-1"
deployment_role_arn = "arn:aws:iam::111122223333:role/TerraformDeployRole-Dev"
environment         = "dev"
 
# Get latest Amazon Linux 2023 AMI:
# aws ec2 describe-images --owners amazon \
#   --filters "Name=name,Values=al2023-ami-*-x86_64" \
#   --query "sort_by(Images,&CreationDate)[-1].ImageId"
ami_id           = "ami-0f58b397bc5c1f2e8"
instance_type    = "t3.micro"
 
vpc_id    = "vpc-0abc12345def67890"
subnet_id = "subnet-0abc12345def67890"  # single subnet for VMs
key_name  = "dev-keypair"
 
root_volume_size = 20
ssh_cidr         = "10.10.0.0/16"   # VPN CIDR
 
additional_tags = {
  CostCenter = "engineering"
  Owner      = "platform-team"
}
