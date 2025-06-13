# Schedule based on Node Resource Usage

## Introduction
Make your scheduler "Least Allocated": give nodes score based on how few resources are allocated[^1] on them   


## Requirements
* multiply each node's current score by the following formula:
  
  $` \frac{  \frac{\text{cpu capacity} - \text{cpu requested}}{\text{cpu capacity}} + \frac{\text{memory capacity} - \text{memory requested}}{\text{memory capacity}}}{2} `$
* pick the one with the new highest score.
* Bind the Pod to the selected node.


[^1]: in kubernetes terms, allocated resources are the sum of requests of all pods on the node not the sum of the usage of all pods on the node 