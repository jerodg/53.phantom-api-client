#!/usr/bin/env python3.8
"""Phantom API Client: Test Audit
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

# @pytest.mark.asyncio
# async def test_get_one_container_audit_data():
#     ts = time.perf_counter()
#     bprint('Test: Get One Container Audit Data')
#
#     async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
#         results = await pac.get_audit_data(query=AuditQuery(container=119109))
#         # print(results)
#
#         assert type(results) is Results
#         assert len(results.success) >= 1
#         assert not results.failure
#
#         tprint(results, top=5)
#
#     bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
#
#
# @pytest.mark.asyncio
# async def test_get_n_containers_audit_data():
#     ts = time.perf_counter()
#     bprint('Test: Get "N" Containers Audit Data')
#
#     async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
#         results = await pac.get_audit_data(query=AuditQuery(container=[119109, 119108]))
#         # print(results)
#
#         assert type(results) is Results
#         assert len(results.success) >= 1
#         assert not results.failure
#
#         tprint(results, top=5)
#
#     bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
#
#
# @pytest.mark.asyncio
# async def test_get_one_user_audit_data():
#     ts = time.perf_counter()
#     bprint('Test: Get One User Audit Data')
#
#     async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
#         results = await pac.get_audit_data(query=AuditQuery(user=5))
#         # print(results)
#
#         assert type(results) is Results
#         assert len(results.success) >= 1
#         assert not results.failure
#
#         tprint(results, top=5)
#
#     bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
#
#
# @pytest.mark.asyncio
# async def test_get_n_users_audit_data():
#     ts = time.perf_counter()
#     bprint('Test: Get "N" Users Audit Data')
#
#     async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
#         results = await pac.get_audit_data(query=AuditQuery(user=[5, 8]))
#         # print(results)
#
#         assert type(results) is Results
#         assert len(results.success) >= 1
#         assert not results.failure
#
#         tprint(results, top=5)
#
#     bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
