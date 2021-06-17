import json
import datetime
from dateutil import tz, parser

from JSONDeserialization.src import epcis_event

DATA_DIR = '../data/'

def map_xml_to_dict(parent):
    """
    Recursive operation which returns a dictionary from
    XMLElementTree
    """
    xml_dict = {}
    if parent.items():xml_dict.update(dict(parent.items()))
    if parent.text:
        xml_dict[parent.tag] = (parent.text).replace('\n','').strip()
    if ('List' in parent):
        for item in parent:
            xml_dict[parent.tag] = item
    else:
        sublist = []
        for element in parent:
            sublist.append(map_xml_to_dict(element))
            xml_dict[parent.tag] = sublist

    return xml_dict


def read_uri(uri):
    """ method returns URI string from a URI"""
    if type(uri) == list:
        return uri[0]['id']
    return epcis_event.URI(uri)

def map_to_epcis_dict(epcis_dict):
    """method creates a new dictionary from a dictionary of attributes """
    epcis_xml_dict = {}
    for attr_keys in epcis_dict:
        for attr in attr_keys.keys():
            epcis_xml_dict[attr] = attr_keys[attr]
    return epcis_xml_dict

def is_primitive(value) -> bool:
    """
    Returns True if the type is a primitive value
    Primitive values include str, int, float, datetime, date, and time.
    """
    if isinstance(value, datetime.datetime):
        return True
    elif isinstance(value, datetime.date):
        return True
    elif isinstance(value, datetime.time):
        return True
    elif isinstance(value, int) or isinstance(value, float):
        return True
    elif isinstance(value, str):
        return True
    else:
        return False

def attr_type_check(instvar, data, attr):

    if isinstance(instvar, str):
        value = data

    if isinstance(instvar, epcis_event.URI):
        value = read_uri(data)

    elif isinstance(instvar, list):
        dict_out = {}
        arr = []
        for item in data:
            if is_primitive(item):
                arr.append(item)
            else:
                arr.append(data)
        dict_out= arr[0]
        value = dict_out

    elif isinstance(instvar, dict):
        dict_out = {}
        keys = data.keys()
        if len(keys):
            for key in keys:
                    dict_out[key] = data[key]
        value = dict_out

    elif isinstance(instvar, datetime.date):
        try:
            value = datetime.datetime.strptime(data, "%Y-%m-%d")
            value = datetime.date(value.year, value.month, value.day)
        except:
            value = data
    elif isinstance(instvar, datetime.datetime):
        utc = tz.tzutc()
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

def map_from_epcis(epcis_event_obj,epcis_json):
    """Map data from a data dictionary  to a class object instance's data attributes.
    Args:
        obj: Event object
        epcis_json: Event dictionary
    """
    if epcis_json is None:
        return None

    with open(DATA_DIR+'schema.json') as f:
        schema_doc = json.load(f)

    for attr in (epcis_event_obj.__dict__.keys()):
        attr = attr[1:]

        try:
            instvar = getattr(epcis_event_obj, attr)
            value = epcis_json[schema_doc['attr_key_mapping'][attr]]
            formated_value = attr_type_check(instvar, value, attr)
            setattr(epcis_event_obj, attr, formated_value)

        except Exception:
            pass

    epcis_json_keys = epcis_json.keys()
    schema_values = schema_doc["attr_key_mapping"].values()
    ext_keys = (set(epcis_json_keys) - set(schema_values))
    ext_dict = {}
    for k in ext_keys:
        ext_dict[k] = epcis_json[k]
    setattr(epcis_event_obj, 'extensions', ext_dict)

    print(epcis_event_obj)

    return epcis_event_obj
