import utils as ut
import json
import db_connect as db_con
import os

class Node:
    '''
    method initializes a object
    Args:
        Event: obj (i.e. ObjectEvent, AggregateEvent, ... for which we want to perform CRUD ops on)
    '''
    def __init__(self, Event) -> None:
        self.event_id = Event.event_id
        self.event_name = Event.__class__.__name__    
        self.attr_dict = ut.retrive_attr_dict_from_event(Event)

    def retrieve_node_by_event_id(self):
        '''
        This method retrives an event using its event_id
        The name attribute is used to determine what kind of Epcis Event it is

        returns an epcis event
        '''
        attribute_dict = self.retrieve_node_properties()
        event_name = attribute_dict["name"]
        event = ut.event_types[event_name]()
        for attr in list(event.__dict__.keys()):
            attr = attr[1:]

            try:
                instvar = getattr(event, attr)
                value = ut.attr_type_check(instvar, attribute_dict[attr])
                setattr(event, attr, value)
            except Exception as e:
                print(str(e), " : ",attr)

        return event

    def update_node(self):
        '''
        this method updates an event with a dictionary of attributes and values
        Args:
             attr_dict: dict
        '''
        
        attr_dict = ut.format_attr_dict(json.dumps(self.attr_dict,default=str))
        cipher_ql = """ MATCH (m:"""+ \
                                self.event_name + """
                               )
                        WHERE m.event_id = $event_id""" +\
                    """ SET  m = """+attr_dict + \
                    """ RETURN m"""
        
        result = connectdb().query(cipher_ql,{"event_id": str(self.event_id)})
        return result

    def remove_node_property(self,attribute):
        '''
        this method removes a property from a node. It takes an
        event attribute as an parameter
        Arg:
            attrubute: str
        '''
        cipher_ql = """ 
                    MATCH (m:"""+ \
                                self.event_name + """
                               )
                    WHERE m.event_id = $event_id
                    REMOVE m."""+attribute + """
                    RETURN m
        """
        result = connectdb().query(cipher_ql,{"event_id": str(self.event_id), "event_name":self.event_name, "attribute":attribute})
        return result

    def retrieve_node_properties(self):
        '''
        This method returns all the properties of an event
        Arg: 
            event_id: uuid 
        '''   
        cipher_ql = """  MATCH (m:"""+ \
                                self.event_name + """
                               )
                         WHERE m.event_id = $event_id
                         RETURN properties(m)
        """
        result = connectdb().query(cipher_ql,{"event_id": str(self.event_id)})
        if list(result):
            result = list(result[0])[0]
        return result
        
    def create_relationship(self,Event_b, relationship_label, relationship_values):
        '''
        this method creates relationship between the class node and another
        Args:
             Event_b : Event (i.e. event to create a relationship with)
             relationship_label: str
             relationship_values: list (optional)
        '''
        event_b_name =  Event_b.__class__.__name__ 
        
        cipher_ql = """
                    MATCH (a:"""+ self.event_name +"""), (m: """+ event_b_name +""")
                    WHERE a.event_id = $event_a_id AND m.event_id = $event_b_id
                    CREATE (a)-[rel: """+relationship_label+ """ {name : $relationship_values}]->(m)
                    RETURN a.name, rel
        """
        print(cipher_ql)
        result = connectdb().query(cipher_ql,{"event_a_id": str(self.event_id), "event_b_id": str(Event_b._event_id),
        "relationship_label":relationship_label,"relationship_values":relationship_values})
        
        return result

    def delete_node(self):
        '''
        This method deletes a node/event using its event_id
        '''
        cipher_ql = """ MATCH (n:"""+ self.event_name + """{event_id : $event_id})
                        DETACH DELETE n
                    """
        result = connectdb().query(cipher_ql,{"event_id": str(self.event_id)})
        return result

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
