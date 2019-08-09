```
 ___ _             _                 _   ___ ___    ___ _ _         _   
| _ \ |_  __ _ _ _| |_ ___ _ __     /_\ | _ \_ _|  / __| (_)___ _ _| |_ 
|  _/ ' \/ _` | ' \  _/ _ \ '  \   / _ \|  _/| |  | (__| | / -_) ' \  _|
|_| |_||_\__,_|_||_\__\___/_|_|_| /_/ \_\_| |___|  \___|_|_\___|_||_\__|
```

![platform](https://img.shields.io/badge/Platform-Mac/*nix/Windows-blue.svg)
![python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![phantom](https://img.shields.io/badge/Phantom-4.2+-blue.svg)
<a href="https://www.mongodb.com/licensing/server-side-public-license"><img src="https://img.shields.io/badge/License-SSPL-green.svg"></a>
![0%](https://img.shields.io/badge/Coverage-0%25-red.svg)
<a href="https://saythanks.io/to/jerodg"><img src="https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg"></a>

(Splunk) Phantom API client.

## Installation
```bash
pip install phantom-api-client
```

## Basic Usage
This modules' primary use-case is inheritance from other REST API clients.

```python

```

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
