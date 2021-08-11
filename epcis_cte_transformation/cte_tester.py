import os, sys

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from JSONDeserialization.epcis_event import (
    QuantityElement,
    QuantityEvent,
    URI,
    CommonEvent,
    AggregationEvent,
    EPCISEvent,
    ObjectEvent,
    TransactionEvent,
    TransformationEvent,
)
from creation_cte import CreationCTE

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
event.quantity_list = [
    QuantityElement(URI("urn:epc:class:lgtin:4012345.012345.998877"), 200, "KGM")
    # QuantityElement(URI("urn:epc:class:lgtin:4012345.012345.998877"), 200, "KGM"),
]
cte = CreationCTE.new_from_epcis(event)
filename = cte.output_xlsx()
