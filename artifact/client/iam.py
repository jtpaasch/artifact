# -*- coding: utf-8 -*-

"""A module to handle IAM groups and users."""

from artifact.client.utils import get_client


def create_user(username):
    """Create a user."""
    client = get_client("iam")
    response = client.create_user(UserName=username)
    return response


def get_user(username):
    """Get info about a user."""
    client = get_client("iam")
    response = client.get_user(UserName=username)
    return response


def delete_user(username):
    """Delete a user."""
    client = get_client("iam")
    response = client.delete_user(UserName=username)
    return response


def create_group(name):
    """Create a group."""
    client = get_client("iam")
    response = client.create_group(GroupName=name)
    return response


def get_group(name):
    """Get info about a group."""
    client = get_client("iam")
    response = client.get_group(GroupName=name)
    return response


def delete_group(name):
    """Delete a group."""
    client = get_client("iam")
    response = client.delete_group(GroupName=name)
    return response


def create_policy(name, contents):
    """Create a policy."""
    client = get_client("iam")
    response = client.create_policy(
        PolicyName=name,
        PolicyDocument=contents)
    return response


def get_policy(arn):
    """Get info about a policy."""
    client = get_client("iam")
    response = client.get_policy(PolicyArn=arn)
    return response


def delete_policy(arn):
    """Delete a policy."""
    client = get_client("iam")
    response = client.delete_policy(PolicyArn=arn)
    return response


def readonly_iam_policy():
    """Generate a readonly policy."""
    return '''{
        "Version": "2012-10-17",
        "Statement": {
            "Effect": "Allow",
            "Action": [
                "iam:Get*",
                "iam:List*"
            ],
            "Resource": "*"
        }
    }
    '''


def attach_group_policy(groupname, policyarn):
    """Attach a policy to a group."""
    client = get_client("iam")
    response = client.attach_group_policy(
        GroupName=groupname,
        PolicyArn=policyarn)
    return response


def create_role(name, contents):
    """Create a role."""
    client = get_client("iam")
    response = client.create_role(
        RoleName=name,
        AssumeRolePolicyDocument=contents)
    return response


def get_role(name):
    """Get info about a role."""
    client = get_client("iam")
    response = client.get_role(RoleName=name)
    return response


def delete_role(name):
    """Delete a role."""
    client = get_client("iam")
    response = client.delete_role(RoleName=name)
    return response
