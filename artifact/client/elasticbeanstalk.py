# -*- coding: utf-8 -*-

"""A module to handle Elastic Beanstalk."""

from artifact.client.utils import get_client


def create_application(name):
    """Create an Elastic Beanstalk application."""
    client = get_client("elasticbeanstalk")
    params = {}
    params["ApplicationName"] = name
    response = client.create_application(**params)
    return response


def delete_application(name, force=True):
    """Delete an Elastic Beanstalk application."""
    client = get_client("elasticbeanstalk")
    params = {}
    params["ApplicationName"] = name
    params["TerminateEnvByForce"] = force
    response = client.delete_application(**params)
    return response


def get_applications():
    """Get info about all Elastic Beanstalk applications."""
    client = get_client("elasticbeanstalk")
    response = client.describe_applications()
    return response


def get_solution_stacks():
    """Get a list of all available solution stacks."""
    client = get_client("elasticbeanstalk")
    response = client.list_available_solution_stacks()
    return response

def get_multicontainer_docker_solution_stack():
    """Get the latest Multi-Container Docker solution stack."""
    response = get_solution_stacks()
    stacks = response.get("SolutionStacks")
    match = "Multi-container Docker 1.7.1"
    items_with_match = (x for x in stacks if match in x)
    result = next(items_with_match, None)
    return result


def create_environment(
        name,
        application,
        cname=None,
        tier="web",
        key=None,
        instance_type="t2.micro",
        profile=None,
        role=None,
        healthcheck_url=None):
    """Create an Elastic Beanstalk environment."""
    client = get_client("elasticbeanstalk")
    params = {}
    params["ApplicationName"] = application
    params["EnvironmentName"] = name
    if not cname:
        cname = name
    params["CNAMEPrefix"] = cname
    if tier == "web":
        tier_definition = {
            "Name": "WebServer",
            "Type": "Standard",
            "Version": "1.0",
        }
    elif tier == "worker":
        tier_definition = {
            "Name": "Worker",
            "Type": "SQS/HTTP",
            "Version": "1.0",
        }
    params["Tier"] = tier_definition
    stack = get_multicontainer_docker_solution_stack()
    params["SolutionStackName"] = stack
    options = []
    if key:
        key_option = {
            "ResourceName": "Key",
            "Namespace": "aws:autoscaling:launchconfiguration",
            "OptionName": "EC2KeyName",
            "Value": key
        }
        options.append(key_option)
    if instance_type:
        instance_type_option = {
            "ResourceName": "InstanceType",
            "Namespace": "aws:autoscaling:launchconfiguration",
            "OptionName": "InstanceType",
            "Value": instance_type,
        }
        options.append(instance_type_option)
    if profile:
        profile_option = {
            "ResourceName": "IamInstanceProfile",
            "Namespace": "aws:autoscaling:launchconfiguration",
            "OptionName": "IamInstanceProfile",
            "Value": profile,
        }
        options.append(profile_option)
    if role:
        role_option = {
            "ResourceName": "ServiceRole",
            "Namespace": "aws:elasticbeanstalk:environment",
            "OptionName": "ServiceRole",
            "Value": role,
        }
        options.append(role)
    if healthcheck_url:
        healthcheck_url_option = {
            "ResourceName": "HealthcheckURL",
            "Namespace": "elasticbeanstalk:application",
            "OptionName": "Application Healthcheck URL",
            "Value": healthcheck_url,
        }
        options.append(healthcheck_url_option)
    if options:
        params["OptionSettings"] = options
    # Note: you can also add OptionsToRemove, just like OptionSettings.
    response = client.create_environment(**params)
    return response


def delete_environment(name, force=True):
    """Delete an Elastic Beanstalk environment."""
    client = get_client("elasticbeanstalk")
    params = {}
    params["EnvironmentName"] = name
    if force:
        params["TerminateResources"] = True
    response = client.terminate_environment(**params)
    return response


def get_environments():
    """Get info about all Elastic Beanstalk environments."""
    client = get_client("elasticbeanstalk")
    response = client.describe_environments()
    return response



