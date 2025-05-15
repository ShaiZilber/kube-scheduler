# Schedule based on Required Node Affinity

## Introduction
Support node affinity as a requirement: Pods can define complex label‑based requirements that nodes must satisfy.

## Requirements

* Only consider nodes fulfilling *all* the terms of matching matchExpressions field (ignore matchFields).
* Reject all nodes where no affinity was specified.
* If no nodes qualify, mark the Pod unschedulable (e.g., emit an event). 
* Otherwise, choose one of the matching nodes at random to bind.