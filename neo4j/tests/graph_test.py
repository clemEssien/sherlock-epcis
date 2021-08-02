import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import graph as g

graph = g.Graph("new_graph")
existing_graph_name = "my-graph"

existing_graph = g.Graph(existing_graph_name)
bool_list = [True, False]

def test_exist_graph():
    response = graph.graph_exists()
    assert response in bool_list

def test_create_graph():
    response = graph.create_graph()
    assert response in bool_list

def test_betweenness():
    response = existing_graph.betweenness()
    assert isinstance(response, dict)

def test_betweenness_random():
    response = existing_graph.betweenness_random(2,0)
    assert isinstance(response, dict)

def test_remove_graph():
    response = graph.remove_graph()
    assert type(response)== list and len(response)<=1 