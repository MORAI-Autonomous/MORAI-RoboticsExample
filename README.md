# MORAI - EXAMPLE DOCKER
### Clone example branch 
```bash
git clone -b docker --single-branch https://github.com/MORAI-Autonomous/MORAI-RoboticsExample.git
cd MORAI-RoboticsExample
```

## Install [Docker](https://docs.docker.com/engine/install/ubuntu/) & [NVIDIA-Docker](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker)

```bash
sudo bash docker-install.sh
```

## Run
`MORAI-EXAMPLE` supports to setup conditions automatically, but `MORAI-SIM` needs to be installed and be running at least until the login screen, which is shown below.

<p align="center"><img src = "https://user-images.githubusercontent.com/93243768/163738426-3b31375a-838e-4a1c-b97d-fc6993d67262.png" width="60%"></p>

#### On host:
```bash
sudo bash docker-run.sh
```

#### On docker image:
```bash
sudo ./runner.sh
```
At the first, you should write your account information to the config.yaml

assume that the account is EXAMPLE_ID / EXAMPLE_PASSWD
```
>>> config.yaml
...
  ########### User setting ############
  user_id: 'EXAMPLE_ID' # User ID
  user_pw: 'EXAMPLE_PASSWD' # User Password
...
```
Check these parameters to change the modes
- `mapping` : set the mapping mode
  - `3d` (default) : use the LeGO-LOAM algorithm
  - `2d` : use the OGM-Cartographer algorithm
  - `none` : do not process the mapping algorithm
- `moving` : set the Ego vehicle control mode
  - `cruise` (defualt) : use the simulator built-in auto drive mode
  - `auto` : use the external control algorithm with ROS or UDP
  - `keyboard` : just control with keyboard and your hands

and close the config.yaml. Then, the algorithm is excuted automatically.

## Clean Docker image
```bash
sudo bash docker-clean.sh
```
