#!/usr/bin/env python

# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import pytest
import re
from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch import *

#
# The purpose of this test is to test
# if namespace are created when a new VRF
# is configured and namespace is deleted
# when a vrf is removed.
#
# For this test, we need below topology
#
#       +---+----+
#       |        |
#       +switch1 |
#       |(Client)|
#       |        |
#       +---+----+
#
# Topology definition
topoDict = {"topoExecution": 1000,
            "topoTarget": "dut01",
            "topoDevices": "dut01",
            "topoFilters": "dut01:system-category:switch"}


def vrf_configuration(**kwargs):
    device1 = kwargs.get('device1', None)

    device1.commandErrorCheck = 0

    # Defining the test steps
    green_vrf = None
    blue_vrf = None

    #Entering VTYSH terminal
    retStruct = device1.VtyshShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"

    #Entering confi terminal SW1
    retStruct = device1.ConfigVtyShell(enter=True)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter config terminal"

    LogOutput('info', "########## Configure VRF's on the switch ##########")
    # Configure green VRF
    devIntRetStruct = device1.DeviceInteract(command="vrf green")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to enter interface"
    LogOutput('info', "### Configured VRF green ###")

    devIntRetStruct = device1.DeviceInteract(command="do start-shell")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to enter shell prompt"

    buff = device1.DeviceInteract(command="ip netns")
    out = buff.get('buffer')
    lines = out.split('\n')
    for line in lines:
        if "nonet" not in line and "swns" not in line and "netns" not in line:
            green_vrf = line.strip()
            LogOutput('info', "### Created namespace "+green_vrf+" ###")
            break

    if green_vrf is None:
        assert 0, "Failed to create green namespace"

    devIntRetStruct = device1.DeviceInteract(command="exit")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to exit from shell prompt"

    # Configure blue VRF
    devIntRetStruct = device1.DeviceInteract(command="vrf blue")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to enter interface"
    LogOutput('info', "### Configured VRF blue ###")

    devIntRetStruct = device1.DeviceInteract(command="do start-shell")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to enter shell prompt"

    buff = device1.DeviceInteract(command="ip netns")
    out = buff.get('buffer')
    lines = out.split('\n')
    for line in lines:
        if "nonet" not in line and "swns" not in line and green_vrf not in \
                line and "netns" not in line:
            blue_vrf = line.strip()
            LogOutput('info', "### Created namespace "+blue_vrf+" ###")
            break

    devIntRetStruct = device1.DeviceInteract(command="exit")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to come out of config terminal"

    vrf_creation_success = False

    if green_vrf is not None and blue_vrf is not None:
        vrf_creation_success = True
        LogOutput('info', "########## Namespaces are successfully created "
                          "##########")

    assert vrf_creation_success is True, "Failed to create namespace " \
                                         "for the VRF's we configured"

    LogOutput('info', "########## Attach an interface to VRF ##########")

    # As per the interface documents, interfaces naming should start with 1.
    # Attach interface 1 to vrf green
    devIntRetStruct = device1.DeviceInteract(command="interface 1")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to enter interface 1 prompt"
    devIntRetStruct = device1.DeviceInteract(command="vrf attach green")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to attach interface 1 to green VRF"
    LogOutput('info', "### Attached 1 to VRF green ###")

    # Exit to config prompt
    devIntRetStruct = device1.DeviceInteract(command="exit")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to return to config prompt"

    # Exit to config prompt
    devIntRetStruct = device1.DeviceInteract(command="do start-shell")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to enter to shell prompt"

    interface_attach = False
    out = device1.DeviceInteract(command="ip netns exec " + green_vrf +
                                         " ifconfig -a")
    if "1         Link encap:Ethernet" in out.get('buffer'):
        interface_attach = True

    assert interface_attach is True, "Unable to attach interface to vrf green"

    # Exit to config prompt
    devIntRetStruct = device1.DeviceInteract(command="exit")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to return to config prompt"

    # Un-Configure green VRF
    devIntRetStruct = device1.DeviceInteract(command="no vrf green")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to remove green VRF"
    LogOutput('info', "### Unconfigured green VRF ###")

    # Un-Configure blue VRF
    devIntRetStruct = device1.DeviceInteract(command="no vrf blue")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to remove blue VRF"
    LogOutput('info', "### Unconfigured blue VRF ###")

    #Exiting Config terminal
    retStruct = device1.ConfigVtyShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to come out of config terminal"

    devIntRetStruct = device1.DeviceInteract(command="start-shell")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to enter shell prompt"

    interface_attach = False
    out = device1.DeviceInteract(command="ip netns exec swns ifconfig -a 1")
    if "1         Link encap:Ethernet" in out.get('buffer'):
        interface_attach = True
        LogOutput('info', "### Moved interface 1 to default namespace ###")

    assert interface_attach is True, "Unable to move interface to default" \
                                     " namespace"

    vrf_deletion_success = True

    buff = device1.DeviceInteract(command="ip netns")
    out = buff.get('buffer')
    lines = out.split('\n')
    for line in lines:
        if green_vrf in line or blue_vrf in line:
            vrf_deletion_success = False

    assert vrf_deletion_success is True, "Failed to delete the namespaces " \
                                         "for the VRF's we de-configured"
    LogOutput('info', "### Deleted namespace " + blue_vrf + " ###")
    LogOutput('info', "### Deleted namespace " + green_vrf + " ###")
    LogOutput('info', "########## Namespaces are successfully deleted"
                      " ##########")
    device1.DeviceInteract(command="exit")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to exit from shell prompt"

    #Exiting VTYSH terminal
    retStruct = device1.VtyshShell(enter=False)
    retCode = retStruct.returnCode()
    assert retCode == 0, "Failed to enter vtysh prompt"


@pytest.mark.skipif(True, reason="skipping the test case.")
@pytest.mark.timeout(1000)
class Test_vrf_configuration:
    def setup_class(cls):
        # Test object will parse command line and formulate the env
        Test_vrf_configuration.testObj = testEnviron(topoDict=topoDict)
        #    Get topology object
        Test_vrf_configuration.topoObj = \
            Test_vrf_configuration.testObj.topoObjGet()

    def teardown_class(cls):
        Test_vrf_configuration.topoObj.terminate_nodes()

    def test_vrf_configuration(self):
        dut01Obj = self.topoObj.deviceObjGet(device="dut01")
        retValue = vrf_configuration(device1=dut01Obj)
