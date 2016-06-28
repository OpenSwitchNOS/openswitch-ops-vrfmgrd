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
Test case 6: Testing scale
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

from pytest import fixture
from vrf_configs import add_vrf, map_port_to_vrf
from vrf_configs import validate_configured_vrf, configure_ipaddress
from vrf_configs import wait_until_interface_up, delete_vrf
from vrf_configs import get_mapped_interface_to_vrf

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
hs1:1 -- sw1:81
sw1:82 -- sw2:92
sw1:83 -- sw2:93
sw1:84 -- sw2:94
sw1:85 -- sw2:95
sw1:86 -- sw2:96
sw1:87 -- sw2:97
sw1:88 -- sw2:98
sw2:91 -- hs2:1
"""

SW1_INTF1_IPV4_ADDR = "10.0.1.2/24"
SW1_INTF2_IPV4_ADDR = "10.0.2.1/24"
SW2_INTF1_IPV4_ADDR = "10.0.3.2/24"
SW2_INTF2_IPV4_ADDR = "10.0.2.2/24"
HS1_INTF1_IPV4_ADDR = "10.0.1.1/24"
HS2_INTF1_IPV4_ADDR = "10.0.3.1/24"

HS1_NETWORK_ADDR = "10.0.1.0/24"
HS2_NETWORK_ADDR = "10.0.3.0/24"

SW1_NEXTHOP_ADDR = SW2_INTF2_IPV4_ADDR.split('/')[0]  # "10.0.2.2"
SW2_NEXTHOP_ADDR = SW1_INTF2_IPV4_ADDR.split('/')[0]  # "10.0.2.1"
HS1_NEXTHOP_ADDR = SW1_INTF1_IPV4_ADDR.split('/')[0]  # "10.0.1.2"
HS2_NEXTHOP_ADDR = SW2_INTF1_IPV4_ADDR.split('/')[0]  # "10.0.3.2"

HS1 = HS1_INTF1_IPV4_ADDR.split('/')[0]  # "10.0.1.1"
HS2 = HS2_INTF1_IPV4_ADDR.split('/')[0]  # "10.0.3.1"

vrf_1 = "vrf1"
vrf_default = "vrf_default"

vrfs = []
for i in range(1, 65):
        vrfs.append('vrf'+str(i))

# Count is 'n' number of times
COUNT = 1


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

# vrf configuration in Switch 1
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
    for vrf_name in vrfs:
        add_vrf(sw2, vrf_name)

    output = sw2.libs.vtysh.show_vrf()
    for vrf_name in vrfs:
        retval = validate_configured_vrf(output, vrf_name)
        if retval:
            print("vrf {0} exist".format(vrf_name))
        else:
            assert False, "vrf {0} not exist".format(vrf_name)

    sw1_vrf_plus_port = []
    for portidx in sw1.ports.values():
        if portidx is '1' or portidx is '2':
            sw1_vrf_plus_port.append((str(portidx), 'vrf1'))
        else:
            sw1_vrf_plus_port.append((str(portidx),
                                     'vrf'+str(int(portidx) - 1)))

    sw2_vrf_plus_port = []
    for portidx in sw2.ports.values():
        if portidx is '1' or portidx is '2':
            sw2_vrf_plus_port.append((str(portidx), 'vrf1'))
        else:
            sw2_vrf_plus_port.append((str(portidx),
                                     'vrf'+str(int(portidx) - 1)))

# Mapping ports to vrf in Switch 1
    for interface, vrf in sw1_vrf_plus_port:
        map_port_to_vrf(sw1, vrf, interface)

# Mapping ports to vrf in Switch 2
    for interface, vrf in sw2_vrf_plus_port:
        map_port_to_vrf(sw2, vrf, interface)

# Configure ip address of vrf links in Switch 1
    for portlbl in sw1.ports.values():
        if portlbl is '1':
            configure_ipaddress(sw1, portlbl, SW1_INTF1_IPV4_ADDR)
        else:
            configure_ipaddress(sw1, portlbl, SW1_INTF2_IPV4_ADDR)

# Configure ip address of vrf links in Switch 2
    for portlbl in sw2.ports.values():
        if portlbl is '1':
            configure_ipaddress(sw2, portlbl, SW2_INTF1_IPV4_ADDR)
        else:
            configure_ipaddress(sw2, portlbl, SW2_INTF2_IPV4_ADDR)

# Configure IP and bring UP host 1 interfaces
    hs1.libs.ip.interface('1', addr=HS1_INTF1_IPV4_ADDR, up=True)

# Configure IP and bring UP host 2 interfaces
    hs2.libs.ip.interface('1', addr=HS2_INTF1_IPV4_ADDR, up=True)

# Wait until interfaces are up
    for switch in [sw1, sw2]:
        for portlbl in switch.ports.values():
            wait_until_interface_up(switch, portlbl)


def test_testing_vrf_scale(topology, configuration, step):
    """
    Testing scale.
    """
    sw1 = topology.get('sw1')
    sw2 = topology.get('sw2')
    hs1 = topology.get('hs1')
    hs2 = topology.get('hs2')

    assert sw1 is not None
    assert sw2 is not None
    assert hs1 is not None
    assert hs2 is not None

    # Set static routes in switches
    with sw1.libs.vtysh.Configure() as ctx:
        ctx.ip_route(HS2_NETWORK_ADDR, SW1_NEXTHOP_ADDR, vrf_name=vrf_1)

    with sw2.libs.vtysh.Configure() as ctx:
        ctx.ip_route(HS1_NETWORK_ADDR, SW2_NEXTHOP_ADDR, vrf_name=vrf_1)

    # Set gateway in hosts
    hs1.libs.ip.add_route('default', HS1_NEXTHOP_ADDR)
    hs2.libs.ip.add_route('default', HS2_NEXTHOP_ADDR)

    sleep(1)
    step('###### Step 1 - Test the ping through VRF RED ######')
    ping = hs1.libs.ping.ping(1, HS2)
    assert ping['transmitted'] == ping['received'] == 1

    for x in range(0, COUNT):
        step('###### Step 2 - Delete the 64 VRFs ######')
        for vrf_name in vrfs:
            delete_vrf(sw1, vrf_name)

        sleep(5)

        output = sw1.libs.vtysh.show_vrf()
        for vrf_name in vrfs:
            retval = validate_configured_vrf(output, vrf_name)
            if retval:
                assert False, "vrf {0} exist".format(vrf_name)
            else:
                print("vrf {0} successfully deleted".format(vrf_name))

        step('##### Step 3 - Validate Mapped ports are moved to'
             ' default vrf #####')
        output = get_mapped_interface_to_vrf(sw1, vrf_default)
        for portidx in sw1.ports.values():
            if portidx in output:
                step("##### Port {0} Mapped to {1} #####".format(portidx,
                     vrf_default))
            else:
                assert False, "Port {0} "
                "not Mapped to {1}".format(portidx, vrf_default)

        sleep(2)

        step('###### Step 4 - ReAdd the 64 VRFs ######')
        for vrf_name in vrfs:
            add_vrf(sw1, vrf_name)

        output = sw1.libs.vtysh.show_vrf()
        for vrf_name in vrfs:
            retval = validate_configured_vrf(output, vrf_name)
            if retval:
                print("vrf {0} exist".format(vrf_name))
            else:
                assert False, "vrf {0} not exist".format(vrf_name)

        vrf_plus_port = []
        for portidx in sw1.ports.values():
            if portidx is '1' or portidx is '2':
                vrf_plus_port.append((str(portidx), 'vrf1'))
            else:
                vrf_plus_port.append((str(portidx),
                                      'vrf'+str(int(portidx) - 1)))

        # Mapping ports to vrf in Switch 1
        step('###### Step 5 - Attaching interfaces to few vrfs  ######')
        for interface, vrf in vrf_plus_port:
            map_port_to_vrf(sw1, vrf, interface)

        # Configure ip address of vrf links in Switch 1
        for portlbl in sw1.ports.values():
            if portlbl is '1':
                configure_ipaddress(sw1, portlbl, SW1_INTF1_IPV4_ADDR)
            else:
                configure_ipaddress(sw1, portlbl, SW1_INTF2_IPV4_ADDR)

        # Wait until interfaces are up
        for portlbl in sw1.ports.values():
            wait_until_interface_up(sw1, portlbl)

        # Set static routes in Switch 1
        with sw1.libs.vtysh.Configure() as ctx:
            ctx.ip_route(HS2_NETWORK_ADDR, SW1_NEXTHOP_ADDR, vrf_name=vrf_1)

        sleep(5)
        step('###### Step 6 - Validate the ping through VRF RED'
             ' should not drop any ping packets ######')
        ping = hs1.libs.ping.ping(1, HS2)
        assert ping['transmitted'] == ping['received'] == 1

    step('##### TEST CASE vrf.06 PASSED')
