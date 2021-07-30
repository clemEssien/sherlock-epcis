import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

# print(currentdir)
print(parentdir)
import graph as g

graph = g.Graph("new_graph")
existing_graph_name = "my-graph"

existing_graph = g.Graph(existing_graph_name)

def graph_exists_response(result)-> bool:
    if type(result) == list:
        if len(result) == 1:
            if 'False' in str(result[0]):
                return True
            if 'True' in str(result):
                return False
    return 
        

def test_exist_graph():
    response = graph.graph_exists()
    assert type(graph_exists_response(response)) == bool
def test_create_graph():
    response = existing_graph.create_graph()
    print(response)
    print(graph_exists_response(response))

test_create_graph()
