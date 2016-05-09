/*
 * (c) Copyright 2016 Hewlett Packard Enterprise Development LP
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */
/************************************************************************//**
 * @ingroup vrfmgrdd
 *
 * @file
 * Source for vrfmgrd table_id generation.
 *
 ***************************************************************************/

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <errno.h>
#include <getopt.h>
#include <limits.h>
#include <signal.h>
#include <stdlib.h>
#include <string.h>

#include "ovsdb-idl.h"
#include "vswitch-idl.h"
#include "openvswitch/vconn.h"
#include "openvswitch/vlog.h"
#include "vrfmgrd.h"

struct free_vrf_id_
{
   uint32_t id;
   bool     id_available;
}free_vrf_id[MAX_VRF_ID];
uint32_t used_vrf_id_num = 1;

/* Intialise the Free VRF Id list during the VRF init. */
void initialize_free_vrf_id_list()
{
    uint32_t i;
    free_vrf_id[0].id = 0;
    free_vrf_id[0].id_available = false;

    for(i = 1; i < MAX_VRF_ID; i++)
    {
        free_vrf_id[i].id = i;
        free_vrf_id[i].id_available = true;
    }
}

static int64_t get_available_id()
{
    int64_t i;
    for(i = used_vrf_id_num; i < MAX_VRF_ID; i++)
    {
        if(free_vrf_id[i].id_available)
        {
            used_vrf_id_num++;
            return i;
        }
    }

    for(i = 0; i < used_vrf_id_num; i++)
    {
        if(free_vrf_id[i].id_available)
        {
            return i;
        }
    }
    return -1;
}

/* ALLOCATE FIRST AVAILABLE VRF ID */
int32_t allocate_first_vrf_id(struct ovsrec_vrf *vrf)
{
    int64_t vrf_id;

    vrf_id = get_available_id();
    if(vrf_id < 0)
    {
        return -1;
    }
    ovsrec_vrf_set_table_id(vrf, &vrf_id, sizeof(vrf_id));
    free_vrf_id[vrf_id].id_available = false;
    return vrf_id;
}

/* During the process restart to update the local VRF list */
void set_vrf_id(int64_t vrf_id)
{
    free_vrf_id[vrf_id].id_available = false;
    return;
}

/* ALLOCATE A SPECFIC VRF-ID */
bool allocate_vrf_id(struct ovsrec_vrf *vrf, uint32_t vrf_id)
{
    uint32_t i;
    const int64_t table_id = vrf_id;
    for(i=0; i < MAX_VRF_ID; i++)
    {
        if(vrf_id == free_vrf_id[i].id && free_vrf_id[i].id_available)
        {
            free_vrf_id[vrf_id].id_available = false;
            ovsrec_vrf_set_table_id(vrf, &table_id, sizeof(vrf_id));
            return true;
        }
    }
    return false;
}

/* FREE VRF ID */
bool free_vrf_allocated_id(uint32_t vrf_id)
{
    uint32_t i;
    for(i=0; i < MAX_VRF_ID; i++)
    {
        if(vrf_id == free_vrf_id[i].id)
        {
            free_vrf_id[i].id_available = true;
            return true;
        }
    }
    return false;
}
