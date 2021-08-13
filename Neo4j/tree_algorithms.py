import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from Neo4j import db_connect as db_con
from dotenv import load_dotenv
load_dotenv()

def simple_paths(source_event_id, source_event_name,  destination_event_id, destination_event_name, relationship):
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
                MATCH (from: """+source_event_name + """ {event_id :$source_event_id}), (to: """+ destination_event_name + """ {event_id: $destination_event_id})
                CALL apoc.algo.allSimplePaths(from, to, $relationship, 1)
                YIELD path
                RETURN path 
    """
    result = connectdb().query(cipher_ql,{"source_event_id": str(source_event_id),
    "destination_event_id": str(destination_event_id), "relationship":relationship+">" })

    return result

def shortest_path(source_event_id, source_event_name,  destination_event_id, destination_event_name, relationship):
    '''
    method returns shortest paths between two Events
    The source/destination_event_name refers to the type of event
    For example, an ObjectEvent instance would have 'ObjectEvent' as it's event_name 
    Args:
        source_event_id : uuid or str
        source_event_name: str
        destination_event_id: uuid or str
        destination_event_name: str
        relationship: str
    '''
    cipher_ql = """
                MATCH (from:"""+ source_event_name + """ {event_id : $source_event_id}), (to: """ + destination_event_name + """{event_id: $destination_event_id})
                CALL apoc.algo.dijkstra(from, to, $relationship,'d') yield path as path, weight as weight
                RETURN path, weight
    """
    result = connectdb().query(cipher_ql,{"source_event_id": str(source_event_id),
    "destination_event_id": str(destination_event_id), "relationship":relationship })

    return result

def forward_trace(event_id, event_label,relationship):
    '''
    This returns the path from the forward trace for a starting node
    Args:
        event_label: str
        relationship: str
    '''
    cipher_ql = """
                MATCH (n: """+ event_label +""" {event_id : $event_id})
                CALL apoc.path.spanningTree(n, {
                relationshipFilter: $relationship,
                    minLevel: 1
                })
                YIELD path
                RETURN path;
    """
    result = connectdb().query(cipher_ql, {"event_id":event_id, "relationship":relationship+">"})
    return result

def backward_trace(event_id, event_label,relationship):
    cipher_ql = """
                MATCH (n: """+ event_label +""" {event_id : $event_id})
                CALL apoc.path.spanningTree(n, {
                relationshipFilter: $relationship,
                    minLevel: 1
                })
                YIELD path
                RETURN path;
    """
    result = connectdb().query(cipher_ql, {"event_id":event_id, "relationship":relationship+"<"})
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