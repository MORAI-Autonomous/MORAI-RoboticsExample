#!/bin/bash
REPO='morai/example'
TAG='robotics'
IMAGE=$(docker images | grep $TAG | awk -F' ' '{print $1}')
if [[ -z $IMAGE ]]; then
  echo "$TAG image is not exist. docker image build start."
  docker build --no-cache --tag $TAG --rm "./"
  docker tag $TAG $REPO:$TAG
else
  echo "$TAG image is already exist. Try docker-run.sh"
fi