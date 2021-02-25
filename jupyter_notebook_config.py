import os

port = int(os.environ.get('JUPYTER_NOTEBOOK_PORT', '8080'))

c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = port
c.NotebookApp.open_browser = False
c.NotebookApp.quit_button = False

if os.environ.get('JUPYTERHUB_SERVICE_PREFIX'):
    c.NotebookApp.base_url = os.environ.get('JUPYTERHUB_SERVICE_PREFIX')

password = os.environ.get('JUPYTER_NOTEBOOK_PASSWORD')
if password:
    import notebook.auth
    c.NotebookApp.password = notebook.auth.passwd(password)
    del password
    del os.environ['JUPYTER_NOTEBOOK_PASSWORD']

image_config_file = '/opt/app-root/src/.jupyter/jupyter_notebook_config.py'

if os.path.exists(image_config_file):
    with open(image_config_file) as fp:
        exec(compile(fp.read(), image_config_file, 'exec'), globals())


# server-proxy configuration
c.ServerProxy.servers = {
            "code-server": {
                "command": [
                    "code-server",
                    "--auth=none",
                    "--disable-telemetry",
                    "--host=127.0.0.1",
                    "--port={port}"
                ],
                "timeout": 30,
                "launcher_entry": {
                    "title": "VS Code",
                    "icon_path": "/opt/app-root/etc/Visual_Studio_Code_1.35_icon.svg",
                    "enabled": False
                },
            },
            "rstudio": {
                "command": [
                    "rserver",
                    "--www-port={port}",
                    "--www-frame-origin=same",
                    "--www-address=127.0.0.1",
                    "--server-data-dir=/opt/app-root/rstudio-server",
                    "--auth-none=1",
                    "--server-user=rstudio-server"
                ],
                "timeout": 30,
                "launcher_entry": {
                    "title": "RStudio",
                    "icon_path": "/opt/app-root/etc/RStudio_logo_flat.svg",
                    "enabled": False
                },
            }
        }
