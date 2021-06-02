# Author: Ryan Oostland
# Last Modified: June 1, 2021
# Script to deserialize standard EPCIS documents.
# GS1StandardExample1-4 from https://www.mimasu.nl/epcis/xmljson
from abc import ABC, abstractmethod
import json
# EPCISEvent attributes can be added or removed dependingon what data we plan on keeping
class EPCISEvent(ABC):
    def __init__(self, event_dict):
        self.event_type = event_dict['isA']
        self.event_time = event_dict['eventTime']
        self.event_time_offset = event_dict['eventTimeZoneOffset']
        if 'epcList' in event_dict:
            self.epc_list = event_dict['epcList']
        if 'parentID' in event_dict:
            self.parent_id = event_dict['parentID']
        if 'childEPCs' in event_dict:
            self.child_epc_list = event_dict['childEPCs']
        if 'inputEpcList' in event_dict:
            self.input_epc_list = event_dict['inputEpcList']
        if 'outputEpcList' in event_dict:
            self.output_epc_list = event_dict['outputEpcList']
        if 'xformID' in event_dict:
            self.xform_id = event_dict['xformID']
        # according to the EPCIS 1.2 standard all events should have an action,
        # but some of the sample documents do not.
        if 'action' in event_dict:
            self.action = event_dict['action']
        if 'bizStep' in event_dict:
            self.business_step = event_dict['bizStep']
        if 'disposition' in event_dict:
            self.disposition = event_dict['disposition']
        if 'readPoint' in event_dict:
            self.read_point = event_dict['readPoint']['id']
        if 'bizLocation' in event_dict:
            self.business_location = event_dict['bizLocation']['id']
        if 'ilmd' in event_dict:
            self.instance_lot_master_data = event_dict['ilmd']
        if 'quantityList' in event_dict:
            self.quantity_list = event_dict['quantityList']
        if 'childQuantityList' in event_dict:
            self.child_quantity_list = event_dict['childQuantityList']
        if 'inputQuantityList' in event_dict:
            self.input_quantity_list = event_dict['inputQuantityList']
        if 'outputQuantityList' in event_dict:
            self.output_quantity_list = event_dict['outputQuantityList']
        if 'bizTransactionList' in event_dict:
            self.business_transaction_list = event_dict['bizTransactionList']
        elif self.event_type == 'TransactionEvent':
            raise ValueError('Transaction Events must have a bizTransactionList')
        if 'sourceList' in event_dict:
            self.source_list = event_dict['sourceList']
        if 'destinationList' in event_dict:
            self.destination_list = event_dict['destinationList']
        
        


def deserializeStandardEPCIS(input_file):
    events = []
    event_objects = []
    with open(input_file) as f:
        epcis_doc = json.load(f)
        if epcis_doc['isA'] != 'EPCISDocument':
            print('{} is an unsupported type'.format(epcis_doc['isA']))
            return
        events = epcis_doc['epcisBody']['eventList']
    for event in events:
        temp_event = EPCISEvent(event)
        event_objects.append(temp_event)

    return event_objects

# print events for proof-of-concept
def main():
    serial_events = deserializeStandardEPCIS('JSONDeserialization/GS1StandardExample4.json')
    for event in serial_events:
        print(event.__dict__)
        print("")

if __name__ == '__main__':
    main()


