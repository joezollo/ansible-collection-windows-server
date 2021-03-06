#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r'''
---
module: win_dhcp_info
short_description: Gathers Info on Windows Server DHCP Objects
author: Joe Zollo (@joezollo)
requirements:
  - This module requires Windows Server 2012 or Newer
description:
  - Gathers Info on Windows Server DHCP Objects
options:
  type:
    description:
      - The object type to gather information on.
      - When l(reservation) is specified, and l(ip)/l(mac) are not, all
        reservations are returned.
      - When l(lease) is specified, and l(ip)/l(mac) are not, all
        leases are returned.
      - When l(scope) is specified, and l(ip)/l(mac) are not, scope
        details are returned.
      - When l(all) is specified, and l(ip)/l(mac) are not, info on all
        leases, reservations and scopes are returned.
    type: str
    default: all
    choices: [ reservation, lease, scope, all ]
  scope_id:
    description:
      - When l(scope_id) is defined, all queries are limited to the
        defined scope.
      - Must be defined when looking up info on an entire scope
    type: str
  ip:
    description:
      - The IPv4 address of the client server/computer.
      - If specified, will lookup a info on a single lease/reservation
      - Can be used to identify an existing lease/reservation, instead of l(mac).
    type: str
  mac:
    description:
      - Specifies the client identifier to be set on the IPv4 address.
      - If defined, will lookup a info on a single lease/reservation.
      - Can be used to identify an existing lease/reservation, instead of l(ip).
      - Windows clients use the MAC address as the client ID, Linux and other 
        operating systems can use other types of identifiers.
    type: str
'''

EXAMPLES = r'''
- name: Gather info on all DHCP reservations
  community.windows.win_dhcp_info:
    type: reservation
  register: dhcp

- name: Gather info on a DHCP reservation with the MAC address 00-A1-B2-C2-D4-E5
  community.windows.win_dhcp_info:
    type: reservation
    mac: 00-A1-B2-C2-D4-E5
  register: dhcp

- name: Gather info on all DHCP leases
  community.windows.win_dhcp_info:
    type: lease
  register: dhcp

- name: Gather info on all DHCP scopes
  community.windows.win_dhcp_info:
    type: scope
  register: dhcp

- name: Gather info on all DHCP leases in the 192.168.55.0 scope
  community.windows.win_dhcp_info:
    type: lease
    scope_id: 192.168.55.0
  register: dhcp

- name: Gather info on all DHCP reservations, leases and scopes
  community.windows.win_dhcp_info:
    type: lease
  register: dhcp

- name: Gather info on a DHCP lease with the MAC address 00:AA:BB:C3:E4:F5
  community.windows.win_dhcp_info:
    type: lease
    mac: '00:AA:BB:C3:E4:F5'
  register: dhcp
'''

RETURN = r'''
leases:
  description: DHCP Lease(s) and Reservation(s)
  returned: When l(type=lease), l(type=reservation) or l(type=all)
  type: list
  sample:
  - client_id: 00-0A-1B-2C-3D-4F
    address_state: InactiveReservation
    ip_address: 172.16.98.230
    description: Really Fancy
    name: null
    scope_id: 172.16.98.0
    description: 10.0.1.0
    hostname: 255.255.255.0
    address_state: Active
    lease_expiration:
      days: 2
      hours: 48

scopes:
  description: DHCP Scope(s)
  returned: When l(type=scope) or l(type=all)
  type: list
  sample:
  - name: 10.0.1.0-vlan1
    scope_id: 10.0.1.0
    subnet_mask: 255.255.255.0
    state: Active
    start_range: 10.0.1.100
    end_range: 10.0.1.199
    lease_duration:
      days: 2
      hours: 48
  - name: 10.0.2.0-vlan2
    scope_id: 10.0.2.0
    subnet_mask: 255.255.255.0
    state: Active
    start_range: 10.0.2.100
    end_range: 10.0.2.199
    lease_duration:
      days: 0
      hours: 3
'''
