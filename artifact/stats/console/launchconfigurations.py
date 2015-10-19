# -*- coding: utf-8 -*-

"""A module to update console stats about launch configurations."""

from datetime import datetime

from artifact.stats.data.launchconfigurations import get_launch_configurations


def data(widget):
    """Get data for the widget."""
    result = widget["data"]
    if not datetime.now().second % 5:
        launchconfig_data = get_launch_configurations()
        fieldsets = []
        for datum in launchconfig_data:
            fieldset = []
            config_name = datum.get("LaunchConfigurationName")
            if config_name:
                fieldset.append(config_name)
            image_id = datum.get("ImageId")
            if image_id:
                fieldset.append(image_id)
            key_name = datum.get("KeyName")
            if key_name:
                fieldset.append(key_name)
            instance_type = datum.get("InstanceType")
            if instance_type:
                fieldset.append(instance_type)
            instance_profile = datum.get("IamInstanceProfile")
            if instance_profile:
                fieldset.append(instance_profile)
            security_groups = datum.get("SecurityGroups")
            if security_groups:
                fieldset += security_groups
            if fieldset:
                fieldsets.append(fieldset)
        if fieldsets:
            result = fieldsets
    return result
