# -*- coding: utf-8 -*-

"""A module to handle VPCs."""

from deploy.client.utils import get_client


def create_vpc(cidr_block):
    """Create a VPC."""
    client = get_client("ec2")
    response = client.create_vpc(CidrBlock=cidr_block)
    return response


def get_vpcs():
    """Get info about all VPCs."""
    client = get_client("ec2")
    response = client.describe_vpcs()
    return response


def delete_vpc(vpc_id):
    """Delete a VPC."""
    client = get_client("ec2")
    response = client.delete_vpc(VpcId=vpc_id)
    return response


def tag_vpc(vpc_id, tag, value):
    """Add a tag to a VPC."""
    client = get_client("ec2")
    response = client.create_tags(
        Resources=[vpc_id],
        Tags=[{"Key": tag, "Value": value}])
    return response
