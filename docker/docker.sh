#!/bin/bash
xhost +
REPO='morai/example-ad_slam'
TAG='v1.0.0'
IMAGE=$(docker images | grep $TAG | awk -F' ' '{print $1}')
if [[ -z $IMAGE ]]; then
  echo "$TAG image is not e
  xist. docker image build start."
  docker build --no-cache --tag $REPO:$TAG --rm "./"
fi
CONTAINER_ID=$(docker container ls -a | grep $IMAGE | awk -F' ' '{print $1}')
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
            $REPO:$TAG
else 
  STATE=$(docker container inspect $CONTAINER_ID | grep "Status" | tr -d "," | awk -F':' '{print $2}' | sed 's/\"//g')
  if [[ $STATE == *"exited"* ]]; then
    echo "$TAG is $STATE"
    docker start -a $CONTAINER_ID

  elif [[ $STATE == *"running"* ]]; then
    echo "$TAG is $STATE"
    docker exec -it $CONTAINER_ID bash
  fi
fi

xhost -