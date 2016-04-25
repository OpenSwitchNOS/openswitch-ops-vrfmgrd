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

    LogOutput('info', "########## Configure VRF's on the switch ##########")
    # Configure green VRF
    devIntRetStruct = device1.DeviceInteract(command="ovs-vsctl add-vrf green")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to Configre VRF"
    LogOutput('info', "### Configured VRF green ###")

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

    # Configure blue VRF
    devIntRetStruct = device1.DeviceInteract(command="ovs-vsctl add-vrf blue")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to Configre VRF"
    LogOutput('info', "### Configured VRF blue ###")

    buff = device1.DeviceInteract(command="ip netns")
    out = buff.get('buffer')
    lines = out.split('\n')
    for line in lines:
        if "nonet" not in line and "swns" not in line and green_vrf not in \
                line and "netns" not in line:
            blue_vrf = line.strip()
            LogOutput('info', "### Created namespace "+blue_vrf+" ###")
            break

    vrf_creation_success = False

    if green_vrf is not None and blue_vrf is not None:
        vrf_creation_success = True
        LogOutput('info', "########## Namespaces are successfully created "
                          "##########")

    assert vrf_creation_success is True, "Failed to create namespace " \
                                         "for the VRF's we configured"

    # Un-Configure green VRF
    devIntRetStruct = device1.DeviceInteract(command="ovs-vsctl del-vrf green")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to remove green VRF"
    LogOutput('info', "### Unconfigured green VRF ###")

    # Un-Configure blue VRF
    devIntRetStruct = device1.DeviceInteract(command="ovs-vsctl del-vrf blue")
    retCode = devIntRetStruct.get('returnCode')
    assert retCode == 0, "Failed to remove blue VRF"
    LogOutput('info', "### Unconfigured blue VRF ###")

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
