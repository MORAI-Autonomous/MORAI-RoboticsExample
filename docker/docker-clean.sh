#!/bin/bash
REPO='morai/example'
TAG='robotics'
IMAGE=$(docker images | grep $TAG | awk -F' ' '{print $3}')
if [[ -z $IMAGE ]]; then
  echo "$TAG image is not exist."
  exit
else
  CONTAINER_ID=$(docker container ls -a | grep $REPO:$TAG | awk -F' ' '{print $1}')
  if [[ -z "$CONTAINER_ID" ]]; then
    echo "$TAG docker container is not exist yet. Cleaning start."
    docker rmi -f $IMAGE
    exit
  else
    STATE=$(docker container inspect $CONTAINER_ID | grep "Status" | tr -d "," | awk -F':' '{print $2}' | sed 's/\"//g')
    if [[ $STATE == *"exited"* ]]; then
      echo "$TAG is $STATE. Cleaning start."
      docker rmi -f $IMAGE
      exit
    elif [[ $STATE == *"running"* ]]; then
      echo "$TAG is $STATE. Cleaning start."
      docker stop $CONTAINER_ID
      sleep 2
      docker rmi -f $IMAGE
      exit
    fi
  fi
fi