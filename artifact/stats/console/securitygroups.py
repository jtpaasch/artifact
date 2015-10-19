# -*- coding: utf-8 -*-

"""A module to update console stats about securitygroups."""

from artifact.stats.console.utils import is_update_needed
from artifact.stats.data.securitygroups import get_security_groups


def data(widget):
    """Get data for the widget."""
    result = widget["data"]
    if is_update_needed():
        sg_data = get_security_groups()
        fieldsets = []
        for datum in sg_data:
            fieldset = []
            group_name = datum.get("GroupName")
            if group_name:
                fieldset.append(group_name)
            group_id = datum.get("GroupId")
            if group_id:
                fieldset.append(group_id)
            owner_id = datum.get("OwnerId")
            if owner_id:
                fieldset.append(owner_id)
            ingress_rules = []
            ingress_data = datum.get("IpPermissions")
            if ingress_data:
                for rule_data in ingress_data:
                    rule = rule_data.get("IpProtocol")
                    if rule and rule_data.get("FromPort"):
                        rule += " "
                        rule += str(rule_data.get("FromPort"))
                        rule += " -"
                    if rule and rule_data.get("ToPort"):
                        rule += " "
                        rule += str(rule_data.get("ToPort"))
                    if rule:
                        ingress_rules.append(rule)
                    ip_ranges = rule_data.get("IpRanges")
                    if ip_ranges:
                        for ip_range in ip_ranges:
                            if ip_range.get("CidrIp"):
                                cidr_block = ip_range.get("CidrIp")
                                ingress_rules.append(cidr_block)
            if ingress_rules:
                fieldset += ingress_rules
            egress_rules = []
            egress_data = datum.get("IpPermissionsEgress")
            if egress_data:
                for rule_data in egress_data:
                    rule = rule_data.get("FromPort")
                    if rule and rule_data.get("FromPort"):
                        rule += " "
                        rule += str(rule_data.get("FromPort"))
                        rule += " -"
                    if rule and rule_data.get("ToPort"):
                        rule += " "
                        rule += str(rule_data.get("ToPort"))
                    if rule:
                        egress_rules.append(rule)
                    if_ranges = rule_data.get("IpRanges")
                    if ip_ranges:
                        for ip_range in ip_ranges:
                            if ip_range.get("CidrIp"):
                                cidr_block = ip_range.get("CidrIp")
                                egress_rules.append(cidr_block)
            if egress_rules:
                fieldset += egress_rules
            if fieldset:
                fieldsets.append(fieldset)
        if fieldsets:
            result = fieldsets
    return result
