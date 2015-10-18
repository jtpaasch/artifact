# -*- coding: utf-8 -*-

"""A module with utils for a bash-directed work flow."""

from artifact.client import launchconfiguration


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
