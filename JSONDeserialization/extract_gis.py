import json
import epcis_event
import datetime

def type_check(value):
    if isinstance(value, datetime.datetime):
        try:
            return value.isoformat("T").replace("+00:00", "") + "Z"
        except:
            print("Attribute ",value," not converted to iso format")
        finally:
            return value
    elif isinstance(value, datetime.date):
        return value.strftime("%Y-%m-%d")
    elif isinstance(value, datetime.time):
        return value.strftime("%H:%M:%S.%f")
    elif isinstance(value, dict):
        return value["id"]
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
    if epcis_json is None:
        return None

    with open('schema.json') as f:
        schema_doc = json.load(f)

    for attr in epcis_event_obj.__dict__.keys():
        if attr in schema_doc['attr_key_mapping'].keys():
            try:
                instvar = getattr(epcis_event_obj, attr)
                value = type_check(epcis_json[schema_doc['attr_key_mapping'][attr]])
                setattr(epcis_event_obj, attr, value)
            except:
                a = 3
                # print(attr)
    print(epcis_event_obj)




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

