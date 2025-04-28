from kubernetes import client, config, watch


def main():
    # log in to cluster
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    w = watch.Watch()

    print("Watching pods in all namespaces...")
    for event in w.stream(v1.list_pod_for_all_namespaces):
        print(event['object'].spec.scheduler_name, flush=True)


if __name__ == '__main__':
    main()
