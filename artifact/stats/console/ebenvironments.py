# -*- coding: utf-8 -*-

"""A module to update console stats about Elastic Beanstalk environments."""

from artifact.stats.console.utils import is_update_needed
from artifact.stats.data.elasticbeanstalk import get_environments


def data(widget):
    """Get data for the widget."""
    result = widget["data"]
    if is_update_needed():
        environments_data = get_environments()
        fieldsets = []
        for datum in environments_data:
            fieldset = []
            environment_name = datum.get("EnvironmentName")
            if environment_name:
                fieldset.append(environment_name)
            environment_id = datum.get("EnvironmentId")
            if environment_id:
                fieldset.append(environment_id)
            app_name = datum.get("ApplicationName")
            if app_name:
                fieldset.append(app_name)
            cname = datum.get("CNAME")
            if cname:
                fieldset.append(cname)
            health = datum.get("Health")
            if health:
                fieldset.append("Health: " + str(health))
            status = datum.get("Status")
            if status:
                fieldset.append(status)
            tier = datum.get("Tier")
            if tier:
                tier_type = tier.get("Name")
                if tier_type:
                    fieldset.append(tier_type)
            if fieldset:
                fieldsets.append(fieldset)
        if fieldsets:
            result = fieldsets
    return result
