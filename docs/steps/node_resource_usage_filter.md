# Schedule based on Node Resource Usage

## Introduction
Make your scheduler resource‑aware: only place pods on nodes where there is enough resources to accommodate it  

## Requirements
* For each node, calculate free CPU and memory after accounting for currently scheduled Pods requests.
* filter out nodes lacking sufficient resources for the new Pod’s requests.
* From the remaining nodes, pick the one with the highest score.
* Bind the Pod there.

