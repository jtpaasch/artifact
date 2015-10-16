# -*- coding: utf-8 -*-

"""A module to handle launch configurations (for auto scaling groups)."""

from artifact.client.utils import get_client
from artifact.client.utils import get_file_contents


def create_launch_configuration(
        name,
        ami_id,
        key_name=None,
        security_groups=None,
        instance_type="t2.micro",
        public_ip=False,
        role_profile=None,
        user_data=None,
        user_data_file=None):
    """Create a launch configuration."""
    client = get_client("autoscaling")
    params = {}
    params["LaunchConfigurationName"] = name
    params["ImageId"] = ami_id
    if key_name:
        params["KeyName"] = key_name
    if security_groups:
        params["SecurityGroups"] = security_groups
    params["InstanceType"] = instance_type
    params["InstanceMonitoring"] = {"Enabled": False}
    if role_profile:
        params["IamInstanceProfile"] = role_profile
    params["AssociatePublicIpAddress"] = public_ip
    if user_data:
        params["UserData"] = user_data
    elif user_data_file:
        params["UserData"] = get_file_contents(user_data_file)
    response = client.create_launch_configuration(**params)
    return response


def get_launch_configurations():
    """Get info about all launch configurations."""
    client = get_client("autoscaling")
    response = client.describe_launch_configurations()
    return response


def delete_launch_configuration(name):
    """Delete a launch configuration."""
    client = get_client("autoscaling")
    response = client.delete_launch_configuration(
        LaunchConfigurationName=name)
    return response
