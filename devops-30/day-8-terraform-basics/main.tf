terraform {
    required_providers {
        local = {
            source = "hashicorp/local"
            version = "~> 2.4"
        }
    }
}

locals {
      name_prefix = "${var.app_name}-${var.environment}"
      common_tags = {
        ManagedBy   = "terraform"
        Environment = var.environment
        UpdatedAt   = timestamp()
      }
}

# Read an existing resource without managing it
data "local_file" "existing_config" {
    filename = "${path.module}/existing.json"
}

output "existing_content" {
    value = data.local_file.existing_config.content
}

resource "local_file" "app_config" {
    filename = "${path.module}/output/${local.name_prefix}-config.json"
    content = jsonencode({
        app_name = var.app_name
        environment = var.environment
        port = var.port
    })
}