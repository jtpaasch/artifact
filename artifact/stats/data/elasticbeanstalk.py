# -*- coding: utf-8 -*-

"""A module to fetch stats about Elastic Beanstalk."""

from artifact.client import elasticbeanstalk


def get_applications():
    """Get data about Elastic Beanstalk applications."""
    data = elasticbeanstalk.get_applications()
    applications = data.get("Applications")
    return applications


def get_environments():
    """Get data about Elastic Beanstalk applications."""
    data = elasticbeanstalk.get_environments()
    environments = data.get("Environments")
    return environments
