FROM ros:melodic

ENV NVIDIA_VISIBLE_DEVICES \
    ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES \
    ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
 && apt-get install -y --no-install-recommends wget nano unzip build-essential libomp-dev python3-pip python-pip\
                                               libpcap-dev libmetis-dev ros-melodic-pcl-ros ros-melodic-image-transport \
                                               libeigen3-dev gedit pcl-tools \
                                               ros-melodic-tf ros-melodic-cv-bridge ros-melodic-rviz \
                                               ros-melodic-message-filters cmake ros-melodic-xacro \
                                               ros-melodic-rosbridge-server python-rospkg \
                                               ros-melodic-diagnostics ros-melodic-roslint \
                                               ros-melodic-velodyne libyaml-cpp-dev tmux python3-setuptools\
 && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install -U numpy==1.16.6 pandas==0.24.2 pyyaml
RUN pip install -U niet==1.8.2 pandas==0.24.2 pyyaml

WORKDIR /root
RUN wget -O gtsam.zip https://github.com/borglab/gtsam/archive/4.0.0-alpha2.zip
RUN unzip gtsam.zip
RUN mkdir /root/gtsam-4.0.0-alpha2/build
WORKDIR /root/gtsam-4.0.0-alpha2/build
RUN cmake .. && make -j4 2> /dev/null
RUN make install

RUN mkdir -p /root/catkin_ws/src
WORKDIR /root/catkin_ws/src
RUN /bin/bash -c '. /opt/ros/melodic/setup.bash; catkin_init_workspace'

RUN sed -i '9c #include "lz4.h"' /usr/include/flann/util/serialization.h
RUN sed -i '10c #include "lz4hc.h"' /usr/include/flann/util/serialization.h

RUN git clone -b robotics --single-branch https://github.com/MORAI-Autonomous/MORAI-EXAMPLE.git
RUN mv MORAI-EXAMPLE/config.yaml /root/catkin_ws/
RUN mv MORAI-EXAMPLE/runner.sh /root/catkin_ws/

WORKDIR /root/catkin_ws
RUN /bin/bash -c '. /opt/ros/melodic/setup.bash; catkin_make -j1'

WORKDIR /root/catkin_ws/src/MORAI-EXAMPLE/SLAM/OGM/scripts
RUN chmod +x *.py

WORKDIR /root/catkin_ws/src/MORAI-EXAMPLE/AD/ros/scripts
RUN chmod +x *.py

WORKDIR /root/catkin_ws/src/MORAI-EXAMPLE/EgoCtrl/scripts
RUN chmod +x *.py

WORKDIR /root/catkin_ws
RUN sed -i "6i source \"/root/catkin_ws/devel/setup.bash\"" /ros_entrypoint.sh

WORKDIR /

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]
