# -*- coding: utf-8 -*-

"""A module to update console stats about ECS tasks."""

from artifact.stats.console.utils import is_update_needed
from artifact.stats.data.ecs import get_services


def data(widget):
    """Get data for the widget."""
    result = widget["data"]
    if is_update_needed():
        services_data = get_services()
        fieldsets = []
        for datum in services_data:
            fieldset = []
            service_name = datum.get("serviceName")
            cluster_arn = datum.get("clusterArn")
            if cluster_arn:
                cluster_name_start = cluster_arn.rfind("/")
                if cluster_name_start:
                    cluster_name = cluster_arn[cluster_name_start + 1:]
                    fieldset.append(cluster_name)
            status = datum.get("status")
            if status:
                fieldset.append(status)
            desired_count = datum.get("desiredCount")
            if desired_count:
                fieldset.append("desired: " + str(desired_count))
            running_count = datum.get("runningCount")
            if running_count:
                fieldset.append("running: " + str(running_count))
            pending_count = datum.get("pendingCount")
            if pending_count:
                fieldset.append("pending: " + str(pending_count))
            task_definition = datum.get("taskDefinition")
            if task_definition:
                fieldset.append("task_definition")
            load_balancers = datum.get("loadBalancers")
            if load_balancers:
                for balancer in load_balancers:
                    balancer_name = balancer.get("loadBalancerName")
                    if balancer_name:
                        fieldset.append("elb: " + balancer_name)
                    container_name = balancer.get("containerName")
                    if container_name:
                        fieldset.append("container: " + container_name)
                    container_port = balancer.get("containerPort")
                    if container_port:
                        fieldset.append("port: " + str(container_port))
            if fieldset:
                fieldsets.append(fieldset)
        if fieldsets:
            result = fieldsets
    return result
