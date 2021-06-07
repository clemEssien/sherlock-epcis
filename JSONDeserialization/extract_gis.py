import datetime
import json
from uuid import UUID
import epcis_event


def map_from_epcis(data, obj):
    """Map data from a data dictionary  to a class object instance's data attributes.

    Args:
        data: Any
            Json Map file
        obj: Any
            The class object to load the data in to
    """
    if data is None:
        return None

    epcis_json = data["attr_key_mapping"]

    for attr in epcis_json.keys():
        setattr(obj, attr, epcis_json[attr])
    return obj

# driver example
def main():
    events = []
    event_objects = []
    with open('JSONDeserialization/GS1StandardExample1.json') as f:
        epcis_doc = json.load(f)
        if epcis_doc['isA'] != 'EPCISDocument':
            print('{} is an unsupported type'.format(epcis_doc['isA']))
            return
        events = epcis_doc['epcisBody']['eventList']

    for event_data in events:
        event_obj = epcis_event.EPCISEvent()
        map_from_epcis(event_data, event_obj)
        event_objects.append(event_obj)

    for event in event_objects:
        print(event)
        print("")

if __name__ == '__main__':
    main()

