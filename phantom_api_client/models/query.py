#!/usr/bin/env python3.8
"""Phantom API Client: Models.Query
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

import datetime as dt
import logging
from dataclasses import dataclass
from typing import List, Optional, Union

from copy import deepcopy
from delorean import Delorean, parse

from base_api_client.models import Record, sort_dict
from phantom_api_client.models import InvalidCombinationError

logger = logging.getLogger(__name__)


@dataclass
class Query(Record):
    """
    Attributes:
        type (str): action_run|artifact|asset|app|app_run|container|playbook_run|cluster_node|ph_user
        page (int): page number to retrieve
        page_size (int): how many results per page
        pretty (bool): pretty format results
        filter (dict): {'_filter_name__icontains': 'test'}
        include_expensive (bool): return all fields
        sort (str): field_name to sort on
        order (str): asc|desc; default desc

    References:
        https://my.phantom.us/4.1/docs/rest/query
    """
    page: Optional[int] = None
    page_size: Optional[int] = 1000  # Optimal page size (depends on semaphore); Change to 1000 after upgrade.
    pretty: Optional[Union[bool, int]] = None
    filter: Optional[Union[dict, None]] = None  # Gets converted to standard Phantom filters in __post_init__
    include_expensive: Optional[Union[bool, int]] = None
    sort: Optional[str] = None
    order: Optional[str] = None
    # Extras
    date_filter_start: Optional[Union[Delorean, str, None]] = None  # YYYY-MM-DDTHH:MM:SS.ffffff
    date_filter_end: Optional[Union[Delorean, str, None]] = None
    date_filter_field: Optional[str] = None  # One of:

    def __post_init__(self):
        if self.include_expensive or self.pretty:
            self.page_size = 500

        if self.pretty:
            self.pretty = 1

        if self.include_expensive:
            self.include_expensive = 1

        if self.filter:
            self.load(**self.filter)
            del self.filter

        if self.date_filter_start:
            self.date_filter_start = parse(self.date_filter_start, dayfirst=False, timezone='UTC')

        if self.date_filter_end:
            self.date_filter_end = parse(self.date_filter_end, dayfirst=False, timezone='UTC')

        if self.date_filter_start and not self.date_filter_end:
            self.date_filter_end = Delorean(timezone='UTC')

        if self.date_filter_end and not self.date_filter_start:
            self.date_filter_start = Delorean(datetime=dt.datetime(2000, 1, 1), timezone='UTC')


@dataclass
class ArtifactQuery(Query):
    """
    Valid Filter Fields
        case_artifact_map, cases, cef, cef_types, child_artifacts, container,
        id, create_time, data, description, end_time, evidence,
        has_note, hash, id, in_case, indicatorartifactrecord, indicators,
        ingest_app, ingest_app_id, kill_chain, label, name, note, owner,
        owner_id, parent_artifact, parent_artifact_id, parent_container,
        parent_container_id, playbook_run, playbook_run_id, severity,
        severity_id, source_artifact_map, source_data_identifier, start_time,
        tags, type, update_time, version

    Args:
        id (Optional[Union[int, List[int]]]):
        id  (Optional[Union[int, List[int]]]):
    """
    id: Optional[Union[int, List[int]]] = None
    container_id: Optional[Union[int, List[int]]] = None

    def __post_init__(self):
        super().__post_init__()

    def dict(self, cleanup: bool = True, dct: Optional[dict] = None, sort_order: str = 'asc') -> dict:
        """
        Args:
            cleanup (Optional[bool]):
            dct (Optional[dict]):
            sort_order (Optional[str]): ASC | DESC

        Returns:
            dct (dict):"""
        if not dct:
            dct = deepcopy(self.__dict__)

        try:
            del dct['id']
        except KeyError:
            pass

        try:
            del dct['container_id']
        except KeyError:
            pass

        try:
            del dct['date_filter_start']
        except KeyError:
            pass

        try:
            del dct['date_filter_end']
        except KeyError:
            pass

        try:
            del dct['date_filter_field']
        except KeyError:
            pass

        if cleanup:
            dct = {k: v for k, v in dct.items() if v is not None}

        if sort_order:
            dct = sort_dict(dct, reverse=True if sort_order.lower() == 'desc' else False)

        return dct

    @property
    def end_point(self):
        if self.container_id:
            ep = f'/container/{self.container_id}/artifacts'
        elif self.id:
            ep = f'/artifact/{self.id}'
        else:
            ep = '/artifact'

        return ep

    @property
    def data_key(self):
        if self.id and not type(self.container_id) is list:
            data_key = None
        else:
            data_key = 'data'

        return data_key


@dataclass
class AuditQuery(Query):
    format: Optional[str] = None  # default json
    start: Optional[str] = None  # ISO 8601 Date|Date-Time; Default 30 days prior
    end: Optional[str] = None  # ISO 8601 Date|Date-Time; Default now
    user: Optional[Union[int, str, List[Union[int, str]]]] = None
    role: Optional[Union[int, str, List[Union[int, str]]]] = None
    authentication: Optional[str] = None
    administration: Optional[str] = None
    playbook: Optional[Union[int, str, List[Union[int, str]]]] = None
    container: Optional[Union[int, str, List[Union[int, str]]]] = None

    def __post_init__(self):
        super().__post_init__()

        if self.user and type(self.user) is list:
            self.user = [str(u) for u in self.user]
            self.user = '%1E'.join(self.user)

        if self.role and type(self.role) is list:
            self.role = [str(r) for r in self.role]
            self.role = '%1E'.join(self.role)

        if self.playbook and type(self.playbook) is list:
            self.playbook = [str(p) for p in self.playbook]
            self.playbook = '%1E'.join(self.playbook)

        if self.container and type(self.container) is list:
            self.container = [str(c) for c in self.container]
            self.container = '%1E'.join(self.container)


@dataclass
class ContainerQuery(Query):
    id: Optional[Union[int, List[int]]] = None
    _annotation_whitelist_users: Optional[Union[bool, int]] = None
    whitelist_candidates: Optional[Union[bool, int]] = None
    phases: Optional[Union[bool, int]] = None
    page_size = 100000  # Temp fix for Phantom < 4.5

    def __post_init__(self):
        super().__post_init__()
        if self._annotation_whitelist_users:
            self._annotation_whitelist_users = 1

        if self.whitelist_candidates:
            self.whitelist_candidates = 1

        if self.phases:
            self.phases = 1

    def dict(self, cleanup: bool = True, dct: Optional[dict] = None, sort_order: str = 'asc') -> dict:
        """
        Args:
            cleanup (Optional[bool]):
            dct (Optional[dict]):
            sort_order (Optional[str]): ASC | DESC

        Returns:
            dct (dict):"""
        if not dct:
            dct = deepcopy(self.__dict__)

        try:
            del dct['phases']
        except KeyError:
            pass

        try:
            del dct['id']
        except KeyError:
            pass

        try:
            del dct['date_filter_start']
        except KeyError:
            pass

        try:
            del dct['date_filter_end']
        except KeyError:
            pass

        try:
            del dct['date_filter_field']
        except KeyError:
            pass

        if self.phases:
            for k, v in dct.items():
                if '_filter' in k:
                    del dct[k]

        if cleanup:
            dct = {k: v for k, v in dct.items() if v is not None}

        if sort_order:
            dct = sort_dict(dct, reverse=True if sort_order.lower() == 'desc' else False)

        return dct

    @property
    def end_point(self):
        try:
            if self.whitelist_candidates:
                wlp = '/permitted_users'
            elif self.phases:
                wlp = '/phases'
            else:
                wlp = ''
        except AttributeError:
            wlp = ''

        if self.id:
            if type(self.id) is list:
                if wlp:
                    raise InvalidCombinationError
                self._filter_id__in = str(self.id)
                ep = '/container'
            else:
                ep = f'/container/{self.id}{wlp}'
        else:
            ep = '/container'

        logger.debug(f'Getting container(s) {"phases" if wlp == "/phases" else ""}...')

        return ep

    @property
    def data_key(self):
        try:
            if self.whitelist_candidates:
                wlp = '/permitted_users'
            elif self.phases:
                wlp = '/phases'
            else:
                wlp = ''
        except AttributeError:
            wlp = ''

        if self.id and not type(self.id) is list:
            data_key = None
        else:
            data_key = 'data'

        if wlp == '/permitted_users':
            data_key = 'users'
        elif wlp == '/phases':
            data_key = 'data'

        return data_key


if __name__ == '__main__':
    print(__doc__)
