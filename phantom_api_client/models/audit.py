#!/usr/bin/env python3.8
"""Phantom API Client: Models.Audit
Copyright © 2019-2020 Jerod Gawne <https://github.com/jerodg/>

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

import datetime as dt
from dataclasses import dataclass
from typing import Union

from base_api_client.models.record import Record


@dataclass
class AuditRecord(Record):
    record: dict
    audit_id: Union[str, None] = None
    audit_source: Union[str, None] = None
    changed_field: Union[str, None] = None
    ip_address: Union[str, None] = None
    new_value: Union[str, None] = None
    note: Union[str, None] = None
    object_id: Union[int, None] = None
    object_type: Union[str, None] = None
    old_value: Union[str, None] = None
    related_object_id: Union[int, None] = None
    related_object_type: Union[str, None] = None
    tenants: Union[str, None] = None  # This is a list of integers as a string
    time: Union[str, dt.datetime, None] = None
    user: Union[str, None] = None
    user_id: Union[int, None] = None

    def __post_init__(self):
        self.record = {k.lower().replace(' ', '_'): v for k, v in self.record.items()}
        super(AuditRecord, self).load(**self.record)
        del self.record
        # todo: convert datetime, populate fields
