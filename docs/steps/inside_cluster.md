# Run inside cluster

## Introduction
Rather than running your scheduler as a standalone process with external kubeconfig, package it into a container and deploy it as a Pod inside the very cluster it schedules. It should use in‑cluster authentication.

## Requirements

* Build a container image using the provided [Containerfile](../../solution/Containerfile).
* Create the required manifests to run the pod inside the cluster.
* Confirm the scheduler schedule pods.