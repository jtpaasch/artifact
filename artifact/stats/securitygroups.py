# -*- coding: utf-8 -*-

"""A module to fetch stats about security groups."""

from deploy.client import securitygroup


def get_security_groups():
    """Get data about security  groups."""
    data = securitygroup.get_security_groups()
    security_groups = data.get("SecurityGroups")
    return security_groups
