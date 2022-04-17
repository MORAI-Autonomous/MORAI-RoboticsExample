#!/bin/bash
set -eu -o pipefail # fail on error and report it, debug all lines
dist=$(. /etc/os-release;echo $ID$VERSION_ID)

if [ ${dist//.} = ubuntu1804 ];then
	echo "Version : ${dist//.}. Installing start."
else
	echo "ERROR: Support only Ubuntu 18.04."
	exit 1
fi
echo "============================"
echo "Docker install"
echo "============================"
sudo apt-get remove -y docker docker-engine docker.io containerd runc docker-ce
sudo rm /var/lib/dpkg/info/libc-bin.*
sudo apt-get clean
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common \
    x11-xserver-utils
echo "next0"
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --batch --yes --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "next1"
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null    
echo "next2"
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

echo "============================"
echo "Nvidia Docker install"
echo "============================"

distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
   && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker