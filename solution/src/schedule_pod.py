import requests.status_codes


def schedule_pod(
    pod: str, namespace: str, node: str, api_url: str, api_token: str
) -> requests.Response:
    """
    Schedules a given pod from the given namespace on the given node, using the given api_token against the given api_url.
    :param pod: Name of the pod to schedule.
    :param namespace: Name of the namespace of the pod.
    :param node: Name of the node to schedule the pod on.
    :param api_url: URL to the API server, including port and protocol, e.g. https://api.my-cluster.com:8443.
    :param api_token: Authorization token for the API server.
    :return: Object representing the response of the API call from the API server.
    """
    res = requests.post(
        url=f"{api_url}/api/v1/namespaces/{namespace}/pods/{pod}/binding",
        json=dict(
            api_version="v1",
            kind="Binding",
            metadata={
                "namespace": namespace,
                "name": pod,
            },
            target={
                "apiVersion": "v1",
                "kind": "Node",
                "name": node,
            },
        ),
        verify=False,
        headers={"Authorization": api_token},
    )
    return res
