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

from time import sleep

port_up = "up"


def add_vrf(sw, vrf_name):
    with sw.libs.vtysh.Configure() as ctx:
        ctx.vrf(vrf_name)


def validate_configured_vrf(output, vrf_name):
        if vrf_name in output.keys():
            return True
        else:
            return False


def map_port_to_vrf(sw, vrf_name, interface):
    with sw.libs.vtysh.ConfigInterface(interface) as ctx:
        ctx.vrf_attach(vrf_name)
        ctx.no_shutdown()


def get_mapped_interface_to_vrf(sw, vrf_name):
    output = sw.libs.vtysh.show_vrf()
    if output:
        return output[vrf_name].keys()


def change_interface_status(sw, interface, status):
    with sw.libs.vtysh.ConfigInterface(interface) as ctx:
        if status is port_up:
            ctx.no_shutdown()
        else:
            ctx.shutdown()


def configure_ipaddress(sw, interface, ip_address):
    with sw.libs.vtysh.ConfigInterface(interface) as ctx:
        ctx.ip_address(ip_address)
        ctx.no_shutdown()


def unmap_port_to_vrf(sw, vrf_name, interface):
    with sw.libs.vtysh.ConfigInterface(interface) as ctx:
        ctx.no_vrf_attach(vrf_name)


def delete_vrf(sw, vrf_name):
    with sw.libs.vtysh.Configure() as ctx:
        ctx.no_vrf(vrf_name)


def configure_loopbackinterface(sw, loopback_id, ip_address):
    with sw.libs.vtysh.ConfigInterfaceLoopback(loopback_id) as ctx:
        ctx.ip_address(ip_address)


def map_loobackinterface_to_vrf(sw, vrf_name, loopback_id):
    with sw.libs.vtysh.ConfigInterfaceLoopback(loopback_id) as ctx:
        ctx.vrf_attach(vrf_name)


def unmap_loobackinterface_from_vrf(sw, vrf_name, loopback_id):
    with sw.libs.vtysh.ConfigInterfaceLoopback(loopback_id) as ctx:
        ctx.no_vrf_attach(vrf_name)


def configure_subinterface(sw, port, sub_interface):
    with sw.libs.vtysh.ConfigSubinterface(port, sub_interface) as ctx:
        ctx.no_shutdown()


def configure_subinterface_ip(sw, port, sub_interface, ip_address):
    with sw.libs.vtysh.ConfigSubinterface(port, sub_interface) as ctx:
        ctx.ip_address(ip_address)
        ctx.no_shutdown()


def enable_dot1q_for_subinterface(sw, port, sub_interface, vlan_id):
    with sw.libs.vtysh.ConfigSubinterface(port, sub_interface) as ctx:
        ctx.encapsulation_dot1_q(vlan_id)


def map_subinterface_to_vrf(sw, vrf_name, port, sub_interface):
    with sw.libs.vtysh.ConfigSubinterface(port, sub_interface) as ctx:
        ctx.vrf_attach(vrf_name)
        ctx.no_shutdown()


def unmap_subinterface_from_vrf(sw, vrf_name, port, sub_interface):
    with sw.libs.vtysh.ConfigSubinterface(port, sub_interface) as ctx:
        ctx.no_vrf_attach(vrf_name)


def wait_until_interface_up(switch, portlbl, timeout=30, polling_frequency=1):
    """
    Wait until the interface, as mapped by the given portlbl, is marked as up.

    :param switch: The switch node.
    :param str portlbl: Port label that is mapped to the interfaces.
    :param int timeout: Number of seconds to wait.
    :param int polling_frequency: Frequency of the polling.
    :return: None if interface is brought-up. If not, an assertion is raised.
    """
    for i in range(timeout):
        status = switch.libs.vtysh.show_interface(portlbl)
        if status['interface_state'] == 'up':
            return
        sleep(polling_frequency)

    assert False, (
        'Interface {}:{} never brought-up after '
        'waiting for {} seconds'.format(
            switch.identifier, portlbl, timeout
        )
    )
