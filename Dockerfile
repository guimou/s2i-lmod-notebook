FROM quay.io/guimou/s2i-minimal-notebook-f32:0.0.1

USER root

# Install packages

RUN dnf -y install xz iproute pam-devel ant lua lua-devel lua-posix lua-filesystem tcl python-keyring && \
    rpm -ivh https://kojipkgs.fedoraproject.org/packages/http-parser/2.9.4/4.eln109/x86_64/http-parser-2.9.4-4.eln109.x86_64.rpm && \
    dnf -y update && \
    dnf clean all

# Install LMod
RUN mkdir -p /build
WORKDIR /build

# Build LMOD
ENV LMOD_VER 8.4.20

RUN curl -LO http://github.com/TACC/Lmod/archive/${LMOD_VER}.tar.gz && \
    mv /build/${LMOD_VER}.tar.gz /build/Lmod-${LMOD_VER}.tar.gz && \
    tar xvf Lmod-${LMOD_VER}.tar.gz

WORKDIR /build/Lmod-${LMOD_VER}

RUN ./configure --prefix=/opt/apps --with-fastTCLInterp=no && \
    make install

# Cleanup
RUN rm -rf /build

ENV JUPYTER_ENABLE_LAB="true" \
    CRIO_RUNTIME="true" \
    ENABLE_PIPENV="1" \
    THOTH_ADVISE="0" \
    THOTH_DRY_RUN="0" \
    THOTH_PROVENANCE_CHECK="0"

# Copying in override assemble/run scripts
COPY upload/scripts /tmp/scripts
# Copying in source code
COPY upload/src /tmp/src
# Change file ownership to the assemble user. Builder image must support chown command.
WORKDIR /opt/app-root/src
RUN chown -R 1001:0 /tmp/scripts /tmp/src
USER 1001
RUN /tmp/scripts/assemble
CMD /tmp/scripts/run
