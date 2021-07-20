import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import datetime
import json
import db_connect as db_con
import User
import LocationDate 
import ItemInstance
import ItemClass
import Location

from JSONDeserialization import epcis_event as epc

event_types = {
    "ObjectEvent": epc.ObjectEvent(),
    "AggregationEvent": epc.AggregationEvent(),
    "QuantityEvent": epc.QuantityEvent(),
    "TransactionEvent": epc.TransactionEvent(),
    "TransformationEvent": epc.TransformationEvent(),
}

node_names = {
    "ObjectEvent": "objevt",
    "AggregationEvent": "aggevt",
    "QuantityEvent": "qtyevt",
    "TransactionEvent": 'txnevt',
    "TransformationEvent": "transevt",
}

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

"""
method creates an event node
Parameter: Any epcis Event
"""
def create_event_node(event):
    event_type = event.__class__.__name__ 
    node_name = node_names[event_type ]
    attributes = {}

    for attr in list(event.__dict__):
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
    return query
    print(query)


"""
method creates a Location node
Parameter: Location object
"""
def create_location_node(Location):
    
    query = """ 
    CREATE (
        loc:Location
        { 	
            id : '""" + Location.id +\
    """'    }
    )
    """
    return query

"""
method creates a LocationDate node
Parameter: Any LocationDate object
"""
def create_location_date_node(LocationDate):
    
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
    return query
    
"""
method creates a Company node
Parameter: Company object
"""
def create_company_node(company):
    
    query = """ 
    CREATE (
        comp:Company
        { 	
            name : '""" + company.name + "'"+\
            ", prefix : '"+ company.prefix + \
    """'   }
    )
    """
    print(query)
    return query

"""
method creates an User node
Parameter: A User object
"""
def create_user_node(user):
    
    query = """ 
    CREATE (
        user:User
        { 	
            id : '""" + user.id +\
    """'    }
    )
    """
    return query

"""
method creates an ItemInstance node
Parameter: A ItemInstance object
"""
def create_item_instance_node(item_class):
    query = """ 
    CREATE (
        item_inst:ItemInstance
        { 	
            epc : '""" + item_class.epc +\
    """'    }
    )
    """
    print(query)
    return query

"""
method creates an ItemClass node
Parameter: ItemClass object
"""
def create_item_class_node(item_class):
    query = """ 
    CREATE (
        item_class:ItemClass
        { 	
            epc : '""" + item_class.epc_class +\
    """'    }
    )
    """
    print(query)
    return query

"""
method creates Upload event relationship
Parameters: A User object and Event Object 
"""
def create_upload_relationship(User, Event):
    event = Event.__class__.__name__ 
    query = """
            MATCH (a:User), (b:"""+event+ """) 
            WHERE a.name = '"""+User.name +"""' AND b.event_id = '"""+str(Event.event_id) +"""'  
            CREATE (a)-[: UploadEvent]->(b) 
            RETURN a,b 
    """
    print(query)
    return query

"""
method creates a business_location relationship
Parameters: A LocationDate and Event Object 
"""
def create_biz_location_relationship(Event, LocationDate):
    event = Event.__class__.__name__ 
    query = """
            MATCH (a:LocationDate), (b:"""+event+ """) 
            WHERE a.date = '"""+LocationDate.date +"""' AND b.business_location = '"""+str(Event.business_location) +"""'  
            CREATE (a)-[: business_location]->(b) 
            RETURN a,b 
    """
    print(query)
    return query
   
"""
method creates a works_for relationship
Parameters: A User and Company Object 
"""
def create_works_for_relationship(User, Company):
    query = """
            MATCH (a:User), (b:Company) 
            WHERE a.id = '"""+User.id +"""' AND b.prefix = '"""+Company.prefix +"""'  
            CREATE (a)-[: works_for]->(b) 
            RETURN a,b 
    """
    print(query)
    return query

"""
method creates owns relationship
Parameters: A Location and Company Object 
"""
def create_owns_relationship(Location, Company):
    query = """
            MATCH (a:Location), (b:Company) 
            WHERE a.id = '"""+str(Location.id) +"""' AND b.prefix = '"""+Company.prefix +"""'  
            CREATE (a)-[:owns]->(b) 
            RETURN a,b 
    """
    print(query)
    return query

"""
method creates epc_list_item relationship
Parameters: A ItemClass and Event Object 
"""
def create_epc_list_item_relationship(item_class, event):
    event_name = event.__class__.__name__ 
    query = """
            MATCH (a:ItemClass), (b:"""+event_name+ """) 
            WHERE a.epc_class = '"""+item_class.epc_class +"""' AND b.event_id = '"""+str(event.event_id) +"""'  
            CREATE (a)-[: epc_list_item]->(b) 
            RETURN a,b 
    """
    print(query)
    return query
   
"""
method creates epc_list_item_instance relationship
Parameters: An ItemInstance and an Event Object 
"""
def create_epc_list_item_instance_relationship(item_instance, event):
    event_name = event.__class__.__name__ 
    query = """
            MATCH (a:ItemInstance), (b:"""+event_name+ """) 
            WHERE a.epc = '"""+item_instance.epc +"""' AND b.event_id = '"""+str(event.event_id) +"""'  
            CREATE (a)-[: epc_list_item]->(b) 
            RETURN a,b 
    """
    print(query)
    return query

"""
method creates input_epc_list relationship
Parameters: An ItemInstance and an Event Object 
"""
def create_input_epc_list_relationship(item_instance, event):
    event_name = event.__class__.__name__ 
    query = """
            MATCH (a:ItemInstance), (b:"""+event_name+ """) 
            WHERE a.epc = '"""+item_instance.epc +"""' AND b.event_id = '"""+str(event.event_id) +"""'  
            CREATE (a)-[: input_epc_list_item]->(b) 
            RETURN a,b 
    """
    print(query)
    return query

"""
method creates parent_id relationship
Parameters: An ItemInstance and an Event Object 
"""
def create_parent_id_relationship(item_instance, event):
    event_name = event.__class__.__name__ 
    query = """
            MATCH (a:ItemInstance), (b:"""+event_name+ """) 
            WHERE a.epc = '"""+item_instance.epc +"""' AND b.event_id = '"""+str(event.event_id) +"""'  
            CREATE (a)-[: parent_id]->(b) 
            RETURN a,b 
    """
    print(query)
    return query

"""
method creates child_epc relationship
Parameters: An ItemInstance and an Event Object 
"""
def create_child_epc_relationship(item_instance, event):
    event_name = event.__class__.__name__ 
    query = """
            MATCH (a:ItemInstance), (b:"""+event_name+ """) 
            WHERE a.epc = '"""+item_instance.epc +"""' AND b.event_id = '"""+str(event.event_id) +"""'  
            CREATE (a)-[:child_epc]->(b) 
            RETURN a,b 
    """
    print(query)
    return query

"""
method creates output_epc_list_item relationship
Parameters: An ItemInstance and an Event Object 
"""
def create_output_epc_list_item_relationship(item_class, event):
    event_name = event.__class__.__name__ 
    query = """
            MATCH (a:ItemClass), (b:"""+event_name+ """) 
            WHERE a.epc_class = '"""+item_class.epc_class +"""' AND b.transformation_id = '"""+str(event.transformation_id) +"""'  
            CREATE (a)-[: output_epc_list_item]->(b) 
            RETURN a,b 
    """
    print(query)
    return query

"""
method creates shared_transformation relationship
Parameters: Two Transformation Event Objects 
"""
def create_shared_transformation_relationship(Event1, Event2):
    event1 = Event1.__class__.__name__ 
    event2 = Event2.__class__.__name__ 
    query = """
            MATCH (a:"""+event1+ """), (b:"""+event2+ """) 
            WHERE a.transformation_id = '"""+Event1.transformation_id +"""' AND b.transformation_id = '"""+(Event2.transformation_id) +"""'  
            CREATE (a)-[:shared_transformation_id]->(b) 
            RETURN a,b 
    """
    print(query)
    return query

#Test these
"""
method creates quantity_list_item relationship
Parameters: ItemClass and TransformationEvent object
"""
def create_quantity_list_item_relationship(item_class, event):
    event_name = event.__class__.__name__ 
    query = """
            MATCH (a:ItemClass), (b:"""+event_name+ """) 
            WHERE a.epc_class = '"""+item_class.epc_class +"""' AND b.event_id= '"""+str(event.event_id) +"""'  
            CREATE (a)-[: quantity_list_item {quantity , uom}]->(b) 
            RETURN a,b 
    """
    print(query)
    return query

"""
method creates quantity_list_item relationship
Parameters: An ItemInstance and an TransactionEvent Object 
"""
def create_quantity_list_item_relationship(item_class, event):
    event_name = event.__class__.__name__ 
    query = """
            MATCH (a:ItemClass), (b:"""+event_name+ """) 
            WHERE a.epc_class = '"""+item_class.epc_class +"""' AND b.event_id = '"""+str(event.event_id) +"""'  
            CREATE (a)-[: quantity_list_item {quantity , uom}]->(b) 
            RETURN a,b 
    """
    print(query)
    return query


"""
method creates quantity_list_item relationship
Parameters: An ItemInstance and an Event Object 
"""
def create_quantity_list_item_relationship(item_class, event):
    event_name = event.__class__.__name__ 
    query = """
            MATCH (a:ItemClass), (b:"""+event_name+ """) 
            WHERE a.epc_class = '"""+item_class.epc_class +"""' AND b.event_id = '"""+str(event.event_id) +"""'  
            CREATE (a)-[: quantity_list_item {quantity , uom}]->(b) 
            RETURN a,b 
    """
    print(query)
    return query

"""
method creates child_quantity_list_item relationship
Parameters: An ItemInstance and an AggregationEvent Object 
"""
def create_child_quantity_list_item_relationship(item_class, event):
    event_name = event.__class__.__name__ 
    query = """
            MATCH (a:ItemClass), (b:"""+event_name+ """) 
            WHERE a.epc_class = '"""+item_class.epc_class +"""' AND b.event_id = '"""+str(event.event_id) +"""'  
            CREATE (a)-[: child_quantity_list_item {quantity ,uom}]->(b) 
            RETURN a,b 
    """
    print(query)
    return query

"""
method creates child_quantity_list_item relationship
Parameters: An ItemInstance and an TransformationEvent Object 
"""
def create_input_quantity_list_item_relationship(item_class, event):
    event_name = event.__class__.__name__ 
    query = """
            MATCH (a:ItemClass), (b:"""+event_name+ """) 
            WHERE a.epc_class = '"""+item_class.epc_class +"""' AND b.transformation_id = '"""+str(event.transformation_id) +"""'  
            CREATE (a)-[: input_quantity_list_item {quantity, uom}]->(b) 
            RETURN a,b 
    """
    print(query)
    return query

"""
method creates child_quantity_list_item relationship
Parameters: An ItemInstance and an TransformationEvent Object 
"""
def create_output_quantity_list_item_relationship(item_class, event):
    event_name = event.__class__.__name__ 
    query = """
            MATCH (a:ItemClass), (b:"""+event_name+ """) 
            WHERE a.epc_class = '"""+item_class.epc_class +"""' AND b.event_id = '"""+str(event.event_id) +"""'  
            CREATE (a)-[: output_quantity_list_item {quantity ,uom}]->(b) 
            RETURN a,b 
    """
    print(query)
    return query


"""
method creates child_quantity_list_item relationship
Parameters: An ItemInstance and an QuantityEvent Object 
"""
def create_epc_class_relationship(item_class, event):
    event_name = event.__class__.__name__ 
    query = """
            MATCH (a:ItemClass), (b:"""+event_name+ """) 
            WHERE a.epc_class = '"""+item_class.epc_class +"""' AND b.event_id= '"""+str(event.event_id) +"""'  
            CREATE (a)-[: epc_class {quantity}]->(b) 
            RETURN a,b 
    """
    print(query)
    return query


"""
method creates date relationship
Parameters: A Location and a LocationDate Object 
"""
def create_date_relationship(Location, LocationDate, date):
    query = """
            MATCH (a:LocationDate), (b:"""+Location+ """) 
            WHERE a.date = '"""+LocationDate.date +"""' AND b.id = '"""+str(Location.id) +"""'  
            CREATE (a)-[:"""+ date +"""]->(b) 
            RETURN a,b 
    """
    print(query)
    return query


conn = db_con.Neo4jConnection(uri="bolt://localhost:7687", 
                       user="neo4j",              
                       password="hjz!MTkA9_E5")
