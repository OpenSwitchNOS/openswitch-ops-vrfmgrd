# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Test case 2: Verify the interface is moved out of the VRF
"""

from pytest import fixture
from .vrf_configs import add_vrf, map_port_to_vrf
from .vrf_configs import validate_configured_vrf, get_mapped_interface_to_vrf
from .vrf_configs import change_interface_status, configure_ipaddress
from .vrf_configs import unmap_port_to_vrf

from time import sleep

TOPOLOGY = """
# +-------+     +-------+
# |  sw1  |-----|  sw2  |
# +-------+     +-------+

# Nodes
[type=openswitch name="Switch 1"] sw1
[type=openswitch name="Switch 2"] sw2

# Links
sw1:1 -- sw2:1
sw1:2 -- sw2:2
sw1:3 -- sw2:3
sw1:4 -- sw2:4
"""

SW1_INTF_IPV4_ADDR = "10.0.0.1/24"

SW1_INTF1 = "1"
SW1_INTF2 = "2"
SW1_INTF3 = "3"
SW1_INTF4 = "4"

SW2_INTF_IPV4_ADDR = "10.0.0.2/24"

SW2_INTF1 = "1"
SW2_INTF2 = "2"
SW2_INTF3 = "3"
SW2_INTF4 = "4"

NEXTHOP_IP = SW2_INTF_IPV4_ADDR.split('/')[0]  # 10.0.0.2

vrf_default = "vrf_default"
vrf_red = "vrf_red"
vrf_green = "vrf_green"
vrf_blue = "vrf_blue"

port_up = "up"


@fixture(scope='module')
def configuration(topology, request):
    sw1 = topology.get("sw1")
    sw2 = topology.get("sw2")

    assert sw1 is not None
    assert sw2 is not None

# port for Switch 1
    p11 = sw1.ports["1"]
    p12 = sw1.ports["2"]
    p13 = sw1.ports["3"]
    p14 = sw1.ports["4"]

# port for Switch 2
    p21 = sw2.ports["1"]
    p22 = sw2.ports["2"]
    p23 = sw2.ports["3"]
    p24 = sw2.ports["4"]

# vrf configuration in Switch 1
    vrfs = [vrf_red, vrf_green, vrf_blue]
    for vrf_name in vrfs:
        add_vrf(sw1, vrf_name)

    output = sw1.libs.vtysh.show_vrf()
    for vrf_name in vrfs:
        retval = validate_configured_vrf(output, vrf_name)
        if retval:
            print("vrf {0} configured successfully".format(vrf_name))
        else:
            assert False, "vrf {0} creation failed".format(vrf_name)

# vrf configuration in Switch 2
    vrfs = [vrf_red, vrf_green, vrf_blue]
    for vrf_name in vrfs:
        add_vrf(sw2, vrf_name)

    output = sw2.libs.vtysh.show_vrf()
    for vrf_name in vrfs:
        retval = validate_configured_vrf(output, vrf_name)
        if retval:
            print("vrf {0} configured successfully".format(vrf_name))
        else:
            assert False, "vrf {0} creation failed".format(vrf_name)

# Mapping ports to vrf in Switch 1
    ports_vrf_red_sw1 = [p12]
    for interface in ports_vrf_red_sw1:
        map_port_to_vrf(sw1, vrf_red, interface)

    ports_vrf_green_sw1 = [p13]
    for interface in ports_vrf_green_sw1:
        map_port_to_vrf(sw1, vrf_green, interface)

    ports_vrf_blue_sw1 = [p14]
    for interface in ports_vrf_blue_sw1:
        map_port_to_vrf(sw1, vrf_blue, interface)

# Mapping ports to vrf in Switch 2
    ports_vrf_red_sw2 = [p22]
    for interface in ports_vrf_red_sw2:
        map_port_to_vrf(sw2, vrf_red, interface)

    ports_vrf_green_sw2 = [p23]
    for interface in ports_vrf_green_sw2:
        map_port_to_vrf(sw2, vrf_green, interface)

    ports_vrf_blue_sw2 = [p24]
    for interface in ports_vrf_blue_sw2:
        map_port_to_vrf(sw2, vrf_blue, interface)

# Change all interface status to UP presented in Switch 1 'vrf_default'
    ports_vrf_default_sw1 = [p11]
    for interface in ports_vrf_default_sw1:
        change_interface_status(sw1, interface, port_up)

# Change all interface status to UP presented in Switch 2 'vrf_default'
    ports_vrf_default_sw2 = [p21]
    for interface in ports_vrf_default_sw2:
        change_interface_status(sw2, interface, port_up)

# Configure ip address of default vrf links in Switch 1
    configure_ipaddress(sw1, SW1_INTF1, SW1_INTF_IPV4_ADDR)

# Configure ip address of vrf links in Switch 1
    configure_ipaddress(sw1, SW1_INTF2, SW1_INTF_IPV4_ADDR)
    configure_ipaddress(sw1, SW1_INTF3, SW1_INTF_IPV4_ADDR)
    configure_ipaddress(sw1, SW1_INTF4, SW1_INTF_IPV4_ADDR)

# Configure ip address of default vrf links in Switch 2
    configure_ipaddress(sw2, SW2_INTF1, SW2_INTF_IPV4_ADDR)

# Configure ip address of vrf links in Switch 2
    configure_ipaddress(sw2, SW2_INTF2, SW2_INTF_IPV4_ADDR)
    configure_ipaddress(sw2, SW2_INTF3, SW2_INTF_IPV4_ADDR)
    configure_ipaddress(sw2, SW2_INTF4, SW2_INTF_IPV4_ADDR)

# Validate configured ip address in Switch 1
    sw1('show ip interface {p11}'.format(**locals()))
    sw1('show ip interface {p12}'.format(**locals()))
    sw1('show ip interface {p13}'.format(**locals()))
    sw1('show ip interface {p14}'.format(**locals()))

# Validate configured ip address in Switch 2
    sw1('show ip interface {p21}'.format(**locals()))
    sw1('show ip interface {p22}'.format(**locals()))
    sw1('show ip interface {p23}'.format(**locals()))
    sw1('show ip interface {p24}'.format(**locals()))


def test_interface_moved_out_of_vrf(topology, configuration, step):
    """
    Test case:
        1- Add a port to VRF and verify the Nexthop ping from that VRF
        2- Move the attacted interface from that VRF to another VRF
        3- Verify the Nexthop ping is succeding for thet VRF. ping should fail
    """

    sw1 = topology.get("sw1")
    sw2 = topology.get("sw2")

    assert sw1 is not None
    assert sw2 is not None

# port for Switch 1
    p11 = sw1.ports["1"]
    p12 = sw1.ports["2"]
    p13 = sw1.ports["3"]
    p14 = sw1.ports["4"]

# port for Switch 2
    p21 = sw2.ports["1"]
    p22 = sw2.ports["2"]
    p23 = sw2.ports["3"]
    p24 = sw2.ports["4"]

# Defined ports for different vrf's in Switch 1
    ports_vrf_default_sw1 = [p11]
    ports_vrf_red_sw1 = [p12]
    ports_vrf_green_sw1 = [p13]
    ports_vrf_blue_sw1 = [p14]

# Defined ports for different vrf's in Switch 2
    ports_vrf_default_sw2 = [p21]
    ports_vrf_red_sw2 = [p22]
    ports_vrf_green_sw2 = [p23]
    ports_vrf_blue_sw2 = [p24]

# Validate Mapped ports in Switch 1 vrf's
    output = get_mapped_interface_to_vrf(sw1, vrf_default)
    for interface in ports_vrf_default_sw1:
        if interface in output:
            step("##### Port {0} Mapped to {1} #####".format(interface,
                 vrf_default))
        else:
            assert False, "Port {0} "
            "not Mapped to {1}".format(interface, vrf_default)

    output = get_mapped_interface_to_vrf(sw1, vrf_red)
    for interface in ports_vrf_red_sw1:
        if interface in output:
            step("##### Port {0} Mapped to {1} #####".format(interface,
                 vrf_red))
        else:
            assert False, "Port {0} "
            "not Mapped to {1}".format(interface, vrf_red)

    output = get_mapped_interface_to_vrf(sw1, vrf_green)
    for interface in ports_vrf_green_sw1:
        if interface in output:
            step("##### Port {0} Mapped to {1} #####".format(interface,
                 vrf_green))
        else:
            assert False, "Port {0} "
            "not Mapped to {1}".format(interface, vrf_green)

    output = get_mapped_interface_to_vrf(sw1, vrf_blue)
    for interface in ports_vrf_blue_sw1:
        if interface in output:
            step("##### Port {0} Mapped to {1} #####".format(interface,
                 vrf_blue))
        else:
            assert False, "Port {0} "
            "not Mapped to {1}".format(interface, vrf_blue)

# Validate Mapped ports in Switch 2 vrf's
    output = get_mapped_interface_to_vrf(sw2, vrf_default)
    for interface in ports_vrf_default_sw2:
        if interface in output:
            step("##### Port {0} Mapped to {1} #####".format(interface,
                 vrf_default))
        else:
            assert False, "Port {0} "
            "not Mapped to {1}".format(interface, vrf_default)

    output = get_mapped_interface_to_vrf(sw2, vrf_red)
    for interface in ports_vrf_red_sw2:
        if interface in output:
            step("##### Port {0} Mapped to {1} #####".format(interface,
                 vrf_red))
        else:
            assert False, "Port {0} "
            "not Mapped to {1}".format(interface, vrf_red)

    output = get_mapped_interface_to_vrf(sw2, vrf_green)
    for interface in ports_vrf_green_sw2:
        if interface in output:
            step("##### Port {0} Mapped to {1} #####".format(interface,
                 vrf_green))
        else:
            assert False, "Port {0} "
            "not Mapped to {1}".format(interface, vrf_green)

    output = get_mapped_interface_to_vrf(sw2, vrf_blue)
    for interface in ports_vrf_blue_sw2:
        if interface in output:
            step("##### Port {0} Mapped to {1} #####".format(interface,
                 vrf_blue))
        else:
            assert False, "Port {0} "
            "not Mapped to {1}".format(interface, vrf_blue)

    ping = sw1.libs.vtysh.ping(NEXTHOP_IP, vrf=vrf_red, count=1)
    assert ping['transmitted'] == ping['received'] == 1

# UnMapping ports from vrf in Switch 1
    for interface in ports_vrf_red_sw1:
        unmap_port_to_vrf(sw1, vrf_red, interface)

    for interface in ports_vrf_red_sw2:
        unmap_port_to_vrf(sw2, vrf_red, interface)

    sleep(2)
    vrf_new = 'vrf_new'
    for sw in [sw1, sw2]:
        add_vrf(sw, vrf_new)

        output = sw.libs.vtysh.show_vrf()
        retval = validate_configured_vrf(output, vrf_new)
        if retval:
            print("vrf {0} configured successfully in {1}".format(vrf_new, sw))
        else:
            assert False, "vrf {0} creation failed in {1}".format(vrf_new, sw)

    for interface in ports_vrf_red_sw1:
        map_port_to_vrf(sw1, vrf_new, interface)

    for interface in ports_vrf_red_sw2:
        map_port_to_vrf(sw2, vrf_new, interface)

    output = get_mapped_interface_to_vrf(sw1, vrf_new)
    for interface in ports_vrf_red_sw1:
        if interface in output:
            step("##### Port {0} Mapped to {1} #####".format(interface,
                 vrf_new))
        else:
            assert False, "Port {0} "
            "not Mapped to {1}".format(interface, vrf_new)

    output = get_mapped_interface_to_vrf(sw2, vrf_new)
    for interface in ports_vrf_red_sw2:
        if interface in output:
            step("##### Port {0} Mapped to {1} #####".format(interface,
                 vrf_new))
        else:
            assert False, "Port {0} "
            "not Mapped to {1}".format(interface, vrf_new)

    configure_ipaddress(sw1, p12, SW1_INTF_IPV4_ADDR)

    configure_ipaddress(sw2, p22, SW2_INTF_IPV4_ADDR)

    ping = sw1.libs.vtysh.ping(NEXTHOP_IP, vrf=vrf_new, count=1)
    assert ping['transmitted'] == ping['received'] == 1

    ping = sw1.libs.vtysh.ping(NEXTHOP_IP, vrf=vrf_red, count=1)
    assert ping['loss_pc'] > 0, "Ping not failed as expected reason -\
                                {0}".format(ping)

    step('##### TEST CASE vrf.02 PASSED #####')
