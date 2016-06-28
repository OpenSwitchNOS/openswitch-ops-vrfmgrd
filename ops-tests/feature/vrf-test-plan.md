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
   - [Interface deletion/movement -- proper clean ups for interface](#test_interface_del_or_movement_proper_cleanups)
   - [L3 Interface deletion/movement -- proper clean ups for subinterface and loopback interface](#test_subinterface_loopbackinterface_for_vrf)
   - [VRF deletion and Recreation with same name -- clean ups](#test_vrf_deletion_recreation_with_samename)
   - [VRF deletion and Recreation with different name -- clean ups](#test_vrf_deletion_recreation_with_differentname)
   - [Config reboot](#test_config_reboot)

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

   ## L3 Interface deletion/movement -- proper clean ups
   #### Objective
   This test case confirms that
        1- Multiple time delete/move the interface from/to the VRF to test the proper clean ups
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
   3. Map 4 interfaces to vrf_red, one port towards to host and others ports connected between the switches
   4. Configure different IP address to each interfaces
   5. Use CLI command to validate VRF configurations, port mappings and IP configurations
   6. Add a static route from sw1 to hs2 via sw2 and sw2 to hs1 via sw1
   7. Initiate host to host ping to test the ping through vrf_red
   8. Detach the interfaces from vrf_red
   9. Verify the detached interfaces are moved to vrf_default
   10. Test the ping through test cases through vrf_red ping should get failed
   11. Attach the same interfaces to vrf_red
   12. Verify the attached same interfaces to vrf_red
   13. Configure ip address
   14. Test the ping through test cases through vrf_red
   15. Repeat the steps 8,9,10,11,12,13 and 14 for 'n' number of times

   ## L3 Interface deletion/movement -- proper clean ups for subinterface and loopback interface
   #### Objective
   This test case confirms that
        1- To test data path over Subinterface and loopback for VRF
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
   3. Use CLI command to validate VRF configuration
   4. Configure 3 Subinterface and 1 loopback interface
   5. Map all the configured subinterface and loopback interface to vrf_red
   6. Use CLI command to verify the mapped interfaces are moved to vrf_red
   7. Configure IP address for all the configured interfaces
   8. Add a static route from sw1 to hs2 via sw2 and sw2 to hs1 via sw1
   9. Initiate host to host ping to test the ping through vrf_red
   10. Detach the interfaces from vrf_red
   11. Verify all the detached interfaces moved to vrf_default from vrf_red
   12. Repeat the step 9 to validate data path destroyed properly for vrf_red
   13. Once again attach all the same interfaces to vrf_red
   14. Use CLI command to verify the mapped interfaces are moved to vrf_red
   15. Configure ip address
   16. Repeat the steps 10,11,12,13,14 and 15 for 'n' number of times
   17. Initiate host to host ping to test the ping through vrf_red

   ## VRF deletion and Recreation with same name -- clean ups
   #### Objective
   This test case confirms that
        1- To test proper clean ups for multiple times deleting and recreating the VRF with same name
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
   2. By default system have vrf_default and user has to configure 8 vrfs namely vrf1, vrf2, vrf3, etc..
   3. Use CLI command to validate VRF configurations
   5. Map 2 interfaces to vrf1 and map 1 interface to all the remaining VRF
   6. Use CLI command to verify the mapped interfaces are moved to all the VRF
   7. Configure IP address for all the configured interfaces
   8. Add a static route from sw1 to hs2 via sw2 and sw2 to hs1 via sw1
   9. Initiate host to host ping to test the ping through vrf1
   10. Detach all the configured VRF
   11. Verify all the VRF deleted successfully
   12. Verify all the mapped port moved to vrf_default
   13. Reconfigure all the VRF with same name
   14. Use CLI command to validate VRF configurations
   15. Map 2 interfaces to vrf1 and map 1 interface to all the remaining VRF
   16. Use CLI command to verify the mapped interfaces are moved to all the VRF
   17. Configure IP address for all the configured interfaces
   18. Repeat the steps 10,11,12,13,14,15,16 and 17 for 'n' number of times
   19. Initiate host to host ping to test the ping through vrf1

   ## VRF deletion and Recreation with different name -- clean ups
   #### Objective
   This test case confirms that
        1- To test proper clean ups for multiple times deleting and recreating the VRF with different name
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
   2. By default system have vrf_default and user has to configure 8 vrfs namely vrf1, vrf2, vrf3, etc..
   3. Use CLI command to validate VRF configurations
   5. Map 2 interfaces to vrf1 and map 1 interface to all the remaining VRF
   6. Use CLI command to verify the mapped interfaces are moved to all the VRF
   7. Configure IP address for all the configured interfaces
   8. Add a static route from sw1 to hs2 via sw2 and sw2 to hs1 via sw1
   9. Initiate host to host ping to test the ping through vrf1
   10. Detach all the configured VRF
   11. Verify all the VRF deleted successfully
   12. Verify all the mapped port moved to vrf_default
   13. Reconfigure all the VRF with same name
   14. Use CLI command to validate VRF configurations
   15. Map 2 interfaces to vrf1 and map 1 interface to all the remaining VRF
   16. Use CLI command to verify the mapped interfaces are moved to all the VRF
   17. Configure IP address for all the configured interfaces
   18. Repeat the steps 10,11,12,13,14,15,16 and 17 for 'n' number of times
   19. Initiate host to host ping to test the ping through vrf1

   ## Config reboot
   #### Objective
   This test case confirms that
        1- To test VRF related save configurations properly applied from startup-config file
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
   3. Use CLI command to validate VRF configuration
   4. Configure 3 Subinterface and 1 loopback interface
   5. Map all the configured subinterface and loopback interface to vrf_red
   6. Use CLI command to verify the mapped interfaces are moved to vrf_red
   7. Configure IP address for all the configured interfaces
   8. Add a static route from sw1 to hs2 via sw2 and sw2 to hs1 via sw1
   9. Initiate host to host ping to test the ping through vrf_red
   10. Verify the VRF related configs are available in show running-config data base
   11. Copy running-config to startup-config
   12. Reboot the system
   13. Wait for defined/supported gracefull time to restart the node
   14. Verify the running-config data base to confirm saved configs are applied properly from startup-config
