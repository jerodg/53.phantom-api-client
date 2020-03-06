#!/usr/bin/env python3.8
"""Phantom API Client: Models.Exceptions
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
import logging
from typing import Union

logger = logging.getLogger(__name__)


class InvalidOptionError(Exception):
    def __init__(self, name: str, message: Union[str, list]):
        super().__init__(message)
        self.name = name
        self.message = message

    def __str__(self):
        if type(self.message) is list:
            msg = '\n'.join(self.message)
        else:
            msg = str(self.message)

        logger.error(f'Invalid Option for {self.name}; should be one of:\n{msg}')

    def __repr__(self):
        if type(self.message) is list:
            msg = '\n'.join(self.message)
        else:
            msg = str(self.message)

        logger.error(f'\nInvalid Option for {self.name}; should be one of:\n{msg}')


class InvalidCombinationError(Exception):
    def __init__(self, ):
        pass
        # tood: research custom exceptions better
