import json
import datetime
import inspect
from JSONDeserialization.src import epcis_event

DATA_DIR = '../data/'

def read_uri(uri):
    if type(uri) == dict:
        return uri['id']
    return epcis_event.URI(uri)

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

def attr_type_check(instvar, data):
    if isinstance(instvar, str):
        value = data
    if isinstance(instvar, list):
        arr_out = []
        for val in data:
                arr_out.append(val)
        return arr_out

    if isinstance(instvar, epcis_event.URI):
        value = read_uri(data)

    elif isinstance(instvar, dict):
        dict_out = {}
        keys = data.keys()
        if len(keys):
            for key in keys:
                    dict_out[key] = data[key]
        return dict_out

    elif isinstance(instvar, datetime.date):
        try:
            value = datetime.datetime.strptime(data, "%Y-%m-%d")
            value = datetime.date(value.year, value.month, value.day)
        except:
            value = data
    elif isinstance(instvar, datetime.datetime):
        try:
            value = datetime.date.fromisoformat(data)
        except:
            value = data
    elif isinstance(instvar, datetime.timezone):
        value = data
    return value


def map_from_epcis(epcis_event_obj,epcis_json):
    """Map data from a data dictionary  to a class object instance's data attributes.

    Args:
        data: Any
            Event dictionary
        obj: Any
            The event object
    """
    if epcis_json is None:
        return None

    with open(DATA_DIR+'/schema.json') as f:
        schema_doc = json.load(f)

    for attr in list(epcis_event_obj.__dict__.keys()):
        attr = attr[1:]

        try:
            instvar = getattr(epcis_event_obj, attr)
            value = epcis_json[schema_doc['attr_key_mapping'][attr]]
            formated_value = attr_type_check(instvar, value)
            setattr(epcis_event_obj, attr, formated_value)

        except Exception as e:
            pass

    epcis_json_keys = epcis_json.keys()
    schema_values = schema_doc["attr_key_mapping"].values()
    ext_keys = (set(epcis_json_keys) - set(schema_values))
    ext_dict = {}
    for k in ext_keys:
        ext_dict[k] = epcis_json[k]
    epcis_event_obj.extensions.append(ext_dict)

    return epcis_event_obj



