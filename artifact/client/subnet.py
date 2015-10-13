# -*- coding: utf-8 -*-

"""A module to handle subnets."""

from artifact.client.utils import get_client


def create_subnet(vpc_id, cidr_block):
    """Create a subnet in a VPC."""
    client = get_client("ec2")
    response = client.create_subnet(VpcId=vpc_id, CidrBlock=cidr_block)
    return response


def get_subnets():
    """Get info about all subnets."""
    client = get_client("ec2")
    response = client.describe_subnets()
    return response


def delete_vpc(subnet_id):
    """Delete a subnet."""
    client = get_client("ec2")
    response = client.delete_subnet(SubnetId=subnet_id)
    return response


def tag_subnet(subnet_id, tag, value):
    """Add a tag to a Subnet."""
    client = get_client("ec2")
    response = client.create_tags(
        Resources=[subnet_id],
        Tags=[{"Key": tag, "Value": value}])
    return response
