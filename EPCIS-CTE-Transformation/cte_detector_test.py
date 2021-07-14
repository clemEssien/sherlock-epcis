import json
import os, sys
from cte_detector import CTEDetector

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
from JSONDeserialization.epcis_event import (
    ObjectEvent,
    TransformationEvent,
    AggregationEvent,
)

if __name__ == "__main__":
    with open("EPCIS-CTE-Transformation/cbv_characteristics.json") as f:
        event_chars = json.load(f)
    detector = CTEDetector(event_chars=event_chars)

    obj_event = ObjectEvent()
    obj_event.action = "OBSERVE"
    obj_event.business_step = "urn:epcglobal:cbv:bizstep:receiving"

    bins = detector.detect_cte(obj_event)
    print(bins)
