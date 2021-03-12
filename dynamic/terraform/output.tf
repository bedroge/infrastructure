output "public_dns_x86_64" {
  value       = aws_instance.infra-x86_64.*.public_dns
}

output "public_dns_aarch64" {
  value       = aws_instance.infra-aarch64.*.public_dns
}

output "public_dns_ppc64le" {
  value       = var.create_ppc64le ? join("", openstack_compute_instance_v2.infra-ppc64le.*.access_ip_v4 ) : ""
}
