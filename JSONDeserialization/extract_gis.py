import datetime
import json
from uuid import UUID


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
    with open('GS1StandardExample1.json') as f:
        epcis_doc = json.load(f)
        if epcis_doc['isA'] != 'EPCISDocument':
            print('{} is an unsupported type'.format(epcis_doc['isA']))
            return
        events = epcis_doc['epcisBody']['eventList']

    for event in events:
        temp_event = EPCISEvent(event)
        event_objects.append(temp_event)

    pp = pprint.PrettyPrinter(indent=2)
    for event in event_objects:
        pp.pprint(event.__dict__)
        print("")

if __name__ == '__main__':
    main()

