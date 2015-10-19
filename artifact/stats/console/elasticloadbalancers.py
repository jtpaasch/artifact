# -*- coding: utf-8 -*-

"""A module to update console stats about elastic load balancers."""

from datetime import datetime

from artifact.stats.data.elasticloadbalancers import get_elastic_load_balancers


def data(widget):
    """Get data for the widget."""
    result = widget["data"]
    if not datetime.now().second % 5:
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
                    for listener in listeners:
                        protocol = listener.get("Protocol")
                        port = listener.get("LoadBalancerPort")
                        instance_protocol = listener.get("InstanceProtocol")
                        instance_port = listener.get("InstancePort")
                        ssl_cert = listener.get("SSLCertificateId")
                        final = protocol + ":" + port \
                                + " -> " \
                                + instance_protocol + ":" + instance_port \
                                + " " + ssl_cert
                        fieldset.append(final)
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
