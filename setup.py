from distutils.core import setup
from setuptools import find_packages
from asgardeo_auth import __name__, __version__, __packages__, __license_name__, \
    __description__, __author__, __author_email__, __homepage__, \
    __download_url__, __keywords__, __bug_tracker__

with open('README.md') as f:
    long_description = f.read()


setup(
    name=__name__,
    packages=find_packages(include=__packages__),
    version=__version__,
    license=__license_name__,
    description=__description__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=__author__,
    author_email=__author_email__,
    url=__homepage__,
    download_url=__download_url__,
    keywords=__keywords__,
    install_requires=[
        'six',
        'requests',
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
        'License :: OSI Approved :: ' + __license_name__,
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
        'Documentation': __homepage__,
        'Bug Tracker': __bug_tracker__,
        'Source Code': __homepage__,
    }
)
