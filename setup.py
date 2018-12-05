from setuptools import setup

setup(
    name='girderauthenticator',
    version='0.1-dev',
    description='Girder OAuth Authenticator for JupyterHub',
    url='https://github.com/Xarthisius/girderauthenticator',
    author='Xarthisius',
    author_email='xarthisius.kk@gmail.com',
    license='BSD-3',
    packages=['girderauthenticator'],
    install_requires=[
        'python-dateutil',
        'jupyterhub',
    ]
)
