# -*- coding: utf-8 -*-

"""A module to update console stats about auto scaling groups."""

from artifact.stats.console.utils import is_update_needed
from artifact.stats.data.autoscalinggroups import get_auto_scaling_groups


def data(widget):
    """Get data for the widget."""
    result = widget["data"]
    if is_update_needed():
        asg_data = get_auto_scaling_groups()
        fieldsets = []
        for datum in asg_data:
            fieldset = []
            group_name = datum.get("AutoScalingGroupName")
            if group_name:
                fieldset.append(group_name)
            launch_config_name = datum.get("LaunchConfigurationName")
            if launch_config_name:
                fieldset.append(launch_config_name)
            min_size = datum.get("MinSize") or 0
            max_size = datum.get("MaxSize") or 0
            desired_size = datum.get("DesiredCapacity") or 0
            size = min_size + " " + max_size + " " + desired_size
            if size:
                fieldset.append(size)
            availability_zones = datum.get("AvailabilityZones")
            if availability_zones:
                fieldset.append(availability_zones)
            elbs = datum.get("LoadBalancerNames")
            if elbs:
                fieldset += elbs
            instances = []
            instance_list = datum.get("Instances")
            if instance_list:
                for instance in instance_list:
                    instance_id = instance.get("InstanceId")
                    if instance_id:
                        instances.append(instance_id)
                    instance_zone = instance.get("AvailabilityZone")
                    if instance_zone:
                        instances.append(instance_zone)
                    instance_status = instance.get("LifecycleState")
                    if instance_status:
                        instances.append(instance_status)
                    instance_health = instance.get("HealthStatus")
                    if instance_health:
                        instances.append(instance_health)
            if instances:
                fieldset += instances
            if fieldset:
                fieldsets.append(fieldset)
        if fieldsets:
            result = fieldsets
    return result
