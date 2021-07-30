import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import db_connect as db_con

class Graph:
    def __init__(self, name) -> None:
        '''
        This method initializes a graph by passing 
        the name of the graph as a string

        Args:
             name: str
        '''
        self.__name = name

    def graph_exists(self) -> bool:
        '''
        method checks to see if a graph with the provided name already exists
        returns boolean 
        '''
        cipher_ql = """
                CALL gds.graph.exists($name) YIELD exists;
        """
        response = connectdb().query(cipher_ql,{"name":self.__name})
        print(response)
        if type(response) == list and len(response) ==1:  
            result = string_btw_xters(str(response),'=','>')
        return  bool(result)

    def create_graph(self):
        '''
        method creates a graph using the name provided in the constructor
        and projects all existing nodes and relationships unto the graph
        '''
        try: 
            if not self.graph_exists():
                response = False
            else:
                cipher_ql = """
                        CALL gds.graph.create($graph_name, '*', '*');
                """
                response = connectdb().query(cipher_ql,{"graph_name":self.__name})
                response = 'Record nodeProjection' in str(response[0])
            return  response
        except Exception as e:
            return False

        
    
    def remove_graph(self):
        '''
        method removes a graph from the catalog
        '''
        cipher_ql = """
                CALL gds.graph.drop($graph_name, false) YIELD graphName;
                """
        response = connectdb().query(cipher_ql,{"graph_name": self.__name} )
        return response


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


def string_btw_xters(string, initial, terminating)->str:
    '''
    method returns the string in between two characters
    Args:
        string: str
        initial character: str
        terminal character: str
    '''
    start = string.find(initial) + len(initial)
    end = string.find(terminating)
    return string[start:end]


 