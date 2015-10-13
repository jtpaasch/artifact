# -*- coding: utf-8 -*-

"""A module to handle Security Groups."""

from artifact.client.utils import get_client


def create_security_group(name, vpc_id):
    """Create a security group."""
    client = get_client("ec2")
    response = client.create_security_group(
        GroupName=name,
        Description=name + " - " + vpc_id,
        VpcId=vpc_id)
    return response


def get_security_groups():
    """Get info about all security groups."""
    client = get_client("ec2")
    response = client.describe_security_groups()
    return response


def delete_security_group(group_id):
    """Delete a security group."""
    client = get_client("ec2")
    response = client.delete_security_group(GroupId=group_id)
    return response


def add_inbound_rule_to_security_group(group_id, protocol, port, cidr_block):
    """Add a rule for inbound traffic to a security group."""
    client = get_client("ec2")
    response = client.authorize_security_group_ingress(
        GroupId=group_id,
        IpProtocol=protocol,
        FromPort=port,
        ToPort=port,
        CidrIp=cidr_block)
    return response


def add_outbound_rule_to_security_group(group_id, protocol, port, cidr_block):
    """Add a rule for outbound traffic to a security group."""
    client = get_client("ec2")
    response = client.authorize_security_group_egress(
        GroupId=group_id,
        IpProtocol=protocol,
        FromPort=port,
        ToPort=port,
        CidrIp=cidr_block)
    return response
