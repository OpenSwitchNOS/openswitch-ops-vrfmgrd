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

VLOG_DEFINE_THIS_MODULE(vrfmgrd_tableid_if);

struct free_vrf_id_
{
   uint32_t id;
   bool     id_available;
}free_vrf_id[MAX_VRF_ID];
uint32_t used_vrf_id_num = MIN_VRF_ID;

/* Intialise the Free VRF Id list during the VRF init. */
void initialize_free_vrf_id_list()
{
    uint32_t i = 0;
    free_vrf_id[DEFAULT_VRF_ID].id = DEFAULT_VRF_ID;
    free_vrf_id[DEFAULT_VRF_ID].id_available = false;

    for(i = MIN_VRF_ID; i < MAX_VRF_ID; i++)
    {
        free_vrf_id[i].id = i;
        free_vrf_id[i].id_available = true;
    }
}

/* Give the first available table_Id from free_vrf_id. */
static int64_t get_available_id()
{
    int64_t vrf_id = 0;
    for(vrf_id = used_vrf_id_num; vrf_id < MAX_VRF_ID; vrf_id++)
    {
        if(free_vrf_id[vrf_id].id_available)
        {
            used_vrf_id_num++;
            return vrf_id;
        }
    }

    for(vrf_id = 0; vrf_id < used_vrf_id_num; vrf_id++)
    {
        if(free_vrf_id[vrf_id].id_available)
        {
            return vrf_id;
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
    const int64_t table_id = vrf_id;

    if(vrf_id > MAX_VRF_ID)
    {
        VLOG_ERR("Obtained a VRF table_id '%d' greater then Max allowed value", vrf_id);
        return false;
    }

    if(free_vrf_id[vrf_id].id_available)
    {
        free_vrf_id[vrf_id].id_available = false;
        ovsrec_vrf_set_table_id(vrf, &table_id, sizeof(vrf_id));
        return true;
    }
    return false;
}

/* FREE VRF ID */
bool free_vrf_allocated_id(uint32_t vrf_id)
{
    if(vrf_id > MAX_VRF_ID)
    {
        VLOG_ERR("Obtained a VRF table_id '%d' greater then Max allowed value", vrf_id);
        return false;
    }

    if(free_vrf_id[vrf_id].id_available)
    {
        VLOG_ERR("Trying to free an unassigned vrf table_id: '%d'", vrf_id);
        return false;
    }
    else
    {
        free_vrf_id[vrf_id].id_available = true;
        return true;
    }
}
