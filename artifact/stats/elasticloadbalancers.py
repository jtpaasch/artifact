# -*- coding: utf-8 -*-

"""A module to fetch stats about elastic load balancers."""

from deploy.client import elasticloadbalancer


def get_elastic_load_balancers():
    """Get data about elastic load balancers."""
    data = elasticloadbalancer.get_elastic_load_balancers()
    elastic_load_balancers = data.get("LoadBalancerDescriptions")
    return elastic_load_balancers
