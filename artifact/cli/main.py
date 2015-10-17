# -*- coding: utf-8 -*-

"""The ``main`` module for the ``cli`` package."""

import click

from botocore.exceptions import ClientError

from artifact.client import autoscalinggroup
from artifact.client import cloudformation
from artifact.client import elasticloadbalancer
from artifact.client import launchconfiguration


def create_cf_template(username, password, email):
    """Create a Cloud Formation template."""
    template = []
    template.append('{')
    template.append('  "AWSTemplateFormatVersion": "2010-09-09",')
    template.append('  "Parameters": {')
    template.append('    "ContainerNameParameter": {')
    template.append('      "Type": "String",')
    template.append('      "Description": "Enter a name for the running container"')
    template.append('    },')
    template.append('    "ImageParameter": {')
    template.append('      "Type": "String",')
    template.append('      "Description": "Enter a registry image (and tag)"')
    template.append('    },')
    template.append('    "MinSizeParameter": {')
    template.append('      "Type": "Number",')
    template.append('      "Default": "1",')
    template.append('      "Description": "Enter the min size"')
    template.append('    },')
    template.append('    "MaxSizeParameter": {')
    template.append('      "Type": "Number",')
    template.append('      "Default": "1",')
    template.append('      "Description": "Enter the max size"')
    template.append('    }')
    template.append('  },')
    template.append('  "Resources": {')
    template.append('    "ReeferLaunchConfig": {')
    template.append('      "Type": "AWS::AutoScaling::LaunchConfiguration",')
    template.append('      "Properties": {')
    template.append('        "AssociatePublicIpAddress": "true",')
    template.append('        "ImageId": "ami-e3106686",')
    template.append('        "InstanceType": "t2.micro",')
    template.append('        "KeyName": "quickly_fitchet",')
    template.append('        "SecurityGroups": [')
    template.append('          "sg-be4db7d8"')
    template.append('        ],')
    template.append('        "UserData": {')
    template.append('          "Fn::Base64": {')
    template.append('            "Fn::Join": [')
    template.append('              "",')
    template.append('              [')
    template.append('                "#!/bin/bash -xe\\n",')
    template.append('                "\\n",')
    template.append('                "# Install and start docker.\\n",')
    template.append('                "yum install -y docker\\n",')
    template.append('                "service docker start\\n",')
    template.append('                "chkconfig docker on\\n",')
    template.append('                "\\n",')
    if username and password and email:
        template.append('                "# Authenticate with docker hub.\\n",')
        template.append('                "docker login \\\\n",')
        template.append('                "    -u ' + username + ' \\\\n",')
        template.append('                "    -p ' + password + ' \\\\n",')
        template.append('                "    -e ' + email + '\\n",')
        template.append('                "\\n",')
    template.append('                "# Pull the docker image.\\n",')
    template.append('                "docker pull ", {"Ref": "ImageParameter"}, " \\n",')
    template.append('                "\\n",')
    template.append('                "# Start the container.\\n",')
    template.append('                "docker run",')
    template.append('                "    --name ", {"Ref": "ContainerNameParameter"},')
    template.append('                "    --restart always",')
    template.append('                "    -dti",')
    template.append('                "    -p 80:80",')
    template.append('                "    ", {"Ref": "ImageParameter"}, "\\n",')
    template.append('                "\\n"')
    template.append('              ]')
    template.append('            ]')
    template.append('          }')
    template.append('        }')
    template.append('      }')
    template.append('    },')
    template.append('    "ReeferASG": {')
    template.append('      "Type": "AWS::AutoScaling::AutoScalingGroup",')
    template.append('      "Properties": {')
    template.append('        "LaunchConfigurationName": {"Ref": "ReeferLaunchConfig"},')
    template.append('        "MinSize": "1",')
    template.append('        "MaxSize": "1",')
    template.append('        "VPCZoneIdentifier": [')
    template.append('          "subnet-a1e1f9d6",')
    template.append('          "subnet-33d2e06a"')
    template.append('        ]')
    template.append('      }')
    template.append('    }')
    template.append('  }')
    template.append('}')
    return "\n".join(template)


def create_user_data(image, username, password, email):
    """Create a user_data script that pulls and runs a docker container."""
    user_data = []
    user_data.append("#!/bin/bash")
    user_data.append("")
    user_data.append("# Print out debug info and exit on any failure.")
    user_data.append("set -x -e")
    user_data.append("")
    user_data.append("# Install and start docker.")
    user_data.append("yum install -y docker")
    user_data.append("service docker start")
    user_data.append("chkconfig docker on")
    user_data.append("")
    if username and password and email:
        user_data.append("# Authenticate with docker.")
        user_data.append("docker login \\")
        user_data.append("    -u '" + username + "' \\")
        user_data.append("    -p '" + password + "' \\")
        user_data.append("    -e '" + email + "'")
        user_data.append("")
    ps_name = image.replace("/", "_").replace(":", "_")
    user_data.append("# Pull down the docker image.")
    user_data.append("docker pull " + image)
    user_data.append("")
    user_data.append("# Now run the container.")
    user_data.append("docker run \\")
    user_data.append("    --name " + ps_name + " \\")
    user_data.append("    --restart always \\")
    user_data.append("    -dti \\")
    user_data.append("    -p 80:80 \\")
    user_data.append("    " + image)
    user_data.append("")
    return "\n".join(user_data)


def create_launch_configuration(name, image, username, password, email):
    """Create a launch configuration for a docker image."""
    user_data = create_user_data(image, username, password, email)
    params = {}
    params["name"] = name
    params["ami_id"] = "ami-e3106686"
    params["key_name"] = "quickly_fitchet"
    params["security_groups"] = ["sg-be4db7d8"]
    params["public_ip"] = True
    params["user_data"] = user_data
    response = launchconfiguration.create_launch_configuration(**params)
    return response


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


@cf.command(name="delete")
@click.argument("name")
def delete_cf(name):
    """Delete a Cloud Formation artifact."""
    response = cloudformation.delete_stack(name)


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
    create_launch_configuration(
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
