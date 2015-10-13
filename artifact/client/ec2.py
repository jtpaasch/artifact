# -*- coding: utf-8 -*-

"""A module to handle EC2 instances."""

from deploy.client.utils import get_client


def create_instance(
        ami_id,
        security_group_id,
        key_name=None,
        instance_type="t2.micro"):
    """Create an EC2 instance."""
    client = get_client("ec2")
    response = client.run_instances(
        ImageId=ami_id,
        MinCount=1,
        MaxCount=1,
        KeyName=key_name,
        SecurityGroupIds=[security_group_id],
        InstanceType=instance_type)
    return response


def get_instances():
    """Get info about all instances."""
    client = get_client("ec2")
    response = client.describe_instances()
    return response


def delete_instance(instance_id):
    """Delete an EC2 instance."""
    client = get_client("ec2")
    response = client.terminate_instances(InstanceIds=[instance_id])
    return response
