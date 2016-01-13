# -*- coding: utf-8 -*-

"""A module to handle Cloud Formation stacks."""

from artifact.client.utils import get_client
from artifact.client.utils import get_file_contents


def create_stack(name, template=None, template_file=None, parameters=None, capabilities=None):
    """Create a Cloud Formation stack."""
    client = get_client("cloudformation")
    params = {}
    params["StackName"] = name
    if template:
        params["TemplateBody"] = template
    elif template_file:
        params["TemplateBody"] = get_file_contents(template_file)
    if parameters:
        params["Parameters"] = parameters
    if capabilities:
        params["Capabilities"] = capabilities
    response = client.create_stack(**params)
    return response


def get_stacks():
    """Get info about all Cloud Formation stacks."""
    client = get_client("cloudformation")
    response = client.describe_stacks()
    return response


def delete_stack(name):
    """Delete a Cloud Formations tack."""
    client = get_client("cloudformation")
    response = client.delete_stack(StackName=name)
    return response
