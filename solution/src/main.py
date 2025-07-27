import os
from random import choice
from typing import Optional

import kubernetes

from schedule_pod import schedule_pod
from solution.src.taints_and_tolerations import tolerates
from solution.src.node_selecor import node_selector_filter


def load_config():
    configuration = kubernetes.client.Configuration()
    kubeconfig = os.getenv("KUBECONFIG")
    if kubeconfig is not None and os.path.isfile(kubeconfig):
        kubernetes.config.load_kube_config(client_configuration=configuration)
    else:
        kubernetes.config.load_incluster_config(client_configuration=configuration)
    return configuration


def select_node(v1: kubernetes.client.CoreV1Api, pod: kubernetes.client.V1Pod) -> Optional[kubernetes.client.V1Node]:
    tiered_nodes = [[], []]
    for node in v1.list_node().items:
        # Advanced Step 1
        if not (node_selector_filter(node, pod)):
            continue

        # Advanced Step 3
        if not (tolerates(node, pod, "NoSchedule")):
            continue

        # Advanced Step 5
        if tolerates(node, pod, "PreferNoSchedule"):
            tiered_nodes[0].append(node)
        else:
            tiered_nodes[1].append(node)

    for tier in tiered_nodes:
        if len(tier) == 0:
            continue

        return choice(tier)

    return None


def main():
    configuration = load_config()

    v1 = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
    w = kubernetes.watch.Watch()

    print("Watching pods in all namespaces...", flush=True)
    for event in w.stream(
            v1.list_pod_for_all_namespaces, field_selector="spec.schedulerName==custom"
    ):
        pod = event["object"]
        if pod.spec.node_name is not None:
            continue

        node = select_node(v1, pod)
        if node is None:
            print(f"Failed to schedule pod {pod.metadata.name}.", flush=True)
            continue

        result = schedule_pod(
            pod=pod.metadata.name,
            namespace=pod.metadata.namespace,
            node=node.metadata.name,
            api_url=configuration.host,
            api_token=configuration.get_api_key_with_prefix("authorization"),
        ).json()
        print(f"Scheduled node with result: {result}", flush=True)


if __name__ == "__main__":
    main()
