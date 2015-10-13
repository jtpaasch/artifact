# -*- coding: utf-8 -*-

"""A module to fetch stats about auto scaling groups."""

from deploy.client import autoscalinggroup


def get_auto_scaling_groups():
    """Get data about auto scaling groups."""
    data = autoscalinggroup.get_auto_scaling_groups()
    auto_scaling_groups = data.get("AutoScalingGroups")
    return auto_scaling_groups
