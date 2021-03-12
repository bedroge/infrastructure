resource "openstack_compute_instance_v2" "infra-ppc64le" {
  name            = "eessi-ppc64le"
  image_id        = "1629a150-4dff-4be3-97b7-01c5ec21f01f" # CentOS 8.3 LE
  flavor_name     = var.instance_ppc64le[var.mode]
  security_groups = [openstack_networking_secgroup_v2.instance.id]
  key_pair        = "${var.localuser}-deployer-key"
  count           = var.create_ppc64le ? 1 : 0

  #block_device {
  #  volume_size = 30
  #}

  network {
    name = "public"
  }

  metadata = {
    Owner = var.localuser
    Name = "eessi-ppc64le"
  }
}
