#!/bin/bash
xhost +
TAG='slam_example'
IMAGE=$(docker images | grep $TAG | awk -F' ' '{print $1}')
if [[ -z $IMAGE ]]; then
  echo "$TAG image is not exist. docker image build start."
  docker build --no-cache --tag $TAG --rm "./"
fi
CONTAINER_ID=$(docker container ls -a | grep $TAG | awk -F' ' '{print $1}')
if [[ -z "$CONTAINER_ID" ]]; then
  echo "$TAG docker container is not exist yet"
  docker run -it --rm -d \
            --net=host \
            --gpus all \
            -e DISPLAY=$DISPLAY \
            -e QT_X11_NO_MITSHM=1 \
            -v /tmp/.X11-unix:/tmp/.X11-unix \
            -w /root/catkin_ws \
            --security-opt apparmor=unconfined \
            --privileged \
            --name=$TAG \
            $TAG
else 
  STATE=$(docker container inspect $CONTAINER_ID | grep "Status" | tr -d "," | awk -F':' '{print $2}' | sed 's/\"//g')
  if [[ $STATE == *"exited"* ]]; then
    echo "$TAG is $STATE"
    docker start -a $TAG

  elif [[ $STATE == *"running"* ]]; then
    echo "$TAG is $STATE"
    docker exec -it $TAG bash
  fi
fi

xhost -


#   docker run -it -d \
#     --init \
#     --net=host \
#     --gpus all \
#     -e DISPLAY=$DISPLAY \
#     -e QT_GRAPHICSSYSTEM=native \
#     --env=LIBUSB_DEBUG=1 \
#     $VOLUME \
#     --group-add=plugdev \
#     --group-add=video \
#     --device=/dev/dri:/dev/dri \
#     --name=$TAG \
#     $TAG \
#     bash

#   WSDIR=`sudo find /home/$USER -name "CMakeLists.txt" | grep "/home/$USER/.*ws/src/CMakeLists.txt" | sed "s/CMakeLists.txt//g"`
#   WSDIR_ARRAY=($WSDIR)
#   #read -a WSDIR <<< $WSDIR
#   DIRLEN=${#WSDIR_ARRAY[@]}
#   echo "$DIRLEN"
#   for (( i=0; i<$DIRLEN; i++)); do
#     TARDIR=`echo ${WSDIR_ARRAY[$i]} | sed "s/\/home\/$USER//g"`
#     VOLUME="$VOLUME --volume=${WSDIR_ARRAY[$i]}:/home/ros$TARDIR:rw "
#   done
#   if [ ! -z "$CUDA_PATH" ] && [ ! -z "$USER_CUDA" ]; then
#     VOLUME="$VOLUME --volume=$CUDA_PATH:/usr/local/cuda-host-$USER_CUDA:rw"
#   fi
#   if [[! -z `echo $ROS_ROOT` ]]; then
#     VOLUME="$VOLUME --volume=$HOME/.ros:/home/ros/.ros:rw -v /opt/ros/kinetic"
#   fi
#   echo "$VOLUME"