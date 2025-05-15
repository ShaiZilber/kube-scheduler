# Schedule based on Node Selectors

## Introduction
Respect Pod authors’ node preferences: if a Pod specifies labels it wants on its node, only assign it to matching nodes.

## Requirements
* Only consider nodes bearing *all* requested labels.
* If none match, mark the Pod unschedulable (e.g., emit an event).
* Otherwise, choose one of the matching nodes to bind at random.