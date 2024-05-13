Getting Started with the Haruspecs Dispatch Rules Engine
Welcome to the Haruspecs Dispatch Rules Engine documentation. This section provides a foundational overview designed for electrical and software engineers who are familiar with microgrid concepts and have a basic understanding of energy nodes within such systems. Haruspecs is engineered to facilitate sophisticated control and optimization strategies for microgrid operations through an intuitive rules-based approach.

# Overview of PROJECTNAME
Haruspecs leverages a flexible and expressive rules engine to dynamically manage energy resources within a microgrid. By defining conditions and corresponding dispatch orders, engineers can automate responses to various operational states, enhancing efficiency and reliability.

## Energy Nodes
Energy nodes are the primary elements within our microgrid model, representing physical and virtual components such as inverters, batteries, and aggregated data points (like total site capacity or external conditions like UTC time).

### Identifiers: Each energy node is uniquely identified by a string that describes its path within the microgrid's topology. For example, heila-001/inverter-001 identifies the first inverter connected to the microgrid controller labeled heila-001.

## TODO links

## Dispatch Orders
Dispatch orders are actions executed in response to specific conditions evaluated within the microgrid. These orders direct energy nodes to adjust their operational parameters or states.

### Format 
A dispatch order includes the targeted energy node and the desired operation, articulated in a straightforward command format.

### Rules
Rules are the core mechanism through which the engine evaluates and reacts to changes in the microgrid. Each rule consists of a condition that, when met, triggers one or more dispatch orders.

Structure: Rules are written as conditional expressions that, upon being true, initiate defined actions.

```text
if (attribute@node_identifier operator value) then action-->node_identifier = new_value[,action-->node_identifier = new_value]
```
TODO railroad diagram
Example Rule:
```text
if (real_power@heila-001/inverter-001 > 500) then set_real_power-->heila-001/inverter-001 = 500
```
This rule monitors the real_power of heila-001/inverter-001. If it exceeds 500 units, the rule triggers a dispatch order to set the real_power to 500 units.
TODO realistic example

Wildcards in Node Identifiers
To streamline rule creation and enhance flexibility, PROJECTNAME supports wildcards in energy node identifiers:

Asterisk (*) Wildcard: Allows rules to target multiple nodes under a pattern, simplifying large-scale operations.

Usage Examples:
- `*/inverter*` matches all inverters across all controllers.
- `heila-001/inverter*` matches all inverters connected to heila-001.

## Simple Rule Writing
Here is a straightforward guide to writing a rule:

TODO