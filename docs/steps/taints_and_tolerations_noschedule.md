# Schedule based on Node Taints and Pod Tolerations – NoSchedule

## Introduction
In this step, you’ll give your scheduler the ability to respect _hard_ taints on nodes. Some nodes may explicitly reject certain Pods unless the Pod includes a matching toleration. Your scheduler should ensure that Pods are only scheduled onto nodes they are allowed to run on, based on these taints and tolerations.

### Further Reading
* https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/

## Requirements

* Read each node’s taints that have the effect 'NoSchedule'.
* Reject all nodes with taints that the unscheduled Pod lacks a matching toleration for.
* Emit an event if a Pod can’t find any node due to taints.