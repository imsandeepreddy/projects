output "config_file_path" {
    description = "Path of generated config file"
    value = local_file.app_config.filename
}
output "environment" {
    description = "Current deployment environment"
    value = var.environment
}