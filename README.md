# MORAI - EXAMPLE DOCKER
### Clone example branch 
```bash
git clone -b example --single-branch https://github.com/MORAI-Autonomous/MORAI-EXAMPLE.git
cd MORAI-EXAMPLE
```

## Install [Docker](https://docs.docker.com/engine/install/ubuntu/) & [NVIDIA-Docker](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker)
```bash
sudo bash docker-install.sh
```

## Run
#### On host:
```bash
sudo bash docker-run.sh
```

#### On docker image:
```bash
sudo ./runner.sh
```

## Clean Docker image
```bash
sudo bash docker-clean.sh
```
