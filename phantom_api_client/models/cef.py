#!/usr/bin/env python3.8
"""Phantom API Client: Models.Cef
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
from typing import Union

from base_api_client.models import Record

logger = logging.getLogger(__name__)


@dataclass
class Cef(Record):
    ApplicationProtocol: Union[str, None] = None
    act: Union[str, None] = None
    app: Union[str, None] = None
    baseEventCount: Union[str, None] = None
    bytesIn: Union[str, None] = None
    bytesOut: Union[str, None] = None
    cat: Union[str, None] = None
    cn1: Union[str, None] = None
    cn1Label: Union[str, None] = None
    cn2: Union[str, None] = None
    cn2Label: Union[str, None] = None
    cn3: Union[str, None] = None
    cn3Label: Union[str, None] = None
    cnt: Union[str, None] = None
    cs1: Union[str, None] = None
    cs1Label: Union[str, None] = None
    cs2: Union[str, None] = None
    cs2Label: Union[str, None] = None
    cs3: Union[str, None] = None
    cs3Label: Union[str, None] = None
    cs4: Union[str, None] = None
    cs4Label: Union[str, None] = None
    cs5: Union[str, None] = None
    cs5Label: Union[str, None] = None
    cs6: Union[str, None] = None
    cs6Label: Union[str, None] = None
    destinationAddress: Union[str, None] = None
    destinationDnsDomain: Union[str, None] = None
    destinationHostName: Union[str, None] = None
    destinationMacAddress: Union[str, None] = None
    destinationNtDomain: Union[str, None] = None
    destinationPort: Union[str, None] = None
    destinationProcessName: Union[str, None] = None
    destinationServiceName: Union[str, None] = None
    destinationTranslatedAddress: Union[str, None] = None
    destinationTranslatedPort: Union[str, None] = None
    destinationUserId: Union[str, None] = None
    destinationUserName: Union[str, None] = None
    destinationUserPrivileges: Union[str, None] = None
    deviceAction: Union[str, None] = None
    deviceAddress: Union[str, None] = None
    deviceCustomDate1: Union[str, None] = None
    deviceCustomDate1Label: Union[str, None] = None
    deviceCustomDate2: Union[str, None] = None
    deviceCustomDate2Label: Union[str, None] = None
    deviceCustomNumber1: Union[str, None] = None
    deviceCustomNumber1Label: Union[str, None] = None
    deviceCustomNumber2: Union[str, None] = None
    deviceCustomNumber2Label: Union[str, None] = None
    deviceCustomNumber3: Union[str, None] = None
    deviceCustomNumber3Label: Union[str, None] = None
    deviceCustomString1: Union[str, None] = None
    deviceCustomString1Label: Union[str, None] = None
    deviceCustomString2: Union[str, None] = None
    deviceCustomString2Label: Union[str, None] = None
    deviceCustomString3: Union[str, None] = None
    deviceCustomString3Label: Union[str, None] = None
    deviceCustomString4: Union[str, None] = None
    deviceCustomString4Label: Union[str, None] = None
    deviceCustomString5: Union[str, None] = None
    deviceCustomString5Label: Union[str, None] = None
    deviceCustomString6: Union[str, None] = None
    deviceCustomString6Label: Union[str, None] = None
    deviceDirection: Union[str, None] = None
    deviceDnsDomain: Union[str, None] = None
    deviceEventCategory: Union[str, None] = None
    deviceExternalId: Union[str, None] = None
    deviceFacility: Union[str, None] = None
    deviceHostname: Union[str, None] = None
    deviceInboundInterface: Union[str, None] = None
    deviceMacAddress: Union[str, None] = None
    deviceOutboundInterface: Union[str, None] = None
    deviceProcessName: Union[str, None] = None
    deviceTranslatedAddress: Union[str, None] = None
    dhost: Union[str, None] = None
    dmac: Union[str, None] = None
    dntdom: Union[str, None] = None
    dpriv: Union[str, None] = None
    dproc: Union[str, None] = None
    dpt: Union[str, None] = None
    dst: Union[str, None] = None
    duid: Union[str, None] = None
    duser: Union[str, None] = None
    dvc: Union[str, None] = None
    dvchost: Union[str, None] = None
    end: Union[str, None] = None
    endTime: Union[str, None] = None
    externalId: Union[str, None] = None
    fileCreateTime: Union[str, None] = None
    fileHash: Union[str, None] = None
    fileId: Union[str, None] = None
    fileModificationTime: Union[str, None] = None
    fileName: Union[str, None] = None
    filePath: Union[str, None] = None
    filePermission: Union[str, None] = None
    fileSize: Union[str, None] = None
    fileType: Union[str, None] = None
    fname: Union[str, None] = None
    fsize: Union[str, None] = None
    _in: Union[str, None] = None
    message: Union[str, None] = None
    method: Union[str, None] = None
    msg: Union[str, None] = None
    oldfileCreateTime: Union[str, None] = None
    oldfileHash: Union[str, None] = None
    oldfileId: Union[str, None] = None
    oldfileModificationTime: Union[str, None] = None
    oldfileName: Union[str, None] = None
    oldfilePath: Union[str, None] = None
    oldfilePermission: Union[str, None] = None
    oldfileType: Union[str, None] = None
    oldfsize: Union[str, None] = None
    out: Union[str, None] = None
    proto: Union[str, None] = None
    receiptTime: Union[str, None] = None
    request: Union[str, None] = None
    requestClientApplication: Union[str, None] = None
    requestCookies: Union[str, None] = None
    requestMethod: Union[str, None] = None
    requestURL: Union[str, None] = None
    rt: Union[str, None] = None
    shost: Union[str, None] = None
    smac: Union[str, None] = None
    sntdom: Union[str, None] = None
    sourceAddress: Union[str, None] = None
    sourceDnsDomain: Union[str, None] = None
    sourceHostName: Union[str, None] = None
    sourceMacAddress: Union[str, None] = None
    sourceNtDomain: Union[str, None] = None
    sourcePort: Union[str, None] = None
    sourceServiceName: Union[str, None] = None
    sourceTranslatedAddress: Union[str, None] = None
    sourceTranslatedPort: Union[str, None] = None
    sourceUserId: Union[str, None] = None
    sourceUserName: Union[str, None] = None
    sourceUserPrivileges: Union[str, None] = None
    spriv: Union[str, None] = None
    spt: Union[str, None] = None
    src: Union[str, None] = None
    start: Union[str, None] = None
    startTime: Union[str, None] = None
    suid: Union[str, None] = None
    suser: Union[str, None] = None
    transportProtocol: Union[str, None] = None
    customCef: dict = None  # Must be single-level dict

    def __post_init__(self):
        if self.customCef:
            self.load(**self.customCef)

            del self.customCef


if __name__ == '__main__':
    print(__doc__)
