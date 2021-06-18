import requests

BASE = "http://127.0.0.1:5000/"

mydata = {
    "isA": "ObjectEvent",
    "eventTime": "2005-04-03T20:33:31.116-06:00",
    "eventTimeZoneOffset": "-06:00",
    "epcList": [
        "urn:epc:id:sgtin:0614141.107346.2017",
        "urn:epc:id:sgtin:0614141.107346.2018",
    ],
    "action": "OBSERVE",
    "bizStep": "urn:epcglobal:cbv:bizstep:shipping",
    "disposition": "urn:epcglobal:cbv:disp:in_transit",
    "readPoint": {"id": "urn:epc:id:sgln:0614141.07346.1234"},
    "bizTransactionList": [
        {
            "type": "urn:epcglobal:cbv:btt:po",
            "bizTransaction": "http://transaction.acme.com/po/12345678",
        }
    ],
}

response = requests.post(BASE + "events/", json=mydata)
print(response)
