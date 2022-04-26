[![MORAILog](./docs/MORAI_Logo.png)](https://www.morai.ai)
===
# MORAI - Robotics example

First step to enjoy the `MORAI Sim: Robotics`

This example support Ubuntu 18.04 or later
```
./
├── AD                        # [Autonomous Drive] Trajectory following example project
│    ├── autonomous_driving     # Algorithm scripts
│    ├── ros                    # ROS1 interface scripts
│    └── udp                    # UDP interface scripts
├── EgoCtrl                   # Simulator control scripts to launch the SLAM examples
├── SLAM                      # SLAM example projects (can use Docker only)
│    ├── LeGO-LOAM              # LeGO-LOAM -> 3D SLAM example with ROS1 interface
│    └── ogm_cartographer       # Cartographer -> 2D SLAM example with ROS1 interface
├── docker                    # Other scripts to manage the docker image
├── msgs                      # ROS1 message files to play examples
├── config.yaml               # Configure file to launch the SLAM example
└── runner.sh                 # SLAM example launcher script
```

- AD(Autonomous Drive)
  - Trajectory follower
  - ROS / UDP communication
  - Smart(adaptive) Cruise Control

- SLAM
  - LeGO-LOAM - 3D SLAM algorithm using a multi channel LiDAR sensor
  - OGM-Cartographer(Google Cartographer for MORAI Robotics) - 2D SLAM algorithm using a single channel LiDAR sensor

# Requirement

- ROS1 desktop-full >= melodic

- python >= 3.7

- niet

- tmux

# Installation

## Native Linux Environment 
#### (only supports the `Autonomous Drive example`)
Basically need packages
```
$ sudo pip install niet
$ sudo apt install tmux
```
### ROS interface
```
$ mkdir -p ~/catkin_ws/src
$ cd ~/catkin_ws/src && catkin_init_workspace
$ git clone https://github.com/MORAI-Autonomous/MORAI-RoboticsExample.git
$ touch MORAI-RoboticsExample/SLAM/LeGO-LOAM/CATKIN_IGNORE
$ touch MORAI-RoboticsExample/SLAM/ogm_cartographer/CATKIN_IGNORE
$ cd ~/catkin_ws
$ rosdep install --from-paths . --ignore-src -r -y
$ find -name 'requirements.txt' | xargs -L 1 sudo pip install -U -r
$ catkin_make
$ source devel/setup.bash
```

### UDP interface
```
$ git clone https://github.com/MORAI-Autonomous/MORAI-RoboticsExample.git
$ cd MORAI-RoboticsExample
$ find -name 'requirements.txt' | xargs -L 1 sudo pip install -U -r
```

## Docker 
#### (supports all examples. [Easy to use](https://github.com/MORAI-Autonomous/MORAI-RoboticsExample/tree/docker))
```
$ git clone -b docker --single-branch https://github.com/MORAI-Autonomous/MORAI-RoboticsExample.git
$ cd MORAI-RoboticsExample
$ sudo ./docker-install.sh
```

# Usage

## AD with ROS
Follow this step if you want to change the trajectory.
```
$ roslaunch morai_standard path_maker.launch
```

Enjoy the example which follow the trajectory with smart cruise control.
```
$ roslaunch morai_standard morai_standard.launch
```

## AD with UDP
```
$ cd AD/udp
```
Follow this step if you want to change the trajectory.
```
$ python3 ./path_maker.py
```

Enjoy the example which follow the trajectory with smart cruise control.
```
$ python3 ./main.py
```

## SLAM with ROS
##### [Easy to use](https://github.com/MORAI-Autonomous/MORAI-RoboticsExample/tree/docker)
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

and then, excute the runner.sh
```
$ ./runner.sh
```

## Docker
##### [Easy to use](https://github.com/MORAI-Autonomous/MORAI-RoboticsExample/tree/docker)
### launch
`MORAI-RoboticsExample` supports to setup conditions automatically, but `MORAI-SIM` needs to be installed and be running at least until the login screen, which is shown below.
![logon_screen](./docs/logon_screen.png)

# License
- MORAI AD License info:  [AD License](./docs/License.md)
- ogm_cartographer License info:  [Cartographer License](./SLAM/ogm_cartographer/LICENSE)
- LeGO-LOAM License info:  [LeGO-LOAM License](./SLAM/LeGO-LOAM/LICENSE)

# Cite SC-LeGO-LOAM
In repository, the [LeGO-LOAM](https://github.com/MORAI-Autonomous/MORAI-RoboticsExample/tree/main/SLAM/LeGO-LOAM) code is modified from [SC-LeGO-LOAM](https://github.com/irapkaist/SC-LeGO-LOAM) which is an extended version of LeGO-LOAM integrated with [Scan Context++](https://github.com/irapkaist/scancontext).
```@INPROCEEDINGS { gkim-2018-iros,
  author = {Kim, Giseop and Kim, Ayoung},
  title = { Scan Context: Egocentric Spatial Descriptor for Place Recognition within {3D} Point Cloud Map },
  booktitle = { Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems },
  year = { 2018 },
  month = { Oct. },
  address = { Madrid }
}
```
```@inproceedings{legoloam2018,
  title={LeGO-LOAM: Lightweight and Ground-Optimized Lidar Odometry and Mapping on Variable Terrain},
  author={Shan, Tixiao and Englot, Brendan},
  booktitle={IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  pages={4758-4765},
  year={2018},
  organization={IEEE}
}
```
