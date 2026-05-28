variable "aws_region" {
  type    = string
  default = "ap-south-1"
}
 
variable "deployment_role_arn" {
  description = "IAM role assumed by Terraform during deployment"
  type        = string
}
 
variable "environment" {
  type    = string
  default = "dev"
}
 
variable "ami_id" {
  description = "Amazon Linux 2023 AMI for ap-south-1"
  type        = string
}
 
variable "instance_type" {
  type    = string
  default = "t3.micro"
}
 
variable "vpc_id" {
  description = "Target VPC for the VM"
  type        = string
}
 
variable "subnet_id" {
  description = "Single subnet inside the VPC where VM will launch"
  type        = string
}
 
variable "key_name" {
  type    = string
  default = null
}
 
variable "root_volume_size" {
  type    = number
  default = 20
}
 
variable "ssh_cidr" {
  description = "CIDR allowed for SSH access"
  type        = string
  default     = "10.0.0.0/8"
}
 
variable "additional_tags" {
  type    = map(string)
  default = {}
}
