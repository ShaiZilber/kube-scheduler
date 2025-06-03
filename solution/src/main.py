import os
from random import choice

import kubernetes

from schedule_pod import schedule_pod
from solution.src.taints_and_tolerations import tolerates


def load_config():
    configuration = kubernetes.client.Configuration()
    kubeconfig = os.getenv('KUBECONFIG')
    if kubeconfig is not None and os.path.isfile(kubeconfig):
        kubernetes.config.load_kube_config(client_configuration=configuration)
    else:
        kubernetes.config.load_incluster_config(client_configuration=configuration)
    return configuration


def select_node(v1: kubernetes.client.CoreV1Api, pod: kubernetes.client.V1Pod) -> kubernetes.client.V1Node:
    filtered_nodes = []
    for node in v1.list_node().items:
        # Advanced Step 3
        if not(tolerates(node, pod)):
            continue

        filtered_nodes.append(node)
    return choice(filtered_nodes)


def main():
    configuration = load_config()

    v1 = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
    w = kubernetes.watch.Watch()

    print("Watching pods in all namespaces...", flush=True)
    for event in w.stream(
            v1.list_pod_for_all_namespaces, field_selector="spec.schedulerName==custom"
    ):
        if event["object"].spec.node_name is not None:
            continue

        node = select_node(v1, event["object"])
        print(
            node,
            schedule_pod(
                pod=event["object"].metadata.name,
                namespace=event["object"].metadata.namespace,
                node=node.metadata.name,
                api_url=configuration.host,
                api_token=configuration.get_api_key_with_prefix("authorization"),
            ).json(),
            flush=True,
        )


if __name__ == "__main__":
    main()
