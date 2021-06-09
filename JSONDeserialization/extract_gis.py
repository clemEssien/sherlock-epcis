import json
import epcis_event


def map_from_epcis(epcis_json, epcis_event_obj):
    """Map data from a data dictionary  to a class object instance's data attributes.

    Args:
        data: Any
            Event dictionary
        obj: Any
            The event object
    """
    if epcis_json is None:
        return None

    for attr in epcis_json.keys():
        setattr(epcis_event_obj, attr, epcis_json[attr])

    return epcis_event_obj

# driver code
def main():
    event_objects = []
    epcis_event_obj = epcis_event.EPCISEvent()
    with open('GS1StandardExample1.json') as f:
        epcis_doc = json.load(f)
        if epcis_doc['isA'] != 'EPCISDocument':
            print('{} is an unsupported type'.format(epcis_doc['isA']))
            return
        events = epcis_doc['epcisBody']['eventList']

    for event in events:
        event_obj = map_from_epcis(event, epcis_event_obj)
        event_objects.append(event_obj)

if __name__ == '__main__':
    main()

