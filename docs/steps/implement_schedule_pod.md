# Implement `schedule_pod` function

## Introduction
Write the provided `schedule_pod` function  

## Requirements
* In your main.py write function with the following signature:
  * schedule_pod(
      pod: str, namespace: str, node: str, api_url: str, api_token: str
  ) -> requests.Response
* The function should make the api call that schedules a pod to a node.
