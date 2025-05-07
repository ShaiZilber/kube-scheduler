from requests import Response

def schedule_pod(
    pod: str, namespace: str, node: str, api_url: str, api_token: str
) -> Response: ...
