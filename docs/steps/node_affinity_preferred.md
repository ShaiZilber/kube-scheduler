# Schedule based on Preferred Node Affinity

## Introduction
Implement weighted preferences: Pods can list desirable node characteristics with weights, and the scheduler pick the node with the highest total “preference” score.

## Requirements

* For each node, calculate a score by summing weights of all matched preferences.
* pick the highest scoring node from the highest non-empty tier. 
  * if multiple nodes score the same, pick one at random.