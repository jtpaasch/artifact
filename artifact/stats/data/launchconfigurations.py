# -*- coding: utf-8 -*-

"""A module to fetch stats about launch configurations."""

from artifact.client import launchconfiguration


def get_launch_configurations():
    """Get data about launch configurations."""
    data = launchconfiguration.get_launch_configurations()
    configs = data.get("LaunchConfigurations")
    return configs
