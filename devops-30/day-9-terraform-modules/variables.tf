variable "app_name" {
    description = "Name of the application"
    type = string
    validation {
        condition = length(var.app_name) > 2
        error_message = "app_name must be atleast 3 characters"
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