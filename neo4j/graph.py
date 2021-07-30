import os
import sys
from typing import Type
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

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

    def graph_exists(self):
        '''
        method checks to see if a graph with the provided name already exists
        returns boolean 
        '''
        query = """
                CALL gds.graph.exists($name) YIELD exists;
        """
        response = connectdb().query(query,self.__name)   
        return  response

    def create_graph(self):
        '''
        method creates a graph using the name provided in the constructor
        and projects all existing nodes and relationships unto the graph
        '''
        query = """
                CALL gds.graph.create($graph_name, '*', '*');
        """
        response = connectdb().query(query,{"graph_name":self.__name},None)   
        return  response
    
    def remove_graph(self):
        '''
        method removes a graph from the catalog
        '''
        query = """
                CALL gds.graph.drop('$graph_name', false) YIELD graphName;
                """
        return connectdb(query,{"graph_name": self.__name} )


 