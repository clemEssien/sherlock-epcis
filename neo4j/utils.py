import json
import datetime
from dateutil import tz, parser
import os
import sys
import uuid

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from JSONDeserialization import extract_gis_from_json as gis
from JSONDeserialization import epcis_event as epc


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

def verify_algo_args(sample_size, seed):
    if isinstance(sample_size, int) and isinstance(seed, int):
            if sample_size >0 and seed >=0:
                return True;
    return False  

def algorithm_response(response):
    result = {}
    if response and len(response) >1:
        for record in response:
            result[record['name']] = record['score']    
    return result

def format_attr_dict(attr_dict):
    attr_dict = attr_dict.split()
    new_attr_dict = ""
    for item in attr_dict:
        if '":' in item:
            new_attr_dict += item.replace('"', ' ')
        elif '[]' in item:
            new_attr_dict += item.replace('[]', '\"\"')
        else:
            new_attr_dict += item
    return new_attr_dict

def retrive_attr_dict_from_event(event):
    attributes = {}
    for attr in list(event.__dict__):
        instvar = getattr(event, attr)
        if isinstance(instvar, dict):
            attributes[attr[1:]] = json.dumps(getattr(event, attr))
        elif isinstance(instvar, list):
            for item in instvar:
                if gis.is_primitive(item):
                    attributes[attr[1:]]  = getattr(event, attr)
                else:
                    attributes[attr[1:]] = str(getattr(event, attr))              
        else:
            attributes[attr[1:]] = getattr(event, attr)
        attributes["name"] = event.__class__.__name__ 
    return attributes


def attr_type_check(instvar, data):
    value = ""

    if isinstance(instvar, uuid.UUID):
        value = uuid.UUID(data)

    if isinstance(instvar, str):
        value = data

    if isinstance(instvar, list):
        dict_out = {}
        arr = []
        if '{' in data:
            dict_out = json.loads(data)
            for item in dict_out:
                arr.append(item)
            value =  dict_out
        else:
            for item in data:
                if gis.is_primitive(item):
                    arr.append(item)
                else:
                    arr.append(item)
            dict_out = arr
            value = dict_out

    if isinstance(instvar, epc.URI):
        value = gis.read_uri(data)

    elif isinstance(instvar, dict):
        dict_out = {}
        if (data):
            dict_out = json.loads(data)
        value = dict_out

    elif isinstance(instvar, datetime.date):
        try:
            value = data
        except Exception as e:
            value = data
    elif isinstance(instvar, datetime.datetime):
        utc = tz.tzutc()
        data = data.replace("Z", "+00:00")
        try:
            value = data.astimezone(utc)
        except:
            try:
                value = parser.parse(value)
            except:
                pass
    elif isinstance(instvar, datetime.timezone):
        value = data
    return value

event_types = {
    "ObjectEvent": epc.ObjectEvent,
    "AggregationEvent": epc.AggregationEvent,
    "QuantityEvent": epc.QuantityEvent,
    "TransactionEvent": epc.TransactionEvent,
    "TransformationEvent": epc.TransformationEvent,
}
