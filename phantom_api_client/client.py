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
from typing import List, Optional, Union
from uuid import uuid4

import aiohttp as aio
import ujson

from base_api_client import BaseApiClient, Results
from phantom_api_client.models import ContainerFilter, ContainerRequest

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

        self.header = {**self.HDR, 'ph-auth-token': self.cfg['Auth']['Token']}

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await BaseApiClient.__aexit__(self, exc_type, exc_val, exc_tb)

    async def get_container_count(self, filter: Optional[ContainerFilter] = ContainerFilter()) -> Results:
        filter.page_size = 1  # Only need one record to get the total count
        filter.page = 0

        async with aio.ClientSession(headers=self.header, json_serialize=ujson.dumps) as session:
            logger.debug('Getting container count...')

            tasks = [asyncio.create_task(self.request(method='get',
                                                      end_point='/container',
                                                      session=session,
                                                      request_id=uuid4().hex,
                                                      params=filter.dict()))]

            results = Results(data=await asyncio.gather(*tasks))

            logger.debug('-> Complete.')

        await session.close()

        return await self.process_results(results)

    async def get_containers(self, filter: Optional[ContainerFilter] = ContainerFilter()) -> Results:
        if filter.limit:
            limit = filter.limit
            del filter.limit
        else:
            limit = (await self.get_container_count(filter)).success[0]['container_count']

        async with aio.ClientSession(headers=self.header, json_serialize=ujson.dumps) as session:
            logger.debug('Getting containers...')

            tasks = []
            for i in range(0, (limit // filter.page_size)):
                filter.page = i
                tasks.append(asyncio.create_task(self.request(method='get',
                                                              end_point='/container',
                                                              session=session,
                                                              request_id=uuid4().hex,
                                                              params=filter.dict())))

            results = await asyncio.gather(*tasks)

            logger.debug('-> Complete.')

        await session.close()

        return await self.process_results(results, 'data')

    async def create_containers(self, containers: Union[List[ContainerRequest], ContainerRequest]) -> Results:

        async with aio.ClientSession(headers=self.header, json_serialize=ujson.dumps) as session:
            logger.debug('Creating container(s)...')

            tasks = [asyncio.create_task(self.request(method='post',
                                                      end_point='/container',
                                                      session=session,
                                                      json=c.dict())) for c in containers]

            results = await asyncio.gather(*tasks)

            logger.debug('-> Complete.')

        await session.close()

        return await self.process_results(results, 'data')


if __name__ == '__main__':
    print(__doc__)
