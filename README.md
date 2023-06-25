# oellrich-graph-in-python
This is a Python implementation of a generic graph class, derived from the C++ implementation of Prof. Martin Oellrich. The goal is to create a tool for additional implementations of algorithms on graphs, such as the Dijkstra-algorithm. It was implemented as part of a university assignment for the course "Operations Research" at the Berlin University of Applied Sciences ([BHT](https://www.bht-berlin.de/)) of [Department II](https://www.bht-berlin.de/ii).

## Requirements
Python 3.9 or higher

## Usage
In order to use the graph class, you can either:
### Option 1
Install the package via pip:
```bash
pip install git+https://github.com/saschkoh/oellrich-graph-in-python
```
and import the graph class into your project using one of the following commands:
```python
import oellrich_graph
from oellrich_graph import Graph, GraphReader
from oellrich_graph import *
```
### Option 2
Download the latest release from the [releases](https://github.com/saschkoh/oellrich-graph-in-python/releases) page and import the graph class into your project by copying the graph folder