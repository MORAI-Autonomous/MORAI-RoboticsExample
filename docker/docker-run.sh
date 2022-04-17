#!/bin/bash
xhost +
REPO='morai/example'
TAG='robotics'
if ! docker --version; then
	echo "ERROR: Did Docker get installed?"
  xhost -
	exit 1
fi
IMAGE=$(docker images | grep $TAG | awk -F' ' '{print $3}')
if [[ -z $IMAGE ]]; then
  echo "$TAG image is not exist. docker image build start."
  docker pull $REPO:$TAG
fi
CONTAINER_ID=$(docker container ls -a | grep $REPO:$TAG | awk -F' ' '{print $1}')
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
            $REPO:$TAG bash
  CONTAINER_ID=$(docker container ls -a | grep $REPO:$TAG | awk -F' ' '{print $1}')
fi
STATE=$(docker container inspect $CONTAINER_ID | grep "Status" | tr -d "," | awk -F':' '{print $2}' | sed 's/\"//g')
if [[ $STATE == *"exited"* ]]; then
  echo "$TAG is $STATE"
  docker start -a $CONTAINER_ID

elif [[ $STATE == *"running"* ]]; then
  echo "$TAG is $STATE"
  docker exec -it $CONTAINER_ID bash
fi

xhost -