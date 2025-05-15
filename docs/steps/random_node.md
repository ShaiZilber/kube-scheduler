# Schedule on random node

## Introduction
Improve your scheduler so it can spread work across the cluster. Instead of always choosing the same node, it should assign each Pod to a randomly selected node. 

## Requirements
* Using the API, list all the nodes of the cluster.
* For every unscheduled Pod, pick one of those nodes at random.
* Bind the Pod on the picked node.
