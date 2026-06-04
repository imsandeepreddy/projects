---
type: code
tags: 
  - terraform
---

## Day 8 — DevOps: Terraform Basics

1. **Understand the mental model before touching code:**
   - Terraform is **declarative** — you describe the desired end state, not the steps to get there
   - Core workflow: `write → init → plan → apply → destroy`
   - **State file** is Terraform's memory — it maps your config to real infrastructure
   - Never edit the state file manually — ever

2. **Install Terraform and set up a provider:**
   - Install via your package manager or [tfenv](https://github.com/tfutils/tfenv) (version manager — preferred)
   - Use **AWS free tier** or **local provider** if you have no cloud account:
     ```bash
     # Verify install
     terraform version
     ```
   - Create your project folder:
     ```
     terraform-basics/
     ├── main.tf
     ├── variables.tf
     ├── outputs.tf
     └── terraform.tfvars
     ```

3. **Write your first `main.tf`** — use local provider to avoid cloud costs if needed:

   **Option A — Local provider (no cloud needed):**
   ```hcl
   terraform {
     required_providers {
       local = {
         source  = "hashicorp/local"
         version = "~> 2.4"
       }
     }
   }

   resource "local_file" "app_config" {
     filename = "${path.module}/output/config.json"
     content  = jsonencode({
       app_name    = var.app_name
       environment = var.environment
       port        = var.port
     })
   }
   ```

   **Option B — AWS provider (if you have an account):**
   ```hcl
   terraform {
     required_providers {
       aws = {
         source  = "hashicorp/aws"
         version = "~> 5.0"
       }
     }
   }

   provider "aws" {
     region = var.region
   }

   resource "aws_s3_bucket" "app_bucket" {
     bucket = "${var.app_name}-${var.environment}-bucket"
     tags = {
       Environment = var.environment
       ManagedBy   = "terraform"
     }
   }
   ```

4. **Write `variables.tf`** — never hardcode values in `main.tf`:
   ```hcl
   variable "app_name" {
     description = "Name of the application"
     type        = string
     validation {
       condition     = length(var.app_name) > 2
       error_message = "app_name must be at least 3 characters"
     }
   }

   variable "environment" {
     description = "Deployment environment"
     type        = string
     default     = "staging"
     validation {
       condition     = contains(["staging", "prod"], var.environment)
       error_message = "environment must be staging or prod"
     }
   }

   variable "port" {
     description = "Application port"
     type        = number
     default     = 8080
   }
   ```
   - Note the `validation` blocks — always validate inputs, don't trust callers

5. **Write `outputs.tf`** — expose values other configs or humans need:
   ```hcl
   output "config_file_path" {
     description = "Path to the generated config file"
     value       = local_file.app_config.filename
   }

   output "environment" {
     description = "Current deployment environment"
     value       = var.environment
   }
   ```

6. **Write `terraform.tfvars`** — your actual variable values:
   ```hcl
   app_name    = "myapp"
   environment = "staging"
   port        = 3000
   ```
   - Add `*.tfvars` to `.gitignore` if it contains secrets
   - Use `terraform.tfvars.example` committed to repo as a template

7. **Run the core workflow — understand each step deeply:**

   ```bash
   # Step 1 — download providers, initialise backend
   terraform init
   ```
   - Inspect `.terraform/` folder created — this is where provider binaries live
   - Never commit `.terraform/` — add to `.gitignore`

   ```bash
   # Step 2 — validate syntax
   terraform validate
   ```

   ```bash
   # Step 3 — preview what will change, nothing is created yet
   terraform plan
   ```
   - Read the plan output carefully: `+` create, `~` update, `-` destroy
   - A plan with unexpected destroys is a red flag — stop and investigate

   ```bash
   # Step 4 — apply the plan
   terraform apply
   ```
   - Type `yes` to confirm — in CI you'd use `-auto-approve`
   - Inspect `terraform.tfstate` — note it contains real resource IDs

   ```bash
   # Step 5 — inspect state
   terraform show
   terraform state list
   ```

8. **Understand the state file deeply:**
   - Open `terraform.tfstate` in an editor — read its structure
   - Run `terraform state show local_file.app_config` — see the full resource record
   - Manually delete your output file, then run `terraform plan` — Terraform detects drift and plans to recreate it
   - This is **drift detection** in action — it compares state to reality

9. **Make a change and observe plan behaviour:**
   - Change `port` in `terraform.tfvars` from `3000` to `4000`
   - Run `terraform plan` — observe it shows an in-place update `~` not a destroy
   - Change `app_name` — observe whether it forces a destroy + recreate vs update
   - Understanding which changes force replacement vs update is critical for production safety

10. **Add a `locals` block — computed values:**
    ```hcl
    locals {
      name_prefix = "${var.app_name}-${var.environment}"
      common_tags = {
        ManagedBy   = "terraform"
        Environment = var.environment
        UpdatedAt   = timestamp()
      }
    }
    ```
    - Use `local.name_prefix` in your resource names
    - Locals reduce repetition and make refactoring easier

11. **Add a `data` source — read existing infrastructure:**
    ```hcl
    # Read an existing resource without managing it
    data "local_file" "existing_config" {
      filename = "${path.module}/existing.json"
    }

    output "existing_content" {
      value = data.local_file.existing_config.content
    }
    ```
    - Data sources are read-only — they query existing state
    - Critical distinction: `resource` manages, `data` only reads

12. **Destroy everything cleanly:**
    ```bash
    terraform destroy
    ```
    - Read the destroy plan before typing `yes`
    - Verify resources are actually gone after destroy completes
    - Note: state file still exists after destroy — it records that resources no longer exist

13. **Add a `.gitignore` for Terraform:**
    ```
    .terraform/
    .terraform.lock.hcl
    terraform.tfstate
    terraform.tfstate.backup
    *.tfvars
    ```
    - Commit only: `main.tf`, `variables.tf`, `outputs.tf`, `terraform.tfvars.example`

**Output:** Full `terraform-basics/` folder committed with all `.tf` files and a README explaining each file's purpose

---