import setuptools

setuptools.setup(
    name="jupyterlmodlauncher",
    version='0.1',
    url="https://github.com/",
    author="Guillaume Moutier based on Project Jupyter Contributors",
    description="gmoutier@redhat.com",
    packages=['jupyterlmodlauncher'],
	keywords=['Jupyter'],
	classifiers=['Framework :: Jupyter'],
    install_requires=[
        'jupyter-server-proxy'
    ],
    entry_points={
        'jupyter_serverproxy_servers': [
            'code-server = jupyterlmodlauncher:setup_codeserver',
            'rstudio = jupyterlmodlauncher:setup_rstudio',
            'openrefine = jupyterlmodlauncher:setup_openrefine',
        ]
    },
    package_data={
        'jupyterlmodlauncher': ['icons/*'],
    },
)
