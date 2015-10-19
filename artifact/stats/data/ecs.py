# -*- coding: utf-8 -*-

"""A module to fetch stats about ECS."""

from artifact.client import ecs


def get_clusters():
    """Get data about ECS clusters."""
    data = ecs.get_clusters()
    clusters = data.get("clusters")
    return clusters
