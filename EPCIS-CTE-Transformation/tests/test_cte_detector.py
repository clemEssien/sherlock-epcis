import pytest
import yaml
import json

import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from cte_detector import CTEDetector
from JSONDeserialization.epcis_event import (
    ObjectEvent,
    TransactionEvent,
    TransformationEvent,
    QuantityEvent,
    AggregationEvent,
)


def test_init():
    with open("EPCIS-CTE-Transformation/cte_detect_config.yaml") as f:
        event_characteristics = yaml.safe_load(f)
    detector = CTEDetector(event_characteristics=event_characteristics)
    assert detector.event_chars == event_characteristics


def test_import_yaml():
    detector = CTEDetector()
    detector.import_yaml_file("EPCIS-CTE-Transformation/cte_detect_config.yaml")
    with open("EPCIS-CTE-Transformation/cte_detect_config.yaml") as f:
        event_chars = yaml.safe_load(f)
    assert detector.event_chars == event_chars
    with pytest.raises(ValueError):
        detector.import_yaml_file("EPCIS-CTE-Transformation/tests/test_cte_detector.py")


def test_import_json():
    detector = CTEDetector()
    detector.import_json_file("EPCIS-CTE-Transformation/cte_detect_config.json")
    with open("EPCIS-CTE-Transformation/cte_detect_config.json") as f:
        event_chars = json.load(f)
    assert detector.event_chars == event_chars
    with pytest.raises(ValueError):
        detector.import_json_file("EPCIS-CTE-Transformation/tests/test_cte_detector.py")


def test_detect_cte_invalid_data_type():
    with open("EPCIS-CTE-Transformation/cte_detect_config.yaml") as f:
        event_chars = yaml.safe_load(f)
    detector = CTEDetector(event_characteristics=event_chars)
    with pytest.raises(TypeError):
        detector.detect_cte(42)


@pytest.mark.parametrize(
    "event_class, action, business_step, cte",
    [
        ("ObjectEvent", "ADD", "commissioning", "growing"),
        ("TransformationEvent", "ADD", "commissioning", "transformation"),
        ("AggregationEvent", "DELETE", "unpacking", "transformation"),
        ("ObjectEvent", "OBSERVE", "shipping", "shipping"),
        ("ObjectEvent", "OBSERVE", "receiving", "receiving"),
        ("ObjectEvent", "ADD", "commission", "growing"),
        ("TransformationEvent", "ADD", "commissioned", "transformation"),
        ("ObjectEvent", "OBSERVE", "shipment", "shipping"),
        ("ObjectEvent", "OBSERVE", "receive", "receiving"),
        ("ObjectEvent", "ADD", "urn:epcglobal:cbv:bizstep:commissioning", "growing"),
        (
            "TransformationEvent",
            "ADD",
            "urn:epcglobal:cbv:bizstep:commissioning",
            "transformation",
        ),
        (
            "AggregationEvent",
            "DELETE",
            "urn:epcglobal:cbv:bizstep:unpacking",
            "transformation",
        ),
        ("ObjectEvent", "OBSERVE", "urn:epcglobal:cbv:bizstep:shipping", "shipping"),
        ("ObjectEvent", "OBSERVE", "urn:epcglobal:cbv:bizstep:receiving", "receiving"),
        ("ObjectEvent", "ADD", "urn:epcglobal:cbv:bizstep:commission", "growing"),
        (
            "TransformationEvent",
            "ADD",
            "urn:epcglobal:cbv:bizstep:commissioned",
            "transformation",
        ),
        ("ObjectEvent", "OBSERVE", "urn:epcglobal:cbv:bizstep:shipment", "shipping"),
        ("ObjectEvent", "OBSERVE", "urn:epcglobal:cbv:bizstep:receive", "receiving"),
    ],
)
def test_detect_cte(event_class, action, business_step, cte):
    with open("EPCIS-CTE-Transformation/cte_detect_config.yaml") as f:
        event_chars = yaml.safe_load(f)
    detector = CTEDetector(event_characteristics=event_chars)

    event = globals()[event_class]()
    event.action = action
    event.business_step = business_step

    assert detector.detect_cte(event) == cte


def test_detect_cte_partially_empty_Event():
    with open("EPCIS-CTE-Transformation/cte_detect_config.yaml") as f:
        event_chars = yaml.safe_load(f)
    detector = CTEDetector(event_characteristics=event_chars)

    event = ObjectEvent()
    event.business_step = "ship"

    assert detector.detect_cte(event) == "shipping"
