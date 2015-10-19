# -*- coding: utf-8 -*-

"""A module to handle ECS (Elastic Container Service) resources."""

from artifact.client.utils import get_client


def create_cluster(name):
    """Create an ECS cluster."""
    client = get_client("ecs")
    params = {}
    params["ClusterName"] = name
    response = client.create_cluster(**params)
    return response


def delete_cluster(name):
    """Delete an ECS cluster."""
    client = get_client("ecs")
    params = {}
    params["cluster"] = name
    response = client.delete_cluster(**params)
    return response


def get_clusters():
    """Get info about all clusters."""
    client = get_client("ecs")
    response = client.describe_clusters()
    return response



