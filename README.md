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
`MORAI-EXAMPLE` supports to setup conditions automatically, but `MORAI-SIM` needs to be installed and be running at least until the login screen.

<img src = "https://user-images.githubusercontent.com/93243768/163738426-3b31375a-838e-4a1c-b97d-fc6993d67262.png" width="60%" align="center">
#### On host:
```bash
sudo bash docker-run.sh
```

#### On docker image:
```bash
sudo ./runner.sh
```
Edit and close `config.yaml` to set the below parameters (only support parameters in `example`)
1. `mapping` -> set mapping type from (`2d` , `3d` , `none`)
2. `moving` -> set moving type from (`auto` , `cruise` , `keyboard`) 

## Clean Docker image
```bash
sudo bash docker-clean.sh
```
