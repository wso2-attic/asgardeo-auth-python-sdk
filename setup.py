from distutils.core import setup
from setuptools import find_packages

with open('README.md') as f:
    long_description = f.read()


name = 'asgardeo-auth-python-sdk'
packages = ('asgardeo_auth', 'asgardeo_auth.*')
version = "0.1.11-dev0"
author = 'Asgardeo'
homepage = 'https://github.com/asgardeo/asgardeo-auth-python-sdk#readme'
license_name = 'Apache Software License'
description = "Asgardeo Auth Python SDK."
bug_tracker = 'https://github.com/asgardeo/asgardeo-auth-python-sdk/issues'
keywords = [
    "Asgardeo",
    "OIDC",
    "OAuth2",
    "Authentication",
    "Authorization"
]
download_url = 'https://github.com/asgardeo/asgardeo-auth-python-sdk/releases'
author = "Asgardeo",
author_email = "beta@asgardeo.io"
default_user_agent = '{}/{} (+{})'.format(name, version, homepage)
default_json_headers = [
    ('Content-Type', 'application/json'),
    ('Cache-Control', 'no-store'),
    ('Pragma', 'no-cache'),
]

setup(
    name=name,
    packages=find_packages(include=packages),
    version=version,
    license=license_name,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=author,
    author_email=author_email,
    url=homepage,
    download_url=download_url,
    keywords=keywords,
    install_requires=[
        'six',
        'requests',
        'python-jose>=3.2.0',
        'Flask>=1.1.2',
        'pyOpenSSL>=20.0.1'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        # as the current state of your package
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: ' + license_name,
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    project_urls={
        'Documentation': homepage,
        'Bug Tracker': bug_tracker,
        'Source Code': homepage,
    }
)
