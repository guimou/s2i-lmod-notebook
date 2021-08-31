"""
Return config on servers to start for codeserver

See https://jupyter-server-proxy.readthedocs.io/en/latest/server-process.html
for more information.
"""
import getpass
import os
import pathlib
import shutil
import subprocess
import tempfile
from textwrap import dedent

def setup_codeserver():
    def _codeserver_command(port):
        working_dir = os.getenv("CODE_WORKINGDIR", None)
        if working_dir is None:
            working_dir = os.getenv("JUPYTER_SERVER_ROOT", ".")

        return ['code-server',
            f'--port={port}',
            "--auth=none",
            "--disable-telemetry",
            "--host=127.0.0.1",
            working_dir ]

    return {
        'command': _codeserver_command,
        'timeout': 30,
        'launcher_entry': {
            'title': 'VS Code',
            'icon_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons', 'vscode.svg'),
            'enabled': False
        }
    }

def setup_openrefine():
    def _openrefine_command(port):
        working_dir = os.getenv("OPENREFINE_WORKINGDIR", None)
        if working_dir is None:
            working_dir = os.getenv("JUPYTER_SERVER_ROOT", ".")

        return ['refine', '-p', f'{port}','-d', f'{working_dir}']

    return {
        'command': _openrefine_command,
        'timeout': 30,
        'launcher_entry': {
            'title': 'OpenRefine',
            'icon_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons', 'openrefine.svg'),
            'enabled': False
        }
    }

def get_rstudio_executable(prog):
    # Find prog in known locations
    other_paths = [
        # When rstudio-server deb is installed
        os.path.join('/usr/lib/rstudio-server/bin', prog),
        # When just rstudio deb is installed
        os.path.join('/usr/lib/rstudio/bin', prog),
    ]
    if shutil.which(prog):
        return prog

    for op in other_paths:
        if os.path.exists(op):
            return op

    raise FileNotFoundError(f'Could not find {prog} in PATH')

def get_icon_path():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'icons', 'rstudio.svg'
    )

def setup_rstudio():
    def _get_env(port):
        return dict(USER=getpass.getuser())

    def db_config():
        '''
        Create a temporary directory to hold rserver's database, and create
        the configuration file rserver uses to find the database.
        https://docs.rstudio.com/ide/server-pro/latest/database.html
        https://github.com/rstudio/rstudio/tree/v1.4.1103/src/cpp/server/db
        '''
        # use mkdtemp() so the directory and its contents don't vanish when
        # we're out of scope
        db_dir = tempfile.mkdtemp()
        # create the rserver database config
        db_conf = dedent("""
            provider=sqlite
            directory={directory}
        """).format(directory=db_dir)
        f = tempfile.NamedTemporaryFile(mode='w', delete=False, dir=db_dir)
        db_config_name = f.name
        f.write(db_conf)
        f.close()
        return db_config_name

    def _get_cmd(port):
        working_dir = os.getenv("RSTUDIO_WORKINGDIR", None)
        if working_dir is None:
            working_dir = os.getenv("JUPYTER_SERVER_ROOT", ".")
        
        cmd = [
            get_rstudio_executable('rserver'),
            '--auth-none=1',
            '--www-frame-origin=same',
            '--www-port=' + str(port),
            '--www-verify-user-agent=0',
            "--www-address=127.0.0.1",
            "--server-data-dir=/opt/app-root/rstudio-server",
            "--server-daemonize=0",
            "--server-user=rstudio-server",
            f"--server-working-dir={working_dir}"
        ]

        # Add additional options for RStudio >= 1.4.x. Since we cannot
        # determine rserver's version from the executable, we must use
        # explicit configuration. In this case the environment variable
        # RSESSION_PROXY_RSTUDIO_1_4 must be set.
        if os.environ.get('RSESSION_PROXY_RSTUDIO_1_4', False):
            # base_url has a trailing slash
            cmd.append('--www-root-path={base_url}rstudio/')
            cmd.append(f'--database-config-file={db_config()}')

        return cmd

    server_process = {
        'command': _get_cmd,
        'timeout': 30,
        'environment': _get_env,
        'launcher_entry': {
            'title': 'RStudio',
            'icon_path': get_icon_path(),
            'enabled': False,

        }
    }
    if os.environ.get('RSESSION_PROXY_RSTUDIO_1_4', False):
        server_process['launcher_entry']['path_info'] = 'rstudio/auth-sign-in?appUrl=%2F'
    return server_process
