import xml.etree.ElementTree as ET
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from extract_gis_from_xml import map_xml_to_dict
from extract_gis_from_xml import map_from_epcis
from extract_gis_from_xml import  map_to_epcis_dict
from extract_gis_from_xml import map_xml_to_dict
from JSONDeserialization import epcis_event as js

DATA_DIR = "./data/"

def find_event_from_xml(xml_element_tree, event_types):
    for event in event_types:
        if xml_element_tree.find(event):
            return event

def main():
    a = 1
    event_types = {
        "ObjectEvent": js.ObjectEvent(),
        "CommonEvent":js.CommonEvent(),
        "AggregationEvent": js.AggregationEvent(),
        "QuantityEvent": js.QuantityEvent(),
        "TransactionEvent": js.TransactionEvent(),
        "TransformationEvent": js.TransformationEvent(),
    }
#
    with open(DATA_DIR+'GS1StandardExample3.xml', 'r') as f:
           tree = ET.parse(f)
           root = tree.getroot()

           if root.tag != "{urn:epcglobal:epcis:xsd:1}EPCISDocument":  # Check for the EPCISDocument tag
               print("Not EPCISDocument")
               return

           for child in root:
               for event_list in child:
                   if len(event_list):
                       for event in event_list:
                           if event:
                               d = map_xml_to_dict(event)
                               try:
                                   xml_doc = d[event.tag]
                                   epcis_event_obj = event_types[event.tag]
                               except Exception:
                                    events = event_types.keys()
                                    event_from_xml = find_event_from_xml(event, event_types)
                                    epcis_event_obj = event_types[event_from_xml]
                                    pass

                               xml_dict = map_to_epcis_dict(xml_doc)
                               print(map_from_epcis(epcis_event_obj, xml_dict))
                   else:
                       print("No Events detected in this document")

if __name__ == '__main__' :
    main()