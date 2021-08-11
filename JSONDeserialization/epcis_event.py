import datetime
import re
from typing import Type
from dateutil import tz, parser
from uuid import UUID


class URI:
    """Provides a class for URI objects as defined in [EPCIS1.2, Section 6.4]

    Attributes:
        uri_str : str
            string representation of the URI.

    GS1 URI Syntax:
        "urn" : <Namespace Identifier> : <Namespace Specfic String> : <Scheme> : <Value>
        examples:
            "urn:epc:id:sgtin:0614141.107346.2018"
            "urn:epcglobal:cbv:bizstep:receiving"
    """

    def __init__(self, uri_str: str):
        """Creates a new URI instance from the given string"""
        self._uri_str: str = uri_str
        self._split_uri: "list[str]" = []
        self._is_split: bool = False
        if re.search("[a-z]+:[a-z]+:[a-z]+:[a-z]+:\S+", self._uri_str):
            self._split_uri = self.uri_str.split(":")
            self._is_split = True

    def __repr__(self) -> str:
        rep = "URI(" + self._uri_str + ")"
        return rep

    def __str__(self) -> str:
        return self._uri_str

    def __eq__(self, other) -> bool:
        try:
            return str(self) == str(other)
        except:
            return False

    @property
    def uri_str(self) -> str:
        return self._uri_str

    @uri_str.setter
    def uri_str(self, value: str) -> None:
        if not isinstance(value, str):
            value = str(value)
        self._uri_str = value

    @property
    def prefix(self) -> str:
        """returns the URI's prefix"""
        if self._is_split:
            return "{}:{}:{}".format(
                self._split_uri[0], self._split_uri[1], self._split_uri[2]
            )
        else:
            raise ValueError("URI does not fit the format needed to find prefix.")

    @property
    def scheme(self) -> str:
        """returns the URI's scheme"""
        if self._is_split:
            return self._split_uri[3]
        else:
            raise ValueError("URI does not fit the format needed to find scheme.")

    @property
    def value(self) -> str:
        """returns the value stored in the URI"""
        if self._is_split:
            return self._split_uri[4]
        else:
            raise ValueError("URI does not fit the format needed to find value.")


class QuantityElement:
    """Provides a class for the QuantityElement structure defined in [EPCIS1.2, Section 7.3.3.3]

    Attributes:
        epc_class : URI
            The identifier for the class to which the specified quantity of objects belongs.
        quantity : float
            How many or how much of the specified EPCClass is denoted by this QuantityElement.
        uom : str
            The unit of measure the quantity is to be interpreted as.
    """

    def __init__(self, epc: URI = URI(""), quant: float = 0, unit: str = ""):
        """Creates a new QuantityElement instance"""
        self.epc_class: URI = epc
        self.quantity: float = quant
        self.uom: str = unit

    def __repr__(self) -> str:
        return (
            "QuantityElement("
            + str(self.epc_class)
            + ", "
            + str(self.quantity)
            + ", "
            + self.uom
            + ")"
        )

    def __eq__(self, other) -> bool:
        try:
            return str(self) == str(other)
        except:
            return False

    @property
    def epc_class(self) -> URI:
        return self._epc_class

    @epc_class.setter
    def epc_class(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        if not isinstance(value, URI):
            raise TypeError("Invalid data type. Must be a URI or string.")
        self._epc_class = value

    @property
    def quantity(self) -> float:
        return self._quantity

    @quantity.setter
    def quantity(self, value: float):
        if not isinstance(value, float):
            try:
                value = float(value)
            except:
                raise TypeError(
                    "Invalid data type. Must be a float or convertible to a float."
                )
        self._quantity = value

    @property
    def uom(self) -> str:
        return self._uom

    @uom.setter
    def uom(self, value: str):
        if not isinstance(value, str):
            value = str(value)
        self._uom = value


class EPCISEvent:
    """Provides a common base type for all EPCIS events [EPCIS1.2, Section 7.4.1]

    Attributes:
        event_id : UUID
            The unique identifier of the event.
        event_time : datetime.datetime
            The date and time that the event occurred.
        event_timezone_offset : datetime.timezone
            The timezone offset in effect at the time and place the event occurred.
        extensions : list[dict]
            A place to add fields not in the EPCIS1.2 standard
    """

    def __init__(self):
        """Creates a new EPCISEvent instance with empty, but type-hinted, attributes"""
        self._event_id = UUID("00000000000000000000000000000000")
        self._event_time = datetime.datetime(1, 1, 1)
        self._event_timezone_offset = datetime.timezone(datetime.timedelta(hours=0))
        self._extensions: "list[dict]" = []

    def __repr__(self) -> str:
        """EPCISEvent representation"""
        rep = self.__class__.__name__ + "(\n"
        for attr in self.__dict__.keys():
            rep = rep + attr + " : " + str(getattr(self, attr)) + "\n"
        return rep + ")"

    @property
    def event_id(self) -> UUID:
        """event_id"""
        return self._event_id

    @event_id.setter
    def event_id(self, value: UUID):
        if isinstance(value, str):
            try:
                value = UUID(value)
            except:
                raise TypeError("Invalid string format.  Must be a UUID.")

        elif not isinstance(value, UUID):
            raise TypeError(
                "Invalid data type.  Must be a UUID or a string representation of a UUID."
            )

        self._event_id = value

    @property
    def event_time(self) -> datetime.datetime:
        """event_time"""
        return self._event_time

    @event_time.setter
    def event_time(self, value: datetime.datetime):
        if isinstance(value, str):
            try:
                value = datetime.datetime.fromisoformat(value)
            except:
                try:
                    value = parser.parse(value)
                except:
                    raise TypeError("Invalid string format. Must be a date.")
        if isinstance(value, datetime.datetime):
            utc = tz.tzutc()
            value = value.astimezone(utc)
        else:
            raise TypeError(
                "Invalid data type. Must be a datetime or a string representation of a datetime."
            )
        self._event_time = value

    @property
    def event_time_local(self) -> datetime.datetime:
        return self._event_time.astimezone(self.event_timezone_offset)

    @property
    def event_timezone_offset(self) -> datetime.timezone:
        """event_timezone_offset"""
        return self._event_timezone_offset

    @event_timezone_offset.setter
    def event_timezone_offset(self, value: datetime.timezone):
        if isinstance(value, str):
            if re.search("[+-][0-1][0-9]:[0-5][0-9]", value) is not None:
                offset = value.split(":")
                # computes hours as a float by taking (|hour| + minutes/60) * -1 or +1 depending on the offset's sign
                value = datetime.timezone(
                    datetime.timedelta(
                        hours=(abs(float(offset[0])) + (float(offset[1]) / 60))
                        * (abs(float(offset[0])) / float(offset[0]))
                    )
                )
            else:
                raise TypeError(
                    "Invalid string. Must be a timezone offset in the form '[+-][0-1][0-9]:[0-5][0-9]'."
                )
        if isinstance(value, float) or isinstance(value, int):
            try:
                value = datetime.timezone(datetime.timedelta(hours=value))
            except:
                raise TypeError("Invalid number. Must be between -24 and 24.")
        if not isinstance(value, datetime.timezone):
            raise TypeError(
                "Invalid data type. Must be a datetime.timezone or a float, int, or string representation of a datetime.timezone."
            )
        self._event_timezone_offset = value

    @property
    def extensions(self) -> "list[dict]":
        return self._extensions

    @extensions.setter
    def extensions(self, value: dict):
        """Append dict to list of extensions."""
        if isinstance(value, dict):
            self._extensions.append(value)
        else:
            raise TypeError("Invalid data type. Must be a list.")

    def delete_extensions(self):
        """Delete the list of extensions."""
        self._extensions = []


class CommonEvent(EPCISEvent):
    """A class containing attributes not in EPCISEvent, but still shared by most events types.

    Attributes:
        action : str
            How this event relates to the lifecycle of the EPCs named in this event.
        business_step : URI
            The business steps of which this event took place.
        disposition : URI
            The business condition of the objects associated with the EPCs.
        read_point : URI
            The read point at which the event took place.
        business_location : URI
            The business location where the objects associated with the EPCs can be found.
        business_transaction_list : list[dict]
            List of business transactions that define the context of this event.
        source_list : list[dict]
            List of source elements providing context about the originating endpoint of a business
            transfer of which this event is a part.
        destination_list : list[dict]
            List of source elements providing context about the terminating endpoint of a business
            transfer of which this event is a part.
    """

    def __init__(self):
        super().__init__()
        self._action: str = ""
        self._business_step: URI = URI("")
        self._disposition: URI = URI("")
        self._read_point: URI = URI("")
        self._business_location: URI = URI("")
        self._business_transaction_list: "list[dict]" = []
        self._source_list: "list[dict]" = []
        self._destination_list: "list[dict]" = []

    @property
    def action(self) -> str:
        """action"""
        return self._action

    @action.setter
    def action(self, value: str):
        if isinstance(value, str):
            self._action = value
        else:
            raise TypeError("Invalid data type. Must be a string")

    @property
    def business_step(self) -> URI:
        """business_step"""
        return self._business_step

    @business_step.setter
    def business_step(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        if not isinstance(value, URI):
            raise TypeError("Invalid type. Must be a URI or a string.")
        self._business_step = value

    @property
    def disposition(self) -> URI:
        """disposition"""
        return self._disposition

    @disposition.setter
    def disposition(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        if not isinstance(value, URI):
            raise TypeError("Invalid type. Must be a URI or a string.")
        self._disposition = value

    @property
    def read_point(self) -> URI:
        """read_point"""
        return self._read_point

    @read_point.setter
    def read_point(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        if not isinstance(value, URI):
            raise TypeError("Invalid type. Must be a URI or a string.")
        self._read_point = value

    @property
    def business_location(self) -> URI:
        """business_location"""
        return self._business_location

    @business_location.setter
    def business_location(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        if not isinstance(value, URI):
            raise TypeError("Invalid type. Must be a URI or a string.")
        self._business_location = value

    @property
    def business_transaction_list(self) -> "list[dict]":
        """business_transaction_list"""
        return self._business_transaction_list

    @business_transaction_list.setter
    def business_transaction_list(self, value: "list[dict]"):
        if isinstance(value, list):
            if len(value) != 0:
                if any(not isinstance(val, dict) for val in value):
                    raise TypeError("Invalid list. List items must be dicts.")
        else:
            raise TypeError("Invalid data type. Must be a list of dicts.")
        self._business_transaction_list = value

    @property
    def source_list(self) -> "list[dict]":
        """source_list"""
        return self._source_list

    @source_list.setter
    def source_list(self, value: "list[dict]"):
        if isinstance(value, list):
            if len(value) != 0:
                if any(not isinstance(val, dict) for val in value):
                    raise TypeError("Invalid list. List items must be dicts.")
        else:
            raise TypeError("Invalid data type. Must be a list of dicts.")
        self._source_list = value

    @property
    def destination_list(self) -> "list[dict]":
        """destination_list"""
        return self._destination_list

    @destination_list.setter
    def destination_list(self, value: "list[dict]"):
        if isinstance(value, list):
            if len(value) > 0:
                if any(not isinstance(val, dict) for val in value):
                    raise TypeError("Invalid list. List items must be dicts.")
        else:
            raise TypeError("Invalid data type. Must be a list of dicts.")
        self._destination_list = value


class ObjectEvent(CommonEvent):
    """Provides a class for EPCIS ObjectEvents [EPCIS1.2, Section 7.4.2]

    Attributes:
        epc_list : list[URI]
            List of one or more EPCs naming specific objects to which the event pertained.
        quantity_list : list[QuantityElement]
            List of one or more QuantifyingElements identfiying objects to which the event pertained.
        instance_lot_master_data : dict
            Instance/lot master data that describes the objects created during this event.

    """

    def __init__(self):
        super().__init__()
        self._epc_list: "list[URI]" = []
        self._quantity_list: "list[QuantityElement]" = []
        self._instance_lot_master_data: dict = {}

    @property
    def epc_list(self) -> "list[URI]":
        """epc_list"""
        return self._epc_list

    @epc_list.setter
    def epc_list(self, value: "list[URI]"):
        if isinstance(value, list):
            if len(value) > 0:
                new_values = []
                for epc in value:
                    if isinstance(epc, str):
                        new_values.append(URI(epc))
                if len(value) == len(new_values):
                    value = new_values
                if any([not isinstance(val, URI) for val in value]):
                    raise TypeError(
                        "Invalid data type. List must contain URIs or string representations of URIs."
                    )
        else:
            raise TypeError(
                "Invalid data type. Must be list of URIs or string representations of URIs."
            )
        self._epc_list = value

    @property
    def quantity_list(self) -> "list[QuantityElement]":
        """quantity_list"""
        return self._quantity_list

    @quantity_list.setter
    def quantity_list(self, value: "list[QuantityElement]"):
        if isinstance(value, list):
            if len(value) > 0:
                new_vals = []
                for val in value:
                    if isinstance(val, dict) and "epcClass" in val.keys():
                        qe = QuantityElement()
                        for a_k in [
                            ("epc_class", "epcClass"),
                            ("quantity", "quantity"),
                            ("uom", "uom"),
                        ]:
                            if a_k[1] in val.keys():
                                setattr(qe, a_k[0], val[a_k[1]])
                        new_vals.append(qe)
                if len(new_vals) == len(value):
                    value = new_vals
                if any(not isinstance(val, QuantityElement) for val in value):
                    raise TypeError(
                        "Invalid data type. List items must be QuantityElements or dict representations of QuantityElements."
                    )
        else:
            raise TypeError(
                "Invalid data type. Must be list of QuantityElements or dict representations of QuantityElements."
            )
        self._quantity_list = value

    @property
    def instance_lot_master_data(self) -> dict:
        """instance_lot_master_data"""
        return self._instance_lot_master_data

    @instance_lot_master_data.setter
    def instance_lot_master_data(self, value: dict):
        if not isinstance(value, dict):
            raise TypeError("Invalid data type. Must be a dict.")
        self._instance_lot_master_data = value


class AggregationEvent(CommonEvent):
    """Provides a class for EPCIS AggregationEvents [EPCIS1.2, Section 7.4.3]

    Attributes:
        parent_id : URI
            Identifier off the parent of the association.
        child_epc_list : list[URI]
            List of EPCs of contained objects identified by instance-level identifiers.
        child_quantity_list : list[QuantityElement]
            List of QuantityElements identifying contained objects.
    """

    def __init__(self):
        super().__init__()
        self._parent_id: URI = URI("")
        self._child_epc_list: "list[URI]" = []
        self._child_quantity_list: "list[QuantityElement]" = []

    @property
    def parent_id(self) -> URI:
        """parent_id"""
        return self._parent_id

    @parent_id.setter
    def parent_id(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        if not isinstance(value, URI):
            raise TypeError("Invalid data type. Must be a URI or a string.")
        self._parent_id = value

    @property
    def child_epc_list(self) -> "list[URI]":
        """child_epc_list"""
        return self._child_epc_list

    @child_epc_list.setter
    def child_epc_list(self, value: "list[URI]"):
        if isinstance(value, list):
            if len(value) > 0:
                new_values = []
                for epc in value:
                    if isinstance(epc, str):
                        new_values.append(URI(epc))
                if len(value) == len(new_values):
                    value = new_values
                if any([not isinstance(val, URI) for val in value]):
                    raise TypeError(
                        "Invalid data type. List must contain URIs or string representations of URIs."
                    )
        else:
            raise TypeError(
                "Invalid data type. Must be list of URIs or string representations of URIs."
            )
        self._child_epc_list = value

    @property
    def child_quantity_list(self) -> "list[QuantityElement]":
        """quantity_list"""
        return self._child_quantity_list

    @child_quantity_list.setter
    def child_quantity_list(self, value: "list[QuantityElement]"):
        if isinstance(value, list):
            if len(value) > 0:
                new_vals = []
                for val in value:
                    if isinstance(val, dict) and "epcClass" in val.keys():
                        qe = QuantityElement()
                        for a_k in [
                            ("epc_class", "epcClass"),
                            ("quantity", "quantity"),
                            ("uom", "uom"),
                        ]:
                            if a_k[1] in val.keys():
                                setattr(qe, a_k[0], val[a_k[1]])
                        new_vals.append(qe)
                if len(new_vals) == len(value):
                    value = new_vals
                if any(not isinstance(val, QuantityElement) for val in value):
                    raise TypeError(
                        "Invalid list. List items must be QuantityElements or dict representations of QuantityElements."
                    )
        else:
            raise TypeError(
                "Invalid data type. Must be list of QuantityElements or dict representations of QuantityElements."
            )
        self._child_quantity_list = value


class QuantityEvent(EPCISEvent):
    """Provides a class for EPCIS QuantityEvents (DEPRECATED) [EPCIS1.2, Section 7.4.4]

    Attributes:
        epc_class : URI
            Identifier specficying the object class to which the event pertains.
        quantity : float
            Quantity of object within class described by this event.
        business_step : URI
            The business steps of which this event took place.
        disposition : URI
            The business condition of the objects associated with the EPCs.
        read_point : URI
            The read point at which the event took place.
        business_location : URI
            The business location where the objects associated with the EPCs can be found.
        business_transaction_list : list[dict]
            List of business transactions that define the context of this event.
    """

    def __init__(self):
        super().__init__()
        self._epc_class: URI = URI("")
        self._quantity: float = 0
        self._business_step: URI = URI("")
        self._disposition: URI = URI("")
        self._read_point: URI = URI("")
        self._business_location: URI = URI("")
        self._business_transaction_list: "list[dict]" = []

    @property
    def epc_class(self) -> URI:
        """epc_class"""
        return self._epc_class

    @epc_class.setter
    def epc_class(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        if not isinstance(value, URI):
            raise TypeError(
                "Invalid data type. Must be URI or string representation of URI."
            )
        self._epc_class = value

    @property
    def quantity(self) -> int:
        """quantity"""
        return self._quantity

    @quantity.setter
    def quantity(self, value: float):
        if not isinstance(value, float):
            try:
                value = float(value)
            except:
                raise TypeError(
                    "Invalid data type. Must be a float or convertible to a float."
                )
        self._quantity = value

    @property
    def action(self) -> str:
        """action"""
        return self._action

    @action.setter
    def action(self, value: str):
        if isinstance(value, str):
            self._action = value
        else:
            raise TypeError("Invalid data type. Must be a string")

    @property
    def business_step(self) -> URI:
        """business_step"""
        return self._business_step

    @business_step.setter
    def business_step(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        if not isinstance(value, URI):
            raise TypeError("Invalid type. Must be a URI or a string.")
        self._business_step = value

    @property
    def disposition(self) -> URI:
        """disposition"""
        return self._disposition

    @disposition.setter
    def disposition(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        if not isinstance(value, URI):
            raise TypeError("Invalid type. Must be a URI or a string.")
        self._disposition = value

    @property
    def read_point(self) -> URI:
        """read_point"""
        return self._read_point

    @read_point.setter
    def read_point(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        if not isinstance(value, URI):
            raise TypeError("Invalid type. Must be a URI or a string.")
        self._read_point = value

    @property
    def business_location(self) -> URI:
        """business_location"""
        return self._business_location

    @business_location.setter
    def business_location(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        if not isinstance(value, URI):
            raise TypeError("Invalid type. Must be a URI or a string.")
        self._business_location = value

    @property
    def business_transaction_list(self) -> "list[dict]":
        """business_transaction_list"""
        return self._business_transaction_list

    @business_transaction_list.setter
    def business_transaction_list(self, value: "list[dict]"):
        if isinstance(value, list):
            if len(value) != 0:
                if any(not isinstance(val, dict) for val in value):
                    raise TypeError("Invalid data type. List items must be dicts.")
        else:
            raise TypeError("Invalid data type. Must be a list of dicts.")
        self._business_transaction_list = value


class TransactionEvent(CommonEvent):
    """Provides a class for EPCIS TransactionEvents [EPCIS1.2, Section 7.4.5]

    Attributes:
        parent_id : URI
            Identifier off the parent of the objects given in epc_list or quantity_list.
        epc_list : list[URI]
            List of one or more EPCs naming specific objects to which the event pertained.
        quantity_list : list[QuantityElement]
            List of one or more QuantifyingElements identfiying objects to which the event pertained.

    """

    def __init__(self):
        super().__init__()
        self._parent_id: URI = URI("")
        self._epc_list: "list[URI]" = []
        self._quantity_list: "list[QuantityElement]" = []

    @property
    def parent_id(self) -> URI:
        """parent_id"""
        return self._parent_id

    @parent_id.setter
    def parent_id(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        if not isinstance(value, URI):
            raise TypeError(
                "Invalid data type. Must be a URI or string representation of a URI."
            )
        self._parent_id = value

    @property
    def epc_list(self) -> "list[URI]":
        """epc_list"""
        return self._epc_list

    @epc_list.setter
    def epc_list(self, value: "list[URI]"):
        if isinstance(value, list):
            if len(value) > 0:
                new_values = []
                for epc in value:
                    if isinstance(epc, str):
                        new_values.append(URI(epc))
                if len(value) == len(new_values):
                    value = new_values
                if any([not isinstance(val, URI) for val in value]):
                    raise TypeError(
                        "Invalid data type. List must contain URIs or string representations of URIs."
                    )
        else:
            raise TypeError(
                "Invalid data type. Must be list of URIs or string representations of URIs."
            )
        self._epc_list = value

    @property
    def quantity_list(self) -> "list[QuantityElement]":
        """quantity_list"""
        return self._quantity_list

    @quantity_list.setter
    def quantity_list(self, value: "list[QuantityElement]"):
        if isinstance(value, list):
            if len(value) > 0:
                new_vals = []
                for val in value:
                    if isinstance(val, dict) and "epcClass" in val.keys():
                        qe = QuantityElement()
                        for a_k in [
                            ("epc_class", "epcClass"),
                            ("quantity", "quantity"),
                            ("uom", "uom"),
                        ]:
                            if a_k[1] in val.keys():
                                setattr(qe, a_k[0], val[a_k[1]])
                        new_vals.append(qe)
                if len(new_vals) == len(value):
                    value = new_vals
                if any(not isinstance(val, QuantityElement) for val in value):
                    raise TypeError(
                        "Invalid data type. List items must be QuantityElements or dict representations of QuantityElements."
                    )
        else:
            raise TypeError(
                "Invalid data type. Must be list of QuantityElements or dict representations of QuantityElements."
            )
        self._quantity_list = value


class TransformationEvent(CommonEvent):
    """Provides a class for EPCIS TransformationEvents [EPCIS1.2, Section 7.4.6]

    Attributes:
        input_epc_list : list[URI]
            List of EPCs identfying objects that were inputs to the transformation.
        input_quantity_list : list[QuantityElement]
            List of QuantityElements identfying objects that were inputs to the transformation.
        output_epc_list : list[URI]
            List of EPCs identfying objects that were outputs from the transformation.
        output_quantity_list : list[QuantityElement]
            List of QuantityElements identfying objects that were outputs from the transformation.
        transformation_id : URI
            Unique identifier linking this event to other TransformationEvents sharing inputs.
        instance_lot_master_data : dict
            Instance/Lot master data that describes the output objects created during this event.

    """

    def __init__(self):
        super().__init__()
        self._input_epc_list: "list[URI]" = []
        self._input_quantity_list: "list[QuantityElement]" = []
        self._output_epc_list: "list[URI]" = []
        self._output_quantity_list: "list[QuantityElement]" = []
        self._transformation_id: URI = URI("")
        self._instance_lot_master_data: dict = {}

    @property
    def input_epc_list(self) -> "list[URI]":
        """input_epc_list"""
        return self._input_epc_list

    @input_epc_list.setter
    def input_epc_list(self, value: "list[URI]"):
        if isinstance(value, list):
            if len(value) > 0:
                new_values = []
                for epc in value:
                    if isinstance(epc, str):
                        new_values.append(URI(epc))
                if len(value) == len(new_values):
                    value = new_values
                if any([not isinstance(val, URI) for val in value]):
                    raise TypeError(
                        "Invalid data type. List must contain URIs or string representations of URIs."
                    )
        else:
            raise TypeError(
                "Invalid data type. Must be list of URIs or string representations of URIs."
            )
        self._input_epc_list = value

    @property
    def input_quantity_list(self) -> "list[QuantityElement]":
        """input_quantity_list"""
        return self._input_quantity_list

    @input_quantity_list.setter
    def input_quantity_list(self, value: "list[QuantityElement]"):
        if isinstance(value, list):
            if len(value) > 0:
                new_vals = []
                for val in value:
                    if isinstance(val, dict) and "epcClass" in val.keys():
                        qe = QuantityElement()
                        for a_k in [
                            ("epc_class", "epcClass"),
                            ("quantity", "quantity"),
                            ("uom", "uom"),
                        ]:
                            if a_k[1] in val.keys():
                                setattr(qe, a_k[0], val[a_k[1]])
                        new_vals.append(qe)
                if len(new_vals) == len(value):
                    value = new_vals
                if any(not isinstance(val, QuantityElement) for val in value):
                    raise TypeError(
                        "Invalid data type. List items must be QuantityElements or dict representations of QuantityElements."
                    )
        else:
            raise TypeError(
                "Invalid data type. Must be list of QuantityElements or dict representations of QuantityElements."
            )
        self._input_quantity_list = value

    @property
    def output_epc_list(self) -> "list[URI]":
        """output_epc_list"""
        return self._output_epc_list

    @output_epc_list.setter
    def output_epc_list(self, value: "list[URI]"):
        if isinstance(value, list):
            if len(value) > 0:
                new_values = []
                for epc in value:
                    if isinstance(epc, str):
                        new_values.append(URI(epc))
                if len(value) == len(new_values):
                    value = new_values
                if any([not isinstance(val, URI) for val in value]):
                    raise TypeError(
                        "Invalid data type. List must contain URIs or string representations of URIs."
                    )
        else:
            raise TypeError(
                "Invalid data type. Must be list of URIs or string representations of URIs."
            )
        self._output_epc_list = value

    @property
    def output_quantity_list(self) -> "list[QuantityElement]":
        """output_quantity_list"""
        return self._output_quantity_list

    @output_quantity_list.setter
    def output_quantity_list(self, value: "list[QuantityElement]"):
        if isinstance(value, list):
            if len(value) > 0:
                new_vals = []
                for val in value:
                    if isinstance(val, dict) and "epcClass" in val.keys():
                        qe = QuantityElement()
                        for a_k in [
                            ("epc_class", "epcClass"),
                            ("quantity", "quantity"),
                            ("uom", "uom"),
                        ]:
                            if a_k[1] in val.keys():
                                setattr(qe, a_k[0], val[a_k[1]])
                        new_vals.append(qe)
                if len(new_vals) == len(value):
                    value = new_vals
                if any(not isinstance(val, QuantityElement) for val in value):
                    raise TypeError(
                        "Invalid data type. List items must be QuantityElements or dict representations of QuantityElements."
                    )
        else:
            raise TypeError(
                "Invalid data type. Must be list of QuantityElements or dict representations of QuantityElements."
            )
        self._output_quantity_list = value

    @property
    def transformation_id(self) -> URI:
        """transaction_form_id"""
        return self._transformation_id

    @transformation_id.setter
    def transformation_id(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        if not isinstance(value, URI):
            raise TypeError("Invalid data type. Must be a URI or string.")
        self._transformation_id = value

    @property
    def instance_lot_master_data(self) -> dict:
        """instance_lot_master_data"""
        return self._instance_lot_master_data

    @instance_lot_master_data.setter
    def instance_lot_master_data(self, value: dict):
        if not isinstance(value, dict):
            raise TypeError("Invalid data type. Must be a dict.")
        self._instance_lot_master_data = value
