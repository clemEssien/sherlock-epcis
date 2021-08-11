import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import db_connect as db_con
from dotenv import load_dotenv
load_dotenv()

def simple_paths(source_event_id, source_event_name,  destination_event_id, destinatione_event_name, relationship):
    '''
    method returns simple paths between two Events
    The source/destination_event_name refers to the type of event
    For example, an ObjectEvent instance would have 'ObjectEvent' as it's event_name 
    Args:
        source_event_id : uuid
        source_event_name: str
        destination_event_id: uuid
        destination_event_name: str
        relationship: str
    '''
    cipher_ql = """
                MATCH (from: """+source_event_name + """ {event_id :$source_event_id}), (to: """+ destinatione_event_name + """ {event_id: $destination_event_id})
                CALL apoc.algo.allSimplePaths(from, to, $relationship, 1)
                YIELD path
                RETURN path 
    """
    result = connectdb().query(cipher_ql,{"source_event_id": str(source_event_id),
    "destination_event_id": str(destination_event_id), "relationship":relationship+">" })

    return result

# Dijkstra shortest path
def shortest_path(Source_node, Destination_node, relationship):
    cipher_ql = """
                MATCH (from:$source_node {id : $source_node_id}), (to:$destination_node{_id:'bc96c735-0776-4b7d-aa69-ac036f506295'})
                CALL apoc.algo.dijkstra(from, to, $relationship,'d') yield path as path, weight as weight
                RETURN path, weight
    """
    result = connectdb().query(cipher_ql,{"source_node":Source_node.__class__.__name__,
    "destination_node":Destination_node.__class__.__name__, "relationship":relationship })

    return result

def forward_trace(Node, relationship):
    cipher_ql = """
                MATCH (n:$node_name {_id : $node_id})
                CALL apoc.path.spanningTree(n, {
                relationshipFilter: $relationship,
                    minLevel: 1
                })
                YIELD path;
    """
    result = connectdb().query(cipher_ql, {"node_name": Node.__class__.__name__ ,"node_id":Node.id, "relationship":relationship+">"})
    return result

def backward_trace(Node, relationship):
    cipher_ql = """
                MATCH (n:$node_name {_id : $node_id})
                CALL apoc.path.spanningTree(n, {
                relationshipFilter: $relationship,
                    minLevel: 1
                })
                YIELD path;
    """
    result = connectdb().query(cipher_ql, {"node_name": Node.__class__.__name__ ,"node_id":Node.id, "relationship":relationship+"<"})
    return result

global conn 
conn = None
def connectdb() -> db_con.Neo4jConnection:
    """method returns a connection to the database"""
    global conn
    if not conn:
        conn = db_con.Neo4jConnection(uri=os.getenv("DB_URI"), 
                       user=os.getenv('DB_USER'),              
                       password=os.getenv('DB_PASS'))
    return conn