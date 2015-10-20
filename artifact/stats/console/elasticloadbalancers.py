# -*- coding: utf-8 -*-

"""A module to update console stats about elastic load balancers."""

from artifact.stats.console.utils import is_update_needed
from artifact.stats.data.elasticloadbalancers import get_elastic_load_balancers


def data(widget):
    """Get data for the widget."""
    result = widget["data"]
    if is_update_needed():
        elb_data = get_elastic_load_balancers()
        fieldsets = []
        for datum in elb_data:
            fieldset = []
            elb_name = datum.get("LoadBalancerName")
            if elb_name:
                fieldset.append(elb_name)
            dns_name = datum.get("DNSName")
            if dns_name:
                fieldset.append(dns_name)
            if datum.get("ListenerDescriptions"):
                listeners = datum.get("ListenerDescriptions")
                if listeners:
                    for listener_object in listeners:
                        listener = listener_object.get("Listener")
                        protocol = listener.get("Protocol")
                        port = listener.get("LoadBalancerPort")
                        instance_protocol = listener.get("InstanceProtocol")
                        instance_port = listener.get("InstancePort")
                        ssl_cert = listener.get("SSLCertificateId")
                        final = str(protocol) + ":" + str(port) \
                                + " -> " \
                                + str(instance_protocol) + ":" + str(instance_port)
                        fieldset.append(final)
            security_groups = datum.get("SecurityGroups")
            if security_groups:
                fieldset += security_groups
            if datum.get("Instances"):
                instance_list = datum.get("Instances")
                for instance in instance_list:
                    if instance.get("InstanceId"):
                        fieldset.append(instance.get("InstanceId"))
            if fieldset:
                fieldsets.append(fieldset)
        if fieldsets:
            result = fieldsets
    return result
