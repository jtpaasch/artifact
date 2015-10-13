# -*- coding: utf-8 -*-

"""A module for displaying stats in the console."""

import sys
import time

import curses
from curses import wrapper

from deploy.stats import autoscalinggroups
from deploy.stats import ec2
from deploy.stats import elasticloadbalancers
from deploy.stats import launchconfigurations
from deploy.stats import securitygroups
from deploy.stats import subnets
from deploy.stats import vpcs


def paint_box(stdscr, width, start_y, start_x, heading, fieldsets):
    """Paint a number of (text) fields in a box on the screen."""
    indent = 2
    padding = width - (len(heading) + 1)
    full_heading = " " + heading
    if padding > 0:
        for x in range(padding):
            full_heading += " "
    stdscr.addstr(start_y, start_x, full_heading, curses.A_REVERSE)
    start_y += 1
    for i, fieldset in enumerate(fieldsets):
        start_y += 1
        for line, field in enumerate(fieldset):
            if line == 0:
                stdscr.addstr(
                    start_y,
                    start_x,
                    "- " + str(field),
                    curses.A_BOLD)
            else:
                stdscr.addstr(
                    start_y,
                    start_x + indent,
                    str(field))
            start_y += 1
                


def show_vpcs(stdscr):
    """Fetch and paint stats about VCPs."""
    data = vpcs.get_vpcs()
    width = 20
    start_y = 0
    start_x = 0
    heading = "VPCs"
    fieldsets = []
    for i, datum in enumerate(data):
        vpc_id = datum.get("VpcId")
        cidr_block = datum.get("CidrBlock")
        status = datum.get("State")
        default = "Default VPC" if datum.get("IsDefault") else ""
        vpc_name = "<Unnamed>"
        if datum.get("Tags"):
            tags = datum.get("Tags")
            for tag in tags:
                if tag.get("Key") == "Name":
                    vpc_name = tag.get("Value")
        fieldsets.append([
            vpc_name,
            vpc_id,
            cidr_block,
            status,
            default,
            ])
    paint_box(stdscr, width, start_y, start_x, heading, fieldsets)


def show_subnets(stdscr):
    """Fetch and paint stats about subnets."""
    data = subnets.get_subnets()
    width = 20
    start_y = 0
    start_x = 25
    heading = "Subnets"
    fieldsets = []
    for datum in data:
        fieldset = []
        subnet_id = datum.get("SubnetId")
        vpc_id = datum.get("VpcId")
        cidr_block = datum.get("CidrBlock")
        availability_zone = datum.get("AvailabilityZone")
        subnet_name = "<Unnamed>"
        if datum.get("Tags"):
            tags = datum.get("Tags")
            for tag in tags:
                if tag.get("Key") == "Name":
                    subnet_name = tag.get("Value")
        fieldset.append(subnet_name)
        fieldset.append(subnet_id)
        fieldset.append(vpc_id)
        fieldset.append(cidr_block)
        fieldset.append(availability_zone)
        fieldsets.append(fieldset)
    paint_box(stdscr, width, start_y, start_x, heading, fieldsets)


def show_auto_scaling_groups(stdscr):
    """Fetch and paint stats about auto scaling groups."""
    data = autoscalinggroups.get_auto_scaling_groups()
    width = 20
    start_y = 0
    start_x = 50
    heading = "Auto Scale Groups"
    fieldsets = []
    for datum in data:
        fieldset = []
        group_name = datum.get("AutoScalingGroupName")
        launch_config = datum.get("LaunchConfigurationName")
        min_size = datum.get("MinSize")
        max_size = datum.get("MaxSize")
        desired_size = datum.get("DesiredCapacity")
        availability_zones = datum.get("AvailabilityZones")
        elastic_load_balancers = datum.get("LoadBalancerNames")
        instances = []
        instance_list = datum.get("Instances")
        if instance_list:
            for instance in instance_list:
                instance_id = instance.get("InstanceId")
                instance_zone = instance.get("AvailabilityZone")
                instance_status = instance.get("LifecycleState")
                instance_health = instance.get("HealthStatus")
                instances.append(instance_id)
                instances.append(instance_zone)
                instances.append(instance_status)
                instances.append(instance_health)
        fieldset.append(group_name)
        if launch_config:
            fieldset.append(launch_config)
        fieldset.append(str(min_size) + " " + str(max_size) + " " + str(desired_size))
        if availability_zones:
            fieldset += availability_zones
        if elastic_load_balancers:
            fieldset += elastic_load_balancers
        if instances:
            fieldset += instances
        fieldsets.append(fieldset)
    paint_box(stdscr, width, start_y, start_x, heading, fieldsets)


def show_ec2_instances(stdscr):
    """Fetch and paint stats about EC2 instances."""
    data = ec2.get_instances()
    width = 20
    start_y = 0
    start_x = 75
    heading = "Instances"
    fieldsets = []
    for i, datum in enumerate(data):
        fieldset = []
        instance_id = datum.get("InstanceId")
        status = datum.get("State").get("Name")
        if status == "terminated":
            continue
        private_dnsname = datum.get("PrivateDnsName")
        public_dnsname = datum.get("PublicDnsName")
        instance_type = datum.get("InstanceType")
        subnet_id = datum.get("SubnetId")
        vpc_id = datum.get("VpcId")
        private_ip = datum.get("PrivateIpAddress")
        public_ip = datum.get("PublicIpAddress")
        instance_name = "<Unnamed>"
        if datum.get("Tags"):
            tags = datum.get("Tags")
            for tag in tags:
                if tag.get("Key") == "Name":
                    instance_name = tag.get("Value")
        security_groups = []
        if datum.get("SecurityGroups"):
            sgs = datum.get("SecurityGroups")
            for sg in sgs:
                group_name = sg.get("GroupName")
                group_id = sg.get("GroupId")
                security_groups.append(group_name + " " + group_id)
        fieldset.append(instance_name)
        fieldset.append(instance_id)
        fieldset.append(instance_type)
        fieldset.append(status)
        if private_dnsname:
            fieldset.append(private_dnsname)
        if private_ip:
            fieldset.append(private_ip)
        if public_dnsname:
            fieldset.append(public_dnsname)
        if public_ip:
            fieldset.append(public_ip)
        fieldset.append(vpc_id)
        fieldset.append(subnet_id)
        if security_groups:
            fieldset.append(", ".join(security_groups))
        fieldsets.append(fieldset)
    paint_box(stdscr, width, start_y, start_x, heading, fieldsets)


def show_elastic_load_balancers(stdscr):
    """Fetch and paint stats about elastic load balancers."""
    data = elasticloadbalancers.get_elastic_load_balancers()
    width = 35
    start_y = 28
    start_x = 25
    heading = "Elastic Load Balancers"
    fieldsets = []
    for i, datum in enumerate(data):
        fieldset = []
        elb_name = datum.get("LoadBalancerName")
        dns_name = datum.get("DNSName")
        if datum.get("ListenerDescriptions"):
            listeners = datum.get("ListenerDescriptions")
            protocols = []
            ports = []
            instance_protocols = []
            instance_ports = []
            ssl_cert_ids = []
            if listeners:
                for listener in listeners:
                    protocol = listener.get("Protocol")
                    protocols.append(str(protocol))
                    port = listener.get("LoadBalancerPort")
                    ports.append(str(port))
                    instance_protocol = listener.get("InstanceProtocol")
                    instance_protocols.append(str(instance_protocol))
                    instance_port = listener.get("InstancePort")
                    instance_ports.append(str(instance_port))
                    ssl_cert_id = listener.get("SSLCertificateId")
                    ssl_cert_ids.append(str(ssl_cert_id))
        instances = []
        if datum.get("Instances"):
            instance_list = datum.get("Instances")
            for instance in instance_list:
                if instance.get("InstanceId"):
                    instances.append(instance.get("InstanceId"))
        if datum.get("SecurityGroups"):
            security_groups = datum.get("SecurityGroups")
        fieldset.append(elb_name)
        fieldset.append(dns_name)
        if protocols:
            fieldset += protocols
        if ports:
            fieldset += ports
        if instance_protocols:
            fieldset += instance_protocols
        if instance_ports:
            fieldset += instance_ports
        if ssl_cert_ids:
            fieldset += ssl_cert_ids
        if security_groups:
            fieldset += security_groups
        if instances:
            fieldset += instances
        fieldsets.append(fieldset)
    paint_box(stdscr, width, start_y, start_x, heading, fieldsets)


def show_launch_configurations(stdscr):
    """Fetch and paint stats about launch configurations."""
    data = launchconfigurations.get_launch_configurations()
    width = 20
    start_y = 9
    start_x = 0
    heading = "Launch Configs"
    fieldsets = []
    for i, datum in enumerate(data):
        fieldset = []
        config_name = datum.get("LaunchConfigurationName")
        ami_id = datum.get("ImageId")
        key_name = datum.get("KeyName")
        security_groups = datum.get("SecurityGroups")
        instance_type = datum.get("InstanceType")
        role_profile = datum.get("IamInstanceProfile")
        fieldset.append(config_name)
        fieldset.append(ami_id)
        fieldset.append(instance_type)
        if key_name:
            fieldset.append(key_name)
        if security_groups:
            fieldset.append(", ".join(security_groups))
        if role_profile:
            fieldset.append(role_profile)
        fieldsets.append(fieldset)
    paint_box(stdscr, width, start_y, start_x, heading, fieldsets)


def show_security_groups(stdscr):
    """Fetch and paint stats about security groups."""
    data = securitygroups.get_security_groups()
    width = 20
    start_y = 18
    start_x = 0
    heading = "Security Groups"
    fieldsets = []
    for i, datum in enumerate(data):
        fieldset = []
        group_name = datum.get("GroupName")
        group_id = datum.get("GroupId")
        owner_id = datum.get("OwnerId")
        ingress_rules = []
        ingress_data = datum.get("IpPermissions")
        if ingress_data:
            for rule_data in ingress_data:
                rule = rule_data.get("IpProtocol")
                if rule_data.get("FromPort"):
                    rule += " "
                    rule += str(rule_data.get("FromPort"))
                    rule += " -"
                if rule_data.get("ToPort"):
                    rule += " "
                    rule += str(rule_data.get("ToPort"))
                ingress_rules.append(rule)
                ip_ranges = rule_data.get("IpRanges")
                if ip_ranges:
                    for ip_range in ip_ranges:
                        if ip_range.get("CidrIp"):
                            ingress_rules.append(ip_range.get("CidrIp"))
        egress_rules = []
        egress_data = datum.get("IpPermissionsEgress")
        if egress_data:
            for rule_data in egress_data:
                rule = rule_data.get("IpProtocol")
                if rule_data.get("FromPort"):
                    rule += " "
                    rule += str(rule_data.get("FromPort"))
                    rule += " -"
                if rule_data.get("ToPort"):
                    rule += " "
                    rule += str(rule_data.get("ToPort"))
                egress_rules.append(rule)
                ip_ranges = rule_data.get("IpRanges")
                if ip_ranges:
                    for ip_range in ip_ranges:
                        if ip_range.get("CidrIp"):
                            egress_rules.append(ip_range.get("CidrIp"))
        fieldset.append(group_name)
        fieldset.append(group_id)
        if owner_id:
            fieldset.append(owner_id)
        if ingress_rules:
            fieldset.append("Inbound rules:")
            fieldset += ingress_rules
        if egress_rules:
            fieldset.append("Outbound rules:")
            fieldset += egress_rules
        fieldsets.append(fieldset)
    paint_box(stdscr, width, start_y, start_x, heading, fieldsets)


def event_loop(stdscr):
    """The main event loop."""
    curses.curs_set(False)  # Hide cursor.
    while True:
        stdscr.clear()
        show_vpcs(stdscr)
        show_subnets(stdscr)
        show_ec2_instances(stdscr)
        show_launch_configurations(stdscr)
        show_elastic_load_balancers(stdscr)
        show_auto_scaling_groups(stdscr)
        show_security_groups(stdscr)
        stdscr.refresh()
        time.sleep(5)


def start():
    """Start the event loop."""
    try:
        wrapper(event_loop)
    except KeyboardInterrupt:
        sys.exit(1)
