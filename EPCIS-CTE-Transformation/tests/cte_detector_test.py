import yaml

import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from cte_detector import CTEDetector

from JSONDeserialization.epcis_event import (
    ObjectEvent,
    TransformationEvent,
    AggregationEvent,
)

if __name__ == "__main__":
    with open("EPCIS-CTE-Transformation/cte_detect_config.yaml") as f:
        event_chars = yaml.safe_load(f)
    detector = CTEDetector(event_chars=event_chars)

    obj_event = ObjectEvent()
    obj_event.action = "OBSERVE"
    obj_event.business_step = "urn:epcglobal:cbv:bizstep:receiving"

    bins = detector.detect_cte(obj_event)
    print(bins)
