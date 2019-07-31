#!/usr/bin/env python3.8
"""Phantom API Client: Models.Artifact
Copyright © 2019 Jerod Gawne <https://github.com/jerodg/>

This program is free software: you can redistribute it and/or modify
it under the terms of the Server Side Public License (SSPL) as
published by MongoDB, Inc., either version 1 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
SSPL for more details.

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

You should have received a copy of the SSPL along with this program.
If not, see <https://www.mongodb.com/licensing/server-side-public-license>."""

from dataclasses import dataclass
from typing import Dict, List, Union

from base_api_client.models.record import Record
from phantom_api_client.models.cef import Cef
from phantom_api_client.models.exceptions import InvalidOptionError


@dataclass
class Artifact(Record):
    container_id: Union[int, None] = None
    cef: Union[Cef, None] = None  # Common Event Format
    cef_types: Union[Dict[str, List[str]], None] = None
    data: Union[dict, None] = None
    description: Union[str, None] = None
    end_time: Union[str, None] = None  # ISO-8601 Timestamp
    ingest_app_id: Union[int, str, None] = None
    kill_chain: Union[str, None] = None
    label: Union[str, None] = None
    name: Union[str, None] = None
    owner_id: Union[str, int, None] = None
    run_automation: bool = True
    severity: Union[str, None] = 'low'
    source_data_identifier: Union[str, None] = None
    start_time: Union[str, None] = None
    tags: Union[List[str], str, None] = None
    type: Union[str, None] = None

    def __post_init__(self):
        kill_chain_opts = ['Reconnaissance',
                           'Weaponization',
                           'Delivery',
                           'Exploitation',
                           'Installation',
                           'Command & Control',
                           'Actions on Objectives',
                           None]
        if self.kill_chain not in kill_chain_opts:
            raise InvalidOptionError('kill_chain', kill_chain_opts)

        label_opts = ['event', 'net flow', 'artifact', 'network', 'test', 'mss', 'qradar-offenses', None]
        if self.label not in label_opts:
            raise InvalidOptionError('label', label_opts)

        severity_opts = ['low', 'medium', 'high', None]
        if self.severity not in severity_opts:
            raise InvalidOptionError('severity', severity_opts)

        if self.data:
            self.data = dict(sorted({k: v for k, v in self.data.items() if v is not None}.items()))

        if type(self.cef) is Cef:
            self.cef = self.cef.dict

    @property
    def dict(self):
        return dict(sorted({k: v for k, v in self.__dict__.items() if v is not None}.items()))

    def struct(self, **entries):
        """This will take a record and return an object."""
        self.__dict__.update(entries)
