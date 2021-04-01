#!/bin/bash

set -x

set -eo pipefail

# Activate Easybuild modules, and activate Code-server and RStudio
source /opt/apps/lmod/lmod/init/profile
module use /opt/apps/easybuild/modules/all
export LMOD_PACKAGE_PATH=/opt/apps/easybuild/

# The 'start-singleuser.sh' script is invoked by JupyterHub installations.
# Execute the 'run' script instead so everything goes through common
# entrypoint. That it is being run under JupyterHub will be determined
# later from environment variables set by JupyterHub.

exec /opt/app-root/builder/run "$@"