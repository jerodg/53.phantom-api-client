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
from typing import Any, List, NoReturn, Optional, Tuple, Union
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

    async def get_artifact_count(self, container_id: Optional[int] = None,
                                 query: Optional[ArtifactQuery] = ArtifactQuery(page=0, page_size=1)) -> Results:
        """
        Performs a single page query to get the 'results_count' & 'num_paqges' based on specified Query.
        Args:
            container_id (Optional[int]):
            query (Optional[Query]):

        Returns:
            results (Results)
        """
        logger.debug(f'Getting artifact count...')

        if container_id:
            ep = f'/container/{container_id}/artifacts'
        else:
            ep = '/artifact'

        tasks = [asyncio.create_task(self.request(method='get',
                                                  end_point=ep,
                                                  request_id=uuid4().hex,
                                                  params=query.dict()))]

        logger.debug('-> Complete.')

        return await self.process_results(Results(data=await asyncio.gather(*tasks)))

    async def get_artifacts(self, artifact_id: Optional[int] = None,
                            container_id: Optional[int] = None,
                            query: Optional[ArtifactQuery] = ArtifactQuery()) -> Results:
        """
        Can retrieve:
            - All artifacts
            - All artifacts from a single container
            - A single artifact
        Args:
            artifact_id (Optional[int]):
            container_id (Optional[int]):
            query (Optional[Query]):

        Returns:
            results (Results)
        """
        if container_id:
            ep = f'/container/{container_id}/artifacts'
        elif artifact_id:
            ep = f'/artifact/{artifact_id}'
        else:
            ep = '/artifact'

        if not artifact_id:
            page_limit = (await self.get_artifact_count(container_id=container_id, query=query)).success[0]['num_pages']
        else:  # When we're getting a single artifact we can skip paging
            page_limit = 1

        logger.debug(f'Getting artifact(s)...')

        tasks = [asyncio.create_task(self.request(method='get',
                                                  end_point=ep,
                                                  request_id=uuid4().hex,
                                                  params={**query.dict(), 'page': i}))
                 for i in range(0, page_limit)]

        results = Results(data=await asyncio.gather(*tasks))

        logger.debug('-> Complete.')

        return await self.process_results(results, 'data' if not artifact_id else None)

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

        for result in results.success:
            result['artifact_id'] = result['id']
            del result['id']

        logger.debug('-> Complete.')

        return results, containers

    async def get_record_count(self, query: Union[ArtifactQuery, AuditQuery, ContainerQuery]) -> Results:
        """
        Performs a single page query to get the 'results_count' & 'num_paqges' based on specified Query.
        Args:
            query (Optional[ContainerQuery]):

        Returns:
            results (Results)
        """
        logger.debug(f'Getting {type(query)} record count...')

        query.page = 0
        query.page_size = 1

        tasks = [asyncio.create_task(self.request(method='get',
                                                  end_point=query.endpoint,
                                                  request_id=uuid4().hex,
                                                  params=query.dict()))]

        logger.debug('-> Complete.')
        return await self.process_results(Results(data=await asyncio.gather(*tasks)))

    async def get_containers(self, query: Optional[ContainerQuery] = ContainerQuery()) -> Results:
        """
        Args:
            query (ContainerQuery):

        Returns:
            results (Results)"""
        if not query.container_id:
            res = await self.get_record_count(query=query)
            print('res:', res)
            print('success:', res.success)
            page_limit = (await self.get_record_count(query=query)).success[0]['num_pages']
        else:  # When we're getting a single container we can skip paging
            page_limit = 1

        tasks = [asyncio.create_task(self.request(method='get',
                                                  end_point=query.endpoint,
                                                  request_id=uuid4().hex,
                                                  params={**query.dict(), 'page': i}))
                 for i in range(0, page_limit)]

        results = await self.process_results(Results(data=await asyncio.gather(*tasks)), query.data_key)

        if query.date_filter_field:
            results = await self.__date_filter(query=query, results=results)

        logger.debug('-> Complete.')

        return results

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

        [c.update_id(next((_['id'] for _ in container_results.success if _['request_id'] == c.data['request_id']), None))
         for c in containers]

        for result in container_results.success:
            result['container_id'] = result['id']
            del result['id']

        artifact_results, containers = await self.create_artifacts(containers)
        container_results.success.extend(artifact_results.success)
        container_results.failure.extend(artifact_results.failure)

        return container_results, containers

    # async def get_user_count(self, query: Optional[Query] = None) -> Results:
    #     if not query:
    #         query = Query(type='ph_user', filter={'_filter_type__in': '["normal", "automation"]'}, page_size=1, page=0)
    #
    #     logger.debug('Getting user count...')
    #
    #     tasks = [asyncio.create_task(self.request(method='get',
    #                                               end_point=query.type,
    #                                               request_id=uuid4().hex,
    #                                               params=query.dict()))]
    #
    #     results = Results(data=await asyncio.gather(*tasks))
    #
    #     logger.debug('-> Complete.')
    #
    #     return await self.process_results(results)

    # async def get_users(self, user_id: Optional[int] = None, query: Optional[Query] = None) -> Results:
    #     if user_id:
    #         t = f'/ph_user/{user_id}'
    #     else:
    #         t = '/ph_user'
    #
    #     if not query:
    #         query = Query(type=t)
    #     elif not query.type:
    #         query.type = t
    #
    #     if not user_id:
    #         page_limit = (await self.get_user_count(query=query)).success[0]['num_pages']
    #     else:  # When we're getting a single user we can skip paging
    #         page_limit = 1
    #
    #     logger.debug(f'Getting user(s)...')
    #
    #     tasks = [asyncio.create_task(self.request(method='get',
    #                                               end_point=query.type,
    #                                               request_id=uuid4().hex,
    #                                               params={**query.dict(), 'page': i}))
    #              for i in range(0, page_limit)]
    #
    #     results = Results(data=await asyncio.gather(*tasks))
    #
    #     logger.debug('-> Complete.')
    #
    #     if user_id:
    #         data_key = None
    #     else:
    #         data_key = 'data'
    #
    #     return await self.process_results(results, data_key)

    async def get_audit_data(self, query: Optional[AuditQuery] = None) -> Results:
        """
        If no audit data is returned for a valid user then no audit data is
        present. Probably due to the user not having logged in before or a database reset.

        Args:
            query (Optional[Query]):

        Returns:
            results (Results)
        """
        logger.debug(f'Getting audit data...')

        t = '/audit'

        if not query:
            query = AuditQuery(type=t)
        elif not query.type:
            query.type = t

        tasks = [asyncio.create_task(self.request(method='get',
                                                  end_point=query.type,
                                                  request_id=uuid4().hex,
                                                  params=query.dict()))]

        results = Results(data=await asyncio.gather(*tasks))

        logger.debug('-> Complete.')

        return await self.process_results(results)

    async def delete_records(self, record_ids: Union[List[int], int], query: Union[ContainerQuery]) -> Results:
        """

        Args:
            record_ids (Union[List[int], int]):
            query (Query): query.type is required

        Returns:
            results (Results)
        """
        logger.debug(f'Deleting {type(query)}, record(s)...')
        self.sem = asyncio.Semaphore()  # Deletes need to be done more slowly. # todo: perhaps not; need more testing

        if not type(record_ids) is list:
            record_ids = [record_ids]

        if type(query) is ContainerQuery:
            ep = '/container'
        else:
            logger.error(f'Unknown query type: {type(query)}')
            raise NotImplementedError

        tasks = [asyncio.create_task(self.request(method='delete',
                                                  end_point=f'{ep}/{rid}',
                                                  request_id=uuid4().hex)) for rid in record_ids]

        results = Results(data=await asyncio.gather(*tasks))

        logger.debug('-> Complete.')

        try:
            self.sem = asyncio.Semaphore(self.cfg['Options']['SEM'])
        except KeyError:
            self.sem = asyncio.Semaphore(self.SEM)

        return await self.process_results(results)

    async def update_records(self, requests: Union[
        ContainerRequest, ArtifactRequest, List[Union[ContainerRequest, ArtifactRequest]]]) -> Results:
        """

        Args:
            requests (Union[
        ContainerRequest, ArtifactRequest, List[Union[ContainerRequest, ArtifactRequest]]]):

        Returns:
            results (Results)
        """
        logger.debug(f'Updating record(s)...')

        if not type(requests) is list:
            requests = [requests]

        tasks = []
        for request in requests:
            if type(request) is ContainerRequest:
                t = '/container'
            elif type(request) is ArtifactRequest:
                t = '/artifact'
            else:
                raise InvalidOptionError('update_request', ['ArtifactRequest', 'ContainerRequest'])

            tasks.append(asyncio.create_task(self.request(method='post',
                                                          end_point=f'{t}/{request.id}',
                                                          request_id=uuid4().hex,
                                                          json=request.dict())))

        results = Results(data=await asyncio.gather(*tasks))

        logger.debug('-> Complete.')

        return await self.process_results(results)


if __name__ == '__main__':
    print(__doc__)
