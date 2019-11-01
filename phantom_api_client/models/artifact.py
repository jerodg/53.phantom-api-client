#!/usr/bin/env python3.8
"""Phantom API Client: Models.ArtifactRequest
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

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union
from uuid import uuid4

from copy import deepcopy

from base_api_client.models.record import Record, sort_dict
from phantom_api_client.models.cef import Cef

logger = logging.getLogger(__name__)


@dataclass
class ArtifactRequest(Record):
    cef: Union[Cef, dict, None] = None  # Common Event Format
    cef_types: Union[Dict[str, List[str]], None] = None
    container_id: Union[int, None] = None
    data: Union[dict, None] = field(default_factory=dict)
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
    # Extras
    id: int = None

    def __post_init__(self):

        if type(self.cef) is Cef:
            self.cef = self.cef.dict()

        try:
            self.data = {**self.data, 'request_id': uuid4().hex}
        except TypeError:
            self.data = {'request_id': uuid4().hex}

    def update_id(self, artifact_id: int):
        self.id = artifact_id

    def dict(self, cleanup: bool = True, dct: Optional[dict] = None, sort_order: str = 'asc') -> dict:
        """
        Args:
            cleanup (Optional[bool]):
            dct (Optional[dict]):
            sort_order (Optional[str]): ASC | DESC

        Returns:
            dct (dict):"""
        dct = deepcopy(self.__dict__)

        del dct['id']

        if cleanup:
            dct = {k: v for k, v in dct.items() if v is not None}

        if sort_order:
            dct = sort_dict(dct, reverse=True if sort_order.lower() == 'desc' else False)

        return dct

    @property
    def end_point(self):
        return f'/artifact/{self.id}'


if __name__ == '__main__':
    print(__doc__)
