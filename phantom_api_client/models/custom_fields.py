#!/usr/bin/env python3.8
"""Phantom API Client: Models.Custom Fields
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

from dataclasses import dataclass
from typing import Union

from phantom_api_client.models.exceptions import InvalidOptionError


@dataclass
class CustomFields:
    """
    References:
        https://soflokydcphat01.info53.com/admin/product_settings/eventsettings/global"""
    alert_source: Union[str, None] = None
    resolution_summary: Union[str, None] = None
    incident_level: Union[str, None] = None
    incident_category: Union[str, None] = None
    true_resolution: Union[str, None] = None
    analysis_completed: Union[str, None] = None
    true_detect_time: Union[str, None] = None
    analysis_started: Union[str, None] = None
    compliance_contacted: Union[str, None] = None
    contain_time: Union[str, None] = None
    vendor_ticket_number: Union[str, None] = None
    mitigated: Union[str, None] = None
    disposition: Union[str, None] = None
    true_event_time: Union[str, None] = None
    customer_exposure: Union[str, None] = None

    def __post_init__(self):
        alert_source_opts = ['Ad-Hoc Notification',
                             'Bricata',
                             'Cisco-ISE',
                             'Cisco-WIPs',
                             'Crowdstrike',
                             'Cylance',
                             'Exabeam',
                             'FireEye',
                             'IDS-Fraud',
                             'InvestigationMailbox',
                             'McAfee-AV',
                             'McAfee-HIPS',
                             'MSSP',
                             'Overwatch',
                             'SecurityAwareness',
                             'Qradar',
                             'Phishlabs',
                             'Test',
                             'Ad-Hoc Notification',
                             'Splunk',
                             None]
        if self.alert_source not in alert_source_opts:
            raise InvalidOptionError('alert_source', alert_source_opts)

        incident_level_opts = ['1', '2', '3', 'Not Applicable', None]
        if self.incident_level not in incident_level_opts:
            raise InvalidOptionError('incident_Level', incident_level_opts)

        incident_category_opts = ['Customer Threat: Commercial ATO',
                                  'Customer Threat: Credential Reuse',
                                  'Customer Threat: Unauthorized Access',
                                  'Cyber Threat: Denial of Service',
                                  'Cyber Threat: Exploitation',
                                  'Cyber Threat: Malware',
                                  'Cyber Threat: Reconnaissance',
                                  'Insider Threat: DLP',
                                  'Insider Threat: NAC',
                                  'Insider Threat: Suspicious Activity',
                                  'Insider Threat: UEBA',
                                  'Cyber Threat: Phishing',
                                  'Cyber Threat: Vishing',
                                  'Cyber Threat: Phishing Redirect',
                                  'Test',
                                  'MSS',
                                  None]
        if self.incident_category not in incident_category_opts:
            raise InvalidOptionError('incident_category', incident_category_opts)

        compliance_contacted_opts = ['Yes', 'No', None]
        if self.compliance_contacted not in compliance_contacted_opts:
            raise InvalidOptionError('compliance_contacted', compliance_contacted_opts)

        mitigated_opts = ['Yes', 'No', 'Not Applicable', None]
        if self.mitigated not in mitigated_opts:
            raise InvalidOptionError('mitigated', mitigated_opts)

        disposition_opts = ['False Positive', 'Security Event', 'Red Team', 'Security Incident', None]
        if self.disposition not in disposition_opts:
            raise InvalidOptionError('disposition', disposition_opts)

        customer_exposure_opts = ['Yes', 'No', None]
        if self.customer_exposure not in customer_exposure_opts:
            raise InvalidOptionError('customer_exposure', customer_exposure_opts)

    @property
    def dict(self):
        d = {'Alert Source':         self.alert_source,
             'Resolution Summary':   self.resolution_summary,
             'Incident Level':       self.incident_level,
             'Incident Category':    self.incident_category,
             'True Resolution':      self.true_resolution,
             'Analysis Completed':   self.analysis_completed,
             'True Detect Time':     self.true_detect_time,
             'Analysis Started':     self.analysis_started,
             'Compliance Contacted': self.compliance_contacted,
             'Contain Time':         self.contain_time,
             'Vendor Ticket Number': self.vendor_ticket_number,
             'Mitigated':            self.mitigated,
             'Disposition':          self.disposition,
             'True Event Time':      self.true_event_time,
             'Customer Exposure':    self.customer_exposure}

        return dict(sorted({k: v for k, v in d.items() if v is not None}.items()))
