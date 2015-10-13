# -*- coding: utf-8 -*-

"""A module to handle ssh keys."""

from artifact.client.utils import get_client


def create_keys(name):
    """Create a key pair."""
    client = get_client("ec2")
    response = client.create_key_pair(KeyName=name)
    return response
