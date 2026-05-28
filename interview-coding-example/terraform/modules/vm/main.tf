# ── Security Group ───────────────────────────────────────────────────
resource "aws_security_group" "this" {
  name        = "${var.vm_name}-sg"
  description = "Security group for ${var.vm_name}"
  vpc_id      = var.vpc_id
 
  # Dynamic ingress — driven by var.ingress_rules list
  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
      description = ingress.value.description
    }
  }
 
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"          # all traffic
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound"
  }
 
  tags = merge(
    { Name = "${var.vm_name}-sg", Environment = var.environment },
    var.additional_tags
  )
}
 
# ── EC2 Instance ─────────────────────────────────────────────────────
resource "aws_instance" "this" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  subnet_id              = var.subnet_id
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.this.id]
 
  root_block_device {
    volume_size           = var.root_volume_size
    volume_type           = "gp3"            # [PROD] gp3 cheaper + faster than gp2
    delete_on_termination = true
    encrypted             = true             # [PROD] always encrypt at rest
  }
 
  metadata_options {
    http_tokens = "required"                 # [PROD] IMDSv2 prevents SSRF attacks
  }
 
  tags = merge(
    { Name = var.vm_name, Environment = var.environment },
    var.additional_tags
  )
 
  lifecycle {
    # [PROD] Uncomment to block accidental destroy in prod
    # prevent_destroy = true
    # ignore_changes  = [ami]  # if AMI managed externally by Packer
  }
}
