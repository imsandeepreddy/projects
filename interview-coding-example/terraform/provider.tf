terraform {
  required_version = ">= 1.5.0"
 
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"  # allows 5.x, blocks 6.x
    }
  }
}
 
provider "aws" {
  region = var.aws_region
 
  # [PROD] Assume a least-privilege role per environment
  assume_role {
    role_arn = var.deployment_role_arn
  }
 
  # [PROD] Default tags applied to every resource automatically
  default_tags {
    tags = {
      ManagedBy   = "Terraform"
      Environment = var.environment
      Repository  = "your-org/infra-repo"
    }
  }
}
