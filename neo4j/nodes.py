import os
import sys
from typing import Type
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import datetime
import json
import db_connect as db_con
from JSONDeserialization import epcis_event as epc

node_names: "dict[str]" = {
    "ObjectEvent": "objevt",
    "AggregationEvent": "aggevt",
    "QuantityEvent": "qtyevt",
    "TransactionEvent": 'txnevt',
    "TransformationEvent": "transevt",
}

def connectdb() -> db_con.Neo4jConnection:
    """method returns a connection to the database"""
    return db_con.Neo4jConnection(uri="bolt://localhost:7687", 
                       user="neo4j",              
                       password=os.environ['NEO4J_PASSWORD'])

def format_dictionary_attribute(dict):
    """as neo4j only stores primitive types or arrays, this method converts dictionary types
       into a string of key value pairs
       Args:
            obj: dictionary variable
       Returns: string of key value pairs
    """
    output = ""
    for key, value in dict:
        output += key+ ":" +value +","
    
    return output[:-1]

def format_query(query):
    query = query.split()
    new_query = ""
    for item in query:
        if '":' in item:
            new_query += item.replace('"', ' ')
        elif '[]' in item:
            new_query += item.replace('[]', '\"\"')
        else:
            new_query += item
    return new_query


def create_event_node(event):
    """Method creates an event node from an event object
        Args: 
             Event node
        Returns:
             Query String
    """
    event_type = event.__class__.__name__ 
    node_name = node_names[event_type]
    attributes = {}

    for attr in list(event.__dict__):
        instvar = getattr(event, attr)
        if isinstance(instvar, dict):
            attributes[attr[1:]] = json.dumps(getattr(event, attr))
        else:
            attributes[attr[1:]] = getattr(event, attr)
    attributes = json.dumps(attributes,default=str)
    query = """ 
            CREATE (""" + \
                node_name + ":" + event_type  + \
                attributes + \
                """
            )
            """
    query = format_query(query)
    print(query)
    return connectdb().query(query,None)	
   

def create_location_node(Location):
    """method creates a Location node
       Args: 
            Location object
    """    
    query = """ 
    CREATE (
        loc:Location
        {   
            id : '""" + Location.id +\
    """'    }
    )
    """
    print(query)
    return connectdb().query(query,None)	
    

def create_location_date_node(LocationDate):
    """method creates a LocationDate node
        Args:
            LocationDate object
    """
    query = """ 
    CREATE (
        loc_date:LocationDate
        {   
            id : '""" + LocationDate.id + "'"+\
            ", date : datetime('"+ LocationDate.date + \
    """')    }
    )
    """
    print(query)
    return connectdb().query(query,None)	
    

def create_company_node(company):
    """method creates a Company node
       Args: 
            Company object
    """
    query = """ 
    CREATE (
        comp:Company
        {   
            id :  '"""+ company.id + "' ," +\
            "location : '""" + company.location + "'"+\
            ", prefix : '"+ company.prefix + \
    """'   }
    )
    """
    print(query)
    return connectdb().query(query,None)	

def create_user_node(user): 
    """method creates an User node
    Args: 
        A User object
    """
    query = """ 
    CREATE (
        user: User
        {   
            id : '""" + str(user.id) +\
    """'    }
    )
    """
    print(query)
    return connectdb().query(query,None)	

def create_item_instance_node(item_class):
    """method creates an ItemInstance node
    Arg: 
        A ItemInstance object
    """
    query = """ 
    CREATE (
        item_inst:ItemInstance
        {   
            epc : '""" + str(item_class.epc) +\
    """'    }
    )
    """
    print(query)
    return connectdb().query(query,None)	


def create_item_class_node(item_class):
    """method creates an ItemClass node
    Args: 
        ItemClass object
    """
    query = """ 
    CREATE (
        item_class:ItemClass
        {   
            epc_class : '""" + str(item_class.epc_class) +\
    """'    }
    )
    """
    print(query)
    return connectdb().query(query,None)	

def create_upload_relationship(User, Event):
    """method creates Upload event relationship
    Args: 
        A User object and Event Object 
    """
    event = Event.__class__.__name__ 
    query = """
            MATCH (a:User), (b:"""+event+ """) 
            WHERE a.id = '"""+ str(User.id) +"""' AND b.event_id = '"""+str(Event.event_id) +"""'  
            CREATE (a)-[: UploadEvent]->(b) 
            RETURN a,b 
    """
    print(query)
    return connectdb().query(query,None)	


def create_biz_location_relationship(Event, LocationDate):
    """method creates a business_location relationship
    Args: 
         obj: LocationDate
         obj: Event Object 
    """
    event = Event.__class__.__name__ 
    query = """
            MATCH (a:LocationDate), (b:"""+event+ """) 
            WHERE a.date = '"""+LocationDate.date +"""' AND b.business_location = '"""+str(Event.business_location) +"""'  
            CREATE (a)-[: business_location]->(b) 
            RETURN a,b 
    """
    print(query)
    return connectdb().query(query,None)	
   

def create_works_for_relationship(User, Company):
    """method creates a works_for relationship
    Args: 
        obj: User
        obj: Company 
    """
    query = """
            MATCH (a:User), (b:Company) 
            WHERE a.id = '"""+User.id +"""' AND b.prefix = '"""+Company.prefix +"""'  
            CREATE (a)-[: works_for]->(b) 
            RETURN a,b 
    """
    print(query)
    return connectdb().query(query,None)	


def create_owns_relationship(Location, Company):
    """method creates owns relationship
    Args: 
        obj: Location
        obj: Company
    """
    query = """
            MATCH (a:Location), (b:Company) 
            WHERE a.id = '"""+str(Location.id) +"""' AND b.prefix = '"""+Company.prefix +"""'  
            CREATE (a)-[:owns]->(b) 
            RETURN a,b 
    """
    print(query)
    return connectdb().query(query,None)	


def create_epc_list_item_relationship(item_class, event):
    """method creates epc_list_item relationship
    Args: 
        obj: ItemClass
        obj: Event 
    """
    event_name = event.__class__.__name__ 
    query = """
            MATCH (a:ItemClass), (b:"""+event_name+ """) 
            WHERE a.epc_class = '"""+str(item_class.epc_class) +"""' AND b.event_id = '"""+str(event.event_id) +"""'  
            CREATE (a)-[:epc_list_item]->(b) 
            RETURN a,b 
    """
    print(query)
    return connectdb().query(query,None)	
   

def create_epc_list_item_instance_relationship(item_instance, event):
    """method creates epc_list_item_instance relationship
    Args: 
        obj: ItemInstance
        obj: Event 
    """
    event_name = event.__class__.__name__ 
    query = """
            MATCH (a:ItemInstance), (b:"""+event_name+ """) 
            WHERE a.epc = '"""+str(item_instance.epc) +"""' AND b.event_id = '"""+str(event.event_id) +"""'  
            CREATE (a)-[:epc_list_item_inst]->(b) 
            RETURN a,b 
    """
    print(query)
    return connectdb().query(query,None)	


def create_input_epc_list_relationship(item_instance, event):
    """method creates input_epc_list relationship
    Args: 
        obj: ItemInstance
        obj: TransformationEvent 
    """
    event_name = event.__class__.__name__ 
    query = """
            MATCH (a:ItemInstance), (b:"""+event_name+ """) 
            WHERE a.epc = '"""+str(item_instance.epc) +"""' AND b.event_id = '"""+str(event.event_id) +"""'  
            CREATE (a)-[:input_epc_list_item]->(b) 
            RETURN a,b 
    """
    print(query)
    return connectdb().query(query,None)	


def create_parent_id_relationship(item_instance, event):
    """method creates parent_id relationship
    Args: 
        obj: ItemInstance
        obj: AggregationEvent 
    """
    event_name = event.__class__.__name__ 
    query = """
            MATCH (a:ItemInstance), (b:"""+event_name+ """) 
            WHERE a.epc = '"""+str(item_instance.epc) +"""' AND b.event_id = '"""+str(event.event_id) +"""'  
            CREATE (a)-[:parent_id]->(b) 
            RETURN a,b 
    """
    print(query)
    return connectdb().query(query,None)	

def create_child_epc_relationship(item_instance, event):
    """method creates child_epc relationship
    Args: 
        obj: ItemInstance
        obj: AggregtionEvent 
    """
    event_name = event.__class__.__name__ 
    query = """
            MATCH (a:ItemInstance), (b:"""+event_name+ """) 
            WHERE a.epc = '"""+str(item_instance.epc) +"""' AND b.event_id = '"""+str(event.event_id) +"""'  
            CREATE (a)-[:child_epc]->(b) 
            RETURN a,b 
    """
    print(query)
    return connectdb().query(query,None)	

def create_output_epc_list_item_relationship(item_class, event):
    """
    method creates output_epc_list_item relationship
       Args: 
            obj: ItemInstance
            obj: Event 
    """
    event_name = event.__class__.__name__ 
    query = """
            MATCH (a:ItemClass), (b:"""+event_name+ """) 
            WHERE a.epc_class = '"""+str(item_class.epc_class) +"""' AND b.transformation_id = '"""+str(event.transformation_id) +"""'  
            CREATE (a)-[: output_epc_list_item]->(b) 
            RETURN a,b 
    """
    print(query)
    return connectdb().query(query,None)	

def create_shared_transformation_relationship(Event1, Event2):
    """method creates shared_transformation relationship
       Args: 
            obj: Transformation
            obj: Event 
    """
    event1 = Event1.__class__.__name__ 
    event2 = Event2.__class__.__name__ 
    query = """
            MATCH (a:"""+event1+ """), (b:"""+event2+ """) 
            WHERE a.transformation_id = '"""+str(Event1.transformation_id) +"""' AND b.transformation_id = '"""+str(Event2.transformation_id) +"""'  
            CREATE (a)-[:shared_transformation_id]->(b) 
            RETURN a,b 
    """
    print(query)
    return connectdb().query(query,None)	

#Test these
def create_quantity_list_item_relationship(item_class, event):
    """method creates quantity_list_item relationship
    Args: 
        obj: ItemClass
        obj: TransformationEvent/TransactionEvent/ObjectEvent
    """
    event_name = event.__class__.__name__ 
    query = """
            MATCH (a:ItemClass), (b:"""+event_name+ """) 
            WHERE a.epc_class = '"""+str(item_class.epc_class) +"""' AND b.event_id= '"""+str(event.event_id) +"""'  
            CREATE (a)-[: quantity_list_item_quantity_uom]->(b) 
            RETURN a,b 
    """
    print(query)
    return connectdb().query(query,None)	
	
def create_child_quantity_list_item_relationship(item_class, event):
    """method creates child_quantity_list_item relationship
    Args: 
         obj: ItemInstance
         obj: AggregationEvent 
    """
    event_name = event.__class__.__name__ 
    query = """
            MATCH (a:ItemClass), (b:"""+event_name+ """) 
            WHERE a.epc_class = '"""+str(item_class.epc_class) +"""' AND b.event_id = '"""+str(event.event_id) +"""'  
            CREATE (a)-[: child_quantity_list_item_quantity_uom]->(b) 
            RETURN a,b 
    """
    print(query)
    return connectdb().query(query,None)	


def create_input_quantity_list_item_relationship(item_class, event):
    """method creates child_quantity_list_item relationship
    Args: 
        obj: ItemInstance
        obj: TransformationEvent 
    """
    event_name = event.__class__.__name__ 
    query = """
            MATCH (a:ItemClass), (b:"""+event_name+ """) 
            WHERE a.epc_class = '"""+str(item_class.epc_class) +"""' AND b.transformation_id = '"""+str(event.transformation_id) +"""'  
            CREATE (a)-[: input_quantity_list_item_quantity_uom]->(b) 
            RETURN a,b 
    """
    print(query)
    return connectdb().query(query,None)	


def create_output_quantity_list_item_relationship(item_class, event):
    """method creates child_quantity_list_item relationship
    Args: 
         obj: ItemInstance
         obj: TransformationEvent 
    """
    event_name = event.__class__.__name__ 
    query = """
            MATCH (a:ItemClass), (b:"""+event_name+ """) 
            WHERE a.epc_class = '"""+str(item_class.epc_class) +"""' AND b.event_id = '"""+str(event.event_id) +"""'  
            CREATE (a)-[: output_quantity_list_item_quantity_uom]->(b) 
            RETURN a,b 
    """
    print(query)
    return connectdb().query(query,None)	


def create_epc_class_relationship(item_class, event):
    """method creates child_quantity_list_item relationship
    Args: 
         obj: ItemInstance
         obj: QuantityEvent 
    """
    event_name = event.__class__.__name__ 
    query = """
            MATCH (a:ItemClass), (b:"""+event_name+ """) 
            WHERE a.epc_class = '"""+str(item_class.epc_class) +"""' AND b.event_id= '"""+str(event.event_id) +"""'  
            CREATE (a)-[: epc_class_quantity]->(b) 
            RETURN a,b 
    """
    print(query)
    return connectdb().query(query,None)	


def create_date_relationship(location, location_date):
    """method creates date relationship
    Args: 
        obj: Location
        obj: LocationDate 
        str: date
    """
    query = """
            MATCH (a:LocationDate), (b:Location) 
            WHERE a.id = '"""+location_date.id +"""' AND b.id = '"""+str(location.id) +"""'  
            CREATE (a)-[:date]->(b) 
            RETURN a,b 
    """
    print(query)
    return connectdb().query(query,None)	
