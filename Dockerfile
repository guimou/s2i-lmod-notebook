FROM quay.io/thoth-station/s2i-minimal-py38-notebook:v0.1.1

USER root

# Install needed packages
RUN yum -y update && \
    yum -y install iproute nano lua \
    http://mirror.centos.org/centos/8-stream/BaseOS/x86_64/os/Packages/pam-1.3.1-15.el8.x86_64.rpm \
    http://mirror.centos.org/centos/8-stream/BaseOS/x86_64/os/Packages/pam-devel-1.3.1-15.el8.x86_64.rpm \
    http://mirror.centos.org/centos/8-stream/AppStream/x86_64/os/Packages/ant-lib-1.10.5-1.module_el8.0.0+47+197dca37.noarch.rpm \
    http://mirror.centos.org/centos/8-stream/AppStream/x86_64/os/Packages/ant-1.10.5-1.module_el8.0.0+47+197dca37.noarch.rpm \
    http://mirror.centos.org/centos/8-stream/PowerTools/x86_64/os/Packages/lua-devel-5.3.4-11.el8.x86_64.rpm \
    http://mirror.centos.org/centos/8-stream/PowerTools/x86_64/os/Packages/lua-posix-33.3.1-9.el8.x86_64.rpm \
    http://mirror.centos.org/centos/8-stream/PowerTools/x86_64/os/Packages/lua-filesystem-1.6.3-7.el8.x86_64.rpm && \
    yum -y clean all && \
    rm -rf /var/cache/yum

# Prepare build directory
RUN mkdir -p /build
WORKDIR /build

# Build LMOD
ENV LMOD_VER 8.4.20

RUN curl -LO http://github.com/TACC/Lmod/archive/${LMOD_VER}.tar.gz && \
    mv /build/${LMOD_VER}.tar.gz /build/Lmod-${LMOD_VER}.tar.gz && \
    tar xvf Lmod-${LMOD_VER}.tar.gz

WORKDIR /build/Lmod-${LMOD_VER}

RUN ./configure --prefix=/opt/apps --with-fastTCLInterp=no && \
    make install && \
    rm -rf /build && \
    ln -s /opt/apps/lmod/lmod/init/profile /etc/profile.d/z00_lmod.sh

ENV JUPYTER_ENABLE_LAB="true" \
    CRIO_RUNTIME="true" \
    ENABLE_PIPENV="1" \
    THOTH_ADVISE="0" \
    THOTH_DRY_RUN="0" \
    THOTH_PROVENANCE_CHECK="0" \
    USER=rstudio-server \
    LMOD_PACKAGE_PATH=/opt/apps/easybuild/

# Copying custom packages
COPY ./packages/jupyterlab-lmod-0.8.2.tgz ./packages/jupyter_server_proxy-3.1.0-py3-none-any.whl ./packages/jupyterlmod-2.0.2-py3-none-any.whl requirements.txt /tmp/
COPY ./packages/jupyterlmodlauncher /tmp/jupyterlmodlauncher

# Replace launch script to load module environment at start
COPY start-singleuser.sh /opt/app-root/bin/start-singleuser.sh

WORKDIR /opt/app-root/src
USER 1001

# Install custom packages
RUN pip install -r /tmp/requirements.txt && \
    pip install /tmp/jupyter_server_proxy-3.1.0-py3-none-any.whl && \
    pip install /tmp/jupyterlmod-2.0.2-py3-none-any.whl && \
    pip install /tmp/jupyterlmodlauncher && \
    jupyter labextension install /tmp/jupyterlab-lmod-0.8.2.tgz && \
    jupyter lab build

CMD source /opt/apps/lmod/lmod/init/profile && module use /opt/apps/easybuild/modules/all && /tmp/scripts/run
