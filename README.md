# MORAI - EXAMPLE DOCKER
### Clone example branch 
```bash
git clone -b example --single-branch https://github.com/MORAI-Autonomous/MORAI-EXAMPLE.git
```
\n
## Install [Docker](https://docs.docker.com/engine/install/ubuntu/) & [NVIDIA-Docker](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker)
```bash
sudo bash docker-install.sh
```
\n
## Run
#### On host:
```bash
sudo bash docker-run.sh
```

#### On docker image:
```bash
sudo ./runner.sh
```
\n
## Clean Docker image
```bash
sudo bash docker-clean.sh
```