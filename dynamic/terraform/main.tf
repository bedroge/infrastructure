provider "aws" {
  region = var.aws_region
}

resource "aws_key_pair" "deployer" {
  key_name = "${var.localuser}-deployer-key"
  public_key = file(var.keys["public"])
  tags = {
    Owner = var.localuser
  }
}

data "http" "icanhazip" {
  url = "http://ipv4.icanhazip.com"
}

resource "aws_security_group" "instance" {
  name = "${var.localuser}-eessi-security"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["${chomp(data.http.icanhazip.body)}/32"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group_rule" "instance_open_public" {
  security_group_id = aws_security_group.instance.id
  count     = var.is_public ? 1 : 0
  type      = "ingress"
  from_port = 22
  to_port   = 22
  cidr_blocks = ["0.0.0.0/0"]
  protocol  = "tcp"
}

terraform {
required_version = ">= 0.14.0"
  required_providers {
    openstack = {
      source  = "terraform-provider-openstack/openstack"
      version = "~> 1.35.0"
    }
  }
}

provider "openstack" {
}

resource "openstack_networking_secgroup_v2" "instance" {
  name = "${var.localuser}-eessi-security"
}

resource "openstack_networking_secgroup_rule_v2" "instance_open_public" {
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = 22
  port_range_max    = 22
  remote_ip_prefix  = "0.0.0.0/0"
  #security_group_id = "${openstack_networking_secgroup_v2.instance.id}"
  security_group_id = openstack_networking_secgroup_v2.instance.id
}

resource "openstack_compute_keypair_v2" "deployer" {
  name       = "${var.localuser}-deployer-key"
  public_key = file(var.keys["public"])
}
