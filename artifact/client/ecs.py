# -*- coding: utf-8 -*-

"""A module to handle ECS (Elastic Container Service) resources."""

from botocore.exceptions import WaiterError

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


def create_task_definition(family, containers, volumes):
    """Register a task definition."""
    client = get_client("ecs")
    params = {}
    params["family"] = family
    params["containerDefinitions"] = containers
    params["volumes"] = volumes
    response = client.register_task_definition(**params)
    return response


def get_task_definition_arns():
    """Get a list of task definition ARNs."""
    result = []
    client = get_client("ecs")
    response = client.list_task_definitions()
    task_definition_arns = response.get("taskDefinitionArns")
    if task_definition_arns:
        result = task_definition_arns
    return result


def get_task_definitions():
    """Get info about all task definitions."""
    result = []
    definition_arns = get_task_definition_arns()
    if definition_arns:
        client = get_client("ecs")
        for definition in definition_arns:
            response = client.describe_task_definition(
                taskDefinition=definition)
            if response:
                details = response.get("taskDefinition")
                if details:
                    result.append(details)
    return result


def delete_task_definition(family, revision):
    """Delete a task definition (family:version)."""
    client = get_client("ecs")
    task_definition_name = family + ":" + str(revision)
    response = client.deregister_task_definition(
        taskDefinition=task_definition_name)
    return response


def delete_task_definition_family(family):
    """Delete a whole family of task definition revisions."""
    names = []
    task_definitions = get_task_definitions()
    if task_definitions:
        for definition in task_definitions:
            family_prefix = definition.get("family")
            revision = definition.get("revision")
            if family_prefix == family:
                names.append((family, revision))
    for full_name in names:
        delete_task_definition(full_name[0], full_name[1])


def get_tasks():
    """Get a list of tasks."""
    result = []
    client = get_client("ecs")
    cluster_arns = get_cluster_arns()
    if cluster_arns:
        for cluster_arn in cluster_arns:
            response = client.list_tasks(cluster=cluster_arn)
            task_arns = response.get("taskArns")
            if task_arns:
                tasks_response = client.describe_tasks(
                    cluster=cluster_arn,
                    tasks=task_arns)
                tasks = tasks_response.get("tasks")
                if tasks:
                    result += tasks
    return result


def run_task(cluster, task_definition):
    """Run a task in a cluster."""
    client = get_client("ecs")
    params = {}
    params["cluster"] = cluster
    params["taskDefinition"] = task_definition
    response = client.run_task(**params)
    return response


def stop_task(cluster, task_id):
    """Stop a task."""
    client = get_client("ecs")
    params = {}
    params["cluster"] = cluster
    params["task"] = task_id
    response = client.stop_task(**params)
    return response


def get_services():
    """Get a list of services."""
    result = []
    client = get_client("ecs")
    cluster_arns = get_cluster_arns()
    if cluster_arns:
        for cluster_arn in cluster_arns:
            response = client.list_services(cluster=cluster_arn)
            service_arns = response.get("serviceArns")
            if service_arns:
                services_response = client.describe_services(
                    cluster=cluster_arn,
                    services=service_arns)
                services = services_response.get("services")
                if services:
                    result += services
    return result


def create_service(
        name,
        task_definition,
        cluster,
        count,
        load_balancers=[],
        role=None):
    """Run a task in a cluster."""
    client = get_client("ecs")
    params = {}
    params["serviceName"] = name
    params["taskDefinition"] = task_definition
    params["cluster"] = cluster
    params["desiredCount"] = count
    if load_balancers:
        params["loadBalancers"] = load_balancers
    if role:
        params["role"] = role
    response = client.create_service(**params)
    return response


def delete_service(name, cluster):
    """Stop a task."""
    client = get_client("ecs")
    params = {}
    params["service"] = name
    params["cluster"] = cluster
    response = client.delete_service(**params)
    return response


def update_service(name, task_definition, cluster, count):
    """Update a service."""
    client = get_client("ecs")
    params = {}
    params["service"] = name
    params["cluster"] = cluster
    params["desiredCount"] = count
    params["taskDefinition"] = task_definition
    response = client.update_service(**params)
    return response


def wait_for_container_instances_to_terminate(instance_ids):
    """Wait for container instances to terminate."""
    client = get_client("ec2")
    waiter = client.get_waiter("instance_terminated")
    waiter.config.max_attempts = 15
    waiter.wait(InstanceIds=instance_ids)
