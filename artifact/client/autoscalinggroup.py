# -*- coding: utf-8 -*-

"""A module to handle auto scaling groups."""

from deploy.client.utils import get_client


def create_auto_scaling_group(
        name,
        launch_configuration,
        min_size,
        max_size,
        desired_size=None,
        subnets=None):
    """Create an auto scaling group."""
    client = get_client("autoscaling")
    params = {}
    params["AutoScalingGroupName"] = name
    params["LaunchConfigurationName"] = launch_configuration
    params["MinSize"] = min_size
    params["MaxSize"] = max_size
    if not desired_size:
        desired_size = min_size
    params["DesiredCapacity"] = desired_size
    if subnets:
        params["VPCZoneIdentifier"] = ",".join(subnets)
    response = client.create_auto_scaling_group(**params)
    return response


def get_auto_scaling_groups():
    """Get info about all auto scaling groups."""
    client = get_client("autoscaling")
    response = client.describe_auto_scaling_groups()
    return response


def delete_auto_scaling_group(name, force_delete=True):
    """Delete an auto scaling group."""
    client = get_client("autoscaling")
    response = client.delete_auto_scaling_group(
        AutoScalingGroupName=name,
        ForceDelete=True)
    return response


def attach_elastic_load_balancer(
        auto_scaling_group_name,
        elastic_load_balancer_names):
    """Attach one or more load balancers to an auto scaling group."""
    client = get_client("autoscaling")
    response = client.attach_load_balancers(
        AutoScalingGroupName=auto_scaling_group_name,
        LoadBalancerNames=elastic_load_balancer_names)
    return response


def detach_elastic_load_balancer(
        auto_scaling_group_name,
        elastic_load_balancer_names):
    """Detach one or more load balancers from an auto scaling group."""
    client = get_client("autoscaling")
    response = client.detach_load_balancers(
        AutoScalingGroupName=auto_scaling_group_name,
        LoadBalancerNames=elastic_load_balancer_names)
    return response
