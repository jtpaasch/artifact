# -*- coding: utf-8 -*-

"""A module to handle EC2 instances."""

from artifact.client.utils import get_client
from artifact.client.utils import get_file_contents


def create_instance(
        ami_id,
        security_group_id,
        key_name=None,
        instance_type="t2.micro",
        user_data=None,
        user_data_file=None):
    """Create an EC2 instance."""
    client = get_client("ec2")
    params = {}
    params["ImageId"] = ami_id
    params["MinCount"] = 1
    params["MaxCount"] = 1
    params["SecurityGroupIds"] = [security_group_id]
    if key_name:
        params["KeyName"] = key_name
    params["InstanceType"] = instance_type
    if user_data:
        params["UserData"] = user_data
    elif user_data_file:
        params["UserData"] = get_file_contents(user_data_file)
    response = client.run_instances(**params)
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
