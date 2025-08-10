# Setup Workshop

## Requirements
* The attendees operating system must be RHEL.

## Steps
* Create inventory file in the current directory named `inventory.yml` with the following format:
  ```yaml
  all:
    hosts:
      <attendee-ip1>: {}
      <attendee-ip2>: {}
      <attendee-ip3>: {}
      ...
      <attendee-ipX>: {}
    vars:
      ansible_user: <username>
  ```
* If the attendees' RHEL version is 9.X or later, run the ansible playbook using the following commands:
  ```bash
  ansible-playbook -i ./inventory.yml ./ansible/site.yml -e "kind_version=v0.29.0" --ask-pass --ask-become-pass
  ```
  Else, run the ansible playbook using the following commands:
  ```bash
  ansible-playbook -i ./inventory.yml ./ansible/site.yml -e "kind_version=v0.19.0" --ask-pass --ask-become-pass
  ```
* Verify the playbook finished successfully.