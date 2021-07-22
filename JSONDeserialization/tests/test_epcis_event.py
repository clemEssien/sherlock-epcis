from _pytest.python import pytest_pycollect_makeitem
from _pytest.python_api import raises
import pytest
from uuid import uuid4
from datetime import datetime, timezone, timedelta
from dateutil import tz

import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from epcis_event import (
    EPCISEvent,
    CommonEvent,
    ObjectEvent,
    URI,
    TransactionEvent,
    TransformationEvent,
    AggregationEvent,
    QuantityElement,
    QuantityEvent,
)


class TestEPCISEvent:
    def test_event_id_set_uuid(self):
        event = EPCISEvent()
        e_id = uuid4()
        event.event_id = e_id
        assert event.event_id == e_id

    def test_event_id_set_uuid_string(self):
        event = EPCISEvent()
        e_id = uuid4()
        event.event_id = str(e_id)
        assert event.event_id == e_id

    def test_event_id_set_incorrect_string(self):
        event = EPCISEvent()
        with pytest.raises(TypeError):
            event.event_id = "foo"

    def test_event_id_set_incorrect_type(self):
        event = EPCISEvent()
        with pytest.raises(TypeError):
            event.event_id = 42

    def test_event_time_set_datetime(self):
        event = EPCISEvent()
        e_time = datetime(2021, 7, 19, 3, 30, 0, tzinfo=tz.tzutc())
        event.event_time = e_time
        assert event.event_time == e_time

    def test_event_time_set_datetime_str(self):
        event = EPCISEvent()
        e_time = datetime(2021, 7, 19, 3, 30, 0, tzinfo=tz.tzutc())
        event.event_time = str(e_time)
        assert event.event_time == e_time

    def test_event_time_set_incorrect_str(self):
        event = EPCISEvent()
        with pytest.raises(TypeError):
            event.event_time = "foo"

    def test_event_time_set_incorrect_type(self):
        event = EPCISEvent()
        with pytest.raises(TypeError):
            event.event_time = 42

    def test_timezone_offset_set_timezone(self):
        event = EPCISEvent()
        offset = timezone(timedelta(hours=-4))
        event.event_timezone_offset = offset
        assert event.event_timezone_offset == offset

    def test_timezone_offset_set_number(self):
        event = EPCISEvent()
        offset = timezone(timedelta(hours=-4))
        event.event_timezone_offset = -4
        assert event.event_timezone_offset == offset
        event.event_timezone_offset = -4.0
        assert event.event_timezone_offset == offset

    def test_timezone_offset_set_incorrect_number(self):
        event = EPCISEvent()
        with pytest.raises(TypeError):
            event.event_timezone_offset = -24
            event.event_timezone_offset = -24.0
            event.event_timezone_offset = 24
            event.event_timezone_offset = 24.0

    def test_timezone_offset_set_str(self):
        event = EPCISEvent()
        offset = timezone(timedelta(hours=-4))
        event.event_timezone_offset = "-04:00"
        assert event.event_timezone_offset == offset

    def test_timezone_offset_set_incorrect_str(self):
        event = EPCISEvent()
        with pytest.raises(TypeError):
            event.event_timezone_offset = "foo"

    def test_local_event_time(self):
        event = EPCISEvent()
        event.event_time = "2005-07-11T11:30:47-04:00"
        event.event_timezone_offset = "-04:00"
        assert event.event_time_local == datetime.fromisoformat(
            "2005-07-11T11:30:47-04:00"
        )

    def test_extensions_set_dict(self):
        event = EPCISEvent()
        event.extensions = {"foo": "bar"}
        event.extensions = {"bucky": "beaver"}
        assert event.extensions == [{"foo": "bar"}, {"bucky": "beaver"}]

    def test_extensions_set_incorrect_type(self):
        event = EPCISEvent()
        with pytest.raises(TypeError):
            event.extensions = "foo"

    def test_delete_extensions(self):
        event = EPCISEvent()
        event.extensions = {"foo": "bar"}
        event.extensions = {"bucky": "beaver"}
        event.delete_extensions()
        assert event.extensions == []


class TestCommonEvent:
    def test_action(self):
        event = CommonEvent()
        event.action = "ADD"
        assert event.action == "ADD"
        with pytest.raises(TypeError):
            event.action = 7

    @pytest.mark.parametrize(
        "prop, string, uri",
        [
            ("business_step", "foo", URI("foo")),
            ("disposition", "foo", URI("foo")),
            ("read_point", "foo", URI("foo")),
            ("business_location", "foo", URI("foo")),
        ],
    )
    def test_URI_properties(self, prop, string, uri):
        event = CommonEvent()
        setattr(event, prop, string)
        assert getattr(event, prop).uri_str == uri.uri_str
        setattr(event, prop, uri)
        assert getattr(event, prop).uri_str == uri.uri_str
        with pytest.raises(TypeError):
            setattr(event, prop, 42)

    @pytest.mark.parametrize(
        "prop, input",
        [
            ("business_transaction_list", [{"foo": "bar"}]),
            ("source_list", [{"foo": "bar"}]),
            ("destination_list", [{"foo": "bar"}]),
        ],
    )
    def test_dict_list_properties(self, prop, input):
        event = CommonEvent()
        setattr(event, prop, input)
        assert getattr(event, prop) == input
        setattr(event, prop, [])
        assert getattr(event, prop) == []
        with pytest.raises(TypeError):
            setattr(event, prop, [42])
            setattr(event, prop, 42)


class TestObjectEvent:
    def test_epc_list(self):
        event = ObjectEvent()
        event.epc_list = []
        assert event.epc_list == []
        uri = URI("foo")
        event.epc_list = [uri]
        assert event.epc_list == [uri]
        event.epc_list = ["foo"]
        assert event.epc_list == [uri]
        with pytest.raises(TypeError):
            event.epc_list = uri

    def test_quantity_list(self):
        event = ObjectEvent()
        event.quantity_list = []
        assert event.quantity_list == []
        event.quantity_list = [{"epcClass": "foo"}]
        qe = QuantityElement(URI("foo"))
        assert event.quantity_list == [qe]
        event.quantity_list = [qe]
        assert event.quantity_list == [qe]
        with pytest.raises(TypeError):
            event.quantity_list = "foo"
            event.quantity_list = ["bar"]

    def test_ilmd(self):
        event = ObjectEvent()
        event.instance_lot_master_data = {"foo": "bar"}
        assert event.instance_lot_master_data == {"foo": "bar"}
        with pytest.raises(TypeError):
            event.instance_lot_master_data = "foobar"


class TestAggregationEvent:
    def test_parent_id(self):
        event = AggregationEvent()
        event.parent_id = "foo"
        uri = URI("foo")
        assert event.parent_id == uri
        event.parent_id = uri
        assert event.parent_id == uri
        with pytest.raises(TypeError):
            event.parent_id = 42

    def test_child_epc_list(self):
        event = AggregationEvent()
        event.child_epc_list = []
        assert event.child_epc_list == []
        uri = URI("foo")
        event.child_epc_list = [uri]
        assert event.child_epc_list == [uri]
        event.child_epc_list = ["foo"]
        assert event.child_epc_list == [uri]
        with pytest.raises(TypeError):
            event.child_epc_list = uri

    def test_child_quantity_list(self):
        event = AggregationEvent()
        event.child_quantity_list = []
        assert event.child_quantity_list == []
        event.child_quantity_list = [{"epcClass": "foo"}]
        qe = QuantityElement(URI("foo"))
        assert event.child_quantity_list == [qe]
        event.child_quantity_list = [qe]
        assert event.child_quantity_list == [qe]
        with pytest.raises(TypeError):
            event.child_quantity_list = "foo"
            event.child_quantity_list = ["bar"]


class TestQuantityEvent:
    @pytest.mark.parametrize(
        "prop, string, uri",
        [
            ("epc_class", "foo", URI("foo")),
            ("business_step", "foo", URI("foo")),
            ("disposition", "foo", URI("foo")),
            ("read_point", "foo", URI("foo")),
            ("business_location", "foo", URI("foo")),
        ],
    )
    def test_URI_properties(self, prop, string, uri):
        event = QuantityEvent()
        setattr(event, prop, string)
        assert getattr(event, prop).uri_str == uri.uri_str
        setattr(event, prop, uri)
        assert getattr(event, prop).uri_str == uri.uri_str
        with pytest.raises(TypeError):
            setattr(event, prop, 42)

    def test_business_transaction_list(self):
        event = QuantityEvent()
        event.business_transaction_list = [{"foo": "bar"}]
        assert event.business_transaction_list == [{"foo": "bar"}]
        event.business_transaction_list = []
        assert event.business_transaction_list == []
        with pytest.raises(TypeError):
            event.business_transaction_list = [42]
            event.business_transaction_list = 42

    def test_quantity(self):
        event = QuantityEvent()
        event.quantity = 42
        assert event.quantity == 42.0
        event.quantity = 42.0
        assert event.quantity == 42.0
        event.quantity = "42.0"
        assert event.quantity == 42.0
        with pytest.raises(TypeError):
            event.quantity = "foo"


class TestTransactionEvent:
    def test_parent_id(self):
        event = TransactionEvent()
        event.parent_id = "foo"
        uri = URI("foo")
        assert event.parent_id == uri
        event.parent_id = uri
        assert event.parent_id == uri
        with pytest.raises(TypeError):
            event.parent_id = 42

    def test_epc_list(self):
        event = TransactionEvent()
        event.epc_list = []
        assert event.epc_list == []
        uri = URI("foo")
        event.epc_list = [uri]
        assert event.epc_list == [uri]
        event.epc_list = ["foo"]
        assert event.epc_list == [uri]
        with pytest.raises(TypeError):
            event.epc_list = uri

    def test_quantity_list(self):
        event = TransactionEvent()
        event.quantity_list = []
        assert event.quantity_list == []
        event.quantity_list = [{"epcClass": "foo"}]
        qe = QuantityElement(URI("foo"))
        assert event.quantity_list == [qe]
        event.quantity_list = [qe]
        assert event.quantity_list == [qe]
        with pytest.raises(TypeError):
            event.quantity_list = "foo"
            event.quantity_list = ["bar"]


class TestTransformationEvent:
    @pytest.mark.parametrize("prop", ["input_epc_list", "output_epc_list"])
    def test_list_URI_properties(self, prop):
        event = TransformationEvent()
        setattr(event, prop, ["foo"])
        uri = URI("foo")
        assert getattr(event, prop) == [uri]
        setattr(event, prop, [uri])
        assert getattr(event, prop) == [uri]
        with pytest.raises(TypeError):
            setattr(event, prop, "foo")
            setattr(event, prop, [42])

    @pytest.mark.parametrize("prop", ["input_quantity_list", "output_quantity_list"])
    def test_list_quantity_element_properties(self, prop):
        event = TransformationEvent()
        setattr(event, prop, [{"epcClass": "foo"}])
        qe = QuantityElement(epc="foo")
        assert getattr(event, prop) == [qe]
        setattr(event, prop, [qe])
        assert getattr(event, prop) == [qe]
        with pytest.raises(TypeError):
            setattr(event, prop, "foo")
            setattr(event, prop, [42])

    def test_transformation_id(self):
        event = TransformationEvent()
        uri = URI("foo")
        event.transformation_id = "foo"
        assert event.transformation_id == uri
        event.transformation_id = uri
        assert event.transformation_id == uri
        with pytest.raises(TypeError):
            event.transformation_id = 42

    def test_ilmd(self):
        event = TransformationEvent()
        ilmd = {"foo": "bar"}
        event.instance_lot_master_data = ilmd
        assert event.instance_lot_master_data == ilmd
        with pytest.raises(TypeError):
            event.instance_lot_master_data = "foobar"


class TestURI:
    def test_uri_can_split(self):
        uri = URI("urn:epc:id:sgtin:0614141.107346.2018")
        assert uri.uri_str == "urn:epc:id:sgtin:0614141.107346.2018"
        assert uri.prefix == "urn:epc:id"
        assert uri.scheme == "sgtin"
        assert uri.value == "0614141.107346.2018"

    def test_uri_cannot_split(self):
        uri = URI("foo")
        assert uri.uri_str == "foo"
        with pytest.raises(ValueError):
            getattr(uri, "prefix")
            getattr(uri, "scheme")
            getattr(uri, "value")


class TestQuantityElement:
    def test_epc_class(self):
        qe = QuantityElement()
        qe.epc_class = "foo"
        uri = URI("foo")
        assert qe.epc_class == uri
        qe.epc_class = uri
        assert qe.epc_class == uri
        with pytest.raises(TypeError):
            qe.epc_class = 42

    def test_quantity(self):
        qe = QuantityElement()
        qe.quantity = 7.0
        assert qe.quantity == 7.0
        qe.quantity = 7
        assert qe.quantity == 7.0
        qe.quantity = "7.0"
        assert qe.quantity == 7.0
        qe.quantity = "7"
        assert qe.quantity == 7.0
        with pytest.raises(TypeError):
            qe.quantity = "foo"

    def test_uom(self):
        qe = QuantityElement()
        qe.uom = "KG"
        assert qe.uom == "KG"
