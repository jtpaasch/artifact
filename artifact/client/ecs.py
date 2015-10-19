# -*- coding: utf-8 -*-

"""A module to handle ECS (Elastic Container Service) resources."""

from artifact.client.utils import get_client


def create_cluster(name):
    """Create an ECS cluster."""
    client = get_client("ecs")
    params = {}
    params["clusterName"] = name
    response = client.create_cluster(**params)
    return response


def delete_cluster(name):
    """Delete an ECS cluster."""
    client = get_client("ecs")
    params = {}
    params["cluster"] = name
    response = client.delete_cluster(**params)
    return response


def get_cluster_arns():
    """Get a list of cluster ARNs."""
    result = []
    client = get_client("ecs")
    response = client.list_clusters()
    cluster_arns = response.get("clusterArns")
    if cluster_arns:
        result = ["default"] + cluster_arns
    return result


def get_clusters():
    """Get info about all clusters."""
    cluster_arns = get_cluster_arns()
    client = get_client("ecs")
    response = client.describe_clusters(clusters=cluster_arns)
    return response


def get_container_instance_arns(cluster):
    """Get a list of instance ARNs for a cluster."""
    result = []
    client = get_client("ecs")
    response = client.list_container_instances(cluster=cluster)
    instance_arns = response.get("containerInstanceArns")
    if instance_arns:
        result = instance_arns
    return result


def get_container_instances(cluster):
    """Get info about all instances in a cluster."""
    result = {}
    instance_arns = get_container_instance_arns(cluster=cluster)
    if instance_arns:
        client = get_client("ecs")
        result = client.describe_container_instances(
            cluster=cluster,
            containerInstances=instance_arns)
    return result



