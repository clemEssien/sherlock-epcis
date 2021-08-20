import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from Neo4j import utils as ut
from dotenv import load_dotenv
load_dotenv()

import db_connect as db_con

class Graph:
    def __init__(self, name) -> None:
        '''
        This method initializes a graph by passing 
        the name of the graph as a string. The remove_graph()
        should be called at the end of each graph algorithm  
        Args:
             name: str
        '''
        self.name = name

    @property
    def name(self)->str:
        return self.__name
    
    @name.setter
    def name(self, value)->str:
        if isinstance(value, str):
            self.__name = value
        else:
            raise ValueError("Graph name has to be a string")
        

    def graph_exists(self) -> bool:
        '''
        method checks to see if a graph with the provided name already exists
        returns boolean 
        '''
        cipher_ql = """
                CALL gds.graph.exists($name) YIELD exists;
        """
        response = connectdb().query(cipher_ql,{"name":self.__name})
        return response[0]['exists']

    def create_graph(self)->bool:
        '''
        method creates a graph using the name provided in the constructor
        and projects all existing nodes and relationships unto the graph
        '''
        try: 
            if self.graph_exists():
                response = False
            else:
                cipher_ql = """
                        CALL gds.graph.create($graph_name, '*', '*');
                """
                response = connectdb().query(cipher_ql,{"graph_name":self.__name})
                response = 'Record nodeProjection' in str(response[0])
            return  response
        except Exception as e:
            print(str(e))
            return False

    
    def betweenness(self)->dict:
        '''
        This method calls the between-ness centrality algorithm on a named graph
        '''
        cipher_ql = """
                    CALL gds.betweenness.stream($graph_name)
                    YIELD nodeId, score
                    RETURN gds.util.asNode(nodeId).name AS name, score
                    ORDER BY name ASC
        """
        response = connectdb().query(cipher_ql,{"graph_name": self.__name} )
        return ut.algorithm_response(response)


    def betweenness_random(self,sample_size, seed)->dict:
        '''
        This method calls the between-ness centrality algorithm on a named graph. But
        as the graph becomes large, it might become an expensive operation to load the
        complete graph in memory. If we choose to use a random sample size, we could use
        the betweenness_random() instead and pass an int to specify the sampel size 
        Args:
             sample_size: int
             seed: int
        '''
        if ut.verify_algo_args(sample_size, seed):
                cipher_ql = """
                            CALL gds.betweenness.stream($graph_name, {samplingSize : $samplingSize, samplingSeed : $samplingSeed})
                            YIELD nodeId, score
                            RETURN gds.util.asNode(nodeId).name AS name, score
                            ORDER BY name ASC
                """
                response = connectdb().query(cipher_ql,{"graph_name": self.__name,"samplingSize": sample_size, "samplingSeed": seed} )
                return ut.algorithm_response(response)

        else:
            return False

    def remove_graph(self)->str:
        '''
        method removes a graph from the catalog
        returns the name of the graph
        '''
        cipher_ql = """
                CALL gds.graph.drop($graph_name, false) YIELD graphName;
                """
        result = connectdb().query(cipher_ql,{"graph_name": self.__name} )
        response = ""
        try:
            response = result[0]['graphName'] 
        except Exception as e:
            response = result
        return response

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