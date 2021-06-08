import json
import epcis_event
import datetime

def type_check(value):
    if isinstance(value, datetime.datetime):
        return value.isoformat("T").replace("+00:00", "") + "Z"
    elif isinstance(value, datetime.date):
        return value.strftime("%Y-%m-%d")
    elif isinstance(value, datetime.time):
        return value.strftime("%H:%M:%S.%f")
    elif isinstance(value, dict):
        return value[id]
    elif isinstance(value, int) or isinstance(value, float) or isinstance(value, str):
        return value


def map_from_epcis(epcis_event_obj,epcis_json):
    """Map data from a data dictionary  to a class object instance's data attributes.

    Args:
        data: Any
            Event dictionary
        obj: Any
            The event object
    """
    epcis_event_list = []
    if epcis_json is None:
        return None

    with open('schema.json') as f:
        schema_doc = json.load(f)

    for attr in schema_doc['attr_key_mapping'].keys():
        if attr in epcis_json.keys():
            value = type_check(epcis_json[schema_doc['attr_key_mapping'][attr]])
            setattr(epcis_event_obj, attr, value)
            epcis_event_list.append(epcis_event_obj)
    return epcis_event_list

# driver code
def main():
    event_objects = []
    with open('GS1StandardExample1.json') as f:
        epcis_doc = json.load(f)
        if epcis_doc['isA'] != 'EPCISDocument':
            print('{} is an unsupported type'.format(epcis_doc['isA']))
            return
        events = epcis_doc['epcisBody']['eventList']

    for event in events:
        epcis_event_obj = epcis_event.EPCISEvent()
        event_objects = map_from_epcis(epcis_event_obj, event)

if __name__ == '__main__':
    main()

