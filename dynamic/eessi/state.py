"""
Classes for managing EESSI infrastructure
:author: Terje Kvernes (University of Oslo)
"""
import json

from eessi.tools import TERRAFORM_DIRECTORY

def lookup_value_by_list(attributes, list_of_keys, default=""):
    """
    Try to find the dictionary value of one of the keys in a given list,
    return the default value if none can be found in the given dictionary.
    """
    matching_keys = attributes.keys() & list_of_keys
    if matching_keys:
        return attributes[matching_keys.pop()]
    else:
        return default

def state(nodes, filename=None):
    """
    Returns a dict of the current terraform state.
    """
    statefile = '{}/terraform.tfstate'.format(TERRAFORM_DIRECTORY)
    if filename:
        statefile = filename

    status_dict = {}

    try:
        with open(statefile, 'r') as file:
            status_dict = json.loads(file.read())

            # if we get nodes passed to us, populate the nodes with data from state.
            for node in nodes:
                arch = node.arch

                for resource in status_dict['resources']:
                    if resource['mode'] == 'managed':
                        if resource['name'] == 'infra-{}'.format(arch):
                            instance = resource['instances'][0]
                            attributes = instance['attributes']

                            node.instance_type = lookup_value_by_list(attributes, ['flavor_name', 'instance_type'])
                            node.public_dns = lookup_value_by_list(attributes, ['public_dns', 'access_ip_v4'])
                            node.public_ipv4 = lookup_value_by_list(attributes, ['access_ip_v4', 'public_ip'])
                            node.public_ipv6 = lookup_value_by_list(attributes, ['access_ip_v6', 'public_ipv6'])
    except FileNotFoundError:
        pass

    return status_dict
