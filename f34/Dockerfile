FROM s2i-minimal-f34-py39-notebook:v0.0.1_custom

USER root

RUN yum -y update && \
    yum -y install xz iproute pam-devel ant lua lua-devel lua-posix lua-filesystem tcl python-keyring rdma-core-devel && \
    yum -y clean all && \
    rm -rf /var/cache/dnf

# Prepare build directory
RUN mkdir -p /build
WORKDIR /build

# Build LMOD
ENV LMOD_VER 8.5.9

RUN curl -LO http://github.com/TACC/Lmod/archive/${LMOD_VER}.tar.gz && \
    mv /build/${LMOD_VER}.tar.gz /build/Lmod-${LMOD_VER}.tar.gz && \
    tar xvf Lmod-${LMOD_VER}.tar.gz

WORKDIR /build/Lmod-${LMOD_VER}

RUN ./configure --prefix=/opt/apps --with-fastTCLInterp=no && \
    make install && \
    rm -rf /build && \
    ln -s /opt/apps/lmod/lmod/init/profile /etc/profile.d/z00_lmod.sh

# Copying custom packages
COPY ./packages/jupyterlab-lmod-0.8.2.tgz ./packages/jupyter_server_proxy-3.1.0-py3-none-any.whl ./packages/jupyterlmod-2.0.2-py3-none-any.whl requirements.txt /tmp/
COPY ./packages/jupyterlmodlauncher /tmp/jupyterlmodlauncher

# Install custom packages
RUN pip install --no-cache-dir -r /tmp/requirements.txt && \
    pip install --no-cache-dir /tmp/jupyter_server_proxy-3.1.0-py3-none-any.whl && \
    pip install --no-cache-dir /tmp/jupyterlmod-2.0.2-py3-none-any.whl && \
    pip install --no-cache-dir /tmp/jupyterlmodlauncher && \
    jupyter labextension install /tmp/jupyterlab-lmod-0.8.2.tgz && \
    jupyter lab build && \
    jupyter lab clean && \
    npm cache clean --force && \
    rm -rf $HOME/.cache/yarn && \
    rm -rf $HOME/.node-gyp && \
    fix-permissions /opt/app-root

ENV USER=rstudio-server \
    MODULESHOME=/opt/apps/lmod/lmod \
    MODULEPATH=/opt/apps/modulefiles/Linux:/opt/apps/modulefiles/Core:/opt/apps/lmod/lmod/modulefiles/Core \
    MODULEPATH_ROOT=/opt/apps/modulefiles \
    MANPATH=/opt/apps/lmod/lmod/share/man: \
    LMOD_DIR=/opt/apps/lmod/lmod/libexec \
    LMOD_SETTARG_FULL_SUPPORT=no \
    LMOD_PACKAGE_PATH=/opt/apps/easybuild/ \
    LMOD_VERSION=8.5.9 \
    LMOD_ROOT=/opt/apps/lmod \
    LMOD_sys=Linux \
    LMOD_CMD=/opt/apps/lmod/lmod/libexec/lmod

# Replace launch script to load module environment at start
COPY start-singleuser.sh /opt/app-root/bin/start-singleuser.sh

WORKDIR /opt/app-root/src
USER 1001

CMD /opt/app-root/bin/start-singleuser.sh --ip=0.0.0.0 --port=8080
