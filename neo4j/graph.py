import os
import sys
from typing import Type
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import json
import db_connect as db_con


global conn 
conn = None

def connectdb() -> db_con.Neo4jConnection:
    """method returns a connection to the database"""
    global conn
    if not conn:
        conn = db_con.Neo4jConnection(uri="bolt://localhost:7687", 
                       user="neo4j",              
                       password=os.environ['NEO4J_PASSWORD'])

    return conn

class Graph:
    def __init__(self, name) -> None:
        '''
        This method initializes a graph by passing 
        the name of the graph as a string

        Args:
             name: str
        '''
        self.__name = name

    def create_graph(self):
        '''
        method creates a graph using the name provided in the constructor
        
        '''
        query = """
                CALL gds.graph.exists($name) YIELD exists;
        """
        response = conn.query(query,self.__name,None)   
        return  response

    def graph_exists(self):
        '''
        method checks to see if a graph with the provided name already exists
        returns boolean 
        '''
        query = """
                CALL gds.graph.exists($name) YIELD exists;
        """
        response = conn.query(query,self.__name)   
        return  response
    
    def project_nodes_to_graph(self):
        '''
        method projects existing nodes to an existing graph in the db
        '''
        
        if graph_exists() == False:
            query = """
            CALL gds.graph.create($name, '*', '*')
            YIELD graphName, nodeCount, relationshipCount;
            """
            return conn.query(query,self.__name)
        else:
            return "A graph with name ",self.__name," already exists"
    
    def remove_node_from_graph(self):
        query = """
        CALL gds.graph.removeNodeProperties('my-graph', ['pageRank', 'communityId'])
        """


 