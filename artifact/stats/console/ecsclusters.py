# -*- coding: utf-8 -*-

"""A module to update console stats about ECS clusters."""

from artifact.stats.console.utils import is_update_needed
from artifact.stats.data.ecs import get_clusters


def data(widget):
    """Get data for the widget."""
    result = widget["data"]
    if is_update_needed():
        cluster_data = get_clusters()
        fieldsets = []
        for datum in cluster_data:
            fieldset = []
            cluster_name = datum.get("clusterName")
            if cluster_name:
                fieldset.append(cluster_name)
            # cluster_arn = datum.get("clusterArn")
            # if cluster_arn:
            #     fieldset.append(cluster_arn)
            status = datum.get("status")
            if status:
                fieldset.append(status)
            instances = datum.get("registeredContainerInstancesCount")
            if instances:
                fieldset.append("Instances: " + str(instances))
            running_tasks = datum.get("runningTasksCount")
            if running_tasks:
                fieldset.append("Running tasks: " + str(running_tasks))
            pending_tasks = datum.get("pendingTasksCount")
            if pending_tasks:
                fieldset.append("Pending tasks: " + str(pending_tasks))
            active_services = datum.get("activeServicesCount")
            if active_services:
                fieldset.append("Active services: " + str(active_services))
            if fieldset:
                fieldsets.append(fieldset)
        if fieldsets:
            result = fieldsets
    return result
