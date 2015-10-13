# -*- coding: utf-8 -*-

"""A module to handle elastic load balancers."""

from artifact.client.utils import get_client


def create_elastic_load_balancer(
        name,
        listeners,
        availability_zones=None,
        subnets=None,
        security_groups=None):
    """Create an elastic load balancer."""
    client = get_client("elb")
    params = {}
    params["LoadBalancerName"] = name
    params["Listeners"] = listeners
    if availability_zones:
        params["AvailabilityZones"] = availability_zones
    if subnets:
        params["Subnets"] = subnets
    if security_groups:
        params["SecurityGroups"] = security_groups
    response = client.create_load_balancer(**params)
    return response


def get_elastic_load_balancers():
    """Get info about all elastic load balancers."""
    client = get_client("elb")
    response = client.describe_load_balancers()
    return response


def delete_elastic_load_balancer(name):
    """Delete an elastic load balancer."""
    client = get_client("elb")
    response = client.delete_load_balancer(
        LoadBalancerName=name)
    return response
