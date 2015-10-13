# -*- coding: utf-8 -*-

"""A module to fetch stats about EC2 instances."""

from deploy.client import ec2 as ec2lib


def get_instances():
    """Get data about EC2 instances."""
    instances = []
    data = ec2lib.get_instances()
    reservations = data.get("Reservations")
    if reservations:
        for reservation in reservations:
            instance_list = reservation.get("Instances")
            for instance in instance_list:
                instances.append(instance)
    return instances
