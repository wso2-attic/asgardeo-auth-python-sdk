# Asgardeo-auth-python-sdk

![Builder](https://github.com/asgardeo/asgardeo-auth-python-sdk/workflows/Builder/badge.svg)
[![Downloads](https://pepy.tech/badge/asgardeo-auth-python-sdk)](https://pepy.tech/project/asgardeo-auth-python-sdk)
[![Stackoverflow](https://img.shields.io/badge/Ask%20for%20help%20on-Stackoverflow-orange)](https://stackoverflow.com/questions/tagged/wso2is)
[![Join the chat at https://join.slack.com/t/wso2is/shared_invite/enQtNzk0MTI1OTg5NjM1LTllODZiMTYzMmY0YzljYjdhZGExZWVkZDUxOWVjZDJkZGIzNTE1NDllYWFhM2MyOGFjMDlkYzJjODJhOWQ4YjE](https://img.shields.io/badge/Join%20us%20on-Slack-%23e01563.svg)](https://join.slack.com/t/wso2is/shared_invite/enQtNzk0MTI1OTg5NjM1LTllODZiMTYzMmY0YzljYjdhZGExZWVkZDUxOWVjZDJkZGIzNTE1NDllYWFhM2MyOGFjMDlkYzJjODJhOWQ4YjE)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/wso2/product-is/blob/master/LICENSE)


Asgardeo Auth Python SDK provides the core methods that are needed to implement OIDC authentication in Python based apps. This SDK can be used to build SDKs for Web Applications from different frameworks such as Flask, Django and various other frameworks that use Python.

## Table of Content

-   [Introduction](#introduction)
-   [Install](#install)
-   [Getting Started](#getting-started)
-   [Develop](#develop)
-   [Contribute](#contribute)
-   [License](#license)

## Introduction
Python Authentication SDK for WSO2 Identity server (aka Product IS) brings up the fast and secure way to add user login to a Python web applications with the help of the WSO2 Identity Server(WSO2 IS).

## Install

Install the library from PyPI.

```
pip install asgardeo-auth-python-sdk
```

## Getting Started

Python Authentication SDK is architectured in a way that any python framework could be integrated with the Core SDK. Currently the SDK itself supports Flask framework. 
you can find the documentation [here](samples/flask/Readme.md).

Still you can implement your own way of implementation using the APIs provided by the core.

## Develop

### Prerequisites

-   `Node.js` (version 10 or above).
-   `npm` package manager.

### Installing Dependencies

The repository is a mono repository. The SDK repository is found in the [asgardeo_auth](https://github.com/asgardeo/asgardeo-auth-python-sdk/tree/main/asgardeo_auth) directory. You can install the dependencies by running the following command at the root.

```
pip3 install -r requirements.txt
```
## Contribute

Please read [Contributing to the Code Base](http://wso2.github.io/) for details on our code of conduct, and the process for submitting pull requests to us.

### Reporting issues

We encourage you to report issues, improvements, and feature requests creating [Github Issues](https://github.com/asgardeo/asgardeo-auth-python-sdk/issues).

Important: And please be advised that security issues must be reported to security@wso2com, not as GitHub issues, in order to reach the proper audience. We strongly advise following the WSO2 Security Vulnerability Reporting Guidelines when reporting the security issues.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.



