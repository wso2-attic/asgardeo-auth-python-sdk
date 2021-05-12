from distutils.core import setup
from setuptools import find_packages
from lib.app_consts import name, version, homepage, license_name, bug_tracker, \
    keywords, description, download_url, author, author_email,packages

with open('README.md') as f:
    long_description = f.read()

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
        'python-jose>=3.2.0',
        'Flask>=1.1.2'
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
