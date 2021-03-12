data "openstack_images_image_v2" "ppc64le" {
  name        = "CentOS 8.3 LE"
  most_recent = true
}
