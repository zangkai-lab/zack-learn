# 记录GPU Server配置过程
## 0. 机器配置
- 注意卷大小50G

## 1. ssh登录
ssh ubuntu@54.146.133.170

## 2. 查看GPU信息
sudo apt-get update
### 安装完整驱动
sudo apt install -y nvidia-driver-535-server
- 内核驱动模块
- CUDA支持
- OpenGL支持
- 工具程序

### 安装工具
sudo apt install -y nvidia-utils-535-server
sudo reboot
nvidia-smi

### 安装CUDA


## 3. 安装miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

