import utils as ut
import json
import db_connect as db_con
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from JSONDeserialization import epcis_event as epc


class Node:
    '''
    method initializes a object
    Args:
        obj: Event (i.e. ObjectEvent, AggregateEvent, ...)
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
        epcis_event = event_types[event_name]

        for attr in list(epcis_event.__dict__.keys()):
            attr = attr[1:]

            try:
                value = attribute_dict[attr]
                setattr(epcis_event, attr, value)
            except Exception as e:
                print(str(e))

        return epcis_event

    def update_node(self):
        '''
        this method updates an event with a dictionary of attributes and values
        Args:
             attr_dict: dict
        '''
        
        attr_dict = ut.format_attr_dict(json.dumps(self.attr_dict,default=str))
        cipher_ql = """ MATCH (m:$event_name)
                        WHERE m.event_id = $event_id""" +\
                    """ SET  m = """+attr_dict + \
                    """ RETURN m"""
        print(cipher_ql)
        result = connectdb().query(cipher_ql,{"event_id": self.event_id, "event_name":self.event_name})
        return result

    def remove_node_property(self,attribute):
        '''
        this method removes a property from a node. It takes an
        event attribute as an parameter
        Arg:
            attrubute: str
        '''
        cipher_ql = """
                    MATCH (m:$event_name)
                    WHERE m.event_id = $event_id
                    REMOVE m.$attribute
                    RETURN m
        """
        result = connectdb().query(cipher_ql,{"event_id": self.event_id, "event_name":self.event_name, "attribute":attribute})
        return result

    def retrieve_node_properties(self):
        '''
        This method returns all the properties of an event
        Arg: 
            event_id: uuid 
        '''   
        cipher_ql = """  MATCH (m:$event_name)
                         WHERE m.event_id = $event_id
                         RETURN properties(m)
        """
        result = connectdb().query(cipher_ql,{"event_id": self.event_id, "event_name":self.event_name})
        return result
        
    def create_relationship(Event_a, Event_b, relationship_label, relationship_values):
        '''
        this method creates relationship between two nodes/events
        e.g. ObjectEvent and AggregationEvent
        Args:
             Event_a : Event
             Event_b : Event
             relationship_label: str
             relationship_values: list (optional)
        '''
        event_a_name =  Event_a.__class__.__name__ 
        event_b_name =  Event_b.__class__.__name__ 
        cipher_ql = """ MATCH (a:$event_a_name), (m:$event_b_name)
                        WHERE a.event_id = $event_a_id AND m.event_id = $event_b_id
                        CREATE (a)-[rel: $relationship_label {name : $relationship_values}]->(m)
                        RETURN a.name, rel 
                    """
        result = connectdb().query(cipher_ql,{"event_a_id": Event_a.event_id, "event_b_id": Event_b.event_id,
        "event_a_name":event_a_name, "event_b_name":event_b_name, "relationship_label":relationship_label,
        "relationship_values":relationship_values})
        return result

    def delete_node(self):
        '''
        This method deletes a node/event using its event_id
        '''
        cipher_ql = """ MATCH (n:$event_name {event_id : $event_id})
                        DETACH DELETE n
                    """
        result = connectdb().query(cipher_ql,{"event_id": self.event_id, "event_name":self.event_name})
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

event_types = {
    "ObjectEvent": epc.ObjectEvent(),
    "AggregationEvent": epc.AggregationEvent(),
    "QuantityEvent": epc.QuantityEvent(),
    "TransactionEvent": epc.TransactionEvent(),
    "TransformationEvent": epc.TransformationEvent(),
}
