# -*- coding: utf-8 -*-

"""A module to update console stats about ECS tasks."""

from artifact.stats.console.utils import is_update_needed
from artifact.stats.data.ecs import get_tasks


def data(widget):
    """Get data for the widget."""
    result = widget["data"]
    if is_update_needed():
        tasks_data = get_tasks()
        fieldsets = []
        for datum in tasks_data:
            fieldset = []
            task_arn = datum.get("taskArn")
            if task_arn:
                task_id_start = task_arn.rfind("/")
                if task_id_start:
                    task_id = task_arn[task_id_start + 1:]
                    fieldset.append(task_id)
            cluster_arn = datum.get("clusterArn")
            if cluster_arn:
                cluster_name_start = cluster_arn.rfind("/")
                if cluster_name_start:
                    cluster_name = cluster_arn[cluster_name_start + 1:]
                    fieldset.append(cluster_name)
            desired_status = datum.get("desiredStatus")
            if desired_status:
                fieldset.append("Desired status: ")
                fieldset.append("  " + desired_status)
            last_status = datum.get("lastStatus")
            if last_status:
                fieldset.append("Last status: ")
                fieldset.append("  " + last_status)
            if fieldset:
                fieldsets.append(fieldset)
        if fieldsets:
            result = fieldsets
    return result
