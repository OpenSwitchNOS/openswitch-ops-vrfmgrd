# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2017 Hewlett Packard Enterprise Development LP
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
Test case 5: Interface attach/detach to/from VRF and testing data path
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

from pytest import fixture
from .vrf_configs import add_vrf, map_port_to_vrf
from .vrf_configs import validate_configured_vrf, configure_ipaddress
from .vrf_configs import wait_until_interface_up, unmap_port_to_vrf
from pytest import set_trace
from time import sleep


TOPOLOGY = """
# +-------+                                 +-------+
# |       |     +-------+     +-------+     |       |
# |  hs1  <----->  sw1  <----->  sw2  <----->  hs2  |
# |       |     +-------+     +-------+     |       |
# +-------+                                 +-------+

# Nodes
[type=openswitch name="Switch 1"] sw1
[type=openswitch name="Switch 2"] sw2
[type=host name="Host 1"] hs1
[type=host name="Host 2"] hs2

# Links
hs1:1 -- sw1:71
sw1:72 -- sw2:82
sw2:83 -- hs2:1
"""

SW1_INTF1_IPV4_ADDR = "10.0.1.2/24"
SW1_INTF2_IPV4_ADDR = "10.0.2.1/24"
SW2_INTF2_IPV4_ADDR = "10.0.2.2/24"
SW2_INTF3_IPV4_ADDR = "10.0.3.2/24"
HS1_INTF1_IPV4_ADDR = "10.0.1.1/24"
HS2_INTF1_IPV4_ADDR = "10.0.3.1/24"

HS1_NETWORK_ADDR = "10.0.1.0/24"
HS2_NETWORK_ADDR = "10.0.3.0/24"

SW1_NEXTHOP_ADDR = SW2_INTF2_IPV4_ADDR.split('/')[0]  # "10.0.2.2"
SW2_NEXTHOP_ADDR = SW1_INTF2_IPV4_ADDR.split('/')[0]  # "10.0.2.1"
HS1_NEXTHOP_ADDR = SW1_INTF1_IPV4_ADDR.split('/')[0]  # "10.0.1.2"
HS2_NEXTHOP_ADDR = SW2_INTF3_IPV4_ADDR.split('/')[0]  # "10.0.3.2"

HS1 = HS1_INTF1_IPV4_ADDR.split('/')[0]  # "10.0.1.1"
HS2 = HS2_INTF1_IPV4_ADDR.split('/')[0]  # "10.0.3.1"

vrf_default = "vrf_default"
vrf_red = "vrf_red"

# Count is 'n' number of times
COUNT = 2


@fixture(scope='module')
def configuration(topology, request):
    sw1 = topology.get("sw1")
    sw2 = topology.get("sw2")
    hs1 = topology.get('hs1')
    hs2 = topology.get('hs2')

    assert sw1 is not None
    assert sw2 is not None
    assert hs1 is not None
    assert hs2 is not None

# port for Switch 1
    p11 = sw1.ports["71"]
    p12 = sw1.ports["72"]

# port for Switch 2
    p22 = sw2.ports["82"]
    p23 = sw2.ports["83"]

# vrf configuration in Switch 1
    vrfs = [vrf_red]
    for vrf_name in vrfs:
        add_vrf(sw1, vrf_name)

    output = sw1.libs.vtysh.show_vrf()
    for vrf_name in vrfs:
        retval = validate_configured_vrf(output, vrf_name)
        if retval:
            print("vrf {0} exist".format(vrf_name))
        else:
            assert False, "vrf {0} not exist".format(vrf_name)

# vrf configuration in Switch 2
    vrfs = [vrf_red]
    for vrf_name in vrfs:
        add_vrf(sw2, vrf_name)

    output = sw2.libs.vtysh.show_vrf()
    for vrf_name in vrfs:
        retval = validate_configured_vrf(output, vrf_name)
        if retval:
            print("vrf {0} exist".format(vrf_name))
        else:
            assert False, "vrf {0} not exist".format(vrf_name)

# Mapping ports to vrf in Switch 1
    ports_vrf_red_sw1 = [p11, p12]
    for interface in ports_vrf_red_sw1:
        map_port_to_vrf(sw1, vrf_red, interface)

# Mapping ports to vrf in Switch 2
    ports_vrf_red_sw2 = [p22, p23]
    for interface in ports_vrf_red_sw2:
        map_port_to_vrf(sw2, vrf_red, interface)

# Configure ip address of vrf links in Switch 1
    configure_ipaddress(sw1, p11, SW1_INTF1_IPV4_ADDR)
    configure_ipaddress(sw1, p12, SW1_INTF2_IPV4_ADDR)

# Configure ip address of vrf links in Switch 2
    configure_ipaddress(sw2, p22, SW2_INTF2_IPV4_ADDR)
    configure_ipaddress(sw2, p23, SW2_INTF3_IPV4_ADDR)

# Configure IP and bring UP host 1 interfaces
    hs1.libs.ip.interface('1', addr=HS1_INTF1_IPV4_ADDR, up=True)

# Configure IP and bring UP host 2 interfaces
    hs2.libs.ip.interface('1', addr=HS2_INTF1_IPV4_ADDR, up=True)

# Wait until interfaces are up
    for switch, portlbl in [(sw1, p11), (sw1, p12), (sw2, p22), (sw2, p23)]:
        wait_until_interface_up(switch, portlbl)


def test_ping_while_port_attach_detach_vrf(topology, configuration, step):
    """
    Set network addresses and static routes between nodes and ping h2 from h1.
    """
    sw1 = topology.get('sw1')
    sw2 = topology.get('sw2')
    hs1 = topology.get('hs1')
    hs2 = topology.get('hs2')

    assert sw1 is not None
    assert sw2 is not None
    assert hs1 is not None
    assert hs2 is not None

    # port for Switch 1
    p11 = sw1.ports["71"]
    p12 = sw1.ports["72"]

    # port for Switch 2
    p22 = sw2.ports["82"]
    p23 = sw2.ports["83"]

    # Set static routes in switches
    with sw1.libs.vtysh.Configure() as ctx:
        ctx.ip_route(HS2_NETWORK_ADDR, SW1_NEXTHOP_ADDR, vrf_name=vrf_red)

    with sw2.libs.vtysh.Configure() as ctx:
        ctx.ip_route(HS1_NETWORK_ADDR, SW2_NEXTHOP_ADDR, vrf_name=vrf_red)

    # Set gateway in hosts
    hs1.libs.ip.add_route('default', HS1_NEXTHOP_ADDR)
    hs2.libs.ip.add_route('default', HS2_NEXTHOP_ADDR)
    step('##### Step 1: Test the ping through test cases through VRF RED')
    sleep(1)
    ping = hs1.libs.ping.ping(1, HS2)
    assert ping['transmitted'] == ping['received'] == 1

    for x in range(0, COUNT):
        step('##### Step 2: Detach the interfaces to VRF RED')
        ports_vrf_red_sw1 = [p11, p12]
        for interface in ports_vrf_red_sw1:
            unmap_port_to_vrf(sw1, vrf_red, interface)

        ports_vrf_red_sw2 = [p22, p23]
        for interface in ports_vrf_red_sw2:
            unmap_port_to_vrf(sw2, vrf_red, interface)

        # Configure ip address of vrf links in Switch 1
        configure_ipaddress(sw1, p11, SW1_INTF1_IPV4_ADDR)
        configure_ipaddress(sw1, p12, SW1_INTF2_IPV4_ADDR)

        # Configure ip address of vrf links in Switch 2
        configure_ipaddress(sw2, p22, SW2_INTF2_IPV4_ADDR)
        configure_ipaddress(sw2, p23, SW2_INTF3_IPV4_ADDR)
        sleep(2)
        # Set static routes in switches
        with sw1.libs.vtysh.Configure() as ctx:
            ctx.ip_route(HS2_NETWORK_ADDR, SW1_NEXTHOP_ADDR)

        with sw2.libs.vtysh.Configure() as ctx:
            ctx.ip_route(HS1_NETWORK_ADDR, SW2_NEXTHOP_ADDR)

        step('##### Step 3: Test the ping through test cases through '
             'vrf_default, ping should get success')
        sleep(2)
        ping = hs1.libs.ping.ping(1, HS2)
        assert ping['transmitted'] == ping['received'] == 1

        step('##### Step 4: Attach the same interfaces to VRF RED')
        for interface in ports_vrf_red_sw1:
            map_port_to_vrf(sw1, vrf_red, interface)

        for interface in ports_vrf_red_sw2:
            map_port_to_vrf(sw2, vrf_red, interface)

        # Configure ip address of vrf links in Switch 1
        configure_ipaddress(sw1, p11, SW1_INTF1_IPV4_ADDR)
        configure_ipaddress(sw1, p12, SW1_INTF2_IPV4_ADDR)

        # Configure ip address of vrf links in Switch 2
        configure_ipaddress(sw2, p22, SW2_INTF2_IPV4_ADDR)
        configure_ipaddress(sw2, p23, SW2_INTF3_IPV4_ADDR)

        # Wait until interfaces are up
        for switch, portlbl in [(sw1, p11), (sw1, p12),
                                (sw2, p22), (sw2, p23)]:
            wait_until_interface_up(switch, portlbl)

        # Set static routes in Switch 1
        with sw1.libs.vtysh.Configure() as ctx:
            ctx.ip_route(HS2_NETWORK_ADDR, SW1_NEXTHOP_ADDR, vrf_name=vrf_red)

        with sw2.libs.vtysh.Configure() as ctx:
            ctx.ip_route(HS1_NETWORK_ADDR, SW2_NEXTHOP_ADDR, vrf_name=vrf_red)

        step('##### Step 5: Test the ping through test cases through VRF RED')
        sleep(2)
        set_trace()
        ping = hs1.libs.ping.ping(1, HS2)
        assert ping['transmitted'] == ping['received'] == 1

    step('##### TEST CASE vrf.05 PASSED')
