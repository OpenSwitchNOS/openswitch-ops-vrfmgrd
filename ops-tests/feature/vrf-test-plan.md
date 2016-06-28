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
   - [vrf based ping between switches for samevrf](#test_vrf-based-ping-between-switches-for-samevrf)
   - [vrf based ping between switches for differentvrf](#test_vrf-based-ping-between-switches-for-differentvrf)
   - [vrf based ping between switches for multiple links mapped to single vrf](#test_vrf-based-ping-between-switches-for-multilinks-map-to-singlevrf)
   - [deletion and addition of the same VRF and testing data path](#test_delete_add_samevrf_check_data_path)
   - [interface attach/detach to/from VRF and testing data path](#test_port_attach_detach_mulititimes_check_data_path)
   - [Testing scale](#test_vrf_scale)
   - [Clear ARP while doing PING] (#test_clear_arp_while_ping)
   - [Make interface down/up and testing data path](#test_port_up_down_multitimes_ckeck_data_path)
   ## vrf based ping between switches for samevrf
   #### Objective
   This test case confirms that
        1- VRF configuration and check if it is configured properly
        2- Add a port to VRF and check if it is moved properly to appropriate vrf
        3- All interfaces are configured with same network ip each interface mapped to different Vrfs and check if it is pinging fine with VRF
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
   1. Setup the topology as show
   2. By default system have vrf_default and user has to configure 3 vrfs namely vrf_red, vrf_green and vrf_blue
   3. Map 4 interfaces to 4 vrfs, one port for one vrf basis
   4. Same ip address is assigned for all the interfaces to validate each namespace context is different from others, so same ip address configuration should work
   5. Use CLI command to validate vrf configurations, port mappings and ip configurations
   6. Use CLI vrf based ping command to validate data path between the same vrfs presented in system

   ## vrf based ping between switches for differentvrf
   #### Objective
   This test case confirms that
        1- Move the interface oneside to another VRF and check If the ping is succeding. It should fail
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
   1. Setup the topology as show
   2. By default system have vrf_default and user has to configure 3 vrfs namely vrf_red, vrf_green and vrf_blue
   3. Map 4 interfaces to 4 vrfs, one port for one vrf basis
   4. Same ip address is assigned for all the interfaces to validate each namespace context is different from others
   5. Use CLI command to validate vrf configurations, port mappings and ip configurations
   6. Use CLI vrf based ping command to validate data path between the same vrfs presented in system
   7. Unmap the port configured to any vrf
   8. Repeate the step 6, ping should fail even destination ip address are presented in other vrfs

   ## vrf based ping between switches for multiple links mapped to single vrf
   #### Objective
   This test case confirms that
        1- Add 2 interfaces to same VRF and check ping via 1 to 2 is going through
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
   1. Setup the topology as show
   2. By default system have vrf_default and user has to configure 3 vrfs namely vrf_red, vrf_green and vrf_blue
   3. Map 8 interfaces to 4 vrfs, two port for one vrf basis
   4. Different ip address is assigned for all the interfaces
   5. Use CLI command to validate vrf configurations, port mappings and ip configurations
   6. Use CLI vrf based ping command to validate data path between the same vrfs presented in system for all the links

   ## deletion and addition of the same VRF and testing data path
   #### Objective
   This test case confirms that
        1- VRF configuration and check if it is configured properly
        2- Add a port to VRF and check if it is moved properly to appropriate vrf
        3- Set network addresses and static routes between nodes and ping host to host
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
   1. Setup the topology as show
   2. By default system have vrf_default and user has to configure vrf_red
   3. Map 2 interfaces to vrf_red, one port towards to host and another one presented between the switches
   4. Different ip address is assigned for all the interfaces
   5. Use CLI command to validate vrf configurations, port mappings and ip configurations
   6. In all the devices configure static routes for all the networks exists in topology
   7. Initiate host to host ping to test the ping through test cases through VRF RED
   8. Delete and add VRF RED / attach interfaces to VRF RED
   9. Test the ping through test cases through VRF RED
   10. Repeat the steps 8 and 9  'n' number of times

   ## interface attach/detach to/from VRF and testing data path
   #### Objective
   This test case confirms that
        1- VRF configuration and check if it is configured properly
        2- Add a port to VRF and check if it is moved properly to appropriate vrf
        3- Set network addresses and static routes between nodes and ping host to host
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
   1. Setup the topology as show
   2. By default system have vrf_default and user has to configure vrf_red
   3. Map 2 interfaces to vrf_red, one port towards to host and another one presented between the switches
   4. Different ip address is assigned for all the interfaces
   5. Use CLI command to validate vrf configurations, port mappings and ip configurations
   6. In all the devices configure static routes for all the networks exists in topology
   7. Initiate host to host ping to test the ping through test cases through VRF RED
   8. Detach and then Attach again the same interfaces to VRF RED
   9. Test the ping through test cases through VRF RED
   10. Repeat the steps 8 and 9  'n' number of times

   ## Testing scale
   #### Objective
   This test case confirms that
        1- VRF configuration and check if it is configured properly
        2- Add a port to VRF and check if it is moved properly to appropriate vrf
        3- Set network addresses and static routes between nodes and ping host to host
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
   2. By default system have vrf_default and user has to configure 64 vrfs(vrf1 - vrf64)
   3. Map 2 interfaces to vrf1, one port towards to host and another one presented between the switches
   4. Map maximum supported interface to other vrfs as one-port-to-one-vrf basis
   5. Same network is assigned for all the links between the switches to identify namespace functionality
   5. Use CLI command to validate vrf configurations, port mappings and ip configurations
   6. In all the devices configure static routes for all the networks exists in topology
   7. Initiate host to host ping to test the ping through test cases through vrf1
   8. Delete all the 64 vrfs, and validate whether all the interfaces are moved to vrf_default
   9. Readd all the 64 vrfs then attach the same interfaces to respective vrfs
   10. Test the ping through test cases through vrf1
   11. Repeat the steps 8,9 and 10  'n' number of times

   ## Clear ARP while doing PING
   #### Objective
   This test case confirms that
        1- VRF configuration and check if it is configured properly
        2- Add a port to VRF and check if it is moved properly to appropriate vrf
        3- Set network addresses and static routes between nodes and ping host to host
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
   1. Setup the topology as show
   2. By default system have vrf_default and user has to configure vrf_red
   3. Map 2 interfaces to vrf_red, one port towards to host and another one presented between the switches
   4. Different ip address is assigned for all the interfaces
   5. Use CLI command to validate vrf configurations, port mappings and ip configurations
   6. In all the devices configure static routes for all the networks exists in topology
   7. Initiate host to host ping to test the ping through test cases through VRF RED
   8. Clear ARP while the ping is going ON
   9. Test the ping through test cases through VRF RED, should not drop any ping packets even clearing ARP
   10. Repeat the steps 8 and 9  'n' number of times

   ## Make interface down/up and testing data path
   #### Objective
   This test case confirms that
        1- VRF configuration and check if it is configured properly
        2- Add a port to VRF and check if it is moved properly to appropriate vrf
        3- Set network addresses and static routes between nodes and ping host to host
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
   1. Setup the topology as show
   2. By default system have vrf_default and user has to configure vrf_red
   3. Map 2 interfaces to vrf_red, one port towards to host and another one presented between the switches
   4. Different ip address is assigned for all the interfaces
   5. Use CLI command to validate vrf configurations, port mappings and ip configurations
   6. In all the devices configure static routes for all the networks exists in topology
   7. Initiate host to host ping to test the ping through VRF RED
   8. Make interface down while ping
   9. Test the ping through VRF RED, ping should get fail
   10. Make interface up
   11. Test the ping through test cases through VRF RED, should not drop any ping packets
   12. Repeat the steps 8,9,10 and 11 'n' number of times
