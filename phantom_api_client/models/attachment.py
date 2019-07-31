#!/usr/bin/env python3.8
"""Phantom API Client: Models.Attachment
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
from dataclasses import dataclass
from typing import Union

from base64 import b64encode
from os import stat
from os.path import basename

from phantom_api_client.models.exceptions import InvalidOptionError

logger = logging.getLogger(basename(__file__)[:-3])


@dataclass
class Attachment:
    """File size is limited to 32MB
    file_name defaults to basename of file_path"""
    file_path: str
    container_id: Union[int, None]
    file_name: Union[str, None] = None
    file_content: str = None  # base64 encoded
    metadata: Union[dict, None] = None

    def __post_init__(self):
        fsize = stat(self.file_path).st_size
        if fsize > 32000000:
            logger.exception(f'File: {self.file_path} is larger than the limit of 32MB ({fsize})')
            raise InvalidOptionError('file_size', ['<= 32MB'])

        try:
            with open(self.file_path, mode='rb') as f:
                self.file_content = b64encode(f.read()).decode()
        except OSError as ose:
            logger.exception(ose)
            raise OSError

        self.metadata = {'contains': ['vault_id']}

        if not self.file_name:
            self.file_name = basename(self.file_path)

        del self.file_path

    @property
    def dict(self):
        return dict(sorted({k: v for k, v in self.__dict__.items() if v is not None}.items()))
