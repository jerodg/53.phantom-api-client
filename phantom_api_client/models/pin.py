#!/usr/bin/env python3.8
"""Phantom API Client: Models.ArtifactRequest
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
from dataclasses import dataclass

from os.path import basename

logger = logging.getLogger(basename(__file__)[:-3])


# todo: update exception to you invalidoption error
@dataclass()
class Pin:
    container_id: int
    message: str
    data: str
    playbook_id: int = None
    pin_type: str = 'data'
    pin_style: str = None

    def __post_init__(self):
        error = False

        pin_type_opts = ['data', 'card_small', 'card_medium', 'card_large']
        if self.pin_type not in pin_type_opts:
            error = True
            logger.exception(f'pin_type must be one of: {pin_type_opts}')

        pin_style_opts = ['white', 'purple', 'red', None]
        if self.pin_style not in pin_style_opts:
            error = True
            logger.exception(f'pin_style must be one of: {pin_style_opts}')

        if error:
            raise NotImplementedError
