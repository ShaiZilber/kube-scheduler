# Schedule based on Quality of Service

## Introduction
In resource‑pressure scenarios, you may want to favor Pods with higher QoS (Guaranteed > Burstable > BestEffort). While QoS influences eviction, you can also bias scheduling order or tie‑breaks by a Pod’s class. ([Kubernetes][7])

### Further Reading
* https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/

## Requirements

* Before binding, sort pending Pods by QoS class (all Guaranteed first, then Burstable, then BestEffort).
* Optionally, when tie‑breaking nodes, prefer those where placing this Pod would result in a higher cluster‐wide QoS balance.
* Document how QoS affects scheduling fairness in your logs.