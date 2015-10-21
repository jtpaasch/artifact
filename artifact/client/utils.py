# -*- coding: utf-8 -*-

"""Utilities for other modules."""

import boto3


def get_client(service):
    """Get a Boto3 session client."""
    boto3_session = boto3.Session()
    return boto3_session.client(service)


def get_file_contents(filepath):
    """Get the contents of a file."""
    with open(filepath) as f:
        return f.read()
