from pathlib import Path
import sys

# Pylance doesn't love this, but it works.
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
from src import epcis_event

obj_event = epcis_event.ObjectEvent()
obj_event.event_time = "2005-04-03T20:33:31.116-06:00"
obj_event.event_timezone_offset = "-06:00"
obj_event.epc_list = (
    ["urn:epc:id:sgtin:0614141.107346.2017" "urn:epc:id:sgtin:0614141.107346.2018"],
)
obj_event.action = "OBSERVE"
obj_event.business_step = "urn:epcglobal:cbv:bizstep:shipping"
obj_event.disposition = "urn:epcglobal:cbv:disp:in_transit"
obj_event.read_point = "urn:epc:id:sgln:0614141.07346.1234"
obj_event.business_transaction_list = [
    {
        "type": "urn:epcglobal:cbv:btt:po",
        "bizTransaction": "http://transaction.acme.com/po/12345678",
    }
]
obj_event.extensions = {
    "example:myField": {
        "@xmlns:example": "http://ns.example.com/epcis",
        "#text": "Example of a vendor/user extension",
    }
}
obj_event.quantity_list = [
    {
        "epcClass": "urn:epc:class:lgtin:4012345.012345.998877",
        "quantity": 200,
        "uom": "KGM",
    }
]
obj_event.business_location = "urn:epc:id:sgln:0614141.00888.0"
obj_event.source_list = [
    {
        "type": "urn:epcglobal:cbv:sdt:possessing_party",
        "source": "urn:epc:id:sgln:4012345.00001.0",
    },
    {
        "type": "urn:epcglobal:cbv:sdt:location",
        "source": "urn:epc:id:sgln:4012345.00225.0",
    },
]
obj_event.destination_list = [
    {
        "type": "urn:epcglobal:cbv:sdt:owning_party",
        "destination": "urn:epc:id:sgln:0614141.00001.0",
    },
    {
        "type": "urn:epcglobal:cbv:sdt:location",
        "destination": "urn:epc:id:sgln:0614141.00777.0",
    },
]

print(obj_event)
