# [DEPRECATED] Asgardeo-auth-python-sdk

## :warning: Warning!
### Python SDK is no longer encouraged and enriched by Asgardeo and may not work with the latest Python versions.
### You can implement login using [Authorization Code flow](https://wso2.com/asgardeo/docs/guides/authentication/oidc/implement-auth-code/#prerequisites) with Asgardeo using OIDC standards.
---

![Builder](https://github.com/asgardeo/asgardeo-auth-python-sdk/workflows/Builder/badge.svg)
[![Downloads](https://pepy.tech/badge/asgardeo-auth-python-sdk)](https://pepy.tech/project/asgardeo-auth-python-sdk)
[![Stackoverflow](https://img.shields.io/badge/Ask%20for%20help%20on-Stackoverflow-orange)](https://stackoverflow.com/questions/tagged/asgardeo)
[![Discord](https://img.shields.io/badge/Join%20us%20on-Discord-%23e01563.svg)](https://discord.gg/wso2)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/asgardeo/asgardeo-auth-python-sdk/blob/main/LICENSE)


## Table of Content

- [Introduction](#introduction)
- [Prerequisite](#prerequisite)
- [Try Out the Sample Apps](#try-out-the-sample-apps)
- [Getting Started](#getting-started)
- [Develop](#develop)
- [Contribute](#contribute)
- [License](#license)

## Introduction

Asgardeo Auth Python SDK provides the core methods that are needed to implement OIDC authentication in Python based apps. This SDK can be used to build SDKs for Web Applications from different frameworks such as Flask, Django and various other frameworks that use Python. By using Asgardeo and the Asgardeo Auth Python SDK, developers will be able to add identity management to their Python based applications fast and secure.

To enable authentication for the sample application, we are using Asgardeo as the Identity Provider.

## Prerequisite

Create an organization in Asgardeo if you don't already have one. The organization name you choose will be referred to as `<tenant>` throughout this document.

## Try Out the Sample Apps

### 1. Create an Application in Asgardeo

Before trying out the sample apps, you need to create an application in **Asgardeo**.

1. Navigate to [**Asgardeo Console**](https://console.asgardeo.io/login) and click on **Applications** under **Develop** tab.

2. Click on **New Application** and then **Traditional Web Application**.

3. Enter **Sample** as the name of the app and add the redirect URL(s). You can find the relevant redirect URL(s) of each sample app in the [Running the sample apps](#2-running-the-sample-apps) section.

4. Click on Register. You will be navigated to management page of the **Sample** application.
   
5. Add `https://localhost:3000` (or whichever the URL your app is hosted on) to **Allowed Origins** under **Protocol** tab.
   
6. Click on **Update** at the bottom.


### 2. Running the sample apps

1. Fork and clone [python-sdk repo](https://github.com/asgardeo/asgardeo-auth-python-sdk)

2. Update configuration file `conf.py` with your registered app details.

  ```python
    auth_config = {
        "login_callback_url": "https://localhost:3000/login",
        "logout_callback_url": "https://localhost:3000/signin",
        "client_host": "https://localhost:3000",
        "client_id": "<client_id>",
        "client_secret": "<client_secret>",
        "server_origin": "https://api.asgardeo.io",
        "tenant_path": "/t/<tenant>",
        "tenant": "<tenant>",
        "certificate_path": "cert/wso2.crt"
    }
```

3. Obtain an [SSL certificate](https://www.globalsign.com/en/blog/how-to-view-ssl-certificate-details) for [https://console.asgardeo.io/](https://console.asgardeo.io/) and replace the content of wso2.crt with the obtained one. 

4. Run `pip3 install -r requirements.txt`

5. Run the application.

6. Navigate to `https://localhost:3000` (or whichever the URL you have hosted the sample app) from the browser.

#### Basic Flask Sample

- Download the Sample: [samples/flask](https://github.com/asgardeo/asgardeo-auth-python-sdk/tree/main/samples/flask)

- Find More Info: [README](/samples/flask/Readme.md)

- **Redirect URL(s):**
  - `https://localhost:3000/login`
  - `https://localhost:3000/signin`
  


## Getting Started

### 1. Install the library from PyPI.

```
pip install asgardeo-auth-python-sdk
```

### 2. Set up the application using the provided APIs
Python Authentication SDK is architectured in a way that any python framework could be integrated with the Core SDK
. Currently the SDK itself supports Flask framework. 
you can find the documentation [here](https://github.com/asgardeo/asgardeo-auth-python-sdk/tree/main/samples/flask/Readme.md).

Still you can implement your own way of implementation using the APIs provided by the core.

## Develop

### Prerequisites

-   `Python`
-   `pip` package manager.

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

This project is licensed under the Apache License 2.0. See the [LICENSE](https://github.com/asgardeo/asgardeo-auth-python-sdk/blob/main/LICENSE) file for details.



