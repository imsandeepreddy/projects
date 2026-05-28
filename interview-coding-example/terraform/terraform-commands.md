# Project structure
```bash
project/
├── modules/           # Reusable modules (ec2, rds, vpc...)
│   ├── vm/
│   │   ├── main.tf
│   │   └── variables.tf
│   │   └── output.tf
├── envs/
│   ├── dev/
│   │   ├── main.tf
│   │   └── variables.tf
│   │   └── output.tf
│   │   └── terraform.tfvars
│   └── prod/
│       ├── main.tf
│       └── terraform.tfvars
├── backend.tf         # Remote state config
└── provider.tf        # Provider version locks
```

# 1. Move into the environment folder
cd envs/dev
 
# 2. Initialize — pass env-specific backend config
terraform init \
  -backend-config="bucket=my-company-tfstate" \
  -backend-config="key=envs/dev/terraform.tfstate" \
  -backend-config="region=ap-south-1"
 
# 3. Preview changes
terraform plan -out=tfplan
 
# 4. Apply
terraform apply tfplan
 
# 5. Verify outputs
terraform output
 
# [GOTCHA] Never run destroy on prod without -target flag + approval gate
terraform destroy  # dev only

# ______count_____________________________________________________
variable "instance_count" {
  type    = number
  default = 3
}

resource "aws_instance" "server" {
  count         = var.instance_count
  ami           = "ami-12345"
  instance_type = "t2.micro"

  tags = {
    Name = "Server-${count.index}" # Server-0, Server-1, Server-2
  }
}
# If you have 3 servers and delete the middle one (Server-1), Terraform will rename Server-2 to Server-1 to fill the gap. This can cause unnecessary re-creations of resources that didn't actually change.

# _______for_each - example 1_____________________________________________________
variable "instances" {
  type = map(any)
  default = {
    "web" = "t2.micro"
    "api" = "t3.small"
    "db"  = "t3.medium"
  }
}

resource "aws_instance" "server" {
  for_each      = var.instances
  ami           = "ami-12345"
  instance_type = each.value # Takes the value (e.g., t2.micro)

  tags = {
    Name = each.key # Takes the key (e.g., "web")
  }
}

# _______for_each - example 2_____________________________________________________
variable "server_names" {
  type    = list(string)
  default = ["web", "api", "db"]
}

resource "aws_instance" "server" {
  # Convert the list to a set to satisfy for_each
  for_each = toset(var.server_names)

  ami           = "ami-12345678"
  instance_type = "t3.micro"

  tags = {
    # each.key and each.value are the same when using a set
    Name = each.value 
  }
}


