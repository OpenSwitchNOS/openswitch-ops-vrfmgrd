## Contents 
   - [vrf based ping between switches for samevrf](#test-vrf-based-ping-between-switches-for-samevrf) 
   - [vrf based ping between switches for differentvrf](#test-vrf-based-ping-between-switches-for-differentvrf) 
   - [vrf based ping between switches for multiple links mapped to single vrf](#test-vrf-based-ping-between-switches-for-multilinks-map-to-singlevrf) 
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

