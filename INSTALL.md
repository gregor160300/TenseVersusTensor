# Setup
This entire thesis was run on a single Intel Arc A770 (16GB) GPU. In order for this to work correctly however we need to use some specific versions of drivers and support packages. This document aims to help you reproduce the setup.

## Ubuntu
We start by installing Ubuntu 22.94, we went with the server version, but the desktop version should work fine.

After installation we need to update to the Linux 6.5 kernel.
```bash
sudo apt update
sudo apt full-upgrade
sudo apt-get install --install-recommends linux-generic-hwe-22.04
sudo reboot now
```

## GPU drivers
We will install the GPU drivers released by Intel. We start with some keys and setting up the repo.

```bash
sudo apt-get install -y gpg-agent wget
wget -qO - https://repositories.intel.com/gpu/intel-graphics.key | \
sudo gpg --dearmor --output /usr/share/keyrings/intel-graphics.gpg
echo "deb [arch=amd64,i386 signed-by=/usr/share/keyrings/intel-graphics.gpg] https://repositories.intel.com/gpu/ubuntu jammy client" | \
sudo tee /etc/apt/sources.list.d/intel-gpu-jammy.list
```

Now we do the actual driver installation.
```bash
sudo apt-get update
sudo apt-get -y install \
    gawk \
    dkms \
    linux-headers-$(uname -r) \
    libc6-dev

sudo apt-get install -y gawk libc6-dev udev\
    intel-opencl-icd intel-level-zero-gpu level-zero \
    intel-media-va-driver-non-free libmfx1 libmfxgen1 libvpl2 \
    libegl-mesa0 libegl1-mesa libegl1-mesa-dev libgbm1 libgl1-mesa-dev libgl1-mesa-dri \
    libglapi-mesa libgles2-mesa-dev libglx-mesa0 libigdgmm12 libxatracker2 mesa-va-drivers \
    mesa-vdpau-drivers mesa-vulkan-drivers va-driver-all vainfo

sudo reboot
```

After reboot we want to add ourselves to the render group
```bash
sudo gpasswd -a ${USER} render
newgrp render
```

## Intel oneAPI
We will install the 2024.0 version of the Intel oneAPI, it is not the latest version, but as of writing the latest version is not compatible with [IPEX-LLM](https://github.com/intel-analytics/ipex-llm).

```bash
wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor | sudo tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null

echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | sudo tee /etc/apt/sources.list.d/oneAPI.list

sudo apt update

sudo apt install intel-oneapi-common-vars=2024.0.0-49406 \
  intel-oneapi-compiler-cpp-eclipse-cfg=2024.0.2-49895 \
  intel-oneapi-compiler-dpcpp-eclipse-cfg=2024.0.2-49895 \
  intel-oneapi-diagnostics-utility=2024.0.0-49093 \
  intel-oneapi-compiler-dpcpp-cpp=2024.0.2-49895 \
  intel-oneapi-mkl=2024.0.0-49656 \
  intel-oneapi-mkl-devel=2024.0.0-49656 \
  intel-oneapi-mpi=2021.11.0-49493 \
  intel-oneapi-mpi-devel=2021.11.0-49493 \
  intel-oneapi-tbb=2021.11.0-49513  \
  intel-oneapi-tbb-devel=2021.11.0-49513 \
  intel-oneapi-ccl=2021.11.2-5  \
  intel-oneapi-ccl-devel=2021.11.2-5 \
  intel-oneapi-dnnl-devel=2024.0.0-49521 \
  intel-oneapi-dnnl=2024.0.0-49521 \
  intel-oneapi-tcm-1.0=1.0.0-435
```

## Python setup
Before we start setting up our Python environment we need to include the Intel oneAPI stuff in our path like so:
```bash
source /opt/intel/oneapi/setvars.sh
```

always source this before activating your virtual environment.

Now we will continue to install Python 3.9:
```bash
sudo apt install python3.9 python3.9-venv
```

Next create the virtual environment and activate it.
```bash
python3.9 -m venv ~/venv
source ~/venv/bin/activate
```

And finally we have to install the Python packages we used to run this project.
```bash
pip install -r requirement.txt
```

The above command might fail due to requiring an extra index url. If this is the case manuallt install the packages, starting with IPEX-LLM:

```
pip install --pre --upgrade ipex-llm[xpu] --extra-index-url https://pytorch-extension.intel.com/release-whl/stable/xpu/us/
```

[Source for this guide: IPEX-LLM Documentation](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Quickstart/install_linux_gpu.html#for-linux-kernel-6-5)
