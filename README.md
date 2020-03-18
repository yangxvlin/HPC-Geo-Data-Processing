# HPC-Geo-Data-Processing
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
COMP90024 Cluster and Cloud Computing - Assignment 1 - 2020S1

## Contributors
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/Olivia0012"><img src="https://avatars3.githubusercontent.com/u/55537942?v=4" width="100px;" alt=""/><br /><sub><b>Olivia</b></sub></a><br /><a href="https://github.com/yangxvlin/HPC-Geo-Data-Processing/commits?author=Olivia0012" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- markdownlint-disable -->
<table>
  <tr>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->
<table>
  <tr>
  </tr>
</table>

## how to run
1. ```pip install -r requirements.txt```
2. run program on computer
```
mpiexec -n numprocs python -m mpi4py pyfile
mpiexec -n 8 python -m mpi4py main.py -grid ../data/melbGrid.json -data ../data/testTwitter.json
mpiexec -n 8 python -m mpi4py main.py -grid ../data/melbGrid.json -data ../data/smallTwitter.json
```
