import json
import os , sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import epcis_event as epc 
import extract_gis_from_json as ex

DATA_DIR = "./data/"

# driver code
event_types = {
    "ObjectEvent": epc.ObjectEvent(),
    "AggregationEvent": epc.AggregationEvent(),
    "QuantityEvent": epc.QuantityEvent(),
    "TransactionEvent": epc.TransactionEvent(),
    "TransformationEvent": epc.TransformationEvent(),
}

with open(DATA_DIR+'GS1StandardExample1.json') as f:
    epcis_doc = json.load(f)
    if epcis_doc['isA'] != 'EPCISDocument':
        print('{} is an unsupported type'.format(epcis_doc['isA']))
    events = epcis_doc['epcisBody']['eventList']

for event in events:
    event_type = (event['isA'])
    epcis_event_obj = event_types[event_type]
    print(ex.map_from_epcis(epcis_event_obj, event))


