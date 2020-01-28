#!/usr/bin/env python3.8
"""Phantom API Client
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

import asyncio
import logging
from typing import Any, List, NoReturn, Tuple, Union
from uuid import uuid4

from delorean import parse

from base_api_client import BaseApiClient, Results
from phantom_api_client.models import *

logger = logging.getLogger(__name__)


class PhantomApiClient(BaseApiClient):
    """Phantom API Client"""

    def __init__(self, cfg: Union[str, dict]):
        """Initializes Class

        Args:
            cfg (Union[str, dict]): As a str it should contain a full path
                pointing to a configuration file (json/toml). See
                config.* in the examples folder for reference.
            sem (Optional[int]): An integer that defines the number of parallel
                requests to make."""
        BaseApiClient.__init__(self, cfg=cfg)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type: None, exc_val: None, exc_tb: None) -> NoReturn:
        await BaseApiClient.__aexit__(self, exc_type, exc_val, exc_tb)

    @staticmethod
    async def __date_filter(query: Union[ContainerQuery], results: Results) -> Results:
        """Date Filter
           - Filters Results by date

        Args:
            query (Union[ContainerQuery]):
            results (Results):

        Returns:
            results (Results):
        """
        results.success = [r for r in results.success if query.date_filter_start <=
                           parse(r[query.date_filter_field], dayfirst=False) <= query.date_filter_end]
        return results

    async def get_record_count(self, query: Union[ArtifactQuery, ContainerQuery, UserQuery]) -> Results:
        """
        Performs a single page query to get the 'results_count' & 'num_paqges' based on specified Query.
        Args:
            query (Optional[ContainerQuery]):

        Returns:
            results (Results)
        """
        logger.debug(f'Getting {type(query)} record count...')

        if not query.page:
            query.page = 0
        if not query.page_size:
            query.page_size = 1

        tasks = [asyncio.create_task(self.request(method='get',
                                                  end_point=query.end_point,
                                                  request_id=uuid4().hex,
                                                  params=query.dict()))]

        logger.debug('-> Complete.')
        return await self.process_results(Results(data=await asyncio.gather(*tasks)))

    async def get_records(self, query: Union[ArtifactQuery, AuditQuery, ContainerQuery]) -> Results:
        """
        Args:
            query (ContainerQuery):

        Returns:
            results (Results)"""
        logger.debug(f'Getting {type(query)}, record(s)...')

        if type(query) is AuditQuery:
            page_limit = 1
        else:
            if not query.id:
                page_limit = (await self.get_record_count(query)).success[0]['num_pages']
            else:  # When we're getting a single container we can skip paging
                page_limit = 1

        tasks = [asyncio.create_task(self.request(method='get',
                                                  end_point=query.end_point,
                                                  request_id=uuid4().hex,
                                                  params={**query.dict(), 'page': i}))
                 for i in range(0, page_limit)]

        results = await self.process_results(Results(data=await asyncio.gather(*tasks)), query.data_key)

        if query.date_filter_field:
            results = await self.__date_filter(query=query, results=results)

        logger.debug('-> Complete.')

        return results

    async def delete_records(self, query: Union[List[ArtifactQuery], List[ContainerQuery]]) -> Results:
        """

        Args:
            query (List[Union[ArtifactQuery, ContainerQuery]]):

        Returns:
            results (Results)"""
        logger.debug(f'Deleting {type(query)}, record(s)...')

        if not type(query) is list:
            query = [query]

        tasks = [asyncio.create_task(self.request(method='delete',
                                                  end_point=q.end_point,
                                                  request_id=uuid4().hex)) for q in query]

        results = Results(data=await asyncio.gather(*tasks))

        logger.debug('-> Complete.')

        return await self.process_results(results)

    async def update_records(self, requests: List[Union[ContainerRequest, ArtifactRequest]]) -> Results:
        """

        Args:
            requests (Union[
        ContainerRequest, ArtifactRequest, List[Union[ContainerRequest, ArtifactRequest]]]):

        Returns:
            results (Results)"""
        logger.debug(f'Updating record(s)...')

        if not type(requests) is list:
            requests = [requests]

        tasks = [asyncio.create_task(self.request(method='post',
                                                  end_point=r.end_point,
                                                  request_id=uuid4().hex,
                                                  json=r.dict())) for r in requests]

        results = Results(data=await asyncio.gather(*tasks))

        logger.debug('-> Complete.')

        return await self.process_results(results)

    async def create_artifacts(self, containers: Union[List[ContainerRequest], ContainerRequest]) -> Tuple[
        Results, List[ContainerRequest]]:
        # todo: handle failure (already exists?)
        logger.debug('Creating artifact(s)...')
        if type(containers) is not list:
            containers = [containers]

        # if type(containers[0]) is ContainerRequest:
        tasks = [asyncio.create_task(self.request(method='post',
                                                  end_point='/artifact',
                                                  request_id=a.data['request_id'],
                                                  json=a.dict())) for x in containers for a in x.artifacts]
        # else:  # ArtifactRequest
        #     tasks = [asyncio.create_task(self.request(method='post',
        #                                               end_point='/artifact',
        #                                               request_id=a.data['request_id'],
        #                                               json=a.dict())) for a in containers]

        results = await self.process_results(Results(data=await asyncio.gather(*tasks)))

        [a.update_id(next((_['id'] for _ in results.success if _['request_id'] == a.data['request_id']), None))
         for x in containers for a in x.artifacts]

        logger.debug('-> Complete.')

        return results, containers

    async def create_containers(self, containers: Union[List[ContainerRequest], ContainerRequest]) -> Tuple[Results, Any]:
        # todo: handle revert_failure
        # todo: handle failure (already exists)
        # todo: handle update_existing
        if type(containers) is not list:
            containers = [containers]

        logger.debug('Creating container(s)...')
        tasks = [asyncio.create_task(self.request(method='post',
                                                  end_point='/container',
                                                  request_id=c.data['request_id'],
                                                  json=c.dict())) for c in containers]

        container_results = await self.process_results(Results(data=await asyncio.gather(*tasks)))
        logger.debug('-> Complete.')

        # print('container_results:\n', container_results)

        [c.update_id(next((_['id'] for _ in container_results.success if _['request_id'] == c.data['request_id']), None))
         for c in containers]

        artifact_results, containers = await self.create_artifacts(containers)
        container_results.success.extend(artifact_results.success)
        container_results.failure.extend(artifact_results.failure)

        return container_results, containers


if __name__ == '__main__':
    print(__doc__)
