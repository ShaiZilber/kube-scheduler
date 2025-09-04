
# Initial Scheduler

## Introduction
In this exercise the attendees will combine the two halves of the scheduler they previously implemented.
Together, these components form a complete basic scheduler. 

## Working Environment
* Everything from the previous step.

## Requirements
* MUST get the list of all pods in all namespaces programmatically.
* MUST get each pod's namespace programmatically.
* MUST get the list of all nodes programmatically.
* MUST filter pods by their `spec.schedulerName` field.
* MUST filter pods that are already scheduled, using the `spec.nodeName` field.
* MUST use the supplied schedule_pod function.
* MUST use a service account and its API token.
* MUST use random node, without any considerations.
* MUST be continuous.
* SHOULD use the watch object to stream the pods, instead of manually infinitely looping with timeout. 
* If not using watch, MUST wait between loop iterations. 




## FAQ
### What do you mean `continuous`?
The scheduler does not run `once` but continually searches for unscheduled pods and schedules them.