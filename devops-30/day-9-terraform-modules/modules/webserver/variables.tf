variable "app_name" { 
    type = string
    default = "sandeep_app"
}
variable "environment"   { 
    type = string
    default = "dev" 
}
variable "port" {
  description = "Application port"
  type        = number
  default     = 5000
}