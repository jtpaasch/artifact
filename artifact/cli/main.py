# -*- coding: utf-8 -*-

"""The ``main`` module for the ``cli`` package."""

import click

from botocore.exceptions import ClientError

from artifact.client import autoscalinggroup
from artifact.client import cloudformation
from artifact.client import elasticloadbalancer


from artifact.cli.utils import bash
from artifact.cli.utils.cloudformation import create_cf_template


@click.group()
def cli():
    """Create artifacts in the cloud."""
    pass


@cli.group()
def cf():
    """Manage cloud formation artifacts."""
    pass


@cf.command(name="create")
@click.argument("name")
@click.option(
    "--min-size",
    default=1,
    help="Minimum number of instances.")
@click.option(
    "--max-size",
    default=1,
    help="Maximum number of instances.")
@click.option(
    "--image",
    help="Docker registry image (with tag).")
@click.option(
    "--username",
    help="Docker registry username.")
@click.option(
    "--password",
    help="Docker registry password.")
@click.option(
    "--email",
    help="Docker registry email.")
@click.option(
    "--template-file",
    help="Cloud Formation template file.")
def create_cf(
        name,
        min_size,
        max_size,
        image,
        username,
        password,
        email,
        template_file):
    """Create a Cloud Formation artifact."""
    ps_name = image.replace("/", "_").replace(":", "_")
    ps_param = {"ParameterKey": "ContainerNameParameter", "ParameterValue": ps_name}
    image_param = {"ParameterKey": "ImageParameter", "ParameterValue": image}
    parameters = [ps_param, image_param]
    params = {}
    params["name"] = name
    params["parameters"] = parameters
    if template_file:
        params["template_file"] = template_file
    else:
        params["template"] = create_cf_template(username, password, email)
    response = cloudformation.create_stack(**params)
    click.echo("Stack " + name + " launching.")


@cf.command(name="delete")
@click.argument("name")
def delete_cf(name):
    """Delete a Cloud Formation artifact."""
    # Note: This does not raise an error if the stack doesn't exist.
    response = cloudformation.delete_stack(name)
    click.echo("Stack " + name + " terminating.")


@cli.group()
def app():
    """Manage application artifacts."""
    pass


@app.command(name="create")
@click.argument("name")
@click.option(
    "--min-size",
    default=1,
    help="Minimum number of instances.")
@click.option(
    "--max-size",
    default=1,
    help="Maximum number of instances.")
@click.option(
    "--desired-size",
    default=1,
    help="Desired number of instances.")
@click.option(
    "--image",
    help="Docker registry image (with tag).")
@click.option(
    "--username",
    help="Docker registry username.")
@click.option(
    "--password",
    help="Docker registry password.")
@click.option(
    "--email",
    help="Docker registry email.")
def create_app(
        name,
        min_size,
        max_size,
        desired_size,
        image,
        username,
        password,
        email):
    """Create an application artifact."""
    bash.create_launch_configuration(
        name,
        image,
        username,
        password,
        email)
    params = {}
    params["name"] = name
    params["min_size"] = 1
    params["max_size"] = 1
    params["desired_size"] = 1
    params["subnets"] = ["subnet-f6e9cadd", "subnet-a1e1f9d6"]
    params["launch_configuration"] = name
    try:
        response = autoscalinggroup.create_auto_scaling_group(**params)
    except ClientError as e:
        if e.response["Error"]["Code"] == "AlreadyExists":
            raise click.ClickException(name + " already exists.")
    success = False
    metadata = response.get("ResponseMetadata")
    if metadata:
        status_code = metadata.get("HTTPStatusCode")
        if status_code == 200:
            success = True
    if success:
        click.echo(name + " launching.")
    else:
        message = name + " was not created. Something went wrong."
        raise click.ClickException(message)


@app.command(name="delete")
@click.argument("name")
def delete_app(name):
    """Delete an application artifact."""
    params = {}
    params["name"] = name
    try:
        response = autoscalinggroup.delete_auto_scaling_group(**params)
    except ClientError as e:
        message = "AutoScalingGroup name not found"
        if e.response["Error"]["Message"].startswith(message):
            raise click.ClickException("No auto scaling group called " + name)
    success = False
    metadata = response.get("ResponseMetadata")
    if metadata:
        status_code = metadata.get("HTTPStatusCode")
        if status_code == 200:
            success = True
    try:
        response = launchconfiguration.delete_launch_configuration(name)
    except ClientError as e:
        message = "Launch configuration name not found"
        if e.response["Error"]["Message"].startswith(message):
            raise click.ClickException("No launch config called " + name)
    success_2 = False
    metadata = response.get("ResponseMetadata")
    if metadata:
        status_code = metadata.get("HTTPStatusCode")
        if status_code == 200:
            success_2 = True
    if success and success_2:
        click.echo(name + " terminating.")
    else:
        message = name + " was not deleted. Something went wrong."
        raise click.ClickException(message)


@app.command()
@click.argument("app_name")
@click.argument("elb_name")
def serve(app_name, elb_name):
    """Serve an application artifact through an ELB."""
    params = {}
    params["auto_scaling_group_name"] = app_name
    params["elastic_load_balancer_names"] = [elb_name]
    try:
        response = autoscalinggroup.attach_elastic_load_balancer(**params)
    except ClientError as e:
        app_msg = "AutoScalingGroup name not found"
        elb_msg = "Provided ELBs may not be valid"
        if e.response["Error"]["Message"].startswith(app_msg):
            raise click.ClickException(app_name + " does not exist.")
        elif e.response["Error"]["Message"].startswith(elb_msg):
            raise click.ClickException(elb_name + " does not exist.")
    success = False
    metadata = response.get("ResponseMetadata")
    if metadata:
        status_code = metadata.get("HTTPStatusCode")
        if status_code == 200:
            success = True
    if success:
        click.echo("Serving " + app_name + " at " + elb_name + ".")
    else:
        message = app_name + " did not get served. Something went wrong."
        raise click.ClickException(message)


@app.command()
@click.argument("app_name")
@click.argument("elb_name")
def unserve(app_name, elb_name):
    """Stop serving an application through an ELB."""
    params = {}
    params["auto_scaling_group_name"] = app_name
    params["elastic_load_balancer_names"] = [elb_name]
    try:
        response = autoscalinggroup.detach_elastic_load_balancer(**params)
    except ClientError as e:
        app_msg = "AutoScalingGroup name not found"
        elb_msg = "Trying to remove Load Balancers that are not part of"
        if e.response["Error"]["Message"].startswith(app_msg):
            raise click.ClickException(app_name + " does not exist.")
        elif e.response["Error"]["Message"].startswith(elb_msg):
            error_msg = app_name + " not connected to any " + elb_name + "."
            raise click.ClickException(error_msg)
    success = False
    metadata = response.get("ResponseMetadata")
    if metadata:
        status_code = metadata.get("HTTPStatusCode")
        if status_code == 200:
            success = True
    if success:
        click.echo("Stopped serving " + app_name + " at " + elb_name + ".")
    else:
        message = app_name + " did not stop serving. Something went wrong."
        raise click.ClickException(message)


@cli.group()
def elb():
    """Manage load balancer artifacts."""
    pass


@elb.command(name="create")
@click.argument("name")
@click.option(
    "--security-group",
    default="sg-be4db7d8",
    help="A security group ID.")
def create_elb(name, security_group):
    """Create an elastic load balancer."""
    params = {}
    params["name"] = name
    params["listeners"] = [{
        "Protocol": "HTTP",
        "LoadBalancerPort": 80,
        "InstancePort": 80,
        }]
    params["subnets"] = ["subnet-f6e9cadd", "subnet-a1e1f9d6"]
    params["security_groups"] = [security_group]
    try:
        response = elasticloadbalancer.create_elastic_load_balancer(**params)
    except ClientError as e:
        if e.response["Error"]["Code"] == "AlreadyExists":
            raise click.ClickException(name + " already exists.")
    success = False
    metadata = response.get("ResponseMetadata")
    if metadata:
        status_code = metadata.get("HTTPStatusCode")
        if status_code == 200:
            success = True
    if success:
        click.echo(name + " launching.")
    else:
        message = name + " was not created. Something went wrong."
        raise click.ClickException(message)


@elb.command(name="delete")
@click.argument("name")
def delete_elb(name):
    """Delete an elastic load balancer."""
    params = {}
    params["name"] = name
    # Note: this does not throw an exception if no such ELB exists.
    response = elasticloadbalancer.delete_elastic_load_balancer(**params)
    success = False
    metadata = response.get("ResponseMetadata")
    if metadata:
        status_code = metadata.get("HTTPStatusCode")
        if status_code == 200:
            success = True
    if success:
        click.echo(name + " terminating.")
    else:
        message = name + " was not deleted. Something went wrong."
        raise click.ClickException(message)
