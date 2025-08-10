# Learn the API

## Introduction
In this exercise the attendees will learn to interact with the api server. 

they are meant to learn about:
* service account + api token
* role + role bindings
* kubernetes python client

## Working Environment
* Use python3.11.

## Requirements

* MUST implement a program that prints a list of all pods in the cluster.
* MUST use service accounts and api token
* MUST NOT use `kubeconfig` files.
* MUST NOT run inside the cluster.
* SHOULD give minimal permissions for the service account.
* SHOULD create a service-account-token type secret to generate the API token.


## FAQ

### Why should I use a service account and not my local user?

* minimal permission:
  * you want to ensure that the code has exactly the permissions it requires.  
* separate the user from the project
  * Removing/Adding permissions from/to the user should not affect the outcome of the code.
  * The project can run longer than the user stays in the organization. this can cause the user to deactivate and the project to fail. 
  * Different users running the same code should have the same outcome no matter their role in the organization.

### Why shouldn't I use the kubeconfig file, even with the service account API token?

You can use the kubeconfig file generally. As part of this workshop we want attendees to understand what loading a kubeconfig file does, so we ask them to implement it manually.

### Can i use load_incluster_config?

No, you are not running "incluster"