# Kubernetes Scheduler Exercise

## Introduction

## Steps
### Basic Steps - Required
0. [Learn the API](./docs/steps/learn_the_api.md)
1. Initial scheduling:
   a. [Schedule a hard coded pod on a programmatically found node.](./docs/steps/programmatic_pod.md)
   b. [Schedule a programmatically found pod on a hard coded node.](./docs/steps/programmatic_node.md)
2. [Run inside cluster.](./docs/steps/inside_cluster.md)

### Advanced Steps - Optional
#### Synchronous
1. [Implement `schedule_pod` function.](./docs/steps/implement_schedule_pod.md)

#### Asynchronous
2. [Schedule based on Node Selectors.](./docs/steps/node_selectors.md)
3. [Schedule based on Node Taints and Pod Tolerations - NoSchedule.](./docs/steps/taints_and_tolerations_noschedule.md)
4. [Schedule based on Node Affinity Required.](./docs/steps/node_affinity_required.md)
5. [Schedule based on Node Taints and Pod Tolerations - PreferNoSchedule.](./docs/steps/taints_and_tolerations_prefernoschedule.md)
6. [Schedule based on Node Affinity Preferred.](./docs/steps/node_affinity_preferred.md)
7. [Schedule based on Pod Affinity/Anti Affinity.](./docs/steps/pod_affinity_and_anti_affinity.md)
8. [Schedule based on resource fit.](./docs/steps/node_resource_usage_filter.md)
9. [Schedule based on resource scoring.](./docs/steps/node_resource_usage_scorer.md)
10. [Schedule based on Quality of Service.](./docs/steps/quality_of_service.md)
11. [Schedule based on Pod Topology Spread Constraints.](./docs/steps/pod_topology_spread_constraints.md)
