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

## Contents
   - [VRF based ping between switches for samevrf](#test_vrf-based-ping-between-switches-for-samevrf)
   - [VRF based ping between switches for differentvrf](#test_vrf-based-ping-between-switches-for-differentvrf)
   - [VRF based Nexthop ping for multiple interfaces mapped with single VRF](#test_vrf-based-nexthop-ping-for-multilinks-map-to-singlevrf)
   - [Deletion and addition of the same VRF and testing data path](#test_delete_add_samevrf_check_data_path)
   - [Interface attach/detach to/from VRF and testing data path](#test_port_attach_detach_mulititimes_check_data_path)
   - [Testing scale](#test_vrf_scale)
   - [Clear ARP while doing PING] (#test_clear_arp_while_ping)
   - [Make interface down/up and testing data path](#test_port_up_down_multitimes_ckeck_data_path)
   ## VRF based ping between switches for same VRF
   #### Objective
   This test case confirms that
        1- VRF configuration and check if it is configured properly
        2- Add a port to VRF and check if it is moved properly to appropriate VRF
        3- All interfaces are configured with same network IP each interface mapped to different VRF and check if it is pinging fine with VRF
   #### Requirements
   - Physical Switch/Switch Test setup
   - **FT File**:
   #### Setup
   ##### Topology diagram
   ```ditaa
   +----------------+           +-----------------+
   |                |-----------|                 |
   |     sw1        |-----------|       sw2       |
   |                |-----------|                 |
   |                |-----------|                 |
   +----------------+           +-----------------+
   ```
   #### Description
   1. Setup the topology as shown
   2. By default system have vrf_default and user has to configure 3 VRF namely vrf_red, vrf_green and vrf_blue
   3. Map 4 interfaces to 4 VRF, one port for one VRF basis
   4. Configure same IP address to the interfaces to confirm each namespcae context is unique
   5. Use CLI command to validate VRF configurations, port mappings and IP configurations
   6. Use CLI VRF based ping command to validate Nexthop connectivity between the same VRF configured in switches

   ## VRF based ping between switches for different VRF
   #### Objective
   This test case confirms that
        1- Add a port to VRF and verify the Nexthop ping from that VRF
        2- Move the attacted interface from that VRF to another VRF
        3- Verify the Nexthop ping is succeding for thet VRF. ping should fail
        and check If the ping is succeding. ping should fail
   #### Requirements
   - Physical Switch/Switch Test setup
   - **FT File**:
   #### Setup
   ##### Topology diagram
   ```ditaa
   +----------------+           +-----------------+
   |                |-----------|                 |
   |     sw1        |-----------|       sw2       |
   |                |-----------|                 |
   |                |-----------|                 |
   +----------------+           +-----------------+
   ```
   #### Description
   1. Setup the topology as shown
   2. By default system have vrf_default and user has to configure 3 VRF namely vrf_red, vrf_green and vrf_blue
   3. Map 4 interfaces to 4 VRF, one port for one VRF basis
   4. Same IP address is assigned for all the interfaces to validate each namespace context is different from others
   5. Use CLI command to validate VRF configurations, port mappings and IP configurations
   6. Use CLI VRF based ping command to validate Nexthop connectivity between the same VRF configured in switches
   7. Unmap the port configured to any VRF
   8. Repeate the step 6, ping should fail even destination IP address is present in other VRF

   ## Verify the Nexthop ping for multiple interfaces mapped with single VRF
   #### Objective
   This test case confirms that
        1- Add 2 interfaces to same VRF and verify the Nexthop ping for all the interfaces
   #### Requirements
   - Physical Switch/Switch Test setup
   - **FT File**:
   #### Setup
   ##### Topology diagram
   ```ditaa
   +----------------+           +-----------------+
   |                |-----------|                 |
   |                |-----------|                 |
   |                |-----------|                 |
   |                |-----------|                 |
   |     sw1        |-----------|       sw2       |
   |                |-----------|                 |
   |                |-----------|                 |
   |                |-----------|                 |
   +----------------+           +-----------------+
   ```
   #### Description
   1. Setup the topology as shown
   2. By default system have vrf_default and user has to configure 3 VRF namely vrf_red, vrf_green and vrf_blue
   3. Map 8 interfaces to 4 VRF, two port for one VRF basis
   4. Configure different IP address to each interfaces
   5. Use CLI command to validate VRF configurations, port mappings and IP configurations
   6. Use CLI VRF based ping command to validate Nexthop connectivity between the same VRF configured in switches for all the links

   ## Deletion and addition of the same VRF and testing data path
   #### Objective
   This test case confirms that
        1- Delete and Readd the VRF multiple times to test data path
   #### Requirements
   - Physical Switch/Switch Test setup
   - **FT File**:
   #### Setup
   ##### Topology diagram
   ```ditaa
   +-------+                                 +-------+
   |       |     +-------+     +-------+     |       |
   |  hs1  <----->  sw1  <----->  sw2  <----->  hs2  |
   |       |     +-------+     +-------+     |       |
   +-------+                                 +-------+
   ```
   #### Description
   1. Setup the topology as shown
   2. By default system have vrf_default and user has to configure vrf_red
   3. Map 2 interfaces to vrf_red, one port towards to host and another one presented between the switches
   4. Configure different IP address to each interfaces
   5. Use CLI command to validate VRF configurations, port mappings and IP configurations
   6. Add a static route from sw1 to hs2 via sw2 and sw2 to hs1 via sw1
   7. Initiate host to host ping to test the ping through test cases through VRF RED
   8. Delete VRF RED
   9. Repeate the step 7, ping should fail even destination IP address is present in other VRF
   10. Readd VRF RED / attach interfaces to VRF RED
   11. Test the ping through test cases through VRF RED
   12. Repeat the steps 8 and 9  'n' number of times

   ## Interface attach/detach to/from VRF and testing data path
   #### Objective
   This test case confirms that
        1- Multiple time detach and attach the interface to VRF to test data path
   #### Requirements
   - Physical Switch/Switch Test setup
   - **FT File**:
   #### Setup
   ##### Topology diagram
   ```ditaa
   +-------+                                 +-------+
   |       |     +-------+     +-------+     |       |
   |  hs1  <----->  sw1  <----->  sw2  <----->  hs2  |
   |       |     +-------+     +-------+     |       |
   +-------+                                 +-------+
   ```
   #### Description
   1. Setup the topology as shown
   2. By default system have vrf_default and user has to configure vrf_red
   3. Map 2 interfaces to vrf_red, one port towards to host and another one presented between the switches
   4. Configure different IP address to each interfaces
   5. Use CLI command to validate VRF configurations, port mappings and IP configurations
   6. Add a static route from sw1 to hs2 via sw2 and sw2 to hs1 via sw1
   7. Initiate host to host ping to test the ping through test cases through VRF RED
   8. Detach interfaces from VRF RED
   9. Repeate the step 7, ping should fail even destination IP address is present in other VRF
   10. ReAttach the same interfaces to VRF RED
   11. Test the ping through test cases through VRF RED
   12. Repeat the steps 8 and 9  'n' number of times

   ## Testing scale
   #### Objective
   This test case confirms that
        1- Testing scale to validate maximum supported VRF
   #### Requirements
   - Physical Switch/Switch Test setup
   - **FT File**:
   #### Setup
   ##### Topology diagram
   ```ditaa
   +-------+                                 +-------+
   |       |     +-------+     +-------+     |       |
   |  hs1  <----->  sw1  <----->  sw2  <----->  hs2  |
   |       |     +-------+     +-------+     |       |
   +-------+                                 +-------+
   ```
   #### Description
   1. Setup the topology as show, and map the supported interface level to each configured vrf
   2. By default system have vrf_default and user has to configure 64 VRF (vrf1 - vrf64)
   3. Map 2 interfaces to vrf1, one port towards to host and another one presented between the switches
   4. Map maximum supported interface to other VRF as one-port-to-one-VRF basis
   5. Same network is assigned for all the links between the switches to identify namespace functionality
   5. Use CLI command to validate VRF configurations, port mappings and IP configurations
   6. Add a static route from sw1 to hs2 via sw2 and sw2 to hs1 via sw1
   7. Initiate host to host ping to test the ping through test cases through vrf1
   8. Delete all the 64 VRF, and validate whether all the interfaces are moved to vrf_default
   9. Readd all the 64 VRF then attach the same interfaces to respective VRF
   10. Test the ping through test cases through vrf1
   11. Repeat the steps 8,9 and 10  'n' number of times

   ## Clear ARP while doing PING
   #### Objective
   This test case confirms that
        1- Clear ARP while the ping is going ON
   #### Requirements
   - Physical Switch/Switch Test setup
   - **FT File**:
   #### Setup
   ##### Topology diagram
   ```ditaa
   +-------+                                 +-------+
   |       |     +-------+     +-------+     |       |
   |  hs1  <----->  sw1  <----->  sw2  <----->  hs2  |
   |       |     +-------+     +-------+     |       |
   +-------+                                 +-------+
   ```
   #### Description
   1. Setup the topology as shown
   2. By default system have vrf_default and user has to configure vrf_red
   3. Map 2 interfaces to vrf_red, one port towards to host and another one presented between the switches
   4. Configure different IP address to each interfaces
   5. Use CLI command to validate VRF configurations, port mappings and IP configurations
   6. Add a static route from sw1 to hs2 via sw2 and sw2 to hs1 via sw1
   7. Initiate host to host ping to test the ping through test cases through VRF RED
   8. Clear ARP while the ping is going ON
   9. Test the ping through test cases through VRF RED, should not drop any ping packets even clearing ARP
   10. Repeat the steps 8 and 9  'n' number of times

   ## Make interface down/up and testing data path
   #### Objective
   This test case confirms that
        1- Multiple time change the interface status UP and DOWN to test the data path
   #### Requirements
   - Physical Switch/Switch Test setup
   - **FT File**:
   #### Setup
   ##### Topology diagram
   ```ditaa
   +-------+                                 +-------+
   |       |     +-------+     +-------+     |       |
   |  hs1  <----->  sw1  <----->  sw2  <----->  hs2  |
   |       |     +-------+     +-------+     |       |
   +-------+                                 +-------+
   ```
   #### Description
   1. Setup the topology as shown
   2. By default system have vrf_default and user has to configure vrf_red
   3. Map 2 interfaces to vrf_red, one port towards to host and another one presented between the switches
   4. Configure different IP address to each interfaces
   5. Use CLI command to validate VRF configurations, port mappings and IP configurations
   6. Add a static route from sw1 to hs2 via sw2 and sw2 to hs1 via sw1
   7. Initiate host to host ping to test the ping through VRF RED
   8. Make interface down while ping
   9. Test the ping through VRF RED, ping should get fail
   10. Make interface up
   11. Test the ping through test cases through VRF RED, should not drop any ping packets
   12. Repeat the steps 8,9,10 and 11 'n' number of times
