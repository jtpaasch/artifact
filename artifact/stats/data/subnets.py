# -*- coding: utf-8 -*-

"""A module to fetch stats about subnets."""

from artifact.client import subnet


def get_subnets():
    """Get data about subnets."""
    data = subnet.get_subnets()
    subnets = data.get("Subnets")
    return subnets
