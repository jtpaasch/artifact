# -*- coding: utf-8 -*-

"""A module to update console stats about subnets."""

from artifact.stats.console.utils import is_update_needed
from artifact.stats.data.subnets import get_subnets


def data(widget):
    """Get data for the widget."""
    result = widget["data"]
    if is_update_needed():
        subnet_data = get_subnets()
        fieldsets = []
        for datum in subnet_data:
            fieldset = []
            subnet_name = "<Unnamed>"
            if datum.get("Tags"):
                tags = datum.get("Tags")
                for tag in tags:
                    if tag.get("Key") == "Name":
                        subnet_name = tag.get("Value")
            if subnet_name:
                fieldset.append(subnet_name)
            subnet_id = datum.get("SubnetId")
            if subnet_id:
                fieldset.append(subnet_id)
            vpc_id = datum.get("VpcId")
            if vpc_id:
                fieldset.append(vpc_id)
            cidr_block = datum.get("CidrBlock")
            if cidr_block:
                fieldset.append(cidr_block)
            if fieldset:
                fieldsets.append(fieldset)
        if fieldsets:
            result = fieldsets
    return result
