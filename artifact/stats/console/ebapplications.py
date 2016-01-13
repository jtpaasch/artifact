# -*- coding: utf-8 -*-

"""A module to update console stats about Elastic Beanstalk applications."""

from artifact.stats.console.utils import is_update_needed
from artifact.stats.data.elasticbeanstalk import get_applications


def data(widget):
    """Get data for the widget."""
    result = widget["data"]
    if is_update_needed():
        applications_data = get_applications()
        fieldsets = []
        for datum in applications_data:
            fieldset = []
            app_name = datum.get("ApplicationName")
            if app_name:
                fieldset.append(app_name)
            versions = datum.get("Versions")
            if versions:
                fieldset.append("Versions:")
                fieldset += ["  " + x for x in versions]
            config_templates = datum.get("ConfigurationTemplates")
            if config_templates:
                fieldset.append("Config templates:")
                fieldset += ["  " + x for x in config_templates]
            if fieldset:
                fieldsets.append(fieldset)
        if fieldsets:
            result = fieldsets
    return result
