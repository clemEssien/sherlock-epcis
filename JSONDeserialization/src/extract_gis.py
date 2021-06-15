import json
import epcis_event
import datetime


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

def attr_type_check(instvar, data, attr):
    if isinstance(instvar, str):
        value = data
    if isinstance(instvar, list):
        value = data
        arr_out = []

        for val in data:
            if is_primitive(val):
                arr_out.append(val)
            else:
                arr_out.append(str(val))
        return arr_out

    if isinstance(instvar, epcis_event.URI):
        value = read_uri(data)

    elif isinstance(instvar, dict):
        print('dict')
        a = 1
        dict_out = {}
        keys = data.keys()
        print(keys)
        if len(keys):
            for key in keys:
                if is_primitive(key):
                    dict_out[key] = data
                else:
                    dict_out[key] = str(data)

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

    with open('schema.json') as f:
        schema_doc = json.load(f)

    for attr in list(epcis_event_obj.__dict__.keys()):
        attr = attr[1:]

        try:

            instvar = getattr(epcis_event_obj, attr)
            value = epcis_json[schema_doc['attr_key_mapping'][attr]]
            formated_value = attr_type_check(instvar, value, attr)
            #default_value = type_check(epcis_json[schema_doc['attr_key_mapping'][attr]])
            # print(attr,formated_value)
            setattr(epcis_event_obj, attr, formated_value)

        except Exception as e:
            a = 1
            # print("error: ",attr, e)

    epcis_json_keys = epcis_json.keys()
    schema_values = schema_doc["attr_key_mapping"].values()
    ext_keys = (set(epcis_json_keys) - set(schema_values))
    ext_dict = {}
    for k in ext_keys:
        ext_dict[k] = epcis_json[k]
    epcis_event_obj.extensions.append(ext_dict)

    #search for keys in epcis_json but not in schema doc and set in the extension



    print(epcis_event_obj)
    print("**************")




# driver code
def main():
    event_types = {
        "ObjectEvent": epcis_event.ObjectEvent(),
        "AggregationEvent": epcis_event.AggregationEvent(),
        "QuantityEvent": epcis_event.QuantityEvent(),
        "TransactionEvent": epcis_event.TransactionEvent(),
        "TransformationEvent": epcis_event.TransformationEvent(),
    }

    with open('GS1StandardExample1.json') as f:
        epcis_doc = json.load(f)
        if epcis_doc['isA'] != 'EPCISDocument':
            print('{} is an unsupported type'.format(epcis_doc['isA']))
            return
        events = epcis_doc['epcisBody']['eventList']

    for event in events:
        event_type = (event['isA'])
        epcis_event_obj = event_types[event_type]
        map_from_epcis(epcis_event_obj, event)

if __name__ == '__main__':
    main()

