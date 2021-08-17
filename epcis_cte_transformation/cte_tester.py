#import pytest
import yaml
import json

import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from JSONDeserialization.epcis_event import (
    ObjectEvent,
    TransactionEvent,
    TransformationEvent,
    QuantityEvent,
    AggregationEvent,
    URI,
    QuantityElement,
)
from receiving_cte import ReceivingCTE

event = ObjectEvent()
# only need event time
event.event_time = "2013-06-08T14:58:56.591+00:00"
event.event_timezone_offset = "+02:00"
# need readpoint
event.read_point = URI("urn:epc:id:sgln:0614141.00777.0")
event.epc_list = [
    URI("urn:epc:id:sgtin:4012345.011122.25")
    # URI("urn:epc:id:sgtin:4012345.011122.25"),
]
event.source_list = [{ "type": URI("urn:epcglobal:cbv:sdt:possessing_party"), "source": URI("urn:epc:id:sgln:4012345.00001.0")}]
event.destination_list = [{ "type": URI("urn:epcglobal:cbv:sdt:owning_party"), "destination": URI("urn:epc:id:sgln:0614141.00001.0")}]
event.quantity_list = [
    QuantityElement(URI("urn:epc:class:lgtin:4012345.012345.998877"), 200, "KGM")
    # QuantityElement(URI("urn:epc:class:lgtin:4012345.012345.998877"), 200, "KGM"),
]
cte = ReceivingCTE.new_from_epcis(event)
print(cte.receipt_time)
print(str(cte.quantity_received[0]) + " " + cte.unit_of_measure[0])
print(cte.receiver_location_identifier)
print(cte.traceability_lot_code[0])
print(cte.traceability_product[0])
#filename = cte.output_xlsx()
