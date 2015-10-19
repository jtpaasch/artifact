# -*- coding: utf-8 -*-

"""A module to update console stats about subnets."""

from datetime import datetime

from artifact.stats.data.ec2 import get_instances


def data(widget):
    """Get data for the widget."""
    result = widget["data"]
    if not datetime.now().second % 5:
        ec2_data = get_instances()
        fieldsets = []
        for datum in ec2_data:
            fieldset = []
            instance_name = "<Unnamed>"
            if datum.get("Tags"):
                tags = datum.get("Tags")
                for tag in tags:
                    if tag.get("Key") == "Name":
                        instance_name = tag.get("Value")
            if instance_name:
                fieldset.append(instance_name)
            instance_type = datum.get("InstanceType")
            if instance_type:
                fieldset.append(instance_type)
            status = datum.get("State").get("Name")
            if status == "terminated":
                continue
            else:
                fieldset.append(status)
            private_dnsname = datum.get("PrivateDnsName")
            if private_dnsname:
                fieldset.append(private_dnsname)
            private_ip = datum.get("PrivateIpAddress")
            if private_ip:
                fieldset.append(private_ip)
            public_dnsname = datum.get("PublicDnsName")
            if public_dnsname:
                fieldset.append(public_dnsname)
            public_ip = datum.get("PublicIpAddress")
            if public_ip:
                fieldset.append(public_ip)
            vpc_id = datum.get("VpcId")
            if vpc_id:
                fieldset.append(vpc_id)
            subnet_id = datum.get("SubnetId")
            if subnet_id:
                fieldset.append(subnet_id)
            security_groups = []
            if datum.get("SecurityGroups"):
                sgs = datum.get("SecurityGroups")
                for sg in sgs:
                    group_name = sg.get("GroupName")
                    group_id = sg.get("GroupId")
                    security_groups.append(group_id + " " + group_name)
            if security_groups:
                fieldset += security_groups
            if fieldset:
                fieldsets.append(fieldset)
        if fieldsets:
            result = fieldsets
    return result
