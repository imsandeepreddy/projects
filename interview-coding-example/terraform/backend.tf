# [PROD] Values supplied at init time via -backend-config flags
# so the same file works for every environment
terraform {
  backend "s3" {
    # terraform init \
    #   -backend-config="bucket=my-tfstate-bucket" \
    #   -backend-config="key=envs/dev/terraform.tfstate" \
    #   -backend-config="region=ap-south-1"
 
    encrypt        = true                        # [PROD] Encrypt state at rest
    dynamodb_table = "terraform-state-lock"      # [PROD] State locking table - legacy but still valid
    #use_lockfile   = true                # No State locking table - recent change from terraform 1.10+
  }
}
