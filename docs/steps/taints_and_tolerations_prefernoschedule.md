# Schedule based on Node Taints and Pod Tolerations – PreferNoSchedule

## Introduction
In this step, you’ll give your scheduler the ability to respect _soft_ taints on nodes. These taints indicate that a node prefers not to run certain Pods, but will still allow them if no better options are available. Your scheduler should try to avoid these nodes when possible, but still schedule Pods there if necessary.

### Further Reading
* https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/
## Requirements

* Separate the node into different tiers, based on how many `PreferNoSchedule` taints are untolerated by the Pod.
* When selecting nodes, select randomly from the highest non-empty tier.
  * Highest tier means fewest untolerated taints.
  * Lowest tier means most untolerated taints.