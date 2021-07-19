import pytest
from uuid import uuid4
from datetime import datetime, timezone, timedelta
from dateutil import tz

import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from epcis_event import EPCISEvent, ObjectEvent, URI


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
