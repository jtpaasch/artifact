# -*- coding: utf-8 -*-

"""A module to update console stats about ECS container instances."""

from artifact.stats.console.utils import is_update_needed
from artifact.stats.data.ecs import get_clusters
from artifact.stats.data.ecs import get_container_instances


def data(widget):
    """Get data for the widget."""
    result = widget["data"]
    if is_update_needed():
        instance_data = get_container_instances()
        fieldsets = []
        for datum in instance_data:
            fieldset = []
            instance_id = datum.get("ec2InstanceId")
            if instance_id:
                fieldset.append(instance_id)
            cluster_name = datum.get("clusterName")
            if cluster_name:
                fieldset.append(cluster_name)
            status = datum.get("status")
            if status:
                fieldset.append(status)
            has_agent = datum.get("agentConnected")
            if has_agent:
                fieldset.append("Agent connected")
            pending_tasks = datum.get("pendingTasksCount")
            if pending_tasks:
                fieldset.append("Pending tasks: " + str(pending_tasks))
            running_tasks = datum.get("runningTasksCount")
            if running_tasks:
                fieldset.append("Running tasks: " + str(running_tasks))
            resources = datum.get("registeredResources")
            if resources:
                for resource in resources:
                    resource_name = resource.get("name")
                    cpu = None
                    memory = None
                    ports = None
                    udp_ports = None
                    if resource_name == "CPU":
                        cpu = resource.get("integerValue")
                    elif resource_name == "MEMORY":
                        memory = resource.get("integerValue")
                    elif resource_name == "PORTS":
                        ports = resource.get("stringSetValue")
                    elif resource_name == "PORTS_UDP":
                        udp_ports = resource.get("stringSetValue")
                    if cpu:
                        fieldset.append("cpu: " + str(cpu))
                    if memory:
                        fieldset.append("memory: " + str(memory))
                    if ports:
                        fieldset.append("ports:")
                        fieldset += ["  " + x for x in ports]
                    if udp_ports:
                        fieldset.append("udp ports:")
                        fieldset += ["  " + x for x in udp_ports]
            remaining_resources = datum.get("registeredResources")
            if remaining_resources:
                for resource in remaining_resources:
                    cpu = None
                    memory = None
                    ports = None
                    udp_ports = None
                    resource_name = resource.get("name")
                    if resource_name == "CPU":
                        cpu = resource.get("integerValue")
                    elif resource_name == "MEMORY":
                        memory = resource.get("integerValue")
                    elif resource_name == "PORTS":
                        ports = resource.get("stringSetValue")
                    elif resource_name == "PORTS_UDP":
                        udp_ports = resource.get("stringSetValue")
                    if cpu:
                        fieldset.append("cpu left: " + str(cpu))
                    if memory:
                        fieldset.append("memory left: " + str(memory))
                    if ports:
                        fieldset.append("ports left:")
                        fieldset += ["  " + x for x in ports]
                    if udp_ports:
                        fieldset.append("udp ports left:")
                        fieldset += ["  " + x for x in udp_ports]
            if fieldset:
                fieldsets.append(fieldset)
        if fieldsets:
            result = fieldsets
    return result
