# -*- coding: utf-8 -*-

"""A module to update console stats about VCPs."""

from artifact.stats.console.utils import is_update_needed
from artifact.stats.data.vpcs import get_vpcs


def data(widget):
    """Get data for the widget."""
    result = widget["data"]
    if is_update_needed():
        vpc_data = get_vpcs()
        fieldsets = []
        for datum in vpc_data:
            fieldset = []
            vpc_name = "<Unnamed>"
            if datum.get("Tags"):
                tags = datum.get("Tags")
                for tag in tags:
                    if tag.get("Key") == "Name":
                        vpc_name = tag.get("Value")
            if vpc_name:
                fieldset.append(vpc_name)
            vpc_id = datum.get("VpcId")
            if vpc_id:
                fieldset.append(vpc_id)
            cidr_block = datum.get("CidrBlock")
            if cidr_block:
                fieldset.append(cidr_block)
            status = datum.get("State")
            if status:
                fieldset.append(status)
            default = "Default VPC" if datum.get("IsDefault") else None
            if default:
                fieldset.append(default)
            if fieldset:
                fieldsets.append(fieldset)
        if fieldsets:
            result = fieldsets
    return result
