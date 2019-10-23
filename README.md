```
 ___ _             _                 _   ___ ___    ___ _ _         _   
| _ \ |_  __ _ _ _| |_ ___ _ __     /_\ | _ \_ _|  / __| (_)___ _ _| |_ 
|  _/ ' \/ _` | ' \  _/ _ \ '  \   / _ \|  _/| |  | (__| | / -_) ' \  _|
|_| |_||_\__,_|_||_\__\___/_|_|_| /_/ \_\_| |___|  \___|_|_\___|_||_\__|
```

![platform](https://img.shields.io/badge/Platform-Mac/*nix/Windows-blue.svg)
![python](https://img.shields.io/badge/Python-3.7/8%2B-blue.svg)
![phantom](https://img.shields.io/badge/Phantom-4.5+-blue.svg)
<a href="https://www.mongodb.com/licensing/server-side-public-license"><img src="https://img.shields.io/badge/License-SSPL-green.svg"></a>
![0%](https://img.shields.io/badge/Coverage-%25-red.svg)
<a href="https://saythanks.io/to/jerodg"><img src="https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg"></a>

# Splunk-Phantom, API client.
Client library for Phantom's REST API.

Developed for use with Phantom v4.5+, however, most functionality *should work 
with previous versions.

Developed for use with Python3.8+, however, it should work with 3.6/7+. There is
no guarantee that future development won't utilize 3.8+ specifc syntax.

__*Not Affiliated with Splunk or Phantom__

## Installation
```bash
pip install phantom-api-client
```

## Basic Usage
This modules' primary use-case is inheritance from other REST API clients.

```python

```

## Special Features (Not Offered by REST API)
- [ ] Get containers; Filtered by Date-Range

## API Implementation, Categories (2/24) ~8.3%, Functions (32/118) ~27.1%
__*These should match unit tests.__
- [ ] Actions:
    - [ ] Run Action
    - [ ] Cancel Running Action
- [ ] Aggregation Rules:
    - [ ] Create Rule
    - [ ] Update Rule
    - [ ] Delete Rule
- [ ] Apps:
    - [ ] Install App    
- [x] Artifacts:
    - [x] Get All Artifacts Count
    - [x] Get Container Artifacts Count
    - [x] Get All Artifacts
    - [x] Get One Artifact
    - [x] Get All Container Artifacts    
    - [x] Create One Artifact
    - [x] Create Artifacts
    - [x] Update Artifact
    - [x] Update Artifacts
    - [x] Delete One Artifact
    - [x] Delete Artifacts
- [ ] Assets:
    - [ ] Create Assets
- [ ] Attachments:
    - [ ] Get Attachment
    - [ ] Get Attachments
    - [ ] Create Attachment
    - [ ] Delete Attachment
- [ ] Audit:
    - [ ] Get One User Audit Data
    - [ ] Get 'N' Users Audit Data
    - [ ] Get One Role Audit Data
    - [ ] Get 'N' Role Audit Data
    - [ ] Get Authentication Audit Data
    - [ ] Get Administration Audit Data
    - [ ] Get One Playbook Audit Data
    - [ ] Get 'N' Playbooks Audit Data
    - [x] Get One Container Audit Data
    - [x] Get 'N' Containers Audit Data
    - [ ] Get All Audit Data
- [ ] CEF:
    - [ ] Get Available CEFs
    - [ ] Create Custom CEF
    - [ ] Get Custom CEFs
    - [ ] Get Custom CEF
    - [ ] Update Custom CEF
    - [ ] Delete Custom CEF
- [ ] Clustering:
    - [ ] Get Nodes
- [x] Containers:
    - [x] Get Containers Count
    - [x] Get Containers Count Filtered
    - [x] Get All Containers
    - [x] Get All Containers Filtered
    - [x] Get One Container
    - [x] Get Many Containers
    - [x] Create One Container
    - [x] Create Containers
    - [x] Update Container
    - [x] Update Containers
    - [x] Delete Container
    - [x] Delete Containers
    - [x] Get Container Phases
    - [x] Get Container Whitelisted Users
    - [x] Get Whitelist Candidates (users who can view a container)
- [ ] Custom Lists:
    - [ ] Get List
    - [ ] Create List
    - [ ] Update List
    - [ ] Delete List
- [ ] Evidence:
    - [ ] Get Container Evidence
    - [ ] Create Container Evidence
    - [ ] Delete Container Evidence
- [ ] HUD:
    - [ ] Pin Container
    - [ ] Update Pin
- [ ] Indicators:
    - [ ] Get Indicator Counts
    - [ ] Get Top Event Labels
    - [ ] Get Top Indicator Types
    - [ ] Get Top Indicator Values
    - [ ] Get Indicators
    - [ ] Get Indicator
    - [ ] Get Artifacts by Indicator
    - [ ] Get Indicator Timeline by Value
    - [ ] Get Containers by Indicator
- [ ] Informational:
    - [ ] Get Version
    - [ ] Get System Info
    - [ ] Get License
    - [ ] Get System Health
    - [ ] Get App Status Info
    - [ ] Get Widget Info    
- [ ] Notes:
    - [ ] Create Container Note
    - [ ] Create Containers Notes
    - [ ] Create Artifact Note
    - [ ] Create Task Note
    - [ ] Update Container Note
    - [ ] Get Container Notes
    - [ ] Get Container Note
    - [ ] Delete Note
    - [ ] Get Artifact Notes
    - [ ] Get Task Notes
    - [ ] Search Notes
- [ ] Playbooks:
    - [ ] Update Playbook Status
    - [ ] Run Playbook
    - [ ] Cancel Running Playbook
    - [ ] Update Source Control Repository
- [ ] Search:
    - [ ] Run Search
- [ ] Severity:
    - [ ] Get Severity's
    - [ ] Create Severity
    - [ ] Delete Severity
    - [ ] Update Severity
- [ ] Status:
    - [ ] Get Status Labels
    - [ ] Create Status Label
    - [ ] Delete Status Label
- [ ] System Settings:
    - [ ] Update System Settings
- [ ] Tenants:
    - [ ] Create Tenant
    - [ ] Update Tenant
- [ ] Users:
    - [x] Get Users Count
    - [x] Get One User
    - [x] Get All Users
    - [ ] Create One User
    - [ ] Update One User
    - [x] Delete One User
    - [ ] Create Role/Permissions
- [ ] Workbooks (formerly known as Case Templates):
    - [ ] Create Case Workflow Template
    - [ ] Create Phase Object
    - [ ] Create Task Object
    - [ ] Add Phase Template to Workflow Template
    - [ ] Add Task to Phase Template 
    - [ ] Get Workbook Phases

## Performance Notes
Phantom v4.2.7532 | Intel(R) Xeon(R) CPU E7-8860 v4 @ 2.20GHz (8 Cores VMWare) | 32GB RAM

#### Get Containers
_No Pretty or Expensive_

| Semaphore 	| PageSize 	| ResultsCount 	| Duration (seconds) 	| Records/Sec.  |
|-----------	|----------	|--------------	|--------------------	| ------------  |
| 1	| 0	| 10260	| 550.368098	| 18.642069	|
| 1	| 100	| 10242	| 506.718879	| 20.212390 |
| 1	| 250	| 10245	| 507.401462	| 20.191112 |
| 1	| 500	| 10247	| 505.141626	| 20.285400 |
| 1	| 1000	| 10248	| 499.583309	| **20.513095** |
| 5	| 100	| 10252	| 103.920112	| 98.652703 |
| 5	| 250	| 10252	| 104.045734	| 98.533592 |
| 5 | 500	| 10252	| 103.959837	| **98.615006** |
| 5 | 1000	| 10252	| 103.284216	| 99.260084 |
| 10	| 100	| 10252	| 62.194716	| 164.83715 |
| 10	| 250	| 10252	| 61.711901	| **166.12678** |
| 10	| 500	| 10252	| 61.747280	| 166.03160 |
| 10	| 1000	| 10252	| 61.791430	| 165.91297 |
| 15	| 100	| 10252	| 53.376854	| 192.068269	|
| 15	| 250	| 10252	| 53.870317	| 190.308884	|
| 15	| 500	| 10252	| 53.380755	| 192.054232	|
| 15	| 1000	| 10252	| 53.107964	| **193.040729**	|
| 25	| 100	| 10252	| 52.471258	| 195.383156	|
| 25	| 250	| 10252	| 52.522734	| 195.191668	|
| 25	| 500	| 10253	| 54.730120	| 187.337430	|
| 25	| 1000	| 10253	| 52.401570	| **195.662075**	|
| 50	| 100	| 10253	| 52.405708	| **195.646626**	|
| 50	| 250	| 10253	| 53.681816	| 190.995773	|
| 50	| 500	| 10253	| 53.105051	| 193.070148	|
| 50	| 1000	| 10253	| 52.813425	| 194.136245	|
| 75	| 100	| 10258	| 59.042822	| **173.738309**	|
| 75	| 250	| 10258	| 60.795224	| 168.730359	|
| 75	| 500	| 10258	| 62.890662	| 163.108475	|
| 75	| 1000	| 10258	| 65.159076	| 157.430102	|

More than 100 simultaneous connections/queries results in missing records.

| Semaphore 	| PageSize 	| ResultsCount 	| Duration (seconds) 	| Records/Sec.  |
|-----------	|----------	|--------------	|--------------------	| ------------  |
| 100	| 100	| 7995	| 47.714157	| **167.560332**	|
| 100	| 250	| 1483	| 14.284200	| 103.821007	|
| 100	| 500	| 1501	| 15.164913	| 98.978475	|
| 100	| 1000	| 1012	| 12.785591	| 79.151602	|
| 250	| 100	| 1043	| 13.511003	| 77.196340	|
| 250	| 250	| 1568	| 17.039635	| 92.020751	|
| 250	| 500	| 1592	| 16.626970	| **95.748051**	|
| 250	| 1000	| 1493	| 17.328146	| 86.160400	|

## Documentation
[GitHub Pages](https://jerodg.github.io/phantom-api-client/)
- Work in Process

## Known Issues
Mass deleting records quits early with timeout error. It would seem the more 
records that are being deleted adds an exponential increase in wait between 
deletes. So far in testing >= 47 (254) 114 at once results in timeout-error.


Phantom v4.2 and earlier has completely broken pagination. You will receive 
duplicate and missing records. You should set the query filter 'page_size' to 
a number greater than the max expected results in order to receive all records 
in a single page.


## License
Copyright © 2019 Jerod Gawne <https://github.com/jerodg/>

This program is free software: you can redistribute it and/or modify
it under the terms of the Server Side Public License (SSPL) as
published by MongoDB, Inc., either version 1 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
SSPL for more details.

You should have received a copy of the SSPL along with this program.
If not, see <https://www.mongodb.com/licensing/server-side-public-license>.
