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
}

resource "local_file" "app_config" {
    filename = "${path.module}/output/${local.name_prefix}-config.json"
    content = jsonencode({
        app_name = var.app_name
        environment = var.environment
        port = var.port
    })
}