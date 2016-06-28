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
Test case 10: L3 Interface deletion/movement -- proper clean ups for
subinterface and loopback interface
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

from pytest import fixture
from vrf_configs import add_vrf, map_port_to_vrf
from vrf_configs import validate_configured_vrf, configure_ipaddress
from vrf_configs import wait_until_interface_up, unmap_port_to_vrf
from vrf_configs import configure_loopbackinterface
from vrf_configs import map_loobackinterface_to_vrf
from vrf_configs import unmap_loobackinterface_from_vrf
from vrf_configs import configure_subinterface
from vrf_configs import configure_subinterface_ip
from vrf_configs import map_subinterface_to_vrf
from vrf_configs import unmap_subinterface_from_vrf
from vrf_configs import enable_dot1q_for_subinterface
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
sw2:85 -- hs2:1
"""

SW1_INTF1_IPV4_ADDR = "10.0.1.2/24"  # sw1-71 -- p11
SW1_INTF2_IPV4_ADDR = "10.0.2.1/24"  # sw1-72 -- p12
SW2_INTF2_IPV4_ADDR = "10.0.2.2/24"  # sw2-82 -- p22
SW2_INTF3_IPV4_ADDR = "10.0.3.2/24"  # sw2-85 -- p25

SW1_LBK_INTF_IPV4_ADDR = "10.10.10.10/32"
SW2_LBK_INTF_IPV4_ADDR = "20.20.20.20/32"
SW1_SUB_INTF21_IPV4_ADDR = "10.0.10.1/24"
SW1_SUB_INTF22_IPV4_ADDR = "10.0.11.1/24"
SW1_SUB_INTF23_IPV4_ADDR = "10.0.12.1/24"
SW2_SUB_INTF21_IPV4_ADDR = "10.0.10.2/24"
SW2_SUB_INTF22_IPV4_ADDR = "10.0.11.2/24"
SW2_SUB_INTF23_IPV4_ADDR = "10.0.12.2/24"

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

    # port for Switch 1
    p11 = sw1.ports["71"]
    p12 = sw1.ports["72"]

    # port for Switch 2
    p22 = sw2.ports["82"]
    p25 = sw2.ports["85"]

    # vrf configuration in Switch 1
    vrfs = [vrf_red]
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
    vrfs = [vrf_red]
    for vrf_name in vrfs:
        add_vrf(sw2, vrf_name)

    output = sw2.libs.vtysh.show_vrf()
    for vrf_name in vrfs:
        retval = validate_configured_vrf(output, vrf_name)
        if retval:
            print("vrf {0} configured successfully".format(vrf_name))
        else:
            assert False, "vrf {0} creation failed".format(vrf_name)

    # Loopback and subinterface config for switch 1
    configure_loopbackinterface(sw1, '1', SW1_LBK_INTF_IPV4_ADDR)
    subinterface_list = [1, 2, 3]
    for subinterface in subinterface_list:
        configure_subinterface(sw1, p12, subinterface)
    sleep(2)
    output = sw1.libs.vtysh.show_interface_subinterface(p12)
    for subinterface in subinterface_list:
        if subinterface in output.keys():
            continue
        else:
            assert False, "Subinterface does not exist"

    # Mapping ports to vrf in Switch 1
    for interface in [p11, p12, 'loopback1']:
        if interface is 'loopback1':
            map_loobackinterface_to_vrf(sw1, vrf_red, '1')
        elif interface is p12:
            map_port_to_vrf(sw1, vrf_red, interface)
            for subinterface in subinterface_list:
                map_subinterface_to_vrf(sw1, vrf_red, interface,
                                        subinterface)
        else:
            map_port_to_vrf(sw1, vrf_red, interface)
    sleep(2)
    output = sw1.libs.vtysh.show_vrf()
    for interface in [p11, p12, 'loopback1']:
        if interface is p12:
            for subinterface in subinterface_list:
                tempsub = str(interface)
                tempsub += '.'
                tempsub += str(subinterface)
                if tempsub in output[vrf_red].keys():
                    continue
                else:
                    assert False, (
                        "interface {0} did not "
                        "move from vrf_default to vrf_red"
                    ).format(tempsub)
        if interface in output[vrf_red].keys():
            continue
        else:
            assert False, (
                "interface {0} did not "
                "move from vrf_default to vrf_red"
            ).format(interface)

    # Loopback and subinterface config for switch 2
    configure_loopbackinterface(sw2, '1', SW2_LBK_INTF_IPV4_ADDR)

    for subinterface in subinterface_list:
        configure_subinterface(sw2, p22, subinterface)
    sleep(2)
    output = sw2.libs.vtysh.show_interface_subinterface(p22)
    for subinterface in subinterface_list:
        if subinterface in output.keys():
            continue
        else:
            assert False, "Subinterface does not exist"

    # Mapping ports to vrf in Switch 2
    for interface in [p22, p25, 'loopback1']:
        if interface is 'loopback1':
            map_loobackinterface_to_vrf(sw2, vrf_red, '1')
        elif interface is p22:
            map_port_to_vrf(sw2, vrf_red, interface)
            for subinterface in subinterface_list:
                map_subinterface_to_vrf(sw2, vrf_red, interface,
                                        subinterface)
        else:
            map_port_to_vrf(sw2, vrf_red, interface)
    sleep(2)
    output = sw2.libs.vtysh.show_vrf()
    for interface in [p22, p25, 'loopback1']:
        if interface is p22:
            for subinterface in subinterface_list:
                tempsub = str(interface)
                tempsub += '.'
                tempsub += str(subinterface)
                if tempsub in output[vrf_red].keys():
                    continue
                else:
                    assert False, (
                        "interface {0} did not move from "
                        "vrf_default to vrf_red"
                    ).format(tempsub)
        if interface in output[vrf_red].keys():
            continue
        else:
            assert False, (
                "interface {0} did not "
                "move from vrf_default to vrf_red"
            ).format(interface)

    sleep(2)

    enable_dot1q_for_subinterface(sw1, p12, '1', '10')
    enable_dot1q_for_subinterface(sw1, p12, '2', '20')
    enable_dot1q_for_subinterface(sw1, p12, '3', '30')

    enable_dot1q_for_subinterface(sw2, p22, '1', '10')
    enable_dot1q_for_subinterface(sw2, p22, '2', '20')
    enable_dot1q_for_subinterface(sw2, p22, '3', '30')

    # Configure ip address of vrf links in Switch 1
    configure_ipaddress(sw1, p11, SW1_INTF1_IPV4_ADDR)
    configure_ipaddress(sw1, p12, SW1_INTF2_IPV4_ADDR)
    configure_loopbackinterface(sw1, '1', SW1_LBK_INTF_IPV4_ADDR)
    configure_subinterface_ip(sw1, p12, '1', SW1_SUB_INTF21_IPV4_ADDR)
    configure_subinterface_ip(sw1, p12, '2', SW1_SUB_INTF22_IPV4_ADDR)
    configure_subinterface_ip(sw1, p12, '3', SW1_SUB_INTF23_IPV4_ADDR)
    output = sw2.libs.vtysh.show_vrf()
    # Configure ip address of vrf links in Switch 2
    configure_ipaddress(sw2, p22, SW2_INTF2_IPV4_ADDR)
    configure_ipaddress(sw2, p25, SW2_INTF3_IPV4_ADDR)
    configure_loopbackinterface(sw2, '1', SW2_LBK_INTF_IPV4_ADDR)
    configure_subinterface_ip(sw2, p22, '1', SW2_SUB_INTF21_IPV4_ADDR)
    configure_subinterface_ip(sw2, p22, '2', SW2_SUB_INTF22_IPV4_ADDR)
    configure_subinterface_ip(sw2, p22, '3', SW2_SUB_INTF23_IPV4_ADDR)

    # Configure IP and bring UP host 1 interfaces
    hs1.libs.ip.interface('1', addr=HS1_INTF1_IPV4_ADDR, up=True)

    # Configure IP and bring UP host 2 interfaces
    hs2.libs.ip.interface('1', addr=HS2_INTF1_IPV4_ADDR, up=True)

    # Wait until interfaces are up
    for switch, portlbl in [(sw1, p11), (sw1, p12),
                            (sw2, p22), (sw2, p25)]:
        wait_until_interface_up(switch, portlbl)


def test_subint_loopbackint_for_vrf(topology, configuration, step):

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
    p25 = sw2.ports["85"]

    # Set static routes in switches
    with sw1.libs.vtysh.Configure() as ctx:
        ctx.ip_route(HS2_NETWORK_ADDR, '10.0.10.2', vrf_name=vrf_red)

    with sw2.libs.vtysh.Configure() as ctx:
        ctx.ip_route(HS1_NETWORK_ADDR, '10.0.10.1', vrf_name=vrf_red)

    with sw1.libs.vtysh.Configure() as ctx:
        ctx.ip_route('20.20.20.20/32', '10.0.10.2', vrf_name=vrf_red)

    with sw2.libs.vtysh.Configure() as ctx:
        ctx.ip_route('10.10.10.10/32', '10.0.10.1', vrf_name=vrf_red)

    # Set gateway in hosts
    hs1.libs.ip.add_route('default', HS1_NEXTHOP_ADDR)
    hs2.libs.ip.add_route('default', HS2_NEXTHOP_ADDR)
    sleep(1)
    step('##### Step 1: Test the ping through test cases'
         'through VRF RED #####')
    ping = hs1.libs.ping.ping(1, HS2)
    assert ping['transmitted'] == ping['received'] == 1
    ping = sw1.libs.vtysh.ping(SW2_SUB_INTF21_IPV4_ADDR.split('/')[0],
                               vrf=vrf_red, count=1)
    assert ping['transmitted'] == ping['received'] == 1
    ping = sw1.libs.vtysh.ping(SW2_SUB_INTF22_IPV4_ADDR.split('/')[0],
                               vrf=vrf_red, count=1)
    assert ping['transmitted'] == ping['received'] == 1
    ping = sw1.libs.vtysh.ping(SW2_SUB_INTF23_IPV4_ADDR.split('/')[0],
                               vrf=vrf_red, count=1)
    assert ping['transmitted'] == ping['received'] == 1
    ping = sw1.libs.vtysh.ping('20.20.20.20',
                               vrf=vrf_red, count=1)
    assert ping['transmitted'] == ping['received'] == 1

    subinterface_list = [1, 2, 3]

    for x in range(0, COUNT):
        step('##### Step 2: Detach the interfaces from vrf_red #####')
        ports_vrf_red_sw1 = [p11, p12, 'loopback1']
        for interface in ports_vrf_red_sw1:
            if interface is 'loopback1':
                unmap_loobackinterface_from_vrf(sw1, vrf_red, '1')
            elif interface is p12:
                unmap_port_to_vrf(sw1, vrf_red, interface)
                for subinterface in subinterface_list:
                    unmap_subinterface_from_vrf(sw1, vrf_red, interface,
                                                subinterface)
            else:
                unmap_port_to_vrf(sw1, vrf_red, interface)

        ports_vrf_red_sw2 = [p22, p25, 'loopback1']
        for interface in ports_vrf_red_sw2:
            if interface is 'loopback1':
                unmap_loobackinterface_from_vrf(sw2, vrf_red, '1')
            elif interface is p22:
                unmap_port_to_vrf(sw2, vrf_red, interface)
                for subinterface in subinterface_list:
                    unmap_subinterface_from_vrf(sw2, vrf_red, interface,
                                                subinterface)
            else:
                unmap_port_to_vrf(sw2, vrf_red, interface)
        sleep(2)
        step('##### Step 3: Verify the detached interfaces '
             'moved to vrf_default #####')
        output = sw1.libs.vtysh.show_vrf()
        for interface in ports_vrf_red_sw1:
            if interface is p12:
                for subinterface in subinterface_list:
                    tempsub = str(interface)
                    tempsub += '.'
                    tempsub += str(subinterface)
                    if tempsub in output[vrf_default].keys():
                        continue
                    else:
                        assert False, (
                            "interface {0} did not "
                            "move from vrf_red to vrf_default"
                        ).format(tempsub)
            if interface in output[vrf_default].keys():
                continue
            else:
                assert False, (
                    "interface {0} did not "
                    "move from vrf_red to vrf_default"
                ).format(interface)
        output = sw2.libs.vtysh.show_vrf()
        for interface in [p22, p25, 'loopback1']:
            if interface is p22:
                for subinterface in subinterface_list:
                    tempsub = str(interface)
                    tempsub += '.'
                    tempsub += str(subinterface)
                    if tempsub in output[vrf_default].keys():
                        continue
                    else:
                        assert False, (
                            "interface {0} did not move from "
                            "vrf_red to vrf_default"
                        ).format(tempsub)
            if interface in output[vrf_default].keys():
                continue
            else:
                assert False, (
                    "interface {0} did not "
                    "move from vrf_red to vrf_default"
                ).format(interface)

        step('##### Step 4: Test the ping through test cases through VRF RED'
             ' ping should get failed')
        ping = hs1.libs.ping.ping(1, HS2)
        if ping['received'] == 0:
            step('Ping gets failed as expected')
        else:
            assert False, "Ping is successful, expected to fail"

        step("##### Step 5: Configure ip address #####")
        # Configure ip address of vrf links in Switch 1
        configure_ipaddress(sw1, p11, SW1_INTF1_IPV4_ADDR)
        configure_ipaddress(sw1, p12, SW1_INTF2_IPV4_ADDR)
        configure_loopbackinterface(sw1, '1', SW1_LBK_INTF_IPV4_ADDR)
        configure_subinterface_ip(sw1, p12, '1', SW1_SUB_INTF21_IPV4_ADDR)
        configure_subinterface_ip(sw1, p12, '2', SW1_SUB_INTF22_IPV4_ADDR)
        configure_subinterface_ip(sw1, p12, '3', SW1_SUB_INTF23_IPV4_ADDR)
        # Configure ip address of vrf links in Switch 2
        configure_ipaddress(sw2, p22, SW2_INTF2_IPV4_ADDR)
        configure_ipaddress(sw2, p25, SW2_INTF3_IPV4_ADDR)
        configure_loopbackinterface(sw2, '1', SW2_LBK_INTF_IPV4_ADDR)
        configure_subinterface_ip(sw2, p22, '1', SW2_SUB_INTF21_IPV4_ADDR)
        configure_subinterface_ip(sw2, p22, '2', SW2_SUB_INTF22_IPV4_ADDR)
        configure_subinterface_ip(sw2, p22, '3', SW2_SUB_INTF23_IPV4_ADDR)

        # Wait until interfaces are up
        for switch, portlbl in [(sw1, p11), (sw1, p12),
                                (sw2, p22), (sw2, p25)]:
            wait_until_interface_up(switch, portlbl)

        step("##### Step 6: Configure static routes #####")
        with sw1.libs.vtysh.Configure() as ctx:
            ctx.ip_route(HS2_NETWORK_ADDR, '10.0.10.2')

        with sw2.libs.vtysh.Configure() as ctx:
            ctx.ip_route(HS1_NETWORK_ADDR, '10.0.10.1')

        sleep(5)
        step('##### Step 7: Test the ping through vrf_default #####')
        ping = hs1.libs.ping.ping(1, HS2)
        assert ping['transmitted'] == ping['received'] == 1

        step('##### Step 8: Attach the same interfaces to VRF RED #####')
        # Mapping ports to vrf in Switch 1
        for interface in [p11, p12, 'loopback1']:
            if interface is 'loopback1':
                map_loobackinterface_to_vrf(sw1, vrf_red, '1')
            elif interface is p12:
                map_port_to_vrf(sw1, vrf_red, interface)
                for subinterface in subinterface_list:
                    map_subinterface_to_vrf(sw1, vrf_red, interface,
                                            subinterface)
            else:
                map_port_to_vrf(sw1, vrf_red, interface)
        sleep(2)
        output = sw1.libs.vtysh.show_vrf()
        for interface in [p11, p12, 'loopback1']:
            if interface is p12:
                for subinterface in subinterface_list:
                    tempsub = str(interface)
                    tempsub += '.'
                    tempsub += str(subinterface)
                    if tempsub in output[vrf_red].keys():
                        continue
                    else:
                        assert False, (
                            "interface {0} did not "
                            "move from vrf_default to vrf_red"
                        ).format(tempsub)
            if interface in output[vrf_red].keys():
                continue
            else:
                assert False, (
                    "interface {0} did not "
                    "move from vrf_default to vrf_red"
                ).format(interface)
        # Mapping ports to vrf in Switch 2
        for interface in [p22, p25, 'loopback1']:
            if interface is 'loopback1':
                map_loobackinterface_to_vrf(sw2, vrf_red, '1')
            elif interface is p22:
                map_port_to_vrf(sw2, vrf_red, interface)
                for subinterface in subinterface_list:
                    map_subinterface_to_vrf(sw2, vrf_red, interface,
                                            subinterface)
            else:
                map_port_to_vrf(sw2, vrf_red, interface)
        sleep(2)
        output = sw2.libs.vtysh.show_vrf()
        for interface in [p22, p25, 'loopback1']:
            if interface is p22:
                for subinterface in subinterface_list:
                    tempsub = str(interface)
                    tempsub += '.'
                    tempsub += str(subinterface)
                    if tempsub in output[vrf_red].keys():
                        continue
                    else:
                        assert False, (
                            "interface {0} did not move from "
                            "vrf_default to vrf_red"
                        ).format(tempsub)
            if interface in output[vrf_red].keys():
                continue
            else:
                assert False, (
                    "interface {0} did not "
                    "move from vrf_default to vrf_red"
                ).format(interface)

        step("##### Step 9: Configure ip address #####")
        # Configure ip address of vrf links in Switch 1
        configure_ipaddress(sw1, p11, SW1_INTF1_IPV4_ADDR)
        configure_ipaddress(sw1, p12, SW1_INTF2_IPV4_ADDR)
        configure_loopbackinterface(sw1, '1', SW1_LBK_INTF_IPV4_ADDR)
        configure_subinterface_ip(sw1, p12, '1', SW1_SUB_INTF21_IPV4_ADDR)
        configure_subinterface_ip(sw1, p12, '2', SW1_SUB_INTF22_IPV4_ADDR)
        configure_subinterface_ip(sw1, p12, '3', SW1_SUB_INTF23_IPV4_ADDR)
        # Configure ip address of vrf links in Switch 2
        configure_ipaddress(sw2, p22, SW2_INTF2_IPV4_ADDR)
        configure_ipaddress(sw2, p25, SW2_INTF3_IPV4_ADDR)
        configure_loopbackinterface(sw2, '1', SW2_LBK_INTF_IPV4_ADDR)
        configure_subinterface_ip(sw2, p22, '1', SW2_SUB_INTF21_IPV4_ADDR)
        configure_subinterface_ip(sw2, p22, '2', SW2_SUB_INTF22_IPV4_ADDR)
        configure_subinterface_ip(sw2, p22, '3', SW2_SUB_INTF23_IPV4_ADDR)

        # Wait until interfaces are up
        for switch, portlbl in [(sw1, p11), (sw1, p12),
                                (sw2, p22), (sw2, p25)]:
            wait_until_interface_up(switch, portlbl)

        step("##### Step 10: Configure static routes #####")
        with sw1.libs.vtysh.Configure() as ctx:
            ctx.ip_route(HS2_NETWORK_ADDR, '10.0.10.2', vrf_name=vrf_red)

        with sw2.libs.vtysh.Configure() as ctx:
            ctx.ip_route(HS1_NETWORK_ADDR, '10.0.10.1', vrf_name=vrf_red)

        sleep(5)
        step('##### Step 11: Test the ping through test cases'
             'through VRF RED #####')
        ping = hs1.libs.ping.ping(1, HS2)
        assert ping['transmitted'] == ping['received'] == 1

    step('##### TEST CASE vrf.10 PASSED')
