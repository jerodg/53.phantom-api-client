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
from typing import Any, List, Optional, Tuple, Union
from uuid import uuid4

import aiohttp as aio
import ujson

from base_api_client import BaseApiClient, Results
from phantom_api_client.models import ContainerRequest, RequestFilter

logger = logging.getLogger(__name__)


class PhantomApiClient(BaseApiClient):
    """Phantom API Client"""
    SEM: int = 15  # This defines the number of parallel async requests to make.

    def __init__(self, cfg: Union[str, dict], sem: Optional[int] = None):
        """Initializes Class

        Args:
            cfg (Union[str, dict]): As a str it should contain a full path
                pointing to a configuration file (json/toml). See
                config.* in the examples folder for reference.
            sem (Optional[int]): An integer that defines the number of parallel
                requests to make."""
        BaseApiClient.__init__(self, cfg=cfg, sem=sem or self.SEM)

        self.session = aio.ClientSession(headers={**self.HDR, 'ph-auth-token': self.cfg['Auth']['Token']},
                                         json_serialize=ujson.dumps,
                                         auth=aio.BasicAuth(login=self.cfg['Auth']['Username'],
                                                            password=self.cfg['Auth']['Password']))

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await BaseApiClient.__aexit__(self, exc_type, exc_val, exc_tb)

    async def get_artifact_count(self, container_id: int, filter: Optional[RequestFilter] = RequestFilter()) -> Results:
        filter.page_size = 1  # Only need one record to get the total count
        filter.page = 0

        logger.debug('Getting container count...')

        tasks = [asyncio.create_task(self.request(method='get',
                                                  end_point=f'/container/{container_id}/containers',
                                                  request_id=uuid4().hex,
                                                  params=filter.dict()))]

        results = Results(data=await asyncio.gather(*tasks))

        logger.debug('-> Complete.')

        return await self.process_results(results)

    async def get_container_count(self, filter: Optional[RequestFilter] = RequestFilter()) -> Results:
        filter.page_size = 1  # Only need one record to get the total count
        filter.page = 0

        logger.debug('Getting container count...')

        tasks = [asyncio.create_task(self.request(method='get',
                                                  end_point='/container',
                                                  request_id=uuid4().hex,
                                                  params=filter.dict()))]

        results = Results(data=await asyncio.gather(*tasks))

        logger.debug('-> Complete.')

        return await self.process_results(results)

    async def get_containers(self, filter: Optional[RequestFilter] = RequestFilter()) -> Results:
        if filter.limit:
            limit = filter.limit
            del filter.limit
        else:
            limit = (await self.get_container_count(filter)).success[0]['count']

        logger.debug('Getting containers...')

        tasks = []
        for i in range(0, (limit // filter.page_size)):
            filter.page = i
            tasks.append(asyncio.create_task(self.request(method='get',
                                                          end_point='/container',
                                                          request_id=uuid4().hex,
                                                          params=filter.dict())))

        results = Results(data=await asyncio.gather(*tasks))

        logger.debug('-> Complete.')

        return await self.process_results(results, 'data')

    async def create_artifacts(self, containers: List[ContainerRequest]) -> Tuple[Results, ContainerRequest]:
        # if type(containers) is not list:
        #     containers = [containers]

        # todo: handle failure (already exists?)
        # print('containers:', containers, type(containers))
        # print(containers[0].containers)
        logger.debug('Creating artifact(s)...')

        # We set the last artifact of the last container to run automation.
        # This will run automation on all newly created objects.

        if type(containers[0]) is ContainerRequest:
            try:
                containers[-1].artifacts[-1].run_automation = True
            except IndexError:  # Container doesn't have containers; NBD
                pass
            tasks = [asyncio.create_task(self.request(method='post',
                                                      end_point='/artifact',
                                                      request_id=a.request_id,
                                                      json=a.dict())) for x in containers for a in x.artifacts]
        else:  # ArtifactRequest
            containers[-1].run_automation = True
            tasks = [asyncio.create_task(self.request(method='post',
                                                      end_point='/artifact',
                                                      request_id=uuid4().hex,
                                                      json=a.dict())) for a in containers]

        results = await self.process_results(Results(data=await asyncio.gather(*tasks)))
        # print('artifact_results1:', results.data)
        # print('artifact_results1:')
        # print(*results.success, sep='\n')

        # Populate artifact id(s)
        [a.update_id(next((_['id'] for _ in results.success if _['request_id'] == a.request_id), None))
         for x in containers for a in x.artifacts]
        # print('artifact_results2:')
        # print(*results.success, sep='\n')
        logger.debug('-> Complete.')

        for result in results.success:
            result['artifact_id'] = result['id']
            del result['id']

        # print('artifact_results3:')
        # print(*results.success, sep='\n')

        # print('artifacts_done')
        # print(*containers, sep='\n')

        return results, containers

    async def create_containers(self, containers: Union[List[ContainerRequest], ContainerRequest],
                                revert_failure: bool = False, update_existing: Optional[bool] = False) -> Tuple[Results, Any]:
        # todo: handle revert_failure
        # todo: handle failure (already exists)
        # todo: handle update_existing
        if type(containers) is not list:
            containers = [containers]

        # print('containers0:', containers)
        # print('container0:', containers[0])
        # Create Containers
        logger.debug('Creating container(s)...')
        tasks = [asyncio.create_task(self.request(method='post',
                                                  end_point='/container',
                                                  request_id=c.request_id,
                                                  json=c.dict())) for c in containers]

        # print('results1:', results)
        # results = Results()
        container_results = await self.process_results(Results(data=await asyncio.gather(*tasks)))
        # print('container_results1:', container_results)
        logger.debug('-> Complete.')

        # if update_existing:
        #     needs_update = []
        #     if results := container_results.failure:
        #         for result in results:
        #             if result['existing_container_id']:
        #                 container = [c for c in containers if c.request_id == result['request_id']]
        #                 needs_update.append(container)
        #
        #     if needs_update:
        #         tasks = [asyncio.create_task(self.request(method='post',
        #                                                   end_point=f'/container/{c.id}',
        #                                                   request_id=uuid4().hex,
        #                                                   json=c.dict())) for c in containers]
        #         container_results = await self.process_results(Results(data=await asyncio.gather(*tasks)))

        # Populate container_id(s)
        [c.update_id(next((_['id'] for _ in container_results.success if _['request_id'] == c.request_id), None))
         for c in containers]

        for result in container_results.success:
            result['container_id'] = result['id']
            del result['id']

        # print('containers:')
        # print(*containers, sep='\n')

        # for c in containers:
        #     del c.request_id

        # Create Comments

        # Create Attachments

        # Create Artifacts
        # print('containers1:', containers)
        artifact_results, containers = await self.create_artifacts(containers)
        # print('artifact_reulst3:', artifact_results)

        # Combine all results into one response
        container_results.success.extend(artifact_results.success)
        container_results.failure.extend(artifact_results.failure)

        # container_results.cleanup()
        return container_results, containers

    async def delete_containers(self, container_ids: Union[List[int], int]):
        tasks = [asyncio.create_task(self.request(method='delete', end_point=f'/container/{cid}')) for cid in container_ids]

        return await self.process_results(Results(data=await asyncio.gather(*tasks)))


if __name__ == '__main__':
    print(__doc__)
