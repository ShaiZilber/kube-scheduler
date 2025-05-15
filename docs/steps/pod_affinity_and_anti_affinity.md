# Schedule based on Pod Affinity/Anti‑Affinity

## Introduction
In this step, you’ll give your scheduler the ability to respect inter-Pod placement rules. These rules let a Pod request to be scheduled near (or away from) other Pods based on labels and topology.

Required rules must be enforced strictly—Pods should only be scheduled onto nodes that meet them. Preferred rules influence node selection but can be relaxed if necessary.

### Further Reading
* https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#types-of-inter-pod-affinity-and-anti-affinity

## Requirements

* Pod Affinity:
  * For each requiredDuringSchedulingIgnoredDuringExecution rule:
    * Group nodes based on the rule's topology key.
    * Reject all nodes without the rule's topology key.
    * Reject all nodes in the node group where no Pod matching the rule’s label selector exists.
  * For each preferredDuringSchedulingIgnoredDuringExecution rule:
    * Group nodes based on the rule's topology key.
    * Skip all nodes without the rule's topology key.
    * For each node group, count the number of occurrences of a Pod matching the rule’s label selector and multiply by the rule's weight for scoring.
    * Add the result from the node's score.
* Pod Anti Affinity:
  * For each requiredDuringSchedulingIgnoredDuringExecution rule:
    * Group nodes based on the rule's topology key.
    * Reject all nodes without the rule's topology key.
    * Reject all nodes in the node group where at least one Pod matching the rule’s label selector exists.
  * For each preferredDuringSchedulingIgnoredDuringExecution rule:
    * Group nodes based on the rule's topology key.
    * Skip all nodes without the rule's topology key.
    * For each node group, count the number of occurrences of a Pod matching the rule’s label selector and multiply by the rule's weight for scoring.
    * Subtract the result from the node's score.
* Pick the node with the highest score.