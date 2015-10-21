# -*- coding: utf-8 -*-

"""A module to update console stats about ECS task definitions."""

from artifact.stats.console.utils import is_update_needed
from artifact.stats.data.ecs import get_task_definitions


def data(widget):
    """Get data for the widget."""
    result = widget["data"]
    if is_update_needed():
        task_definitions_data = get_task_definitions()
        fieldsets = []
        for datum in task_definitions_data:
            fieldset = []
            family = datum.get("family")
            revision = datum.get("revision")
            if family and revision:
                task_def_name = str(family) + ":" + str(revision)
                fieldset.append(task_def_name)
            status = datum.get("status")
            if status:
                fieldset.append(status)
            containers = datum.get("containerDefinitions")
            if containers:
                for container in containers:
                    container_name = container.get("name")
                    if container_name:
                        fieldset.append("- " + container_name)
                    container_image = container.get("image")
                    if container_image:
                        fieldset.append("  " + container_image)
                    container_cpu = container.get("cpu")
                    if container_cpu:
                        fieldset.append("  cpu: " + str(container_cpu))
                    container_memory = container.get("memory")
                    if container_memory:
                        fieldset.append("  memory: " + str(container_memory))
                    port_mappings = container.get("portMappings")
                    ports = []
                    if port_mappings:
                        for mapping in port_mappings:
                            protocol = mapping.get("protocol")
                            host_port = mapping.get("hostPort")
                            container_port = mapping.get("containerPort")
                            port = str(protocol) + " " \
                                   + str(host_port) + ":" \
                                   + str(container_port)
                            ports.append(port)
                        if ports:
                            fieldset += ["  " + x for x in ports]
            if fieldset:
                fieldsets.append(fieldset)
        if fieldsets:
            result = fieldsets
    return result
