output "instance_id" {
  description = "EC2 instance ID"
  value       = module.app_vm.instance_id
}
 
output "private_ip" {
  value = module.app_vm.private_ip
}
 
output "security_group_id" {
  value = module.app_vm.security_group_id
}
