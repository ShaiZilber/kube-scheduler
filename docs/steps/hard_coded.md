# Schedule on hard coded node

## Introduction
Implement the simplest scheduler: it should look for any Pod that hasn’t been placed yet and, if it’s meant for your scheduler, assign it unconditionally to a single, pre‑configured node.

## Requirements
* Continuously watch for Pods that remain unassigned and specify your scheduler.
* For each such Pod, bind it to the preconfigured node.
* Do not defer to the built‑in scheduler—you must handle scheduling yourself.
* Record each placement in your logs for visibility.

## Hints

