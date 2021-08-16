import uuid
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import crud_ops as c
import nodes as n

from JSONDeserialization import epcis_event as epc

obj_event = epc.ObjectEvent()
agg_event = epc.AggregationEvent()
tx_event = epc.TransactionEvent()
trans_event = epc.TransformationEvent()
trans_event1 = epc.TransformationEvent()
qty_event = epc.QuantityEvent()

obj_event.event_id = uuid.UUID("14ab0519-c147-43c6-a6ea-9bd21c259752").hex
obj_event._read_point = "urn:epc:id:sgln:0012345.11111.400"

obj_event.name = "ObjectEvent"
obj_event._epc_list = ["urn:epc:id:sgtin:0614141.107346.2017","urn:epc:id:sgtin:0614141.107346.2018"]
obj_event._action = "OBSERVE"
obj_event._event_time = "2005-07-11T11:30:47-04:00"
obj_event._event_timezone_offset = "-04:00"
obj_event._extensions = [{"foo": "bar"}, {"bucky": "beaver"}]

agg_event._event_id = uuid.UUID("a2624953-f2e6-4369-8e71-9ee1a19d81d5")
agg_event._read_point = "urn:epc:id:sgln:0614141.00777.0"
agg_event._parent_id =  "urn:epc:id:sgln:5566661.00777.0"
agg_event._name="AggregationEvent"

node = c.Node(obj_event)
n.create_event_node(obj_event)
n.create_event_node(agg_event)
n.create_event_node(qty_event)

def test_retrieve_node_properties():
    result = node.retrieve_node_properties()
    assert result['event_id'] == str(obj_event.event_id)

def test_retrieve_node_by_id():
    result = node.retrieve_node_by_event_id()
    assert str(result.event_id) == str(obj_event.event_id)

def test_create_relationship():
    relationship = "NEXT"
    result = node.create_relationship(agg_event, relationship, ['next'])
    assert (result[0].data()['a.name'] == obj_event.name)

def test_remove_node_property():
    result = node.remove_node_property('epc_list')
    assert ("epc_list" not in result[0].data()['m'].keys())

def test_update_node():
    obj_event._epc_list = ["urn:epc:id:sgtin:0614141.107346.2017","urn:epc:id:sgtin:0614141.107346.2018"]
    result = node.update_node()
    assert("epc_list" in result[0].data()['m'].keys())

def test_delete_node():
    result = node.delete_node()
    assert(result == [])

