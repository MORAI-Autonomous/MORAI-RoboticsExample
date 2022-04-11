# MORAI - EXAMPLE DOCKER

## Install [Docker](https://docs.docker.com/engine/install/ubuntu/)
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

## Install [NVIDIA-Docker](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker)
### Setting up Docker
```bash
curl https://get.docker.com | sh \
  && sudo systemctl --now enable docker
```
### Setting up NVIDIA Container Toolkit
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
      && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
            sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
            sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```
### Install the nvida-docker2 packages
```bash
sudo apt-get update
```
```bash
sudo apt-get install -y nvidia-docker2
```
### Restart the Docker daemon to complete the installation after setting the default runtime
```bash
sudo systemctl restart docker
```

## Ready for GUI visualization
```bash
sudo apt-get install x11-xserver-utils
```

## Run
```bash
git clone -b example --single-branch https://github.com/MORAI-Autonomous/MORAI-EXAMPLE.git
cd MORAI-EXAMPLE
```
```bash
sudo ./docker.sh
```

### On docker image:
```bash
source devel/setup.bash
./runner.sh
```
