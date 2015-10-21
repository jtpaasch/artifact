# -*- coding: utf-8 -*-

"""The ``main`` module for the ``cli`` package."""

import json

import click

from botocore.exceptions import ClientError

from artifact.client import autoscalinggroup
from artifact.client import cloudformation
from artifact.client import ecs
from artifact.client import elasticloadbalancer
from artifact.client import launchconfiguration

from artifact.cli.utils import bash
from artifact.cli.utils.cloudformation import create_cf_template


@click.group()
def cli():
    """Create artifacts in the cloud."""
    pass


@cli.group()
def cluster():
    """Manage ECS cluster artifacts."""
    pass


@cluster.command(name="create")
@click.argument("name")
@click.option(
    "--security-group",
    default=["sg-be4db7d8"],
    multiple=True,
    help="AWS security group ID.")
@click.option(
    "--key",
    default="quickly_fitchet",
    help="Key name for instance.")
@click.option(
    "--role",
    default="ecsInstanceRole",
    help="IAM Instance profile.")
@click.option(
    "--min-size",
    default=1,
    help="Min number of instances.")
@click.option(
    "--max-size",
    default=1,
    help="Max number of instances.")
@click.option(
    "--desired-size",
    default=1,
    help="Desired number of instances.")
@click.option(
    "--subnet",
    default=["subnet-a1e1f9d6"],
    multiple=True,
    help="A subnet to launch in.")
def create_cluster(
        name,
        security_group,
        key,
        role,
        min_size,
        max_size,
        desired_size,
        subnet):
    """Create an ECS cluster."""
    # Create a cluster.
    cluster_response = ecs.create_cluster(name)

    # Create a launch config for that cluster.
    lc_params = {}
    lc_params["name"] = name
    lc_params["ami_id"] = "ami-c16422a4"
    lc_params["key_name"] = key
    lc_params["security_groups"] = security_group
    lc_params["public_ip"] = True
    lc_params["user_data"] = "#!/bin/bash\n" \
                             + "echo ECS_CLUSTER=" + name + " >> /etc/ecs/ecs.config"
    lc_params["role_profile"] = role
    lc_response = launchconfiguration.create_launch_configuration(**lc_params)

    # Create an auto scaling group.
    asg_params = {}
    asg_params["name"] = name
    asg_params["launch_configuration"] = name
    asg_params["min_size"] = min_size
    asg_params["max_size"] = max_size
    asg_params["desired_size"] = desired_size
    asg_params["subnets"] = subnet
    asg_response = autoscalinggroup.create_auto_scaling_group(**asg_params)

    # Report a message.
    click.echo(name + " is launching.")


@cluster.command(name="delete")
@click.argument("name")
def delete_cluster(name):
    """Delete an ECS cluster."""
    asg_response = autoscalinggroup.delete_auto_scaling_group(name)
    lc_response = launchconfiguration.delete_launch_configuration(name)
    instances_response = ecs.get_container_instances(name)
    container_instances = instances_response.get("containerInstances")
    if container_instances:
        instance_ids = []
        for instance in container_instances:
            instance_id = instance.get("ec2InstanceId")
            if instance_id:
                instance_ids.append(instance_id)
        if instance_ids:
            click.echo("Waiting for instances to terminate...")
            ecs.wait_for_container_instances_to_terminate(instance_ids)
    cluster_response = ecs.delete_cluster(name)
    click.echo(name + " terminated.")


@cli.group()
def task():
    """Manage ECS tasks."""
    pass

    
@task.command(name="create")
@click.argument("definition_file", type=click.File("rb"))
def create_task(definition_file):
    """Create a task from a DEFINITION_FILE."""
    contents = json.loads(definition_file.read().decode("utf-8"))
    name = contents.get("family")
    containers = contents.get("containerDefinitions")
    volumes = contents.get("volumes")
    td_response = ecs.create_task_definition(name, containers, volumes)
    click.echo(name + " created.")


@task.command(name="delete")
@click.argument("name")
def delete_task(name):
    """Delete a task definition."""
    td_response = ecs.delete_task_definition_family(name)
    click.echo(name + " deleted.")    


@task.command(name="run")
@click.argument("name")
@click.argument("cluster")
def run_task(name, cluster):
    """Run a task in a cluster."""
    response = ecs.run_task(cluster, name)
    click.echo("Running " + name + " in " + cluster)


@task.command(name="stop")
@click.argument("name")
@click.argument("cluster")
def stop_task(name, cluster):
    """Stop a task in a cluster."""
    response = ecs.stop_task(cluster, name)
    click.echo("Stopping " + name)


@cli.group()
def service():
    """Manage ECS services."""
    pass


@service.command(name="create")
@click.argument("name")
@click.argument("cluster")
@click.option(
    "--count",
    default=1,
    help="Desired number of tasks.")
@click.option(
    "--elb",
    nargs=2,
    help="Load_balancer -> container.")
def create_service(name, cluster, count, elb):
    """Create a service in a cluster."""
    params = {}
    params["name"] = name
    params["task_definition"] = name
    params["cluster"] = cluster
    params["count"] = count
    if elb:
        params["load_balancers"] = [{
            "loadBalancerName": elb[0],
            "containerName": elb[1],
            "containerPort": 80,
        }]
        params["role"] = "ecsServiceRole"
    response = ecs.create_service(**params)
    click.echo("Creating " + name + " in " + cluster)


@service.command(name="delete")
@click.argument("name")
@click.argument("cluster")
def delete_service(name, cluster):
    """Delete a service in a cluster."""
    scale_response = ecs.update_service(name, name, cluster, 0)
    response = ecs.delete_service(name, cluster)
    click.echo("Deleting " + name + " in " + cluster)


@service.command(name="update")
@click.argument("name")
@click.argument("cluster")
@click.option(
    "--task-definition",
    default=None,
    help="A new task definition to use.")
@click.option(
    "--count",
    type=int,
    help="The number of tasks.")
def update_service(name, cluster, task_definition, count):
    """Update a service in a cluster."""
    params = {}
    if not task_definition:
        task_definition = name
    if not count:
        raise click.ClickException("No count specified.")
    response = ecs.update_service(name, task_definition, cluster, count)
    click.echo("Updating " + name + " in " + cluster)


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
