import os
from pathlib import Path
from random import choice

import kubernetes.client
from kubernetes import client, watch, config

from schedule_pod import schedule_pod


def load_config():
    configuration = client.Configuration()
    if kubeconfig := os.getenv('KUBECONFIG'):
        kubeconfig = Path(kubeconfig)
    if kubeconfig is not None and kubeconfig.exists() and kubeconfig.is_file():
        config.load_kube_config(client_configuration=configuration)
    else:
        config.load_incluster_config(client_configuration=configuration)
    return configuration


def select_node(v1: kubernetes.client.CoreV1Api, pod: kubernetes.client.V1Pod) -> kubernetes.client.V1Node:
    nodes = v1.list_node().items
    return choice(nodes)


def main():
    configuration = load_config()

    v1 = client.CoreV1Api(client.ApiClient(configuration))
    w = watch.Watch()

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
