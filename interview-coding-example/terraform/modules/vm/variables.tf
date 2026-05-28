variable "vm_name" {
  description = "Name tag for the EC2 instance"
  type        = string
}
 
variable "ami_id" {
  description = "AMI ID (region-specific, use data source or SSM)"
  type        = string
}
 
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}
 
variable "subnet_id" {
  description = "Subnet ID inside the target VPC"
  type        = string
}
 
variable "vpc_id" {
  description = "VPC ID — used to scope the security group"
  type        = string
}
 
variable "key_name" {
  description = "EC2 Key Pair for SSH access (null disables SSH)"
  type        = string
  default     = null
}
 
variable "root_volume_size" {
  description = "Root EBS volume size in GiB"
  type        = number
  default     = 20
}
 
variable "environment" {
  description = "Environment label (dev / staging / prod)"
  type        = string
}
 
variable "additional_tags" {
  description = "Extra tags merged onto every resource"
  type        = map(string)
  default     = {}
}
 
variable "ingress_rules" {
  description = "List of inbound security group rules"
  type = list(object({
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
    description = string
  }))
  default = []
}
