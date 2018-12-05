# JupyterHub Girder OAuth Authenticato

A JupyterHub authenticator for Girder OAuth plugin

## Installation

To install clone this repository and run:

```
cd girderauthenticator
pip install -e .
```

## Configuration

You should edit your :file:`jupyterhub_config.py` to set the authenticator class:

```
c.JupyterHub.authenticator_class = 'girderauthenticator.auth.GirderOAuthAuthenticator'
```

### Required configuration

You'll also need to set some configuration options including the FQDN of your JupyterHub, Girder API, Girder OAuth provider.

```
c.GirderOAuthAuthenticator.jupyterhub_url = 'https://jupyterhub.local.wholetale.org'
c.GirderOAuthAuthenticator.api_url = 'https://girder.local.wholetale.org/api/v1'
c.GirderOAuthAuthenticator.girder_provider = 'Globus'
```
