# Semi-Programmatic Scheduling

## Introduction
In this exercise the attendees will learn the two halves of scheduling:
* Scheduling all unscheduled pods (retrieved programmatically) to a hard-coded node.
* Scheduling a hard coded pod to a random node (retrieved programmatically).

Together, these components form a complete basic scheduler. Presented separately, they create a gentler learning curve, making it easier for attendees to grasp the concept of scheduling.

## Working Environment
* Everything from the previous step.
* [main.py](../../exercise/main.py).
* [schedule_pod.pyi](../../exercise/schedule_pod.pyi) - Gives the signature of `schedule_pod` function.
* schedule_pod.pyc - this is the obfuscated implementation of the `schedule_pod` function.  
  can be compiled using the following commands:
  ```bash
  python3.11 -m compileall ./solution/src/schedule_pod.py
  mv ./__pycache__/schedule_pod.cpython-311.pyc ./schedule_pod.pyc 
  ```

## Requirements

### Programmatic Pod
* MUST get the list of all pods in all namespaces programmatically.
* MUST get each pod's namespace programmatically.
* MUST filter pods by their `spec.schedulerName` field.
* MUST filter pods that are already scheduled, using the `spec.nodeName` field.
* MUST use a hard-coded node name.
* MUST use the supplied schedule_pod function.
* MUST use a service account and its API token.
* SHOULD NOT be continuous.

### Programmatic Node
* MUST get the list of all nodes programmatically.
* MUST use random node, without any considerations.
* MUST use a hard-coded pod name and namespace.
* MUST use the supplied schedule_pod function.
* MUST use a service account and its API token.
* SHOULD NOT be continuous.


## FAQ
### What does the field `schedulerName` do?
The field is an indicator for a scheduler to add the pod to its scheduling queue. 
It is up to the scheduler to look for the scheduler name properly and only schedule pods that use his "name".
The scheduler name is an agreement between the pod creator and the scheduler creator on what the identifier for the scheduler is.

### How can i filter out scheduled pods?
You should look at the `spec.nodeName` field. Only scheduled pods have a non-empty value for this field.
other ways such as looking at the status of the pod or keeping track of already scheduled pods have noticeable drawbacks and are not acceptable.
