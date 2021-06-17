import json
from JSONDeserialization.src import epcis_event
from JSONDeserialization.src.extract_gis_from_json import map_from_epcis

DATA_DIR = '../data/'

# driver code
event_types = {
    "ObjectEvent": epcis_event.ObjectEvent(),
    "AggregationEvent": epcis_event.AggregationEvent(),
    "QuantityEvent": epcis_event.QuantityEvent(),
    "TransactionEvent": epcis_event.TransactionEvent(),
    "TransformationEvent": epcis_event.TransformationEvent(),
}

with open(DATA_DIR+'GS1StandardExample1.json') as f:
    epcis_doc = json.load(f)
    if epcis_doc['isA'] != 'EPCISDocument':
        print('{} is an unsupported type'.format(epcis_doc['isA']))
    events = epcis_doc['epcisBody']['eventList']

for event in events:
    event_type = (event['isA'])
    epcis_event_obj = event_types[event_type]
    map_from_epcis(epcis_event_obj, event)


