from kubernetes import client, watch, config

from schedule_pod import schedule_pod


def main():
    configuration = client.Configuration()
    config.load_incluster_config(client_configuration=configuration)

    # configuration = client.Configuration(host="https://localhost:6443")
    # configuration.api_key["authorization"] = (
    #     "eyJhbGciOiJSUzI1NiIsImtpZCI6IlZTWFpfSEpXa0V4UDZtbWg4bkozUEZJZkI3Z2lWMG9ubTRXYnJiWEN3bTQifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoyMTA2NjE0NjIyLCJpYXQiOjE3NDY2MTgyMjIsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwianRpIjoiNGQ1MGY3Y2UtYzM5YS00YmE2LTg0YmEtNTVlYjNlODg4YWNhIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJkZWZhdWx0Iiwic2VydmljZWFjY291bnQiOnsibmFtZSI6InNjaGVkdWxlciIsInVpZCI6IjdmY2U2ZTdkLWUzZmQtNDZhOC04YzRlLWQ4ODQwMmIxN2E3NCJ9fSwibmJmIjoxNzQ2NjE4MjIyLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6ZGVmYXVsdDpzY2hlZHVsZXIifQ.rE_jrJXMaPfBcrNH9j6SSQCn5zE1Md9QBfZ4Y6HxVYRNjZ64egca-ubvT_S4k_6RFwgses6Dnkcg5yxu4Ry8fG9mh2Url2DXcWQRneP5MMQ83UkBdGbwi74oSzJfWsByHC_NWjs6G3n6aAa3aVyMJIDI2PL-0hVrvZqbMKW_bz70VboseqhjTXxA4omIFRZCM75ZKo7UB9SeN42ipMQFnF7CeMJvCyq5smwtteYCe3ip6bFmHKMwj1zwCY1CjcJIh8odz9X6tszwjjZQeW2x9RSaRZ_vXDRIuNwiSL3uedndcdqakV_7QDTvc61XEGhF82e0YmJvU3G69xfsHBfaBQ"
    # )
    # configuration.api_key_prefix["authorization"] = "Bearer"
    # # configuration.host = 'https://localhost:6443'
    # configuration.verify_ssl = False

    v1 = client.CoreV1Api(client.ApiClient(configuration))
    w = watch.Watch()

    print("Watching pods in all namespaces...")
    for event in w.stream(
        v1.list_pod_for_all_namespaces, field_selector="spec.schedulerName==custom"
    ):
        if event["object"].spec.node_name is not None:
            continue

        print(
            schedule_pod(
                pod=event["object"].metadata.name,
                namespace=event["object"].metadata.namespace,
                node="docker-desktop",
                api_url=configuration.host,
                api_token=configuration.get_api_key_with_prefix("authorization"),
            ),
        )


if __name__ == "__main__":
    main()
