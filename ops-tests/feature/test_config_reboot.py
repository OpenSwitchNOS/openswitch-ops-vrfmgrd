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
Test case 13: config reboot
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

from pytest import fixture
from .vrf_configs import add_vrf, map_port_to_vrf
from .vrf_configs import validate_configured_vrf, configure_ipaddress
from .vrf_configs import wait_until_interface_up
from .vrf_configs import configure_loopbackinterface
from .vrf_configs import map_loobackinterface_to_vrf
from .vrf_configs import configure_subinterface
from .vrf_configs import configure_subinterface_ip
from .vrf_configs import map_subinterface_to_vrf
from .vrf_configs import enable_dot1q_for_subinterface
from deepdiff import DeepDiff
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

SW1_SUBINTF21_NHOP_ADDR = SW1_SUB_INTF21_IPV4_ADDR.split('/')[0]  # "10.0.10.1"
SW2_SUBINTF21_NHOP_ADDR = SW2_SUB_INTF21_IPV4_ADDR.split('/')[0]  # "10.0.10.2"
HS1_NEXTHOP_ADDR = SW1_INTF1_IPV4_ADDR.split('/')[0]              # "10.0.1.2"
HS2_NEXTHOP_ADDR = SW2_INTF3_IPV4_ADDR.split('/')[0]              # "10.0.3.2"

HS1 = HS1_INTF1_IPV4_ADDR.split('/')[0]  # "10.0.1.1"
HS2 = HS2_INTF1_IPV4_ADDR.split('/')[0]  # "10.0.3.1"

vrf_default = 'vrf_default'
vrf_red = 'vrf_red'
vrfs = [vrf_red]

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
    for vrf_name in vrfs:
        add_vrf(sw1, vrf_name)

    output = sw1.libs.vtysh.show_vrf()
    for vrf_name in vrfs:
        retval = validate_configured_vrf(output, vrf_name)
        if retval:
            print("vrf {0} exist".format(vrf_name))
        else:
            assert False, "vrf {0} creation failed".format(vrf_name)

    # vrf configuration in Switch 2
    for vrf_name in vrfs:
        add_vrf(sw2, vrf_name)

    output = sw2.libs.vtysh.show_vrf()
    for vrf_name in vrfs:
        retval = validate_configured_vrf(output, vrf_name)
        if retval:
            print("vrf {0} exist".format(vrf_name))
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
                        "interface {0} does not "
                        "moved from vrf_default to vrf_red"
                    ).format(tempsub)

        if interface in output[vrf_red].keys():
            continue
        else:
            assert False, (
                "interface {0} does not "
                "moved from vrf_default to vrf_red"
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
                        "interface {0} does not moved from "
                        "vrf_default to vrf_red"
                    ).format(tempsub)
        if interface in output[vrf_red].keys():
            continue
        else:
            assert False, (
                "interface {0} does not "
                "moved from vrf_default to vrf_red"
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


def test_config_reboot(topology, configuration, step):

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

    # Set static routes in switches
    static_routes_sw1 = {}
    for keys in vrfs:
        if keys in static_routes_sw1.keys():
            continue
        else:
            static_routes_sw1[keys] = []

    static_routes_sw1[vrf_red].append(HS2_NETWORK_ADDR.split('/')[0])
    static_routes_sw1[vrf_red].append(SW2_LBK_INTF_IPV4_ADDR.split('/')[0])

    with sw1.libs.vtysh.Configure() as ctx:
        ctx.ip_route(HS2_NETWORK_ADDR, SW2_SUBINTF21_NHOP_ADDR,
                     vrf_name=vrf_red)

    with sw1.libs.vtysh.Configure() as ctx:
        ctx.ip_route(SW2_LBK_INTF_IPV4_ADDR, SW2_SUBINTF21_NHOP_ADDR,
                     vrf_name=vrf_red)

    with sw2.libs.vtysh.Configure() as ctx:
        ctx.ip_route(HS1_NETWORK_ADDR, SW1_SUBINTF21_NHOP_ADDR,
                     vrf_name=vrf_red)

    with sw2.libs.vtysh.Configure() as ctx:
        ctx.ip_route(SW1_LBK_INTF_IPV4_ADDR, SW1_SUBINTF21_NHOP_ADDR,
                     vrf_name=vrf_red)

    # Set gateway in hosts
    hs1.libs.ip.add_route('default', HS1_NEXTHOP_ADDR)
    hs2.libs.ip.add_route('default', HS2_NEXTHOP_ADDR)
    sleep(1)
    step('##### Step 1: Test the ping through test cases'
         ' through VRF RED #####')
    ping = hs1.libs.ping.ping(1, HS2)
    assert ping['transmitted'] == ping['received'] == 1

    step('##### Step 2: Verify the VRF related configs are available'
         ' in show running-config data base #####')
    run_conf_breboot = sw1.libs.vtysh.show_running_config()
    subinterface_list = [1, 2, 3]
    interface_vrf_mappings = {}
    for interface in [p11, p12, 'loopback1']:
        if interface is p12:
            for subinterface in subinterface_list:
                tempsub = str(interface)
                tempsub += '.'
                tempsub += str(subinterface)
                if tempsub in run_conf_breboot['interface']['subint'].keys():
                    interface_vrf_mappings[tempsub] = \
                        run_conf_breboot['interface']['subint'][tempsub]['vrf']

            interface_vrf_mappings[interface] = \
                run_conf_breboot['interface'][interface]['vrf']
        elif interface is 'loopback1':
            loopback_interface = interface[:8]
            loopback_id = interface[8:].strip()
            loopback_interface += ' '
            loopback_interface += loopback_id
            interface_vrf_mappings[interface] = \
                run_conf_breboot['interface'][loopback_interface]['vrf']
        else:
            if run_conf_breboot['interface'][interface]['vrf'] is None:
                run_conf_breboot['interface'][interface]['vrf'] = 'vrf_default'
            interface_vrf_mappings[interface] = \
                run_conf_breboot['interface'][interface]['vrf']

    for interface in [p11, p12, 'loopback1']:
        if 'vrf_red' in interface_vrf_mappings[interface]:
            continue
        else:
            assert False, "interface {0} belongs to {1}" \
                .format(interface, interface_vrf_mappings[interface])

    for vrf_name in vrfs:
        if vrf_name in run_conf_breboot['vrf']:
            continue
        else:
            assert False, "vrf_name {0} does not exist in" \
                " show running-config".format(vrf_name)

    for vrf_name in vrfs:
        for route in static_routes_sw1[vrf_name]:
            if route in run_conf_breboot['ip_routes'].keys():
                vrfname = run_conf_breboot['ip_routes'][route]['vrf_name']
                if vrfname == vrf_name:
                    continue
                else:
                    assert False, "Invalid static route configuration" \
                        " Actual static route configuration of network" \
                        " {0} is {1}".format(route, vrfname)
            else:
                assert False, "configured static route entry does not exist" \
                    " in show running-config for {0} network" \
                    .format(route)
    step('##### Step 3: Copy running-config to startup-config'
         ' data base #####')
    shell = 'vtysh'
    output = sw1.libs.vtysh.copy_running_config_startup_config(shell)

    if 'success' in output['status']:
        sleep(2)
        step('##### Step 4: Reboot the system to validate reconfig'
             ' of saved configuration getting invoke properly #####')
        # cmd = "reboot"
        # sw1(cmd.format(**locals()), shell='bash')
        # sleep(120), wait for 120 seconds, need to tune based on graceful
        # restart time
    else:
        assert False, "copy running-config to startup-config failed"

    step('##### Step 5: Verify the running-config data base to confirm'
         ' saved configs are applied properly #####')
    sleep(5)
    run_conf_areboot = sw1.libs.vtysh.show_running_config()
    ddiff = DeepDiff(run_conf_areboot, run_conf_breboot)
    assert not ddiff
    step('##### TEST CASE vrf.13 PASSED')
