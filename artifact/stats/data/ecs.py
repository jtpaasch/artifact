# -*- coding: utf-8 -*-

"""A module to fetch stats about ECS."""

from artifact.client import ecs


def get_clusters():
    """Get data about ECS clusters."""
    data = ecs.get_clusters()
    clusters = data.get("clusters")
    return clusters


def get_container_instances():
    """Get data about ECS container instances."""
    result = []
    clusters = get_clusters()
    for cluster in clusters:
        cluster_name = cluster.get("clusterName")
        if cluster_name:
            instance_data = ecs.get_container_instances(cluster_name)
            instances = instance_data.get("containerInstances")
            if instances:
                for instance in instances:
                    instance["clusterName"] = cluster_name
                result += instances
    return result


def get_services():
    """Get data about ECS services."""
    return []


def get_tasks():
    """Get data about ECS tasks."""
    result = []
    tasks = ecs.get_tasks()
    if tasks:
        result = tasks
    return result


def get_task_definitions():
    """Get data about ECS task definitions."""
    result = []
    response = ecs.get_task_definitions()
    if response:
        result = response
    return result


def get_services():
    """Get data about ECS services."""
    result = []
    response = ecs.get_services()
    if response:
        result = response
    return result
