"""
Return config on servers to start for codeserver

See https://jupyter-server-proxy.readthedocs.io/en/latest/server-process.html
for more information.
"""
import os
import shutil

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

def setup_rstudio():
    def _rstudio_command(port):
        working_dir = os.getenv("RSTUDIO_WORKINGDIR", None)
        if working_dir is None:
            working_dir = os.getenv("JUPYTER_SERVER_ROOT", ".")

        return ['rserver',
            f'--www-port={port}',
            "--auth-none=1",
            "--www-frame-origin=same",
            "--www-address=127.0.0.1",
            "--server-data-dir=/var/run/rstudio-server",
            "--server-daemonize=0",
            "--server-user=rstudio-server",
            f"--server-working-dir={working_dir}"
        ]

    return {
        'command': _rstudio_command,
        'timeout': 30,
        'launcher_entry': {
            'title': 'RStudio',
            'icon_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons', 'rstudio.svg'),
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
