from epcis_cte_transformation.cte import CTEBase
import os, sys
import datetime
import json
import pytest

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


def test_object_event():
    event = ObjectEvent()
    event.event_time = "2013-06-08T14:58:56.591+00:00"
    event.event_timezone_offset = "+02:00"
    event.read_point = URI("urn:epc:id:sgln:0614141.00777.0")
    event.epc_list = [URI("urn:epc:id:sgtin:4012345.011122.25")]
    event.quantity_list = [
        QuantityElement(URI("urn:epc:class:lgtin:4012345.012345.998877"), 200, "KGM")
    ]

    for epc_val in event.epc_list:
        epc = epc_val.value
    for qe in event.quantity_list:
        quantity = qe.quantity
        uom = qe.uom

    event_value_list = [
        "2013-06-08 16:58:56.591000+02:00",
        event.read_point.value,
        epc,
        quantity,
        uom,
    ]

    cte = CreationCTE.new_from_epcis(event)

    cte_value_list = [
        cte.creation_completion_date,
        cte.location_where_food_was_created,
        cte.traceability_product,
        cte.quantity,
        cte.uom,
    ]

    assert event_value_list == cte_value_list


def test_aggregation_event():
    event = AggregationEvent()
    event.event_time = "2013-06-08T14:58:56.591+00:00"
    event.event_timezone_offset = "+02:00"
    event.read_point = URI("urn:epc:id:sgln:0614141.00777.0")
    event.child_epc_list = [URI("urn:epc:id:sgtin:4012345.011122.25")]
    event.child_quantity_list = [
        QuantityElement(URI("urn:epc:class:lgtin:4012345.012345.998877"), 200, "KGM")
    ]

    for epc_val in event.child_epc_list:
        epc = epc_val.value
    for qe in event.child_quantity_list:
        quantity = qe.quantity
        uom = qe.uom

    event_value_list = [
        "2013-06-08 16:58:56.591000+02:00",
        event.read_point.value,
        epc,
        quantity,
        uom,
    ]

    cte = CreationCTE.new_from_epcis(event)

    cte_value_list = [
        cte.creation_completion_date,
        cte.location_where_food_was_created,
        cte.traceability_product,
        cte.quantity,
        cte.uom,
    ]

    assert event_value_list == cte_value_list


def test_transaction_event():
    event = TransactionEvent()
    event.event_time = "2013-06-08T14:58:56.591+00:00"
    event.event_timezone_offset = "+02:00"
    event.read_point = URI("urn:epc:id:sgln:0614141.00777.0")
    event.epc_list = [URI("urn:epc:id:sgtin:4012345.011122.25")]
    event.quantity_list = [
        QuantityElement(URI("urn:epc:class:lgtin:4012345.012345.998877"), 200, "KGM")
    ]

    for epc_val in event.epc_list:
        epc = epc_val.value
    for qe in event.quantity_list:
        quantity = qe.quantity
        uom = qe.uom

    event_value_list = [
        "2013-06-08 16:58:56.591000+02:00",
        event.read_point.value,
        epc,
        quantity,
        uom,
    ]

    cte = CreationCTE.new_from_epcis(event)

    cte_value_list = [
        cte.creation_completion_date,
        cte.location_where_food_was_created,
        cte.traceability_product,
        cte.quantity,
        cte.uom,
    ]

    assert event_value_list == cte_value_list


def test_transformation_event():
    event = TransformationEvent()
    event.event_time = "2013-06-08T14:58:56.591+00:00"
    event.event_timezone_offset = "+02:00"
    event.read_point = URI("urn:epc:id:sgln:0614141.00777.0")
    event.input_epc_list = [URI("urn:epc:id:sgtin:4012345.011122.25")]
    event.input_quantity_list = [
        QuantityElement(URI("urn:epc:class:lgtin:4012345.012345.998877"), 200, "KGM")
    ]

    for epc_val in event.input_epc_list:
        epc = epc_val.value
    for qe in event.input_quantity_list:
        quantity = qe.quantity
        uom = qe.uom

    event_value_list = [
        "2013-06-08 16:58:56.591000+02:00",
        event.read_point.value,
        epc,
        quantity,
        uom,
    ]

    cte = CreationCTE.new_from_epcis(event)

    cte_value_list = [
        cte.creation_completion_date,
        cte.location_where_food_was_created,
        cte.traceability_product,
        cte.quantity,
        cte.uom,
    ]

    assert event_value_list == cte_value_list


def test_common_event():
    event = CommonEvent()
    event.event_time = "2013-06-08T14:58:56.591+00:00"
    event.event_timezone_offset = "+02:00"
    event.read_point = URI("urn:epc:id:sgln:0614141.00777.0")
    cte = CreationCTE.new_from_epcis(event)

    event_value_list = [
        "2013-06-08 16:58:56.591000+02:00",
        event.read_point.value,
    ]
    cte_value_list = [
        cte.creation_completion_date,
        cte.location_where_food_was_created,
    ]

    assert event_value_list == cte_value_list
