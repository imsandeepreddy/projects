module "app_vm" {
  source = "../../modules/vm"
 
  vm_name          = "app-server-${var.environment}"
  ami_id           = var.ami_id
  instance_type    = var.instance_type
  subnet_id        = var.subnet_id          # single subnet inside the VPC
  vpc_id           = var.vpc_id
  key_name         = var.key_name
  root_volume_size = var.root_volume_size
  environment      = var.environment
  additional_tags  = var.additional_tags
 
  ingress_rules = [
    {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = [var.ssh_cidr]  # [PROD] restrict to VPN/bastion CIDR
      description = "SSH from VPN"
    },
    {
      from_port   = 8080
      to_port     = 8080
      protocol    = "tcp"
      cidr_blocks = ["10.0.0.0/8"]  # internal traffic only
      description = "App port from internal network"
    },
  ]
}
