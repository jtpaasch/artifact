# -*- coding: utf-8 -*-

"""A module to fetch stats about VCPs."""

from artifact.client import vpc


def get_vpcs():
    """Get data about VPCs."""
    data = vpc.get_vpcs()
    vpcs = data.get("Vpcs")
    return vpcs
