import json
import epcis_event


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

    for attr in schema_doc['attr_key_mapping'].keys():
        setattr(epcis_event_obj, attr, schema_doc['attr_key_mapping'][attr])

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
        map_from_epcis(epcis_event_obj, event)

if __name__ == '__main__':
    main()

