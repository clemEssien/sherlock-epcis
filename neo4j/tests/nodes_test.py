import os
import sys
import uuid
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import Company as c
import ItemClass as ic
import ItemInstance as it
import Location as l
import LocationDate as ld
import User as us
import nodes as n

from JSONDeserialization import epcis_event as epc
from uuid import UUID

from _pytest.python import pytest_pycollect_makeitem
from _pytest.python_api import raises
import pytest


item_class = ic.ItemClass("urn:epc:id:sgtin:0614141.107346.2018")
company = c.Company('01', 'urn:epc:id','urn:epc:id:sgln:0012345.11111.0')
location = l.Location('urn:epc:id:sgln:0012345.11111.0',"")
location_date = ld.LocationDate('urn:epc:id:sgln:0614141.00888.0', '2021-07-22')
item_instance = it.ItemInstance('urn:epc:id:sgln:0456432.0096.0')


user = us.User(uuid.UUID("f5cefc07-0c34-4b55-b3bf-671e5fd9835b"),"Clement")


obj_event = epc.ObjectEvent()
agg_event = epc.AggregationEvent()
tx_event = epc.TransactionEvent()
trans_event = epc.TransformationEvent()
trans_event1 = epc.TransformationEvent()
qty_event = epc.QuantityEvent()

obj_event.event_id = uuid.UUID("14ab0519-c147-43c6-a6ea-9bd21c259752").hex
obj_event._read_point = "urn:epc:id:sgln:0012345.11111.400"

agg_event.event_id = uuid.UUID("a2624953-f2e6-4369-8e71-9ee1a19d81d5").hex
agg_event.read_point = "urn:epc:id:sgln:0614141.00777.0"
agg_event.parent_id =  "urn:epc:id:sgln:5566661.00777.0"

tx_event.event_id = uuid.UUID("5d218c6c-761a-4f10-9827-7eb8b76c0749").hex
tx_event.read_point = "urn:epc:id:sgln:Building_Red_V7<"
tx_event.parent_id = "urn:epc:id:sgln:53331.00564.0"

trans_event.event_id = uuid.UUID("247e4422-2d24-4493-ae7b-2546a37a740a").hex
trans_event.transformation_id = "urn:epc:id:sgtin:4012345.077889.28"

trans_event1.event_id = uuid.uuid4()
trans_event1.transformation_id = "urn:epc:id:sgtin:40012847.077889.12"

qty_event.event_id = uuid.UUID("2b1a19c2-ee96-4f3a-82ef-6b662fdf9928").hex
qty_event.read_point = "urn:epc:id:sgln:Building_Pink_V4<"


#testing creating nodes for all events
def test_create_event_node():
    assert n.create_event_node(agg_event) == []
    assert n.create_event_node(qty_event) == []
    assert n.create_event_node(trans_event) == []
    assert n.create_event_node(trans_event1) == []
    assert n.create_event_node(tx_event) == []
    assert n.create_event_node(obj_event) == []
    
def create_company_node():
    assert n.create_company_node(company) == []

def test_create_location_node():
    assert n.create_location_node(location) == []

def test_create_location_date_node():
    assert n.create_location_date_node(location_date) == []

def test_create_user_node():
    assert n.create_user_node(user) == []

def test_item_instance_node():
    assert n.create_item_instance_node(item_instance) == []

def test_item_class_node():
    assert n.create_item_class_node(item_class) == []

def test_create_upload_relationship():
    relationship = n.create_upload_relationship(user, agg_event) 
    assert isinstance(relationship,list) and len(relationship) >=1

def test_create_epc_list_item_relationship(): 
    relationship = n.create_epc_list_item_relationship(item_class, agg_event)
    assert isinstance(relationship,list) and len(relationship) >=1

def test_create_epc_list_item_instance_relationship():
    relationship = n.create_epc_list_item_instance_relationship(item_instance,obj_event)
    assert isinstance(relationship,list) and len(relationship) >=1

def test_create_input_epc_list_relationship():
    relationship = n.create_input_epc_list_relationship(item_instance, trans_event)
    assert isinstance(relationship,list) and len(relationship) >=1

def test_create_parent_id_relationship():
    relationship = n.create_parent_id_relationship(item_instance, tx_event)
    assert isinstance(relationship,list) and len(relationship) >=1

def test_create_child_epc_relationship():
    relationship =n.create_child_epc_relationship(item_instance, agg_event)
    assert isinstance(relationship,list) and len(relationship) >=1

def test_create_output_epc_list_item_relationship():
    relationship = n.create_output_epc_list_item_relationship(item_class, trans_event)
    assert isinstance(relationship,list) and len(relationship) >=1

def test_create_shared_transformation_relationship():
    relationship = n.create_shared_transformation_relationship(trans_event, trans_event1)
    assert isinstance(relationship,list) and len(relationship) >=1

def test_create_quantity_list_item_relationship():
    relationship =n.create_quantity_list_item_relationship(item_class, tx_event)
    assert isinstance(relationship,list) and len(relationship) >=1

def test_create_quantity_list_item_relationship():
    relationship = n.create_quantity_list_item_relationship(item_class, obj_event)
    assert isinstance(relationship,list) and len(relationship) >=1

def test_create_child_quantity_list_item_relationship():
    relationship = n.create_child_quantity_list_item_relationship(item_class, agg_event)
    assert isinstance(relationship,list) and len(relationship) >=1

def test_create_input_quantity_list_item_relationship():
    relationship = n.create_input_quantity_list_item_relationship(item_class, trans_event)
    assert isinstance(relationship,list) and len(relationship) >=1

def test_create_output_quantity_list_item_relationship():
    relationship = n.create_output_quantity_list_item_relationship(item_class, trans_event)
    assert isinstance(relationship,list) and len(relationship) >=1

def test_create_epc_class_relationship():
    relationship = n.create_epc_class_relationship(item_class, qty_event)
    assert isinstance(relationship,list) and len(relationship) >=1


def test_create_date_relationship():
    relationship = n.create_date_relationship(location, location_date)
    assert isinstance(relationship,list) and len(relationship) >=1